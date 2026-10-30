"""Replay the frozen full-root certificate and verify the legal-background family.

Original programs execute unchanged in temporary copies. The parameter-family
check clears all symbolic denominators and compares rational polynomial
coefficients, rather than inferring an all-p statement from finite samples.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
REL = Path("research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11")
D = [F(4), F(6), F(2)]  # 2(p+1)(p+2)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def neg(a):
    return [-x for x in a]


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def strings(p):
    return list(map(str, trim(p)))


def symbolic_family():
    # Each list gives constant, p, p^2 coefficients of a type multiplicity.
    weights = {
        1: [4, 5, 1], 2: [5, 6, 1],
        4: [3, 2], 8: [3, 2],
        20: [2], 24: [2], 36: [2], 40: [2],
        49: [2, 3, 1], 50: [2, 3, 1],
    }
    occupied = {1, 2, 49, 50}
    a, b = [F(6), F(2)], [F(7), F(2)]
    refs = [
        ["aa", b, b, b, b, b],
        [a, "bb", b, b, b, b],
        [a, b, "half-b", b, b, b],
        [a, b, b, "half-b", b, b],
        [[5, 2], a, a, a, [4, 2], a],
        [[5, 2], a, a, a, a, [4, 2]],
    ]
    reply = [1, 4, 4, 4, 5, 4]  # B,R,R,R,S,R
    raw_numerators = []
    rows = []
    for first in range(6):
        values = []
        for last in range(6):
            numerator = [F(0)]
            for mask, weight in weights.items():
                if not mask & (1 << last):
                    continue
                load = 1 + bool(mask & (1 << first))
                if mask in occupied:
                    quotient = [4, 2] if load == 1 else [2, 2]
                else:
                    quotient = [x / load for x in D]
                numerator = add(numerator, mul(weight, quotient))
            expected = refs[first][last]
            if expected == "aa":
                target = mul(mul([1, 1], a), [2, 2])
            elif expected == "bb":
                target = mul(mul([1, 1], b), [2, 2])
            elif expected == "half-b":
                target = mul(b, [x/2 for x in D])
            else:
                target = mul(expected, D)
            assert trim(numerator) == trim(target), (first, last, numerator, target)
            values.append(numerator)
        chosen = values[reply[first]]
        gaps = [add(chosen, neg(value)) for value in values]
        assert all(all(c >= 0 for c in gap) for gap in gaps)
        raw_numerators.append(values)
        rows.append({
            "first": first, "chosen_reply": reply[first],
            "six_payoff_numerators": [strings(v) for v in values],
            "six_chosen_minus_alternative_numerators": [strings(v) for v in gaps],
        })
    first_numerators = [raw_numerators[reply[x]][x] for x in range(6)]
    assert all(trim(x) == mul(a, D) for x in first_numerators)
    total = [F(0)]
    for weight in weights.values():
        total = add(total, weight)
    assert total == list(map(F, [27, 21, 4]))
    # For p>=1, only masks outside 'occupied' are fresh.
    fresh = [F(0)]
    for mask, weight in weights.items():
        if mask not in occupied:
            fresh = add(fresh, weight)
    assert fresh == list(map(F, [14, 4]))
    assert add(add(a, b), neg(fresh)) == [F(-1)]
    return {
        "status": "PASS", "domain": "all integer p>=0 for tail SPE; p>=1 for zero-new-coverage failure",
        "common_positive_denominator_coefficients": strings(D),
        "coefficient_order": "constant, p, p^2, ...",
        "client_count_coefficients": strings(total),
        "last_reply_rows": rows,
        "first_deviation_numerators": [strings(x) for x in first_numerators],
        "all_36_payoff_identities_coefficientwise_equal": True,
        "all_36_last_reply_gap_numerators_coefficientwise_nonnegative": True,
        "all_6_first_deviations_equal_to_2p_plus_6": True,
        "fresh_optimum_p_at_least_1_coefficients": strings(fresh),
        "tail_profit_coefficients": strings(add(a, b)),
        "GLOBAL_gap_p_at_least_1": "-1",
        "root_reachability_proved_in_original_programs": "p=1 only, by the supplied full-root certificate",
        "supplemental_p2_p3_checks": "finite_parameters.py separately constructs and verifies the two finite root policies; no all-p claim",
    }


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=BASE/"replay")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BASE/"source-manifest.json").read_text())
    for row in manifest["primary_sources"] + manifest["reused_runtime_dependencies"]:
        raw = (BASE/row["preserved_relative_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["id"]
    repo = next(p for p in BASE.parents if (p/"work.py").is_file())
    workspace = repo/"cleanup/workspaces/Boss2"
    checks = {}
    for program, outputs, label in [
        (REL/"background/global_actual_prefix_audit.py",
         [REL/"background"/name for name in (
             "global_actual_prefix_instance.json",
             "global_actual_prefix_complete_spe.json",
             "global_actual_prefix_audit.json")], "author"),
        (REL/"parent/audit_actual_prefix_independent.py",
         [REL/"parent/actual_prefix_independent_audit.json"], "independent"),
    ]:
        with tempfile.TemporaryDirectory(prefix="actual-prefix-replay-", dir=workspace) as name:
            stage = Path(name)/"original"
            shutil.copytree(BASE/"original", stage)
            result = subprocess.run([sys.executable, str(stage/program)],
                                    cwd=stage, capture_output=True, text=True, check=True)
            write(out/(label+"-stdout.json"), json.loads(result.stdout))
            for relative in outputs:
                frozen = (BASE/"original"/relative).read_bytes()
                regenerated = (stage/relative).read_bytes()
                assert json.loads(regenerated) == json.loads(frozen), str(relative)
                assert regenerated == frozen, str(relative)
                (out/label).mkdir(exist_ok=True)
                (out/label/relative.name).write_bytes(regenerated)
                checks[str(relative)] = {
                    "all_fields_equal": True, "byte_identical": True,
                    "sha256": hashlib.sha256(regenerated).hexdigest(),
                }
    family = symbolic_family()
    write(out/"symbolic-family.json", family)
    certificate = json.loads((BASE/"original"/REL/"background/global_actual_prefix_complete_spe.json").read_text())
    policy = {tuple(row["history"]): row["action"] for row in certificate["actions"]}
    manual_reply = [1, 4, 4, 4, 5, 4]
    actual_reply = [policy[(0, 1, a)] for a in range(6)]
    assert actual_reply == [1, 5, 5, 5, 5, 4]
    summary = {
        "status": "PASS", "primary_source_hashes": len(manifest["primary_sources"]),
        "reused_dependency_hashes": len(manifest["reused_runtime_dependencies"]),
        "frozen_outputs": checks,
        "full_root_ordered_nodes": 259, "comparisons_including_self": 1554,
        "nonself_comparisons": 1295,
        "manual_tail_last_replies": manual_reply,
        "root_certificate_tail_last_replies": actual_reply,
        "manual_tail_and_root_certificate_not_identical_off_path": True,
        "difference": "After AB followed by B,T,Q, manual tail chooses R; full-root certificate chooses S. Both are exact best replies and give the same first-player payoff.",
        "symbolic_family": "all 36 rational payoff identities and weak inequalities verified by polynomial coefficients",
        "GLOBAL_failure_on_actual_root_prefix": {"p": 1, "P": 17, "Delta": 0, "freshOPT2": 18},
        "supplemental_finite_parameters": "See finite_parameters.py and replay/finite-parameters; supplied frozen audit programs themselves concern p=1.",
        "not_performed": ["No new proof of full-root reachability for every p.",
                          "No new general welfare or safety-bridge claim."],
    }
    write(out/"semantic-reconciliation.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
