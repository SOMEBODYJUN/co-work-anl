"""Finite search for OPT <= W + m*u_i, a candidate strictly beyond the tail."""

from pathlib import Path
import sys
import random
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def main():
    rng = random.Random(202610211407)
    checked = outcomes = 0
    for m, q, runs in [(4, 7, 300), (5, 8, 300), (6, 8, 300)]:
        for run in range(runs):
            weights = {}
            for _ in range(rng.randrange(3, 3*q)):
                mask = sum(1 << t for t in rng.sample(range(q), rng.choices([1,2,3], [5,4,1])[0]))
                weights[mask] = weights.get(mask, 0)+rng.randrange(1, 11)
            inst = Instance(tuple(map(str, range(q))), tuple(
                CustomerType(frozenset(j for j in range(q) if mask >> j & 1), weight)
                for mask, weight in weights.items()), m)
            opt = inst.optimal_welfare()
            solver = ExactSPESolver(inst)
            for counts in solver.outcomes():
                W = inst.welfare(counts)
                utilities = inst.topic_payoffs(counts)
                minimum = min(u for c, u in zip(counts, utilities) if c)
                outcomes += 1
                if opt > W+m*minimum:
                    cert = solver.certificate(counts)
                    verified = verify_certificate(inst, cert)
                    assert verified.valid
                    result = {
                        "candidate": "OPT <= W + m*u_i for every player",
                        "status": "counterexample found",
                        "instance": inst.to_dict(), "counts": counts,
                        "ordered_actual": verified.terminal_history,
                        "W": W, "OPT": opt, "min_u": str(minimum),
                        "bridge_gap": str(opt-W-m*minimum),
                        "certificate": cert.to_dict(),
                        "checked_instances": checked+1, "checked_outcomes": outcomes,
                    }
                    out = Path(__file__).with_name("individual_deficit_counterexample.json")
                    out.write_text(json.dumps(result, indent=2)+"\n")
                    print(json.dumps({key: result[key] for key in result if key != "certificate"}, indent=2))
                    return
            checked += 1
        print(json.dumps({"completed_m": m, "checked_instances": checked,
                          "checked_outcomes": outcomes}), flush=True)
    print(json.dumps({"status": "no counterexample in finite search", "checked_instances": checked,
                      "checked_outcomes": outcomes}), flush=True)


if __name__ == "__main__":
    main()
