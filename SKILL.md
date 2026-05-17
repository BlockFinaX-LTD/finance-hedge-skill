---
name: dynamic-hedging
description: Price option premiums and manage derivatives risk across all asset classes (equities, FX, rates, commodities, crypto, credit, and emerging markets). Grounded in Nassim Taleb's *Dynamic Hedging* (trader perspective) and John Hull's *Options, Futures, and Other Derivatives* (textbook reference). Use when the user asks to price vanilla or exotic options, compute Greeks, build a vol surface, hedge an option book, value swaps or credit derivatives, evaluate fat-tail or counterparty risk, or reason about derivatives in illiquid/EM markets. Covers Black-Scholes-Merton and its real-world failures, the full Greeks (delta/gamma/vega/theta + shadow gamma + minor Greeks), volatility smile/skew, fat tails and stochastic volatility, liquidity holes, exotics (binaries, barriers, lookbacks, Asians, compounds, multi-asset), bucketing, VaR/ES, swaps (IRS, currency, OIS discounting), securitization/CDOs, credit derivatives (CDS, indices, Gaussian copula), XVAs (CVA/DVA/FVA/MVA/KVA), interest rate derivatives (Black-76, Vasicek, Hull-White, HJM, LMM), GARCH vol estimation, real options, and emerging-markets-specific adjustments (jumps, pegs, devaluation skew, illiquidity premium, capital controls).
---

# Dynamic Hedging — Option Pricing & Risk Management

This skill prices option premiums and reasons about derivatives risk using two complementary canonical sources:
- **Nassim Taleb's *Dynamic Hedging: Managing Vanilla and Exotic Options* (1997)** — trader/practitioner framing; market making, fat tails, liquidity holes, smile causality, exotic-hedging tricks, EM
- **John Hull's *Options, Futures, and Other Derivatives* (10th ed., 2018)** — textbook/math-first framing; formal derivations, post-1997 markets (CDS, ABS, XVAs, OIS, GARCH, LMM), real options, mishaps

Reference files cite both. When both cover a topic, the Taleb-anchored file usually has the intuition and the Hull-anchored file has the formal machinery.

## Sources of truth

**Taleb (canonical, in-skill copy):** `references/dynamic_hedging_full.md` (~18.5k lines)
- Original: `C:\Users\ADMIN\rift\financeskill\dynamic_hedging.md`
- Navigator: [references/chapter_navigator.md](references/chapter_navigator.md)

**Hull (canonical, original location):** `C:\Users\ADMIN\rift\financeskill\derivatives.md` (~57k lines)
- Navigator: [references/hull_navigator.md](references/hull_navigator.md)
- *Note: chapters appear in paste-order, not strict numeric sequence; use the navigator's line ranges.*

Reference files in this skill point into the books by **line range**. When you need authoritative detail on a concept, read the relevant lines directly from the source — do not paraphrase from memory. Nuances (continuous-time delta is NOT a hedge ratio; shadow gamma; vvol; CVA wrong-way risk; LMM multi-curve discounting) are easy to corrupt in summary.

## When to use

Invoke when the user asks for:
- Option pricing (vanilla, American, or exotic) on any asset class
- Computing or interpreting Greeks (delta, gamma, vega, theta, rho, plus shadow gamma, charm, vanna, volga, color)
- Implied/historical volatility analysis, smile/skew fitting, GARCH/EWMA vol forecasting
- Hedging strategy for an option book or directional exposure
- Fat-tail / stochastic-vol reasoning (Taleb Ch 15 territory)
- Emerging markets derivatives (BRL, ZAR, TRY, INR, IDR, MXN, NGN, pegged FX, devaluation risk)
- Exotic structures: binaries, barriers, lookbacks, Asians, compounds, baskets
- Swaps (IRS, currency, basis, equity, variance) — valuation, OIS discounting
- Credit derivatives — CDS, indices, CDOs, hazard-rate bootstrapping, Gaussian copula
- Interest rate derivatives — caps/floors, swaptions, Bermudans, short-rate / HJM / LMM models
- XVAs — CVA, DVA, FVA, MVA, KVA; counterparty / funding / capital adjustments
- Securitization — ABS, MBS, CDO tranching, waterfall, post-2007 lessons
- VaR / Expected Shortfall, bucketing, P/L attribution
- Real options on capital projects
- "Why does my Black-Scholes price disagree with the market?" questions
- Derivatives risk management postmortems (Barings, LTCM, AIG, London Whale, etc.)

