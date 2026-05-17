# Pricing Decision Tree

Use this BEFORE running a pricer. Pick the model that matches the structure — flat-vol BS is the wrong default for most things.

## Step 1: Decompose the payoff (Ch 2 framework)

For any option, answer six questions:

1. **Homogeneity** — Does payoff scale linearly with spot? (Standard calls/puts yes; binaries no; cliquets partially.)
2. **Payoff continuity** — Is the payoff function continuous in spot at expiry? (Vanilla yes; binary no; barrier discontinuous in time.)
3. **Barriers** — Any knock-in/knock-out features?
4. **Number of assets** — Single, basket, rainbow, spread?
5. **Order** — Is the underlying itself an option? (Compound, chooser.)
6. **Path dependence** — Does intermediate-path matter? (Asian = yes; lookback = yes; barrier = yes; vanilla European = no.)

## Step 2: Pick the model

```
              ┌── European, single asset, no barrier, no path-dep
              │      └── BLACK-SCHOLES (with smile-adjusted vol)
              │
              ├── American or Bermudan, no barrier
              │      └── BINOMIAL TREE (200+ steps) or LSM Monte Carlo
              │
              ├── Barrier (single, continuous monitoring)
              │      ├── Vanilla underlying, GBM → MERTON BARRIER FORMULA (closed-form)
              │      └── Else → MONTE CARLO with barrier-bias correction
              │
              ├── Barrier (discrete monitoring)
              │      └── MONTE CARLO with monitoring-frequency adjustment
              │
              ├── Binary (digital)
              │      ├── European → BS digital (but ALWAYS spread-quote it; see Ch 17)
              │      └── American (one-touch, no-touch) → CLOSED-FORM (reflection principle) or MC
              │
              ├── Asian
              │      ├── Geometric average → CLOSED-FORM (lognormal of geometric mean)
              │      └── Arithmetic average → MONTE CARLO (or Turnbull-Wakeman approx)
              │
              ├── Lookback
              │      ├── Continuous monitoring → CLOSED-FORM (Goldman-Sosin-Gatto)
              │      └── Discrete → MONTE CARLO
              │
              ├── Multi-asset / basket / rainbow / spread
              │      └── MONTE CARLO with correlation matrix (or Margrabe for 2-asset spread)
              │
              ├── Compound, chooser
              │      └── GESKE FORMULA (compound) or CLOSED-FORM CHOOSER
              │
              └── Stochastic vol or jumps material (EM, crypto, deep OTM)
                     ├── HESTON (stochastic vol, closed-form via FFT)
                     ├── SABR (rates, FX smile fitting)
                     └── MERTON JUMP-DIFFUSION (event-risk overlay)
```

## Step 3: Volatility input — the most-mispriced input

Flat-vol BS underprices the wings systematically (Ch 15). For any non-ATM option:

- **Liquid market:** pull the implied vol off the smile at the relevant strike+tenor
- **Illiquid market:** interpolate from the closest liquid surface; widen by an "unobservability premium"
- **No surface available:** start with historical vol but add a wing premium based on the empirical fat-tail kurtosis (Ch 15 lines 11141–11250 — vvol model)
- **For barriers:** the relevant vol is around the barrier, not ATM — sticky-strike vs. sticky-delta matters (Ch 9)
- **For binaries:** vol skew implies the digital price; never use a single vol number (Ch 17)

## Step 4: Rates and carry

- **Equities:** `r` = risk-free in trade currency; `q` = continuous dividend yield (or discrete cash dividends modeled separately)
- **FX (Garman-Kohlhagen):** `r` = domestic rate, `q` = foreign rate. Spot S is units of domestic per unit foreign.
- **Commodities:** `q` = convenience yield − storage cost. For futures-settled options use Black-76 (no spot drift; use F directly).
- **Crypto:** treat staking yield as q if applicable. Funding rates on perps are a separate cash flow.
- **EM:** be careful about which rate. For EM FX, use NDF-implied yields if onshore rates are not freely tradable (capital controls).

## Step 5: Sanity checks before quoting

1. **Put-call parity**: `C − P = S·e^(-qT) − K·e^(-rT)`. If violated, your inputs are wrong.
2. **Bounds**: `max(S·e^(-qT) − K·e^(-rT), 0) ≤ C ≤ S·e^(-qT)` for a call.
3. **Greeks reasonable**: Delta in [0, e^(-qT)] for a call. Gamma positive for long. Vega positive for long.
4. **Time monotonicity**: A longer-dated option (same strike) should not be cheaper than a shorter-dated one for vanillas (caveat: deep-ITM dividend-paying stocks can violate this).
5. **Smile-implied price vs. flat-vol price**: If the option is OTM and your smile-adjusted price is more than 20% off flat-vol BS, that's expected — don't "fix" the model.

## When to refuse to quote

- Underlying has no observable price or recent volume
- Tenor extends past your liquid vol surface and you have no jump-overlay data
- Payoff has a barrier in an extremely illiquid region (price impact of hedging > theoretical premium)
- For EM: capital controls or peg events make the risk-neutral measure economically meaningless

In these cases, quote a *range* with explicit uncertainty bands and flag the structural problem.
