# Fungibility, Convergence, and Stacking (Ch 12 — lines 9747–10346)

> *"Find me an arbitrage in commodities and I will show you a squeeze."* — Ch 12 epigraph

Read this when pricing commodity options, dealing with delivery-specific contracts, or considering "stacking" hedges across tenors.

## Fungibility — what it is (line 9760)

> *"Fungibility refers to the degree of specificity required for the satisfaction of the deliverability obligation. A highly fungible commodity is an abstract one and could be created electronically (like a swap). A nonfungible one is specific and cannot be created at will, such as livestock."*

From the pricing-theory side (line 9769): *"Fungibility reflects the feasibility of risk-neutral replication of a derivative security."*

This is foundational. Black-Scholes-Merton **requires** risk-neutral replication, which requires the underlying to be tradeable in both directions on demand. For non-fungible underlyings, BSM is at best a quoting convention, never a no-arbitrage truth.

## The fungibility ranking

| Level | Examples | Implications |
|---|---|---|
| **Extreme fungible** | Major currencies (USD, EUR, JPY) — bank-created electronically, wired anywhere instantly | BS pricing nearly exact; term structure follows clean cash-and-carry |
| **Highly fungible** | Liquid equities, on-the-run bonds, gold | BS works well, small basis to physical |
| **Moderately fungible** | Off-the-run bonds, IL bonds, commodity futures | Convergence to cash via delivery mechanism; basis risk |
| **Delivery-specific** | Oil at specific grade/location, agricultural commodities | One-way arbitrage; price differences sustained by shipping costs/time |
| **Non-fungible** | Livestock, perishables, physically-delivered with grade specs | No two-way arb; squeeze risk; term structure can be wild |

## The cash-and-carry boundary (line 9881)

For storable commodities:
```
F(t) ≤ S × exp((r + storage_cost − convenience_yield) × t)
```

This is the **maximum contango line**. Forward can't exceed it: an arb can buy spot, store, sell forward, and lock in profit. *Upper boundary only* — forward can go arbitrarily low (backwardation has no equivalent bound).

The example (line 9894): spot = $20, storage = 8% annualized → max-contango line is yield curve + 8%. Forward can sit anywhere below this line.

### Three categories of commodities (line 9904)
1. **Two-way arbitrageable** — currencies, liquid equities, fixed income. BS applies cleanly.
2. **One-way arbitrageable** — physical commodities with carry costs. Max-contango bounds forward from above; nothing bounds it from below.
3. **Non-arbitrageable on time line** — perishables (live cattle, fresh produce, electricity). Term structure pure supply-demand.

## The squeeze (line ~5068, cross-ref Ch 5)

For non-fungible commodities, **open interest can exceed deliverable supply**. Owners of the physical know this and force delivery, creating one-way price moves. Examples Taleb cites:
- Cattle futures with grade specifications: open interest > living animals of that grade
- Squeeze duration = until open interest drops to physical ceiling

**The price during a squeeze isn't a fair price.** It's the maximum a forced short can pay before defaulting. Pricing models that assume continuous risk-neutral measure are wrong here by construction.

## Calendar spreads on non-fungible commodities

> **Risk Management Rule (line 9876):** *A calendar spread in options on cash assets in less fungible commodities needs to be decomposed into its different components and analyzed separately.*

For fungible: a calendar spread is mostly term-structure-of-vol exposure.
For non-fungible: a calendar spread is **two different products** — different supply/demand, different storage, different squeeze risk. Cannot be modeled as one position.

Example: a 1-year vs 2-year crude oil calendar is *not* the same product. The 1-year is exposed to current supply imbalances; the 2-year is exposed to multi-year demand forecasts.

## Convergence

Forward → spot at expiry, for fungible commodities. Convergence speed depends on:
- **Deliverability mechanism** — futures with physical delivery converge precisely; cash-settled converge to the settlement reference
- **Carry cost stability** — if storage costs are volatile, convergence is bumpy
- **Squeeze risk near delivery** — converging futures are vulnerable to delivery-window manipulation

For options on convergent products, **Greeks of the option on cash and option on future become fungible near expiry** (within the variance of carry). Far from expiry, they can diverge meaningfully.

## Stacking (line ~10000+ in chapter)

**Stacking** = hedging exposure across multiple tenors using a single (typically liquid) tenor.

Example: a 2-year FX exposure hedged with 1-month FX forwards rolled monthly. Benefits:
- Lower bid-offer cost (1m liquidity > 2y liquidity)
- Easier to size and exit
Risks:
- **Rollover risk** — basis swap rate between 1m and 2y can move
- **Funding risk** — each roll requires funding the MTM gain/loss
- **Behavioral, not mechanical** hedge: the relationship between short-tenor and long-tenor isn't deterministic

Famous failures of stacking:
- Metallgesellschaft 1993 — stacked long-tenor diesel exposure with short-tenor crude futures. Funding squeeze on the roll forced liquidation at the worst moment.

**Rule:** stacking saves on bid-offer in calm regimes and concentrates risk into the roll moments. The savings are real; the risk is too.

## Greek-fungibility hierarchy (line 9937)

> *"The stability of second derivatives will be higher than first ones, and so on, as one goes into higher order differentials. This means that if the deltas of the 9-month does not properly hedge that of the 3-month, the gamma hedges will be more stable."*

Practical implication: when hedging an exotic with vanillas, **match the highest-order Greek you can** (gamma, vanna, volga) — those relationships are most stable across tenor.

> *"A trader should initially square up his delta in each expiration, then concentrate on the gammas, and so on."*

Bucket by tenor (see [bucketing.md](bucketing.md)), neutralize delta-by-tenor first, then gamma, then vega, then minors.

## Practical rules

1. **Check fungibility before using BS.** For delivery-specific products, BS prices are approximate at best; reality includes squeeze risk that BS can't model.
2. **The max-contango line bounds forwards from above, nothing bounds them from below.** Backwardation can be arbitrary; super-contango cannot.
3. **Calendar spreads on non-fungible commodities are NOT one position.** Decompose and price each leg.
4. **Stacking is a behavioral hedge.** Save it for liquid markets in calm regimes; expect tail risk on the rolls.
5. **Match higher-order Greeks first when cross-tenor hedging.** Delta is the least stable; gamma/vega/vanna are more so.
6. **Near delivery, options on cash and options on future approximately converge.** Far from delivery, treat as separate products.
