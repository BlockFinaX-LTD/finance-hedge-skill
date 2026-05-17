# Credit Risk (Hull Ch 24)

The default-probability framework underlying CVA, CDS pricing, and credit derivatives. Read alongside [hull_xvas.md](hull_xvas.md) (CVA mechanics) and [hull_credit_derivatives.md](hull_credit_derivatives.md) (CDS mechanics).

## Two ways to express default risk

| Concept | Definition |
|---------|------------|
| **Default probability** | Prob[firm defaults by time t] (cumulative) |
| **Hazard rate** (default intensity) `λ(t)` | Conditional default rate: `Prob[default in (t, t+Δt) given survival to t] = λ(t) · Δt` |
| **Survival probability** `S(t)` | `S(t) = exp(−∫₀ᵗ λ(s) ds)` |
| **Cumulative default prob** `Q(t)` | `Q(t) = 1 − S(t)` |
| **Default density** `f(t)` | `f(t) = λ(t) · S(t)` |

If hazard rate is constant: `S(t) = e^(−λt)`, `Q(t) = 1 − e^(−λt)`.

## Real-world vs risk-neutral default probabilities

These are different and the difference is large.

- **Real-world** (P-measure): historical default frequencies. From Moody's transition matrices, rating-letter-to-empirical-default-rate tables.
- **Risk-neutral** (Q-measure): implied from market prices — bond spreads, CDS spreads. Includes a risk premium for systematic default exposure plus liquidity premium.

**Rule of thumb (Hull Ch 24):** Q-measure default probabilities are typically **5–10× larger** than P-measure for investment grade, smaller multiple for high yield. The ratio shrinks for very low-grade credits.

When to use which:
- **Pricing** (any derivative valuation): risk-neutral (Q). Use spreads.
- **Risk management / capital / expected loss / VaR**: real-world (P). Use rating-based default frequencies.

Using P-measure default probs to price CDS will systematically underprice them — that's why the "fair value" of CDS using P-measure looks "cheap."

## Implying default probability from bond yields

If a defaultable bond yields `y` and the equivalent default-free bond yields `y*`, then approximately:
```
y − y* ≈ λ̄ · (1 − R)
```
where λ̄ is the average hazard rate over the bond's life and R is recovery rate.

So: hazard rate ≈ spread / (1 − R).

A 100 bp spread with R = 40% recovery implies λ̄ ≈ 100 / 60 ≈ 167 bp ≈ 1.67% per annum hazard.

This is the **credit triangle**: spread ≈ λ · (1 − R). It's only exact in the limit of small spreads, but in practice it's accurate enough for back-of-envelope work.

## Recovery rates

Average historical recoveries (post-default, by seniority):
- Senior secured: ~50–55%
- Senior unsecured: ~35–40%
- Subordinated: ~25–30%
- Junior subordinated: ~15–20%

Recoveries are negatively correlated with default rates (countercyclical) — when defaults spike, the marginal defaulter has less to recover. This compounds tail loss.

For pricing CDS / CVA, **assume R = 40%** for senior unsecured corporate as the market-standard convention. CDS quotes embed an implied (R, λ) joint; market convention fixes R to back out λ.

## Merton's structural model

A firm's equity is a call option on its assets struck at the value of its debt. Default = equity goes to zero.

Let V be firm asset value, σ_V its volatility, D the face value of debt due at T.
- Equity at time T: E_T = max(V_T − D, 0)
- Today's equity: `E_0 = V_0 N(d_1) − D · e^(−rT) · N(d_2)` (BS call formula)
- Risk-neutral default probability: `N(−d_2)`

```
d_2 = [ln(V_0/D) + (r − σ_V²/2) T] / (σ_V √T)
```

**The Merton inversion:** given observable E_0 and σ_E (equity vol), solve simultaneously for V_0 and σ_V. Then Q(default) = N(−d_2).

KMV (Moody's Analytics) commercialized this with the **distance to default** = `d_2` and a proprietary mapping from DTD to empirical default rates (calibrated to a large database of defaults, so essentially mapping risk-neutral d_2 to real-world default probabilities).

## Counterparty credit risk

Derivatives counterparty risk is **bilateral and exposure-dependent**:
- If MTM > 0 to you, the counterparty owes you and you have counterparty risk.
- If MTM < 0, you owe and have no counterparty risk (but the counterparty does).

**Expected exposure** at time t: `EE(t) = E^Q[max(V(t), 0)]`. Hull simulates the derivative's MTM path under Q and averages the positive part at each time.

CVA = `(1 − R) · ∫₀ᵀ EE(t) · dPD(t)` (see [hull_xvas.md](hull_xvas.md)).

For a single uncollateralized IRS:
- Exposure profile rises mid-life (most time-value at risk), then falls as the swap rolls down.
- For an FX forward, exposure rises monotonically (single bullet payment).
- For a long option position (e.g. you bought a swaption), exposure profile mirrors the option's value path.

## Netting and collateralization

Without netting: counterparty exposure = `Σ max(V_i, 0)` (sum of positive MTMs across all trades).
With netting (ISDA master agreement): counterparty exposure = `max(Σ V_i, 0)` (positive MTM after netting all trades).

Netting can reduce gross exposure by 50–90% for a large bilateral book.

Collateral (CSA — credit support annex) further reduces exposure. With daily margining:
- Exposure ≈ MTM moves over the close-out / cure period (typically 10 business days) before default
- For perfectly collateralized counterparties, CVA is tiny but not zero (close-out period exposure + margining frictions)

## Wrong-way risk

When exposure and counterparty default probability are positively correlated. Examples:
- Buying CDS protection on Company X from Bank Y that holds X's debt (Bank Y defaults exactly when X does)
- FX forward to receive emerging-market currency from a bank in that country (devaluation = both bank weakness and exposure spike)
- Equity TRS where the underlying is the counterparty's own stock

Wrong-way risk dramatically increases CVA. Hull Ch 24 recommends modeling jointly via copula or factor-correlated default + exposure model rather than naively scaling CVA.

## Rating transition matrices

Moody's / S&P publish empirical transition matrices: probability of moving from rating X to rating Y over a horizon (typically 1 year).
```
[AAA → AAA] [AAA → AA] [AAA → A] ... [AAA → D]
[AA → AAA]  [AA → AA]  [AA → A]  ... [AA → D]
...
```
Used to model credit migration, not just default — useful for portfolios where rating downgrades trigger forced selling.

## Practical rules

1. **Q ≠ P for default probabilities.** Use Q (spreads) for pricing, P (history) for capital and stress testing. Mixing them is a common error.
2. **Credit triangle: `spread ≈ hazard × (1 − recovery)`.** Memorize this. It's the back-of-envelope CDS quote.
3. **Assume R = 40% for senior unsecured corporates.** Market standard for CDS.
4. **Wrong-way risk is not a footnote.** For sovereign / single-name CDS, wrong-way drives CVA. Model jointly.
5. **Netting reduces exposure dramatically.** When evaluating a new trade, always compute its *incremental* contribution to netted exposure, not its standalone notional.
6. **Recovery negatively correlates with default rate** — stress your recovery assumption down 10–20% in tail-loss calculations.
7. **Merton model gives you distance-to-default, not real-world PD.** Calibrate the mapping if you need empirical default rates.

Cross-link: [hull_credit_derivatives.md](hull_credit_derivatives.md) for CDS market mechanics, [hull_xvas.md](hull_xvas.md) for CVA formula and implementation, [hull_securitization.md](hull_securitization.md) for portfolio credit derivatives (CDOs).
