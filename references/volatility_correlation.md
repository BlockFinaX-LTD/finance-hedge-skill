# Volatility and Correlation (Ch 6 — lines 5268–5936)

> *"What traders and historians share is an ingrained distrust of the notion of correlation."* — Ch 6 epigraph

Read this when estimating a volatility input, picking between historical and implied, or building a correlation matrix for a multi-asset position.

## Definitions

### Volatility (line 5283)
> *"The amount of variability in the returns of a particular asset."*

Two flavors:
- **Actual / historical** — what the market actually did
- **Implied** — what option prices say it will be, backed out through BS as a quoting convention (even if you believe BS is wrong; you use it because the market uses it — line 5292)

### Correlation (line 5298)
> *"The least-square measured association between two random variables. It identifies the degree of certainty with which a person can predict the move in one random variable as a result of a change in the other variable."*

The variables are **log-returns** (ln P_t − ln P_{t−1}), not price levels.

Flavors:
- **Actual / historical** — measured from data
- **Implied** — derived from option prices on the components (see Module D and [correlation_triangles.md](correlation_triangles.md))

## The most-common correlation blunder (line 5317)

> *"Traders often make the simple blunder of assuming that a 100% correlation between two assets A and B means that asset A should move by 1% in response to asset B moving up by 1%. This is not true."*

Correlation = expected **ratio** of moves *divided by their corresponding volatilities*. Two assets can correlate 100% while one moves 2x the other — that's a `beta`-style relationship inside a correlation of 1.0.

When the user asks "if A moves 1%, how much does B move?", the answer is `ρ · (σ_B / σ_A) · ΔA`, not `ρ · ΔA`.

## "Markets aren't lognormal" (line 5328)

Lognormality assumes prices can't go negative — convenient for stocks and FX, problematic for:
- Rates (Euroyen at 0.10% in 1995 — line 5390)
- Spreads and basis
- Anything that can be quoted on either side of zero (carbon credits, weather, electricity)

Taleb's rule (line 5400): *"Traders should take theoretical dogma less seriously."*

## Geometric vs. arithmetic Brownian motion (line 5343)

| | Geometric BM | Arithmetic BM (Bachelier) |
|---|---|---|
| Assumption | Constant **% move** per unit time | Constant **$ move** per unit time |
| Negative prices? | Impossible | Possible |
| Standard model in | Equities, FX, commodities | Rates (sometimes), spreads |
| Vol scales with | Spot level | Constant |

**Real markets are mixed** (line 5413): arithmetic in the short term, geometric in the long. The choice matters enormously for OTM pricing in unusual rate environments.

**The Eurodollar story (line 5371):** in 1991–93, dealers selling OTM Eurodollar calls assumed % volatility was stable; tick vol turned out to be stable instead → "they were short vol at very low levels" → big losses. **Always check whether your assumed vol convention matches market behavior.**

**The Euroyen story (line 5390):** rates dropped to 0.10%, where a 1bp move = 160% % vol. Market priced 100-calls / puts-struck-at-zero. Bachelier (arithmetic) became plausible again. *"Perhaps that man Bachelier was right."*

## Vol calculation methods

### Standard close-to-close (line 5421)

> Volatility for a dynamic hedger could be calculated as the square root of the sum of the **squares** of the movements, **not** the deviations from an average.

Reasoning (line 5430): if a market moves 1% each day for a month all in the same direction, standard deviation = 0 (no deviation from mean = 1%). An option trader's instinct says "this is 1%-a-day vol" — so use squared returns, not squared deviations.

For estimation:
- Standard form: `σ² = Σ(r_i − r̄)² / (n−1)` — drops 1 degree of freedom
- "Dynamic-hedger" form: `σ² = Σ(r_i)² / n` — assumes mean ≈ 0

The two converge when there's no trend. They diverge when there is. **In trending markets, classical vol underestimates the hedger's realized P/L variance.**

### Parkinson estimator (line ~700 — Ch 6 contents)

Uses **daily high-low range** instead of close-to-close:
```
σ²_P = (1 / (4·ln 2)) · (ln(H/L))²
```

Advantages:
- 4–5× more efficient than close-to-close (less data needed for same accuracy)
- Catches intraday volatility that close-to-close misses

Limitations:
- Underestimates vol when intraday range is constrained (limit-up/down, low-volume sessions)
- Doesn't work for markets with gaps (where close ≠ next open)

### Variance ratio method

Compare realized vol at two sampling frequencies (e.g., 1-day vs 5-day). If returns are truly random walk, the variance scales linearly with time → ratio ≈ 1. Significant deviations indicate:
- Mean reversion (ratio < 1) — typical for many EM FX
- Trending / momentum (ratio > 1) — typical for some commodity markets
- Vol clustering — neither, but autocorrelation in squared returns

Used to detect non-randomness without committing to a specific alternative model.

### Filtering

Subtract a moving-average or factor model before measuring vol. Removes "smooth" drift to isolate the diffusive component. Common when underlying has known seasonality (commodities) or known event days (Fed meetings, earnings).

## "There is no such thing as constant volatility and correlation" (line 5333)

The chapter's load-bearing claim. Vol and correlation are themselves **stochastic processes** — they regime-shift, mean-revert at non-constant speeds, and respond to spot moves non-linearly.

> *"Markets have adjusted to the fact that volatility is not constant, not yet to the fact that correlation is volatile."*

This is the same fat-tail issue addressed in [fat_tails.md](fat_tails.md) but applied to correlation. Implied correlation surfaces are still relatively crude — a frontier for sophisticated multi-asset traders.

## Practical rules

1. **Pick your vol convention to match the market's behavior, not theoretical preference.** Lognormal for equities, normal/Bachelier for low rates and spreads.
2. **For dynamic hedgers, prefer the sum-of-squared-returns formula over standard-deviation-from-mean.** It matches the P/L you'll realize.
3. **Use Parkinson alongside close-to-close.** Disagreement signals intraday vol the close misses.
4. **Correlation ≠ beta.** Translate properly: `expected ΔB = ρ · (σ_B/σ_A) · ΔA`.
5. **Treat correlation as stochastic.** Stress test with ±0.2 to ±0.4 shocks and correlation-to-1 in stress.
6. **For EM, low-rate, or distressed assets, always question lognormality.**
