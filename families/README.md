# Twist families: infinitely many counterexamples, with exact limits

## The idea
- **The family:** take a short alternating 4-braid word W (the *skeleton*) and close up (W σ₂⁻ᵈ)³ for a twist d = 1, 2, 3, …
- **One formula for every member:** σ₂ acts in the reduced Burau representation as the identity plus a rank-one piece, so σ₂⁻ᵈ = I + (x − 1)Π with x = (−t)⁻ᵈ. The Alexander polynomial of every member is therefore given by one exact formula:

      (1 + t + t² + t³) Δ_{K_d}(t)  =  c₀(t) + c₁(t)·x + c₂(t)·x² + c₃(t)·x³,     x = (−t)⁻ᵈ

  The cⱼ are fixed integer polynomials.
- **The parent polynomial:** outside the unit circle x shrinks to 0 as d grows, so the roots of the knots converge to the roots of c₀.
- **The certificate:** if c₀ has a root z* with Re z* < −1, Rouché's theorem on a small circle around z* gives a twist d₀. From d₀ on, every member of the family has a root in that circle, so every one breaks Hoste's conjecture.

## Example: the family of K33 and K39
For W = σ₁³ σ₂⁻³ σ₃³:
- **Parent polynomial** (the rest of c₀ is (t² + 1)(t² − t + 1)², which has roots only on the unit circle):

      t¹⁶ − 2t¹⁵ + 8t¹⁴ − 22t¹³ + 46t¹² − 101t¹¹ + 189t¹⁰ − 303t⁹ + 441t⁸ − 539t⁷ + 547t⁶ − 478t⁵ + 329t⁴ − 170t³ + 70t² − 18t + 3

- **Its root:** z* = −1.1501872074 ± 1.6348058308 i.
- **The certificate:** Rouché gives d₀ = 5, so every K_d with d ≥ 5 has a root within 0.08 of z*, with real part below −1.07.
- **The small cases:** d = 2 (K33, 33 crossings) and d = 4 (K39) are checked directly.
- **The result:** for every even d the closure is an alternating knot that breaks Hoste's conjecture. The roots converge to z* exponentially, getting about 4× closer for every 2 extra twists:

| d | crossings | root nearest z* | distance to z* |
|---|---|---|---|
| 2 | 33 | −1.074749 − 1.791570 i | 1.7e−1 |
| 4 | 39 | −1.191848 − 1.652333 i | 4.5e−2 |
| 6 | 45 | −1.150483 − 1.621860 i | 1.3e−2 |
| 8 | 51 | −1.147257 − 1.635921 i | 3.1e−3 |
| 10 | 57 | −1.150685 − 1.635404 i | 7.8e−4 |
| 14 | 69 | −1.150139 − 1.634797 i | 4.9e−5 |

## All families with skeletons up to 10 letters
- **The search:** all 36,316 skeletons of at most 10 letters were checked exactly; they are listed in `families_L10.json`.
- **The count:** 102 give families whose parent polynomial has a root past −1. Each comes with its limit root and its Rouché threshold d₀, which is 4 or 5.
- **Simplest:** σ₁³σ₂⁻²σ₃³ (8 letters), limit −1.0408.
- **Deepest:** σ₁³σ₂⁻⁴σ₃³ (the family of K39), limit −1.1736.
- **With 12-letter skeletons:** σ₁⁴σ₂⁻⁴σ₃⁴ reaches −1.238088. A local search over single-letter changes, from 10 different starting skeletons, always ends there.

## All families with skeletons up to 13 letters
All 1,038,334 skeletons of at most 13 letters were checked exactly; the 2,478 that break are listed in `families_L13.json`.
- **Distinct families:** 629, after merging the symmetric twins given by flipping σ₁ ↔ σ₃ and by reversing the word.
- **Growth:** the count rises about 2.7× per extra letter:

| skeleton letters | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|
| breaking families | 6 | 26 | 70 | 222 | 596 | 1,558 |

- **The best family:** σ₁⁴σ₂⁻⁴σ₃⁴, limit −1.238088. It is the best of all families up to 13 letters, confirmed by the exhaustive search.
- **Rouché thresholds:** d₀ ranges from 2 to 17, most often 5.

