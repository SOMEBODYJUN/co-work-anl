"""Attack the OPEN static allowance bridge using complete ordered strategies.

Every LP contains every nonzero incentive row of the fixed full strategy.
Only rational points passing a separate definition-level verifier are accepted.
Finite success is no universal bound. Run from anywhere in this checkout.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import reduce
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import random
import sys
import time

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "history/source/notes/customer_attraction/transport_round"))
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    "boss8_cone_source", ROOT / "history/source/notes/customer_attraction/transport_round/common_q_generator.py")
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)
from customer_attraction.model import CustomerType, Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def static_row(space, terminal, topic):
    load = space.den[terminal]
    return tuple(F(space.n + 1, int(c) + 1) * int(inc) if c else F(space.n * int(inc))
                 for c, inc in zip(load, space.inc[:, topic]))


def clones_of(values):
    scale = lcm(*(v.denominator for v in values))
    weights = [int(v * scale) for v in values]
    common = reduce(gcd, weights)
    return tuple(w // common for w in weights)


def verify(space, cone, clones, topic):
    instance = Instance(tuple(f"T{a}" for a in range(space.m)),
        tuple(CustomerType(frozenset(a for a in range(space.m) if mask & (1 << a)), k)
              for mask, k in enumerate(clones, 1) if k), space.n)
    terminal = int(cone["realized"][0])
    counts = space.tc[terminal]
    cert = StrategyCertificate({h: int(a) for h, a in zip(space.histories, cone["policy"])}, counts)
    checked = verify_certificate(instance, cert)
    checked.assert_valid()
    welfare = instance.welfare(counts)
    # Recompute the static sum by removing each individual, not by its row.
    static = F(0)
    for action, copies in enumerate(counts):
        if not copies:
            continue
        q = list(counts)
        q[action] -= 1
        q[topic] += 1
        static += copies * instance.topic_payoffs(tuple(q))[topic]
    row_value = sum(c * a for c, a in zip(clones, static_row(space, terminal, topic)))
    assert static == row_value
    ratio = static / welfare
    return {"instance": instance.to_dict(), "strategy": cert.to_dict(),
            "query_topic": topic, "D_T": str(static), "W": welfare,
            "OPT": instance.optimal_welfare(), "D_over_W": str(ratio),
            "SA_gap": str(F(space.n + 1, space.n) * welfare - static),
            "verified_histories": checked.checked_histories,
            "verified_nonself_deviations": checked.checked_deviations}


def formula_checks():
    # Count-level exhaustive check: the c=0, c=m and m=1 boundaries matter.
    checks = 0
    for players in range(1, 13):
        for load in range(players + 1):
            direct = (F(1) if load else F(0)) + F(players - load, load + 1)
            formula = F(players + 1, load + 1) if load else F(players)
            assert direct == formula
            checks += 1
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", type=int, default=5)
    ap.add_argument("--topics", type=int, default=7)
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--seconds", type=float, default=90)
    ap.add_argument("--seed", type=int, default=202610218)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    formula_count = formula_checks()
    s = source.Space(args.players, args.topics)
    rng = random.Random(args.seed)
    queue = []
    for j in range(12):
        queue.append(tuple(rng.randint(1, 12) if rng.random() < .35 else 0
                           for _ in range(s.k)))
    # The residual two-player reply cycle is embedded as a seed, never assumed
    # to stay an SPE when the player count changes.
    if s.m >= 5:
        residual = {2: 3, 4: 3, 9: 2, 17: 2, 26: 2, 28: 2}
        queue.append(tuple(residual.get(mask, 0) for mask in range(1, s.k + 1)))
    started = time.monotonic()
    best = None
    records = []
    seen = set()
    step = 0
    while step < args.steps and time.monotonic() - started < args.seconds and queue:
        weights = queue.pop(0)
        if max(weights, default=0) == 0:
            continue
        # All integer matrix products in the discovery engine remain far from
        # int64 overflow. Larger rational witnesses may still be verified below.
        if sum(weights) * s.L > 10**13:
            continue
        for mode in ("random", "root_min"):
            cone, meta = s.synthesize(weights, rng.randrange(2**30), mode)
            if cone["digest"] in seen:
                continue
            seen.add(cone["digest"])
            step += 1
            maximum = None
            for topic in range(s.m):
                row = static_row(s, int(cone["realized"][0]), topic)
                result = linprog(-np.array(row, dtype=float), A_ub=-cone["gamma"] / s.L,
                    b_ub=np.zeros(len(cone["gamma"])), A_eq=[cone["c"]], b_eq=[1],
                    bounds=(0, None), method="highs")
                if not result.success:
                    raise RuntimeError(result.message)
                point = s.rational_point(cone, result)
                if point is None:
                    records.append({"step": step, "topic": topic, "exact_recovery": False})
                    continue
                endpoint = clones_of(point)
                ratio = sum(v * a for v, a in zip(point, row))
                records.append({"step": step, "topic": topic, "D_over_W": str(ratio),
                                "rows": len(cone["gamma"]), "exact_recovery": True})
                if maximum is None or ratio > maximum[0]:
                    maximum = ratio, endpoint, topic
                if best is None or ratio > F(best["D_over_W"]):
                    best = verify(s, cone, endpoint, topic)
                    best["discovery"] = meta
                    print(json.dumps({"step": step, "new_best": str(ratio),
                                      "SA_refuted": F(best["SA_gap"]) < 0}), flush=True)
                if ratio > F(s.n + 1, s.n):
                    args.steps = step
                    break
            if maximum:
                _, endpoint, _ = maximum
                queue.append(endpoint)
                jitter = [3 * w for w in endpoint]
                jitter[rng.randrange(s.k)] += 1
                queue.append(tuple(jitter))
            if step >= args.steps or time.monotonic() - started >= args.seconds:
                break
    report = {"scope": "Finite complete-history SPE cone discovery; SA remains open unless an exact counterexample is stored",
              "parameters": vars(args) | {"output": str(args.output)},
              "formula_checks": formula_count, "cones": step,
              "elapsed_seconds": time.monotonic() - started,
              "best": best, "records": records}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"cones": step, "best_ratio": best["D_over_W"] if best else None,
                      "output": str(args.output)}), flush=True)


if __name__ == "__main__":
    main()