## Workflow for pricing an option premium

1. **Classify the structure** before reaching for a formula. Use Ch 2's six dimensions: homogeneity, payoff continuity, barriers, asset count, order, path dependence. See [references/pricing_decision_tree.md](references/pricing_decision_tree.md).
2. **Pick the pricing method** that matches the structure (NOT just Black-Scholes by default):
   - European vanilla, liquid underlying, stable vol → Black-Scholes-Merton with a smile adjustment
   - American, deep ITM, or with dividends/carry → binomial / trinomial tree or LSM Monte Carlo
   - Path-dependent (barrier, Asian, lookback) → Monte Carlo or closed-form where it exists (e.g., Merton barrier under GBM)
   - Multi-asset / basket → Monte Carlo with a correlation matrix
   - Emerging markets / illiquid → jump-diffusion or stochastic-vol model + liquidity/skew premium; see [references/emerging_markets.md](references/emerging_markets.md)
3. **Source the inputs:**
   - Spot, strike, time to expiry, risk-free rate (in the *quote* currency), carry/dividend yield
   - Volatility — never use a flat number for OTM options; pull from the vol surface or imply from market quotes
   - For EM: factor in devaluation skew, capital-control risk, peg integrity
4. **Compute and sanity-check** with scripts in [scripts/](scripts/):
   - `bs_pricer.py` — vanilla European + full Greeks
   - `binomial_pricer.py` — American + Bermudan
   - `monte_carlo.py` — path-dependent and multi-asset
   - `em_adjustments.py` — jump-diffusion overlay, skew adjustments
5. **Reconcile with the market.** A model price that disagrees with the market is information — usually the market is pricing in something your model isn't (jumps, regime risk, liquidity, supply/demand imbalance). Don't override the market silently; surface the gap to the user.
6. **Report Greeks alongside the premium.** A price without Greeks is half an answer. At minimum: delta, gamma, vega, theta. For barriers and binaries also report behavior near the barrier (Ch 19–20). See [references/greeks.md](references/greeks.md).
7. **Flag distribution risk** when material — fat tails (Ch 15) systematically underprice OTM wings under flat-vol Black-Scholes. See [references/fat_tails.md](references/fat_tails.md).

## Taleb's core principles (apply throughout)

These show up in nearly every chapter and should anchor your reasoning:

- **"It ain't physics."** Markets are not stationary; constant-vol-constant-correlation assumptions are scaffolding, not truth (Ch 6: "There Is No Such Thing as Constant Volatility and Correlation").
- **Continuous-time delta is a benchmark, not a hedge ratio.** Especially around barriers, deltas can be mathematically correct and operationally insane (Ch 7, the "Half Billion-Dollar Delta" anecdote at lines 6223–6253).
- **Shadow gamma > gamma.** Static gamma understates risk; gamma changes with vol and time, and what kills books is the gamma you didn't see (Ch 8).
- **Tails are explained by vol-of-vol.** Smile and fat tails arise from stochastic volatility plus correlation between spot and vol (Ch 15 lines 11134–11250).
- **Adverse selection.** Market makers systematically get the "bad" side of the distribution (Ch 15 line 11121).
- **Liquidity is asymmetric.** Stop orders and barriers create liquidity holes; price impact ≠ historical slippage (Ch 4).
- **Bucketing matters.** Aggregate Greeks lie; bucket by tenor, strike, and underlying (Ch 14).

## Reference files

### Taleb-anchored (trader intuition, market microstructure, fat tails)

**Pricing core:**
- [references/chapter_navigator.md](references/chapter_navigator.md) — line-range index into Taleb's book by topic
- [references/instruments.md](references/instruments.md) — Taleb Ch 1: derivatives taxonomy, linear vs. nonlinear, soft optionality, primary/secondary risks, forwards vs. futures
- [references/pricing_decision_tree.md](references/pricing_decision_tree.md) — Taleb Ch 2 + which method for which payoff
- [references/volatility_correlation.md](references/volatility_correlation.md) — Taleb Ch 6: implied vs. historical, lognormal vs. arithmetic, Parkinson estimator, "no constant vol/corr"
- [references/greeks.md](references/greeks.md) — Taleb Ch 7–11: formulas, signs, and Taleb's emphasis points for each Greek
- [references/fat_tails.md](references/fat_tails.md) — Taleb Ch 15: smile/vvol relationship, stochastic volatility
- [references/exotic_options.md](references/exotic_options.md) — Taleb Ch 17–23: binaries, barriers, lookbacks, Asians, compounds, multi-asset
- [references/emerging_markets.md](references/emerging_markets.md) — EM-specific overlays (cross-chapter synthesis)

