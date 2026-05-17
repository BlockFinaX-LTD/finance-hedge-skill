# Swaps (Hull Ch 7)

Plain-vanilla interest rate swaps (IRS) and currency swaps. Read alongside [hull_xvas.md](hull_xvas.md) (modern valuation under OIS) and [hull_interest_rates.md](hull_interest_rates.md) (forward rate construction).

## The plain-vanilla IRS

Two counterparties agree to exchange cash flows for a notional principal `L` over `N` payment dates:
- **Fixed leg:** pays `K · L · τ_i` where K is the swap rate, τ_i is the day-count fraction
- **Float leg:** pays `R_i · L · τ_i` where R_i is the floating rate (historically LIBOR) observed at the start of period i, paid at the end

Notional is **not exchanged** in a single-currency IRS. Net payments only.

The fixed rate K that makes the swap have zero value at initiation is **the swap rate**.

## Two valuation lenses (Hull Ch 7.6–7.7)

A swap is worth the same whether decomposed as bonds or as FRAs — choose the lens that fits your data.

### As a portfolio of bonds
- Receive-fixed swap = **long fixed-rate bond, short floating-rate bond**
- Value = `B_fix − B_fl`
- `B_fl` is `L` at the next reset (a floater always resets to par at each reset), discounted: `B_fl = (L + next_coupon) · DF(t_next)`
- `B_fix = Σ K·L·τ_i · DF(t_i) + L · DF(t_N)`

### As a portfolio of FRAs
- Each floating payment is a forward rate fixed today; replace each `R_i` with its forward `F_i`
- Value = `Σ L · τ_i · (F_i − K) · DF(t_i)`
- This is the modern post-crisis way: discount each cash flow with OIS curve; project floats with LIBOR-curve forwards (see [hull_xvas.md](hull_xvas.md))

## The comparative advantage argument (Hull §7.4) — and Taleb's objection

Hull's textbook motivation: company A borrows fixed cheaply, company B borrows floating cheaply, they swap, both end up better off than going direct in their preferred market.

**But:** the spread arises because lenders price A's *floating* exposure differently — the spread compensates for credit risk that doesn't disappear by swapping. It's not free money. Treat the comparative advantage story as pedagogically useful, **not** as a real-world driver. Real drivers: hedging existing balance-sheet exposures, structural rate views, regulatory capital, asset-liability matching.

## Currency swaps

Exchange of principal (at start AND end) and periodic interest in two currencies. Both legs can be fixed, both floating, or one of each.

- **Notional IS exchanged** in currency swaps (unlike IRS)
- Valuation as two bonds, one in each currency, with FX conversion at spot
- Or as a portfolio of forward FX contracts

Currency swap valuation formula:
```
V_swap = B_d − S_0 · B_f
```
where `B_d` = domestic-currency-bond value of the leg the firm receives, `B_f` = foreign-currency-bond value of the leg it pays, `S_0` = spot FX.

## OIS discounting (post-2008 standard)

Pre-crisis: discount with LIBOR (and project floats with LIBOR). This implicitly assumed LIBOR ≈ risk-free.

Post-crisis: LIBOR contains bank credit risk. **Collateralized** derivatives are discounted at the rate paid on collateral (typically overnight, ≈ OIS / SOFR / EFFR). Forward LIBORs are still projected from the LIBOR curve.

This is the "dual-curve" or "multi-curve" framework:
- One curve to project forwards (LIBOR / IBOR / forward-looking term rate)
- Another curve to discount (OIS / SOFR)

LIBOR transition (now post-2023): the IBOR family has been largely replaced by overnight RFRs (SOFR in USD, SONIA in GBP, ESTR in EUR, TONA in JPY). Forward-looking term SOFR exists but is restricted. "Compounded-in-arrears" floating legs are standard in the cleared market.

## Credit risk in swaps

Single-currency IRS has lower credit risk than its notional suggests because:
- Principal isn't exchanged
- The mark-to-market value is bounded by the discounted spread on the fixed-vs-realized-floating

Currency swaps have **higher** credit risk than IRS because principal IS exchanged.

Counterparty risk = CVA (see [hull_xvas.md](hull_xvas.md)).

## Variations (Ch 33)

- **Compounding swap** — floating payments accrue and compound until paid (no intra-period payments)
- **Currency swap** — different currency on each leg
- **LIBOR-in-arrears swap** — floating rate fixed and paid at end of period (requires convexity adjustment)
- **CMS / CMT swap** — floating leg is the swap rate / Treasury rate (also needs convexity adjustment)
- **Differential swap (diff swap)** — receive floating in one currency on a notional in another currency (quanto adjustment)
- **Accrual swap** — interest accrues only on days the floating index is in a specified range
- **Cancelable swap** — one party can terminate (= IRS + receiver/payer swaption)
- **Equity swap** — one leg pays equity return (price change + dividends)
- **Variance swap** — payoff = (realized variance − strike²) × notional

## Practical rules

1. **Swap rate at inception ≈ par swap rate** = the K that makes B_fix = B_fl.
2. **For valuation, decompose as FRAs and discount each leg's cash flows separately** — projection curve ≠ discount curve.
3. **Currency swaps carry more credit risk than IRS** because notional is exchanged. CVA is materially larger.
4. **Convexity / timing / quanto adjustments are needed** whenever the floating rate is paid in a non-standard way (in arrears, in a different currency, or referencing a CMS rate). See [hull_ir_derivatives.md](hull_ir_derivatives.md) Ch 30.
5. **Comparative advantage is a story, not a strategy.** Real swap demand comes from hedging, capital, and structural views.
6. **OIS / SOFR discounting is the post-crisis standard** for collateralized swaps. For uncollateralized counterparties, add CVA/FVA — see [hull_xvas.md](hull_xvas.md).
