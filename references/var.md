# Value-at-Risk (Module E — lines 18900–19269)

> *"Abyssus abyssum invocat (The abyss calls for the abyss)."* — Latin proverb, Module E epigraph

Taleb's framing of VaR is **deeply critical**. Read this when asked to compute, report, or interpret VaR — and especially before letting any VaR number drive a decision.

## What VaR is (definition, line 18915)

> *"Value-at-risk is a method of estimating the maximum loss for a portfolio at a confidence level **assuming a knowledge of the process governing its components**."*

The italicized clause is the entire problem. If the process is known, VaR is meaningful. If it isn't (and it never is, in real markets), VaR is a number with the *appearance* of precision and the substance of fiction.

## Taleb's structural objections (lines 18910–18965)

1. **VaR can only work if it's unsuccessful.** Like portfolio insurance: if everyone uses it, the actions VaR triggers (liquidation at the stop) become market-moving, invalidating the underlying distributional assumptions. (Line 18910 — references Taleb 1997.)
2. **Condensing complex risk into one number distorts.** Simplification destroys the information that mattered.
3. **Charlatanism risk.** A VaR statement to a board member sounds like an airplane-crash statistic but isn't. It lulls non-traders into false security.
4. **Wrong reading:** *"Within 99.7% you won't lose more than $1M next month."* — invalid. (Line 18956)
5. **Correct reading:** *"You're expected to lose no more than $100k within the next two hours with 66% accuracy, **provided you don't try to liquidate and no peer firm holds the same portfolio**."* (Line 18960)

Note the conditionals in #5: stationarity assumption + no-correlation-with-peers assumption.

## How VaR is computed (simplified, line 18970)

Inputs:
- Portfolio positions
- Volatilities (typically annualized historical)
- Correlation matrix between positions
- Confidence level (1σ ≈ 66%, 2σ ≈ 95%, 3σ ≈ 99.7%)

Output: portfolio variance via the standard quadratic form `σ²_p = w'Σw`, then convert to dollar P/L at the chosen confidence level.

### Worked example from Taleb (line 19009)

Universe: USD-DEM, USD-JPY, T-Bond futures, SP500 futures. May 1995 data. 9m annualized vols.

**Example 1 (no diversification):** $20M face value in any single instrument → daily 1σ exposure per Table E.2.

**Example 2 (cross-position):** USD-DEM long vs USD-JPY short reduces 1σ exposure to ~71% of single-currency, due to positive correlation. (Line 19032)

**Example 3 (USD-DEM vs USD-FRF):** highly correlated pair; the cross-position 1σ exposure is **25%** of either single-currency exposure — the residual DEM-FRF volatility is 3.03% vs ~12% for the singles. (Line 19071)

The math is right under its assumptions. *That's the problem.*

## Failure modes (Taleb's enumeration, line 19085+)

### Problem 1: Assumed homoskedasticity
VaR assumes Gaussian returns (or at least stationary distributions). Markets aren't:
- Fat tails — risk lives precisely where the model can't see (line 19094)
- High peaks — body of the distribution looks tighter than Gaussian, tails much wider
- Heteroskedasticity — `σ·√t` rule breaks when vol regimes shift

### Problem 2: Correlation instability
The correlation matrix used to diversify positions is computed from a sample window. In stress:
- All risk assets correlate toward 1
- Hedges (long DM bonds vs short EM equity) reverse sign
- The diversification benefit *evaporates exactly when needed*

### Problem 3: Liquidity not modeled (line 4369 / Ch 4)
VaR usually assumes positions can be marked at mid-market. Real liquidation costs:
- 3–10× wider spreads in stress
- Price impact scales nonlinearly with size
- Forced sellers have no choice → market knows → fades them

### Problem 4: Endogeneity
Once VaR is the constraint, traders trade to optimize *VaR-adjusted P/L*. They take risks VaR doesn't measure (jump risk, gap risk, skew). The unmeasured tail grows precisely because of the measure.

## When VaR is useful

Despite Taleb's broadsides, VaR has legitimate uses:
- **Comparing the relative risk of two portfolios** under the same model assumptions (the model is wrong but consistently wrong)
- **Stacking analysis** (Ch 12) — using VaR to size a single hedge against another
- **Communicating order-of-magnitude** to non-traders (with caveats stated)
- **Regulatory compliance** — when externally required
- **Internal stop-loss governance** — as a *trigger* for human review, not an automatic action

## Better alternatives (or supplements)

- **Stress tests / scenario analysis** — explicit "what if the peg breaks? what if vol doubles? what if correlation goes to 1?"
- **Expected shortfall (CVaR / TVaR)** — conditional on being in the tail, what's the expected loss? Better than VaR for fat-tailed distributions; still subject to model risk.
- **Maximum-loss-under-liquidation** — what's the actual cost of exiting, including stressed spreads?
- **Greek-by-Greek bucketed reporting** (Ch 14) — preserves information VaR destroys

## Practical rules

1. **Never report VaR as a single number without confidence intervals and stated assumptions.**
2. **Always supplement VaR with stress scenarios** — particularly correlation-to-1 and 2σ vol shock.
3. **The fattest tail in your distribution is in your model, not in the market.** Assume your model underestimates tail by 2–5×.
4. **VaR is best used as a comparative measure**, not an absolute one.
5. **Be especially skeptical of VaR for portfolios containing optionality, EM assets, or any position whose hedge is itself illiquid.**
6. **Read Taleb 1997 cited at line 18911** ("VaR paradox") — the original source on why VaR succeeds only when nobody uses it.
