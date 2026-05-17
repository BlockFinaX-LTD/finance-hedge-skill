# Risk Neutrality Explained (Module B — lines 18214–18405)

The essential foundation: why we use "risk-neutral probabilities" in option pricing, what they mean, and what they don't mean.

## Step 1: The "fair dice" / no-free-lunch principle (line 18229)

Start in an economy with **zero interest rates**. A security at price 100 with two outcomes:
- 101.01 with probability 0.499
- 98.99 with probability 0.501

Expected payoff:
```
101.01 × 0.499 + 98.99 × 0.501 = 100
```

The security is **fairly priced**: it's a fair game. No free lunch.

In binomial form:
```
p·exp(u) + (1−p)·exp(v) = 1
```
where u, v are log-returns of up/down moves and p is the up-probability.

## Skew and probability fairness (line 18265)

Now allow the up-move to be larger than the down-move. For fairness:
```
larger up-move ⇒ lower up-probability
```

Example: up to 105.13 with probability 0.165, down to 98.99 with probability 0.835. Expected payoff:
```
105.13 × 0.165 + 98.99 × 0.835 ≈ 100
```

This is **physical-world skew**: asymmetric move sizes balanced by asymmetric probabilities.

## Step 2: Adding interest rates — the risk-neutral measure (line 18277)

In a real economy, an asset with expected return μ should grow at μ per unit time. If μ ≠ r (risk-free rate), the difference is a **risk premium**.

For option pricing, the **Black-Scholes-Merton breakthrough** is:

> *"Option replication eliminates the delta and the exposure to the asset's change of direction (i.e., the return) and would let the operator only concern himself with the volatility of the asset, not its required rate of return, nor the operator's risk preference."* (line 18294)

Therefore:
> **For arbitrage trading and option valuation, the drift of the underlying non-interest-paying asset needs to be replaced by the risk-neutral rate in the economy.** (line 18309)

This is **change of measure**: we *fictitiously* re-weight the probabilities of up-moves and down-moves so that the expected return equals the risk-free rate. The new measure is called **Q** (risk-neutral) as opposed to **P** (physical).

## Why this works (the BSM argument, line 18298)

Build a delta-neutral, self-financing portfolio that replicates the option through continuous rebalancing:
- Short the option
- Long Δ shares of underlying
- Hold the residual in risk-free bonds

The portfolio has no exposure to asset direction (Δ-neutral). Its growth rate must equal the risk-free rate (no arbitrage). The option price that makes this work is the Black-Scholes price.

**Crucially:** the option price doesn't depend on μ. Two traders with different views of μ agree on the option price. The risk-neutral measure is a **pricing tool**, not a prediction.

## Put-call parity as the risk-neutral argument's traders' version (line 18352)

Traders rarely think about Girsanov; they think about put-call parity:
```
Call − Put = Forward
```

The forward price is *already* risk-neutral (cash-and-carry forces it to r − q). So call and put together must replicate the forward → their prices must satisfy the parity → the operator's "bullishness" or "bearishness" cancels out in any combined position.

> *"Bullishness would normally raise the value of the call. But arbitrage would also raise the value of the put, to satisfy the equality... Hence one's preferences should not affect the option's fair value."* (line 18375)

This is the trader-intuitive way to internalize risk-neutrality.

## What the risk-neutral measure is NOT

This is where most misunderstandings happen. The risk-neutral measure:

- **Is NOT a forecast.** Probabilities under Q are not what you expect to happen.
- **Does NOT mean traders are risk-neutral.** They aren't. The mathematical fiction sidesteps the question of risk preferences.
- **Does NOT require complete markets.** It works as long as you can replicate the option's payoff with traded instruments.
- **Does NOT eliminate volatility risk.** Vol is still the parameter you guess wrong about.

Risk-neutral probabilities are tools for pricing. The real-world probabilities (under P) determine what *actually* happens to your P/L.

## Generalization (line 18386)

> *"The risk-neutral drift used for a pair is the difference between the two risk-neutral drifts."*

Applied to:
- **Dividend-paying stock:** drift = r − q (risk-free minus dividend yield)
- **FX (Garman-Kohlhagen):** drift = r_domestic − r_foreign
- **Commodity future:** drift = r − convenience_yield + storage_cost
- **Bond:** drift = r − coupon yield

This is why every BS-family formula has a "carry term" that depends on the asset class — it's the appropriate risk-neutral drift for that asset.

## The Girsanov theorem (mentioned, line 18382)

The mathematical machinery for changing measures. Provides the explicit transformation from P to Q. Practitioners rarely need it directly, but it explains why the change of measure preserves the volatility while shifting the drift. Reference for the curious: any textbook on continuous-time finance, e.g., Shreve.

## Risk-neutral pricing in three sentences

1. Build a replicating portfolio under the assumption that all assets grow at the risk-free rate.
2. Price the option as the discounted expectation under that fictitious world.
3. The result is the no-arbitrage price in the real world, because the replication argument doesn't depend on the actual drift.

## Practical rules

1. **The drift in your BS formula is r − q (or r_d − r_f for FX). It is NOT your expected return.**
2. **Risk-neutral probabilities have units of price, not units of belief.**
3. **Don't try to "calibrate" the risk-neutral drift to historical data.** It is determined by no-arbitrage, not by data.
4. **When you change asset class, change the carry term, not the framework.** Equity q, FX r_f, commodity (storage − convenience).
5. **Risk-neutrality is a no-arbitrage statement, not a prediction.** Your P/L is determined by the real-world process, not the risk-neutral one.
