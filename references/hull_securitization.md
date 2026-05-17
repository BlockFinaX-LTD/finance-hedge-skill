# Securitization & The Credit Crisis of 2007 (Hull Ch 8)

How loans get repackaged into tradable securities, and how the resulting structures became the centerpiece of the 2007–08 financial crisis. Taleb's 1997 book predates the post-2000 structured-credit explosion, so this is Hull-exclusive territory.

## ABS — the basic structure

An asset-backed security (ABS) sells a pool of cash-flow-generating loans (mortgages, auto loans, credit-card receivables) to a special purpose vehicle (SPV). The SPV issues tranches with different seniority:

```
Assets ──→ SPV ──┬──→ Senior tranche      (e.g. 80%)  ──  rated AAA
                 ├──→ Mezzanine tranche   (e.g. 15%)  ──  rated BBB
                 └──→ Equity tranche      (e.g.  5%)  ──  unrated
```

**Waterfall:** interest and principal cash flows are paid sequentially — senior first, then mezz, then equity. **Losses absorb in reverse order:** first 5% wipes equity, next 15% wipes mezz, then senior takes hits.

A senior tranche is "AAA" because in normal scenarios it gets paid before junior tranches lose principal. The equity tranche has the highest *promised* yield but absorbs first loss.

## MBS — mortgage-backed securities

The original asset class. Two main subtypes:
- **Agency MBS** (Ginnie Mae / Fannie Mae / Freddie Mac) — government-guaranteed against credit default. Investors bear only prepayment risk.
- **Non-agency MBS** (private label, including subprime) — investors bear both credit and prepayment risk.

**Prepayment risk:** when rates fall, borrowers refinance → MBS receives principal back early at exactly the time reinvestment yields are worst. Negative convexity. Hull notes early MBS investors underestimated this.

## CDOs and ABS CDOs

A **CDO** (collateralized debt obligation) is an ABS whose underlying pool is itself bonds or loans (corporate bonds, leveraged loans, ABS tranches).

An **ABS CDO** (or Mezz ABS CDO) pools the *mezzanine* tranches of many ABSs and re-tranches them. Because the underlying tranches were already BBB, a small percentage of cumulative loss in the raw pool would wipe most of the ABS-CDO mezz tranches — yet the senior 65% of the ABS CDO was still rated AAA.

```
Raw assets ──→ ABS                       ──→ Senior (80%) AAA
                                          ├──→ Mezz (15%)  BBB ──┐
                                          └──→ Equity (5%)        │
                                                                  ↓
                                Pool of many ABS Mezz tranches ──→ ABS CDO
                                                                        ├──→ Senior (65%) "AAA"
                                                                        ├──→ Mezz (25%)   BBB
                                                                        └──→ Equity (10%)
```

Hull's key arithmetic: in the example structure, **90% of the principal of the underlying loans was rated AAA** (80% of ABS + 65% of 15% of ABS via the CDO). This is much more AAA paper than the underlying loans could realistically support.

## How AAA blew up — Hull's mechanics

The AAA-rated tranche of the ABS itself survives losses up to 20% on the underlying loan pool. The AAA tranche of the ABS CDO is far more fragile:

| Loss on raw pool | ABS equity | ABS mezz loss % | ABS CDO senior loss |
|------------------|-----------|-----------------|---------------------|
| 10% | wiped | 5/15 = 33% | survives (equity+mezz of CDO absorb) |
| 10.25% | wiped | 35% | just survives (mezz CDO wiped) |
| 17% | wiped | 80% | loses 45/65 = 69% of principal |
| 20% | wiped | 100% | wiped |

So the "AAA" senior tranche of the ABS CDO is destroyed entirely by a 20% loss on the raw pool — the same loss level that the AAA tranche of the ABS itself just barely survives. **Same rating, vastly different risk.**

## Why ratings failed

1. **Correlation underestimated.** Rating agencies modelled defaults with assumed loss correlations that fit benign times. In a regional housing downturn, mortgages default together (regional shocks dominate idiosyncratic risk).
2. **Static rating snapshot.** AAA bonds historically had near-zero default rates over a 5-year horizon, so the same label was applied to ABS CDO seniors without recognizing that the rating-to-loss-distribution relationship was utterly different.
3. **Issuer-pays model.** Agencies were paid by structurers, who shopped for ratings.
4. **Gaussian copula misuse** — see [hull_credit_derivatives.md](hull_credit_derivatives.md) on the David X. Li copula.

## Incentive failures

Hull is explicit (Ch 8.4) about the broken incentive chain:
- **Borrowers** — many were liar / NINJA loans (no income, no job, no assets) underwritten with no documentation.
- **Mortgage brokers** — paid on origination volume, no skin in the game post-sale.
- **Originators** — sold loans to securitizers, off-balance-sheet, so default risk was someone else's problem.
- **Securitizers** — fee-based on issuance volume.
- **Rating agencies** — paid by issuer, competed on lenient ratings.
- **Senior bank executives** — bonus-incentivized on accounting profit, asymmetrically rewarded for taking unrecognized tail risk.
- **Investors** — relied on the AAA label, didn't model the underlying.

The Dodd-Frank rule (2010) requiring originators to retain at least 5% of any securitization addresses this — sellers must keep some skin in the game.

## What happened in 2007–08

1. House prices peaked 2006, then fell ~30% national average (much more in subprime-heavy markets).
2. Subprime mortgage delinquencies rose, ABS equity wiped, mezz wiped.
3. ABS CDO mezz and even senior tranches lost most of their principal.
4. Banks held large amounts of "super-senior" ABS CDO paper that they had marked at AAA — write-downs were massive.
5. Counterparty trust collapsed. AIG had written CDS protection on hundreds of billions of ABS CDOs (no margin, no collateral) — when MTM moved, collateral calls bankrupted them. Bear Stearns and Lehman failed on related exposures.
6. The interbank market froze (LIBOR-OIS spread blew out from ~10 bp to >350 bp).

## Lessons (Hull §8.5 + Ch 37)

1. **Rating ≠ risk distribution.** Tail risk of a "AAA" ABS CDO senior is nothing like tail risk of a true AAA corporate bond.
2. **Correlation is the dominant risk in pooled credit.** A small change in assumed default correlation dramatically changes loss distribution of senior tranches.
3. **Tranching does not create AAA out of thin air** — it slices the loss distribution, but does not reduce total losses.
4. **Skin-in-the-game matters.** Originator retention requirements reduce moral hazard.
5. **Transparency.** Investors must be able to look through to the underlying loans, not just the rating.

## Practical rules

1. **Look through every tranche.** A AAA tranche on a pool of BBB tranches is a different beast than a AAA corporate bond.
2. **Stress correlation.** For senior tranches the loss distribution is overwhelmingly correlation-driven; flat-correlation copula pricing systematically underprices senior risk.
3. **Beware the "no losses in N years" headline.** The mortgage securities that blew up in 2008 had impeccable backtests through 2006.
4. **Cross-link:** see [hull_credit_derivatives.md](hull_credit_derivatives.md) for Gaussian copula CDO pricing, [hull_credit_risk.md](hull_credit_risk.md) for default probability framework, [hull_mishaps.md](hull_mishaps.md) for the broader crisis postmortem.
