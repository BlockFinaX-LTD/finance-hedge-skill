# Probabilistic Rankings in Arbitrage (Module F — lines 19270–19579)

Stochastic-dominance rules: ways to bound option prices without a pricing model. Useful for sanity-checking quotes, detecting arbitrage, and pricing illiquid options by interpolation.

## The core concept: stochastic dominance (line 19292)

> *"When an instrument or combination of instruments is at least as valuable as another set, the author will use the sign ≥ to express the inequality. Instrument A ≥ B means that A in all possible events (under all parameter changes) is deemed to be at least equal to instrument B."*

**Stochastic dominance** = one payoff dominates another in every state of the world. This gives **model-free** price relationships: A ≥ B implies price(A) ≥ price(B), no matter what model you use.

Veteran option traders price entire chains using just these rules — *"trading without 'sheets'"* (line 19332).

## European option rules

### Strike monotonicity (line 19312)

For European calls C(K, T) with strike K:
- `C(K1, T) ≥ C(K2, T)` if K1 ≤ K2 (lower-strike call always ≥ higher-strike call)

For European puts P(K, T):
- `P(K1, T) ≥ P(K2, T)` if K1 ≥ K2 (higher-strike put always ≥ lower-strike put)

This is immediate from the payoff: a lower-strike call has weakly higher payoff in every state.

### The butterfly rule (line 19319)

For three equally-spaced strikes K1 < K2 < K3 (with K2 = (K1 + K3)/2):

```
2·C(K2, T) ≤ C(K1, T) + C(K3, T)
```

Or equivalently: `C(K1) - 2·C(K2) + C(K3) ≥ 0`. The butterfly is non-negative.

**Why:** the butterfly payoff is zero everywhere except in the "eye" around K2, where it's positive. It can't be worth less than zero.

By put-call parity, same rule for puts:
```
2·P(K2, T) ≤ P(K1, T) + P(K3, T)
```

### Strike convexity (corollary)

Option price as a function of strike is **convex**. The butterfly rule above is exactly the discrete-second-derivative-is-positive condition.

> *"They [veteran traders] can price the entire spectrum using a small number of options."*

If you know prices at K1, K3, K5 you can bound C(K2) and C(K4) by convexity. With a smooth interpolation you can quote the whole chain from a few points.

### Straddle vs strangle (line 19340)

A straddle (same strike K, both call and put) is ≥ a strangle (call at K_high, put at K_low ≤ K ≤ K_high). The straddle has wider profit at expiry for the same moneyness.

## Calendar rules (line 19346)

For a longer-dated straddle vs. shorter-dated straddle:
```
Straddle(K, T2) ≥ Straddle(K, T1)  for T2 > T1
```
(after taking financing into account / in present-value terms)

**Exceptions** (line 19357): for non-fungible underlyings, this can fail. A longer-dated option on perishable cattle can be cheaper than a shorter-dated one because long-dated cattle simply can't exist. Fungibility matters (see [fungibility.md](fungibility.md)).

For **serial options** (different expiries on the same underlying future), the calendar rule holds unconditionally.

## Barrier and digital rules (line 19364)

### Barriers reduce value

```
C(S, K, T)  ≥  C_KO(S, K, T, H_high)   (knock-out is worse than vanilla)
C(S, K, T)  ≥  C_KO(S, K, T, H_low)    (down-out KO is worse than vanilla)
```

A no-barrier call is always worth at least as much as one with a knock-out barrier.

### Barriers closer to spot reduce value more

Any barrier option is worth more if the barrier is FARTHER from spot. Approaching the barrier reduces value because the option's "death probability" rises.

### Single barrier dominates double barrier

For a shared trigger H:
```
Single-barrier(H) ≥ Double-barrier(H, H')
```

A double barrier has two ways to die; a single only one.

### American digital vs European digital

American (if-touched) ≥ European (at-expiry). The American pays off if the event happens at any time; the European only at expiry. The American captures more states.

## Correlation rules (line 19396)

For at-the-money straddle prices or implied volatilities, in a three-currency world A, B, C (using A as numeraire):

### Triangle inequality on volatilities (line 19408)
```
|v(A-B) - v(A-C)|  ≤  v(B-C)  ≤  v(A-B) + v(A-C)
```

The cross vol v(B-C) must be inside the triangle range bounded by the legs.

### Implied correlation must be in [-1, 1] (line 19421)

> *"Given three security pairs, implied volatility between them cannot be such that one of the implied correlations exceeds 1 in absolute value."*

If quotes imply |ρ| > 1, the quotes are arbitrageable in principle.

### Positive-definite implied covariance matrix (line 19437)

> *"An implied covariance matrix (implied from at-the-money option prices) needs to be positive definite (its eigenvalues need to be positive definite)."*

For larger universes (5+ assets), check the full implied covariance matrix's eigenvalues. Negative eigenvalues = arbitrage.

### Worked example (line 19458)

For vol(USD/DEM) = 14% and vol(DEM/FRF) = 4%:
- The minimum allowable vol(USD/FRF) is 10% (achieved at ρ = +1)
- The maximum allowable vol(USD/FRF) is 18% (achieved at ρ = -1)

Outside [10%, 18%], a correlation arbitrage exists:
- Below 10%: buy USD/FRF + DEM/FRF, sell USD/DEM → short correlation at the boundary
- Above 18%: opposite → long correlation at the boundary

These are correlation arbs but **the locked profit depends on terminal cross-currency P/L**, which isn't deterministic across all numeraires — so it's not a "perfect" arbitrage in the strict sense, but it's a high-probability mispricing.

## What about American options?

The book primarily uses these rules for Europeans because the optimal-exercise complication breaks some inequalities. For Americans:
- American call ≥ European call (always)
- American put ≥ European put (always)
- The strike-monotonicity and butterfly rules still hold
- The calendar rule may fail for deep-ITM Americans (the rolldown to expiry can dominate the time-value gain)

## Practical applications

### 1. Sanity-check broker quotes
Compute the butterfly. If negative, the quotes are inconsistent — either an arb or a quoting error. Most often it's a quoting error.

### 2. Interpolate the smile
Given prices at a few strikes, use the convexity-in-strike constraint to bound prices at intermediate strikes. Better than linear interpolation.

### 3. Detect smile-shape inconsistencies
The butterfly-must-be-positive rule is **the** constraint on arbitrage-free smile fits. SVI and SABR (see [scripts/smile_fitter.py](../scripts/smile_fitter.py)) satisfy it by construction; ad-hoc spline fits often don't.

### 4. Compare exotic to vanilla
Whatever exotic you're pricing, you can bound it by appropriate vanilla portfolios using these rules. Useful for sanity-checking your model.

### 5. Price illiquid options by ranking
For an illiquid strike, find liquid strikes that bound it from both sides via these rules. Your fair price is in the bounded range. The range tightens as you add more liquid quotes.

## Practical rules

1. **The butterfly is non-negative.** This is THE arbitrage-free constraint on a smile.
2. **Calendar-vol must be non-decreasing in tenor for serial options.** Exceptions exist for non-fungible underlyings.
3. **Barriers monotonically reduce value.** Closer barrier = bigger reduction.
4. **The implied covariance matrix must be positive semi-definite.** Check eigenvalues for multi-asset quotes.
5. **For three currencies, |ρ| ≤ 1 constrains the vol triangle.** Use [correlation_triangles.md](correlation_triangles.md) to enforce this.
6. **Use rankings to bound illiquid options.** Veterans price entire chains by rank alone — it's a powerful technique.
