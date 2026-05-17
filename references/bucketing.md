# Bucketing and Topography (Ch 14 — lines 10709–11096)

> *"Never hire a very well dressed option trader."* — Ch 14 epigraph

Read this when reporting Greeks on a book of more than ~3 options, especially mixing tenors or strikes, and ALWAYS for path-dependent positions.

## Why aggregate Greeks lie

A single net delta of "+100" on a book can mean radically different things:
- 100 net delta from a single ATM 1-month call (sensible, hedgeable)
- 100 net delta from +500 long 1-year call delta and −400 short 1-week put delta (a calendar position whose net delta is meaningless)
- 100 net delta with all the gamma stacked in one tenor and all the vega in another (a position about to violently shift its own deltas)

**Bucketing = breaking the Greeks down by parameter (tenor, strike, underlying) so the *shape* of the position is visible.**

## Static straight bucketing (line 10726)

The simplest method: for each option, attribute its full Greek to the bucket of its expiration tenor. Useful for European options on stable underlyings; misleading otherwise.

### Worked example from Taleb (line 10752)

GBP-USD position, spot 1.6050. Trader buys a 6-month (183d) ATM call, GBP 100mm notional, paid 4.578%, hedged at 50 deltas.
- 183d USD rate = 5.8438% (360-basis)
- GBP rate = 6.915%

Resulting straight buckets (in USD):
- **Delta:** present value of forward delta. Spot delta = 82,656 / (1 + 0.0183·0.06915) = $79,850k
- **Gamma:** GBP 8,355k — the position picks up that much for a 1% rally (approximate, ignores 3rd derivative)
- **Vega:** $438k per 1 vol-point
- **Rho (foreign / Rho2):** (183/360) × 82,656 × 100bp = $420,168; PV'd = $408k
- **Rho (domestic / Rho1):** $408k − premium-financing exposure ($4.57M × 183/360 × 1bp basis) = ~$385k

The point: **Rho1 ≠ Rho2** and you need *both*, bucketed by tenor, to manage rate risk on FX options.

## Why straight bucketing fails for American / path-dependent (line 10817)

- **American options:** early-exercise risk migrates the effective tenor with the market. As the underlying moves, the option's "remaining life" can shrink unpredictably.
- **Barriers:** a knock-out near its barrier behaves like a *much shorter* option; the same knock-out far from its barrier behaves like a vanilla. The bucket the position belongs in is **state-dependent**.
- **Higher vol shortens KO duration but lengthens American option duration** (line 10836) — opposite effects, same input.
- **Knock-ins and deferred-strike options** start in one bucket and end in another. They are *forward-forward* bucket positions in disguise.

## Forward-forward bucketing (line 10855)

For path-dependent and forward-starting options, the right framework is the **forward-forward bucket**: a 2D grid where the entry is "vega exposure starting at time t₁, ending at time t₂".

### Construction (line 10874)
1. Set up a binomial / Monte Carlo tree
2. Bump vol in *one* time segment, leaving others constant
3. Re-price; the price difference is the vega for that forward-forward bucket
4. Repeat for every (t₁, t₂) cell

For pure-European books, all the rows of the f-f matrix are equal (vol perturbation is location-independent); for path-dependent books, the off-diagonal cells are where the risk lives.

This is computationally expensive — Taleb notes (line 10862) it was a long-standing obsession before numerical techniques caught up.

## Topography — the position's "landscape"

Beyond bucketing, view the book as a function over **(spot × vol × time)**. The "topography" reveals:
- **Cliffs** = barrier proximity (steep ∂Price/∂S regions)
- **Saddles** = mixed long/short gamma profiles
- **Pits** = regions where you lose regardless of direction
- **Plateaus** = regions where the position is benign

A book without a topographic view is a book with hidden cliffs.

## Vega bucketing details

A net vega of "$100k" can be:
- All concentrated at 1m tenor (high vvol exposure, jumps around)
- Spread across 6m–2y (stable, slow-moving)
- A barbell of short 1m + long 1y (calendar play, term-structure exposed)

**Bucket vega by tenor at minimum.** For sophisticated books, also bucket by strike (smile vega):
- ATM vega = exposure to level shift
- 25Δ wing vega = exposure to skew/smile shape

## Practical rules

1. **Never present an aggregate Greek without its bucket breakdown** when the book has > 5 options.
2. **For any path-dependent position**, the straight-bucket Greek is wrong. Compute the f-f bucket or at minimum re-bucket dynamically as the underlying moves.
3. **Rho1 ≠ Rho2 for FX options.** Foreign and domestic rate sensitivities are different Greeks; bucket them separately.
4. **Vega buckets without smile information are still incomplete.** A parallel vol shift is a hypothetical that never happens.
5. **The topography view catches risks aggregate Greeks hide:** sweep spot, vol, and time over realistic ranges and look for cliffs.
