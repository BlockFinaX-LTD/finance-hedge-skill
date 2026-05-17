# Numeraire Relativity and the Two-Country Paradox (Module C — lines 18406–18698)

Read this when pricing FX options, hedging across currencies, or any time the P/L "feels different" depending on which currency you measure in. It's the most subtle and most-violated principle in FX option pricing.

## Numeraire — what it is (line 18411)

> *"A base currency for an operator, also called a numeraire, is one in which his final P/L is expressed. A countercurrency is the one that corresponds to the number of units traded."*

A numeraire can be:
- A currency (most common: USD, EUR, GBP)
- A stock index ("SP500-based investor")
- A bond fund
- A commodity (gold for a gold miner)
- Anything else you measure your wealth in

Traders working in USD think USD is "natural" and everything else is "an asset". That's a parochial view. To a EUR-based trader, USD is the asset. **Both views are equally valid; the math has to handle both.**

## The non-trivial invariance: P/L depends on numeraire (line 18430)

> *"The notion is counterintuitive because in most people's minds a currency pair is invertible. A JPY against the USD is the inverse of the USD against the JPY. However, although the equality will apply to the price, it will not apply to the profits and losses since the P/L will be caused by currencies diverging and that such divergence will cause a change in the yardstick."*

**The price is invertible, the P/L is not.** When USD/DEM moves from 1.40 to 1.50, a DEM-based trader on the long-USD side makes DEM 1,000,000; a USD-based trader doing the inverse trade (long DEM, short USD at 1/1.40) doesn't make $666,400 on the same notional — the dollar amount changes because the inverse rate changes asymmetrically.

### Worked example from Taleb (line 18488)
- Trader buys $10M USD at USD/DEM = 1.40 → controls DEM 14M
- Market rallies to 1.50 → trader sells $10M → makes DEM 1M
- If he's DEM-based: clean profit DEM 1M, no further risk
- If he's USD-based: he has DEM 1M and needs to convert back to USD — exchange rate risk on the profit itself

To replicate the inverse trade as a USD-based person: trade DEM 14M (not $10M). Enter at 1.40, exit at 1.50 (= 1/0.6666). Need to trade $9,333,333 at exit to be square in DEM units.

**The lesson:** the units of the trade depend on which numeraire you're hedging to.

## A put on USD/DEM is a call on DEM/USD (line 18438)

Same instrument, two views. Implication:
- A long-USD call with USD as numeraire = a long-DEM put with DEM as numeraire (mirror image)
- The Greeks look different from each side!
- Delta in USD-base is not the inverse of delta in DEM-base — there's a relativistic correction

For the dollar-based trader: USD/DEM going to infinity = pure short DEM, limited downside risk. For the DEM-based trader: that same move = USD/DEM going to infinity = unlimited upside on long-USD position.

**Both are right.** Both are about the same underlying.

## The Two-Country Paradox (line 18533)

Two traders, German and American. USD/DEM = 1.42. Interest rates equal. Forward = 1.42 (no carry). Both have "view" that the other's currency will weaken.

Build a binomial tree under risk-neutrality. Per Module G, the up-move probability for USD/DEM is:
```
p = (1 - d) / (u - d) = (1 - exp(-σ√t)) / (exp(σ√t) - exp(-σ√t))
```

For 20% vol, 6 months:
- u = exp(0.20 × √0.5) = 1.152
- d = exp(-0.20 × √0.5) = 0.868
- p_up ≈ 46.47%
- p_down ≈ 53.53%

The German (numeraire = DEM): expected USD/DEM at expiry = 1.42 × (1.152 × 0.4647 + 0.868 × 0.5353) = 1.42 ✓

But invert each cell to look at DEM/USD: the expected DEM/USD = 1/1.42 × ... ≠ 1/1.42! Because of Jensen's inequality on the exp: **the expected value of 1/x is not 1/expected(x)** for a convex function.

So: the German expects USD/DEM to stay at 1.42, BUT he expects DEM/USD to APPRECIATE.

Meanwhile, the American (numeraire = USD): expected DEM/USD to stay at 1/1.42 = 0.7042, but expects USD/DEM to APPRECIATE.

**Both traders correctly believe their own currency will strengthen relative to the other.** This is the paradox: under the same risk-neutral measure, each numeraire sees its own asset as appreciating against the other.

## The mathematical resolution: Siegel's paradox

The convexity adjustment is `(1/2) × σ² × t`. The expected value of `1/S` exceeds `1/E(S)` by this term. So the German sees a DEM/USD expected appreciation of about `0.5 × 0.20² × 0.5 = 0.01` (1%) in log terms — and the same applies symmetrically for the American.

This is a real economic effect: **the convexity of currency cross-rates creates a perceived appreciation in each direction**. It does not violate no-arbitrage; it's a feature of lognormal pricing in multiple numeraires.

## Practical implications for option pricing

### Different deltas in different numeraires (line 18594)

> *"A call on dollar-mark will therefore not have the same delta as a put on mark-dollar."*

Same option viewed from two sides has two different deltas. Reason: the units of the delta differ.
- USD/DEM call delta is in "DEM per USD per USD-spot move"
- DEM/USD put delta is in "USD per DEM per DEM-spot move"

These differ by a Jacobian.

### Numeraire flipping (line 18601)

> *"Numeraire flipping consists of switching the unit in which the numeraire is expressed from base currency to counterasset."*

Practical use:
- Hedging a position naturally denominated in one currency from the perspective of another
- Pricing an option struck in a non-standard numeraire (e.g., a USD-strike option on USD/JPY)

### Risk Management Rule (line 18514)

> *"A position in a numeraire is considered neutral. A residual long the numeraire will be positive P/L, a residual short the numeraire will be negative P/L."*

The numeraire balance is invisible — it's "cash" in the relevant currency. Everything that's not the numeraire is an open position.

A DEM balance is square for a German trader and open for a US trader. A USD balance is the opposite.

## Practical rules

1. **State the numeraire explicitly for every FX option you price.** "Long USD/DEM call" is ambiguous — say "USD-base" or "DEM-base".
2. **The price is invariant under numeraire change. The Greeks are not.** Translate carefully.
3. **The two-country paradox is real, not an arbitrage.** It's Jensen's inequality on lognormal returns.
4. **Use Garman-Kohlhagen as the FX-version of BS:** r_d = domestic, r_f = foreign (acts like q). But remember "domestic" depends on the numeraire.
5. **For pegged or managed currencies, both views matter.** A USD-based trader on long USD/HKD has different risk than a HKD-based trader on short HKD/USD even though they're the same trade. Capital controls and convertibility risk hit asymmetrically.
6. **Hedging clients in a foreign currency: confirm which currency the hedge is FOR.** Hedging USD-revenue for a German client → numeraire is DEM, not USD.
