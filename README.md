# A 55-crossing counterexample to Hoste's conjecture

**Hoste's conjecture** (J. Hoste, 2002; stated in Lyubich–Murasugi, *Topology Appl.* 159 (2012), Conjecture 1): if K is an alternating knot, every root z of its Alexander polynomial Δ_K(t) satisfies Re(z) > −1.

**The knot K55** is the closure of the 4-strand braid

    (σ₁² σ₂⁻³ σ₃ σ₂⁻¹ σ₃ σ₂⁻² σ₁)⁵

- **Crossings:** 55.
- **Alternating:** σ₁ and σ₃ appear only positively and σ₂ only negatively, so the closed-braid diagram is alternating.
- **Knot, not link:** the braid permutation is a 4-cycle.
- **Its Alexander polynomial** (degree 52, coefficients in `k55_certificate.json`) has the roots

      z = −1.12352541571570459062212413960 ± 1.35602878189159477935587183763 i

  These have Re(z) < −1.

**A second example, K57,** is (σ₃ σ₂⁻⁵ σ₁³ σ₂⁻⁶ σ₃⁴)³: 57 crossings, with roots at −1.19091423284003776230 ± 1.41538951538023486785 i.

**A smaller one, K45,** is (σ₃ σ₂⁻¹ σ₃ σ₂⁻¹ σ₃² σ₂⁻⁴ σ₁³ σ₂⁻²)³: 45 crossings, with roots at −1.08099125200658141624 ± 1.59244134977223715792 i. It passes the same checks. A search of 40,000 patterns up to 54 crossings found nothing smaller; that search was not exhaustive.

## Previously known
Counterexamples were known only among alternating Montesinos knots:
- **Existence:** Ishikawa, *JKTR* 2018.
- **Explicit examples:** Hirasawa–Ishikawa–Suzuki, *Topology Appl.* 253 (2019).
  - The smallest claimed has 740 crossings (numerical; Ishikawa, Remark 5.6). The smallest verified in the paper has 778.
  - Their roots reach only Re ≈ −1.001.

We found no earlier counterexample that is a braid closure, that has fewer than 740 crossings, or whose roots go clearly past −1.

## Checks (`verify.py`)
Run `pip install mpmath` (optional: `pip install snappy`), then `python verify.py K45` (or `K55`, `K57`). It runs in seconds and:
1. computes Δ exactly from the reduced Burau representation: (1 + t + t² + t³) Δ(t) = det(I − ψ(β));
2. checks the word is alternating and the closure is one component;
3. checks Δ has strictly alternating coefficient signs, which rules out a t ↦ −t convention slip, and that it is symmetric, with Δ(1) = 1, monic, of degree c − n + 1 (52 for K55, 42 for K45);
4. finds the roots to 50 digits, with |Δ(z)| ≈ 10⁻³⁴;
5. counts roots in the box −6 < Re < −1, |Im| < 6 by the argument principle, which finds 2 without locating them;
6. with SnapPy installed, recomputes Δ = det(V − tVᵀ) from the Seifert matrix of the actual diagram, an independent method, and confirms the diagram is alternating with one component.

## How it was found
- **The obstacle:** searching alternating braids one at a time stalls at about −0.9992. The near-miss roots lie on the unit circle, which touches Re = −1 only at t = −1, never a root.
- **The key fact:** for a repeated block B, every root of every closure of Bᵃ lies on the curve {t : |λᵢ(t)| = 1}, where λᵢ are the eigenvalues of B's Burau matrix.
- **The search:** blocks were scored by how far left the part of that curve off the unit circle reaches. Blocks whose curve crosses Re = −1 give knots whose roots cross for suitable a.

## Files
- `verify.py`: standalone verification.
- `k45_certificate.json`, `k55_certificate.json`, `k57_certificate.json`: braid word, PD code, exact Alexander coefficients, roots, and checks.
- `45.html`, `55.html`, `57.html`: open in a browser to see each knot in 3D (drag to rotate, scroll to zoom).

Status: computer-verified as above; not yet reviewed by a knot theorist.
