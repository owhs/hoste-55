# A 31-crossing counterexample to Hoste's conjecture

**Hoste's conjecture** (J. Hoste, 2002; stated in Lyubich–Murasugi, *Topology Appl.* 159 (2012), Conjecture 1): if K is an alternating knot, every root z of its Alexander polynomial Δ_K(t) satisfies Re(z) > −1.

**The smallest found, K31,** is the closure of the 4-strand braid

    σ₃³ σ₂⁻² σ₁³ σ₂⁻³ σ₃³ σ₂⁻³ σ₁³ σ₂⁻² σ₃² σ₂⁻² σ₁² σ₂⁻³

- **Crossings:** 31. The diagram is alternating (σ₁, σ₃ positive, σ₂ negative) and has one component.
- **Its Alexander polynomial** (degree 28, coefficients in `k31_certificate.json`) has the roots

      z = −1.01608378899900962566418729758 ± 1.83677969979327281882746228039 i

- **How it was found:** random sampling of 4-, 5- and 6-strand alternating braids built from runs of 2–4 equal crossings ("twist regions"), 17–32 crossings, 2.3 million knots. Two different 31-crossing counterexamples turned up, and none smaller. Deleting crossings from either gives no 29-crossing counterexample. Smaller ones are not ruled out.

**A symmetric one, K33,** is the closure of the 4-strand braid

    (σ₁³ σ₂⁻³ σ₃³ σ₂⁻²)³

- **Crossings:** 33.
- **Alternating:** σ₁ and σ₃ appear only positively and σ₂ only negatively.
- **Knot, not link:** the braid permutation is a 4-cycle.
- **Its Alexander polynomial** (degree 30, coefficients in `k33_certificate.json`) has the roots

      z = −1.07474917750139153258250205343 ± 1.79156965053453656761727200278 i

  These have Re(z) < −1.

**How K33 was found:** an exhaustive search of one simple family, 4-braid blocks made of at most 6 runs of a single generator (σ₁ᵃ σ₂⁻ᵇ σ₃ᶜ σ₂⁻ᵈ …), repeated, up to 39 crossings: 139,932 knots. It found 116 counterexamples, and K33 is the smallest. Smaller counterexamples outside this family are not ruled out.

### An infinite family with one shared root

**Proposition.** Let B = σ₁³ σ₂⁻³ σ₃³ σ₂⁻² and z₀ = −1.0747491775013915… + 1.7915696505345365… i, the root of K33. For every odd m, the closure of B^(3m) is an alternating knot with Δ(z₀) = 0. So there are infinitely many alternating counterexamples to Hoste's conjecture, all sharing the root z₀.

**Proof.**
1. Let ψ be the reduced Burau representation of the 4-strand braid group, and λ₁(t), λ₂(t), λ₃(t) the eigenvalues of ψ(B).
2. For any k, (1 + t + t² + t³) Δ_{B^k}(t) = det(I − ψ(B)^k) = ∏ᵢ (1 − λᵢ(t)^k).
3. K33 is the closure of B³ and Δ_{B³}(z₀) = 0. The point z₀ is not a 4th root of unity, so 1 − λᵢ(z₀)³ = 0 for some i.
4. Then λᵢ(z₀)^(3m) = 1, so det(I − ψ(B)^(3m)) vanishes at z₀, and so does Δ_{B^(3m)}.
5. B^(3m) is alternating, since σ₁ and σ₃ occur only positively and σ₂ only negatively. Its permutation is a 4-cycle when m is odd, so the closure is a knot. ∎

The same argument shows more generally: a root of the closure of B^k is a root of the closure of B^(km) for every m. `family.py` checks the family numerically: |Δ(z₀)| ≈ 10⁻⁸² relative to Δ's size, for the knots of 33, 99, …, 495 crossings, at 80 digits.

Other powers of the same block cross the line too: B⁵, B⁷, B⁹ and B¹¹ have roots at Re −1.123, −1.120, −1.134 and −1.128 (Newton-verified). As k grows, the roots of B^k spread along the curve {t : |λᵢ(t)| = 1} described below.

### Twist families with exact limits
Twisting one group of a skeleton more and more gives a family whose roots converge to the roots of one fixed "parent" polynomial. Examples:
- For K33 and K39, (σ₁³σ₂⁻³σ₃³σ₂⁻ᵈ)³ breaks Hoste's conjecture for **every even d**, with roots converging to −1.150187 ± 1.634806 i.
- Of all 1,038,334 skeletons up to 13 letters, 2,478 give such families (629 distinct). Every one comes with an exact limit and a certified threshold.

