"""Attack one explicit general candidate, not Q-CAG-HALF directly.

SAIC: m max_T J_T(z) + B(z) <= 2 W(z) for every complete pure SPE,
where J_T=sum_{x in T}1/(1+c_x), B=sum_x c_x/(1+c_x).
Only previously frozen strategy cones are used; no fixed-size theorem is claimed.
"""
from pathlib import Path
import importlib.util
import json
from fractions import Fraction as F
import sys

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("cone_audit", ROOT / "tests/audits/customer_attraction_strategy_lp.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
import numpy as np
from scipy.optimize import linprog


def main():
    source = ROOT / "evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json"
    frozen = json.loads(source.read_text())
    p, m = frozen["parameters"]["topics"], frozen["parameters"]["players"]
    best = None
    solved = 0
    for idx, entry in enumerate(frozen["cone_proofs"]):
        actions = {tuple(row["history"]): row["action"] for row in entry["actions"]}
        cone = mod.StrategyCone(p, m, actions)
        for query in range(p):
            objective = []
            for mask in range(1, 1 << p):
                c = sum(cone.root[a] for a in range(p) if mask & (1 << a))
                objective.append(F(m * bool(mask & (1 << query)) + c, 1 + c) - 2 * bool(c))
            result = linprog(-np.array(objective, dtype=float), A_ub=-cone.matrix,
                             b_ub=np.zeros(len(cone.rows)), A_eq=np.array([cone.welfare], dtype=float),
                             b_eq=[1], bounds=(0, None), method="highs")
            if not result.success:
                raise RuntimeError(result.message)
            values = tuple(F(float(x)).limit_denominator(10**7) for x in result.x)
            if not (cone.verify(values) and mod.dot(cone.welfare, values) == 1):
                values = cone.recover_vertex(result.x)
            if values is None or not cone.verify(values) or mod.dot(cone.welfare, values) != 1:
                continue
            solved += 1
            value = mod.dot(objective, values)
            if best is None or value > F(best["normalized_excess"]):
                clones = mod.integer_clones(values)
                assert mod.independently_verify(cone, clones)
                best = dict(cone_index=idx, query=query, normalized_excess=str(value),
                            clones=clones, root_counts=cone.root, actions=entry["actions"],
                            all_history_exact_verified=True)
    output = dict(candidate="SAIC", source=str(source.relative_to(ROOT)),
                  universal_bound_proved=False, exact_feasible_lp_candidates=solved,
                  candidate_refuted=F(best["normalized_excess"]) > 0, best=best)
    dest = Path(__file__).with_name("attack_actual_insertion.json")
    dest.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "best"}, indent=2))
    print({k: v for k, v in best.items() if k != "actions"})


if __name__ == "__main__":
    main()
