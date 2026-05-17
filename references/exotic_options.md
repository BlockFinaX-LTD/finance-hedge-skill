# Exotic Options Playbook

Chapter-by-chapter notes for pricing each exotic family. Source lines reference `dynamic_hedging.md`.

## Binary (digital) options — Ch 17 (Eur, lines 12510–13463) & Ch 18 (Am, lines 13464–14110)

### European cash-or-nothing (pays $1 if S_T > K, else 0)

- **Closed form (BS world):** `C_digital = e^(-rT)·N(d2)`
- **The trap:** flat-vol BS digital ignores the smile, but the digital price is exactly `−∂C_vanilla/∂K` — fully smile-determined. Always price digitals from the **smile slope at K**, not flat vol.
- **Practical:** quote and trade digitals as **call spreads** with a narrow width (e.g., K and K+ε). Width ε reflects your bid-offer.

### American binary (one-touch, no-touch)

- One-touch: pays $1 if S ever crosses K before T
- Reflection-principle closed form exists under GBM
- **Risk profile is brutal:** delta goes vertical at the barrier; gamma is a delta function. Static replication is the right approach (Ch 19).

## Barrier options — Ch 19 (lines 14111–15314) & Ch 20 (lines 15315–16338)

### Types

- **Knock-out:** option dies if barrier touched (down-and-out call, up-and-out call/put, etc.)
- **Knock-in:** option activates only if barrier touched
- **Double barrier:** both upper and lower
- **Window barrier:** barrier only active in a sub-interval

### Pricing

- **Continuous monitoring, GBM, flat vol:** Merton/Rubinstein-Reiner closed-form
- **Discrete monitoring:** apply Broadie-Glasserman-Kou correction: shift barrier by `±0.5826·σ·√(Δt)` (factor based on ζ(1/2))
- **With smile:** Monte Carlo with smile-consistent dynamics (local vol or stochastic vol)
- **Static replication (Ch 19):** replicate a barrier with a strip of vanillas. Robust to model risk.

### Risk management

- The famous "half billion-dollar delta" story is a barrier-option story (Ch 7 lines 6223–6253). Continuous-time delta near a barrier can be 10,000% but the actual risk is bounded by the option's maximum payoff.
- **Pin risk** near the barrier: small spot moves cause large P/L
- **Hedge with vanillas + a barrier-specific overlay**, never with continuous delta
- The right Greek to monitor near a barrier is **gamma w.r.t. time and vol**, not just spot

## Lookback options — Ch 23 (lines 17411–17769)

- **Floating-strike lookback:** payoff is `S_T − min(S_t)` (call) or `max(S_t) − S_T` (put)
- **Fixed-strike lookback:** payoff is `max(0, max(S_t) − K)` (call)
- **Closed form** under GBM, continuous monitoring: Goldman-Sosin-Gatto (1979)
- **Discrete monitoring:** Monte Carlo or analytical adjustment

Lookbacks are **expensive** — they have positive convexity in everything. Use sparingly.

## Asian options — Ch 23 (lines 17411–17769)

- **Average price option:** strike is the average of S_t over a window
- **Average strike option:** payoff against the average

### Geometric Asian
- Closed-form (the geometric mean of lognormals is lognormal)
- Useful as a control variate for arithmetic Asian Monte Carlo

### Arithmetic Asian
- No closed-form
- **Turnbull-Wakeman approximation:** match moments of the arithmetic average to a lognormal. Good for moderate vol.
- **Monte Carlo with geometric-Asian control variate:** standard approach. Variance reduction is ~10–100x.
- **Curran's approximation:** conditioning method, very accurate.

Asians are **cheaper than vanillas** (averaging reduces effective vol by ~1/√3 for arithmetic). Common in commodity and FX hedging programs.

## Compound options — Ch 21 (lines 16339–16585)

- Option on an option (call on call, call on put, etc.)
- **Geske (1979) closed form** for European compounds on BS underlyings
- Uses bivariate normal CDF
- Sensitivity: a compound has **vega-of-vega** as a first-order Greek

## Chooser options — Ch 21

- At time t* < T, holder chooses to make it a call or a put with the same K and T
- **Simple chooser** (same K and T): put-call parity gives a closed form decomposing it into call + put
- **Complex chooser** (different parameters per branch): no clean closed form

## Multi-asset options — Ch 22 (lines 16586–17410)

### Margrabe (1978) exchange option

- Payoff: `max(S1_T − S2_T, 0)`
- **Closed form:** acts like a BS option with `σ² = σ1² + σ2² − 2ρσ1σ2`, strike treated as the second asset's forward
- Spread options at K=0; for K≠0 use Monte Carlo or Kirk's approximation

### Basket options

- Payoff on a weighted sum of multiple assets
- No closed-form in general (sum of lognormals isn't lognormal)
- **Standard approach:** Monte Carlo with full correlation matrix
- **Moment matching** (Levy approx): match basket's first two moments to a lognormal. Quick but biased for high vol or low correlation.

### Rainbow options (best-of, worst-of)

- Payoff on `max(S1, S2, ...)` or `min(...)`
- **Stulz (1982) closed form** for two-asset European
- More assets: Monte Carlo

### Correlation as a risk factor

- Multi-asset options have **correlation vega** ("cega")
- Correlation is the most-unstable input — it regime-shifts hard, especially in EM
- For basket and best-of, **always stress correlation by ±0.2** and report sensitivity

See also Module D (correlation triangles, lines 18699–18899) for constraints on correlation matrices in multi-asset settings.

## General exotic-pricing checklist

1. Is there a closed form under the assumptions you're willing to make?
2. If MC: do you have a variance-reduction technique (control variate, antithetic, importance sampling)?
3. Have you stressed model parameters that the closed form treats as constants?
4. Can the position be statically replicated? If yes, prefer that over dynamic hedging.
5. For barriers/binaries: what's the behavior in a 1-tick window around the discontinuity?
6. For multi-asset: have you validated the correlation matrix is positive semi-definite?
