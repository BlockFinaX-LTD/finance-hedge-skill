# Derivatives Mishaps and What We Can Learn From Them (Hull Ch 37)

A catalog of derivatives disasters and the systemic lessons. Hull's framing complements Taleb's anecdotes (the "Half Billion-Dollar Delta" story in Ch 7 / lines 6223–6253, and various market-making war stories).

## The major losses

### Barings Bank (1995) — $1.4 bn

Nick Leeson, a 28-year-old trader in Singapore, ran both the trading desk AND the back office for Nikkei 225 futures. He took large long positions, hid losses in error account "88888," then doubled down. The Kobe earthquake (Jan 17, 1995) crashed the Nikkei. Leeson's hidden losses ballooned. Barings — a 233-year-old British merchant bank — collapsed.

**Lesson:** segregate trading and back office. Always. No exceptions.

### Allied Irish Banks (2002) — $700 m

Currency trader John Rusnak hid losses by fabricating fictitious offsetting trades, exploiting weak controls at Allfirst (AIB's US subsidiary).

**Lesson:** independent confirmation of all trades with the counterparty. Don't trust trader-reported P&L.

### Long-Term Capital Management (LTCM) (1998) — $4 bn

Famous hedge fund staffed by Nobel laureates and ex-Salomon bond arbs. Massively leveraged convergence trades (on-the-run vs. off-the-run Treasuries, swap spreads, EM bonds). Russia defaulted Aug 1998; correlations went to 1; liquidity vanished; LTCM's positions moved against them in lockstep. Fed-orchestrated bailout.

**Lessons:**
- Leverage + illiquid positions = lethal when correlations rise
- VaR models calibrated to recent history miss regime shifts
- Models assuming continuous markets fail when gaps appear
- Reputation and Nobel prizes don't substitute for risk limits

### Société Générale / Jérôme Kerviel (2008) — $7.2 bn

Junior trader took enormous unauthorized directional positions on European equity index futures, hidden via fictitious offsetting forwards. The fraud was discovered during a market downturn; unwinding the positions in panic mode crystallized the loss.

**Lesson:** Real-time gross position monitoring, not just net.

### JP Morgan "London Whale" (2012) — $6.2 bn

Chief Investment Office trader Bruno Iksil took large positions in CDX.IG and CDX.IG.9 tranches as a "hedge." Position size moved the market. When prices moved against the position, hedge fund competitors identified and front-ran the unwind.

**Lessons:**
- A "hedge" big enough to move the market isn't a hedge
- Concentration in illiquid markets — even highly liquid sounding ones like CDX — creates a death spiral on unwind
- "Tail-risk hedging" by buying obscure tranches needs scrutiny when the size exceeds market depth

### AIG (2008) — $99 bn injection, government rescue

AIG Financial Products wrote credit default swaps on hundreds of billions of "super-senior" ABS CDOs. Collateral was not posted at trade inception (AIG was AAA-rated, so the ISDA CSA didn't require it). As the CDOs deteriorated, AIG was contractually required to post collateral — but couldn't raise the cash without selling its insurance subsidiary's assets.

**Lessons:**
- AAA isn't a substitute for collateral
- One-way collateral terms become catastrophic when credit deteriorates
- Selling deep-OTM protection on senior tranches is like writing flood insurance from a basement office — pleasant premium until the flood

### Metallgesellschaft (1993) — $1.3 bn

German conglomerate's US subsidiary sold long-dated forward oil delivery contracts (10-year) and hedged with short-dated NYMEX futures. As oil prices fell, the short-dated futures showed mark-to-market losses requiring cash margin, while the long-dated forwards (gains, but not yet realized) had no offsetting cash inflow. Liquidity crisis.

**Lessons:**
- Stack-and-roll hedges have funding risk that match-funded hedges don't
- Cash flow ≠ economic P&L
- Long-dated commitments hedged with short-dated instruments have rollover and basis risk
- See [fungibility.md](fungibility.md) for the Taleb angle on Metallgesellschaft

### Orange County (1994) — $1.6 bn

County treasurer Bob Citron invested in structured notes (inverse floaters, leveraged FRNs) using repo financing. Rising rates in 1994 produced both interest-payment losses on the leveraged longs AND mark-to-market losses on the repo collateral. Forced liquidation crystallized the loss.

**Lesson:** Don't run government cash-management like a hedge fund. Especially with leverage. Especially when the principal can't articulate the position's risk.

### Procter & Gamble / Gibson Greetings (1994) — $157 m / $20 m

Bankers Trust sold complex structured swaps with embedded leverage that corporates didn't understand. P&G's loss came from a swap whose payments depended on the spread between the 30-year Treasury yield and the 5-year yield, leveraged. As the spread moved unfavorably, the loss multiplied.

**Lessons:**
- Don't enter a derivative you can't decompose into vanilla components
- Be skeptical of structures designed by counterparties whose incentive is to take the other side
- Fiduciary duty applies even when the law doesn't say it does

### Amaranth Advisors (2006) — $6.5 bn

Hedge fund energy trader Brian Hunter built enormous long positions in natural gas spread contracts (March/April calendar spread). Forced unwind in late summer when prices moved against him.

**Lesson:** Position size relative to market depth. Same lesson as London Whale, just before it.

### Knight Capital (2012) — $440 m in 45 minutes

Algorithmic trading firm deployed new code with a bug. The bug caused unintended order routing. Within 45 minutes, Knight had accumulated unwanted positions worth $7 bn and absorbed the spread cost to unwind.

**Lessons:**
- Deployment discipline and kill switches matter more than model sophistication
- Speed of execution = speed of disaster
- A bug in production for 30 minutes can bankrupt a firm

## Cross-cutting lessons (Hull §37.5)

### For traders

1. **Risk limits are the limit. Period.** Don't double down to recover losses.
2. **If you don't understand a position, you don't own it.** You're holding it for the model — and models break.
3. **Be careful about claiming to have spotted opportunities the market missed.** When the market disagrees with you on a major theme, you are usually wrong (LTCM, AIG).

### For risk managers

4. **VaR is a useful summary number, not the whole risk picture.** Tail scenarios matter more than 99% VaR. See [var.md](var.md).
5. **Liquidity risk is separate from market risk.** A position that "VaR shows me 95% safe" can blow up in unwind cost.
6. **Stress-test correlation going to 1.** That's what crises do.
7. **Real-time monitoring of gross positions.** Net is insufficient when fraud or unauthorized trades are possible.

### For senior management

8. **Don't run a financial institution on bonuses tied to one-year accounting profit.** This rewards taking unrecognized tail risk.
9. **Segregate trading, back office, and risk.** No exceptions, no matter how senior the trader.
10. **The CEO should be able to explain every major position.** If you can't, you shouldn't have it.
11. **Know your trader before sending him to Singapore alone.** (Barings)

### For regulators

12. **Capital requirements based on Q-measure models** (VaR, CVaR) miss tail risk. Stress capital separately.
13. **Skin in the game** for originators (Dodd-Frank securitization retention) reduces moral hazard.
14. **Central clearing of standard derivatives** reduces but doesn't eliminate counterparty risk — it concentrates it in CCPs that become systemically important.

### For investors / pension funds / corporates

15. **Pay for transparency.** A complex product is usually opaque to extract margin for the structurer.
16. **Don't use derivatives you can't decompose.** P&G could have hedged with a vanilla swap; they bought a leveraged spread bet.
17. **Match the hedge to the exposure.** Match-funding > stack-and-roll for long-dated commitments.

## Hull's headline summary

> "Do not assume that you can outguess the market. If a deal seems too good to be true, it probably is. Risk limits are an essential part of risk management. Be on the lookout for fraud."

Cross-link: [hull_securitization.md](hull_securitization.md) (AIG and the credit crisis), [hull_credit_derivatives.md](hull_credit_derivatives.md) (Gaussian copula misuse), [hull_xvas.md](hull_xvas.md) (post-crisis valuation reset), [fungibility.md](fungibility.md) (Metallgesellschaft / stack-and-roll), [var.md](var.md) (why VaR isn't enough), [liquidity.md](liquidity.md) (Taleb on the asymmetry that killed LTCM and Amaranth).
