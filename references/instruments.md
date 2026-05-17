# Introduction to the Instruments (Ch 1 — lines 1681–2910)

The framework chapter. Establishes the conceptual vocabulary used throughout the book. Read first when you're new to derivatives, or when you want to verify that your classification of a product is correct before pricing it.

## What a derivative is (line 1700)

> *"A derivative is a security whose price ultimately depends on that of another asset (called underlying)."*

Range from simple (futures) to complex (exotics), with everything in between.

## The single most important split: linear vs. nonlinear (line 1708)

| | Linear | Nonlinear |
|---|---|---|
| Definition | First-order only (no second derivative) | Second derivative ≠ 0 |
| Hedging | Lock in completely with another linear instrument | Requires **dynamic hedging** |
| Greeks | Delta only | Delta, gamma, vega, theta, rho, plus minors |
| Examples | Forwards, futures, swaps | Options, callable bonds, structured notes |
| Time value | None | Carries time decay ("rent") |

> **Risk Management Rule (line 1724):** *All nonlinear derivatives are time-dependent in their price.*

This is the **contamination principle**: nonlinearity = gamma = convexity, and gamma always comes with theta. You can't have one without the other. (Free convexity would be free money — it doesn't exist.)

## The Greeks — basic definitions (line 1736)

These are introduced briefly in Ch 1 and expanded in Ch 7–11. Quick reminder:

- **Delta** — sensitivity of option price to underlying price
- **Gamma** — sensitivity of delta to underlying price (second derivative)
- **Vega** — sensitivity to implied volatility
- **Theta** — expected price change with passage of time at risk-neutral growth
- **Rho** — sensitivity to interest rates or dividend yield

"Long gamma" / "long vega" = positive sensitivity (a higher P/L at higher gamma/vega).

For the full treatment, see [greeks.md](greeks.md).

## The Hedger's viewpoint (line 1766)

Two parties, two utility functions:
- **User** — cares about terminal value (cash flows at expiry)
- **Manufacturer (dynamic hedger)** — cares about replication cost along the path

For a dynamic hedger, "long call" and "long put" are nearly the same risk once the spot hedge is in place — **what matters is strike and expiration**. This is non-obvious to users and a frequent source of confusion in client conversations.

## Synthetic securities and the Mirror Image Rule (line ~22)

**Put-call-asset arbitrage (the synthetic):**
- Long stock + long put = long call + (cash short bond)
- Long call − long put = forward
- Combinations of these decompose ANY linear or option-vanilla payoff into others

**Mirror Image Rule:** every option strategy has an equivalent strategy on the opposite side achieved by changing the underlying position. A short put + short stock = short call (delta-wise, with strike/expiry alignment).

This is one of the few **purely deterministic** relationships in the book — see [arbitrage.md](arbitrage.md) for "mechanical vs. behavioral" distinction.

## Hard and soft optionality (line ~20)

- **Hard optionality** — explicit, contractual right to do or not do something (the rights in a vanilla option contract).
- **Soft optionality** — embedded, structural, not contractually explicit. Examples: a borrower's prepayment right, an insured's lapse right, a customer's renewal right.

Soft options are everywhere in non-traditional contracts. They are **underpriced systematically** because users don't see them as options. The deal you signed has more optionality than the contract spells out.

## Early exercise and American options (line ~508)

- **Soft American options** — early exercise rarely optimal (most American calls on non-dividend stocks: never exercise early; American puts: sometimes).
- **Hard American options** — early exercise meaningful (deep ITM American puts; American calls just before a discrete dividend).

**Warning about early exercise tests (line ~519):** standard binomial tests assume continuous risk-neutral growth. In stress or near discrete events (dividends, expiry cusps), the tests fail. Don't trust automatic early-exercise pricing for paths near corporate events.

## Forwards, futures, forward-forwards (line ~522)

- **Forward** — OTC, no daily mark-to-market, principal credit exposure, single cash flow at delivery
- **Future** — exchange-traded, daily MTM, margin, settled to fund continuously
- **Forward-forward** — a forward starting at a future date and expiring at another future date

### Marks-to-market differences (line ~530)
Daily MTM on futures creates a *correlation between the financing rate and the underlying*. If rates and the underlying are correlated, this creates a small convexity adjustment vs the forward price. Matters for FX and rates, less for equities.

### Credit
- Forward: full bilateral counterparty credit
- Future: margin + clearinghouse (effectively zero credit if exchange solvent)

This is why a "forward" and a "future" on the same underlying differ in price beyond carry effects.

## Primary vs. secondary risks (line ~538)

> **Core Risk Management:** distinguish primary and secondary risks.

- **Primary risk** = the risk the instrument is intended to take (long-spot risk on a forward, long-vega on a long call)
- **Secondary risk** = side effects (rho, basis risk, settlement risk, model risk)

A position can be hedged on primary risk and still blow up on secondary. The 2008 example: AIG super-senior CDS were "hedged" on primary credit risk but exposed on secondary collateral / liquidity risk.

**Rule:** enumerate all the Greeks (and non-Greek risks) of any position before sizing it. The primary risk is the one you priced; the secondary risks are the ones that bite you.

## Applying the framework to specific instruments (line ~542)

For every product, ask:
1. Linear or nonlinear? In which parameters?
2. Hard or soft optionality?
3. Path-dependent? American / European / Bermudan?
4. Primary risk vs. secondary risks?
5. Fungible or delivery-specific? (See [bucketing.md](bucketing.md) and Ch 12.)
6. Mechanically or behaviorally arbitrageable? (See [arbitrage.md](arbitrage.md).)

If you can answer these six before reaching for a pricer, you've avoided 80% of mispricings.

## Practical rules

1. **Test linearity in every parameter, not just spot.** A position can be linear in spot and dramatically convex in vol.
2. **Soft options live everywhere.** Look for them in client contracts, employee comp, prepayment terms.
3. **Dynamic hedging makes every nonlinear product time-decaying.** The "rent" you pay (theta) is the price of the convexity you own.
4. **Primary risk is what you priced. Secondary risk is what kills you.** Enumerate both.
5. **Forwards ≠ futures, even with same maturity and underlying.** Daily-MTM convexity matters for rates and FX.
