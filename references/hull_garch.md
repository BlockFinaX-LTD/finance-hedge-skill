# Estimating Volatilities and Correlations (Hull Ch 23)

Modern variance-and-correlation forecasting. Taleb's [volatility_correlation.md](volatility_correlation.md) covers the Parkinson (range) estimator and the philosophy ("no constant vol or correlation"); this file covers the parametric estimators every quant uses in production: EWMA and GARCH.

## Returns vs prices

Define daily continuously compounded return:
```
u_i = ln(S_i / S_{i−1})
```
Use returns (not log-prices or arithmetic returns) — they are approximately mean zero, scale linearly with √t, and have well-defined moments under standard models.

For volatility estimation, often **assume the mean is zero**. The mean is small relative to the daily standard deviation, and estimating both adds noise.

## Equally weighted estimator (baseline)

```
σ̂² = (1/m) · Σ_{i=1..m} u_{n−i}²
```

Problems:
1. All observations weighted equally; an extreme move from 250 days ago has the same weight as yesterday.
2. Volatility clustering is real (markets have quiet and stormy regimes), but the estimator can't see it.
3. When the extreme move drops out of the window (m+1 days later), the estimate suddenly drops — the "ghost" effect.

## EWMA — exponentially weighted moving average

Each observation gets exponentially declining weight:
```
σ̂_n² = λ · σ̂_{n−1}² + (1 − λ) · u_{n−1}²
```

Equivalent to weighting `u_{n−i}²` by `(1 − λ) · λ^(i−1)`.

The single parameter λ controls memory:
- **λ = 0.94** — RiskMetrics convention (≈ 1-month effective horizon for daily data).
- **λ = 0.97** — slower-reacting; often a better fit for equity indices.

Advantages: trivial to compute (one-line recursion), no parameters to estimate beyond λ, captures volatility clustering and the recent-jump effect.

Limitation: no mean reversion. EWMA forecasts assume current vol persists forever — wrong over long horizons.

## GARCH(1,1) — the workhorse

```
σ̂_n² = ω + α · u_{n−1}² + β · σ̂_{n−1}²
```

Three parameters: ω > 0, α ≥ 0, β ≥ 0, with α + β < 1 for stationarity.

Decompose into the **mean-reverting** form:
```
σ̂_n² = γ V_L + α · u_{n−1}² + β · σ̂_{n−1}²
```
where γ = 1 − α − β and V_L = ω / γ is the **long-run variance**. Pull rate of mean reversion = γ.

EWMA is the GARCH(1,1) special case where ω = 0 and α + β = 1.

**Persistence** = α + β. High persistence (close to 1) means shocks decay slowly; equity returns typically α+β ≈ 0.97–0.99, FX returns typically a bit lower.

## Maximum likelihood estimation (MLE)

Hull derives the GARCH MLE under normality:
```
log L = −Σ [ ln(σ_i²) + u_i² / σ_i² ]    (constant dropped)
```
Maximize numerically over (ω, α, β). Returns rarely look exactly normal — fat tails persist after GARCH because the *innovation* still has excess kurtosis — but the MLE is consistent and standard errors are robust enough for practical use.

Practical pitfalls:
1. The objective surface is shallow near the optimum; different starting points give different (ω, α, β) with similar likelihood. Constrain by setting V_L from sample variance and only optimize over α, β.
2. Boundary issues: if α+β hits 1 in optimization, the model becomes IGARCH (= EWMA). Most software pulls solutions back from the boundary.
3. Outliers dominate the likelihood. Robust GARCH (t-innovations, GED-innovations) reduces this.

## Forecasting forward variance

Under GARCH(1,1), expected variance at time t (in days from now) is:
```
E[σ²_{n+t}] = V_L + (α + β)^t · (σ²_n − V_L)
```

Expected average variance from now to T (in days):
```
V(T) = (1/T) · Σ_{t=1..T} E[σ²_{n+t}]
      = V_L + (1 − (α+β)^T) / (T · (1 − (α+β))) · (σ²_n − V_L)
```

This is the GARCH-implied term structure of variance — useful for pricing options of different maturities consistently.

If current vol is above V_L, GARCH forecasts a decline (mean reversion) — and *implied volatility* of longer options will typically be lower than at-the-money short. This is a partial explanation for the term structure of vol but doesn't capture the full smile-vs-tenor surface; for that, see [fat_tails.md](fat_tails.md) (vvol drives smile).

## Correlations under EWMA / GARCH

Multivariate version. Covariance between assets X and Y, EWMA form:
```
cov_n = λ · cov_{n−1} + (1 − λ) · u^X_{n−1} · u^Y_{n−1}
```

Correlation = cov / (σ_X · σ_Y). Each variance updated separately (or by multivariate GARCH).

**Consistency constraint:** the variance-covariance matrix V must be positive semi-definite. For 2 or 3 assets you can update variances and the covariance separately and check by hand. For 5+ assets, naive element-wise EWMA can produce non-PSD matrices.

Solutions:
- **VECH model** — full multivariate GARCH but explodes in parameters
- **DCC (Dynamic Conditional Correlation)** — estimate univariate GARCH for each volatility, then correlation matrix as a separate EWMA-like recursion with PSD enforcement
- **Factor models** — assume returns driven by a low-dimensional factor structure (preserves PSD by construction)

## Practical rules

1. **Use EWMA when you need a fast vol forecast for VaR or sizing.** Set λ = 0.94 for global equities/rates; tune by validation for any asset.
2. **Use GARCH(1,1) when you care about the term structure of vol forecasts.** Especially for option pricing and capital calculations.
3. **Persistence + long-run vol are the two numbers that matter.** A model with α + β = 0.98 forecasts vol returning to V_L over months; α + β = 0.85 forecasts it returning over days.
4. **MLE is unstable on a small sample.** Refit at least monthly on a rolling 5-year window; alert when parameters change meaningfully.
5. **Realized variance from high-frequency data is much more efficient.** If you have intraday data, use 5-min-sampled realized variance — see Parkinson, Garman-Klass, and Yang-Zhang estimators in [volatility_correlation.md](volatility_correlation.md).
6. **For multi-asset, enforce PSD.** Don't ship a covariance matrix without checking eigenvalues — see [correlation_triangles.md](correlation_triangles.md).
7. **GARCH ≠ implied vol surface.** GARCH gives a forecast of *real-world* variance; the *risk-neutral* variance embedded in option prices typically exceeds it (the variance risk premium). Don't conflate.
