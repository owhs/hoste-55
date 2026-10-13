"""Verify the counterexamples to Hoste's conjecture (K31, K33, K39, K45, K55, K57).

Hoste's conjecture (2002; Lyubich-Murasugi 2012, Conj. 1): if K is an alternating knot, every root z of its Alexander
polynomial satisfies Re(z) > -1.

The knots: closures of 4-strand braids, e.g. K33 = (s1^3 s2^-3 s3^3 s2^-2)^3. Generators s1, s3 appear only positively and
s2 only negatively, so the closed braid diagram is alternating; the braid permutation is a 4-cycle, so it is a knot.

This script computes the Alexander polynomial exactly from the reduced Burau representation,
    (1 + t + t^2 + t^3) * Delta(t) = det(I - psi(beta)),
checks it, and finds its roots to 50 digits. Optional: if SnapPy is installed, it recomputes Delta from the Seifert matrix
of the actual knot diagram, an independent method.

Requirements: Python 3.8+, mpmath (pip install mpmath). Optional: snappy, sympy.
Run: python verify.py [K31 | K33 | K39 | K45 | K55 | K57 | all]   (default K31)
"""
import sys

import mpmath

KNOTS = {   # name: (block, strands, repeats); 1 = s1, -2 = s2^-1, ...
    "K31": ([3, 3, 3, -2, -2, 1, 1, 1, -2, -2, -2, 3, 3, 3, -2, -2, -2, 1, 1, 1, -2, -2, 3, 3, -2, -2, 1, 1, -2, -2, -2], 4, 1),
    "K33": ([1, 1, 1, -2, -2, -2, 3, 3, 3, -2, -2], 4, 3),
    "K39": ([1, 1, 1, -2, -2, -2, 3, 3, 3, -2, -2, -2, -2], 4, 3),
    "K45": ([3, -2, 3, -2, 3, 3, -2, -2, -2, -2, 1, 1, 1, -2, -2], 4, 3),
    "K55": ([1, 1, -2, -2, -2, 3, -2, 3, -2, -2, 1], 4, 5),
    "K57": ([3, -2, -2, -2, -2, -2, 1, 1, 1, -2, -2, -2, -2, -2, -2, 3, 3, 3, 3], 4, 3),
}
NAME = sys.argv[1] if len(sys.argv) > 1 else "K31"
if NAME == "all":   # every knot in turn, each in its own run
    import subprocess
    for k in KNOTS:
        print(f"\n===== {k} =====", flush=True)
        subprocess.run([sys.executable, __file__, k], check=True)
    sys.exit(0)
BLOCK, STRANDS, REPEATS = KNOTS[NAME]
WORD = BLOCK * REPEATS


# ---------- integer polynomials (lists of coefficients, lowest degree first) ----------
def padd(a, b):
    out = (a + [0] * (len(b) - len(a))) if len(b) > len(a) else a[:]
    for i, c in enumerate(b):
        out[i] += c
    return out


def pscale(a, c, shift=0):
    return [0] * shift + [c * x for x in a]


def pmul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pdet(M):
    if len(M) == 1:
        return M[0][0]
    out = []
    for c in range(len(M)):
        sub = [row[:c] + row[c + 1:] for row in M[1:]]
        out = padd(out, pscale(pmul(M[0][c], pdet(sub)), (-1) ** c))
    return out


def alexander_burau(word, n):
    """exact Delta(t) of the closed braid, up to +-t^k.
    Reduced Burau: psi(s_i) acts on column i of an (n-1)x(n-1) matrix; for s_i^-1 we multiply by (-t) psi(s_i)^-1, which
    is polynomial, and correct with (-t)^k at the end: f(t) = det((-t)^k I - Q), Q = (-t)^k psi(beta)."""
    m = n - 1
    P = [[[1] if r == c else [] for c in range(m)] for r in range(m)]
    k = 0
    for g in word:
        j = abs(g) - 1
        col = lambda c: [P[r][c] for r in range(m)]
        L = col(j - 1) if j >= 1 else None
        C = col(j)
        R = col(j + 1) if j + 1 < m else None
        if g > 0:
            new = [pscale(C[r], -1, 1) for r in range(m)]                      # -t * C
            if L is not None:
                new = [padd(new[r], pscale(L[r], 1, 1)) for r in range(m)]    # + t * L
            if R is not None:
                new = [padd(new[r], R[r]) for r in range(m)]                  # + R
            for r in range(m):
                P[r][j] = new[r]
        else:
            k += 1
            new = [C[r][:] for r in range(m)]                                  # C
            if L is not None:
                new = [padd(new[r], pscale(L[r], -1, 1)) for r in range(m)]   # - t * L
            if R is not None:
                new = [padd(new[r], pscale(R[r], -1)) for r in range(m)]      # - R
            for r in range(m):
                for c in range(m):
                    if c != j:
                        P[r][c] = pscale(P[r][c], -1, 1)                       # other columns times -t
                P[r][j] = new[r]
    lead = pscale([1], (-1) ** k, k)
    M = [[padd(lead if r == c else [], pscale(P[r][c], -1)) for c in range(m)] for r in range(m)]
    f = pdet(M)
    while f and f[-1] == 0:
        f.pop()
    q, rem = [], f[:]                                                          # divide by 1 + t + ... + t^(n-1)
    while len(rem) >= n:
        lead_c = rem[-1]; q.append(lead_c)
        for i in range(n):
            rem[len(rem) - n + i] -= lead_c
        rem.pop()
    assert all(x == 0 for x in rem), "division failed"
    q = q[::-1]
    while q and q[0] == 0:
        q.pop(0)
    return q


