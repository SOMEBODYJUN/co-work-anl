#!/usr/bin/env python3
"""Independent explicit path/OPT/breakpoint check of the finite PAY DAG."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver

spec = importlib.util.spec_from_file_location(
    "pay_dag_under_review", Path(__file__).parents[1] / "pay" / "all_path_pay.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def explicit_value(inst):
    m, q = inst.players, inst.topic_count
    counts = {inst.counts(h) for h in product(range(q), repeat=m)}
    opt = max(map(inst.welfare, counts))
    opts = [d for d in counts if inst.welfare(d) == opt]
    answer, paths = None, 0
    for path in ExactSPESolver(inst).ordered_outcomes():
        u = inst.player_payoffs(path)
        prefix, early = [0] * q, F(0)
        path_min = None
        for i in range(m - 1):
            k = m - i
            for d in opts:
                types = []
                points = {F(0), F(4)}
                for client in inst.customers:
                    b = sum(prefix[a] for a in client.topics)
                    z = sum(d[a] for a in client.topics)
                    if not z:
                        continue
                    types.append((client.multiplicity, b, z))
                    points.add(F(4*m*(b+1), z*(k-1)+m*(b+1)))
                for t in points:
                    charge = sum((w * (1 - F(2*(k-2)*z, m*(b+k))
                        - min(t*z/(m*(b+1)), (t*z/m+4-t)/(b+k)))
                        for w, b, z in types), F(0))
                    margin = charge - 2*early
                    path_min = margin if path_min is None else min(path_min, margin)
            prefix[path[i]] += 1
            early += u[i]
        paths += 1
        answer = path_min if answer is None else max(answer, path_min)
    return answer, paths, len(opts)


def main():
    cases = [
        Instance.from_topic_sets([set(), set(), set()], players=4),
        Instance.from_topic_sets([{0, 1, 2}, {1, 3}, {2, 3, 4}], players=3),
        Instance.from_topic_sets([{0, 1}, {1, 2}, {0, 2, 3}], players=4),
    ]
    report = []
    for inst in cases:
        brute, paths, opts = explicit_value(inst)
        dag = module.inspect_instance(inst)
        assert F(dag['max_over_SPE_paths_min_over_prefix_opt_t']) == brute
        report.append({"m": inst.players, "topics": inst.topic_count,
                       "all_ordered_SPE_paths": paths, "optimal_counts": opts,
                       "literal_breakpoint_and_DAG_value": str(brute)})
    print(json.dumps({"status": "passed", "cases": report,
        "scope": "Finite implementation audit only; not a general PAY proof."}, indent=2))


if __name__ == '__main__':
    main()