**Market structure & trading:**
- [references/market_making.md](references/market_making.md) — Ch 3 distilled: locals vs. paper vs. arbs, leaning, commoditized vs. nonstandard, adverse selection, arcsine law of P/L
- [references/liquidity.md](references/liquidity.md) — Ch 4 distilled: slippage, liquidity holes, stop-order mechanics, one-way traps, barrier-induced vacuums
- [references/arbitrage.md](references/arbitrage.md) — Ch 5 distilled: mechanical vs. behavioral stability, deterministic relationships, passive arbitrage, the squeeze
- [references/fungibility.md](references/fungibility.md) — Ch 12 distilled: fungibility ranking, cash-and-carry boundary, calendar spreads on non-fungible commodities, stacking
- [references/option_market_wrinkles.md](references/option_market_wrinkles.md) — Ch 13 distilled: pin risk, sticky strikes, market barriers, triple-witching, pre-weekend vol
- [references/trading_concepts.md](references/trading_concepts.md) — Ch 16 distilled: static vs. dynamic replication, neutral spreading, risk reversals/butterflies/calendars, bleed

**Risk management & quantitative framework:**
- [references/bucketing.md](references/bucketing.md) — Ch 14 distilled: why aggregate Greeks lie, straight vs. forward-forward bucketing, topography view
- [references/var.md](references/var.md) — Module E distilled: VaR definition, Taleb's objections, failure modes, better alternatives
- [references/brownian_motion.md](references/brownian_motion.md) — Module A distilled: random walk intuition, √t scaling, CLT pitfalls, diffusion property
- [references/risk_neutrality.md](references/risk_neutrality.md) — Module B distilled: the change-of-measure argument, put-call parity intuition, what risk-neutral is NOT
- [references/numeraire.md](references/numeraire.md) — Module C distilled: numeraire relativity, two-country paradox, Siegel's paradox, numeraire flipping
- [references/correlation_triangles.md](references/correlation_triangles.md) — Module D distilled: vols-as-distances geometry, implied correlation, arbitrage-free constraints on multi-asset surfaces
- [references/probabilistic_rankings.md](references/probabilistic_rankings.md) — Module F distilled: stochastic-dominance rules, butterfly arbitrage, calendar inequalities, model-free bounds
- [references/option_pricing_math.md](references/option_pricing_math.md) — Module G distilled: Itô's lemma, the -σ²/2 correction, BS PDE derivation, multi-asset Itô

### Hull-anchored (textbook math, post-1997 markets)

- [references/hull_navigator.md](references/hull_navigator.md) — line-range index into Hull's book by topic; Hull-vs-Taleb mapping
- [references/hull_interest_rates.md](references/hull_interest_rates.md) — Hull Ch 4: compounding, zero/forward rates, FRA, duration, convexity, key-rate duration
- [references/hull_swaps.md](references/hull_swaps.md) — Hull Ch 7: IRS, currency swap, comparative advantage critique, OIS discounting, swap variants
- [references/hull_securitization.md](references/hull_securitization.md) — Hull Ch 8: ABS, MBS, CDO, waterfall, ABS CDO, 2007 crisis postmortem
- [references/hull_xvas.md](references/hull_xvas.md) — Hull Ch 9: CVA/DVA/FVA/MVA/KVA mechanics, OIS vs LIBOR discounting
- [references/hull_garch.md](references/hull_garch.md) — Hull Ch 23: EWMA, GARCH(1,1), maximum likelihood, multivariate consistency
- [references/hull_credit_risk.md](references/hull_credit_risk.md) — Hull Ch 24: default probabilities (P vs Q), credit triangle, Merton model, wrong-way risk
- [references/hull_credit_derivatives.md](references/hull_credit_derivatives.md) — Hull Ch 25: CDS, hazard bootstrapping, indices, Gaussian copula, CDO tranching
- [references/hull_ir_derivatives.md](references/hull_ir_derivatives.md) — Hull Ch 29–32: Black-76, caps/swaptions, convexity/timing/quanto, Vasicek/CIR/Hull-White/HJM/LMM, multi-curve
- [references/hull_real_options.md](references/hull_real_options.md) — Hull Ch 36: defer/abandon/expand/switch options, Margrabe, compound staged investment
- [references/hull_mishaps.md](references/hull_mishaps.md) — Hull Ch 37: Barings, LTCM, SocGen, London Whale, AIG, Metallgesellschaft, lessons

