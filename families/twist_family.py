"""Twist families of alternating knots that break Hoste's conjecture, with exact limits.

For a skeleton word W in s1, s2^-1, s3 (an alternating 4-braid word) and a twist d, let K_d be the closure of
(W s2^-d)^3. In the reduced Burau representation psi(s2)^-d = I + (x - 1) Pi with x = (-t)^-d, where Pi is the
rank-one projector with (-t - 1) Pi = S2 - I. So, exactly,

    det(I - psi(K_d block)^3)  =  c0(t) + c1(t) x + c2(t) x^2 + c3(t) x^3,      x = (-t)^-d,

and (1 + t + t^2 + t^3) Delta_{K_d}(t) is this determinant (up to a unit). For |t| > 1, x -> 0 as d grows, so the roots
of Delta_{K_d} outside the unit circle converge to the roots of the "parent" polynomial c0. If c0 has a root z* with
Re z* < -1, Rouche's theorem on a small circle around z* gives a twist d0 beyond which every K_d has a root inside that
circle, so every such knot breaks Hoste's conjecture.

This script computes c0..c3 exactly (integer polynomial matrices), roots c0, finds d0 (checked on 4,000 points of the
circle with a 1.5x margin), and checks the convergence directly on the knots' own Alexander polynomials.

Requirements: numpy, mpmath.
Run:  python twist_family.py                      (default skeleton s1^3 s2^-3 s3^3: the family of K33 and K39)
      python twist_family.py 1 1 1 1 -2 -2 -2 -2 3 3 3 3     (any skeleton: 1 = s1, -2 = s2^-1, 3 = s3)
"""
import sys

import mpmath
import numpy as np


# ---------- integer polynomials in t (lowest degree first) and in (t, x) (dict: x-power -> polynomial in t)
def padd(a, b):
    out = list(a) + [0] * (len(b) - len(a)) if len(b) > len(a) else list(a)
    for i, c in enumerate(b):
        out[i] += c
    return out


