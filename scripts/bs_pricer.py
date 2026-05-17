"""
Black-Scholes-Merton pricer with full Greeks.

Works for any asset class where BSM applies as a quoting convention:
- Equities (q = continuous dividend yield)
- FX (q = foreign rate, r = domestic rate — Garman-Kohlhagen)
- Commodities (q = convenience yield - storage)
- Crypto (q = staking yield if any)
- Futures: use Black-76 by setting S = F and r = q (or use --black76 flag)

Reminder from Taleb (Dynamic Hedging, Ch 7): BS is for pricing benchmarks
and getting a fair value, NOT a hedging strategy. Continuous-time delta is
not a hedge ratio for portfolios or near barriers.

Usage:
    python bs_pricer.py --S 100 --K 105 --T 0.5 --r 0.05 --q 0.02 --sigma 0.20 --type call
    python bs_pricer.py --S 100 --K 100 --T 0.25 --r 0.05 --sigma 0.30 --type put --black76
"""
import argparse
import math
from dataclasses import dataclass


SQRT_2PI = math.sqrt(2.0 * math.pi)


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / SQRT_2PI


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass
class BSResult:
    price: float
    delta: float
    gamma: float
    vega: float      # per 1.00 vol (divide by 100 for per-vol-point)
    theta: float     # per year (divide by 365 for per-calendar-day)
    rho: float       # per 1.00 rate
    vanna: float
    volga: float
    charm: float
    color: float
    d1: float
    d2: float


def black_scholes(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    q: float = 0.0,
    option_type: str = "call",
) -> BSResult:
    """Generalized BSM. For FX use r=domestic, q=foreign. For futures use q=r (Black-76)."""
    if T <= 0:
        intrinsic = max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0)
        return BSResult(intrinsic, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    if sigma <= 0:
        raise ValueError("sigma must be > 0")

    sqrtT = math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)
    Nd1 = _norm_cdf(d1)
    Nd2 = _norm_cdf(d2)
    nd1 = _norm_pdf(d1)

    if option_type == "call":
        price = S * disc_q * Nd1 - K * disc_r * Nd2
        delta = disc_q * Nd1
        rho = K * T * disc_r * Nd2
        theta = (
            -S * disc_q * nd1 * sigma / (2.0 * sqrtT)
            - r * K * disc_r * Nd2
            + q * S * disc_q * Nd1
        )
        charm = -disc_q * (
            nd1 * (2.0 * (r - q) * T - d2 * sigma * sqrtT) / (2.0 * T * sigma * sqrtT)
            - q * Nd1
        )
    elif option_type == "put":
        price = K * disc_r * _norm_cdf(-d2) - S * disc_q * _norm_cdf(-d1)
        delta = disc_q * (Nd1 - 1.0)
        rho = -K * T * disc_r * _norm_cdf(-d2)
        theta = (
            -S * disc_q * nd1 * sigma / (2.0 * sqrtT)
            + r * K * disc_r * _norm_cdf(-d2)
            - q * S * disc_q * _norm_cdf(-d1)
        )
        charm = -disc_q * (
            nd1 * (2.0 * (r - q) * T - d2 * sigma * sqrtT) / (2.0 * T * sigma * sqrtT)
            + q * _norm_cdf(-d1)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    gamma = disc_q * nd1 / (S * sigma * sqrtT)
    vega = S * disc_q * nd1 * sqrtT
    vanna = -disc_q * nd1 * d2 / sigma
    volga = vega * d1 * d2 / sigma
    color = -disc_q * nd1 / (2.0 * S * T * sigma * sqrtT) * (
        2.0 * q * T + 1.0 + (2.0 * (r - q) * T - d2 * sigma * sqrtT) * d1 / (sigma * sqrtT)
    )

    return BSResult(price, delta, gamma, vega, theta, rho, vanna, volga, charm, color, d1, d2)


def implied_vol(
    market_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    q: float = 0.0,
    option_type: str = "call",
    tol: float = 1e-7,
    max_iter: int = 100,
) -> float:
    """Newton-Raphson implied vol with bisection fallback."""
    intrinsic = max(S * math.exp(-q * T) - K * math.exp(-r * T), 0.0) if option_type == "call" \
        else max(K * math.exp(-r * T) - S * math.exp(-q * T), 0.0)
    if market_price < intrinsic - 1e-10:
        raise ValueError(f"Market price {market_price} below intrinsic {intrinsic}")

    sigma = 0.20
    for _ in range(max_iter):
        res = black_scholes(S, K, T, r, sigma, q, option_type)
        diff = res.price - market_price
        if abs(diff) < tol:
            return sigma
        if res.vega < 1e-12:
            break
        sigma -= diff / res.vega
        if sigma <= 0:
            sigma = 0.001

    lo, hi = 1e-4, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        res = black_scholes(S, K, T, r, mid, q, option_type)
        if abs(res.price - market_price) < tol:
            return mid
        if res.price < market_price:
            lo = mid
        else:
            hi = mid
    return mid


def main():
    p = argparse.ArgumentParser(description="Black-Scholes-Merton pricer with Greeks")
    p.add_argument("--S", type=float, required=True, help="Spot price")
    p.add_argument("--K", type=float, required=True, help="Strike")
    p.add_argument("--T", type=float, required=True, help="Time to expiry (years)")
    p.add_argument("--r", type=float, required=True, help="Risk-free rate (decimal, e.g. 0.05)")
    p.add_argument("--sigma", type=float, required=True, help="Volatility (decimal)")
    p.add_argument("--q", type=float, default=0.0, help="Dividend/foreign yield/carry (decimal)")
    p.add_argument("--type", choices=["call", "put"], default="call")
    p.add_argument("--black76", action="store_true", help="Black-76 mode (sets q=r for futures)")
    p.add_argument("--implied", type=float, default=None, help="If set, solve for implied vol from this market price")
    args = p.parse_args()

    q = args.r if args.black76 else args.q

    if args.implied is not None:
        iv = implied_vol(args.implied, args.S, args.K, args.T, args.r, q, args.type)
        print(f"Implied vol: {iv:.6f}  ({iv*100:.3f}%)")
        return

    res = black_scholes(args.S, args.K, args.T, args.r, args.sigma, q, args.type)
    print(f"=== BSM {args.type.upper()} on S={args.S} K={args.K} T={args.T}y ===")
    print(f"  Price       : {res.price:.6f}")
    print(f"  % of spot   : {100.0*res.price/args.S:.4f}%")
    print(f"  Delta       : {res.delta:.6f}")
    print(f"  Gamma       : {res.gamma:.6f}")
    print(f"  Vega        : {res.vega:.6f}  (per 1.00 vol; per vol-point: {res.vega/100:.6f})")
    print(f"  Theta       : {res.theta:.6f}  (per year; per cal-day: {res.theta/365:.6f})")
    print(f"  Rho         : {res.rho:.6f}")
    print(f"  Vanna       : {res.vanna:.6f}")
    print(f"  Volga       : {res.volga:.6f}")
    print(f"  Charm       : {res.charm:.6f}")
    print(f"  Color       : {res.color:.6f}")
    print(f"  d1, d2      : {res.d1:.6f}, {res.d2:.6f}")
    print()
    print("Reminder (Taleb Ch 7): continuous-time delta is a benchmark, not a hedge ratio.")
    print("For OTM options, flat-vol BS underprices wings — consult the smile (Ch 9, 15).")


if __name__ == "__main__":
    main()