See [`families/`](families/).

**The first example found, K55,** is the closure of the 4-strand braid

    (σ₁² σ₂⁻³ σ₃ σ₂⁻¹ σ₃ σ₂⁻² σ₁)⁵

- **Crossings:** 55.
- **Alternating:** σ₁ and σ₃ appear only positively and σ₂ only negatively, so the closed-braid diagram is alternating.
- **Knot, not link:** the braid permutation is a 4-cycle.
- **Its Alexander polynomial** (degree 52, coefficients in `k55_certificate.json`) has the roots

      z = −1.12352541571570459062212413960 ± 1.35602878189159477935587183763 i

  These have Re(z) < −1.

**A second example, K57,** is (σ₃ σ₂⁻⁵ σ₁³ σ₂⁻⁶ σ₃⁴)³: 57 crossings, with roots at −1.19091423284003776230 ± 1.41538951538023486785 i.

**A smaller one, K45,** is (σ₃ σ₂⁻¹ σ₃ σ₂⁻¹ σ₃² σ₂⁻⁴ σ₁³ σ₂⁻²)³: 45 crossings, with roots at −1.08099125200658141624 ± 1.59244134977223715792 i. It passes the same checks.

**K39** is (σ₁³ σ₂⁻³ σ₃³ σ₂⁻⁴)³: 39 crossings, with roots at −1.19184765240544104700 ± 1.65233250328234941290 i. It passes the same checks. It was found by sampling braid blocks that match rules learned (by a decision tree) from 260,000 labelled random blocks. That search was not exhaustive.

## Previously known
Counterexamples were known only among alternating Montesinos knots:
- **Existence:** Ishikawa, *JKTR* 2018.
- **Explicit examples:** Hirasawa–Ishikawa–Suzuki, *Topology Appl.* 253 (2019).
  - The smallest claimed has 740 crossings (numerical; Ishikawa, Remark 5.6). The smallest verified in the paper has 778.
  - Their roots reach only Re ≈ −1.001.

We found no earlier counterexample that is a braid closure, that has fewer than 740 crossings, or whose roots go clearly past −1.

## Checks (`verify.py`)
Run `pip install mpmath` (optional: `pip install snappy`), then `python verify.py K31` (or `K33`, `K39`, `K45`, `K55`, `K57`, or `all`). It runs in seconds and:
1. computes Δ exactly from the reduced Burau representation: (1 + t + t² + t³) Δ(t) = det(I − ψ(β));
2. checks the word is alternating and the closure is one component;
3. checks Δ has strictly alternating coefficient signs, which rules out a t ↦ −t convention slip, and that it is symmetric, with Δ(1) = ±1 (sign of the normalisation), monic, of degree c − n + 1 (28 for K31, 30 for K33, 36 for K39, 42 for K45, 52 for K55);
4. finds the roots to 50 digits, with |Δ(z)| ≈ 10⁻³⁴;
5. counts roots in the box −6 < Re < −1, |Im| < 6 by the argument principle, which finds 2 without locating them;
6. with SnapPy installed, recomputes Δ = det(V − tVᵀ) from the Seifert matrix of the actual diagram, an independent method, and confirms the diagram is alternating with one component.

## How it was found
- **The obstacle:** searching alternating braids one at a time stalls at about −0.9992. The near-miss roots lie on the unit circle, which touches Re = −1 only at t = −1, never a root.
- **The key fact:** for a repeated block B, every root of every closure of Bᵃ lies on the curve {t : |λᵢ(t)| = 1}, where λᵢ are the eigenvalues of B's Burau matrix.
- **The search:** blocks were scored by how far left the part of that curve off the unit circle reaches. Blocks whose curve crosses Re = −1 give knots whose roots cross for suitable a.

## Files
- `verify.py`: standalone verification.
- `NOTES.md`: side findings (balanced windings, the ring-resonator view, coils, other conjectures checked) and lessons from the search.
- `family.py`: checks that K33's root is a root of every knot in the infinite family (B^(3m), m odd).
- `k31_certificate.json`, `k33_certificate.json`, `k39_certificate.json`, `k45_certificate.json`, `k55_certificate.json`, `k57_certificate.json`: braid word, PD code, exact Alexander coefficients, roots, and checks.
- `index.html`: all the knots; `31.html` … `57.html`: open in a browser to see each knot in 3D (drag to rotate, scroll to zoom).
- `make_viewers.py`: rebuilds every page from the certificates (add a `k<N>_certificate.json`, rerun, its page appears).

Status: computer-verified as above; not yet reviewed by a knot theorist.
