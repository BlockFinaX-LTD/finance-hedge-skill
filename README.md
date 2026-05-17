# dynamic-hedging

A Claude Code skill for option pricing and derivatives risk management. Grounded in two canonical sources:

- **Nassim Taleb** — *Dynamic Hedging: Managing Vanilla and Exotic Options* (1997) — trader/practitioner perspective
- **John Hull** — *Options, Futures, and Other Derivatives* (10th ed., 2018) — textbook/math-first reference

The two complement each other: Taleb gives intuition (smile causality, liquidity holes, fat tails, market microstructure); Hull gives formal machinery and post-1997 coverage (CDS, ABS, XVAs, OIS discounting, GARCH, LMM, real options, mishaps postmortems).

## What this skill covers

- Vanilla and exotic option pricing across all asset classes (equities, FX, rates, commodities, crypto, credit, emerging markets)
- The full Greeks (delta, gamma, vega, theta, rho, plus shadow gamma, charm, vanna, volga, color)
- Volatility smile/skew fitting (SVI, SABR), implied vs historical vol, GARCH(1,1) / EWMA
- Black-Scholes-Merton and its real-world failures; stochastic vol (Heston), jump-diffusion (Merton)
- Exotic structures: binaries, barriers, lookbacks, Asians, compound options, baskets, spreads
- Swaps (IRS, currency, basis, equity, variance) — valuation, OIS discounting
- Credit derivatives — CDS, indices, Gaussian copula CDO pricing, hazard rate bootstrapping
- XVAs — CVA, DVA, FVA, MVA, KVA
- Interest rate derivatives — Black-76, Vasicek, CIR, Hull-White, HJM, LMM, multi-curve discounting
- Securitization — ABS, MBS, CDO tranching, waterfall, 2007 credit crisis lessons
- Risk management — VaR, Expected Shortfall, bucketing, P/L attribution
- Real options on capital projects
- Emerging markets overlays (jump-diffusion, devaluation skew, peg-break decomposition, capital controls)
- Derivatives mishaps postmortems (Barings, LTCM, AIG, JPM London Whale, etc.)

## Structure

```
dynamic-hedging/
├── SKILL.md                     # Lean workflow + pointers
├── references/                  # Distilled topic files + canonical sources
│   ├── chapter_navigator.md     # Taleb book → line range index
│   ├── hull_navigator.md        # Hull book → line range index
│   ├── dynamic_hedging_full.md  # (NOT in this repo — see setup)
│   ├── instruments.md, greeks.md, fat_tails.md, ...   # Taleb distillations
│   └── hull_swaps.md, hull_xvas.md, hull_credit_*.md, ...  # Hull distillations
└── scripts/                     # Pure-stdlib Python pricers
    ├── bs_pricer.py             # Black-Scholes + Greeks + IV solver
    ├── binomial_pricer.py       # CRR tree, American/European/Bermudan
    ├── monte_carlo.py           # Asian, barrier, lookback, spread, basket
    ├── heston_pricer.py         # Stochastic vol via characteristic function
    ├── smile_fitter.py          # SVI + SABR smile fitting
    └── em_adjustments.py        # Merton jump-diffusion, peg-break decomposition
```

## Setup

1. Clone into your Claude Code skills directory:
   ```powershell
   cd $env:USERPROFILE\.claude\skills
   git clone <this-repo-url> dynamic-hedging
   ```
2. Drop your own copy of the Taleb source markdown into `references/dynamic_hedging_full.md` — the skill's chapter navigator references it by line range.
3. (Optional) If you have Hull's textbook in markdown, place it somewhere on disk and update the Hull source path in `SKILL.md` and `references/hull_navigator.md` to match. The skill is fully usable without Hull's source — the Hull distillation files stand alone — but verbatim-quote lookups require the source.
4. Reload Claude Code (skills auto-load from `~/.claude/skills/`). Verify with `/help` — the skill should appear in the list.

## Scripts

All scripts are pure-stdlib Python (no numpy/scipy needed). Run any with `--help`:

```bash
python scripts/bs_pricer.py --S 100 --K 100 --T 0.25 --r 0.05 --sigma 0.2 --type call
python scripts/binomial_pricer.py --S 100 --K 95 --T 0.5 --r 0.05 --sigma 0.3 --steps 1000 --american
python scripts/monte_carlo.py --type asian --S 100 --K 100 --T 1 --r 0.05 --sigma 0.25 --paths 100000
python scripts/heston_pricer.py --S 100 --K 100 --T 1 --r 0.05 --v0 0.04 --kappa 1.5 --theta 0.04 --xi 0.3 --rho -0.7
python scripts/smile_fitter.py --strikes 90,95,100,105,110 --vols 0.25,0.22,0.20,0.21,0.24 --F 100 --T 0.25
python scripts/em_adjustments.py --S 5.0 --K 5.5 --T 0.5 --r 0.10 --sigma 0.20 --jump-lambda 1.0 --jump-mean -0.05 --jump-std 0.15
```

## Reference file conventions

- ~6–7 KB per distillation file
- Lead with key formulas + intuition; end with numbered "Practical rules"
- Cross-link with markdown links
- Cite source by line range so the LLM can read authoritative text when needed
- Taleb files: bare names (`greeks.md`, `fat_tails.md`)
- Hull files: `hull_` prefix (`hull_swaps.md`, `hull_xvas.md`)

## Asset-class default models

| Asset class | Default model | Key adjustments |
|---|---|---|
| DM equities | BS + vol surface | Left-skew, discrete dividends |
| DM FX (G10) | Garman-Kohlhagen | Approximately symmetric smile; widens in crisis |
| Rates | Black-76 / Hull-White / LMM | Multi-curve discounting; smile via SABR-LMM |
| Swaps | Bond/FRA decomposition + OIS | XVA stack for uncollateralized counterparties |
| Credit | Hazard rate / CDS / Gaussian copula | Wrong-way risk; correlation stress on senior tranches |
| Commodities | Black-76 on futures | Seasonality, term structure |
| Crypto | BS as starting point | High vol, fat tails, weekend gaps |
| EM equities | BS + jump overlay | Sovereign risk, low liquidity |
| EM FX | Jump-diffusion or stoch-vol | Devaluation skew, peg/break, capital controls |
| EM rates | Black-76 + sovereign spread | Inflation regime, currency-rates correlation |
| Real options | NPV + tree / LSM | Defer, abandon, expand, switch, compound |

## License

Skill code, scripts, and distillation summaries: MIT (or your preference — TBD).

The source books (`dynamic_hedging_full.md` if added locally, and any Hull markdown you add) remain the copyright of their respective authors and publishers. Do not redistribute.
