"""
Heston (1993) stochastic-volatility pricer for European options.

The Heston model:
  dS = (r - q) S dt + sqrt(v) S dW1
  dv = kappa (theta - v) dt + xi sqrt(v) dW2
  dW1 dW2 = rho dt

Parameters:
  v0     — initial variance
  kappa  — mean-reversion speed of variance
  theta  — long-run mean variance
  xi     — vol-of-vol
  rho    — correlation between spot and vol shocks

Pricing via the semi-analytic characteristic-function approach (Lord-Kahl
formulation, numerically stable via the "Little Trap"). Integration is
adaptive Simpson on the truncated frequency domain.

Per Taleb Ch 15: Heston captures vvol-driven fat tails AND skew (via rho < 0).
It is the canonical stochastic-vol model for equity index pricing.

Usage:
    python heston_pricer.py --S 100 --K 100 --T 1.0 --r 0.03 --q 0.0 \
        --v0 0.04 --kappa 2.0 --theta 0.04 --xi 0.3 --rho -0.7 --type call

    # Sweep strikes to see the model-implied smile
    python heston_pricer.py --S 100 --T 1.0 --r 0.03 --q 0.0 \
        --v0 0.04 --kappa 2.0 --theta 0.04 --xi 0.5 --rho -0.7 --smile
"""
import argparse
import cmath
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs_pricer import implied_vol


def heston_char_func(u, S, T, r, q, v0, kappa, theta, xi, rho, j: int = 1):
    """Heston characteristic function (Little Trap / Albrecher form for stability).
       j=1 gives the in-the-money probability; j=2 gives the risk-neutral prob."""
    x = math.log(S)
    a = kappa * theta
    if j == 1:
        u_ = 0.5
        b = kappa - rho * xi
    else:
        u_ = -0.5
        b = kappa

    d = cmath.sqrt((rho * xi * 1j * u - b) ** 2 - xi * xi * (2 * u_ * 1j * u - u * u))
    g = (b - rho * xi * 1j * u - d) / (b - rho * xi * 1j * u + d)

    exp_dT = cmath.exp(-d * T)
    C = (r - q) * 1j * u * T + (a / (xi * xi)) * (
        (b - rho * xi * 1j * u - d) * T - 2.0 * cmath.log((1.0 - g * exp_dT) / (1.0 - g))
    )
    D = (b - rho * xi * 1j * u - d) / (xi * xi) * ((1.0 - exp_dT) / (1.0 - g * exp_dT))
    return cmath.exp(C + D * v0 + 1j * u * x)


def heston_price(S, K, T, r, q, v0, kappa, theta, xi, rho, option_type="call",
                 u_max: float = 200.0, n_steps: int = 1000):
    """Semi-analytic price via Gil-Pelaez inversion."""
    log_K = math.log(K)

    def integrand(u, j):
        cf = heston_char_func(u, S, T, r, q, v0, kappa, theta, xi, rho, j)
        return (cmath.exp(-1j * u * log_K) * cf / (1j * u)).real

    def simpson(f, a, b, n):
        if n % 2:
            n += 1
        h = (b - a) / n
        s = f(a) + f(b)
        for i in range(1, n):
            x = a + i * h
            s += 4 * f(x) if i % 2 else 2 * f(x)
        return s * h / 3.0

    eps = 1e-6
    P1 = 0.5 + (1.0 / math.pi) * simpson(lambda u: integrand(u, 1), eps, u_max, n_steps)
    P2 = 0.5 + (1.0 / math.pi) * simpson(lambda u: integrand(u, 2), eps, u_max, n_steps)

    call = S * math.exp(-q * T) * P1 - K * math.exp(-r * T) * P2
    if option_type == "call":
        return call
    elif option_type == "put":
        return call - S * math.exp(-q * T) + K * math.exp(-r * T)
    else:
        raise ValueError("option_type must be call or put")


def main():
    p = argparse.ArgumentParser(description="Heston stochastic-vol pricer")
    p.add_argument("--S", type=float, required=True)
    p.add_argument("--K", type=float, default=None, help="Strike (omit when using --smile)")
    p.add_argument("--T", type=float, required=True)
    p.add_argument("--r", type=float, required=True)
    p.add_argument("--q", type=float, default=0.0)
    p.add_argument("--v0", type=float, required=True, help="Initial variance (NOT vol)")
    p.add_argument("--kappa", type=float, required=True, help="Mean-reversion speed")
    p.add_argument("--theta", type=float, required=True, help="Long-run mean variance")
    p.add_argument("--xi", type=float, required=True, help="Vol-of-vol")
    p.add_argument("--rho", type=float, required=True, help="Spot-vol correlation")
    p.add_argument("--type", choices=["call", "put"], default="call")
    p.add_argument("--smile", action="store_true",
                   help="Print full smile (5 strikes spanning ±2σ) instead of single price")
    p.add_argument("--u-max", type=float, default=200.0)
    p.add_argument("--steps", type=int, default=1000)
    args = p.parse_args()

    feller = 2.0 * args.kappa * args.theta - args.xi ** 2
    if feller < 0:
        print(f"  WARNING: Feller condition violated (2*kappa*theta - xi^2 = {feller:.4f} < 0). Variance can hit 0.")

    if args.smile:
        sigma_proxy = math.sqrt(args.theta)
        strikes = [args.S * math.exp(k * sigma_proxy * math.sqrt(args.T))
                   for k in (-1.5, -0.75, 0.0, 0.75, 1.5)]
        print(f"\n=== Heston smile (T={args.T}y) ===")
        print(f"  Strike      Price        Implied vol")
        for K in strikes:
            price = heston_price(args.S, K, args.T, args.r, args.q,
                                 args.v0, args.kappa, args.theta, args.xi, args.rho,
                                 args.type, args.u_max, args.steps)
            try:
                iv = implied_vol(price, args.S, K, args.T, args.r, args.q, args.type)
                iv_str = f"{iv*100:.3f}%"
            except Exception:
                iv_str = "n/a"
            print(f"  {K:9.4f}   {price:9.6f}   {iv_str}")
        return

    if args.K is None:
        raise SystemExit("--K is required when not using --smile")

    price = heston_price(args.S, args.K, args.T, args.r, args.q,
                         args.v0, args.kappa, args.theta, args.xi, args.rho,
                         args.type, args.u_max, args.steps)
    iv = implied_vol(price, args.S, args.K, args.T, args.r, args.q, args.type)

    print(f"\n=== Heston {args.type.upper()} on S={args.S} K={args.K} T={args.T}y ===")
    print(f"  Price          : {price:.6f}")
    print(f"  BS-implied vol : {iv*100:.4f}%")
    print(f"  v0    = {args.v0:.4f} (vol = {math.sqrt(args.v0)*100:.2f}%)")
    print(f"  theta = {args.theta:.4f} (long-run vol = {math.sqrt(args.theta)*100:.2f}%)")
    print(f"  kappa = {args.kappa:.4f}, xi = {args.xi:.4f}, rho = {args.rho:+.4f}")


if __name__ == "__main__":
    main()
