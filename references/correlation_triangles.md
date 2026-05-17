# Correlation Triangles (Module D — lines 18699–18899)

A graphical / geometric framework for thinking about implied correlation across multi-asset universes. Most useful for FX (multi-currency worlds) but generalizes to any set of correlated assets.

## The core idea

Each asset is a **point in Euclidean space**. The **distance between two points = the implied volatility of the cross-pair**. Correlation = cosine of the angle between the volatility segments emanating from a common numeraire.

```
v(x, y) = distance between point x and point y
       = implied volatility of trading pair x-y
```

This satisfies the metric properties:
1. `v(x, x) = 0` — vol of asset against itself is zero
2. `v(x, y) = v(y, x)` — symmetric (vol doesn't care which side you quote)
3. `v(x, y) ≤ v(x, z) + v(z, y)` — **triangle inequality**

## Setting up a three-currency world (line 18758)

Take USD as numeraire at origin (0, 0). One-month implied vols:
- DEM at (7, 12.12) → v(USD/DEM) = √(7² + 12.12²) ≈ 14% ✓
- JPY at (11, 4.79) → v(USD/JPY) = √(11² + 4.79²) ≈ 12% ✓

Then **DEM-JPY cross volatility is determined automatically**:
```
v(DEM/JPY) = √((7-11)² + (12.12-4.79)²) = √(16 + 53.7) ≈ 8.35%
```

The cross vol is **not free to set**. Once you fix USD/DEM, USD/JPY, and the correlation, the DEM/JPY vol is determined. Three quotes ⇒ one constraint.

## Correlation as cosine of angle (line 18793)

Given two segments x-n and y-n (both ending at numeraire n), the implied correlation between them equals the cosine of the angle between them.

If the angle is:
- **0°** → cos = 1.0 → perfect positive correlation
- **90°** → cos = 0.0 → uncorrelated
- **180°** → cos = -1.0 → perfect negative correlation

## The correlation triangle rule (line 18813)

> *"Correlation (x-n, y-n) = correlation (n-x, n-y)."*

The correlation between asset x measured against numeraire n and asset y measured against numeraire n equals the correlation between asset n measured against numeraire x and asset n measured against numeraire y.

**Translation:** the implied correlation viewed from any numeraire is the same. Choose your numeraire for convenience; the answer is unique.

## Implied correlation matrix from option prices (line 18814)

Given 3 currencies (A, B, C), you can quote 3 pairs (A-B, A-C, B-C) and get 3 implied vols. From these:

```
v(B-C)² = v(A-B)² + v(A-C)² - 2 × v(A-B) × v(A-C) × ρ(A-B, A-C)
```

Solve for ρ:
```
ρ(A-B, A-C) = (v(A-B)² + v(A-C)² - v(B-C)²) / (2 × v(A-B) × v(A-C))
```

This is the **implied correlation** between the two pairs — what the market is pricing.

## What changes correlation, what changes volatility (line 18825)

> *"For correlation to remain constant, the volatilities of the sides should increase by the same percentage amount."*

- **Scale ALL three pairs' vols by same factor** → correlation unchanged, all vols up
- **Rotate one pair (change its angle relative to others)** → vols unchanged, correlation shifts
- **Move one pair closer to another in one direction** → that pair's vol changes; correlation reflects the angle change

This decomposition helps make sense of market moves: a vol-shock is mostly the first (scaling), an FX regime shift is mostly the second (rotation).

## Adding dimensions: more assets (line 18837)

Add GBP: need a 3D coordinate system. With (x, y, z) coordinates:
- USD at (0, 0, 0)
- DEM at (7, 12.12, 0)
- JPY at (11, 4.79, 0)
- GBP at (?, ?, z_GBP > 0) — needs a 3rd dimension to satisfy all distance constraints

For N assets, you need N-1 dimensions (in general). Reality only gives us 3 dimensions for visualization, so for >4 assets you visualize subuniverses.

## SP500 vs USD — orthogonal vols (line 18862)

In the SP500-DEM-JPY-USD universe, the implied correlation between SP500-USD and (any FX pair against USD) is approximately zero — so the SP500-USD segment is **orthogonal** to the FX segments.

This is empirically true most of the time. It breaks down in crises (FX flight to USD, equity sell-off, correlation → 1).

## Arbitrage-free implied correlations (line 18871)

The triangle structure imposes constraints:
- Sum of squared vols must satisfy the triangle inequality
- The implied covariance matrix must be **positive semi-definite** (eigenvalues ≥ 0)

Any shift in the implied vols that violates these is an arbitrage. In practice:
- Quote USD/DEM and DEM/FRF and USD/FRF
- Compute the implied ρ(USD/DEM, USD/FRF)
- If |ρ| > 1, the quotes are inconsistent — arb exists in principle (in practice, transaction costs kill most such arbs)

From line ~19438 (Module F): for vol(USD/DEM) = 14%, vol(DEM/FRF) = 4%, the implied vol(USD/FRF) must be between 10% and 18% for the correlation to be in [-1, 1]. Outside that range, the volatility triangle is degenerate.

## Practical applications

### 1. Sanity-checking multi-asset quotes
For any cross-pair you're quoted, decompose into its triangle. The third leg should imply a sensible correlation.

### 2. Hedging cross-pair exposure with major pairs
If DEM/FRF is illiquid but USD/DEM and USD/FRF are liquid, hedge DEM/FRF synthetically. The triangle geometry tells you the right ratio.

### 3. Vol surface consistency in baskets
For a basket option, the basket vol depends on component vols AND correlations. Use triangle relations to verify the implied correlation surface is internally consistent.

### 4. Detecting regime shifts
When the triangle geometry "rotates" significantly, the correlation is shifting even though level vol may be unchanged. Useful early warning for relative-value books.

## Practical rules

1. **For any FX cross, decompose into the legs against your numeraire.** The cross is constrained.
2. **The implied correlation matrix from vol triangles must be positive semi-definite.** Check eigenvalues.
3. **Three vol quotes = one constraint.** Quoted markets in liquid majors do enforce this most of the time.
4. **Correlations imply volatilities and vice versa.** You don't get to set them independently.
5. **For >4-asset universes, work in subuniverses or use the implied covariance matrix directly.** Visualization breaks down.
6. **Regime shifts often show up as rotations in the triangle.** Track angles, not just lengths.
