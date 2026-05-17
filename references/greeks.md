# The Greeks — Quick Reference

Formulas below are for a European call/put under Black-Scholes-Merton. d₁ and d₂ as standard:

```
d1 = [ln(S/K) + (r - q + σ²/2)T] / (σ√T)
d2 = d1 - σ√T
```

`S` = spot, `K` = strike, `T` = time to expiry (years), `r` = risk-free rate, `q` = dividend/carry yield, `σ` = vol, `N(·)` = standard normal CDF, `n(·)` = standard normal PDF.

## First-order

| Greek | Formula (call) | Formula (put) | Sign | What it tells you |
|---|---|---|---|---|
| **Delta** Δ | e^(-qT)·N(d1) | e^(-qT)·[N(d1) − 1] | Call: 0…1, Put: −1…0 | Spot sensitivity. **NOT a hedge ratio in general** — see Ch 7 |
| **Vega** ν | S·e^(-qT)·n(d1)·√T | same | Long options: positive | Vol sensitivity (per 1.00 vol, so divide by 100 for "per vol point") |
| **Theta** Θ | complex; see below | complex; see below | Long options: usually negative | Time decay. NOT linear; accelerates near expiry for ATM, flat for deep OTM |
| **Rho** ρ | K·T·e^(-rT)·N(d2) | −K·T·e^(-rT)·N(−d2) | + for calls, − for puts | Rate sensitivity. Matters more for long-dated and FX |

Theta (call): `−S·e^(-qT)·n(d1)·σ / (2√T) − r·K·e^(-rT)·N(d2) + q·S·e^(-qT)·N(d1)`

## Second-order

| Greek | Formula | What it tells you |
|---|---|---|
| **Gamma** Γ | e^(-qT)·n(d1) / (S·σ·√T) | Curvature of P/L w.r.t. spot. Same for call and put |
| **Vanna** | ∂Δ/∂σ = −e^(-qT)·n(d1)·d2/σ | How delta moves when vol moves. Big for risk reversals |
| **Volga** (vomma) | ∂ν/∂σ = vega·d1·d2/σ | Vega convexity — why OTM options are "long vol of vol" |
| **Charm** | ∂Δ/∂T | Delta decay through time |
| **Color** | ∂Γ/∂T | Gamma decay through time |

## Taleb's emphasis points (book lines)

- **Delta is murky beyond a single stable option.** Ch 7, lines 6155–6188. The risk manager's "delta limit" mindset breaks down for portfolios and especially barriers (the "half billion-dollar delta" story, ~line 6223).

- **Shadow gamma > static gamma.** Ch 8 (lines 6827–7321). Real gamma exposure changes with vol level — what looks like flat gamma at current vol becomes massive long/short gamma if vol moves. Always stress gamma at ±2σ vol shocks.

- **Vega is not one number.** Ch 9 (lines 7322–8019). The vol surface has term structure AND smile. Parallel vega assumes the whole surface shifts uniformly — it never does. Bucket vega by tenor and strike (Ch 14).

- **Theta and gamma are siamese.** Long options: positive gamma, negative theta. You pay theta for the right to gamma-scalp. The breakeven move per day is roughly `σ·√(1/252)` for ATM — if realized exceeds this, gamma wins; if not, theta wins.

- **Minor Greeks aren't minor for exotics.** Charm and vanna dominate near expiry and near barriers. Color matters for short-dated ATM gamma scalping.

## Risk-reporting hygiene

For any position, report at minimum:
1. **Delta** (in spot-equivalent units)
2. **Gamma** (P/L per 1% spot move from gamma alone — `0.5·Γ·(0.01·S)²`)
3. **Vega** (P/L per 1 vol point — `vega/100`)
4. **Theta** (P/L per day — calendar days, not trading)

For exotics, ALSO report:
- Behavior near barriers / discontinuities (price as you sweep spot through the barrier)
- Vega bucketed by tenor
- Cross-Greeks if the position is sensitive (vanna for risk-reversals, volga for OTM-heavy books)

## Hedging hierarchy (Taleb's preference)

1. **Static replication** if possible (Ch 19). Hedge a barrier by buying/selling other vanillas that replicate the payoff.
2. **Discrete delta hedging** with a tolerance band — don't continuously rebalance, set a rebalancing threshold.
3. **Greek-balanced book** (delta + gamma + vega ≈ 0 across buckets).
4. Avoid: continuous-time delta hedging as a literal strategy. It's a pricing benchmark, not an operational plan (Ch 7 line 6186: "Continuous time models should be used for pricing and getting a benchmark fair value, not to hedge.").
