# Option Pricing Math (Module G — lines 19580–20315)

The mathematical foundation: Itô's lemma, the Black-Scholes PDE, and the standard pricing machinery. Read when you need to understand *why* a pricing formula has the form it does, or want to derive a custom model.

## Itô's lemma — heuristic statement (line 19582)

> *"The gist of Itô's method is that a function of a random walk (not smooth) is smooth and differentiable."*

This sounds wrong — Brownian paths are NOT smooth (Module A line 17961). The trick: while paths are jagged, **expectations** of functions of paths are well-defined and obey calculus-like rules.

## The Itô process (line 19637)

```
dW = μ(W, t) dt + σ(W, t) dZ
```

where:
- `μ(W, t)` = drift (deterministic component, scales with dt)
- `σ(W, t)` = diffusion (random component, scales with dZ ∝ √dt)
- `dZ` = standard Brownian increment

The differential `dW` is shorthand for an integral; don't treat it as an ordinary derivative.

## The Itô multiplication table (line 19631)

```
dt · dt = 0
dt · dW = 0
dW · dW = σ² dt
```

The last rule is the punch line of stochastic calculus. It says **the square of a Brownian increment, dW², is NOT zero — it equals σ² dt**. Ordinary calculus says (dx)² → 0; Itô calculus says (dW)² does not.

This single fact is responsible for the extra term in Itô's lemma vs. the ordinary chain rule.

## Itô's lemma (line 19650)

For F(W, t):

```
dF = ∂F/∂t dt + ∂F/∂W dW + (1/2) ∂²F/∂W² (dW)²
```

The third term is **the extra term** vs. ordinary calculus. Substituting (dW)² = σ² dt:

```
dF = [∂F/∂t + (1/2)σ² ∂²F/∂W²] dt + σ ∂F/∂W dW
```

This is the form practitioners actually use.

## Applying to log(S) (line 19674)

Suppose `dS/S = μ dt + σ dZ` (geometric Brownian motion). Let F = log(S):
- ∂F/∂t = 0
- ∂F/∂S = 1/S
- ∂²F/∂S² = -1/S²

Itô gives:
```
d log(S) = (μ - σ²/2) dt + σ dZ
```

The `-σ²/2` is the **Itô correction**. It's why the lognormal model's expected log-return is `μ - σ²/2`, not `μ`.

Integrating:
```
S_T = S_0 · exp((μ - σ²/2) T + σ √T · Z)
```

This is **the** formula used throughout BS and Monte Carlo pricing. See [scripts/bs_pricer.py](../scripts/bs_pricer.py) and [scripts/monte_carlo.py](../scripts/monte_carlo.py).

## The Itô correction in plain English

A lognormal asset with simple growth rate μ has **expected log return < μ** because volatility creates a downward drag of σ²/2.

Equivalent statement: `E[S_T] = S_0 · exp(μT)` exactly, but `exp(E[log S_T]) = S_0 · exp((μ - σ²/2) T)` — these differ by exp(σ²T/2). This is Jensen's inequality on the exponential, and it's why σ²/2 keeps appearing in option formulas.

## Three pricing methods (line 19710)

The chapter outlines three equivalent ways to derive option prices:

### 1. Black-Scholes (1973) — replication argument
- Build a delta-neutral, self-financing portfolio
- Set its growth rate equal to the risk-free rate (no arbitrage)
- Derive the BS PDE: `∂V/∂t + (1/2)σ²S² ∂²V/∂S² + rS ∂V/∂S - rV = 0`
- Solve with boundary condition V(T) = max(S - K, 0)
- Get the BS formula

### 2. Harrison-Kreps (1979) / Harrison-Pliska (1981) — martingale measure
- Find a probability measure Q under which discounted prices are martingales
- Price = expectation under Q of discounted payoff
- More general: works for any contingent claim, not just options
- Requires market completeness (any claim is replicable)

### 3. Feynman-Kac — probabilistic PDE solution
- Connects PDE solutions to expectations under stochastic processes
- For path-independent options: `Price = E^Q[exp(-rT) · payoff(S_T)]`
- For soft path-dependent (e.g., barriers): `Price = E^Q[exp(-rT) · payoff(path, T)]`
- This is the form Monte Carlo simulates directly

