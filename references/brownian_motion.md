# Brownian Motion (Module A — lines 17784–18213)

The intuition for random walks. Read this if you want to *understand* what your Monte Carlo, BS formula, and Greeks are implicitly assuming.

## Random walk vs. Brownian motion (line 17794)

> *"A random walk for security prices means that a share of the price changes of the security over a given period of time is random. The share of the price change that is not expected to be random is called the drift."*

```
Brownian motion = Random walk + Drift
```

Module A focuses on the random component; drift is Module B (risk-neutrality).

## The drunk man analogy (line 17814)

Walk down Madison Avenue. Dead drunk, no memory. Each step: forward + (left or right) with equal probability. After 10 steps:
- Most extreme: 10 left or 10 right
- All combinations in between
- Histogram of final positions → bell curve (central limit theorem in action)

This is **Markovian** (no memory) and **stationary** (each step distribution is identical).

Securities markets are assumed to follow a similar walk, with one hitch: **step size scales with asset price** (geometric Brownian motion, not arithmetic — but see [volatility_correlation.md](volatility_correlation.md) for when arithmetic is right).

## Constructing a path on a spreadsheet (line 17834)

The recipe:
1. Generate N normal random numbers, mean 0, std 1 (`NORMINV(RAND(), 0, 1)` in Excel)
2. Initial price S₀ in cell A3 (say 100)
3. Vol σ in cell A2 (say 0.157 = 15.7% annual)
4. Each row: `S_{t} = S_{t-1} × exp(σ × sqrt(1/248) × Z_t)`
5. Plot column A

The result: a jagged path that looks like real market data.

> *"Repeating the random number generation to get a fresh series of 'white noise' numbers causes new paths to form on the screen."*

This is how all Monte Carlo pricing works under the hood. Our [monte_carlo.py](../scripts/monte_carlo.py) does exactly this in Python with antithetic variates for variance reduction.

## Why standard deviation scales as √t (line 17935)

In the +1/−1 binary walk:
- After n steps, sum is between −n and +n
- Mean E(W) = 0
- Variance E(W²) = n (since each step's W² = 1, and steps are independent)
- Std dev = √n

So **for a process with constant per-unit-time variance, std dev grows with √t, not t**. This is THE fundamental scaling law of diffusion.

Implications:
- 1-day vol × √252 ≈ annual vol
- 1-week vol × √52 ≈ annual vol
- 2x the time → √2 ≈ 1.41x the vol

**This breaks in heteroskedastic markets** (where vol regime-shifts) and in markets with jumps (where parts of the move aren't diffusive). VaR (see [var.md](var.md)) leans heavily on this scaling and fails when it doesn't hold.

## The central limit theorem, intuitively (line 17927)

Taleb's heuristic derivation: take many independent +1/−1 binary steps. The sum's distribution approaches Gaussian. He calls this *"perhaps the most misinterpreted law in the history of mathematics."*

The misinterpretation: CLT says **sums** of independent random variables tend to Gaussian. People generalize this to "everything is Gaussian eventually."

Three problems with that generalization:
1. **Independence requirement.** Real returns have autocorrelation (vol clustering, momentum, mean reversion).
2. **Identical-distribution requirement.** Real distributions regime-shift.
3. **Finite-variance requirement.** If the underlying distribution has infinite variance (Lévy stable, Cauchy), CLT doesn't apply — you get stable distributions, not Gaussian. Many financial return distributions have *finite* variance in any finite sample but *very* heavy tails (see [fat_tails.md](fat_tails.md)).

The fix-up: assume markets are *approximately* Gaussian *most* of the time, and add fat-tail and jump components for the rest.

## Diffusion property (line 17961)

> *"The principal property of a diffusion is that, no matter how small time is sliced, the function remains jagged."*

The path is **continuous everywhere, differentiable nowhere**. You can zoom in arbitrarily and still see roughness. This is what makes Itô calculus necessary (Module G): ordinary calculus assumes smoothness, but Brownian paths aren't smooth.

Analogy: the coastline. No matter how high your resolution, more wiggles appear. The total "length" is undefined (or infinite). Same with Brownian paths.

## What this means for your option model

1. **The volatility input is the *coefficient* on the diffusion term.** It's the σ in `dS/S = μ dt + σ dW`.
2. **Realized vol from data is an *estimator* of σ.** It has sampling error proportional to 1/√n.
3. **For a 1-day forecast, the BS model is approximately right** if you got vol right.
4. **For a long-dated forecast, errors compound.** Stochastic vol matters more, jumps matter more, structural change matters more.

## Generalizing to multiple assets

For two correlated assets:
```
dW1 = σ1 dt-step × Z1
dW2 = σ2 dt-step × (ρ·Z1 + √(1-ρ²)·Z2)
```
where Z1 and Z2 are independent standard normals.

This is how multi-asset Monte Carlo (basket options, spread options) works in [monte_carlo.py](../scripts/monte_carlo.py): generate correlated normals via Cholesky decomposition (or its 2-asset shortcut above), advance each asset, sum/intersect the resulting paths.

## Practical rules

1. **A Brownian-motion model is your starting point, not your ending point.** Add fat-tail / jump / stochastic-vol overlays when accuracy matters.
2. **√t scaling is the diffusion signature.** When realized scaling deviates from √t, you have non-diffusive behavior — investigate before pricing.
3. **The path is jagged at every scale.** This is why Itô (not ordinary) calculus is necessary for option pricing.
4. **CLT does NOT guarantee Gaussian returns.** It requires independence, IID, finite variance — all violated in real markets.
5. **Monte Carlo is the operational version of "generate Brownian paths."** Variance reduction (antithetic, control variates) gets you accuracy without runtime blowup.
