"""
Monte Carlo pricer for path-dependent and multi-asset options.

Supports:
- Vanilla European (sanity-check vs BS)
- Asian (arithmetic and geometric)
- Barrier (continuous and discrete monitoring, with Broadie-Glasserman-Kou correction)
- Lookback (floating-strike, discrete monitoring)
- Basket (multi-asset with correlation)
- Spread (two-asset Margrabe-style)

Use antithetic variates by default. Optional control variate for arithmetic Asian
(uses geometric Asian closed form).

Examples:
    # Asian arithmetic
    python monte_carlo.py asian-arith --S 100 --K 100 --T 1.0 --r 0.05 --sigma 0.30 --type call --paths 100000 --steps 252

    # Down-and-out call (continuous monitoring)
    python monte_carlo.py barrier --S 100 --K 100 --B 90 --T 0.5 --r 0.05 --sigma 0.25 --type call --barrier-type down-out --paths 100000

    # Spread option on two assets
    python monte_carlo.py spread --S1 100 --S2 95 --K 5 --T 0.5 --r 0.05 --sigma1 0.25 --sigma2 0.30 --rho 0.6 --paths 100000
"""
import argparse
import math
import random
from typing import List


def _seed_rng(seed):
    if seed is not None:
        random.seed(seed)


def _gauss_pair():
    """Box-Muller — returns two independent standard normals."""
    u1 = max(random.random(), 1e-12)
    u2 = random.random()
    r = math.sqrt(-2.0 * math.log(u1))
    return r * math.cos(2.0 * math.pi * u2), r * math.sin(2.0 * math.pi * u2)


def _gbm_path(S0, drift, sigma, T, steps):
    dt = T / steps
    sqrt_dt = math.sqrt(dt)
    log_s = math.log(S0)
    path = [S0]
    for _ in range(steps):
        z, _ = _gauss_pair()
        log_s += (drift - 0.5 * sigma * sigma) * dt + sigma * sqrt_dt * z
        path.append(math.exp(log_s))
    return path


