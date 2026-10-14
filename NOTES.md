# Notes: side findings and lessons

These are observations made along the way. They are less polished than the main results, and each one is marked as a theorem, a measurement or an analogy.

## Counterexamples are balanced windings (measurement, with a reason)
- **The observation:** the net twist (writhe: positive minus negative crossings) of the counterexamples is close to zero. K31 has +1, K33 has +3 and K39 has −3.
- **The measurement:** among all 2,368 knots of 39 crossings in the syllable family, counterexamples never exceed |writhe| / crossings = 0.23, while the others reach 0.69. Balance alone separates them better than chance, with AUC 0.72.
- **The reason (theorem, Murasugi):** an alternating knot whose crossings all twist one way is *special alternating*, and all its Alexander roots lie on the unit circle. Such a knot can never break Hoste's line, and the more one-sided a winding is, the closer it gets to that regime. Breaking the line needs the twists to roughly cancel.
- **The analogy:** this is the same cancellation idea as a twisted-pair cable.

## The Burau maths as a ring resonator (exact rewording, then analogy)
- **The picture:** treat each crossing as a coupler that multiplies a travelling wave by −t. A closed braid is then a ring of couplers.
- **Roots are resonances:** det(I − M) = 0 says a wave comes back unchanged after one trip round the ring. That is an exact rewording.
- **The unit circle is the lossless case (theorem, Squier):** for |t| = 1 the Burau matrices preserve a Hermitian form, so energy is conserved there.
- **Hoste's line in this language:** write −t = e^g · e^{iφ}, with g the gain per crossing and φ the phase. Re t = −1 becomes g = −ln(cos φ), so Hoste's conjecture says an alternating ring cannot resonate with more gain than −ln(cos φ).
- **Where the families sit (measurement):** all 102 breaking families with skeletons up to 10 letters resonate at a phase of 53–59° per crossing and a gain of 0.62–0.69, crossing that curve by 0.003 to 0.16. Deeper families do it at a *smaller* phase, where the line is easier to cross.

## Knots as coils (measurement; the physics is textbook)
- **The setup:** the 3D wire of each knot was used as a coil, with its field computed by the Biot–Savart law. In the air gap above the winding, the azimuthal harmonics come only in multiples of the braid's period: multiples of 3 for K33, K39, K45 and K57, and multiples of 5 for K55. K31, which has no symmetry, has all harmonics.
- **The geometric version:** SnapPy finds the same symmetries in the hyperbolic geometry: D₃ for K33 and K39, ℤ/3 for K45 and K57, ℤ/5 for K55, and the trivial group for K31.
- **Winding practice:** Roebel bars and Litz wire use braid transpositions so that every strand spends equal time in every position. The braid ends with each strand back in place, a link rather than a single cycle, so it is a related idea, not the same condition as "the closure is a knot".

## Two other conjectures checked on the same knots (measurement)
- **Log-concavity and Fox's trapezoidal conjecture:** no failure in 50,688 family knots, the twist-family members up to 159 crossings, K31, or 9,972 random alternating 4-braid knots of 31 to 119 crossings. These knots break Hoste's conjecture but not these two.
- **Liechti's conjecture** (positive knots have roots with Re < 1): no failure in 19,958 random positive diagrams of 10 to 32 crossings. Their off-circle roots stayed right of 0.5.

## Lessons from the search (method)
1. **A plateau is often a wall.** The first search stalled at −0.9992 because the near-misses sat on the unit circle, which can never cross −1. The fix was to change what is measured, not to search harder.
2. **Turn infinite sets into one object.** A twist family is one polynomial, and infinitely many repeats are one curve. Exact and fast beats clever and approximate.
3. **Verify extreme numbers at high precision.** Three apparent depth records were artifacts: FFT reconstruction, split repeated roots, and overflowing eigenvalues.
4. **Diversity beats cleverness when generating.** Small edits of known winners found about twice as many new families as any learned scorer did. Filtering the edits with a learned model made the search worse, because the filter narrowed the variety of candidates.
5. **Build in the symmetries.** Flipping a braid (σ₁ ↔ σ₃) or reading it backwards gives the same knot. Encodings that ignore these disguises work better.
