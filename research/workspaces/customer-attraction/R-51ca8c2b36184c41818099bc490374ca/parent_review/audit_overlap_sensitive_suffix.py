"""Root's independent exact audit of the real final-two-player inequality."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def membership_audit():
    cases = 0
    for bits in product(range(2), repeat=6):
        c, d, t1, t2, r1, r2 = bits
        t, r = t1+t2, r1+r2
        h, z = t1*r1+t2*r2, t1*t2
        psi = 8*c-c*t+h-4*c*r+8*z
        assert psi >= 0
        for b in [F(0), F(1), F(2), F(3), F(17), F(10**6), F(1, 2), F(11, 7)]:
            U = lambda x, y: F(x)/(b+1+y)
            R = lambda x, y: U(x, y)+U(y, x)
            u, v = U(c, d), U(d, c)
            fs = u-U(t1, r1)+u-U(t2, r2)
            ps = v-U(t1, c)+v-U(t2, c)
            zs = v-U(r1, c)+v-U(r2, c)
            vs = U(r1, t1)-U(t2, t1)+U(r2, t2)-U(t1, t2)
            G = 3*fs+ps+4*zs+4*vs
            g = F(1)/((b+1)*(b+2))
            B = 6*u+10*v+8*g*c
            assert B-8*R(t1, t2)-G == g*psi
            assert B-10*R(c, d) == 4*g*c*(d-b)
            if b.denominator == 1:
                assert B <= 10*R(c, d)+2*int(b == 0)*c*d
            cases += 1
    return cases


def endpoint(p, q):
    """Build actual disjoint unit customers, then check every root and last move."""
    first = [{0, 1, 2}, {0, 1, 3}, {0, 1}, {3, 4}]
    reply_first = [1, 0, 3, 0]
    second = [{0, 1}, {2}]
    axes_a = range(4) if p else [None]
    axes_b = range(2) if q else [None]
    if not p and not q:
        axes_a, axes_b = [None], [None]
    labels = list(product(axes_a, axes_b))
    themes = {}
    for a, b in labels:
        customers = set()
        if a is not None:
            customers |= {("a", j, x) for j in range(p) for x in first[a]}
        if b is not None:
            customers |= {("b", j, x) for j in range(q) for x in second[b]}
        themes[a, b] = customers
    root = (2 if p else None, 0 if q else None)
    replies = {(a, b): (reply_first[a] if p else None, 0 if q else None)
               for a, b in labels}

    def U(a, b):
        return sum((F(1, 1+int(x in themes[b])) for x in themes[a]), F(0))

    chosen_second = replies[root]
    u = U(root, chosen_second)
    checks = 0
    for a in labels:
        assert u >= U(a, replies[a])
        checks += 1
        for b in labels:
            assert U(replies[a], a) >= U(b, a)
            checks += 1
    W = len(themes[root] | themes[chosen_second])
    I = len(themes[root] & themes[chosen_second])
    OPT = max(len(themes[a] | themes[b]) for a, b in product(labels, repeat=2))
    assert (W, I, OPT) == (4*p+2*q, 2*q, 5*p+3*q)
    assert 8*OPT == 10*W+2*I
    return {"p": p, "q": q, "W": W, "I": I, "OPT": OPT, "comparisons": checks}


def main():
    records = [endpoint(p, q) for p in range(5) for q in range(5)]
    for denominator in range(1, 11):
        for numerator in range(denominator+1):
            e = endpoint(denominator-numerator, 2*numerator)
            assert F(e["I"], e["W"]) == F(numerator, denominator)
    report = {"status": "exact independent audit passed", "membership_cases": membership_audit(),
              "endpoint_records": records, "rational_ratio_denominator_max": 10}
    Path(__file__).with_name("overlap_sensitive_suffix_audit.json").write_text(
        json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k != "endpoint_records"}))


if __name__ == "__main__":
    main()