def pmul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def ptrim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def badd(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = padd(out.get(k, []), v)
    return out


def bmul(a, b):
    out = {}
    for i, u in a.items():
        for j, v in b.items():
            out[i + j] = padd(out.get(i + j, []), pmul(u, v))
    return out


def bneg(a):
    return {k: [-c for c in v] for k, v in a.items()}


def mat_mul(A, B):
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            s = {}
            for l in range(3):
                s = badd(s, bmul(A[i][l], B[l][j]))
            row.append(s)
        out.append(row)
    return out


def det3(M):
    a, b, c = M[0]; d, e, f = M[1]; g, h, i = M[2]
    return badd(badd(bmul(a, badd(bmul(e, i), bneg(bmul(f, h)))), bneg(bmul(b, badd(bmul(d, i), bneg(bmul(f, g)))))),
                bmul(c, badd(bmul(d, h), bneg(bmul(e, g)))))


C = lambda p: {0: p}
ONE, ZERO, T, MT = C([1]), {}, C([0, 1]), C([0, -1])
ID = [[ONE if i == j else ZERO for j in range(3)] for i in range(3)]
S1 = [[MT, ZERO, ZERO], [ONE, ONE, ZERO], [ZERO, ZERO, ONE]]          # reduced Burau of s1, s2, s3 on 4 strands
S2 = [[ONE, T, ZERO], [ZERO, MT, ZERO], [ZERO, ONE, ONE]]
S3 = [[ONE, ZERO, ZERO], [ZERO, ONE, T], [ZERO, ZERO, MT]]
S2ADJ = [[MT, MT, ZERO], [ZERO, ONE, ZERO], [ZERO, C([-1]), MT]]      # adj(S2) = (-t) S2^-1, polynomial


def family_polynomial(W, k=3):
    """{j: c_j(t)} with det(D I - P(x)^k) = sum_j c_j(t) x^j; D = ((-t)^q (t + 1))^k clears all denominators"""
    Q, q = ID, 0
    for g in W:
        Q = mat_mul(Q, {1: S1, 3: S3, -2: S2ADJ}[g]); q += g == -2
    one_minus_x = {0: [1], 1: [-1]}
    S2mI = [[badd(S2[i][j], bneg(ID[i][j])) for j in range(3)] for i in range(3)]
    R = [[badd(bmul(C([1, 1]), ID[i][j]), bmul(one_minus_x, S2mI[i][j])) for j in range(3)] for i in range(3)]
    P = mat_mul(Q, R); Pk = P
    for _ in range(k - 1):
        Pk = mat_mul(Pk, P)
    D = [1]
    for _ in range(k):
        D = pmul(D, [1, 1])
        for _ in range(q):
            D = pmul(D, [0, -1])
    M = [[badd(C(D) if i == j else ZERO, bneg(Pk[i][j])) for j in range(3)] for i in range(3)]
    return {j: ptrim(v) for j, v in det3(M).items() if ptrim(v)}


def parent_roots(F):
    c0 = ptrim(F.get(0, []))
    while c0 and c0[0] == 0:
        c0 = c0[1:]
    mpmath.mp.dps = 40
    out = []
    for z in np.roots(c0[::-1]):
        if abs(z) <= 1 + 1e-6 or abs(z + 1) < 1e-3:
            continue
        try:
            zz = mpmath.findroot(lambda s: mpmath.polyval(c0[::-1], s), mpmath.mpc(z), tol=1e-30, maxsteps=100)
        except Exception:
            continue
        if abs(mpmath.polyval(c0[::-1], zz)) / mpmath.polyval([abs(c) for c in c0[::-1]], abs(zz)) < 1e-25:
            out.append(complex(zz))
    return sorted({(round(z.real, 12), round(z.imag, 12)) for z in out}), c0


def rouche_d0(F, z, rho):
    pts = z + rho * np.exp(2j * np.pi * np.arange(4000) / 4000)
    ev = lambda p: np.polyval(p[::-1], pts) if p else 0 * pts
    c0 = np.abs(ev(F.get(0, [])))
    for d in range(1, 400):
        tail = sum(np.abs(ev(v)) * np.abs(pts) ** (-j * d) for j, v in F.items() if j >= 1)
        if np.all(c0 > 1.5 * tail):
            return d
    return None


# ---------- the knots themselves: Alexander polynomial from the Burau representation (as in verify.py)
def alexander(word, n=4):
    m = n - 1
    P = [[[1] if r == c else [] for c in range(m)] for r in range(m)]
    k = 0
    sc = lambda a, c, s=0: [0] * s + [c * x for x in a]
    for g in word:
        j = abs(g) - 1
        col = lambda c: [P[r][c] for r in range(m)]
        L = col(j - 1) if j >= 1 else None; Cc = col(j); Rr = col(j + 1) if j + 1 < m else None
        if g > 0:
            new = [sc(Cc[r], -1, 1) for r in range(m)]
            if L is not None: new = [padd(new[r], sc(L[r], 1, 1)) for r in range(m)]
            if Rr is not None: new = [padd(new[r], Rr[r]) for r in range(m)]
            for r in range(m): P[r][j] = new[r]
        else:
            k += 1
            new = [Cc[r][:] for r in range(m)]
            if L is not None: new = [padd(new[r], sc(L[r], -1, 1)) for r in range(m)]
            if Rr is not None: new = [padd(new[r], sc(Rr[r], -1)) for r in range(m)]
            for r in range(m):
                for c in range(m):
                    if c != j: P[r][c] = sc(P[r][c], -1, 1)
                P[r][j] = new[r]
    lead = sc([1], (-1) ** k, k)
    Mx = [[padd(lead if r == c else [], sc(P[r][c], -1)) for c in range(m)] for r in range(m)]
    def pdet(M):
        if len(M) == 1: return M[0][0]
        out = []
        for c in range(len(M)):
            out = padd(out, sc(pmul(M[0][c], pdet([row[:c] + row[c + 1:] for row in M[1:]])), (-1) ** c))
        return out
    f = ptrim(pdet(Mx)); q, rem = [], f[:]
    while len(rem) >= n:
        c = rem[-1]; q.append(c)
        for i in range(n): rem[len(rem) - n + i] -= c
        rem.pop()
    q = q[::-1]
    while q and q[0] == 0: q.pop(0)
    return q


def is_knot(word, n=4):
    p = list(range(n))
    for g in word:
        i = abs(g) - 1; p[i], p[i + 1] = p[i + 1], p[i]
    x, s = p[0], 1
    while x != 0: x, s = p[x], s + 1
    return s == n


def main():
    W = [int(a) for a in sys.argv[1:]] or [1, 1, 1, -2, -2, -2, 3, 3, 3]
    name = {1: "s1", -2: "s2^-1", 3: "s3"}
    print("skeleton W =", " ".join(name[g] for g in W), " family K_d = closure of (W s2^-d)^3")
    F = family_polynomial(W)
    print(f"exact: det(I - psi^3) = c0 + c1 x + c2 x^2 + c3 x^3 with x = (-t)^-d; degrees {[len(F[j]) - 1 for j in sorted(F)]}")
    roots, c0 = parent_roots(F)
    past = [complex(*r) for r in roots if r[0] < -1]
    if not past:
        print("the parent polynomial has no root with real part < -1: this family does not break Hoste for large d")
        return
    z = min(past, key=lambda w: w.real)
    rho = min(0.08, 0.9 * (abs(z.real) - 1))
    d0 = rouche_d0(F, z, rho)
    print(f"parent root z* = {z.real:.10f} {'+' if z.imag >= 0 else '-'} {abs(z.imag):.10f} i")
    print(f"Rouche: for every d >= {d0}, K_d has a root within {rho} of z* (real part < {z.real + rho:.4f})")
    print("check on the knots themselves (exact Alexander polynomial, root nearest z*):")
    mpmath.mp.dps = 50
    for d in range(1, 16):
        w = (W + [-2] * d) * 3
        if not is_knot(w):
            continue
        a = alexander(w)[::-1]
        start = min(np.roots(a), key=lambda s: abs(s - z))   # the knot's own root nearest z*, then refined
        try:
            r = mpmath.findroot(lambda s: mpmath.polyval(a, s) / mpmath.polyval([abs(c) for c in a], abs(s)), mpmath.mpc(start), maxsteps=200)
            r = complex(r)
            print(f"  d = {d:2d}: {len(w):3d} crossings, root {r.real:.6f} {'+' if r.imag >= 0 else '-'} {abs(r.imag):.6f} i, "
                  f"distance to z* {abs(r - z):.1e}{'   (past -1)' if r.real < -1 else ''}")
        except Exception:
            print(f"  d = {d:2d}: {len(w):3d} crossings, Newton did not converge from z* (small d: the root is still far)")


if __name__ == "__main__":
    main()
