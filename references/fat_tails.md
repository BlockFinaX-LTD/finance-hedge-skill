# Fat Tails and Stochastic Volatility (Ch 15 Distilled)

**Read the source:** `dynamic_hedging.md` lines 11097–11786. This is the most important chapter in the book for option pricing accuracy and the one most easily mishandled by paraphrase.

## The core insight

Black-Scholes assumes constant volatility. Real markets have **stochastic volatility** ("vvol" = volatility of volatility, related to the 4th moment / kurtosis). This single fact explains:

- Why OTM options trade richer than flat-vol BS predicts (the "wings" / tails)
- Why ATM options are largely unaffected (their gamma w.r.t. vol — i.e., volga — is near zero)
- Why the smile exists at all

From Taleb (line 11141): *"The prime reason for the higher price of in-the-money and out-of-the-money options than the Black-Scholes value is the phenomenon traders call the 'volatility of volatility,' or vvol. It is related to the fourth moment, or kurtosis."*

## The smile, mechanically

- **Symmetric smile** = stochastic vol with no spot-vol correlation
- **Left skew** (puts richer than calls) = negative correlation between spot returns and vol changes. Typical for equity indices (S&P, FTSE) — vol spikes on drawdowns.
- **Right skew** = positive spot-vol correlation. Typical for some commodities (oil supply shocks: price up + vol up) and crypto in bull phases.

Taleb's warning (line 11211): correlation between asset returns and vol is **non-linear**. *"Typically, the correlation holds from small moves but may reverse for a large one. A clear example is the SP500 futures: Volatility drops after a small rally but increases after a large one."*

## Why variable vol → fat tails (line 11230)

> Conditional on being in the tails, the most likely state is one of high volatility. High volatility can more easily take the market to the tails than a lower one. Thus the tails will have the thickness of the higher volatility.
>
> The lower volatility is more likely to keep the market in the middle, the "peak." Thus the distribution, when in the middle, is more likely to take the shape of a lower volatility.

So the empirical distribution is a **mixture**: high-vol shape in the tails, low-vol shape in the body. This is also why histograms look "peaked AND fat-tailed" simultaneously (line 11271). Both features come from the same generative process.

## Practical pricing implications

1. **Never quote OTM with flat ATM vol.** Use the smile, or if pricing in an illiquid market, add a wing premium proportional to kurtosis estimates.

2. **The Black-Scholes implied vol is just a quoting convention.** It is what makes BS reproduce the market price — not a "real" parameter. Two options on the same underlying can have different implied vols and that is correct, not arbitrageable.

3. **Vega is convex.** OTM options have positive volga (vomma) — they benefit from vol-of-vol. The convexity-aware fair value is higher than flat BS suggests.

4. **For trade ideas:** Selling tails (short OTM strangles) is short vvol. It looks like free money in calm regimes and is the canonical way books blow up.

## The "anxiety of markets" rule (line 11121)

> Option traders are likely to get the "bad" distribution through their market making. Somehow, the anxiety of markets gets reflected in their position. Economists call this phenomenon **adverse selection.**

Implication: if you're systematically short wings, your realized vol-of-vol will exceed your priced vol-of-vol because counterparties only show up to buy wings when they have a reason. Pricing models that assume symmetric information underprice this.

## Estimating vvol in practice

True vvol is not directly observable. Proxies:

- Historical std-dev of rolling 21-day realized vol
- Implied vol of vol from VIX options / VVIX (where listed)
- Range-based estimators (Parkinson, Garman-Klass) compared to close-to-close — divergence signals vvol
- Empirical kurtosis of returns vs. 3 (excess kurtosis); rough conversion to vvol via the model in Ch 15 line 11151+ (Hull-White adaptation)

## Distributions seen in real markets (Ch 15 figures 15.3–15.6)

Taleb shows histograms vs. matched-vol normal for:
- Japanese yen (1985–95)
- S&P 500 cash (1985–95)
- US 30-year yield (1985–95)
- EuroMark futures (1992–95)

All display the **high-peak + fat-tail** syndrome. This is the rule, not the exception. Any pricing model that assumes Gaussian returns is wrong on day one; the question is whether the wrongness matters for your strike.

## Quick test: is fat-tail risk material for this option?

For a given option, fat-tail mispricing matters most when:
- Strike is >1σ from spot (the further OTM, the more)
- Tenor is short (≤ 90 days) — vvol's marginal impact is concentrated
- Underlying has high empirical kurtosis (most EM FX, single names, commodities)
- Counterparty selection is non-random (institutional flow buying tails)

If all four apply, add a fat-tail premium of 10–40% over flat-vol BS for the wing. Always disclose.
