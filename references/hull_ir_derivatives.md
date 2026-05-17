# Interest Rate Derivatives (Hull Ch 29–32)

Pricing options on rates, swaps, and bonds. The hardest topic in derivatives because the "underlying" is the entire yield curve, not a single asset.

Read after [hull_interest_rates.md](hull_interest_rates.md) (zero curves, forwards) and [hull_swaps.md](hull_swaps.md) (swap mechanics).

## The three main contracts (Ch 29)

### Caps and floors

A **cap** on a floating-rate liability pays the holder when the floating rate exceeds the cap rate K:
```
Caplet payoff at end of period i: L · τ_i · max(R_i − K, 0)
```
A cap is a portfolio of caplets, each a call on a future forward LIBOR / SOFR rate.

A **floor** is the put analog: payoff = `max(K − R_i, 0)`.

A **collar** = long cap + short floor = bracket the float between two strikes.

### European swaptions

Option to **enter** an IRS at a future date at a fixed strike rate K.
- Payer swaption (right to pay fixed K, receive float) = call on swap rate
- Receiver swaption (right to receive fixed K) = put on swap rate

Settlement on exercise: either physical (enter the underlying swap) or cash (pay/receive PV difference at then-prevailing swap rate).

### European bond options

Right to buy/sell a specified bond at strike price K at expiry T. Embedded in callable / putable bonds.

## Black's model for rates (Ch 29)

The simplest market-standard model: assume the underlying *forward* (forward rate, forward swap rate, forward bond price) is lognormal under its T-forward measure. Apply Black-76:
```
caplet: V = L · τ · DF · [F · N(d_1) − K · N(d_2)]
where F = forward rate for the period, DF = discount factor to payment date
d_1 = [ln(F/K) + σ²T/2] / (σ √T)
```

For swaptions, treat the forward swap rate as the underlying and use the **annuity factor** (PV of 1 paid on each fixed-leg date) as the discount measure:
```
payer swaption value = A · [F_swap · N(d_1) − K · N(d_2)]
```

Black's model **isn't fully arbitrage-free across products** — each caplet, each swaption uses its own lognormal assumption, and these are mutually inconsistent. But it's the quoting convention, and for single-product pricing it's fine.

**Lognormal vs normal Black:** in low / negative rate regimes (2014–2021 Europe), lognormal Black breaks down (log of negative rate is undefined). The market uses **shifted lognormal** (`F + α` lognormal for some shift α > 0) or **normal Black** (Bachelier) instead.

## Convexity, timing, and quanto adjustments (Ch 30)

These three adjustments correct for measure mismatches between expected value and quoted forward.

### Convexity adjustment

The forward rate isn't the same as the expected future spot rate under the natural pricing measure. The difference is the convexity adjustment.

Example: a LIBOR-in-arrears swap (LIBOR fixed and paid at start of period) vs vanilla (fixed at start, paid at end). The in-arrears version requires a convexity adjustment:
```
Adjusted forward ≈ F + F² · σ_F² · T / (1 + F · τ)
```

### Timing adjustment

When a payment based on a rate observed at t_1 is paid at t_2 ≠ t_2 (the natural maturity):
```
Adjusted forward = F · exp[ −ρ · σ_R · σ_P · (t_2 − t_1) · T ]
```
where ρ is the correlation between the rate and the discount-bond-to-payment-time, σ_R / σ_P are their vols.

### Quanto adjustment

Payment in currency X based on a rate observed in currency Y:
```
Adjusted forward = F · exp[ ρ · σ_F · σ_FX · T ]
```
where σ_FX is the FX rate vol, ρ is correlation between FX and Y-rate.

Quanto adjustments are big in EM derivatives — local rate × developed-market settlement.

## Short-rate models (Ch 31)

Model the **instantaneous short rate** r(t) and derive everything else from no-arbitrage.

### Vasicek (1977)
```
dr = a (b − r) dt + σ dW
```
- Mean-reverting around b at speed a, constant vol σ
- **Closed-form** bond prices and bond options
- Problem: rates can go negative (sometimes a feature, mostly a bug)

### CIR (Cox-Ingersoll-Ross, 1985)
```
dr = a (b − r) dt + σ √r dW
```
- Mean-reverting, but vol scales with √r so rates can't go negative under Feller condition (2ab ≥ σ²)
- Bond prices in closed form
- Bond options require numerical integration

### Hull-White / Extended Vasicek (Ch 31)
```
dr = [θ(t) − a r] dt + σ dW
```
- θ(t) deterministic function chosen to fit the **initial term structure exactly**
- Same mean-reversion-and-constant-vol structure as Vasicek
- Closed-form bond and option prices via affine framework
- The standard for caps / swaptions pricing in practice

