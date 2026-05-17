# Chapter Navigator — Dynamic Hedging

Line ranges into `references/dynamic_hedging_full.md` (in-skill copy, ~18,517 lines; identical to original at `C:\Users\ADMIN\rift\financeskill\dynamic_hedging.md`). When you need authoritative text, read the relevant range with the Read tool — do not paraphrase Taleb from memory.

**Distilled chapters** (own reference file) — read the reference file first, drop into the source only for verbatim quotes or examples not in the distillation:

- Ch 1 → [instruments.md](instruments.md)
- Ch 2 → [pricing_decision_tree.md](pricing_decision_tree.md) (also covers method selection)
- Ch 3 → [market_making.md](market_making.md)
- Ch 4 → [liquidity.md](liquidity.md)
- Ch 5 → [arbitrage.md](arbitrage.md)
- Ch 6 → [volatility_correlation.md](volatility_correlation.md)
- Ch 7–11 → [greeks.md](greeks.md)
- Ch 12 → [fungibility.md](fungibility.md)
- Ch 13 → [option_market_wrinkles.md](option_market_wrinkles.md)
- Ch 14 → [bucketing.md](bucketing.md)
- Ch 15 → [fat_tails.md](fat_tails.md)
- Ch 16 → [trading_concepts.md](trading_concepts.md)
- Ch 17–23 → [exotic_options.md](exotic_options.md)
- Module A → [brownian_motion.md](brownian_motion.md)
- Module B → [risk_neutrality.md](risk_neutrality.md)
- Module C → [numeraire.md](numeraire.md)
- Module D → [correlation_triangles.md](correlation_triangles.md)
- Module E → [var.md](var.md)
- Module F → [probabilistic_rankings.md](probabilistic_rankings.md)
- Module G → [option_pricing_math.md](option_pricing_math.md)
- EM overlay (cross-chapter synthesis) → [emerging_markets.md](emerging_markets.md)

**All chapters now distilled.** Every chapter and module in the book has a dedicated reference file. The source `dynamic_hedging_full.md` remains canonical for verbatim quotes, worked examples, and footnotes not captured in the distillations.

## Part I — Markets, Instruments, People

| # | Chapter | Lines | Read when |
|---|---|---|---|
| 1 | Introduction to the Instruments | 1683–2910 | Classifying a product; forwards vs. futures; primary vs. secondary risks |
| 2 | The Generalized Option | 2913–3321 | Decomposing any structure along 6 dimensions before pricing |
| 3 | Market Making and Market Using | 3324–4247 | Bid-offer logic, adverse selection, "monkeys on a typewriter" P/L statistics |
| 4 | Liquidity and Liquidity Holes | 4250–4873 | Stop orders, barrier vacuums, why slippage models lie |
| 5 | Arbitrage and the Arbitrageurs | 4876–5267 | What truly counts as arb; squeezes; arb duration |
| 6 | Volatility and Correlation | 5268–5936 | "There is no such thing as constant vol or correlation"; Parkinson estimator |

## Part II — Measuring Option Risks

| # | Chapter | Lines | Read when |
|---|---|---|---|
| 7 | Adapting BSM: The Delta | 6134–6826 | Delta definitions; why continuous-time delta ≠ hedge ratio; the half-billion-dollar delta story (~6223) |
| 8 | Gamma and Shadow Gamma | 6827–7321 | Static gamma is incomplete; gamma's vol/time dependence |
| 9 | Vega and the Volatility Surface | 7322–8019 | Smile, skew, term structure; vega convexity |
| 10 | Theta and Minor Greeks | 8020–9003 | Theta decay shape; charm/vanna/volga/color |
| 11 | The Greeks and Their Behavior | 9004–9746 | Cross-Greek interactions; what changes near expiry, near the money, in vol moves |
| 12 | Fungibility, Convergence, and Stacking | 9747–10346 | When positions truly offset and when they don't |
| 13 | Some Wrinkles of Option Markets | 10347–10708 | Market quirks: pin risk, expiry mechanics, settlement |
| 14 | Bucketing and Topography | 10709–11096 | Aggregating Greeks correctly across tenor/strike/underlying |
| 15 | **Beware the Distribution** | 11097–11786 | **CORE FAT-TAIL CHAPTER.** Stochastic vol, vvol, smile origin, histograms of real markets |
| 16 | Option Trading Concepts | 11787–12454 | Practical heuristics; risk-reversals, butterflies, calendars |

## Part III — Trading and Hedging Exotic Options

| # | Chapter | Lines | Read when |
|---|---|---|---|
| 17 | Binary Options: European Style | 12510–13463 | Cash-or-nothing, asset-or-nothing; smile-implied prices |
| 18 | Binary Options: American Style | 13464–14110 | One-touch, no-touch; American digital pricing |
| 19 | Barrier Options (I) | 14111–15314 | Knock-in/out mechanics; static replication |
| 20 | Barrier Options (II) | 15315–16338 | Advanced barrier behavior, delta tricks, double barriers |
| 21 | Compound, Choosers, and Higher Order | 16339–16585 | Options on options; chooser pricing |
| 22 | Multiasset Options | 16586–17410 | Baskets, rainbows, spread options; correlation as a risk |
| 23 | Minor Exotics: Lookback and Asian | 17411–17769 | Floating/fixed strike lookback; arithmetic vs. geometric Asian |

## Part IV — Modules (Mathematical Foundations)

| # | Module | Lines | Read when |
|---|---|---|---|
| A | Brownian Motion on a Spreadsheet | 17784–18213 | Intuition for paths; bridging discrete-continuous |
| B | Risk Neutrality Explained | 18214–18405 | Why we use Q-measure for pricing |
| C | Numeraire Relativity / Two-Country Paradox | 18406–18698 | FX option pricing subtleties; Siegel's paradox |
| D | Correlation Triangles | 18699–18899 | Multi-asset correlation constraints |
| E | Value-at-Risk | 18900–19269 | VaR construction and limitations |
| F | Probabilistic Rankings in Arbitrage | 19270–19579 | Comparing arb strategies under uncertainty |
| G | Option Pricing | 19580–20315 | Pricing models, stochastic vol formulation |

## Front matter

| Section | Lines |
|---|---|
| Preface | 178–405 |
| Acknowledgments | 406–461 |
| Contents | 462–1456 |
| Introduction: Dynamic Hedging | 1457–1664 |

## Topic → chapter shortcuts

- **"Why does my BS price disagree with the market?"** → Ch 9 (vol surface) + Ch 15 (fat tails)
- **"How do I hedge this barrier?"** → Ch 19–20 + Ch 7 (delta caveats)
- **"What's the right way to think about gamma?"** → Ch 8 (shadow gamma) + Ch 11
- **"How risky is my book in aggregate?"** → Ch 14 (bucketing) + Module E (VaR)
- **"How do I price a basket?"** → Ch 22 + Module D
- **"Smile / skew / sticky strike vs sticky delta?"** → Ch 9 + Ch 15
- **"Early exercise / American options?"** → Ch 1 (lines ~508–520) + Ch 18 for American binaries
