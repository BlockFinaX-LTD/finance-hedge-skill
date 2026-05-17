# XVAs — Credit, Funding, and Capital Valuation Adjustments (Hull Ch 9)

The post-2008 reset of derivatives pricing: textbook Black-Scholes assumes risk-free, perfectly-collateralized, frictionless markets. Real derivatives need a stack of adjustments. "XVA" is the umbrella term.

## The adjustments

| Acronym | Name | Adjusts for |
|---------|------|-------------|
| **CVA** | Credit Valuation Adjustment | counterparty might default |
| **DVA** | Debit (Debt) Valuation Adjustment | *I* might default |
| **FVA** | Funding Valuation Adjustment | cost of funding uncollateralized derivatives |
| **MVA** | Margin Valuation Adjustment | cost of funding initial margin posted to CCP / bilateral IM |
| **KVA** | Capital Valuation Adjustment | regulatory capital tied up against the trade |
| **ColVA** | Collateral Valuation Adjustment | non-cash collateral, embedded optionality in CSA |

Default-free Black-Scholes price `f_nd` → adjusted price:
```
f_actual = f_nd − CVA + DVA − FVA − MVA − KVA + ColVA
```
(signs differ by convention; here positive XVAs reduce the dealer's value of an asset.)

## CVA — counterparty default risk

```
CVA = (1 − R) · Σ_i q_i · v_i · DF_i
```
- `R` = expected recovery rate on the counterparty
- `q_i` = unconditional default probability of counterparty in interval i
- `v_i` = expected exposure (positive MTM) at time t_i
- `DF_i` = discount factor

Equivalently: CVA = `(1−R) · ∫ EE(t) · dPD(t)` where EE is expected positive exposure.

Practical drivers:
1. **Exposure profile.** For a swap, expected exposure peaks somewhere mid-life and declines as the swap rolls down. For options, exposure is one-sided (only the long has counterparty risk).
2. **Default probability term structure.** Pulled from CDS spreads of the counterparty (or a credit proxy).
3. **Wrong-way risk.** Exposure and default probability positively correlated → CVA bigger than the formula suggests when the two are modelled independently.

CVA desks at large dealers centralize all counterparty risk and hedge the firm-wide CVA with CDS, equity, FX hedges.

## DVA — your own default

The mirror image. If *you* might default, the value of your *liability* is reduced for the counterparty's loss-given-your-default. By accounting symmetry, you book a GAIN.

```
DVA = (1 − R_self) · Σ_i q_i^self · v_i^negative · DF_i
```

**The counterintuitive effect:** if your own credit deteriorates, DVA increases → you book derivatives-portfolio gains. Goldman, JPM and others booked multi-billion-dollar DVA gains in 2011 quarters when their credit widened.

Reasonable people disagree about whether DVA "should" be recognized. Hedging your own DVA requires shorting your own credit (selling protection on yourself — operationally impossible, structurally awkward). FASB requires DVA disclosure; Basel disallows DVA from regulatory capital.

## FVA — funding cost on uncollateralized derivatives

The dealer's situation: a hedge fund buys an option from Bank A. No collateral on the option. Bank A hedges by trading with another dealer through a CCP — that hedge requires variation margin (collateral).

The collateral the dealer posts has to be **funded** at the dealer's marginal funding cost, not the risk-free rate. FVA = present value of (funding spread × expected variation margin).

Hull's two-sided view (Hull §9.2):
- **Practitioner view:** use average debt funding spread.
- **Hull/White (2012) view:** marginal cost of funding for a risk-free activity is the risk-free rate, not the firm's average funding spread. Using the firm's average funding cost as a project-discount-rate makes safe projects look bad and risky ones look good (the "single WACC problem" from corporate finance).

The debate is unresolved in practice. Most dealers use a funding-cost based FVA but with different spreads (some net it against DVA2, some don't).

## MVA — initial margin funding

Post-crisis regulations require **initial margin** (IM, sometimes called "independent amount") on uncleared derivatives between financial counterparties (UMR — Uncleared Margin Rules, phased in 2016–2022). IM also required by CCPs on cleared trades.

IM is collateral that *stays* with the receiving party throughout the trade — it's funded for the whole life of the trade.

```
MVA = PV( IM(t) · funding_spread(t) )
```

For long-dated swaps with high initial margin requirements (e.g. swaptions, cross-currency swaps), MVA can be 5–20% of the trade's notional value.

## KVA — regulatory capital cost

A derivative position consumes regulatory capital under Basel III (CCR RWA + CVA RWA + market risk + leverage ratio capital). KVA = PV of (capital × required return on capital − risk-free interest the capital would earn).

```
KVA ≈ PV( K(t) · (r_e − r_f) )
```
where K(t) is regulatory capital tied to the trade, r_e is the bank's cost of equity, r_f is risk-free.

For long-dated, uncollateralized trades with high counterparty credit risk weight, KVA can rival CVA in size.

## OIS vs LIBOR discounting (Hull §9.4)

**Pre-crisis convention:** discount all derivative cash flows at LIBOR. Equivalent to assuming LIBOR ≈ risk-free.

**Post-crisis convention:** discount **collateralized** derivatives at the rate paid on the collateral (typically OIS / SOFR / EFFR — overnight, near-risk-free). Project LIBOR-referenced floats with the LIBOR curve.

Result: a swap valued under old (LIBOR-LIBOR) and new (LIBOR-OIS) frameworks gives different prices. The transition was a one-time ~$1tn re-valuation across the industry.

LIBOR transition (USD: SOFR, GBP: SONIA, EUR: €STR, JPY: TONA, CHF: SARON) replaced IBORs by 2023 for new derivatives — fallback language transitioned existing trades.

## Practical rules

1. **Always quote XVA-inclusive prices for non-collateralized derivatives.** CVA alone can be 1–5% of notional for long-dated uncollateralized swaps with weaker counterparties.
2. **Wrong-way risk dominates for autocorrelated counterparties** (e.g. an oil-producing-country sovereign writing oil call options). Model jointly, not independently.
3. **DVA is real for accounting, contested for hedging.** Don't try to monetize it.
4. **MVA and KVA matter most for long-dated uncollateralized or asymmetrically-cleared trades.** For a 30-year swaption, MVA may exceed CVA.
5. **OIS / SOFR discounting is the standard.** If you see LIBOR-LIBOR discounting in code, it's pre-crisis and wrong.
6. **CVA is a one-way street operationally.** Hedging it requires liquid single-name CDS; for counterparties without CDS, use proxy hedges (index CDS + basis estimate).
7. **The XVA stack is not additive in the textbook way.** Components interact (DVA2 reduces FVA, KVA depends on CVA volatility, etc.) — full firm-wide XVA calculations are simulation-heavy.

Cross-link: [hull_credit_risk.md](hull_credit_risk.md) for the default-probability framework underlying CVA, [hull_credit_derivatives.md](hull_credit_derivatives.md) for CDS markets used to imply default probabilities and hedge CVA, [hull_securitization.md](hull_securitization.md) for the 2008 backdrop that motivated XVA.
