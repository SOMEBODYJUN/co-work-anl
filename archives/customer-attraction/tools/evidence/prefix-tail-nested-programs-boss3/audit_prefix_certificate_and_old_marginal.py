"""Independent rational readback from raw S/Z/V and the consumed old margins.

No frozen program is imported. The prefix certificate is checked on every
literal (actual bits, comparison count, reply count, aligned intersection)
state in its conditional domain. Only the K and hist records consumed by
lift_old_point are audited from that separate old input, not its 1033 rows.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
OLD = HERE / "original/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json"


def share(bit, load):
    return F(bit, load) if bit else F(0)


def check_prefix(record):
    threshold = record["min_a_load"]
    coefficients = {name: F(value) for name, value in record["coefficients"].items()}
    assert all(value >= 0 for value in coefficients.values())
    literal = 0
    projected = set()
    minimum = None
    zero = 0
    witness = None
    for actual in product((0, 1), repeat=6):
        prefix = sum(actual[:4])
        a, b = actual[-2:]
        if a and prefix < threshold:
            continue
        load = sum(actual)
        utilities = [share(bit, load) for bit in actual]
        for d, ell in product(range(7), repeat=2):
            for intersection in range(max(0, d + ell - 6), min(d, ell) + 1):
                denominator = (prefix + 1) * (prefix + 2)
                # Literal true-query rows, before cancellation of the aligned
                # intersection between the six compared topics and replies.
                s = 6 * utilities[4] - F(d, prefix + 1) + F(intersection, denominator)
                z = 6 * utilities[5] - F(ell, prefix + a + 1)
                v = F(d * ell - 6 * intersection, denominator)
                rows = {"G": s + z / 12 + v / 6}
                for i in range(6):
                    denominator_i = 6 - i + sum(actual[:i])
                    for j in range(6):
                        rows[f"floor:{i+1}:{j+1}"] = utilities[i] - F(actual[j], denominator_i)
                    rows[f"optfloor:{i+1}"] = 6 * utilities[i] - F(d, denominator_i)
                residual = 2 * int(load > 0) - int(d > 0) - sum(coefficients[name] * rows[name] for name in coefficients)
                if minimum is None or residual < minimum:
                    minimum = residual
                    witness = {"actual_bits": "".join(map(str, actual)), "d": d, "ell": ell, "intersection": intersection}
                assert residual >= 0, (threshold, actual, d, ell, intersection, residual)
                literal += 1
                zero += residual == 0
                projected.add((actual, d, ell))
    assert len(projected) == record["states"]
    assert minimum == F(record["minimum"])
    assert record["negative_count"] == 0 and record["negative_examples"] == []
    return {"threshold": threshold, "coefficients": {k: str(v) for k, v in coefficients.items()},
            "projected_states": len(projected), "literal_states_with_intersection": literal,
            "minimum_residual": str(minimum), "zero_literal_states": zero, "minimum_witness": witness,
            "interpretation": "complete coefficient proof for this conditional domain, together with true-row semantics"}


def old_marginal():
    raw = OLD.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == "24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11"
    data = json.loads(raw)
    cells = defaultdict(F)
    k = F(0)
    hist = 0
    k_records = 0
    for column in data["columns"]:
        if column["kind"] == "K":
            value = F(column["weight"])
            assert value >= 0
            k += value
            k_records += 1
        elif column["kind"] == "hist":
            hist += 1
            bits = column["actual_bits"]
            d = column["d"]
            value = F(column["weight"])
            assert len(bits) == 6 and set(bits) <= {"0", "1"}
            assert isinstance(d, int) and 0 <= d <= 6 and value >= 0
            if value:
                cells[(bits, d)] += value
    w = sum(value for (bits, _), value in cells.items() if "1" in bits)
    o = sum(value for (_, d), value in cells.items() if d > 0)
    assert w == F(data["W"])
    assert hist == 16 and k_records == 1 and len(cells) == 8
    return {"input_sha256": hashlib.sha256(raw).hexdigest(), "input_bytes": len(raw),
            "total_input_columns": len(data["columns"]), "hist_records_read": hist,
            "K_records_read": k_records, "K": str(k), "W": str(w), "O": str(o),
            "positive_marginal_cells": [{"actual_bits": bits, "d": d, "weight": str(value)} for (bits, d), value in sorted(cells.items())],
            "scope": "only the consumed K/hist margin; the other 194 reply columns and original 1033 inequalities are not reverified"}


def main():
    reports = json.loads((HERE / "runs/prefix_floor_lp.stdout.json").read_text())
    certified = [check_prefix(record) for record in reports if "coefficients" in record]
    assert [record["threshold"] for record in certified] == [3, 4]
    out = {"status": "passed", "prefix_certificates": certified,
           "unverified_float_infeasibility_thresholds": [record["min_a_load"] for record in reports if "coefficients" not in record],
           "old_margin": old_marginal()}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
