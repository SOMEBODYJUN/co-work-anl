"""Exact supplemental root checks for the source's finite p=2,3 observations.

The frozen oracle constructs an ordered policy with the requested actual path.
A separate integer-share loop checks every ordered node and every alternative.
Only payoff vectors are cached by counts; the strategy remains fully ordered.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import time

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE/"original"))
from customer_attraction import CustomerType, Instance, ExactSPESolver


def check(p, out):
    started = time.monotonic()
    weights = {1:(p+1)*(p+4), 2:(p+1)*(p+5), 4:2*p+3, 8:2*p+3,
               20:2, 24:2, 36:2, 40:2, 49:(p+1)*(p+2), 50:(p+1)*(p+2)}
    n, q = 2*p+2, 6
    instance = Instance(tuple("ABTQRS"),
                        tuple(CustomerType(frozenset(a for a in range(q)
                                                     if mask & (1 << a)), w)
                              for mask, w in weights.items()), n)
    target = (0,)*p + (1,)*p + (0,1)
    certificate = ExactSPESolver(instance).certificate(on_path=target)
    actions = certificate.actions
    expected_nodes = sum(q**d for d in range(n))
    assert len(actions) == expected_nodes
    scale = math.lcm(*range(1, n+1))
    memberships = [(tuple(a for a in range(q) if mask & (1 << a)), w)
                   for mask, w in weights.items()]

    @lru_cache(None)
    def pay(counts):
        values = [0]*q
        assert sum(counts) == n
        for members, weight in memberships:
            load = sum(counts[a] for a in members)
            if not load:
                continue
            assert scale % load == 0
            contribution = weight*(scale//load)
            for a in members:
                if counts[a]:
                    values[a] += contribution
        return tuple(values)

    outcomes = {}
    comparisons = zero = strict = 0
    minimum_positive = None
    for depth in range(n-1, -1, -1):
        for history in product(range(q), repeat=depth):
            chosen = actions[history]
            assert type(chosen) is int and 0 <= chosen < q
            children = []
            for alternative in range(q):
                child = history + (alternative,)
                counts = (tuple(child.count(a) for a in range(q)) if depth == n-1
                          else outcomes[child])
                assert counts[alternative] > 0
                children.append(counts)
            actual = children[chosen]
            current = pay(actual)[chosen]
            for alternative, counts in enumerate(children):
                gap = current-pay(counts)[alternative]
                assert gap >= 0, (p, history, chosen, alternative, gap)
                comparisons += 1
                if gap:
                    strict += 1
                    minimum_positive = gap if minimum_positive is None else min(minimum_positive, gap)
                else:
                    zero += 1
            outcomes[history] = actual
    actual_path = ()
    while len(actual_path) < n:
        actual_path += (actions[actual_path],)
    assert actual_path == target
    welfare = sum(w for mask, w in weights.items()
                  if any(mask & (1 << a) for a in actual_path))
    optimum = sum(weights.values())  # All six labels fit into n>=6 slots.
    assert welfare == (p+1)*(4*p+13)
    assert optimum == 4*p*p+21*p+27
    assert tuple(pay(outcomes[()])[a] for a in actual_path) == tuple(
        scale*(2*p+6 if a == 0 else 2*p+7) for a in actual_path)
    digits = "".join(str(actions[h]) for depth in range(n)
                     for h in product(range(q), repeat=depth))
    assert len(digits) == expected_nodes
    filename = f"full-root-p{p}-policy.txt"
    raw = (digits+"\n").encode()
    (out/filename).write_bytes(raw)
    report = {
        "status": "PASS", "p": p, "players": n, "topics": list("ABTQRS"),
        "weights": weights, "unit_customers": optimum,
        "policy_encoding": "One digit per history, increasing length then lexicographic indices; trailing newline excluded.",
        "policy_file": filename, "policy_sha256": hashlib.sha256(raw).hexdigest(),
        "ordered_nodes": expected_nodes, "comparisons_including_self": comparisons,
        "nonself_comparisons": comparisons-expected_nodes,
        "zero_comparisons_including_self": zero, "strict_comparisons": strict,
        "share_scale": scale, "minimum_positive_scaled_gap": minimum_positive,
        "payoff_count_cache_size": pay.cache_info().currsize,
        "actual_path": actual_path, "root_W": welfare, "root_OPT": optimum,
        "actual_prefix": target[:-2], "tail_P": 4*p+13,
        "tail_Delta": 0, "tail_freshOPT2": 4*p+14, "GLOBAL_gap": -1,
        "claim_scope": "This finite p only; no all-p root reachability assertion.",
        "elapsed_seconds": time.monotonic()-started,
    }
    (out/f"full-root-p{p}-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=BASE/"replay/finite-parameters")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for p in (2, 3):
        report = check(p, args.out_dir)
        print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
