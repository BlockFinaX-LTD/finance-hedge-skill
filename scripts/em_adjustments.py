"""
Emerging-markets pricing adjustments.

For EM and any market where flat-vol BS systematically misprices:
  1. Merton jump-diffusion: layer discrete jumps on top of GBM diffusion.
     Calibrate to historical event frequency and magnitude.
  2. Smile-widening: parametric SSVI-like widening of the wings.
  3. Peg-break decomposition: for pegged FX, decompose into
     (P_hold × small-vol BS) + (P_break × jump payoff).

Usage:
    # Jump-diffusion call on EM FX, 3 month, 5% jumps expected per year, -10% mean jump
    python em_adjustments.py jump --S 5.10 --K 5.30 --T 0.25 --r 0.10 --sigma 0.12 --q 0.045 \
        --lam 5 --jump-mean -0.10 --jump-std 0.05 --type call

    # Peg-break: HKD/USD long-dated OTM call as binary on peg break
    python em_adjustments.py peg --S 7.80 --K 8.50 --T 1.0 --r 0.05 --q 0.045 \
        --p-break 0.05 --jump-size 0.15 --base-sigma 0.005 --type call
"""
import argparse
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs_pricer import black_scholes


def merton_jump_diffusion(
    S, K, T, r, sigma, q,
    lam: float,            # jump intensity (events per year)
    jump_mean: float,      # mean log-jump size (e.g., -0.10 = -10% drop on average)
    jump_std: float,       # std-dev of log-jump
    option_type: str = "call",
    n_terms: int = 50,
):
    """Merton (1976) jump-diffusion. Price = Poisson-weighted sum of BS prices
       with adjusted vol and drift for n=0,1,2,... jumps."""
    k = math.exp(jump_mean + 0.5 * jump_std ** 2) - 1.0
    r_adj_base = r - lam * k
    price = 0.0
    log_lam_T = math.log(lam * T) if lam * T > 0 else float("-inf")
    log_fact = 0.0
    for n in range(n_terms):
        if n > 0:
            log_fact += math.log(n)
        sigma_n = math.sqrt(sigma * sigma + n * jump_std * jump_std / T) if T > 0 else sigma
        r_n = r_adj_base + n * (jump_mean + 0.5 * jump_std ** 2) / T if T > 0 else r_adj_base
        bs = black_scholes(S, K, T, r_n, sigma_n, q, option_type)
        if lam * T == 0:
            weight = 1.0 if n == 0 else 0.0
        else:
            weight = math.exp(-lam * T + n * log_lam_T - log_fact)
        price += weight * bs.price
        if weight < 1e-15 and n > 10:
            break
    return price


def peg_break_price(
    S, K, T, r, q,
    p_break: float,        # probability peg breaks within T
    jump_size: float,      # log-magnitude of devaluation if breaks (e.g., 0.15 = 15%)
    base_sigma: float,     # vol while peg holds (typically near zero)
    option_type: str = "call",
):
    """Two-state model: peg holds with small-vol BS, or breaks with single jump.
       This is the right framework for HKD/AED/SAR-USD type instruments."""
    bs_hold = black_scholes(S, K, T, r, max(base_sigma, 1e-4), q, option_type).price
    S_post = S * math.exp(jump_size) if option_type == "call" else S * math.exp(-jump_size)
    sigma_post = max(0.20, base_sigma * 5)
    bs_break = black_scholes(S_post, K, T, r, sigma_post, q, option_type).price
    return (1 - p_break) * bs_hold + p_break * bs_break, {
        "hold_component": (1 - p_break) * bs_hold,
        "break_component": p_break * bs_break,
        "p_break": p_break,
    }


def smile_widen_price(S, K, T, r, sigma_atm, q, option_type, skew_param: float, kurt_param: float):
    """Heuristic smile widening for OTM strikes.
       Uses SSVI-inspired adjustment:
         sigma(K) = sigma_atm * (1 + skew_param * m + kurt_param * m^2)
       where m = ln(K/F) / (sigma_atm * sqrt(T)) is moneyness in vol units.
       Recommended starting params for EM FX: skew=-0.10 (left skew), kurt=0.30."""
    if T <= 0:
        return black_scholes(S, K, T, r, sigma_atm, q, option_type).price
    F = S * math.exp((r - q) * T)
    m = math.log(K / F) / (sigma_atm * math.sqrt(T))
    factor = 1.0 + skew_param * m + kurt_param * m * m
    sigma_eff = max(sigma_atm * factor, 0.001)
    bs = black_scholes(S, K, T, r, sigma_eff, q, option_type)
    return bs.price, sigma_eff


