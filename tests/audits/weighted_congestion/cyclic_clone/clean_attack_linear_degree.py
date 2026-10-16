#!/usr/bin/env python3
"""从literal资源关联独立复核线性次数下界的端点、扭转和clock修复。

No research module or other audit is imported.  Small auxiliary games test
finite identities only; the all-p theorem is checked analytically in the
companion review.  All costs use Fraction and recompute loads after a genuine
single-player deviation.  With no --output the JSON record goes only to stdout;
an explicit output is created exclusively and never overwrites an old record.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import platform
import shlex
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[4]
SOURCE = "research/current/weighted_congestion/linear_degree_allstate_lower_bound.md"
SOURCE_SHA256 = "04181c4d5c09fb85ac84270e06743571e156a8334611943aa5f6b865f9409c33"
OLD_FREEZE_SHA256 = "c1f846520baa918b5506013e7a2704fb059e64f1f03c6699c0183b799ee0029c"


@dataclass(frozen=True)
class Resource:
    coefficient: F
    degree: int


class BinaryGame:
    """An ordinary resource-subset game; no closed-form endpoint costs."""

    def __init__(self, weights):
        self.weights = tuple(map(F, weights))
        self.actions = [[[], []] for _ in weights]
        self.resources = []
        self.cache = {}

    def pair(self, users_and_phases, coefficient, degree):
        users_and_phases = tuple(users_and_phases)
        assert len({i for i, _ in users_and_phases}) == len(users_and_phases)
        start = len(self.resources)
        self.resources.extend([Resource(F(coefficient), degree)] * 2)
        for i, phase in users_and_phases:
            assert phase in (0, 1)
            self.actions[i][0].append(start + phase)
            self.actions[i][1].append(start + (1 ^ phase))

    def values(self, state):
        state = tuple(state)
        if state not in self.cache:
            loads = [F(0) for _ in self.resources]
            for i, action in enumerate(state):
                for e in self.actions[i][action]:
                    loads[e] += self.weights[i]
            fees = [r.coefficient * load ** r.degree
                    for r, load in zip(self.resources, loads)]
            costs = tuple(sum((fees[e] for e in self.actions[i][b]), F(0))
                          for i, b in enumerate(state))
            self.cache[state] = (costs, tuple(loads))
        return self.cache[state]

    def move(self, state, player):
        changed = list(state)
        changed[player] ^= 1
        return tuple(changed)

    def edge(self, state, player):
        return (self.values(state)[0][player],
                self.values(self.move(state, player))[0][player])


def front_bit(phase, j, N):
    phase %= 2 * N
    return int(j < phase) if phase < N else int(j >= phase - N)


def front_state(xh, xl, N):
    return tuple(front_bit(x, j, N) for x in (xh, xl) for j in range(N))


def build_test(N, K, orientation, epsilon, degree):
    game = BinaryGame([F(1)] * N + [epsilon] * N)
    for h in range(N):
        users = [(h, 0)]
        for k in range(K):
            u = (h + k) % N
            # Literal pos(h)=2h and pos(u)=2u+1, rather than an endpoint table.
            sigma = int(2 * u + 1 > 2 * h) ^ int(orientation == -1)
            users.append((N + u, sigma))
        game.pair(users, F(1), degree)
    assert all(a[0] and a[1] and set(a[0]).isdisjoint(a[1]) for a in game.actions)
    return game


def heavy_table(r, N, K, degree):
    r %= 2 * N
    n = K - min(r, K) if r <= N else min(r - N, K)
    return ((1 + F(n, K)) ** degree, (2 - F(n, K)) ** degree)


def light_table(r, N, K, orientation, epsilon, degree):
    es = [int(front_bit(r, (-k) % N, N) ==
              (int(k == 0) ^ int(orientation == -1))) for k in range(K)]
    before = sum((((K-k) * epsilon + es[k]) ** degree for k in range(K)), F(0))
    after = sum((((k+1) * epsilon + 1-es[k]) ** degree for k in range(K)), F(0))
    return before, after


def run_test_case(N, K, degree):
    counts = {key: 0 for key in (
        "adjacent_heavy_forward_backward", "adjacent_light_forward_backward",
        "adjacent_light_endpoint_bounds", "return_light_forward_backward",
        "return_defect_patterns", "return_defect_margin_bounds",
        "twist_endpoint_costs", "sweep_edges")}
    adjacent = build_test(N, K, -1, F(1, K), degree)
    epsilon = F(1, degree * N)
    returning = build_test(N, N, +1, epsilon, degree)
    X = sum(((1+F(r, K)) ** degree for r in range(1, K+1)), F(0))
    Y = sum((F(r, K) ** degree for r in range(1, K+1)), F(0))
    U = sum(((1+r*epsilon) ** degree for r in range(1, N+1)), F(0))
    V = sum(((r*epsilon) ** degree for r in range(1, N+1)), F(0))
    W = (1+N*epsilon) ** degree
    alpha = F(2)  # Auxiliary margin identity; no small-degree theorem is asserted.
    Z = U-alpha*V
    for r in range(2*N):
        s = front_state(0, r, N)
        assert adjacent.edge(s, 0) == heavy_table(r, N, K, degree)
        assert adjacent.edge(s, N-1) == heavy_table(r+1, N, K, degree)[::-1]
        counts["adjacent_heavy_forward_backward"] += 2
        s = front_state(r, 0, N)
        for game, Kt, ot, epst, label in (
                (adjacent, K, -1, F(1, K), "adjacent_light_forward_backward"),
                (returning, N, +1, epsilon, "return_light_forward_backward")):
            forward = game.edge(s, N)
            backward = game.edge(s, 2*N-1)
            assert forward == light_table(r, N, Kt, ot, epst, degree)
            assert backward == light_table(r+1, N, Kt, ot, epst, degree)[::-1]
            counts[label] += 2
            if ot == -1:
                assert max(forward + backward) <= X
                counts["adjacent_light_endpoint_bounds"] += 4
    for T in range(N):
        even_r = -T
        even_es = [int(front_bit(even_r, (-k) % N, N) == int(k == 0))
                   for k in range(N)]
        assert [k for k, e in enumerate(even_es) if not e] == list(range(T+1))
        odd_forward_r = N-T+1
        odd_es = [int(front_bit(odd_forward_r, (-k) % N, N) == int(k == 0))
                  for k in range(N)]
        assert [k for k, e in enumerate(odd_es) if e] == list(range(T))
        counts["return_defect_patterns"] += 2
        for r, mover in ((even_r, N), (N-T, 2*N-1)):
            old, new = returning.edge(front_state(r, 0, N), mover)
            assert old-alpha*new >= Z-(alpha+1)*(T+1)*W
            counts["return_defect_margin_bounds"] += 1
    for xh, xl in product(range(2*N), repeat=2):
        for game in (adjacent, returning):
            s = front_state(xh, xl, N)
            translated = front_state(xh+1, xl+1, N)
            for group, x in ((0, xh), (1, xl)):
                for j in {x % N, (x-1) % N}:
                    i, image = group*N+j, group*N+(j+1) % N
                    assert game.edge(s, i) == game.edge(translated, image)
                    counts["twist_endpoint_costs"] += 2
    for game, old_h, new_h, old_l, new_l in (
            (adjacent, F(2)**degree, F(1), Y, X),
            (returning, F(1), W, U, V)):
        state = (0,) * (2*N)
        for _ in range(2):
            for j in range(N):
                for i, expected in ((j, (old_h, new_h)), (N+j, (old_l, new_l))):
                    assert game.edge(state, i) == expected
                    state = game.move(state, i)
                    counts["sweep_edges"] += 1
        assert state == (0,) * (2*N)
    return {"input": {"N": N, "K": K, "degree": degree,
                      "adjacent_weights": ["1", str(F(1, K))],
                      "return_weights": ["1", str(epsilon)],
                      "auxiliary_defect_alpha": str(alpha)}, "checks": counts}


def is_front(state):
    return sum(x != y for x, y in zip(state, state[1:])) <= 1


def run_clock_case(N, degree=3):
    weight, amplitude = F(2, 5), F(7, 3)
    game = BinaryGame([weight] * N)
    triples = tuple((0, i, j) for i, j in combinations(range(1, N), 2))
    for triple in triples:
        game.pair(zip(triple, (0, 1, 0)), amplitude / (3*weight) ** degree, degree)
    Lc, delta = comb(N-1, 2), F(2, 3) ** degree
    assert all(len(a[0]) == len(a[1]) <= Lc for a in game.actions)
    counts = {"all_states": 0, "nonfront_repairs": 0,
              "front_preserving_edges": 0, "resource_trigger_identities": 0}
    for state in product((0, 1), repeat=N):
        costs, loads = game.values(state)
        triggered = []
        for pair, triple in enumerate(triples):
            pattern = tuple(state[i] for i in triple)
            trigger = pattern in ((0, 1, 0), (1, 0, 1))
            full = max(loads[2*pair:2*pair+2]) == 3*weight
            assert trigger == full
            if full:
                triggered.append(triple)
            counts["resource_trigger_identities"] += 1
        assert bool(triggered) == (not is_front(state))
        counts["all_states"] += 1
        if triggered:
            i = next(j for j in range(1, N) if state[j] != state[0])
            after = game.move(state, i)
            after_costs, after_loads = game.values(after)
            assert any(i in triple for triple in triggered)
            assert costs[i] >= amplitude
            assert all(after_loads[e] <= 2*weight for e in game.actions[i][after[i]])
            assert after_costs[i] <= len(game.actions[i][after[i]]) * amplitude * delta
            counts["nonfront_repairs"] += 1
        else:
            for i in range(N):
                after = game.move(state, i)
                if is_front(after):
                    after_costs, after_loads = game.values(after)
                    assert costs[i] == after_costs[i]
                    assert all(after_loads[e] <= 2*weight for e in game.actions[i][after[i]])
                    counts["front_preserving_edges"] += 1
    return {"input": {"N": N, "degree": degree, "weight": str(weight),
                      "amplitude": str(amplitude), "Lc": Lc}, "checks": counts}


def actual_starting_budget():
    """Test CLOCK at p0 by an exact integer cross-product, without logs."""
    p = 2**20
    m = 2
    while 2**(m-1) < p*p:
        m += 1
    Q = p**4
    N = p**(4*m-5)
    Lc = comb(N-1, 2)
    power2, power3 = 1 << p, 3**p
    # (2/3)^p <= H/(16 alpha^2 B_* Lc), after clearing all denominators.
    lhs = (40*p*p*m*Q**(m-1)*Lc) << (2*p)
    rhs = (250*power2-25*p)*power3
    assert lhs <= rhs
    assert m <= p and N >= p**7 and (m-1)*Q < N
    return {"input": {"p": p, "m": m, "Q_formula": "p^4",
                      "N_formula": "p^(4m-5)", "N_bit_length": N.bit_length(),
                      "Lc_formula": "binom(N-1,2)"},
            "integer_inequality": "40*p^2*m*Q^(m-1)*Lc*2^(2p) <= (250*2^p-25*p)*3^p",
            "lhs_bit_length": lhs.bit_length(), "rhs_bit_length": rhs.bit_length(),
            "passes": True,
            "scope": "One exact endpoint check; the all-p bound is an analytic proof obligation."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error("--output must be new; frozen evidence is never overwritten")
    source_sha = hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest()
    if source_sha != SOURCE_SHA256:
        raise RuntimeError("The reviewed proof bytes changed; obtain a new frozen review hash")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        head = None
    record = {
        "schema": "wc-independent-exact-audit-v1",
        "title": "线性次数全状态下界的clean独立literal恒等式核验",
        "status": "passed",
        "metadata": {
            "source_path": SOURCE, "source_sha256": source_sha,
            "initial_candidate_sha256": OLD_FREEZE_SHA256,
            "code_path": str(Path(__file__).resolve().relative_to(ROOT)),
            "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "command": shlex.join(["python3", *sys.argv]),
            "cwd": str(Path.cwd()), "repository_head": head,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "arithmetic": "Exact Python integers and fractions.Fraction; no floats or Decimal",
            "precision": "Exact; no rounding and no numerical tolerance",
            "randomness": "None; deterministic exhaustive finite inputs; no seed",
            "independence": "Imports no research module and no other audit; reconstructs literal resource sets",
            "output_policy": "Optional --output uses exclusive creation; otherwise stdout only"},
        "coverage": {
            "scope": "Finite identity regressions, clock state exhaustion, and one exact p0 budget check",
            "not_claimed": ["Exhaustion of the enormous G_p", "A computer proof of all p>=2^20",
                            "A priority or external peer-review determination"],
            "small_test_inputs_are_auxiliary": True},
        "test_cases": [run_test_case(3, 3, 3), run_test_case(5, 2, 3), run_test_case(7, 3, 3)],
        "clock_cases": [run_clock_case(N) for N in range(3, 8)],
        "actual_starting_budget": actual_starting_budget()}
    output = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(output)
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