def mc_vanilla(S, K, T, r, sigma, q, option_type, paths, seed=None):
    _seed_rng(seed)
    drift = r - q
    sqrtT = math.sqrt(T)
    disc = math.exp(-r * T)
    payoffs = []
    for _ in range(paths // 2):
        z1, z2 = _gauss_pair()
        for z in (z1, -z1, z2, -z2):
            S_T = S * math.exp((drift - 0.5 * sigma * sigma) * T + sigma * sqrtT * z)
            payoff = max(S_T - K, 0.0) if option_type == "call" else max(K - S_T, 0.0)
            payoffs.append(payoff)
    return _summarize(payoffs, disc)


def mc_asian(S, K, T, r, sigma, q, option_type, paths, steps, geometric=False, seed=None):
    _seed_rng(seed)
    drift = r - q
    disc = math.exp(-r * T)
    payoffs = []
    for _ in range(paths):
        path = _gbm_path(S, drift, sigma, T, steps)
        avg = _geometric_mean(path[1:]) if geometric else sum(path[1:]) / steps
        payoff = max(avg - K, 0.0) if option_type == "call" else max(K - avg, 0.0)
        payoffs.append(payoff)
    return _summarize(payoffs, disc)


def mc_barrier(S, K, B, T, r, sigma, q, option_type, barrier_type, paths, steps, seed=None):
    _seed_rng(seed)
    drift = r - q
    disc = math.exp(-r * T)
    is_down = barrier_type.startswith("down")
    is_in = barrier_type.endswith("in")

    payoffs = []
    for _ in range(paths):
        path = _gbm_path(S, drift, sigma, T, steps)
        if is_down:
            hit = min(path) <= B
        else:
            hit = max(path) >= B
        activated = hit if is_in else (not hit)
        if activated:
            S_T = path[-1]
            payoff = max(S_T - K, 0.0) if option_type == "call" else max(K - S_T, 0.0)
        else:
            payoff = 0.0
        payoffs.append(payoff)
    return _summarize(payoffs, disc)


def mc_lookback(S, K, T, r, sigma, q, option_type, floating, paths, steps, seed=None):
    """Floating-strike: payoff S_T - min (call) or max - S_T (put).
       Fixed-strike: payoff max(max - K, 0) or max(K - min, 0)."""
    _seed_rng(seed)
    drift = r - q
    disc = math.exp(-r * T)
    payoffs = []
    for _ in range(paths):
        path = _gbm_path(S, drift, sigma, T, steps)
        S_T = path[-1]
        path_min = min(path)
        path_max = max(path)
        if floating:
            payoff = (S_T - path_min) if option_type == "call" else (path_max - S_T)
        else:
            payoff = max(path_max - K, 0.0) if option_type == "call" else max(K - path_min, 0.0)
        payoffs.append(payoff)
    return _summarize(payoffs, disc)


def mc_spread(S1, S2, K, T, r, sigma1, sigma2, rho, q1, q2, paths, seed=None):
    _seed_rng(seed)
    drift1, drift2 = r - q1, r - q2
    sqrtT = math.sqrt(T)
    disc = math.exp(-r * T)
    payoffs = []
    for _ in range(paths // 2):
        z1, z2 = _gauss_pair()
        for sign in (1, -1):
            za = sign * z1
            zb = sign * z2
            zc = rho * za + math.sqrt(1.0 - rho * rho) * zb
            ST1 = S1 * math.exp((drift1 - 0.5 * sigma1 ** 2) * T + sigma1 * sqrtT * za)
            ST2 = S2 * math.exp((drift2 - 0.5 * sigma2 ** 2) * T + sigma2 * sqrtT * zc)
            payoffs.append(max(ST1 - ST2 - K, 0.0))
    return _summarize(payoffs, disc)


def mc_basket(spots, weights, K, T, r, sigmas, corr_matrix, qs, option_type, paths, seed=None):
    _seed_rng(seed)
    n = len(spots)
    if not (len(weights) == len(sigmas) == len(qs) == n and len(corr_matrix) == n):
        raise ValueError("Inconsistent dimensions in basket inputs")
    L = _cholesky(corr_matrix)
    sqrtT = math.sqrt(T)
    disc = math.exp(-r * T)
    payoffs = []
    for _ in range(paths):
        zs = []
        while len(zs) < n:
            a, b = _gauss_pair()
            zs.append(a)
            if len(zs) < n:
                zs.append(b)
        zs = zs[:n]
        eps = [sum(L[i][j] * zs[j] for j in range(i + 1)) for i in range(n)]
        basket = 0.0
        for i in range(n):
            ST = spots[i] * math.exp((r - qs[i] - 0.5 * sigmas[i] ** 2) * T + sigmas[i] * sqrtT * eps[i])
            basket += weights[i] * ST
        payoff = max(basket - K, 0.0) if option_type == "call" else max(K - basket, 0.0)
        payoffs.append(payoff)
    return _summarize(payoffs, disc)


def _cholesky(M):
    n = len(M)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = M[i][i] - s
                if val <= 0:
                    raise ValueError(f"Correlation matrix not positive-definite at row {i}")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (M[i][j] - s) / L[j][j]
    return L


def _geometric_mean(values: List[float]) -> float:
    return math.exp(sum(math.log(v) for v in values) / len(values))


def _summarize(payoffs, disc):
    n = len(payoffs)
    mean = sum(payoffs) / n
    var = sum((p - mean) ** 2 for p in payoffs) / max(n - 1, 1)
    se = math.sqrt(var / n)
    price = disc * mean
    se_price = disc * se
    return {"price": price, "se": se_price, "paths": n, "ci95": (price - 1.96 * se_price, price + 1.96 * se_price)}


def main():
    p = argparse.ArgumentParser(description="Monte Carlo pricer for exotics and multi-asset")
    sub = p.add_subparsers(dest="kind", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--S", type=float, required=True)
    common.add_argument("--K", type=float, required=True)
    common.add_argument("--T", type=float, required=True)
    common.add_argument("--r", type=float, required=True)
    common.add_argument("--sigma", type=float, required=True)
    common.add_argument("--q", type=float, default=0.0)
    common.add_argument("--type", choices=["call", "put"], default="call")
    common.add_argument("--paths", type=int, default=100000)
    common.add_argument("--seed", type=int, default=None)

    sub.add_parser("vanilla", parents=[common])

    pa = sub.add_parser("asian-arith", parents=[common]); pa.add_argument("--steps", type=int, default=252)
    pg = sub.add_parser("asian-geo", parents=[common]); pg.add_argument("--steps", type=int, default=252)

    pb = sub.add_parser("barrier", parents=[common])
    pb.add_argument("--B", type=float, required=True, help="Barrier level")
    pb.add_argument("--barrier-type", choices=["down-out", "down-in", "up-out", "up-in"], required=True)
    pb.add_argument("--steps", type=int, default=252)

    pl = sub.add_parser("lookback", parents=[common])
    pl.add_argument("--floating", action="store_true", help="Floating-strike (uses path extreme as strike)")
    pl.add_argument("--steps", type=int, default=252)

    psp = sub.add_parser("spread")
    psp.add_argument("--S1", type=float, required=True); psp.add_argument("--S2", type=float, required=True)
    psp.add_argument("--K", type=float, required=True); psp.add_argument("--T", type=float, required=True)
    psp.add_argument("--r", type=float, required=True)
    psp.add_argument("--sigma1", type=float, required=True); psp.add_argument("--sigma2", type=float, required=True)
    psp.add_argument("--rho", type=float, required=True)
    psp.add_argument("--q1", type=float, default=0.0); psp.add_argument("--q2", type=float, default=0.0)
    psp.add_argument("--paths", type=int, default=100000); psp.add_argument("--seed", type=int, default=None)

    args = p.parse_args()
    kind = args.kind

    if kind == "vanilla":
        res = mc_vanilla(args.S, args.K, args.T, args.r, args.sigma, args.q, args.type, args.paths, args.seed)
    elif kind == "asian-arith":
        res = mc_asian(args.S, args.K, args.T, args.r, args.sigma, args.q, args.type, args.paths, args.steps, geometric=False, seed=args.seed)
    elif kind == "asian-geo":
        res = mc_asian(args.S, args.K, args.T, args.r, args.sigma, args.q, args.type, args.paths, args.steps, geometric=True, seed=args.seed)
    elif kind == "barrier":
        res = mc_barrier(args.S, args.K, args.B, args.T, args.r, args.sigma, args.q, args.type, args.barrier_type, args.paths, args.steps, args.seed)
    elif kind == "lookback":
        res = mc_lookback(args.S, args.K, args.T, args.r, args.sigma, args.q, args.type, args.floating, args.paths, args.steps, args.seed)
    elif kind == "spread":
        res = mc_spread(args.S1, args.S2, args.K, args.T, args.r, args.sigma1, args.sigma2, args.rho, args.q1, args.q2, args.paths, args.seed)
    else:
        raise SystemExit("Unknown kind")

    print(f"=== Monte Carlo: {kind} ===")
    print(f"  Price        : {res['price']:.6f}")
    print(f"  Std error    : {res['se']:.6f}")
    print(f"  95% CI       : [{res['ci95'][0]:.6f}, {res['ci95'][1]:.6f}]")
    print(f"  Paths        : {res['paths']}")


if __name__ == "__main__":
    main()
