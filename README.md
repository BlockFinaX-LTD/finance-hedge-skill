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

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed (CLI, desktop, or IDE extension)
- Git
- Python 3.9+ on `PATH` if you want to run the pricing scripts (pure stdlib — no pip install needed)

### Install the skill

Claude Code auto-discovers skills in `~/.claude/skills/` (user scope, available in every project) or `<project>/.claude/skills/` (project scope, only in that project). Pick one and clone there.

**Windows (PowerShell):**
```powershell
# user scope — recommended
mkdir $env:USERPROFILE\.claude\skills -Force | Out-Null
cd $env:USERPROFILE\.claude\skills
git clone https://github.com/BlockFinaX-LTD/finance-claude-skill.git dynamic-hedging
```

**macOS / Linux:**
```bash
# user scope — recommended
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/BlockFinaX-LTD/finance-claude-skill.git dynamic-hedging
```

The directory **must be named `dynamic-hedging`** so the path matches the `name:` field in `SKILL.md`.

### Configure source-book paths (one-time)

Two reference files were authored against specific paths on the original machine. After cloning, you may need to update them so they point to your own paths:

- `SKILL.md` and `references/hull_navigator.md` reference Hull's book at `c:\Users\ADMIN\rift\financeskill\derivatives.md`. The skill still works without it — all 11 Hull distillation files stand alone — but **verbatim quote lookups** from Hull's source require the file. If you have Hull's textbook in markdown, place it somewhere local and update these two files with the new absolute path (or delete the references entirely).
- Taleb's source (`references/dynamic_hedging_full.md`) is **included in the repo**, so no action needed for Taleb.

### Verify

1. Restart Claude Code (or reload its skill registry).
2. In a new conversation, ask:
   ```
   /list-skills
   ```
   or simply:
   ```
   what skills do you have available?
   ```
3. You should see `dynamic-hedging` in the listing. Test with a sample query:
   ```
   Price a 3-month ATM call on a stock at $100, vol 25%, risk-free 5%.
   ```
   Claude should invoke the skill, use `scripts/bs_pricer.py`, and return premium plus Greeks.

### Updating

```bash
cd ~/.claude/skills/dynamic-hedging
git pull
```
Claude Code reloads the skill on next session start.

### Uninstalling

```bash
rm -rf ~/.claude/skills/dynamic-hedging         # macOS / Linux
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\dynamic-hedging   # Windows
```

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