## More repeats: a ceiling
Repeating the block k times instead of 3 gives deeper limits that level off. For the skeleton σ₁⁴σ₂⁻⁶σ₃⁴:

| repeats k | 3 | 5 | 7 | ∞ |
|---|---|---|---|---|
| limit | −1.219 | −1.378 | −1.382 | −1.3844 |

- **Why it levels off:** as k → ∞ the parent's roots fill the curve {|μ(t)| = 1} of the 3×3 matrix N = ψ(W)(I − Π), so the k = ∞ limit takes milliseconds to compute.
- **Fatter twist groups don't go deeper:** σ₁ⁿσ₂⁻ⁿσ₃ⁿ peaks at n = 5 to 6, around −1.37.
- **A false lead, checked:** curve points that seemed to reach −3 for n ≥ 15 were rounding errors. Eigenvalues at 120 digits show no curve left of −1.5.
- **So:** the evidence puts the deepest roots of alternating 4-braid knots near −1.38 to −1.40. The deepest block curve found by search reaches −1.3963.

## The smallest members
Families without repeats (k = 1) contain the smallest counterexamples. K31 is a member of the family of its own 28-letter skeleton, with limit −1.00439 and d₀ = 7.
- **Searched:** 14.5 million random no-repeat skeletons of 14 to 30 letters, each family checked exactly, and its small members checked on their own Alexander polynomials.
- **Below 31:** no member with fewer than 31 crossings was found anywhere.
- **New 31-crossing counterexamples:** several turned up. The deepest, with root −1.01714, is σ₁³σ₂⁻²σ₃²σ₂⁻²σ₁²σ₂⁻³σ₃³σ₂⁻³σ₁³σ₂⁻²σ₃³σ₂⁻³.
- **Caveat:** this is evidence, not proof, that 31 is the minimum for these knots.

## Why it is fast (methods)
- **Rank-one twist:** a generator with eigenvalues {1, 1, −t} has powers I + (x − 1)Π. So an infinite twist family is one polynomial in x = (−t)⁻ᵈ with fixed coefficients.
- **Exact arithmetic:** matrices of integer polynomials, with adj(S₂) = (−t)S₂⁻¹ for the inverse letters and the denominators cleared, so nothing is rounded. One infinite family takes about 0.04 s, and a million families take 39 minutes on 15 cores.
- **Certificates:** Hurwitz gives the limit; Rouché on a small circle gives an explicit threshold d₀.
- **Limits in k:** as the number of repeats k grows, the roots fill the curve where an eigenvalue has size 1. That is one 3×3 matrix and no polynomial at all.
- **Pitfalls hit and fixed:**
  - Reconstructing the polynomial from samples (FFT) produced fake deep roots.
  - Ordinary root finders split repeated roots on the unit circle into rings of fake roots. Factor the polynomial first, or Newton-check every root.
  - Double-precision eigenvalues fail once matrix entries reach about 10²¹.
  - Cross-checking the exact engine against a numeric determinant caught a sign error.

## Run it
`python twist_family.py` checks the K33 / K39 family. `python twist_family.py 1 1 1 1 -2 -2 -2 -2 3 3 3 3` checks any skeleton, written with 1 = σ₁, −2 = σ₂⁻¹ and 3 = σ₃. It needs numpy and mpmath and runs in seconds.

The script:
- computes c₀…c₃ exactly;
- roots the parent polynomial;
- finds d₀;
- checks the convergence on the knots' own Alexander polynomials.

## Notes
- **What is not new:** the principle that roots of a family converge to the roots of a limiting function is Ishikawa's (JKTR 2018, Thm 5.4, for Montesinos knots), and in general it goes back to Beraha, Kahane and Weiss.
- **What is new here:** exact parent polynomials for braid skeletons, certified thresholds, and an exhaustive list for small skeletons.
- **Rigour:** the Rouché inequality is checked on 4,000 points of the circle with a 1.5× margin. That is a computer check, not interval arithmetic.
