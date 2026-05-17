# Arbitrage and the Arbitrageurs (Ch 5 — lines 4874–5267)

Read this when: building a relative-value trade, judging whether a "free lunch" is real, or evaluating risk vs return on a "spread" position.

## Traders' definition vs. academic definition (line 4885)

- **Academic:** a linear combination of securities costing 0 that can have positive value but never negative value.
- **Trader:** the **expected value** of a self-financing portfolio (which CAN be negative) is positive.

Traders are far more permissive — they call lots of things "arbitrage" that academics would call risky trading. **Mind the gap.** "Risk arbitrage" in equities (M&A) has *nothing* to do with arbitrage — it's directional with extra steps.

## Mechanical vs. behavioral stability (line 4926)

The single most important distinction in the chapter.

| | Mechanical | Behavioral |
|---|---|---|
| Link type | Identifiable, reproducible | Established by historical records |
| Robustness | Should survive market moves | Stable until regime shift |
| Hedge quality | Ironclad | "Apparent" — booby trap potential |
| Examples | Cost-of-carry, cross-currency triangle, knock-in + vanilla = knock-out, forward-forward box | US-Canada swap curves, DEM-CHF (until Berlin Wall fell), corp bond hedges |

**Taleb's warning (line 4949):** *"These apparent relationships provide the market with booby traps."* Anything established by correlation alone breaks in the regime where it matters most.

## Deterministic relationships (line 4955) — examples

- A **basket** = sum of components → replicable exactly
- A **cross-currency** = ratio of two USD pairs → replicable exactly
- A **knock-out call** = vanilla call − knock-in call (same strike/barrier) → replicable exactly via Ch 19 static replication
- **Put-call parity:** C − P = S·e^(-qT) − K·e^(-rT) → deterministic, holds always

When you hedge a deterministic relationship, the P/L on expiration is locked **regardless of market path**.

## Behavioral relationships — examples and risks

- **Bond vs swap** — stops tracking in credit-stress crises (line 4982: Italian example, US flight-to-quality)
- **Currency stacking** — using DEM as a proxy for EUR-area exposure: works until it doesn't (regime shifts)
- **VaR-implied hedges** — same fragility (the correlation matrix used was calm-regime)

The general principle: **correlation-based hedges are short the correlation itself**. They're short volatility-of-correlation. When everything correlates to 1 in a crisis, every behavioral hedge fails simultaneously.

## Passive arbitrage (line 5002)

The capital-neutral swap of an asset for a similar one with better features. Examples:
- Switching a bond for a higher-yielding bond of same duration/credit
- Replacing a stock with a convertible when convertibles are discounted due to borrow costs
- Rolling along the yield curve to the cheapest issue

**Passive arbitrage has structural advantages over active:** the passive arb already owns the security, so they don't pay the high repo/borrow costs an active arb faces. They capture the discount that exists *because* active arbs can't fully arb it.

## The "squeeze" — an absorbing barrier (line 5068)

A trade can be mechanically perfectly hedged and *still* blow up because of a **squeeze** — when one leg can't be funded/borrowed/financed at expected cost. Examples:
- Short bond → repo cost spikes when bond becomes special
- Short stock → borrow rate spikes 100x in crowded short
- Box spread → counterparty failure on one leg

A squeeze is an **absorbing barrier**: once hit, the trade can't be brought back to its theoretical state.

## Arbitrage and the variance of returns (line 5160)

Active arbitrageurs face a counterintuitive result: increasing the number of "arbitrage" positions can *increase* portfolio variance if the positions share a common factor (squeeze risk, liquidity risk, model risk).

This is why LTCM-style books are dangerous: many small "uncorrelated" arbs that turn out to share a hidden factor (in 1998: flight to quality liquidity).

## Practical rules

1. **Test every "arbitrage" for mechanical vs. behavioral stability.** If you can't write down the deterministic link, it's a directional bet with extra steps.
2. **Squeeze risk is a hidden short option** on funding/borrow. Price it explicitly when sizing the trade.
3. **Static replications are deterministic; dynamic ones are behavioral.** Prefer static when feasible (especially for barriers — Ch 19).
4. **Correlation in calm ≠ correlation in stress.** Stress-test all multi-leg trades with correlation forced to extremes.
5. **Passive arbitrage often beats active** when you can be naturally on the right side of borrow/repo asymmetries.