For complex options, **Feynman-Kac + Monte Carlo** is the workhorse. For closed-form vanillas, **Black-Scholes** or its asset-class variants suffice.

## Multi-asset Itô (line 19761)

For F(W₁, W₂, t) with two correlated processes:
```
dF = [∂F/∂t + (1/2)σ₁² ∂²F/∂W₁² + (1/2)σ₂² ∂²F/∂W₂² + ρσ₁σ₂ ∂²F/∂W₁∂W₂] dt
     + σ₁ ∂F/∂W₁ dW₁ + σ₂ ∂F/∂W₂ dW₂
```

The cross-term `ρσ₁σ₂ ∂²F/∂W₁∂W₂` is what makes correlation a first-class input to multi-asset option pricing.

## Black-Scholes PDE — derivation sketch (after line 19775)

1. Form the portfolio: long 1 option, short Δ shares
2. Δ-neutralize: Δ = ∂V/∂S, eliminating dS terms
3. The portfolio is now riskless → must grow at r
4. Equate to total derivative via Itô; collect terms
5. Get:
```
∂V/∂t + (1/2) σ² S² ∂²V/∂S² + r S ∂V/∂S - r V = 0
```

Solving with V(T, S) = max(S - K, 0) gives the BS call formula.

The **discount rate** is r (risk-free). The **drift** is replaced by r (under Q, not P). Volatility is σ — that's the only "real-world" parameter that matters under risk-neutrality.

## Where the BS assumptions break

The derivation assumes:
1. Continuous trading (you can rebalance the hedge instantly)
2. No transaction costs
3. Constant σ (no smile, no vvol)
4. Lognormal dynamics (no jumps, no fat tails)
5. Continuous price processes (no gaps)
6. Constant r (no rates risk)
7. Unlimited borrowing/lending at r

Real markets violate ALL seven. The BS formula remains useful because:
- The structure is approximately right for ATM short-dated options on liquid underlyings
- It's a quoting convention (implied vol)
- The Greeks it produces are approximately right for risk management

For deep OTM, long-dated, or illiquid options, replace BS with:
- Stochastic vol (Heston — see [scripts/heston_pricer.py](../scripts/heston_pricer.py))
- Jump-diffusion (Merton — see [scripts/em_adjustments.py](../scripts/em_adjustments.py))
- Local vol (smile-consistent diffusion)
- Smile-fitted vol surface (SVI/SABR — see [scripts/smile_fitter.py](../scripts/smile_fitter.py))

## Numerical methods (line 19737)

> *"Numerical integration can be lengthier in computer time but saves in considerable programming labor and presents a smaller error rate."*

Three main numerical approaches for option pricing:
1. **Closed-form / quasi-closed-form** — BS, Heston (via CF inversion), Merton barrier, etc.
2. **Trees (binomial / trinomial)** — early-exercise, discrete dividends. [scripts/binomial_pricer.py](../scripts/binomial_pricer.py).
3. **Monte Carlo** — anything path-dependent. [scripts/monte_carlo.py](../scripts/monte_carlo.py).
4. **PDE solvers** — implicit/explicit finite-difference; less common in pure-Python.

Taleb's preference: numerical integration (essentially Monte Carlo) for flexibility and smaller error rate vs. error-prone closed-form derivations.

## Practical rules

1. **The Itô correction (-σ²/2) is not a typo.** It's what makes lognormal pricing internally consistent.
2. **Under risk-neutrality, the drift is r (or r-q for dividends, r_d-r_f for FX, etc.).** Replace your real-world μ.
3. **Three pricing methods give the same answer when they apply.** Use whichever is most convenient.
4. **Feynman-Kac + Monte Carlo is the most general pricing tool.** Use it for anything weird.
5. **Cross-Greeks come from the cross-term in multi-asset Itô.** ρσ₁σ₂ is correlation's first-order effect on multi-asset option prices.
6. **BS assumptions are convenient lies.** Useful as a starting point, never as final truth — see [fat_tails.md](fat_tails.md), [pricing_decision_tree.md](pricing_decision_tree.md).
