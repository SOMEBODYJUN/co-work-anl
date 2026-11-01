"""Finite exact checks of a symbolic maximal-catalog bridge obstruction."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import ExactSPESolver, Instance, verify_certificate


def build(k, full):
    groups = [{3 * i, 3 * i + 1} for i in range(k)]
    b, d = 3 * k, 3 * k + 1
    sets = [x | {3 * i + 2} for i, x in enumerate(groups)]
    labels = [f"A{i + 1}" for i in range(k)]
    sets += [x | {b} for x in groups]
    labels += [f"B{i + 1}" for i in range(k)]
    if full:
        sets += groups
        labels += [f"C{i + 1}" for i in range(k)]
    sets.append({b, d})
    labels.append("D")
    return Instance.from_topic_sets(sets, players=k + 1, labels=tuple(labels))


def check(k, certificate_limit):
    out = {"k": k, "players": k + 1, "predicted_opt": 3 * k + 2}
    for full in [False, True]:
        tag = "full" if full else "maximal"
        instance = build(k, full)
        solver = ExactSPESolver(instance)
        optimum = instance.optimal_welfare()
        minimum = solver.minimum_welfare()
        assert optimum == 3 * k + 2
        row = {"opt": optimum, "minimum_SPE_welfare": minimum,
               "outcome_count": len(solver.outcomes())}
        if full:
            path = tuple(range(2 * k, 3 * k)) + (3 * k,)
            target = instance.counts(path, terminal=True)
            assert target in solver.outcomes()
            assert instance.welfare(target) == 2 * k + 2
            row["designated_path"] = list(path)
            row["designated_welfare"] = 2 * k + 2
        else:
            assert minimum == 3 * k + 1
            predicted = set()
            for extra in range(k, 2 * k + 1):
                counts = [1] * k + [0] * (k + 1)
                counts[extra] = 1
                predicted.add(tuple(counts))
            assert solver.outcomes() == frozenset(predicted)
            path = (k,) + tuple(range(1, k)) + (0,)
            target = instance.counts(path, terminal=True)
            assert target in solver.outcomes()
            assert instance.welfare(target) == 3 * k + 1
            row["designated_path"] = list(path)
            row["designated_welfare"] = 3 * k + 1
        if k <= certificate_limit:
            certificate = solver.certificate(on_path=path)
            report = verify_certificate(instance, certificate)
            report.assert_valid()
            row["full_ordered_history_certificate_verified"] = True
            row["decision_histories"] = len(certificate.actions)
        out[tag] = row
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, default=4)
    parser.add_argument("--certificate-limit", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"status": "finite_exact_verification_only",
              "symbolic_proof": "maximal_catalog_boundary.md",
              "checks": [check(k, args.certificate_limit)
                         for k in range(1, args.max_k + 1)]}
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(payload)
    else:
        print(payload, end="")
