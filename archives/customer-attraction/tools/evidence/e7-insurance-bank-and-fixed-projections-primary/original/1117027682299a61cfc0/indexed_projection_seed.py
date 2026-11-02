"""A single explicit signed-repair seed test, not an instance scan.

Project the frozen 437-row primal to actual ABCDE membership and the
comparison multiplicity j.  Uniformly realize the five comparison labels
over all j-subsets.  No old continuation/menu property is asserted.
The resulting ten-topic game, or its fifteen-topic extension retaining
the five old fixed replies, is evaluated by the exact all-SPE
continuation-set solver. Integer replication realizes all masses.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import json
import hashlib
import argparse
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-fixed", action="store_true", help="also retain old fixed U,V,W,X,Y")
    parser.add_argument("--output", type=Path, help="new result file; existing files are never overwritten")
    args = parser.parse_args()
    source = ROOT / "evidence/certificates/customer_attraction/five_player_indexed_bound.json"
    data = json.loads(source.read_text())["primal"]
    full_fixed = args.full_fixed
    fixed_count = 10 if full_fixed else 5
    topic_count = fixed_count + 5
    types = defaultdict(int)
    for atom in data["atoms"]:
        j = sum(atom["AB_hist"][4:])
        assert j == sum(atom["AE_hist"][4:])
        assert j == sum(atom["second_hist"][8:])
        actual = frozenset(i for i, bit in enumerate(atom["bits"][:fixed_count]) if bit == "1")
        each = int(atom["mass_numerator"]) * (10 // comb(5, j))
        for chosen in combinations(range(fixed_count, topic_count), j):
            types[actual | frozenset(chosen)] += each
    inst = Instance(tuple("ABCDEUVWXY"[:fixed_count]) + tuple(f"T{i}" for i in range(1, 6)),
                    tuple(CustomerType(typ, weight) for typ, weight in sorted(types.items(), key=lambda item: tuple(item[0]))),
                    5)
    scale = 10 * int(data["denominator"])
    path = tuple(range(5))
    z = inst.counts(path, terminal=True)
    u = [value / scale for value in inst.player_payoffs(path)]
    W = Fraction(inst.welfare(z), scale)
    OPT = Fraction(inst.optimal_welfare(), scale)
    B = 2 * W - OPT
    last = inst.topic_payoff(4, z)
    last_br = all(inst.topic_payoff(action, inst.counts(path[:-1] + (action,), terminal=True)) <= last
                  for action in range(inst.topic_count))
    print(json.dumps({"phase": "instance", "types": len(types), "topics": topic_count, "players": 5,
                      "count_states_upper": comb(topic_count + 5, 5), "terminal_states": comb(topic_count + 4, 5),
                      "W": str(W), "OPT": str(OPT), "B": str(B),
                      "u": list(map(str, u)), "last_br": last_br}, ensure_ascii=False), flush=True)
    solver = ExactSPESolver(inst)
    M = []
    ell = []
    start = time.monotonic()
    for i in range(4):
        prefix = inst.counts(path[:i])
        row = []
        for action in range(inst.topic_count):
            child = list(prefix)
            child[action] += 1
            outcomes = solver.outcomes(child)
            row.append(min(inst.topic_payoff(action, outcome) for outcome in outcomes) / scale)
        ell.append(row)
        M.append(max(row))
        print(json.dumps({"phase": "threshold", "i": i + 1, "M": str(M[-1]),
                          "ell": list(map(str, row)), "stats": solver.stats.__dict__,
                          "elapsed_seconds": time.monotonic() - start}), flush=True)
    g = [M[i] - u[i] for i in range(4)]
    P = sum((max(x, 0) for x in g), Fraction(0))
    N = sum((max(-x, 0) for x in g), Fraction(0))
    p = max([Fraction(0)] + g)
    n = max([Fraction(0)] + [-x for x in g])
    C = 2 * P - N + p + n
    out = {"candidate": "uniform-j-symmetrized projection of indexed primal to " + "ABCDEUVWXY"[:fixed_count] + ",T1,...,T5",
           "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
           "scale": scale, "types": len(types), "topics": list(inst.topics),
           "last_br": last_br, "W": str(W), "OPT": str(OPT), "B": str(B),
           "u": list(map(str, u)), "M": list(map(str, M)), "g": list(map(str, g)),
           "C": str(C), "B_plus_C": str(B + C), "B_plus_C_decimal": float(B + C),
           "ell": [list(map(str, row)) for row in ell],
           "stats": solver.stats.__dict__, "elapsed_seconds": time.monotonic() - start}
    print(json.dumps(out, indent=2), flush=True)
    target = args.output or Path(__file__).with_name("indexed_projection_15_seed_result.json" if full_fixed else "indexed_projection_seed_result.json")
    with target.open("x") as stream:
        stream.write(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
