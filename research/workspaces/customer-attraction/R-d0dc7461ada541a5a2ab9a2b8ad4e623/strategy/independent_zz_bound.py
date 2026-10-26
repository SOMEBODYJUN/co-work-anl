"""Independent exact review of one Z-to-Z obstruction at the saved 3889 point.

This reads frozen data only. It does not import either the author's row
generator or the parent's diagnostic. For distinct i,j,l, the source reply
is e=(B,i,j), the query reply is f=(C,i,l). Each true terminal IC is

    E[(Z_e-Z_f)/(a+R_e+1)] >= 0.

The own four-state marginal fixes E[R_e Z_e]. The only unfixed term has a
positive coefficient and is bounded by min(E[R_e], E[Z_f]). A negative sum
of these upper bounds rules out every joint extension of the saved local
marginals, without assuming a threshold coupling or joint attainability.

The class sums over all distinct triples, hence is invariant under the
stabilizer of the old word histogram. Any putative extension can be
averaged over that stabilizer; its per-label local marginals then equal
the stored orbit marginals. No claim that same-orbit bits are identical
is needed. This excludes one saved point, not every half-violating point
of an enlarged system, and is neither a game nor an SPE counterexample.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / (
    "research/workspaces/customer-attraction/"
    "R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/"
    "attractive_nested_exact.json"
)
EXPECTED_SHA256 = "cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1"
EXPECTED_BOUND = Fraction(
    -77805114978912902524965135501273065957,
    176731722247831414031521292083980140160,
)


def main():
    raw = SOURCE.read_bytes()
    digest = sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA256
    data = json.loads(raw)
    blocks = []
    for column in data["columns"]:
        if column["kind"] == "hist":
            words = []
            for word, count in zip(product((0, 1), repeat=3), column["hist"]):
                words.extend([word] * count)
            assert len(words) == 6
            current = {
                "a": sum(map(int, column["actual_bits"][:4])),
                "mass": Fraction(column["weight"]),
                "words": words,
                "states": {},
            }
            blocks.append(current)
        elif column["kind"] == "joint-reply":
            family, diagonal, wi, wj = column["group"]
            key = family, diagonal, tuple(wi), tuple(wj)
            current["states"].setdefault(key, {})[tuple(column["state"])] = (
                Fraction(column["weight"])
            )

    upper_bound = Fraction(0)
    comparison_count = 0
    nonzero_histogram_contributions = 0
    for block in blocks:
        a, words, states = block["a"], block["words"], block["states"]
        for state in states.values():
            assert set(state) == {(0, 1), (1, 0), (1, 1)}
            assert min(state.values()) >= 0
            assert sum(state.values()) <= block["mass"]
        subtotal = Fraction(0)
        for i, j, ell in permutations(range(6), 3):
            source = states[0, 0, words[i], words[j]]
            query = states[1, 0, words[i], words[ell]]
            source_z = source[0, 1] + source[1, 1]
            source_r = source[1, 0] + source[1, 1]
            query_z = query[0, 1] + query[1, 1]
            denominator = (a + 1) * (a + 2)
            subtotal += (source_z - query_z) / (a + 1)
            subtotal -= source[1, 1] / denominator
            subtotal += min(source_r, query_z) / denominator
            comparison_count += 1
        upper_bound += subtotal
        nonzero_histogram_contributions += bool(subtotal)

    assert upper_bound == EXPECTED_BOUND
    assert upper_bound < 0
    print(json.dumps({
        "scope": "One saved four-state marginal point has no joint extension satisfying the specified Z-to-Z IC class; no whole-system or SPE claim",
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": digest,
        "class": {"source_family": 0, "query_family": 1, "index_partition": [0, 1, 0, 2]},
        "histograms": len(blocks),
        "labelled_comparisons": comparison_count,
        "nonzero_histogram_contributions": nonzero_histogram_contributions,
        "unrestricted_joint_upper_bound": str(upper_bound),
        "strictly_negative": upper_bound < 0,
        "matches_parent_diagnostic": upper_bound == EXPECTED_BOUND,
    }, indent=2))


if __name__ == "__main__":
    main()
