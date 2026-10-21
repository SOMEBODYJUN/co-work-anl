"""Independent definition-level audit; no project solver imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "continuation_geometry" / "blind_input.json"

def main():
    obj = json.loads(SOURCE.read_text())
    ins = obj["instance"]
    prefix = obj["ordered_prefix"]
    p = len(ins["topics"])
    assert ins["players"] - len(prefix) == 2
    customers = [(frozenset(c["topics"]), c["multiplicity"])
                 for c in ins["customers"]]
    assert all(isinstance(w, int) and w > 0 for _, w in customers)
    assert len(set(frozenset(i for i, (B, w) in enumerate(customers) if a in B)
                   for a in range(p))) == p
    def utility(history, a):
        return sum((F(w, sum(t in B for t in history))
                    for B, w in customers if a in B), F(0))
    table = {}
    all_pairs = []
    for a, b in product(range(p), repeat=2):
        h = prefix + [a, b]
        first = utility(h, a)
        last = utility(h, b)
        table[a, b] = (first, last, first + last)
        all_pairs.append({"a": a, "b": b, "first": first,
                          "last": last, "profit": first + last})
    replies = {a: [b for b in range(p)
                   if table[a,b][1] == max(table[a,j][1] for j in range(p))]
               for a in range(p)}
    floors = {a: min(table[a,b][0] for b in replies[a]) for a in range(p)}
    threshold = max(floors.values())
    pure = [(table[a,b][2], a, b) for a in range(p) for b in replies[a]
            if table[a,b][0] >= threshold]
    pure_min = min(x[0] for x in pure)
    convex = [(z, a, [(b,F(1))]) for z,a,b in pure]
    for a in range(p):
        for lo, hi in product(replies[a], repeat=2):
            u0, _, z0 = table[a,lo]
            u1, _, z1 = table[a,hi]
            if u0 < threshold < u1:
                t = (threshold-u0)/(u1-u0)
                convex.append(((1-t)*z0+t*z1, a, [(lo,1-t),(hi,t)]))
    convex_min = min(x[0] for x in convex)
    optimal_mixtures = [x for x in convex if x[0] == convex_min]
    for z,a,mix in optimal_mixtures:
        assert sum(t for b,t in mix) == 1
        assert all(t >= 0 and b in replies[a] for b,t in mix)
        assert sum(t*table[a,b][0] for b,t in mix) >= threshold
        assert sum(t*table[a,b][2] for b,t in mix) == z
    report = {"source": str(SOURCE.relative_to(HERE.parent)),
              "prefix": prefix, "all_terminal_pairs": all_pairs,
              "last_best_replies": replies, "first_branch_floors": floors,
              "first_threshold": threshold,
              "pure_spe_pairs": [{"a":a,"b":b,"profit":z} for z,a,b in pure],
              "pure_minimum_profit": pure_min,
              "convexified_minimum_profit": convex_min,
              "gap": pure_min-convex_min,
              "optimal_mixtures": optimal_mixtures,
              "method": "Exact Fraction enumeration of all 25 pairs and all two-point threshold intersections; no imported solver or proposer derivation."}
    clean = json.loads(json.dumps(report, default=str))
    (HERE / "projected_hull_independent_audit.json").write_text(
        json.dumps(clean, indent=2)+"\n")
    print(json.dumps({k: clean[k] for k in ("first_threshold", "last_best_replies", "pure_minimum_profit", "convexified_minimum_profit", "gap", "optimal_mixtures")}, indent=2))

if __name__ == "__main__":
    main()