**Canonical sources:**
- [references/dynamic_hedging_full.md](references/dynamic_hedging_full.md) — full Taleb book (820 KB), read by line range from chapter_navigator
- `C:\Users\ADMIN\rift\financeskill\derivatives.md` — full Hull book (~2.4 MB), read by line range from hull_navigator

## Scripts

All scripts are pure-stdlib Python (no numpy/scipy needed). Run with `python scripts/<name>.py --help`.

**Pricing engines:**
- [scripts/bs_pricer.py](scripts/bs_pricer.py) — Black-Scholes-Merton + full Greeks + implied-vol solver. FX (Garman-Kohlhagen), futures (Black-76) via flags.
- [scripts/binomial_pricer.py](scripts/binomial_pricer.py) — Cox-Ross-Rubinstein tree for American / European / Bermudan.
- [scripts/monte_carlo.py](scripts/monte_carlo.py) — Asian, barrier, lookback, spread, basket. Antithetic variates; barrier-bias correction.
- [scripts/heston_pricer.py](scripts/heston_pricer.py) — Heston stochastic-vol via characteristic-function inversion. Use for vvol-aware smile pricing.

**Calibration & adjustments:**
- [scripts/smile_fitter.py](scripts/smile_fitter.py) — SVI (raw) and SABR (Hagan asymptotic) smile fitters. Pass strikes + market vols, get parameters.
- [scripts/em_adjustments.py](scripts/em_adjustments.py) — Merton jump-diffusion, smile widening, peg-break decomposition for pegged FX.

## Asset-class coverage notes

| Asset class       | Default model               | Key adjustments                                               | Reference file |
|-------------------|-----------------------------|---------------------------------------------------------------|----------------|
| DM equities       | BS + vol surface            | Skew (left-leaning), dividend discrete cash flows             | [greeks.md](references/greeks.md), [fat_tails.md](references/fat_tails.md) |
| DM FX (G10)       | Garman-Kohlhagen (BS w/ rd, rf) | Smile usually symmetric; widens in crisis                 | [numeraire.md](references/numeraire.md) |
| Rates             | Black-76 / Hull-White / LMM | Term structure; cap/floor vol cube; multi-curve discounting   | [hull_ir_derivatives.md](references/hull_ir_derivatives.md), [hull_interest_rates.md](references/hull_interest_rates.md) |
| Swaps             | Bond/FRA decomposition + OIS discounting | XVA stack for uncollateralized counterparties     | [hull_swaps.md](references/hull_swaps.md), [hull_xvas.md](references/hull_xvas.md) |
| Credit            | Hazard-rate / CDS / Gaussian copula | Wrong-way risk, recovery, correlation stress         | [hull_credit_risk.md](references/hull_credit_risk.md), [hull_credit_derivatives.md](references/hull_credit_derivatives.md) |
| Commodities       | Black-76 on futures         | Seasonality, term structure (contango/backwardation)          | [fungibility.md](references/fungibility.md) |
| Crypto            | BS as starting point        | High vol, fat tails, weekend gaps, exchange risk              | [fat_tails.md](references/fat_tails.md) |
| **EM equities**   | BS + jump overlay           | Sovereign risk, low liquidity, sudden gaps                    | [emerging_markets.md](references/emerging_markets.md) |
| **EM FX**         | Jump-diffusion or stoch-vol | Devaluation skew, peg/break risk, capital controls            | [emerging_markets.md](references/emerging_markets.md) |
| **EM rates**      | Black-76 + sovereign spread | Inflation regime risk, currency-rates correlation             | [emerging_markets.md](references/emerging_markets.md) |
| Real / project    | NPV + tree / LSM            | Defer/abandon/expand/switch; calibrate to commodity forwards  | [hull_real_options.md](references/hull_real_options.md) |

For any EM asset, **always consult [references/emerging_markets.md](references/emerging_markets.md) before quoting** — flat-vol BS will systematically misprice the wings.

## Output conventions

When delivering a price, report:
- **Premium** in both quote currency per unit and as % of notional
- **Model used** (BS / binomial steps / MC paths)
- **Greeks** (delta, gamma, vega, theta minimum)
- **Inputs assumed** (especially vol — flag if implied vs. historical)
- **Confidence / caveats** — particularly if the underlying is illiquid, if vol is stale, or if the payoff is near a discontinuity (barrier, binary strike)