The **two-factor Hull-White** adds a second mean-reverting factor; needed to fit cap and swaption smile / term-structure simultaneously.

### General one-factor short-rate
All one-factor short-rate models share a critical limitation: bond prices of all maturities are perfectly correlated. Real curves twist and butterfly — needs ≥2 factors.

## HJM framework (Heath-Jarrow-Morton, 1992) — Ch 32

Don't model the short rate — model the entire **forward rate curve** `f(t, T)` directly. The drift under Q is determined by the volatility structure (the **HJM drift condition**):
```
df(t, T) = α(t, T) dt + σ(t, T) dW(t)
α(t, T) = σ(t, T) · ∫_t^T σ(t, s) ds
```

HJM is a **framework**, not a model — you choose the volatility function σ(t, T). Different choices give different models. Hull-White is HJM with σ(t, T) = σ · e^(−a(T−t)).

**Drawback:** HJM modeled forward rates are not directly observable. Markets quote LIBOR / SOFR forwards over finite periods, not instantaneous forwards.

## LIBOR Market Model (LMM / BGM) — Ch 32

Model the **forward LIBOR rates** directly (the observable quantities). Each forward `F_k(t)` (forward LIBOR for accrual period [T_{k−1}, T_k]) is lognormal under its own T_k-forward measure:
```
dF_k / F_k = σ_k(t) dW_k(t)   (under Q_{T_k})
```

Under a different measure, each F_k has its own drift adjustment (depending on correlations among forwards).

**Why LMM won the market:**
- Calibrates exactly to cap prices (per-caplet vol = σ_k)
- Calibrates to swaption prices via correlation structure
- Same modeling object (forward LIBOR) as the quoted vol surface

**Calibration:** typically a piecewise-constant σ_k(t) for each forward × a correlation matrix among forwards. Reduce-rank the correlation matrix to 2–3 factors for tractability.

**Smile in LMM:** vanilla LMM is lognormal → no smile. Extensions:
- **Shifted LMM:** F shifted to handle low/negative rates
- **CEV LMM / displaced diffusion:** local-volatility extension
- **SABR-LMM:** SABR per forward → cap and swaption smiles fit jointly

## Post-crisis multi-curve framework (Ch 32.6)

Pre-crisis: a single LIBOR curve to project floats AND discount. Post-crisis:
- Multiple curves to project (3M LIBOR ≠ 6M LIBOR ≠ EONIA ≠ SOFR forwards)
- One curve to discount collateralized derivatives (OIS / SOFR)
- One curve to discount each uncollateralized counterparty's exposure (= OIS + funding spread, → see [hull_xvas.md](hull_xvas.md))

Practical implementation: build the OIS curve from OIS swaps. Build each IBOR-tenor curve as an "OIS + tenor basis spread" curve from market basis swaps. Project forwards from the relevant tenor curve; discount with OIS.

## Practical rules

1. **For quoting individual caps / swaptions, use Black-76.** It's the market convention even though not arbitrage-consistent.
2. **For pricing exotics (Bermudan swaptions, calls on swaps, callable bonds), use a calibrated model.** Hull-White is the workhorse; LMM is more accurate but heavier.
3. **One-factor models can't capture curve twist.** For products sensitive to the curve shape (CMS spread options, range accruals, callable swaps), use two-factor Hull-White or LMM.
4. **In negative / low-rate regimes, switch to shifted-lognormal or normal vol quotes.** Don't try to make F · √T work near F = 0.
5. **Convexity adjustments aren't optional.** A LIBOR-in-arrears swap or a CMS-paid-on-different-tenor needs the adjustment to avoid systematic mispricing (10s of bp on long-dated trades).
6. **Calibrate per-product, but check global consistency.** A Hull-White calibrated to caps may misprice swaptions by 5–10 vol points — fine for hedging caps, bad for trading both.
7. **Multi-curve discounting is mandatory** for collateralized trades. Single-curve pricing is a pre-2008 artifact.
8. **For Bermudan swaptions, use Longstaff-Schwartz (LSM) regression-based MC.** Built into [scripts/binomial_pricer.py](../scripts/binomial_pricer.py) is single-asset Bermudan; multi-factor LMM Bermudans need a custom LSM implementation.

Cross-link: [hull_swaps.md](hull_swaps.md) for the underlying swap mechanics, [hull_interest_rates.md](hull_interest_rates.md) for the yield curve, [risk_neutrality.md](risk_neutrality.md) for the change-of-measure mechanics, [numeraire.md](numeraire.md) for the forward-measure trick (caplets in T-forward measure, swaptions in annuity measure).