def main():
    p = argparse.ArgumentParser(description="EM and jump-diffusion adjustments")
    sub = p.add_subparsers(dest="mode", required=True)

    pj = sub.add_parser("jump", help="Merton jump-diffusion pricing")
    for arg in ["S", "K", "T", "r", "sigma"]:
        pj.add_argument(f"--{arg}", type=float, required=True)
    pj.add_argument("--q", type=float, default=0.0)
    pj.add_argument("--lam", type=float, required=True, help="Jump intensity per year")
    pj.add_argument("--jump-mean", type=float, required=True, help="Mean log-jump size")
    pj.add_argument("--jump-std", type=float, required=True, help="Std of log-jump")
    pj.add_argument("--type", choices=["call", "put"], default="call")

    pp = sub.add_parser("peg", help="Pegged-FX two-state pricing")
    for arg in ["S", "K", "T", "r"]:
        pp.add_argument(f"--{arg}", type=float, required=True)
    pp.add_argument("--q", type=float, default=0.0)
    pp.add_argument("--p-break", type=float, required=True)
    pp.add_argument("--jump-size", type=float, required=True, help="Log-magnitude of devaluation")
    pp.add_argument("--base-sigma", type=float, default=0.005)
    pp.add_argument("--type", choices=["call", "put"], default="call")

    ps = sub.add_parser("smile", help="Smile-widened BS")
    for arg in ["S", "K", "T", "r", "sigma"]:
        ps.add_argument(f"--{arg}", type=float, required=True)
    ps.add_argument("--q", type=float, default=0.0)
    ps.add_argument("--skew", type=float, default=-0.10)
    ps.add_argument("--kurt", type=float, default=0.30)
    ps.add_argument("--type", choices=["call", "put"], default="call")

    args = p.parse_args()

    if args.mode == "jump":
        price = merton_jump_diffusion(
            args.S, args.K, args.T, args.r, args.sigma, args.q,
            args.lam, args.jump_mean, args.jump_std, args.type
        )
        bs_only = black_scholes(args.S, args.K, args.T, args.r, args.sigma, args.q, args.type).price
        print(f"=== Merton jump-diffusion {args.type.upper()} ===")
        print(f"  Jump-diffusion price : {price:.6f}")
        print(f"  Plain BS price       : {bs_only:.6f}")
        print(f"  Jump premium         : {price - bs_only:+.6f}  ({100*(price-bs_only)/bs_only:+.2f}%)")
    elif args.mode == "peg":
        price, detail = peg_break_price(
            args.S, args.K, args.T, args.r, args.q,
            args.p_break, args.jump_size, args.base_sigma, args.type
        )
        print(f"=== Peg-break decomposition {args.type.upper()} ===")
        print(f"  Total price          : {price:.6f}")
        print(f"  Hold component (1-p) : {detail['hold_component']:.6f}")
        print(f"  Break component (p)  : {detail['break_component']:.6f}")
        print(f"  P(break)             : {detail['p_break']:.4f}")
        print(f"\n  NOTE: long-dated OTM peg-currency options are essentially binary bets")
        print(f"  on peg break. Don't size on Sharpe — size on max-loss.")
    elif args.mode == "smile":
        price, sig_eff = smile_widen_price(
            args.S, args.K, args.T, args.r, args.sigma, args.q, args.type, args.skew, args.kurt
        )
        bs_flat = black_scholes(args.S, args.K, args.T, args.r, args.sigma, args.q, args.type).price
        print(f"=== Smile-widened {args.type.upper()} (skew={args.skew}, kurt={args.kurt}) ===")
        print(f"  Smile-adjusted price : {price:.6f}")
        print(f"  Flat-vol BS price    : {bs_flat:.6f}")
        print(f"  Effective vol at K   : {sig_eff*100:.3f}% (vs ATM {args.sigma*100:.3f}%)")
        print(f"  Wing premium         : {price - bs_flat:+.6f}  ({100*(price-bs_flat)/max(bs_flat,1e-9):+.2f}%)")


if __name__ == "__main__":
    main()
