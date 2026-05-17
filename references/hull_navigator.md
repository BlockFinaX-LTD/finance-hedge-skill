# Hull Navigator — Options, Futures, and Other Derivatives (10th ed.)

Approximate line ranges into `c:\Users\ADMIN\rift\financeskill\derivatives.md` (~57k lines). Use Read with offset/limit for authoritative text; chapters are paste-ordered so a few sections appear out of numeric sequence.

**Hull vs Taleb — when to read which:**
- **Hull** = textbook, math-first, formal derivations, full taxonomy of instruments, post-1997 markets (CDS, ABS, XVAs, OIS discounting). Use for: rates derivatives, credit derivatives, swaps, securitization, real options, GARCH, formal model derivations.
- **Taleb** = trader, practitioner, P/L-first, fat-tail and microstructure obsessions. Use for: market making, liquidity holes, smile/skew intuition, exotic option hedging tricks, emerging markets, "why the model is wrong."

Many topics appear in both — when so, the dedicated Hull distillation cross-links to the Taleb one and vice versa.

## Hull → distillation map

**Distilled (own reference file):**
- Ch 4 → [hull_interest_rates.md](hull_interest_rates.md)
- Ch 7 → [hull_swaps.md](hull_swaps.md)
- Ch 8 → [hull_securitization.md](hull_securitization.md)
- Ch 9 → [hull_xvas.md](hull_xvas.md)
- Ch 23 → [hull_garch.md](hull_garch.md)
- Ch 24 → [hull_credit_risk.md](hull_credit_risk.md)
- Ch 25 → [hull_credit_derivatives.md](hull_credit_derivatives.md)
- Ch 29–33 → [hull_ir_derivatives.md](hull_ir_derivatives.md)
- Ch 36 → [hull_real_options.md](hull_real_options.md)
- Ch 37 → [hull_mishaps.md](hull_mishaps.md)

