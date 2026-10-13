"""Check the infinite family: K33's root z0 is a root of the closure of B^(3m) for every odd m, B = s1^3 s2^-3 s3^3 s2^-2.

Why (the proof is in README.md): (1 + t + t^2 + t^3) Delta(B^k)(t) = det(I - psi(B)^k) = prod_i (1 - lambda_i(t)^k), where
lambda_i(t) are the eigenvalues of B's reduced Burau matrix. At z0 some lambda_i(z0)^3 = 1, so lambda_i(z0)^(3m) = 1 too.

This script computes Delta exactly for each knot and evaluates it at z0 to 80 digits.
Requirements: mpmath. Run: python family.py [max_m]   (default 15: knots of 33, 99, ..., 495 crossings)
"""
import sys

import mpmath

MAX_M = int(sys.argv[1]) if len(sys.argv) > 1 else 15
sys.argv = [sys.argv[0], "K33"]   # verify.py reads its knot name from the command line on import
import verify as V  # noqa: E402

mpmath.mp.dps = 80
B = [1, 1, 1, -2, -2, -2, 3, 3, 3, -2, -2]
c33 = V.alexander_burau(B * 3, 4)
z0 = mpmath.findroot(lambda z: mpmath.polyval(c33[::-1], z), mpmath.mpc(-1.0747, 1.7916))
print(f"z0 = {mpmath.nstr(z0, 40)}  (the K33 root, Re z0 < -1)")
print(f"{'m':>3} {'crossings':>10}  knot  |Delta(z0)| relative to the size of Delta")
for m in range(1, MAX_M + 1, 2):
    w = B * (3 * m)
    c = V.alexander_burau(w, 4)
    rel = abs(mpmath.polyval(c[::-1], z0)) / mpmath.polyval([abs(x) for x in c[::-1]], abs(z0))
    print(f"{m:>3} {len(w):>10}  {V.is_knot(w, 4)}  {mpmath.nstr(rel, 3)}")
print("every value ~1e-80 means z0 is a root of each knot's Alexander polynomial: all are counterexamples")
