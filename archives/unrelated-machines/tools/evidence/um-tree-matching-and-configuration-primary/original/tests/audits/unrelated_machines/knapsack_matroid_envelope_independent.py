"""Independent finite audit, not a proof of the universal statement.

Directly enumerates families on E={h,s_1,...,s_k}, retains those satisfying
all three independent-set matroid axioms and containing every weight<=1 set,
and exhausts unordered p-tuples (repetitions allowed) of retained families.
Integer weight units avoid numerical error. No matroid classification is used
by the enumerator; the classification is checked afterwards.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
import hashlib
import json
import platform
from pathlib import Path


def independent_sets(family_bits, n):
    return [s for s in range(1 << n) if family_bits >> s & 1]


def matroid_axioms(family_bits, n):
    if not family_bits & 1:
        return False
    indep = independent_sets(family_bits, n)
    for s in indep:
        for j in range(n):
            if s >> j & 1 and not (family_bits >> (s ^ (1 << j)) & 1):
                return False
    for a in indep:
        for b in indep:
            if a.bit_count() >= b.bit_count():
                continue
            if not any((b >> j & 1) and not (a >> j & 1)
                       and (family_bits >> (a | (1 << j)) & 1)
                       for j in range(n)):
                return False
    return True


def main():
    output = {
        "python": platform.python_version(),
        "method": "all family truth tables, direct matroid axioms, all unordered tuples with repetitions",
        "arithmetic": "integer weights in units of 1/k; Fraction output",
        "scope": "k=1..4; p=1..k+1",
        "limits": "finite exhaustive audit, no universal proof; no scheduling algorithm tested",
        "rows": [],
    }
    for k in range(1, 5):
        n = k + 1
        mandatory = sum(1 << s for s in range(1 << n)
                        if not (s & 1) or s == 1)
        optional = [2*t+1 for t in range(1, 1 << k)]
        matroids = []
        for choices in range(1 << len(optional)):
            family = mandatory
            for pos, s in enumerate(optional):
                if choices >> pos & 1:
                    family |= 1 << s
            if matroid_axioms(family, n):
                matroids.append(family)
        # Independently compare the resulting families to the predicted unique-circuit forms.
        full = (1 << (1 << n)) - 1
        predicted = {full}
        for a in range(1, 1 << k):
            circuit = 2*a+1
            predicted.add(sum(1 << s for s in range(1 << n)
                              if (s & circuit) != circuit))
        assert set(matroids) == predicted
        weights = [k*(s & 1) + (s >> 1).bit_count() for s in range(1 << n)]
        row = {"k": k, "truth_tables_examined": 1 << len(optional),
               "admissible_matroid_count": len(matroids), "p": []}
        for p in range(1, k+2):
            best = 2*k
            attaining = None
            tuple_count = 0
            for indices in combinations_with_replacement(range(len(matroids)), p):
                common = full
                for idx in indices:
                    common &= matroids[idx]
                value = max(weights[s] for s in range(1 << n) if common >> s & 1)
                if value < best:
                    best, attaining = value, indices
                tuple_count += 1
            expected = max(k, 2*k-p)
            assert best == expected, (k, p, best, expected)
            assert (2*k-best) == min(k,p)  # inverse check
            row["p"].append({"p":p,"tuples_examined":tuple_count,
                             "minimum_units":best,"D":str(Fraction(best,k)),
                             "attaining_tuple_indices":attaining})
        output["rows"].append(row)
    output["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
