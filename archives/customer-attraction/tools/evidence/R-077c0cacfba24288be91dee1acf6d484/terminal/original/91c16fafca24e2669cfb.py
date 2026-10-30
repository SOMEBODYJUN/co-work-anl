"""Search the fractional deficit bridge on attached repository example instances."""

from pathlib import Path
import sys
import json
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver


def price_value(inst, t):
    q, n = inst.topic_count, len(inst.customers)
    objective = np.array([float(t)]*q+[-c.multiplicity for c in inst.customers])
    rows = []
    for i, c in enumerate(inst.customers):
        row = [float(-int(j in c.topics)) for j in range(q)]+[0.0]*n
        row[q+i] = 1.0
        rows.append(row)
    return linprog(objective, A_ub=rows, b_ub=[0.0]*n,
                   bounds=[(0, None)]*q+[(0, 1)]*n, method="highs")


def main():
    root = Path(__file__).resolve().parents[5]
    instances = outcomes = 0
    best_slack = None
    details = []
    for path in sorted((root/"examples/customer_attraction").glob("*.json")):
        try:
            inst = Instance.from_dict(json.loads(path.read_text()))
        except (KeyError, ValueError, TypeError):
            continue
        if not 2 <= inst.players <= 6 or inst.topic_count > 8:
            continue
        inst_outcomes = 0
        for counts in ExactSPESolver(inst).outcomes():
            W = inst.welfare(counts)
            u = inst.topic_payoffs(counts)
            minimum = min(val for val, count in zip(u, counts) if count)
            res = price_value(inst, minimum)
            assert res.status == 0
            slack = W+res.fun
            outcomes += 1
            inst_outcomes += 1
            if best_slack is None or slack < best_slack:
                best_slack = slack
            if slack < -1e-7:
                result = {"status": "floating counterexample candidate", "file": str(path),
                          "counts": counts, "W": W, "u_min": str(minimum),
                          "B": -res.fun, "query_z": res.x[:inst.topic_count].tolist()}
                Path(__file__).with_name("existing_price_counterexample_candidate.json").write_text(
                    json.dumps(result, indent=2)+"\n")
                print(json.dumps(result, indent=2))
                return
        instances += 1
        details.append({"file": path.name, "outcomes": inst_outcomes})
    report = {"status": "no price bridge counterexample in specified existing examples",
              "instances": instances, "outcomes": outcomes, "minimum_float_slack": best_slack,
              "details": details}
    Path(__file__).with_name("existing_price_probe_report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
