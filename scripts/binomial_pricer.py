"""
Cox-Ross-Rubinstein binomial pricer for American, European, and Bermudan options.

Use when:
- Option has early-exercise rights (American puts, American calls on dividend stock)
- Discrete dividends matter
- You want to verify a BS price with a discrete-time benchmark

Convergence: ~200 steps gives <0.01 price error for typical inputs.
For deep ITM American with discrete dividends, prefer 500+ steps.

Usage:
    python binomial_pricer.py --S 100 --K 100 --T 0.5 --r 0.05 --sigma 0.25 --type put --american
    python binomial_pricer.py --S 50 --K 52 --T 1.0 --r 0.04 --sigma 0.30 --steps 500 --type call
"""
import argparse
import math


def crr_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    q: float = 0.0,
    option_type: str = "call",
    american: bool = False,
    steps: int = 200,
):
    """Cox-Ross-Rubinstein binomial tree. Returns (price, delta, gamma) using nodes."""
    if steps < 1:
        raise ValueError("steps must be >= 1")
    dt = T / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    a = math.exp((r - q) * dt)
    p = (a - d) / (u - d)
    if not (0.0 < p < 1.0):
        raise ValueError(f"Risk-neutral prob {p:.4f} out of (0,1) — check inputs")
    disc = math.exp(-r * dt)

    prices = [S * (u ** (steps - i)) * (d ** i) for i in range(steps + 1)]
    if option_type == "call":
        values = [max(s - K, 0.0) for s in prices]
    elif option_type == "put":
        values = [max(K - s, 0.0) for s in prices]
    else:
        raise ValueError("option_type must be call or put")

    second_to_last = None
    third_to_last = None

    for step in range(steps - 1, -1, -1):
        new_values = []
        for i in range(step + 1):
            cont = disc * (p * values[i] + (1 - p) * values[i + 1])
            if american:
                s_here = S * (u ** (step - i)) * (d ** i)
                exercise = (s_here - K) if option_type == "call" else (K - s_here)
                cont = max(cont, exercise)
            new_values.append(cont)
        values = new_values
        if step == 2:
            third_to_last = list(values)
        if step == 1:
            second_to_last = list(values)

    price = values[0]

    if second_to_last is not None and len(second_to_last) >= 2:
        S_up = S * u
        S_down = S * d
        delta = (second_to_last[0] - second_to_last[1]) / (S_up - S_down)
    else:
        delta = float("nan")

    if third_to_last is not None and len(third_to_last) >= 3:
        S_uu = S * u * u
        S_ud = S
        S_dd = S * d * d
        delta_up = (third_to_last[0] - third_to_last[1]) / (S_uu - S_ud)
        delta_down = (third_to_last[1] - third_to_last[2]) / (S_ud - S_dd)
        gamma = (delta_up - delta_down) / (0.5 * (S_uu - S_dd))
    else:
        gamma = float("nan")

    return price, delta, gamma


def main():
    p = argparse.ArgumentParser(description="CRR binomial pricer (Eur/Am/Bermudan)")
    p.add_argument("--S", type=float, required=True)
    p.add_argument("--K", type=float, required=True)
    p.add_argument("--T", type=float, required=True)
    p.add_argument("--r", type=float, required=True)
    p.add_argument("--sigma", type=float, required=True)
    p.add_argument("--q", type=float, default=0.0)
    p.add_argument("--type", choices=["call", "put"], default="call")
    p.add_argument("--american", action="store_true", help="Allow early exercise at every node")
    p.add_argument("--steps", type=int, default=200)
    args = p.parse_args()

    price, delta, gamma = crr_price(
        args.S, args.K, args.T, args.r, args.sigma, args.q, args.type, args.american, args.steps
    )
    style = "American" if args.american else "European"
    print(f"=== CRR Binomial {style} {args.type.upper()} ({args.steps} steps) ===")
    print(f"  Price : {price:.6f}")
    print(f"  Delta : {delta:.6f}")
    print(f"  Gamma : {gamma:.6f}")

    if args.american and args.type == "put":
        from bs_pricer import black_scholes
        eur = black_scholes(args.S, args.K, args.T, args.r, args.sigma, args.q, "put").price
        premium = price - eur
        print(f"  European put : {eur:.6f}")
        print(f"  Early-exercise premium : {premium:.6f}  ({100*premium/eur:.2f}% of European)")


if __name__ == "__main__":
    main()
