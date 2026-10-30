#!/usr/bin/env python3
"""Exact standard-library sign certificate for source equation (3), d=32.

Use `python verify.py` to verify the frozen certificate, or
`python verify.py --generate new_certificate.json` to produce a new one.
No floating point or external packages are used.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from math import comb, lcm
from pathlib import Path
import time

if not __debug__:
    raise RuntimeError("Run without -O: verification assertions must be enabled.")

D = 32
P = 89
Q = 50
T = Fraction(P, Q)
N_MAX = 55
W_LO = Fraction(1, 55)
FORMAT = "source32-bernstein-v1"


def add(a, b, factor=1):
    out = a[:] + [0] * max(0, len(b) - len(a))
    for i, value in enumerate(b):
        out[i] += factor * value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def scale(a, factor):
    return [factor * x for x in a]


def linear_power(slope, degree):
    return [comb(degree, i) * slope**i for i in range(degree + 1)]


def obstruction(n, k):
    """q^2 times the beta-eliminated obstruction polynomial."""
    aa = linear_power(1, D)
    bb = linear_power(1, k)
    cc = linear_power(n, k)
    dd = [0] * k + [n**k]
    ww = [0] * D + [1]
    first = multiply(add(scale(aa, Q), [-P]), add(scale(bb, Q), dd, -P))
    second = multiply(add(scale(cc, P), [-Q]), add(scale(aa, P), ww, -Q))
    return add(scale(first, n), second, -1)


def interval(n):
    return W_LO, Fraction(1, max(1, n - 1))


@lru_cache(maxsize=None)
def binomial_data(m):
    rows = [[comb(i, j) for j in range(i + 1)] for i in range(m + 1)]
    common = lcm(*(comb(m, j) for j in range(m + 1)))
    weights = [common // comb(m, j) for j in range(m + 1)]
    return rows, common, weights


def bernstein_integer_vector(poly, left, right):
    """Return a positive common scale times all Bernstein coefficients.

    Let m=degree(poly), a=A/R, b=B/R, and L=lcm(binomial(m,j)).
    Returned vector is L*R^m times the degree-m Bernstein vector on [a,b].
    """
    m = len(poly) - 1
    r = lcm(left.denominator, right.denominator)
    a = left.numerator * (r // left.denominator)
    b = right.numerator * (r // right.denominator)
    delta = b - a
    assert delta > 0
    rows, common, weights = binomial_data(m)
    ap = [a**i for i in range(m + 1)]
    rp = [r**i for i in range(m + 1)]
    dp = [delta**i for i in range(m + 1)]
    power = [
        dp[j] * sum(poly[i] * rows[i][j] * ap[i - j] * rp[m - i]
                    for i in range(j, m + 1))
        for j in range(m + 1)
    ]
    return [sum(power[j] * rows[i][j] * weights[j] for j in range(i + 1))
            for i in range(m + 1)]


def halve(vector):
    """Integer de Casteljau midpoint subdivision, with positive rescaling."""
    m = len(vector) - 1
    rows = [vector]
    for depth in range(1, m + 1):
        old = rows[-1]
        rows.append([old[i] + old[i + 1] for i in range(len(old) - 1)])
    left = [rows[j][0] << (m - j) for j in range(m + 1)]
    right = [rows[m - j][j] << j for j in range(m + 1)]
    return left, right


def vector_digest(vector):
    return sha256(("\n".join(map(str, vector)) + "\n").encode("ascii")).hexdigest()


def leaf_record(code, vector):
    return {"path": code, "maximum": str(max(vector)),
            "vector_sha256": vector_digest(vector)}


def certify(vector, code="", depth_limit=20):
    if max(vector) < 0:
        return [leaf_record(code, vector)]
    if len(code) >= depth_limit:
        raise ArithmeticError(f"strict sign not certified at depth {depth_limit}: {code}")
    left, right = halve(vector)
    return certify(left, code + "0", depth_limit) + certify(right, code + "1", depth_limit)


def fraction_pair(value):
    return [value.numerator, value.denominator]


def generate():
    records = []
    for n in range(1, N_MAX + 1):
        for k in range(1, D + 1):
            a, b = interval(n)
            poly = obstruction(n, k)
            leaves = certify(bernstein_integer_vector(poly, a, b))
            records.append({"n": n, "k": k, "degree": len(poly) - 1,
                            "interval": [fraction_pair(a), fraction_pair(b)],
                            "leaves": leaves})
    leaf_count = sum(len(record["leaves"]) for record in records)
    max_depth = max(len(leaf["path"]) for record in records for leaf in record["leaves"])
    return {"format": FORMAT, "d": D, "t": fraction_pair(T), "n_max": N_MAX,
            "w_lower": fraction_pair(W_LO), "records": records,
            "summary": {"polynomials": len(records), "leaves": leaf_count,
                        "maximum_subdivision_depth": max_depth}}


def verify_tree(vector, leaves, code="", used=None):
    if used is None:
        used = set()
    if code in leaves:
        leaf = leaves[code]
        if max(vector) >= 0:
            raise AssertionError(f"nonnegative Bernstein coefficient at leaf {code!r}")
        assert leaf["maximum"] == str(max(vector)), "frozen maximum mismatch"
        assert leaf["vector_sha256"] == vector_digest(vector), "frozen vector mismatch"
        used.add(code)
        return used
    assert len(code) < 20, "missing leaf or excessive depth"
    left, right = halve(vector)
    verify_tree(left, leaves, code + "0", used)
    verify_tree(right, leaves, code + "1", used)
    return used


def horner(poly, x):
    result = 0
    for coefficient in reversed(poly):
        result = result * x + coefficient
    return result


def check_identities():
    # Independent literal evaluation guards the expanded elimination formula.
    for n, k, w in [(1, 1, Fraction(1, 55)), (3, 17, Fraction(1, 5)),
                    (55, 32, Fraction(1, 54)), (2, 32, Fraction(1))]:
        aa, bb, cc, dd, ww = (1 + w)**D, (1 + w)**k, (1 + n*w)**k, (n*w)**k, w**D
        literal = n*(Q*aa - P)*(Q*bb - P*dd) - (P*cc - Q)*(P*aa - Q*ww)
        assert horner(obstruction(n, k), w) == literal
    # Independently evaluate the Bernstein identity at rational coordinates.
    poly = [2, -3, 5, -7]
    a, b = Fraction(1, 7), Fraction(4, 5)
    vec = bernstein_integer_vector(poly, a, b)
    m = len(poly) - 1
    r = lcm(a.denominator, b.denominator)
    common = lcm(*(comb(m, j) for j in range(m + 1)))
    for x in [Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(1)]:
        value = sum(vec[j]*comb(m, j)*x**j*(1-x)**(m-j) for j in range(m+1))
        assert value == common*r**m*horner(poly, a + (b-a)*x)
    lvec, rvec = halve(vec)
    for x in [Fraction(0), Fraction(2, 7), Fraction(1)]:
        lval = sum(lvec[j]*comb(m,j)*x**j*(1-x)**(m-j) for j in range(m+1))
        rval = sum(rvec[j]*comb(m,j)*x**j*(1-x)**(m-j) for j in range(m+1))
        factor = 2**m*common*r**m
        assert lval == factor*horner(poly, a + (b-a)*x/2)
        assert rval == factor*horner(poly, a + (b-a)*(1+x)/2)


def verify(certificate):
    assert certificate["format"] == FORMAT
    assert certificate["d"] == D
    assert certificate["t"] == fraction_pair(T)
    assert certificate["n_max"] == N_MAX
    assert certificate["w_lower"] == fraction_pair(W_LO)
    assert (1 + W_LO)**D < T, "analytic finite-n reduction failed"
    check_identities()
    records = certificate["records"]
    expected = [(n, k) for n in range(1, N_MAX+1) for k in range(1, D+1)]
    assert [(record["n"], record["k"]) for record in records] == expected
    leaf_count = max_depth = 0
    for record in records:
        n, k = record["n"], record["k"]
        poly = obstruction(n, k)
        a, b = interval(n)
        assert record["degree"] == len(poly) - 1
        assert record["interval"] == [fraction_pair(a), fraction_pair(b)]
        listed = record["leaves"]
        assert listed, "empty interval cover"
        leaves = {leaf["path"]: leaf for leaf in listed}
        assert len(leaves) == len(listed), "duplicate leaf"
        assert all(set(code) <= {"0", "1"} for code in leaves)
        used = verify_tree(bernstein_integer_vector(poly, a, b), leaves)
        assert used == set(leaves), "overlap or unreachable interval leaf"
        leaf_count += len(leaves)
        max_depth = max(max_depth, *(len(code) for code in leaves))
    summary = {"polynomials": len(records), "leaves": leaf_count,
               "maximum_subdivision_depth": max_depth}
    assert certificate["summary"] == summary
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--generate", type=Path, metavar="NEW_PATH")
    args = parser.parse_args()
    started = time.monotonic_ns()
    if args.generate:
        if args.generate.exists():
            parser.error("refusing to overwrite a frozen certificate")
        certificate = generate()
        verify(certificate)
        args.generate.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
        action = "GENERATED AND VERIFIED"
    else:
        certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
        verify(certificate)
        action = "VERIFIED"
    print(json.dumps({"result": action, "claim": "F_32 <= 89/50",
                      **certificate["summary"],
                      "arithmetic": "Python exact integers/Fraction; no floats",
                      "elapsed_milliseconds": (time.monotonic_ns() - started) // 1_000_000}, indent=2))


if __name__ == "__main__":
    main()