**Covered by Taleb distillation (read Taleb first, drop into Hull for formal proofs):**
- Hull Ch 1–3, 5–6 → see [instruments.md](instruments.md), [market_making.md](market_making.md), [liquidity.md](liquidity.md)
- Hull Ch 10–12 → [instruments.md](instruments.md), [trading_concepts.md](trading_concepts.md)
- Hull Ch 13 → bridges to [option_pricing_math.md](option_pricing_math.md) (Hull's tree treatment is the standard reference)
- Hull Ch 14 → [option_pricing_math.md](option_pricing_math.md) (Itô/Wiener)
- Hull Ch 15 → [option_pricing_math.md](option_pricing_math.md) + [risk_neutrality.md](risk_neutrality.md)
- Hull Ch 17–18 → [instruments.md](instruments.md) (FX/index/futures options, Garman-Kohlhagen, Black-76)
- Hull Ch 19 → [greeks.md](greeks.md)
- Hull Ch 20 → [fat_tails.md](fat_tails.md) (Hull's smile coverage is descriptive; Taleb's is causal)
- Hull Ch 21 → [option_pricing_math.md](option_pricing_math.md) + scripts
- Hull Ch 22 → [var.md](var.md) (Hull adds expected shortfall, basel back-testing)
- Hull Ch 26 → [exotic_options.md](exotic_options.md)
- Hull Ch 28 → [risk_neutrality.md](risk_neutrality.md), [numeraire.md](numeraire.md)

## Approximate line ranges (paste-ordered)

| # | Chapter | Lines | Notes |
|---|---|---|---|
| 1 | Introduction | 1–2300 | Derivatives markets overview, hedgers/speculators/arbitrageurs |
| 2 | Mechanics of Futures Markets | 2300–3700 | Margin, clearing, daily settlement |
| 3 | Hedging Strategies Using Futures | 3700–5300 | Minimum-variance hedge ratio, stack-and-roll |
| 4 | Interest Rates | 5300–7300 (also ~37231) | Compounding, zero/par/forward, FRA, duration, convexity |
| 5 | Determination of Forward & Futures Prices | 7300–8900 | Cost of carry, consumption assets, convenience yield |
| 6 | Interest Rate Futures | 8900–10200 | T-bond futures, Eurodollar futures, convexity adjustment, duration-based hedging |
| 7 | Swaps | ~10200–11800 (heading at 11492) | IRS, currency swap, comparative advantage, OIS discounting |
| 8 | Securitization & Credit Crisis of 2007 | 11800–12700 | ABS, MBS, CDO, waterfall, ABS CDO, 2007 crisis |
| 9 | XVAs (CVA/DVA/FVA/MVA/KVA) | 12700–13300 | Credit/debit/funding/margin/capital valuation adjustments |
| 10 | Mechanics of Options Markets | 13300–14700 | American/European, contract specs, margin |
| 11 | Properties of Stock Options | ~14698–15800 | Bounds, put-call parity, early exercise rules |
| 12 | Trading Strategies Involving Options | 15800–17000 | Spreads, combinations |
| 13 | Binomial Trees | 16950–19250 | CRR tree, risk-neutral valuation, American options |
| 14 | Wiener Processes & Itô's Lemma | 19256–21000 | Markov processes, GBM, log-normal property |
| 15 | The Black-Scholes-Merton Model | 21000–23700 | BSM derivation, dividend yields, implied vol |
| 16 | Employee Stock Options | 23700–24500 | Accounting, vesting, valuation |
| 17 | Options on Stock Indices & Currencies | 24500–25600 | Garman-Kohlhagen, range forwards |
| 18 | Futures Options & Black's Model | 25600–26600 | Black-76, put-call parity for futures options |
| 19 | The Greek Letters | 26626–28900 | Delta hedging, gamma, vega, theta, dynamic hedging |
| 20 | Volatility Smiles | 28918–29900 | Smile/skew descriptions, sticky strike vs sticky delta |
| 21 | Basic Numerical Procedures | 29984–36300 | Tree methods, finite differences, Monte Carlo |
| 22 | Value at Risk & Expected Shortfall | 36312–~37200 | VaR, ES, historical sim, model building, stressed VaR |
| 23 | Estimating Volatilities & Correlations | ~37200–39800 | EWMA, GARCH(1,1), maximum likelihood, consistent correlations |
| 24 | Credit Risk | 39806–41587 | Default probs, recovery rates, Merton model, CVA/DVA basics |
| 25 | Credit Derivatives | 41587–~43000 | CDS, hazard rates, CDS indices, ABS CDO, Gaussian copula |
| 26 | Exotic Options | ~43000–45600 | Hull's enumeration of exotics: packages, perpetuals, barriers, Asians, lookbacks, baskets |
| 27 | More on Models and Numerical Procedures | ~45600–47500 | Jump-diffusion, stochastic vol, IVF model, variance reduction |
| 28 | Martingales and Measures | 47546–~50000 | Change of numeraire, equivalent martingale measure, forward risk-neutral measure |
| 29 | Interest Rate Derivatives: Standard Market Models | ~50000–~52000 | Black's model for bond options, caps, swaptions |
| 30 | Convexity, Timing, Quanto Adjustments | ~52000–~53500 | Convexity adjustment, quanto adjustment, timing adjustment |
| 31 | Interest Rate Derivatives: Models of the Short Rate | ~53500–~55000 | Vasicek, CIR, Hull-White, two-factor models |
| 32 | HJM, LMM, and Multiple Zero Curves | ~55000–~56500 | HJM framework, LIBOR Market Model, multi-curve discounting |
| 33 | Swaps Revisited | ~56500–~57200 | Compounding swaps, currency swaps, accrual swaps |
| 34 | Energy & Commodity Derivatives | ~57200–~57400 | Agricultural, energy, weather; mean-reversion models |
| 35 | Real Options | ~57400–57533 | Investment as option, abandonment, expansion |
| 36 | Real Options | 57533–~57700 | (heading found at 57533) |
| 37 | Derivatives Mishaps & Lessons | ~57700–end | Barings, LTCM, AIG, JPM London Whale, lessons |

*(Chapter numbering varies slightly across Hull editions — 36/37 in 10th ed. The exact boundary between Ch 35/36/37 depends on which sections the paste preserved.)*

## Topic → Hull chapter shortcuts

- **"How do I price a swap?"** → Ch 7 + Ch 28 (martingales for general framework) + [hull_swaps.md](hull_swaps.md)
- **"What's CVA/DVA/FVA?"** → Ch 9 + [hull_xvas.md](hull_xvas.md)
- **"How does a CDS work?"** → Ch 25 + [hull_credit_derivatives.md](hull_credit_derivatives.md)
- **"GARCH vs EWMA for vol estimation?"** → Ch 23 + [hull_garch.md](hull_garch.md)
- **"Short-rate model — Vasicek or Hull-White?"** → Ch 31 + [hull_ir_derivatives.md](hull_ir_derivatives.md)
- **"How do I model an investment as an option?"** → Ch 36 + [hull_real_options.md](hull_real_options.md)
- **"Big derivatives losses — what to learn?"** → Ch 37 + [hull_mishaps.md](hull_mishaps.md)
- **"How does securitization work?"** → Ch 8 + [hull_securitization.md](hull_securitization.md)
- **"Duration-based hedge with Eurodollar futures?"** → Ch 6 + Ch 4 + [hull_interest_rates.md](hull_interest_rates.md)
- **"Counterparty credit risk modeling?"** → Ch 24 + Ch 9 + [hull_credit_risk.md](hull_credit_risk.md)
