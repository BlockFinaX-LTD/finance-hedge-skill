# Emerging Markets Overlay

Taleb's 1997 book doesn't have a dedicated EM chapter, but the entire framework applies — EM is just where the book's assumptions (constant vol, continuous trading, Gaussian returns) break hardest. This file applies the Taleb lens to EM specifically.

## What makes EM derivatives different

1. **Fat tails are fatter.** Empirical kurtosis on EM FX (TRY, ARS, RUB historically, NGN, EGP) routinely exceeds 10 vs. ~3 for Gaussian. Ch 15's vvol framework applies but with bigger numbers.
2. **Jumps are the norm.** Devaluation events, central-bank interventions, capital-control announcements. These are discrete-time gaps that no diffusion model captures cleanly.
3. **Liquidity is asymmetric and conditional.** Bid-offer widens 5–20x in stress (Ch 4 territory). Hedging cost ≠ historical slippage.
4. **The risk-neutral measure may not exist economically.** If a currency is pegged or capital controls block the hedging trade, the no-arbitrage argument that underpins BS doesn't hold.
5. **Correlations regime-shift hard.** Calm-regime corrs between EM FX and US rates can flip sign in crisis.

## Asset-class playbook

### EM FX (BRL, MXN, ZAR, TRY, INR, IDR, KRW, COP, CLP, etc.)

- **Default model:** Garman-Kohlhagen (BS for FX) as a *quoting convention*, but with the **smile fitted from market quotes**. Never use flat ATM vol.
- **Skew typically:** strong left skew (devaluation premium) — calls on USD/EM-FX are richer than puts. The market is paying for the tail risk of local-currency depreciation.
- **Rates input:** if onshore rates differ from offshore (capital controls), use NDF-implied yields, not the policy rate.
- **Jump overlay:** for tenors > 1 month, add a Merton-style jump component. Calibrate jump intensity λ to historical event frequency (typically 1–4 events/year), jump size to realized event magnitudes.
- **NDF vs deliverable:** NDF markets (BRL, INR, KRW, TWD, CLP, COP) settle in USD. Pricing logic identical to deliverable forwards but counterparty/settlement risk differs.

### EM equities (single names and indices)

- BS as starting point but with smile + jump overlay
- **Dividend risk:** EM companies cut dividends in crisis. Discrete cash dividend modeling preferred over continuous q.
- **Sovereign overlay:** equity vol correlates with sovereign CDS in stress. If pricing long-dated, build in sovereign-event scenario.
- **Trading halts / circuit breakers:** these are barriers in disguise. If your option could expire during a halted session, that's a discontinuity to model.

### EM rates / inflation-linked

- Use Black-76 on the forward rate as base
- Add a sovereign spread to the discount curve
- High correlation between rates and FX in EM (carry trade unwind dynamics). Cross-Greek (vanna) matters.
- For inflation-linked products: the inflation index itself can be politically manipulated (e.g., Argentina INDEC pre-2015). Use independent estimates.

### EM commodities (commodity-currency linkages)

- Many EM economies are commodity-driven (CLP-copper, ZAR-gold/platinum, BRL-soy/iron). FX vol and commodity vol are linked.
- For options on local commodity producers, double-count the sovereign + commodity exposure.

## Specific event types to model

| Event | Asset effect | Pricing adjustment |
|---|---|---|
| **Devaluation** (peg break) | Step jump in FX; vol explodes | Pre-event: model as Bernoulli with size×prob; post-event: re-strike everything |
| **Capital controls imposed** | Onshore-offshore basis blows out | Use offshore-deliverable instruments only; widen vols |
| **Default / restructuring** | Bond prices collapse; equity goes to zero or near it | Sovereign CDS as proxy; jump-to-default in pricing |
| **Election / referendum** | Vol term structure spikes around date | Build event-specific vol point into the surface |
| **IMF intervention** | Stabilizes vol but introduces conditionality risk | Two-scenario weighting |

## Pegged / managed currencies — special case

For HKD-USD, AED-USD, SAR-USD, and other hard pegs:
- **Don't price as normal FX.** The "spot vol" is near zero but the **break-risk** is a binary event.
- Model as: P(peg holds) × small-vol BS + P(peg breaks) × devaluation jump
- Long-dated OTM calls on USD/peg-currency are essentially binary bets on peg break — price accordingly
- Implied vol on these often looks "too cheap" on a Sharpe basis; that's because it's a binary, not a continuous-vol exposure

## The "Argentina rule" (not in Taleb, but Taleb-adjacent)

For any EM derivative, ask: *"What does this position pay in a hard crisis?"* If the answer requires the counterparty to be solvent and the legal system to honor the contract, factor in:
- Counterparty risk (CVA)
- Settlement risk (will USD actually be deliverable?)
- Legal risk (can the contract be enforced under local law?)

A theoretically-perfect hedge that can't settle is worse than no hedge.

## What scripts to use

- `bs_pricer.py` — fine as the *baseline* but always layer on smile and jumps for EM
- `em_adjustments.py` — Merton jump-diffusion overlay, smile widening, peg-break decomposition
- `monte_carlo.py` — best for any EM exotic; supports jump-diffusion and stochastic vol

## Sanity check before quoting EM

1. Do I have a real vol surface or am I extrapolating?
2. Is there an upcoming scheduled event (election, central bank, IMF) within the tenor?
3. Is the underlying tradable for hedging in the size I'm pricing?
4. What's the realistic bid-offer if I had to unwind in stress (not in calm)?
5. Have I priced the jump risk separately from the diffusive vol?

If any answer is "no" or "unknown," widen the spread or refuse to quote.
