"""针对冻结实际选择器的集成审计；原矩阵OPT oracle由本文件独立枚举。

本文件显式导入被测选择器；independent_first_move.py则完全不导入它。
"""
from fractions import Fraction as F
from itertools import product
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import hashlib
import json
import sys


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: frozen_selector_fullp_audit.py CANONICAL_SELECTOR_PATH")
    code = Path(sys.argv[1]).resolve()
    spec = spec_from_file_location("frozen_canonical_selector", code)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    values = (F(0), F(1, 2), F(1), F(3, 2), F(2), None)
    columns = [c for c in product(values, repeat=2) if any(x is not None for x in c)]
    counts = {"matrices": 0, "pruned_initial_schedules": 0,
              "DONE": 0, "MOVE": 0, "NO_T_SCHEDULE": 0,
              "nonpruned_matrices": 0}
    for n in range(3):
        for cols in product(columns, repeat=n):
            P = [[cols[j][i] for j in range(n)] for i in range(2)]
            counts["matrices"] += 1
            counts["nonpruned_matrices"] += any(
                x is not None and x > 1 for row in P for x in row)
            owner_options = [tuple(i for i in range(2) if P[i][j] is not None)
                             for j in range(n)]
            legal = list(product(*owner_options))

            def load(assignment):
                out = [F(0), F(0)]
                for j, i in enumerate(assignment):
                    out[i] += P[i][j]
                return out

            # Full original P, including processing times >T, enters this oracle.
            optimum = min(max(load(a)) for a in legal)
            for sigma in legal:
                L = load(sigma)
                if max(L) > 2 or any(P[i][j] > 1 for j, i in enumerate(sigma)):
                    continue
                counts["pruned_initial_schedules"] += 1
                C = max(F(1), max(L))
                U = max(F(2), C+F(1, 2))
                result = mod.first_step(P, sigma, F(1), C)
                counts[result["status"]] += 1
                if result["status"] == "NO_T_SCHEDULE":
                    assert optimum > 1
                elif result["status"] == "DONE":
                    assert max(load(result["assignment"])) <= 1
                else:
                    assert sum(i != j for i, j in
                               zip(sigma, result["assignment"])) == 1
                    assert max(load(result["assignment"])) <= U
                    assert all(P[i][j] <= 1 for j, i in
                               enumerate(result["assignment"]))
    print(json.dumps({
        "status": "all_checks_passed", "counts": counts,
        "arithmetic": "fractions.Fraction; T=1",
        "domain": "m=2,n=0..2,p in {0,1/2,1,3/2,2,infinity}",
        "selector_sha256": hashlib.sha256(code.read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Integration audit of one frozen selector, not an independent theorem proof."
    }, indent=2))


if __name__ == "__main__":
    main()
