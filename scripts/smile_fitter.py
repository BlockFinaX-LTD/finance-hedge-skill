"""
Volatility smile / surface fitter.

Two parametrizations supported:

  1. SVI (Stochastic Volatility Inspired) — Gatheral's raw form:
        w(k) = a + b * (rho*(k-m) + sqrt((k-m)^2 + sigma^2))
     where w = total implied variance (sigma_imp^2 * T), k = log-moneyness ln(K/F).
     Industry standard for equity index surfaces. Arbitrage-free under constraints.

  2. SABR — Hagan et al. asymptotic for forward dynamics:
        sigma_imp ≈ alpha / (F*K)^((1-beta)/2) * (1 + ...corrections...)
     Industry standard for rates and FX. Four parameters: alpha, beta, rho, nu.

Fitting is least-squares on log-moneyness grid. Input: list of (strike, market_vol)
points for a single tenor. Output: fitted params + smooth curve.

Per Taleb Ch 9 + Ch 15: the smile encodes vol-of-vol and spot-vol correlation.
The fitted parameters have direct economic interpretation:
  - SVI a, b      → ATM vol level and overall wing width
  - SVI rho       → spot-vol correlation (drives skew)
  - SVI sigma, m  → smile curvature and center
  - SABR alpha    → ATM vol (when beta=1)
  - SABR beta     → backbone (0=normal, 1=lognormal, 0.5=CIR-like)
  - SABR rho      → spot-vol correlation (skew)
  - SABR nu       → vol-of-vol (smile curvature)

Usage:
    python smile_fitter.py svi --F 100 --T 0.5 --strikes 80,90,100,110,120 --vols 0.30,0.22,0.18,0.22,0.30
    python smile_fitter.py sabr --F 100 --T 0.5 --strikes 80,90,100,110,120 --vols 0.30,0.22,0.18,0.22,0.30 --beta 0.5
"""
import argparse
import math
from typing import List, Tuple


def _nelder_mead(f, x0, max_iter=2000, tol=1e-8):
    """Lightweight Nelder-Mead without numpy. Good enough for 2-5 dim smile fitting."""
    n = len(x0)
    alpha, gamma, rho_n, sigma_n = 1.0, 2.0, 0.5, 0.5
    simplex = [list(x0)]
    for i in range(n):
        point = list(x0)
        point[i] = point[i] + (0.05 if point[i] != 0 else 0.05)
        simplex.append(point)
    fvals = [f(p) for p in simplex]

    for _ in range(max_iter):
        order = sorted(range(n + 1), key=lambda i: fvals[i])
        simplex = [simplex[i] for i in order]
        fvals = [fvals[i] for i in order]
        spread = max(fvals) - min(fvals)
        if spread < tol:
            break

        centroid = [sum(simplex[i][j] for i in range(n)) / n for j in range(n)]
        worst = simplex[-1]

        xr = [centroid[j] + alpha * (centroid[j] - worst[j]) for j in range(n)]
        fr = f(xr)
        if fvals[0] <= fr < fvals[-2]:
            simplex[-1] = xr; fvals[-1] = fr; continue

        if fr < fvals[0]:
            xe = [centroid[j] + gamma * (xr[j] - centroid[j]) for j in range(n)]
            fe = f(xe)
            simplex[-1] = xe if fe < fr else xr
            fvals[-1] = fe if fe < fr else fr
            continue

        xc = [centroid[j] + rho_n * (worst[j] - centroid[j]) for j in range(n)]
        fc = f(xc)
        if fc < fvals[-1]:
            simplex[-1] = xc; fvals[-1] = fc; continue

        best = simplex[0]
        simplex = [best] + [
            [best[j] + sigma_n * (simplex[i][j] - best[j]) for j in range(n)] for i in range(1, n + 1)
        ]
        fvals = [f(p) for p in simplex]

    return simplex[0], fvals[0]


# -----------------------------------------------------------------------------
# SVI raw parametrization
# -----------------------------------------------------------------------------

def svi_total_variance(k, a, b, rho, m, sigma):
    """w(k) = a + b * (rho*(k-m) + sqrt((k-m)^2 + sigma^2))."""
    return a + b * (rho * (k - m) + math.sqrt((k - m) ** 2 + sigma ** 2))


def svi_implied_vol(K, F, T, params):
    a, b, rho, m, sigma = params
    k = math.log(K / F)
    w = svi_total_variance(k, a, b, rho, m, sigma)
    if w <= 0 or T <= 0:
        return float("nan")
    return math.sqrt(w / T)


def fit_svi(strikes: List[float], vols: List[float], F: float, T: float):
    """Fit SVI raw params to a list of (strike, market_vol) at single T."""
    targets = [(math.log(K / F), v * v * T) for K, v in zip(strikes, vols)]

    def loss(params):
        a, b, rho, m, sigma = params
        if b < 0 or sigma <= 0 or abs(rho) >= 1.0:
            return 1e12
        return sum((svi_total_variance(k, a, b, rho, m, sigma) - w_mkt) ** 2 for k, w_mkt in targets)

    atm_var = (sum(v for v in vols) / len(vols)) ** 2 * T
    x0 = [0.5 * atm_var, atm_var, -0.3, 0.0, 0.1]
    best, fbest = _nelder_mead(loss, x0)
    return {"a": best[0], "b": best[1], "rho": best[2], "m": best[3], "sigma": best[4], "rss": fbest}


# -----------------------------------------------------------------------------
# SABR (Hagan 2002 asymptotic)
# -----------------------------------------------------------------------------

