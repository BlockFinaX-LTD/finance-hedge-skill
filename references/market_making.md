# Market Making (Ch 3 — lines 3322–4247)

Read this when: thinking about bid-offer, why prices behave the way they do around your order, why your fills are systematically worse than mid, or how to set markets in your own product.

## Three-tier classification (pit jargon)

- **Local** — floor market maker. Pure price-sensitive, entirely liquidity-driven. Has the time/space advantage.
- **Paper** — end customers. Locals eagerly trade with paper (they "feel the edge"). A local trying to trade with another local has to disguise his order *to make it look like paper*.
- **Arb** — arbitrageur or maker-hybrid. Transfers liquidity between markets (for a small fee).

The implication for pricing: when you quote a customer, you are deciding which side of the local/paper dynamic to be on. Charging too tight a spread to paper is throwing away edge; quoting too wide to another maker exposes you to adverse selection.

## Book runner vs. price taker

- **Book runner** = market maker. Posts bid + offer; tries to earn a large part of the spread vs. mid; aims for *transaction positivity*.
- **Price taker** = market user. Incurs transaction costs proportional to liquidity.
- **Crucially:** "A market maker's willingness to take on a position will increase as the price becomes more attractive; not so for the market user (except in liquidity holes)" — line 3380.

### Leaning

Effective market makers **lean on a position**: keep a core long or short bias and skew their prices around it. Typically *defensive*:
- Bull trend → makers fear getting short → shade bids AND offers upward
- Bear trend → opposite

This is why your fills shift against you even when the market hasn't "moved" — the maker rebalanced.

## Commoditized vs. nonstandard products (lines 3418–3473)

| | Commoditized | Nonstandard |
|---|---|---|
| Volume | High | Low |
| Spread | Narrow | Wide |
| Tools | Standard software | Custom code per trade |
| Edge | Small per trade, made on volume | Large per trade |
| Examples | Vanilla FX/equity options, single-barrier knock-outs | Multi-asset structures, reset barriers, extendable expirations |

Taleb's observation (line 3465): *"All successful nonstandard products become commoditized."* Five years separates "junior trader can price it" from "PhD required."

**Pricing implication:** for commoditized products, market price IS truth — your model should reproduce it or you're wrong. For nonstandard products, your model IS the price — and counterparty knows you wrote it, so they shop the trade.

## Adverse selection and the risk management of market makers (Ch 3 + Ch 15)

Counterparties show up to trade when *they* have a reason. As a result:
- Buy orders cluster before rallies, sell orders before drops
- Tail buyers appear before tail events
- Your filled trades are conditioned on counterparty information you don't have

This is why naive "average implied vol" backtests look profitable to *sell* but actually lose money — the trades you fill aren't a random sample of the population.

## "Monkeys on a typewriter" (lines ~3580–3650) and the arcsine law

Taleb's recurring caveat: a profitable track record is partially a *survivorship artifact*. Given enough traders flipping coins, some will have N-year winning streaks. Statistical inference from track records needs:
- Sharpe ratios with N high enough to be significant (rule of thumb: needs years of data, not months)
- Adjustment for the size of the trader population (Bonferroni-style)
- The **arcsine law** on P/L: cumulative P/L spends most of its time near its extremes, not near zero. A trader can be "up" for long stretches by random chance.

Implication: trust process more than P/L, especially over short horizons.

## Practical rules

1. **Set your spread to your worst-case adverse-selection scenario**, not your average customer.
2. **Skew your quotes** in the direction of your accumulated inventory (defensive).
3. **For nonstandard products**, charge for the modeling effort AND the model risk.
4. **Watch the arcsine effect** when judging your own (or anyone's) track record.
5. **"A fast nickel is better than a slow dollar"** (line 3427) — in commoditized markets, edge × volume beats edge alone.
