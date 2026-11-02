"""Informed exact reconstruction of three saved inputs, not a discovery scan.

No original solver, NumPy, SciPy, RNG or canonical game package is imported.
Menus use the proved full-history outcome recursion. Certificates are expanded
on every ordered history, then checked separately by splitting each individual
unit customer among its actual covering positions after every forced action.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def dump(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


class FixedGame:
    def __init__(self, source):
        self.q, self.m = source["q"], source["r"]
        self.weights = {int(mask): weight for mask, weight in source["weights"].items()}
        self.units = tuple(mask for mask, weight in self.weights.items() for _ in range(weight))
        self.thresholds = {}
        self.zero = (0,) * self.q
        self.menus(self.zero)

    @lru_cache(None)
    def payoff(self, terminal, action):
        assert terminal[action] > 0
        return sum((F(weight, sum(terminal[b] for b in range(self.q) if mask >> b & 1))
                    for mask, weight in self.weights.items() if mask >> action & 1), F(0))

    def next_count(self, count, action):
        result = list(count)
        result[action] += 1
        return tuple(result)

    @lru_cache(None)
    def menus(self, count):
        if sum(count) == self.m:
            return frozenset((count,))
        children = [self.menus(self.next_count(count, a)) for a in range(self.q)]
        floor = max(min(self.payoff(t, a) for t in child) for a, child in enumerate(children))
        self.thresholds[count] = floor
        return frozenset(t for a, child in enumerate(children) for t in child if self.payoff(t, a) >= floor)

    def route(self, target, first=None, last=None):
        @lru_cache(None)
        def find(count):
            if sum(count) == self.m:
                return () if count == target else None
            for a in range(self.q):
                if count[a] >= target[a] or (sum(count) == 0 and first is not None and a != first):
                    continue
                if sum(count) == self.m - 1 and last is not None and a != last:
                    continue
                child = self.next_count(count, a)
                if target in self.menus(child) and self.payoff(target, a) >= self.thresholds[count]:
                    suffix = find(child)
                    if suffix is not None:
                        return (a,) + suffix
            return None
        result = find(self.zero)
        assert result is not None
        return result

    def certificate(self, target, route):
        actions = {}

        def expand(history, count, goal):
            if len(history) == self.m:
                assert count == goal
                return
            candidates = [a for a in range(self.q)
                          if goal in self.menus(self.next_count(count, a)) and self.payoff(goal, a) >= self.thresholds[count]]
            chosen = route[len(history)] if history == route[:len(history)] else min(candidates)
            assert chosen in candidates
            actions[history] = chosen
            for a in range(self.q):
                child = self.next_count(count, a)
                goal_a = goal if a == chosen else min(self.menus(child), key=lambda t: (self.payoff(t, a), t))
                expand(history + (a,), child, goal_a)

        expand((), self.zero, target)
        expected = {h for length in range(self.m) for h in product(range(self.q), repeat=length)}
        assert set(actions) == expected
        return actions

    def unit_payoffs(self, ordered_terminal):
        result = [F(0)] * self.m
        covered = 0
        for mask in self.units:
            positions = [i for i, a in enumerate(ordered_terminal) if mask >> a & 1]
            if positions:
                covered += 1
                for i in positions:
                    result[i] += F(1, len(positions))
        return tuple(result), covered

    def audit(self, actions, target, route):
        @lru_cache(None)
        def finish(history):
            return history if len(history) == self.m else finish(history + (actions[history],))

        minimum = F(0)
        records = []
        for history in sorted(actions, key=lambda h: (len(h), h)):
            selected = actions[history]
            on = self.unit_payoffs(finish(history))[0][len(history)]
            values = [self.unit_payoffs(finish(history + (a,)))[0][len(history)] for a in range(self.q)]
            gaps = [on - value for value in values]
            assert min(gaps) >= 0, (history, selected, gaps)
            minimum = min(minimum, min(gaps))
            records.append({"history": history, "action": selected, "utility": str(on),
                            "forced_action_utilities": list(map(str, values)), "minimum_gap": str(min(gaps))})
        actual = finish(())
        assert actual == route and tuple(Counter(actual)[a] for a in range(self.q)) == target
        actual_payoffs, welfare = self.unit_payoffs(actual)
        optimum = max(self.unit_payoffs(t)[1] for t in product(range(self.q), repeat=self.m))
        return {"status": "passed", "unit_clients": len(self.units), "q": self.q, "players": self.m,
                "nodes": len(actions), "comparisons_including_self": len(actions) * self.q,
                "comparisons_changing_action": len(actions) * (self.q - 1), "minimum_gap": str(minimum),
                "actual_ordered_path": actual, "actual_count": target, "actual_payoffs": list(map(str, actual_payoffs)),
                "W": welfare, "OPT": optimum, "root_threshold": str(self.thresholds[self.zero]),
                "actual_path_thresholds": [str(self.thresholds[tuple(Counter(actual[:i])[a] for a in range(self.q))]) for i in range(self.m)],
                "actions": [{"history": h, "action": a} for h, a in sorted(actions.items(), key=lambda p: (len(p[0]), p[0]))],
                "node_audit": records}


def main():
    entries = {}
    for stem, mode in (("aggregate_entry_threshold_counterexample", "aggregate"),
                       ("last_payoff_counterexample", "last"),
                       ("threshold_monotonicity_counterexample", "threshold")):
        source_path = BASE / "original" / (stem + ".json")
        source = json.loads(source_path.read_text())
        game = FixedGame(source)
        if mode in ("aggregate", "last"):
            target = tuple(source["actual"])
            assert target in game.menus(game.zero)
            route = game.route(target, last=source["last"] if mode == "last" else None)
        else:
            scale = source["scale"]
            bad = []
            # Every source row is checked as an admissible transition in its
            # stated subtree; it need not lie on one common root actual path.
            for count, a, before, after in source["bad"]:
                count = tuple(count)
                child = game.next_count(count, a)
                assert game.thresholds[count] == F(before, scale)
                assert game.thresholds[child] == F(after, scale) < game.thresholds[count]
                witnesses = sorted(t for t in game.menus(child) if game.payoff(t, a) >= game.thresholds[count])
                assert witnesses
                bad.append({"count": count, "action": a, "parent_threshold": str(F(before, scale)),
                            "child_threshold": str(F(after, scale)), "drop": str(F(before - after, scale)),
                            "supporting_terminal_count": witnesses[0]})
            # Use the source's empty-prefix row to obtain a whole original
            # four-player SPE demonstrating the drop at the actual root edge.
            root_row = next(row for row in bad if tuple(row["count"]) == game.zero)
            target = tuple(root_row["supporting_terminal_count"])
            route = game.route(target, first=root_row["action"])
        report = game.audit(game.certificate(target, route), target, route)
        report["source_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if mode == "aggregate":
            assert report["W"] == F(source["W"])
            assert game.thresholds[game.zero] == F(source["theta"])
            gap = F(report["W"]) - game.m * game.thresholds[game.zero]
            assert gap == F(source["difference"]) < 0
            report["W_minus_players_times_root_threshold"] = str(gap)
        elif mode == "last":
            assert report["W"] == F(source["W"])
            assert tuple(Counter(route[:-1])[a] for a in range(game.q)) == tuple(source["prefix"])
            lastpay = F(report["actual_payoffs"][-1])
            assert lastpay == F(source["lastpay"])
            report["last_payoff_budget_excess"] = str((game.m - 1) * lastpay - report["W"])
            assert F(report["last_payoff_budget_excess"]) > 0
        else:
            report["all_source_bad_transitions"] = bad
            report["source_integer_scale"] = scale
            assert len(bad) == 16
        dump(mode + "-fixed-exact-audit.json", report)
        entries[mode] = {k: v for k, v in report.items() if k not in ("actions", "node_audit")}
    dump("fixed-input-summary.json", {"status": "passed", "execution_scope": "three saved inputs only; no RNG, original solver or LP executed", "instances": entries})
    print(json.dumps({mode: {key: value for key, value in report.items() if key in
                             ("status", "unit_clients", "nodes", "comparisons_including_self", "actual_ordered_path", "actual_payoffs", "W", "OPT", "root_threshold", "W_minus_players_times_root_threshold", "last_payoff_budget_excess")}
                      for mode, report in entries.items()}, indent=2))


if __name__ == "__main__":
    main()