def sabr_implied_vol(K, F, T, alpha, beta, rho, nu):
    """Hagan et al. (2002) lognormal implied vol from SABR. Handles ATM case separately."""
    if alpha <= 0 or nu < 0 or abs(rho) >= 1 or beta < 0 or beta > 1:
        return float("nan")
    if abs(F - K) < 1e-12:
        FK = F ** (1.0 - beta)
        term1 = alpha / FK
        term2 = (
            ((1 - beta) ** 2 / 24.0) * alpha ** 2 / FK ** 2
            + 0.25 * rho * beta * nu * alpha / FK
            + (2 - 3 * rho ** 2) / 24.0 * nu ** 2
        )
        return term1 * (1.0 + term2 * T)

    log_FK = math.log(F / K)
    z = (nu / alpha) * (F * K) ** ((1 - beta) / 2.0) * log_FK
    x_z = math.log((math.sqrt(1 - 2 * rho * z + z * z) + z - rho) / (1 - rho))
    if abs(x_z) < 1e-14:
        x_z = 1e-14

    pre = (F * K) ** ((1 - beta) / 2.0)
    denom = pre * (
        1.0
        + ((1 - beta) ** 2 / 24.0) * log_FK ** 2
        + ((1 - beta) ** 4 / 1920.0) * log_FK ** 4
    )
    factor = (
        1.0
        + (
            ((1 - beta) ** 2 / 24.0) * alpha ** 2 / pre ** 2
            + 0.25 * rho * beta * nu * alpha / pre
            + (2 - 3 * rho ** 2) / 24.0 * nu ** 2
        ) * T
    )
    return (alpha / denom) * (z / x_z) * factor


def fit_sabr(strikes: List[float], vols: List[float], F: float, T: float, beta: float = 0.5):
    """Fit SABR (alpha, rho, nu) holding beta fixed (standard practice)."""
    def loss(params):
        alpha, rho, nu = params
        if alpha <= 0 or nu < 0 or abs(rho) >= 0.999:
            return 1e12
        s = 0.0
        for K, v in zip(strikes, vols):
            v_model = sabr_implied_vol(K, F, T, alpha, beta, rho, nu)
            if math.isnan(v_model):
                return 1e12
            s += (v_model - v) ** 2
        return s

    atm_vol = sum(vols) / len(vols)
    alpha_init = atm_vol * F ** (1.0 - beta)
    x0 = [alpha_init, -0.3, 0.4]
    best, fbest = _nelder_mead(loss, x0)
    return {"alpha": best[0], "beta": beta, "rho": best[1], "nu": best[2], "rss": fbest}


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def _parse_floats(s: str) -> List[float]:
    return [float(x.strip()) for x in s.split(",")]


def main():
    p = argparse.ArgumentParser(description="Volatility smile fitter (SVI / SABR)")
    sub = p.add_subparsers(dest="model", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--F", type=float, required=True, help="Forward")
    common.add_argument("--T", type=float, required=True, help="Time to expiry (years)")
    common.add_argument("--strikes", type=str, required=True, help="Comma-separated strikes")
    common.add_argument("--vols", type=str, required=True, help="Comma-separated implied vols (decimal)")
    common.add_argument("--grid", type=int, default=21, help="Output strike grid for fitted curve")

    sub.add_parser("svi", parents=[common])

    psabr = sub.add_parser("sabr", parents=[common])
    psabr.add_argument("--beta", type=float, default=0.5, help="SABR beta (held fixed)")

    args = p.parse_args()
    strikes = _parse_floats(args.strikes)
    vols = _parse_floats(args.vols)
    if len(strikes) != len(vols):
        raise SystemExit("strikes and vols must have same length")

    print(f"\n=== Fitting {args.model.upper()}: F={args.F}, T={args.T}, {len(strikes)} points ===")

    if args.model == "svi":
        res = fit_svi(strikes, vols, args.F, args.T)
        print(f"  a     = {res['a']:.6f}")
        print(f"  b     = {res['b']:.6f}")
        print(f"  rho   = {res['rho']:.6f}   (spot-vol correlation proxy)")
        print(f"  m     = {res['m']:.6f}   (smile center, in log-moneyness)")
        print(f"  sigma = {res['sigma']:.6f}   (smile curvature)")
        print(f"  RSS   = {res['rss']:.2e}")
        params = (res['a'], res['b'], res['rho'], res['m'], res['sigma'])
        print("\n  K        market_vol   fitted_vol   diff_vol_pts")
        for K, v in zip(strikes, vols):
            vm = svi_implied_vol(K, args.F, args.T, params)
            print(f"  {K:8.3f}  {v*100:9.3f}%   {vm*100:9.3f}%   {(vm-v)*100:+7.3f}")
    elif args.model == "sabr":
        res = fit_sabr(strikes, vols, args.F, args.T, args.beta)
        print(f"  alpha = {res['alpha']:.6f}")
        print(f"  beta  = {res['beta']:.4f} (fixed)")
        print(f"  rho   = {res['rho']:.6f}   (spot-vol correlation)")
        print(f"  nu    = {res['nu']:.6f}   (vol-of-vol)")
        print(f"  RSS   = {res['rss']:.2e}")
        print("\n  K        market_vol   fitted_vol   diff_vol_pts")
        for K, v in zip(strikes, vols):
            vm = sabr_implied_vol(K, args.F, args.T, res['alpha'], res['beta'], res['rho'], res['nu'])
            print(f"  {K:8.3f}  {v*100:9.3f}%   {vm*100:9.3f}%   {(vm-v)*100:+7.3f}")


if __name__ == "__main__":
    main()
