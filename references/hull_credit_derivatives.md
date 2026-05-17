# Credit Derivatives (Hull Ch 25)

CDS, indices, CDOs, and the Gaussian copula. Read [hull_credit_risk.md](hull_credit_risk.md) first for the default-probability framework.

## Single-name CDS

**Mechanics:** Protection buyer pays a periodic premium (the **CDS spread**, in bp p.a.) to the protection seller. On a credit event (default, restructuring) on the reference entity:
- Buyer delivers a defaulted obligation
- Seller pays par (or settles cash for par − recovery)

Standard contract: 5-year tenor, ISDA standard documentation, quarterly payments (Mar/Jun/Sep/Dec 20). Big-Bang protocol (2009) standardized restructuring clauses and made CDS centrally clearable.

**Quote convention:** the spread `s` is the premium that makes the contract have zero value at initiation. As credit improves, existing protection becomes less valuable; new spreads tighten. P&L on a long-protection position is roughly:
```
ΔV ≈ −Notional · (s_new − s_old) · RPV01
```
where RPV01 = risky annuity (PV of 1 bp of spread paid until default or maturity).

## CDS valuation

Decompose into two legs:

**Premium leg** (buyer pays):
```
PV_prem = s · Σ τ_i · DF_i · S(t_i)
```
where S(t_i) = survival prob at i, DF_i = discount factor.

**Protection leg** (seller pays if default):
```
PV_prot = (1 − R) · ∫₀ᵀ DF(t) · dQ(t)
       ≈ (1 − R) · Σ DF(t_i) · [S(t_{i−1}) − S(t_i)]
```

Fair spread: `s* = PV_prot / Σ τ_i · DF_i · S(t_i)`. With constant hazard rate λ:
```
s ≈ λ · (1 − R)   (credit triangle)
```

ISDA Standard Model (cdsmodel.com) is the industry-standard pricer; closed form under constant hazard, constant interest rate, and 40% fixed recovery.

## Implied hazard rate

Given a CDS spread term structure (1Y, 3Y, 5Y, 7Y, 10Y) and assumed R = 40%:
- Bootstrap piecewise-constant λ(t) so each CDS price equals the market
- Same machinery as bootstrapping a zero curve from swap rates

The bootstrapped hazard curve gives you risk-neutral default probabilities at any horizon for that name.

## CDS indices

**CDX** (North America), **iTraxx** (Europe / Asia) — equally-weighted baskets of 100–125 single-name CDS. Subindices:
- CDX.IG — Investment Grade NA (125 names)
- CDX.HY — High Yield NA (100 names)
- iTraxx Europe — IG European (125 names)
- iTraxx Crossover — sub-IG European (75 names)

Roll every 6 months on Mar 20 / Sep 20. New "on-the-run" series replaces older series; existing positions remain on the previous series.

**Index spread ≠ average of single-name spreads** — the index trades on its own supply/demand. The difference is the **index basis** (a few bp).

## CDS index tranches

Tranches of an index basket. Standard attachment/detachment points (CDX.IG):
- 0–3% (equity)
- 3–7% (mezzanine)
- 7–15% (senior mezz)
- 15–30% (senior)
- 30–60% (super senior, rare)

Tranche pays out losses on the index portfolio between attachment and detachment. Equity wiped first; super-senior survives unless losses exceed 30%.

## The Gaussian copula — David X. Li (2000)

The market standard pricing model for CDS index tranches and CDOs. Notorious for its role in the 2008 crisis.

**Setup:** Each reference entity i has a default time τ_i, with marginal CDF Q_i(t) (from single-name CDS curves). Define standard-normal latent variable:
```
X_i = ρ · M + √(1 − ρ²) · Z_i
```
where M is a common factor (the "market"), Z_i are idiosyncratic, all standard normal.

Default trigger: entity i defaults by time t if `X_i ≤ N⁻¹(Q_i(t))`.

**Conditional on M = m**, defaults are independent. Given M = m, the conditional default probability of name i is:
```
p_i(t | m) = N( [N⁻¹(Q_i(t)) − ρm] / √(1 − ρ²) )
```

Loss distribution: integrate over M (standard normal). Equally-weighted, equally-correlated index → loss distribution is tractable in closed form (recursive Andersen-Sidenius-Basu, or Hull-White binomial recursion).

**The single number:** the "compound correlation" or **base correlation** is the ρ that makes the Gaussian copula price match the market tranche price. Different tranches imply different correlations — analogous to volatility smile in equity options. The market quotes tranches via base correlations.

## Why the copula broke in 2008

The pricing framework is mathematically fine. The problems were:
1. **ρ was calibrated to benign-era data** when defaults appeared idiosyncratic. The crisis revealed near-perfect default correlation in the subprime mortgage pool.
2. **Senior tranche pricing is exquisitely correlation-sensitive.** A move in ρ from 0.2 to 0.5 changes a "AAA" super-senior's expected loss by orders of magnitude.
3. **No tail dependence.** The Gaussian copula has tail-dependence coefficient = 0 — pairwise extreme events are asymptotically independent. Reality has substantial tail dependence (defaults cluster in crises). The t-copula and Clayton copula address this; both were known pre-2008 and ignored.

David X. Li himself warned the model was being misused. The famous Wired headline "Recipe for Disaster: The Formula That Killed Wall Street" (2009) overstates Li's responsibility but captures the systemic over-reliance.

## Synthetic CDOs

Same tranching as cash CDOs but the underlying is a pool of single-name CDS (or an index) rather than physical bonds. Pricing via Gaussian copula (or successor models). Synthetic CDOs were the main vehicle through which AIG took catastrophic exposure to senior credit risk.

## Other credit derivatives Hull covers

- **Binary CDS** — fixed payoff on default (not par-minus-recovery)
- **Basket CDS** — pays out on Nth default in a basket of names
- **CDS on indices / sectors / sovereigns** — same mechanics
- **Total return swap (TRS)** — one party pays total return on a bond/loan, the other pays a financing rate. Effectively a synthetic long-bond position without funding.
- **CDS options** — option on a forward-starting CDS, or a credit default swaption

## Practical rules

1. **CDS spread × duration ≈ MTM sensitivity per bp.** Memorize RPV01 for the 5Y on-the-run names you trade.
2. **Hazard rate ≈ spread / (1 − R).** R = 40% by market convention; use higher R for secured, lower for subordinated.
3. **Don't price senior CDO tranches with Gaussian copula and a calibrated ρ from benign data.** This is the 2008 mistake.
4. **Use t-copula or Clayton copula for tail-aware pricing.** Or just stress ρ → 1 as a sanity check on senior tranches.
5. **Wrong-way risk in single-name CDS:** never buy protection on a counterparty who is correlated with the reference entity (e.g. don't buy GS protection from Morgan Stanley).
6. **Index basis is a real thing.** Don't assume index = average of single names.
7. **CDS is a quoted spread, not a price.** "Tightening" = spread going down = protection getting cheaper = the credit improving.

Cross-link: [hull_credit_risk.md](hull_credit_risk.md) for default probability framework, [hull_securitization.md](hull_securitization.md) for the 2008 backdrop and CDO structuring, [hull_xvas.md](hull_xvas.md) for using CDS spreads to imply CVA hedges, [hull_mishaps.md](hull_mishaps.md) for AIG.