def is_knot(word, n):
    perm = list(range(n))
    for g in word:
        i = abs(g) - 1
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    x, steps = perm[0], 1
    while x != 0:
        x, steps = perm[x], steps + 1
    return steps == n


def roots_in_box(c, x0, x1, y0, y1, steps=4000):
    """argument principle: number of roots of c inside the box, without locating them"""
    p = lambda z: mpmath.polyval(c[::-1], z)
    corners = [mpmath.mpc(x0, y0), mpmath.mpc(x1, y0), mpmath.mpc(x1, y1), mpmath.mpc(x0, y1), mpmath.mpc(x0, y0)]
    total, prev = mpmath.mpf(0), p(corners[0])
    for a, b in zip(corners, corners[1:]):
        for s in range(1, steps + 1):
            cur = p(a + (b - a) * s / steps)
            total += mpmath.arg(cur / prev)
            prev = cur
    return total / (2 * mpmath.pi)


def main():
    mpmath.mp.dps = 50
    print(f"braid: ({' '.join(('s%d' % g) if g > 0 else ('s%d^-1' % -g) for g in BLOCK)})^{REPEATS} on {STRANDS} strands, {len(WORD)} crossings")
    alt = all((g > 0) == (abs(g) % 2 == 1) for g in WORD)
    print(f"alternating braid word (s1, s3 positive; s2 negative): {alt}")
    print(f"one component (permutation is a {STRANDS}-cycle): {is_knot(WORD, STRANDS)}")
    D = alexander_burau(WORD, STRANDS)
    print(f"Alexander polynomial: degree {len(D) - 1}, coefficients (lowest first): {D}")
    print(f"  coefficients alternate in sign (so this is Delta(t), not Delta(-t)): {all(D[i] * D[i + 1] < 0 for i in range(len(D) - 1))}")
    print(f"  symmetric: {D == D[::-1] or D == [-x for x in D[::-1]]};  Delta(1) = {sum(D)};  monic: {abs(D[0]) == 1}")
    roots = mpmath.polyroots(D[::-1], maxsteps=2000, extraprec=600)
    past = sorted([z for z in roots if mpmath.re(z) < -1], key=lambda z: mpmath.im(z))
    print(f"roots with real part < -1: {len(past)}")
    for z in past:
        print(f"  {mpmath.nstr(z, 30)}   |Delta(z)| = {mpmath.nstr(abs(mpmath.polyval(D[::-1], z)), 3)}")
    print(f"argument principle, roots in Re (-6, -1) x Im (-6, 6): {mpmath.nstr(roots_in_box(D, -6, -1, -6, 6), 6)}")
    try:                                                                       # independent method, optional
        import snappy  # noqa: F401
        import spherogram
        L = spherogram.Link(spherogram.ClosedBraid(WORD).PD_code())
        V = [[int(x) for x in row] for row in L.seifert_matrix()]
        s = seifert_alexander(V)
        norm = lambda p: tuple(p) if p[0] > 0 else tuple(-x for x in p)
        print(f"SnapPy check: diagram alternating {L.is_alternating()}, components {len(L.link_components)}, "
              f"Seifert-matrix polynomial equals the Burau one: {norm(s) == norm(D)}", flush=True)
    except ImportError:
        print("(optional SnapPy check skipped: pip install snappy)")


def bareiss(M):
    """exact integer determinant"""
    M = [list(r) for r in M]; n, sign, prev = len(M), 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k]:
                    M[k], M[i] = M[i], M[k]; sign = -sign; break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1] if n else 1


def seifert_alexander(V):
    """Delta(t) = det(V - t V^T): exact values at t = 0..n, then exact interpolation (Fractions)"""
    from fractions import Fraction
    n = len(V)
    xs = list(range(n + 1))
    ys = [bareiss([[V[i][j] - t * V[j][i] for j in range(n)] for i in range(n)]) for t in xs]
    coef = [Fraction(y) for y in ys]
    for j in range(1, n + 1):
        for i in range(n, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    poly = [coef[n]]
    for i in range(n - 1, -1, -1):
        out = [Fraction(0)] * (len(poly) + 1)
        for k, c in enumerate(poly):
            out[k + 1] += c; out[k] -= xs[i] * c
        out[0] += coef[i]
        poly = out
    p = [int(c) for c in poly]
    while p and p[-1] == 0:
        p.pop()
    while p and p[0] == 0:
        p.pop(0)
    return p


if __name__ == "__main__":
    main()
