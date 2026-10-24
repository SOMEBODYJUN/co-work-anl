#!/usr/bin/env python3
"""Exact diagnostics for the full-tail ROW account; never a finite proof."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def scalar_checks():
    checked = sharp = 0
    for m in range(1, 13):
        for r in range(1, m + 1):
            p = m - r
            beta = F(m, r * (p + 1))
            assert 0 < beta <= 1
            for b, a, inside in product(range(p + 1), range(r + 1), (0, 1)):
                covered = int(b + a > 0)
                fresh = int(b == 0 and a > 0)
                credit = F(covered - inside) + F(inside, b + 1)
                utility = F(a, b + a) if a else F(0)
                inventory = F(fresh) + (F(inside, b + 1) + 1 - inside if b else 0)
                assert credit == inventory
                assert credit >= beta * utility + (1 - beta) * fresh
                if b:
                    signed = F(b * (1 - a), (b + 1) * (b + a)) if inside else F(b, b + a)
                    assert credit - utility == signed
                checked += 1
            if p:
                assert F(1, p + 1) / F(r, m) == beta
                sharp += 1
    return {"scalar_cases": checked, "sharp_single_client_contexts": sharp}


class Game:
    def __init__(self, name, m, topics, policy):
        self.name, self.m, self.topics, self.policy = name, m, topics, policy
        self.n = len(set().union(*topics))

    def finish(self, history):
        result = tuple(history)
        while len(result) < self.m:
            result += (self.policy(result),)
        return result

    def load(self, topics):
        return Counter(x for topic in topics for x in self.topics[topic])

    def utility(self, leaf, role):
        c = self.load(leaf)
        return sum((F(1, c[x]) for x in self.topics[leaf[role]]), F(0))

    def phi(self, old, suffix):
        c = self.load(suffix)
        return sum((sum((F(1, old[x] + k) for k in range(1, count + 1)), F(0))
                    for x, count in c.items()), F(0))


def audit_game(game, menus):
    nodes = comparisons = accounts = 0
    nonzero_return = nonzero_gamma = 0
    root_accounts = []
    for i in range(game.m):
        for h in product(range(len(game.topics)), repeat=i):
            z = game.finish(h)
            u = game.utility(z, i)
            for t in range(len(game.topics)):
                assert u >= game.utility(game.finish(h + (t,)), i)
                comparisons += 1
            nodes += 1
            b = game.load(h)
            actual = game.load(z)
            W = len(actual)
            r = game.m - i
            beta = F(game.m, r * (i + 1))
            fresh = sum(1 for x in actual if not b[x])
            V = sum((game.utility(z, j) for j in range(i, game.m)), F(0))
            for menu in menus:
                O = set().union(*(game.topics[t] for t in menu))
                omega = sum((F(1, b[x] + 1) for x in O), F(0))
                credit = F(W - len(O)) + omega
                assert credit >= beta * V + (1 - beta) * fresh
                if not menu:
                    continue
                q = len(menu)
                d = game.load(menu)
                leaves = [game.finish(h + (t,)) for t in menu]
                tails = [zj[i + 1:] for zj in leaves]
                row = sum((game.utility(zj, i) for zj in leaves), F(0))
                lamb = repetition = F(0)
                for tail in tails:
                    k = game.load(tail)
                    lamb += sum((F(k[x], (b[x] + 1) * (b[x] + 1 + k[x])) for x in O), F(0)) / q
                    repetition += sum((F(d[x] - 1, b[x] + 1 + k[x]) for x in O), F(0)) / q
                gamma = deletion = F(0)
                for j, t in enumerate(menu):
                    for other_tail in tails:
                        prior = leaves[j]
                        g_pair = e_pair = F(0)
                        for k in range(1, r):
                            nxt = game.finish(h + (t,) + other_tail[:k])
                            g = game.utility(prior, i + k) - game.utility(nxt, i + k)
                            assert g >= 0
                            old_suffix = prior[i:]
                            new_suffix = nxt[i:]
                            e = (game.phi(b, new_suffix[:k] + new_suffix[k + 1:])
                                 - game.phi(b, old_suffix[:k] + old_suffix[k + 1:]))
                            if k == r - 1:
                                assert e == 0
                            g_pair += g
                            e_pair += e
                            prior = nxt
                        assert (game.phi(b, (t,) + other_tail) - game.phi(b, leaves[j][i:])
                                == -g_pair + e_pair)
                        gamma += g_pair / (q * q)
                        deletion += e_pair / (q * q)
                assert row - (len(O) - W) == credit - lamb + repetition + q * (gamma - deletion)
                nonzero_return += int(deletion != 0)
                nonzero_gamma += int(gamma != 0)
                accounts += 1
                if not h:
                    root_accounts.append({"menu": menu, "row": row, "gap": len(O) - W,
                                          "credit": credit, "lambda": lamb, "repetition": repetition,
                                          "gamma": gamma, "deletion": deletion})
    return {"name": game.name, "m": game.m, "nodes": nodes, "IC_comparisons_including_self": comparisons,
            "row_accounts": accounts, "nonzero_deletion_accounts": nonzero_return,
            "nonzero_gamma_accounts": nonzero_gamma,
            "W": len(game.load(game.finish(()))), "root_accounts": root_accounts}


def fixtures():
    yield Game("zero_clients_empty_topic", 3, [set()], lambda h: 0), [(), (0,), (0, 0, 0)]
    yield Game("single_client_forced_topic", 4, [{0}], lambda h: 0), [(), (0,), (0, 0, 0, 0)]
    for m in range(1, 7):
        topics = [set(range(m))] + [{m + j} for j in range(m - 1)]
        yield Game("existing_all_big", m, topics, lambda h: 0), [(), tuple(range(m)), (0,) * m]
    types = [(4, 1), (27, 4), (29, 3), (30, 3), (31, 2), (32, 1),
             (43, 3), (45, 3), (46, 3), (51, 3), (53, 3), (54, 3), (59, 2)]
    topics = [set() for _ in range(6)]
    x = 0
    for mask, count in types:
        for _ in range(count):
            for t in range(6):
                if mask >> t & 1:
                    topics[t].add(x)
            x += 1
    assert x == 34 and len({frozenset(t) for t in topics}) == 6

    def policy(h):
        if not h:
            return 0
        if len(h) == 1:
            return 3 if h[0] < 3 else 0
        start = 0 if h[1] < 3 else 3
        return next(t for t in range(start, start + 3) if t not in h)

    yield Game("existing_34_customer_policy", 3, topics, policy), [(), (0,), (0, 2, 5), (2, 2, 5), tuple(range(6))]


def main():
    output = {"status": "exact_implementation_audit_only", "scope": "identities and full IC of named fixtures; not a general proof",
              "scalar": scalar_checks(), "games": [audit_game(game, menus) for game, menus in fixtures()],
              "five_player_beta_by_position": [F(5, (6 - i) * i) for i in range(1, 6)]}
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(output, default=encode, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "scalar": output["scalar"],
                      "fixtures": len(output["games"]),
                      "row_accounts": sum(g["row_accounts"] for g in output["games"]),
                      "nonzero_deletion_accounts": sum(g["nonzero_deletion_accounts"] for g in output["games"]),
                      "five_player_beta_by_position": output["five_player_beta_by_position"]}, default=encode))


if __name__ == "__main__":
    main()
