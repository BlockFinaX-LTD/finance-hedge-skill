# Real Options (Hull Ch 36)

Applying derivatives valuation to real-world business decisions: a manager's option to invest, abandon, expand, or switch. Read when valuing a capital project or operating flexibility that traditional NPV understates.

## The basic insight

A traditional DCF / NPV calculation discounts a fixed expected cash-flow stream at a hurdle rate. It assumes the project unfolds passively — no managerial flexibility.

Real projects have embedded optionality:
- **Option to defer** (wait before committing) — analogous to a call on the project NPV
- **Option to abandon** — put on remaining value, struck at salvage value
- **Option to expand** — call on incremental capacity
- **Option to contract** — put on capacity reduction
- **Option to switch** — exchange option between two operating modes
- **Compound options** — staged investment, each stage opens the option to proceed to the next

Real options analysis (ROA) values this flexibility using BSM-style machinery. The output: NPV(static) + Value(flexibility).

## Why traditional DCF fails

1. **Sunk-cost framing.** Once you've started, marginal logic says continue — but the *option* to stop has value that DCF ignores.
2. **Single discount rate.** DCF discounts uncertain cash flows at a single risk-adjusted rate. Optionality has nonlinear payoff, so a single discount rate misvalues it (the option premium changes with σ even when E[payoff] doesn't).
3. **Over-investment in mediocre projects, under-investment in highly uncertain ones.** DCF systematically rejects projects whose option value comes from uncertainty itself.

The classic Dixit-Pindyck example: at typical commodity prices, oil-field development "barely positive NPV" under DCF can be deeply positive under real options analysis because the firm can choose to develop only if prices reach a threshold.

## Risk-neutral valuation in real options

The hard part: there's no traded asset whose price equals the underlying real variable.

For commodity-price-driven projects, Hull uses **market-implied risk-neutral price processes**:
```
dS = (r − y) S dt + σ S dW    (under Q)
```
where y is the **convenience yield** (or, for commodities with quoted forward curves, calibrated to match forwards).

For project-specific uncertainty without a traded hedge:
- Use **simulated NPV under subjective probabilities** (P-measure)
- Discount at the **certainty-equivalent rate** = project-specific risk-adjusted rate
- This is closer to DCF flavored with optionality than to genuine risk-neutral pricing

Hull's pragmatic take: when no traded asset exists, real-options analysis is **decision support**, not arbitrage-free pricing. The point is to make the optionality visible, not to claim a unique market price.

## The standard examples

### Option to defer a development project

Underlying: project value V (function of commodity price or demand).
Strike: investment cost I.
Time: deferral window T.

Payoff at exercise: `max(V − I, 0)`.

Decision rule: develop now if V exceeds the **trigger value** V* > I + option value of waiting. V* is solved as the boundary in a perpetual or finite-horizon American call problem.

### Option to abandon

Asset value follows GBM; salvage value S* is the strike of a put. Manager abandons whenever V < S* and the put's continuation value < intrinsic. Solved as American put on V.

### Option to expand

Option to invest incremental capital I_e to gain incremental value V_e. Pay I_e to receive V_e — a call on V_e struck at I_e.

### Option to switch

Exchange option between two production modes (e.g. oil-fired vs gas-fired plant). Margrabe (1978) exchange option formula:
```
V_switch = V_1 · N(d_1) − V_2 · N(d_2)
d_1 = [ln(V_1/V_2) + σ_X² T / 2] / (σ_X √T)
σ_X² = σ_1² + σ_2² − 2 ρ σ_1 σ_2
```
No risk-free rate appears — it's a pure relative-value option.

### Compound options — staged investment

Many real projects involve sequential gates (e.g. drug development: preclinical → Phase 1 → Phase 2 → Phase 3 → approval). Each phase has cost; success allows option to proceed to next.

Pricing: backward induction on a tree. At final node, value = max(approved product NPV − final cost, 0). At intermediate nodes, value = max(continue option PV − stage cost, 0) × P(success at this stage).

## Numerical methods

For most real options the closed-form is unavailable. Methods:

1. **Binomial / trinomial tree** on the underlying state variable. Add a backward step at each node to evaluate the optimal management decision. Works for one or two state variables. See [scripts/binomial_pricer.py](../scripts/binomial_pricer.py).

2. **Monte Carlo with LSM** (Longstaff-Schwartz). For >2 state variables or path-dependent options. Simulate paths under risk-neutral measure (or P-measure with risk-adjusted discounting), regress continuation value on state variables, exercise where intrinsic > continuation.

3. **Finite difference** on the PDE. For 1-2 state variables; precise but harder to set up than trees.

## When NOT to use real options

Real options ≠ all uncertainty deserves an option premium. Don't use ROA when:
1. **Management doesn't actually have the optionality.** Many "real options" exist only on paper — bureaucratic, contractual, or capacity constraints prevent the manager from actually deferring / abandoning / switching.
2. **The "uncertainty" is mostly idiosyncratic.** Real options pricing assumes the firm can hedge or that the relevant risks are systematic. If the underlying risk is pure idiosyncratic (e.g. R&D success on a never-tried drug), risk-neutral pricing doesn't apply cleanly.
3. **The required management discipline is unrealistic.** ROA values assume managers exercise optimally. Behavioral biases (sunk cost, escalation of commitment, optimism) mean real exercise is suboptimal — ROA over-values flexibility.

## Practical rules

1. **Static NPV is a floor, not a ceiling.** When flexibility is material, the project is worth more than NPV says.
2. **Volatility ADDS value to projects with optionality.** This inverts intuition from DCF, where higher discount rate (vol → discount rate) reduces value.
3. **Find the trigger threshold, not just the option value.** Operationally what management cares about is "when do I commit?" — that's the optimal exercise boundary, not the option premium.
4. **Match the model to the actual decision.** A defer option needs an American call boundary; an abandon option needs an American put; a switch needs Margrabe.
5. **For commodity-price-driven projects, calibrate to the forward curve.** Don't use historical drift as the risk-neutral drift.
6. **For project-specific risk without a traded hedge, ROA is decision support not pricing.** State assumptions explicitly; use sensitivity analysis rather than claiming a single price.
7. **Watch out for compound real options.** Phase-gate R&D projects have multiplicative success probabilities and stage costs; naive DCF treats them as linear.

Cross-link: [option_pricing_math.md](option_pricing_math.md) for the BSM framework underlying real-options pricing, [hull_credit_risk.md](hull_credit_risk.md) (Merton's equity-as-call insight is the foundation of real-options thinking), [exotic_options.md](exotic_options.md) for compound and exchange option pricing, [risk_neutrality.md](risk_neutrality.md) for the change-of-measure caveats when no traded hedge exists.
