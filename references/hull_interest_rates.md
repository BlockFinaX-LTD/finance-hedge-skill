# Interest Rates (Hull Ch 4)

The plumbing for every fixed-income and rates derivative. Read before Ch 6 (interest rate futures), Ch 7 (swaps), and Ch 29–32 (rates derivatives).

## Types of rates Hull distinguishes

| Rate | What it is |
|------|-----------|
| Treasury rate | Government borrowing in its own currency. Lowest credit risk. |
| LIBOR / IBOR | Interbank unsecured lending (London/EU/etc). Reflects bank credit. Now mostly replaced by RFRs. |
| Repo rate | Secured overnight (collateralized borrowing). Lower than LIBOR. |
| Overnight (Fed funds / OIS / SOFR / SONIA / €STR) | Risk-free benchmark. |
| Swap rate | Fixed leg rate that makes a vanilla IRS have zero value. |
| Zero (spot) rate | Yield on a zero-coupon bond of given maturity. |

## Compounding conventions

The same nominal rate means different things under different compounding frequencies. Hull formalizes:
- **m-times-per-year compounding:** A = P · (1 + R_m/m)^(mT)
- **Continuous compounding:** A = P · e^(R_c · T)

Conversion: `R_c = m · ln(1 + R_m/m)`. Continuous compounding is the convention in option pricing because it linearizes the math (the Itô framework).

## Zero rates and bond pricing

A coupon bond is valued by discounting each cash flow at the appropriate **zero rate** for that maturity, not at the bond's own yield:
```
B = Σ c_i · e^(−R_i · t_i) + F · e^(−R_N · t_N)
```
where R_i is the zero rate to time t_i. Bond's yield-to-maturity is the single rate that makes this work for that bond — useful for comparison, not for pricing other bonds.

**Bootstrapping the zero curve:** start with the shortest-maturity instrument with known zero rate, then iteratively solve for longer zero rates from prices of coupon bonds or swap rates.

## Forward rates

The forward rate `R_F` for the period between t_1 and t_2 (with t_1 < t_2) is the rate locked in today for borrowing/lending over that future period.

From zero rates:
```
R_F = (R_2 · t_2 − R_1 · t_1) / (t_2 − t_1)
```
(continuous compounding). With m-compounding the formula is similar but with `(1 + R/m)` terms.

**FRA (forward rate agreement):** OTC contract locking in `R_K` for a period [t_1, t_2]. Cash settled at t_1 in arrears: payoff = L · (R_K − R_realized) · τ / (1 + R_realized · τ). Hull values an FRA as if R_F were certain — discount the expected payoff at the relevant zero rate.

## Duration and convexity

For a bond with price `B` and yield `y`:

**Duration (Macaulay):** weighted-average time to cash flow
```
D = Σ t_i · (c_i · e^(−y t_i) / B)
```

**Modified duration:** `D* = D / (1 + y/m)` (or just D under continuous compounding) — gives price sensitivity:
```
ΔB / B ≈ −D* · Δy
```

**Convexity:** second-order term
```
C = Σ t_i² · (c_i · e^(−y t_i) / B)

ΔB / B ≈ −D · Δy + (1/2) · C · Δy²
```

Duration is the "delta" of a bond w.r.t. yield; convexity is the "gamma." Long bonds have high duration; longer dated AND lower coupon = highest duration. Convexity is always positive for vanilla bonds (price is convex in yield).

**Duration-based hedge ratio** (for hedging with bond futures):
```
N* = (P · D_P) / (V_F · D_F)
```
where P is portfolio value, V_F is futures price, D_P / D_F are durations of portfolio and underlying of the future.

## Parallel-shift limitation

Duration assumes a parallel shift in the zero curve. In reality:
- Curves twist (steepening / flattening)
- Curves butterfly (mid maturities move differently than ends)
- Spread curves (corporate – Treasury) move semi-independently

Better: **key-rate duration** (or partial DV01s) — sensitivity to a shift in each maturity bucket separately. This is Taleb's [bucketing.md](bucketing.md) idea applied to rates.

## Theories of term structure

Hull lists three classical theories (Ch 4.10):
1. **Expectations theory:** forward rates = expected future spot rates. (Empirically false — forwards are biased predictors.)
2. **Market segmentation:** each maturity has its own supply/demand; no necessary linkage. (Too strong; some linkage exists.)
3. **Liquidity preference:** investors prefer short-dated; lenders demand a premium for long-dated. Yield curve typically slopes upward. Most consistent with data.

For derivatives pricing we usually don't take a view on which theory is right — we just bootstrap a zero curve from market prices and project forwards under the appropriate measure.

## Day-count conventions

- **Actual/Actual** — used for US Treasuries
- **30/360** — used for US corporate and municipal bonds
- **Actual/360** — used for US money market (T-bills, LIBOR / SOFR)
- **Actual/365 fixed** — used for GBP money market
- These matter for swap and FRA valuation; sloppy day-count handling produces 1–5 bp errors that add up.

## Quoted vs cash bond prices

For coupon bonds:
- **Quoted (clean) price:** what's quoted in the market.
- **Cash (dirty / invoice) price:** what you actually pay = quoted + accrued interest since last coupon.

T-bond futures invoice price formula:
```
Cash price = (most recent settlement) · (conversion factor) + accrued interest
```

## Practical rules

1. **Continuous compounding for pricing math, market convention for quoting.** Convert at the boundary.
2. **Always bootstrap from liquid instruments.** Pre-2008 the bootstrap was LIBOR/swaps; now it's OIS-discounted from cleared swaps and futures, with FRAs / swaps / basis spreads for the projection curve.
3. **Forward rate ≠ expected future spot rate** under real-world measure. They differ by a risk premium and a convexity term — see Ch 30.
4. **Duration is a parallel-shift first-order approximation.** Use key-rate / partial durations for real risk.
5. **Convexity is positive for vanilla bonds but negative for callable / MBS** — the prepayment option makes the holder short an option, flipping convexity.
6. **Cross-link:** [hull_swaps.md](hull_swaps.md) for swap-rate construction, [hull_ir_derivatives.md](hull_ir_derivatives.md) for option-pricing on rates, [bucketing.md](bucketing.md) for the topographic-risk view, [hull_xvas.md](hull_xvas.md) for the post-crisis OIS discounting framework.
