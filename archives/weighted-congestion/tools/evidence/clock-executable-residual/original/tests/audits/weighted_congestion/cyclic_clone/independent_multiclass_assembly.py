#!/usr/bin/env python3
"""独立重建多类基体与锚定时钟；小参数恒等式审计，不验证一般非存在定理。"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import comb, lcm
from pathlib import Path
import platform
import shlex
import sys

PROOF_SHA256 = "04181c4d5c09fb85ac84270e06743571e156a8334611943aa5f6b865f9409c33"
ROOT = Path(__file__).resolve().parents[4]
PROOF_PATH = ROOT / "research/current/weighted_congestion/linear_degree_allstate_lower_bound.md"


def bit_phase(x, j, n):
    x %= 2 * n
    return int(j < x) if x < n else int(j >= x - n)


class Game:
    """实际资源字典：每个动作保存资源 ID，按玩家真权计算真实负载。"""

    def __init__(self, m, n, k, p, clocks=False):
        assert 2 <= k <= n and m >= 2 and n >= 3 and p >= 1
        self.m, self.n, self.k, self.p = m, n, k, p
        self.players = tuple(itertools.product(range(m), range(n)))
        self.pid = {v: i for i, v in enumerate(self.players)}
        self.weights = [k ** (m - 1 - a) for a, _ in self.players]
        self.actions = [[[], []] for _ in self.players]
        self.resources = {}
        self.tests = []
        self.clock_names = set()
        self.amplitudes = [F(2 * a + 3, a + 2) for a in range(m - 1)]
        self.return_amplitude = F(7, 5)
        self.clock_amplitude = F(11, 7)
        for a in range(m - 1):
            self.add_test(("adj", a), a, a + 1, k, -1,
                          self.amplitudes[a] / self.weights[self.pid[(a, 0)]] ** p)
        self.add_test(("return",), 0, m - 1, n, +1,
                      self.return_amplitude / self.weights[self.pid[(0, 0)]] ** p)
        if clocks:
            for a in range(m):
                w = self.weights[self.pid[(a, 0)]]
                for i in range(1, n):
                    for j in range(i + 1, n):
                        name = ("clock", a, i, j)
                        self.clock_names.add(name)
                        self.add_pair(name, self.clock_amplitude / (3 * w) ** p,
                                      [((a, 0), 0), ((a, i), 1), ((a, j), 0)])
        self.names = list(self.resources)
        self.rid = {v: i for i, v in enumerate(self.names)}
        self.denominator = lcm(*(d["coefficient"].denominator for d in self.resources.values()))
        self.resource_users = []
        self.fees = []
        self.clock_rids = set()
        self.base_rids = set()
        for rid, name in enumerate(self.names):
            info = self.resources[name]
            users = [(self.pid[v], action) for v, action in info["users"]]
            self.resource_users.append(users)
            potential = sum(self.weights[v] for v, _ in users)
            c = int(info["coefficient"] * self.denominator)
            self.fees.append([c * load ** p for load in range(potential + 1)])
            (self.clock_rids if name[0][0] == "clock" else self.base_rids).add(rid)
        self.action_ids = [[[self.rid[r] for r in action] for action in actions]
                           for actions in self.actions]
        for a0, a1 in self.action_ids:
            assert a0 and a1 and set(a0).isdisjoint(a1)

    def add_pair(self, name, coefficient, users):
        for side in (0, 1):
            self.resources[(name, side)] = {"coefficient": coefficient, "users": []}
        for player, sigma in users:
            for action in (0, 1):
                resource = (name, sigma ^ action)
                self.resources[resource]["users"].append((player, action))
                self.actions[self.pid[player]][action].append(resource)

    def add_test(self, label, a, b, width, orientation, coefficient):
        self.tests.append((label, a, b, width, orientation))
        for h in range(self.n):
            users = [((a, h), 0)]
            for offset in range(width):
                j = (h + offset) % self.n
                sigma = int(j * self.m + b > h * self.m + a) ^ int(orientation == -1)
                users.append(((b, j), sigma))
            self.add_pair(("base", label, h), coefficient, users)

    def loads(self, state):
        return [sum(self.weights[player] for player, action in users if state[player] == action)
                for users in self.resource_users]

    def cost_pair(self, state, player, loads=None, selected=None):
        if loads is None:
            loads = self.loads(state)
        old_action = state[player]
        old_ids = self.action_ids[player][old_action]
        new_ids = self.action_ids[player][1 - old_action]
        if selected is not None:
            old_ids = [r for r in old_ids if r in selected]
            new_ids = [r for r in new_ids if r in selected]
        old = sum(self.fees[r][loads[r]] for r in old_ids)
        new = sum(self.fees[r][loads[r] + self.weights[player]] for r in new_ids)
        return old, new

    def test_pair(self, state, player, label):
        selected = {self.rid[name] for name in self.names
                    if name[0][:2] == ("base", label)}
        return tuple(F(x, self.denominator) for x in self.cost_pair(state, player, selected=selected))

    def phase_state(self, phases):
        return tuple(bit_phase(phases[a], j, self.n) for a, j in self.players)

    def twist(self, state):
        twisted = [None] * len(state)
        for old, (a, j) in enumerate(self.players):
            twisted[self.pid[(a, (j + 1) % self.n)]] = state[old] ^ int(j == self.n - 1)
        return tuple(twisted)

    def triggering_clocks(self, state):
        result = set()
        for name in self.clock_names:
            _, a, i, j = name
            bits = [state[self.pid[(a, t)]] for t in (0, i, j)]
            if bits[0] == bits[2] != bits[1]:
                result.add(name)
        return result


def independent_new_cost(game, state, player):
    updated = list(state)
    updated[player] ^= 1
    loads = game.loads(updated)
    return sum(game.fees[r][loads[r]] for r in game.action_ids[player][updated[player]])


def front_and_endpoint_audit(m, n, k, p):
    game = Game(m, n, k, p)
    eps = F(1, k ** (m - 1))
    endpoint_checks = 0
    phase_count = 0
    for phases in itertools.product(range(2 * n), repeat=m):
        phase_count += 1
        state = game.phase_state(phases)
        assert game.twist(state) == game.phase_state(tuple(x + 1 for x in phases))
        for a in range(m - 1):
            A = game.amplitudes[a]
            for backward in (0, 1):
                r = (phases[a + 1] - phases[a] + backward) % (2 * n)
                num = k - min(r, k) if r <= n else min(r - n, k)
                expected = (A * (1 + F(num, k)) ** p, A * (2 - F(num, k)) ** p)
                if backward:
                    expected = expected[::-1]
                player = game.pid[(a, (phases[a] - backward) % n)]
                assert game.test_pair(state, player, ("adj", a)) == expected
                endpoint_checks += 1
                r_light = (phases[a] - phases[a + 1] + backward) % (2 * n)
                es = [int(bit_phase(r_light, (-t) % n, n) == int(t != 0)) for t in range(k)]
                expected_light = (
                    A * sum((F(k - t, k) + es[t]) ** p for t in range(k)),
                    A * sum((F(t + 1, k) + 1 - es[t]) ** p for t in range(k)))
                if backward:
                    expected_light = expected_light[::-1]
                player = game.pid[(a + 1, (phases[a + 1] - backward) % n)]
                assert game.test_pair(state, player, ("adj", a)) == expected_light
                X = sum((1 + F(t, k)) ** p for t in range(1, k + 1))
                assert all(value <= A * X for value in expected_light)
                endpoint_checks += 1
        for backward in (0, 1):
            r = (phases[0] - phases[-1] + backward) % (2 * n)
            es = [int(bit_phase(r, (-t) % n, n) == int(t == 0)) for t in range(n)]
            expected = (
                game.return_amplitude * sum(((n - t) * eps + es[t]) ** p for t in range(n)),
                game.return_amplitude * sum(((t + 1) * eps + 1 - es[t]) ** p for t in range(n)))
            if backward:
                expected = expected[::-1]
            player = game.pid[(m - 1, (phases[-1] - backward) % n)]
            assert game.test_pair(state, player, ("return",)) == expected
            endpoint_checks += 1
    parity_checks = 0
    for T in range(n):
        even_r = (-T) % (2 * n)
        e_even = [int(bit_phase(even_r, (-t) % n, n) == int(t == 0)) for t in range(n)]
        assert e_even.count(0) == T + 1
        odd_r = (n - T + 1) % (2 * n)
        e_odd = [int(bit_phase(odd_r, (-t) % n, n) == int(t == 0)) for t in range(n)]
        assert e_odd.count(1) == T
        parity_checks += 2
    # 两轮完整拼装：以实际位串逐玩家翻位，不用端点公式提供输入。
    state = [0] * len(game.players)
    sweep_moves = 0
    X = sum((1 + F(t, k)) ** p for t in range(1, k + 1))
    Y = sum(F(t, k) ** p for t in range(1, k + 1))
    U = sum((1 + t * eps) ** p for t in range(1, n + 1))
    V = sum((t * eps) ** p for t in range(1, n + 1))
    for _ in range(2):
        for j, a in itertools.product(range(n), range(m)):
            player = game.pid[(a, j)]
            pair = tuple(F(x, game.denominator) for x in game.cost_pair(state, player))
            expected = [F(0), F(0)]
            if a < m - 1:
                expected[0] += game.amplitudes[a] * 2 ** p
                expected[1] += game.amplitudes[a]
            if a > 0:
                expected[0] += game.amplitudes[a - 1] * Y
                expected[1] += game.amplitudes[a - 1] * X
            if a == 0:
                expected[0] += game.return_amplitude
                expected[1] += game.return_amplitude * (1 + n * eps) ** p
            if a == m - 1:
                expected[0] += game.return_amplitude * U
                expected[1] += game.return_amplitude * V
            assert pair == tuple(expected)
            assert game.cost_pair(state, player)[1] == independent_new_cost(game, state, player)
            state[player] ^= 1
            sweep_moves += 1
    assert not any(state)
    return {"m": m, "N": n, "K": k, "degree": p,
            "phase_vectors": phase_count, "endpoint_pairs": endpoint_checks,
            "return_parity_counts": parity_checks, "sweep_moves": sweep_moves}


def multiclass_allstate_audit(m, n, k, p):
    game = Game(m, n, k, p, clocks=True)
    full_states = 0
    deviation_checks = 0
    repair_checks = 0
    pair_participation_checks = 0
    clock_pairs = comb(n - 1, 2)
    for player in range(len(game.players)):
        used = {game.names[r][0] for r in game.action_ids[player][0] if r in game.clock_rids}
        assert len(used) <= clock_pairs
        a, j = game.players[player]
        assert len(used) == (clock_pairs if j == 0 else n - 2)
        # 重类自己的一个邻接窗口、作为轻类参加K窗口；返回端只参与指定角色。
        base_used = {game.names[r][0] for r in game.action_ids[player][0] if r in game.base_rids}
        expected = int(a < m - 1) + k * int(a > 0) + int(a == 0) + n * int(a == m - 1)
        assert len(base_used) == expected
        pair_participation_checks += 2
    for state in itertools.product((0, 1), repeat=m * n):
        full_states += 1
        loads = game.loads(state)
        twisted = game.twist(state)
        tloads = game.loads(twisted)
        # 基体扭转对任意状态与全部真实单人偏离的精确协变；clock不作此断言。
        for player, (a, j) in enumerate(game.players):
            target = game.pid[(a, (j + 1) % n)]
            assert game.cost_pair(state, player, loads, game.base_rids) == game.cost_pair(
                twisted, target, tloads, game.base_rids)
            # 完整基体+所有类clock 的新成本，由直接翻位重算核对。
            assert game.cost_pair(state, player, loads)[1] == independent_new_cost(game, state, player)
            deviation_checks += 1
        triggered = game.triggering_clocks(state)
        for a in range(m):
            bits = state[a * n:(a + 1) * n]
            is_front = sum(bits[j] != bits[j - 1] for j in range(1, n)) <= 1
            class_triggered = {t for t in triggered if t[1] == a}
            assert bool(class_triggered) == (not is_front)
            if is_front:
                continue
            first = next(j for j in range(1, n) if bits[j] != bits[0])
            player = game.pid[(a, first)]
            changed = list(state)
            changed[player] ^= 1
            changed_triggers = game.triggering_clocks(changed)
            participating = {game.names[r][0] for r in game.action_ids[player][0]
                             if r in game.clock_rids}
            assert participating.intersection(triggered)
            assert not participating.intersection(changed_triggers)
            old_clock, new_clock = game.cost_pair(state, player, loads, game.clock_rids)
            assert F(old_clock, game.denominator) >= game.clock_amplitude
            assert F(new_clock, game.denominator) <= clock_pairs * game.clock_amplitude * F(2, 3) ** p
            # 此玩家没有别类clock，repair只改一个动作位。
            assert all(name[1] == a for name in participating)
            assert sum(x != y for x, y in zip(state, changed)) == 1
            repair_checks += 1
    return {"m": m, "N": n, "K": k, "degree": p,
            "states": full_states, "all_player_deviations": deviation_checks,
            "illegal_class_repairs": repair_checks,
            "participation_checks": pair_participation_checks,
            "resources": len(game.resources), "players": len(game.players)}


def clock_singleclass_audit(n, p):
    checks = 0
    repairs = 0
    triples = list(itertools.combinations(range(1, n), 2))
    for bits in itertools.product((0, 1), repeat=n):
        triggered = [(i, j) for i, j in triples if bits[0] == bits[j] != bits[i]]
        front = sum(bits[t] != bits[t - 1] for t in range(1, n)) <= 1
        assert bool(triggered) == (not front)
        checks += 1
        if not front:
            first = next(t for t in range(1, n) if bits[t] != bits[0])
            flipped = list(bits)
            flipped[first] ^= 1
            assert any(first in t for t in triggered)
            assert all(not (flipped[0] == flipped[j] != flipped[i])
                       for i, j in triples if first in (i, j))
            repairs += 1
        for i, j in triples:
            sides = [bits[0], bits[i] ^ 1, bits[j]]
            counts = [sides.count(s) for s in sides]
            if (i, j) in triggered:
                assert all(F(c, 3) ** p == 1 for c in counts)
            else:
                assert all(F(c, 3) ** p <= F(2, 3) ** p for c in counts)
    return {"N": n, "degree": p, "bitstrings": checks, "repairs": repairs}


def clock_twist_noninvariance():
    game = Game(3, 4, 2, 3, clocks=True)
    state = (0,) * 12
    twisted = game.twist(state)
    p0, p1 = game.pid[(0, 0)], game.pid[(0, 1)]
    before = F(game.cost_pair(state, p0, selected=game.clock_rids)[0], game.denominator)
    after = F(game.cost_pair(twisted, p1, selected=game.clock_rids)[0], game.denominator)
    assert before == 3 * game.clock_amplitude * F(2, 3) ** 3
    assert after == 2 * game.clock_amplitude * F(2, 3) ** 3
    assert before != after
    return {"N": 4, "degree": 3, "clock_amplitude": str(game.clock_amplitude),
            "allzero_anchor_clock_cost": str(before),
            "twisted_corresponding_player_clock_cost": str(after),
            "interpretation": "Base symmetry does not extend to the anchored clock game; the proof uses it only before adding clocks."}


def integer_degree_certificate():
    """Check the exact base and induction identities of the dyadic budget proof.

    The proof for every integer k>=20 is in the accompanying review; the
    bounded loop is a regression of the polynomial identity, not that proof.
    """
    def exponent(k):
        return 24 * (k + 1) ** 2 + k
    assert exponent(20) == 10604 < 2 ** 19 == 524288
    for k in range(20, 257):
        assert 2 * exponent(k) - exponent(k + 1) == 24 * k * k + k - 49 > 0
        assert exponent(k) < 2 ** (k - 1)
        assert 2 * k + 3 <= 2 ** k
    endpoints = []
    for k in (20, 21, 32, 64, 128, 256):
        for p in (2 ** k, 2 ** k + 1, 2 ** (k + 1) - 1):
            ell = (p * p - 1).bit_length()
            assert p.bit_length() - 1 == k
            assert ell <= 2 * (k + 1)
            assert ell + 1 <= 2 * k + 3 <= 2 ** k
            endpoints.append({"p": str(p), "k": k, "m": ell + 1})
    p0 = 2 ** 20
    ell0 = (p0 * p0 - 1).bit_length()
    assert ell0 == 40
    assert 3 ** p0 > 2 ** p0 * (ell0 + 1) * p0 ** (12 * ell0)
    return {"base_F20": exponent(20), "base_comparison_exponent": 2 ** 19,
            "induction_identity": "2F(k)-F(k+1)=24k^2+k-49>0 for k>=20",
            "identity_regression_k": [20, 256], "dyadic_endpoints": endpoints,
            "exact_integer_majorant_at_p0": True,
            "scope": "Exact checks supplement the analytic induction in the review; not finite enumeration of all p."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--proof", type=Path, default=PROOF_PATH)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("output exists; refusing to overwrite frozen evidence")
    if args.proof:
        actual = hashlib.sha256(args.proof.read_bytes()).hexdigest()
        if actual != PROOF_SHA256:
            parser.error(f"proof SHA mismatch: {actual}")
    result = {
        "audit": "independent multiclass literal resource assembly",
        "proof_sha256": PROOF_SHA256,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "code_path": str(Path(__file__).resolve().relative_to(ROOT)),
        "command": shlex.join([sys.executable, *sys.argv]),
        "actual_proof_sha256": hashlib.sha256(args.proof.read_bytes()).hexdigest(),
        "input_source": "Deterministic parameters and positive amplitudes explicitly fixed in this source; each case records m,N,K,p.",
        "python": platform.python_version(),
        "arithmetic": "integer-scaled exact rational resource costs and Fraction endpoint expressions",
        "seed": None,
        "scope": "Small parameters verify identities and assembly only; no claim that these instances meet p>=2^20 or establish the general theorem.",
        "allstate": [multiclass_allstate_audit(*t) for t in ((3, 3, 2, 2), (4, 3, 2, 3), (3, 4, 2, 3))],
        "front_endpoints": [front_and_endpoint_audit(*t) for t in ((3, 3, 2, 2), (4, 3, 2, 3), (3, 4, 2, 3), (3, 5, 3, 4))],
        "singleclass_clocks": [clock_singleclass_audit(n, p) for n, p in ((3, 2), (4, 3), (5, 2), (6, 3), (7, 4), (8, 3), (9, 2), (10, 3))],
        "clock_twist_boundary": clock_twist_noninvariance(),
        "integer_degree_certificate": integer_degree_certificate(),
        "status": "all exact assertions passed",
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as f:
            f.write(payload)
    sys.stdout.write(payload)


if __name__ == "__main__":
    main()
