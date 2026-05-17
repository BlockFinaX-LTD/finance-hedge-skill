# Option Trading Concepts (Ch 16 — lines 11787–12454)

> *"Hiring a trader is like selling volatility. If he does very well or very poorly, you are out of a job."* — Ch 16 epigraph

This chapter packages the *practical* trading vocabulary: replication, spreading, neutrality. Read it when reasoning about how to structure a trade, not just price it.

## Option replication — three flavors

1. **Static replication** (line 11809) — find a portfolio whose payoff matches the option's, with no rebalancing required. Reduces P/L variance AND transaction costs.
2. **Dynamic replication** (line 11880) — maintain Greek neutrality through continuous rebalancing. The Black-Scholes-Merton paradigm. Makes every option **path-dependent in practice** (line 11894).
3. **Decomposition** ≠ replication — sometimes you decompose a payoff for value discovery (e.g., revealing skew risk) without intending to replicate.

The simplest static replication is **put-call-asset arbitrage** (line 11815): a long call + short stock = long put + short bond (synthetically). Always works.

**Warning (line 11819):** never statically replicate an instrument with a *stopping time* (unstable duration, e.g., barrier, American) using instruments with *constant duration* (vanillas to expiry). The duration mismatch sneaks in path risk.

## Derman's static replication (line 11832)

For barriers especially:
1. Build a binomial tree
2. Walk back from expiry, replicating the payoff at as many nodes as possible using vanilla options
3. The resulting vanilla portfolio approximates the barrier's payoff

Taleb's extension (line 11843): match **payoffs AND Greeks** at every node (delta, modified gamma/vega, theta, Rho1, Rho2, bleed, correlation delta). The "best static hedge matches all Greeks across all states."

Tradeoff: matching all Greeks may consume the trade's edge in bid-offer cost across many illiquid lines.

## Dynamic hedging — what it really means (line 11880)

> *"Dynamic hedging implies sticking to a minimum Greek exposure and rebalancing continuously to achieve a certain neutrality."*

Notes from Taleb:
- It doesn't try to fully replicate; it manages residual exposures
- It re-balances delta as the market moves AND as delta bleeds with time
- It uses options (not just spot) to manage gamma evolution
- It manages Rho1 and Rho2 as rates move
- **Side effect:** under dynamic hedging, every option becomes path-dependent (line 11894). The P/L from hedging is realized along the path, not at expiry.

## Neutral spreading (line 11899)

Buying one option against selling another with different strikes/expirations — a form of dynamic hedging with explicit Greek constraints.

### Advantages (line 11944)
- **Captures the central limit:** reduce variance (luck), maximize drift (skill).
- **Insulates from formula risk:** if BS misprices OTM options, a spread of two OTMs cancels much of the bias. *"Both options would be (mis)priced, so the relative trade is robust."* (line 11949 — paraphrased)
- **Allows market-making edge to compound:** spreaders are valued by exchanges, get leverage.

### Caveats
- Spread distance matters: too far apart and the spread becomes a directional bet
- **Skew makes downside strikes structurally different from upside strikes** (line 11912). A 5% OTM put is not a 5% OTM call.
- For exotics: the rules extend, but distances between strikes/expirations become harder to assess.

## Risk reversals, butterflies, calendars (mentioned across Ch 16)

| Structure | Composition | Primary exposure |
|---|---|---|
| **Risk reversal** | Long OTM call + short OTM put (or reverse) | Skew. Vanna-heavy. |
| **Butterfly** | Long wings, short body (3 strikes) | Kurtosis / vol-of-vol. Volga-heavy. |
| **Calendar** | Long far-month, short near-month, same strike | Term structure of vol. |
| **Diagonal** | Different strikes AND tenors | Combined skew + term-structure |
| **Straddle / strangle** | Long call + long put (same / different strikes) | Pure long vol / gamma |

A market maker reading customer flow uses these structures to decompose what the customer is paying for: *"They're paying up for the put-side skew"* vs. *"They want short-dated convexity."*

## "Bleed" — the time-decay of every Greek

Bleed = ∂(Greek)/∂t — how each Greek decays through time, independent of spot/vol moves:
- Delta bleeds (charm)
- Gamma bleeds (color)
- Vega bleeds
- Even rho bleeds

For dynamic-hedged books, bleeding Greeks change the rebalancing needs day to day. Reporting Greeks "as of close" without their bleed predicts tomorrow's hedge poorly.

## Practical rules

1. **Prefer static replication for barriers and binaries.** Dynamic hedging through discontinuities is operationally insane (Ch 7's "half billion-dollar delta").
2. **Spread strategies beat outright long/short** for market makers because they cancel formula risk.
3. **Spreading across skew is structurally different from spreading across the smile body.** Calls aren't the mirror of puts.
4. **Calendars are about term structure, not directional vol.** Don't model a calendar as ratio of two vegas — model the forward-vol.
5. **Bleed reporting matters more than spot-vol Greeks for short-dated books.** A 1-week ATM straddle is mostly theta/gamma, and both bleed nonlinearly to zero.
