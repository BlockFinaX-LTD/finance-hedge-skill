# Some Wrinkles of Option Markets (Ch 13 — lines 10347–10708)

> *"Sell [volatility] on Thursday and buy on Friday."* — old option proverb on vol-selling before weekends

Read this when something looks "off" near option expiry, when behavior near strikes feels artificial, or when a textbook arbitrage trade refuses to lock in.

## Expiration pin risk (line 10357)

> *"The expiration pin risk is the expiration variance for an options position. It results from the absence of timely information about the outcome of the option assignment lottery."*

The mechanic:
- Option market closes
- Notification of assignment comes later (often 24+ hours)
- Underlying may keep trading or news may hit in between
- Trader has to decide whether to exercise BEFORE knowing what counterparty will do

> **Risk Management Rule (line 10374):** *Put/call parity does NOT hold for non-cash-settled listed options (both European and American).*

This is one of the few places put-call parity breaks down, and it surprises everyone who learned it as a theorem.

### Worked example (line 10384)
- Market closes at 100 exactly
- Trader is short the 100 calls, long the 100 puts, long the underlying future
- "Perfect" textbook conversion — zero P/L at expiry
- BUT: trader doesn't know whether his short calls will be assigned
  - Exercise puts → hope all calls get abandoned (uncertain)
  - Abandon puts → hope all calls get exercised (uncertain)
- Counterparty in the same bind

Worse (line 10404): the future closes at 101 but news of a scandal hits after close. The 100 puts officially expire OTM — but if the market would open lower, the trader should have exercised them. Many of these decisions are coin flips between "lose a fortune" and "make a fortune."

**Solution that works:** cash-settled futures expiring simultaneously with the option (Eurodollars, Euromarks, SP500 quarterly). Conversion/reversal is then a true arbitrage.

**Naming warning (line 10429):** "pin risk" is *also* used for the P/L swing at a barrier for barrier-option books. Two completely different concepts, same name. Always disambiguate.

## Sticky strikes (line 10437)

> *"Sticky strikes are over-the-counter or listed strikes in which the buildup of a large open interest alters the behavior of the market around the strike price near expiration."*

### The mechanism (line 10444)
- Large open interest concentrated in **one or few non-delta-hedging parties** (covered writers, retail, institutional sellers)
- The counterparties to that flow (dealers) ARE delta hedging — they're long gamma
- As expiry nears and spot approaches the strike, dealers buy below the strike, sell above → **stability around the strike**

The spot gets "stuck" near the strike because all the gamma-long delta-hedging dealers are pushing it back. The non-hedging customer doesn't push back — they're indifferent until expiry.

> **Risk Management Rule (line 10493):** *When dynamic hedgers are long a strike (and consequently, static hedgers short it) the strike will be sticky. It will whip otherwise.*

### Translation
- **Dealers long gamma at strike X, customer short** → spot sticks to X (calm before expiry)
- **Dealers short gamma at strike X, customer long** → spot whips violently near X (dealers chase deltas the wrong way)

This is **the** source of the famous "currency overnight cheap → market stabilizes to strike; expensive → whips" phenomenon (line 10485).

### Tail wagging dog (line 10480)
*"It is often the case of the tail wagging the dog."* Spot is being driven by option positioning, not the other way around. Cash traders complain. Very little academic research has been done on this. Practical implication: option open interest IS spot-relevant information.

## Market barriers (line 10501)

> *"A market barrier is a level that is supposed to cause some stickiness because of institutional constraints."*

**Not the same as barrier options.** Market barriers are external constraints. Examples (line 10510):
- Currency bands (central bank intervention zone) — HKD-USD, AED-USD, formerly ERM currencies
- Floor prices on agricultural commodities (government-guaranteed)
- Exchange-imposed price limits (circuit breakers, limit-up/down)

### Are they barriers in the optionality sense?
- Vol *should* dampen near a credible market barrier (mean reversion)
- But: **credibility is the key word**. Market barriers don't always hold
- Pricing options near a market barrier requires explicit modeling of the barrier-break probability

This is the same logic as the peg-break decomposition in [emerging_markets.md](emerging_markets.md) — a market barrier is a soft peg.

## Pre-weekend / pre-holiday vol selling

The chapter epigraph captures a folk rule: sell vol on Thursday (high time value before weekend), buy back Friday afternoon (after weekend decay). Mechanism:
- Options price calendar days but trade trading days
- A Friday-expiry option carries the weekend in its theta — a Friday quote reflects 3 days of decay over 1 trading day
- Symmetric vol-sellers can scoop a known premium per weekend

Caveat: weekends *can* have news. The pre-weekend trade is **selling a small positive expected value with a large negative tail** — classic short-vol trade. Backtests look great until they don't.

## Triple witching hour (mentioned, Ch 4 line ~75)

When stock options, index options, and futures all expire simultaneously (third Friday of March/June/Sept/Dec). Concentrated unwinding creates liquidity holes (see [liquidity.md](liquidity.md)). Standard during the last hour of trading; sometimes spills over to the next session.

## Other wrinkles in this chapter

The chapter covers several other minor topics worth knowing exist:
- **Strike price clusters** — option market makers price strikes more tightly when several are clustered (interpolation)
- **Cabinet trades** — listed options pricing convention for near-zero options
- **Block trades** — large negotiated trades printed at end of session at one price
- **Settlement mechanics** — different exchanges, different rules; matters for quant-driven strategies

Read source lines 10500–10708 for the full set.

## Practical rules

1. **Put-call parity is a theorem ONLY for cash-settled European options expiring simultaneously with their reference.** Everywhere else, parity is approximate.
2. **Don't enter physical-settle conversions/reversals near ATM at expiry.** Pin risk is real and can swing P/L dramatically.
3. **Read open interest as positioning information.** Concentrated strikes with non-hedger flow → sticky behavior near expiry.
4. **Strikes are sticky when dealers are long gamma; they whip when dealers are short gamma.** Reverse-engineer the dealer position from customer flow.
5. **Market barriers ≠ barrier options.** Both create discontinuities, but their breakability is a separate dimension.
6. **The pre-weekend vol decay trade is a short-vol exposure.** Profitable in expectation, sized by your tail tolerance.
