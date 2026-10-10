"""Independently audit the uploaded theta counterexample and tiny SPE sets.

The saved ordered-history policy is replayed using the unit-customer definition
and Fraction arithmetic. No outcome recurrence or uploaded payoff table is used
in that replay. Integer type multiplicities are grouped identical unit clones.
Separately, tiny complete-policy enumeration cross-checks three implementations.
This finite audit neither proves nor refutes a universal half-coverage theorem.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import platform
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "history/source/notes/customer_attraction/uploaded_2026-10-10"
sys.path.insert(0, str(ROOT))


def require(condition, message):
    """Unlike assert, all certificate checks remain active under python -O."""
    if not condition:
        raise ValueError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def profiles(topics, players):
    for path in combinations_with_replacement(range(topics), players):
        yield tuple(path.count(a) for a in range(topics))


class DefinitionGame:
    """Payoffs from attracted-unit-customer counts, with no SPE recursion."""

    def __init__(self, topics, players, weights):
        require(type(topics) is int and topics > 0, "invalid topic count")
        require(type(players) is int and players >= 0, "invalid player count")
        require(all(type(mask) is int and 0 < mask < (1 << topics)
                    and type(weight) is int and weight >= 0
                    for mask, weight in weights.items()), "invalid clone multiplicity")
        self.topics, self.players = topics, players
        self.types = tuple((mask, weight) for mask, weight in sorted(weights.items()) if weight)

    @lru_cache(None)
    def payoffs(self, counts):
        require(len(counts) == self.topics and sum(counts) == self.players,
                "payoff requires a terminal count vector")
        # Each clone of mask contributes 1/load to each attracted player.
        # Group integer numerators by denominator before forming Fractions.
        active = tuple((a, c) for a, c in enumerate(counts) if c)
        totals = [[0] * (self.players + 1) for _ in range(self.topics)]
        for mask, weight in self.types:
            attracted = tuple((a, c) for a, c in active if mask & (1 << a))
            load = sum(c for _, c in attracted)
            if load:
                for a, _ in attracted:
                    totals[a][load] += weight
        return tuple(sum((Fraction(total, load) for load, total in enumerate(row)
                          if load and total), Fraction(0)) for row in totals)

    @lru_cache(None)
    def welfare(self, counts):
        support = sum(1 << a for a, c in enumerate(counts) if c)
        return sum(weight for mask, weight in self.types if mask & support)

    def counts(self, path):
        return tuple(path.count(a) for a in range(self.topics))

    def utility(self, action, path):
        return self.payoffs(self.counts(path))[action]


def replay_saved_policy(game, rows, target):
    require(all(isinstance(row, dict) and set(row) == {"history", "action"}
                for row in rows), "malformed policy row")
    require(all(isinstance(row["history"], list)
                and all(type(a) is int and 0 <= a < game.topics for a in row["history"])
                and type(row["action"]) is int and 0 <= row["action"] < game.topics
                for row in rows), "illegal saved action or history")
    actions = {tuple(row["history"]): row["action"] for row in rows}
    required = {h for depth in range(game.players)
                for h in product(range(game.topics), repeat=depth)}
    require(len(actions) == len(rows) and set(actions) == required,
            "saved policy must contain each ordered decision history exactly once")

    @lru_cache(None)
    def terminal(prefix):
        path = prefix
        while len(path) < game.players:
            path += (actions[path],)
        return path

    comparison_count = zero_gap_count = 0
    smallest_positive_gap = None
    for history, chosen in actions.items():
        actual = terminal(history)
        require(actual[len(history)] == chosen, "saved policy replay mismatch")
        own = game.utility(chosen, actual)
        for alternative in range(game.topics):
            deviation = terminal(history + (alternative,))
            gap = own - game.utility(alternative, deviation)
            require(gap >= 0, f"profitable deviation at {history}: {alternative}, gap {gap}")
            comparison_count += 1
            zero_gap_count += gap == 0
            if gap > 0:
                smallest_positive_gap = (gap if smallest_positive_gap is None
                                         else min(gap, smallest_positive_gap))
    actual = terminal(())
    require(game.counts(actual) == target, "declared saved target differs from replay")
    utilities = tuple(game.utility(a, actual) for a in actual)
    welfare = game.welfare(target)
    require(sum(utilities) == welfare, "unit-customer welfare conservation failed")
    return {"ordered_decision_histories": len(actions),
            "comparisons_including_chosen_actions": comparison_count,
            "genuine_alternative_comparisons": comparison_count - len(actions),
            "zero_gap_comparisons_including_chosen": zero_gap_count,
            "smallest_strict_incentive_gap": str(smallest_positive_gap),
            "saved_on_path_zero_based": list(actual),
            "saved_on_path_utilities": [str(x) for x in utilities],
            "welfare": welfare,
            "root_action_continuations": [
                {"action": a, "terminal": list(terminal((a,))),
                 "root_utility": str(game.utility(a, terminal((a,))))}
                for a in range(game.topics)]}


def direct_policy_outcomes(topics, players, weights):
    """Exhaust all full ordered strategy maps, using individually expanded clones."""
    clones = tuple(frozenset(a for a in range(topics) if mask & (1 << a))
                   for mask, count in weights.items() for _ in range(count))

    @lru_cache(None)
    def payoff(action, path):
        return sum((Fraction(1, sum(a in likes for a in path))
                    for likes in clones if action in likes), Fraction(0))

    histories = [h for depth in range(players) for h in product(range(topics), repeat=depth)]
    terminal_paths = tuple(product(range(topics), repeat=players))
    outcomes = set()
    accepted = 0
    for choices in product(range(topics), repeat=len(histories)):
        policy = dict(zip(histories, choices))
        continuation = {h: h for h in terminal_paths}
        valid = True
        for history in reversed(histories):
            chosen = policy[history]
            actual = continuation[history + (chosen,)]
            own = payoff(chosen, actual)
            if any(payoff(a, continuation[history + (a,)]) > own for a in range(topics)):
                valid = False
                break
            continuation[history] = actual
        if valid:
            accepted += 1
            outcomes.add(tuple(continuation[()].count(a) for a in range(topics)))
    return outcomes, accepted, topics ** len(histories)


def tiny_crosschecks(uploaded, search):
    from customer_attraction import CustomerType, ExactSPESolver, Instance

    instances = policies = accepted_policies = prefix_sets = 0
    digest = sha256()
    cases = [(2, players, dict(zip((1, 2, 3), values)))
             for values in product(range(3), repeat=3) for players in (1, 2, 3)]
    cases.extend((3, 2, dict(zip(range(1, 8), values)))
                 for values in product(range(2), repeat=7))
    for topics, players, weights in cases:
        direct, accepted, tried = direct_policy_outcomes(topics, players, weights)
        up = uploaded.Game(topics, players, weights)
        customers = tuple(CustomerType(frozenset(a for a in range(topics)
                                                if mask & (1 << a)), count)
                          for mask, count in weights.items() if count)
        solver = ExactSPESolver(Instance(tuple(f"S{a}" for a in range(topics)), customers, players))
        data = search.exact_outcomes(topics, players,
                                     tuple(weights.get(mask, 0) for mask in range(1, 1 << topics)))
        searched = {data["leaves"][i] for i in data["outcome_ids"]}
        root = (0,) * topics
        require(direct == set(up.outcomes(root)) == set(solver.outcomes()) == searched,
                f"tiny full-policy outcome disagreement: {(topics, players, weights)}")
        for depth in range(players + 1):
            for prefix in profiles(topics, depth):
                require(up.outcomes(prefix) == solver.outcomes(prefix),
                        f"prefix-set disagreement: {prefix}")
                prefix_sets += 1
        digest.update(json.dumps([topics, players, weights, sorted(direct)],
                                 sort_keys=True, separators=(",", ":")).encode())
        instances += 1
        policies += tried
        accepted_policies += accepted
    return {"instance_count": instances, "complete_policy_maps_examined": policies,
            "accepted_policy_maps": accepted_policies,
            "uploaded_canonical_prefix_sets_compared": prefix_sets,
            "scope": ["27 two-topic multiplicity-0/1/2 inputs for each n=1,2,3",
                      "128 three-topic presence/absence inputs for n=2"],
            "comparators": ["direct unit-clone full ordered-policy enumeration",
                            "uploaded NumPy integer Game", "canonical Fraction ExactSPESolver",
                            "audit search exact_outcomes with integer LCM scaling"],
            "ordered_inputs_and_root_sets_sha256": digest.hexdigest()}


def audit(source_dir):
    manifest_path = source_dir / "SHA256.json"
    manifest = json.loads(manifest_path.read_text())
    require(set(manifest) == {"RESEARCH.md", "exact_spe.py", "auxiliary_counterexample.json",
                              "verification_report.json"}, "unexpected original SHA manifest")
    actual_hashes = {name: sha256((source_dir / name).read_bytes()).hexdigest()
                     for name in manifest}
    require(actual_hashes == manifest, "archived original bytes differ from SHA manifest")
    certificate_path = source_dir / "auxiliary_counterexample.json"
    source_path = source_dir / "exact_spe.py"
    cert = json.loads(certificate_path.read_text())
    require(set(cert) == {"status", "m", "n", "weights", "target", "policy"},
            "unexpected uploaded certificate schema")
    weights = {int(mask): count for mask, count in cert["weights"].items()}
    require(len(weights) == len(cert["weights"]), "duplicate integer mask")
    game = DefinitionGame(cert["m"], cert["n"], weights)
    target = tuple(cert["target"])
    require(all(type(c) is int and c >= 0 for c in target)
            and len(target) == game.topics and sum(target) == game.players,
            "invalid declared target")
    replay = replay_saved_policy(game, cert["policy"], target)

    optimum = -1
    optimal_counts = []
    terminals = tuple(profiles(game.topics, game.players))
    for terminal in terminals:
        value = game.welfare(terminal)
        if value > optimum:
            optimum, optimal_counts = value, [terminal]
        elif value == optimum:
            optimal_counts.append(terminal)
    theta = None
    minimizers = []
    prefix_count = 0
    for history_counts in profiles(game.topics, game.players - 1):
        replies = []
        for a in range(game.topics):
            terminal = tuple(c + (a == b) for b, c in enumerate(history_counts))
            replies.append(game.payoffs(terminal)[a])
        best = max(replies)
        if theta is None or best < theta:
            theta, minimizers = best, [history_counts]
        elif best == theta:
            minimizers.append(history_counts)
        prefix_count += 1
    largest = max(sum(weight for mask, weight in game.types if mask & (1 << a))
                  for a in range(game.topics))
    own = Fraction(replay["saved_on_path_utilities"][0])
    require(theta - own == 1, "saved theta auxiliary counterexample margin changed")
    require(2 * replay["welfare"] >= optimum, "unexpected half-coverage counterexample")
    require(theta >= Fraction(optimum, 2 * game.players - 1), "first theta lower bound failed")
    require(theta >= Fraction(2 * optimum - (game.players - 1) * largest, 2 * game.players),
            "second theta lower bound failed")

    uploaded = load_module("uploaded_cag_spe_audit", source_path)
    search = load_module("cag_integer_search_audit", ROOT / "tests/audits/customer_attraction_search.py")
    regenerated, offset = uploaded.auxiliary_counterexample()
    require(regenerated.weights == weights, "saved masks differ from uploaded deterministic construction")
    saved_policy = {tuple(row["history"]): row["action"] for row in cert["policy"]}
    require(regenerated.verify(saved_policy) == target, "uploaded verifier disagrees with replay")
    require(regenerated.last_floor() == theta and regenerated.optimum() == optimum,
            "uploaded theta/OPT disagree with definition audit")
    root_outcomes = regenerated.outcomes((0,) * game.topics)
    require(target in root_outcomes, "uploaded recurrence omits the saved certificate target")
    for terminal in terminals:
        require(regenerated.welfare(terminal) == game.welfare(terminal),
                f"uploaded terminal coverage differs at {terminal}")
        for a, count in enumerate(terminal):
            if count:
                require(Fraction(regenerated.score(terminal, a), regenerated.Q)
                        == game.payoffs(terminal)[a],
                        f"uploaded terminal payoff differs at {terminal}, action {a}")

    report = {"claim": "CA-LAST-FLOOR-ALL-PLAYERS-NO",
              "scope": "one saved complete pure history-dependent SPE and finite implementation cross-checks",
              "universal_half_coverage_proved": False, "half_coverage_refuted": False,
              "external_review_recorded": False, "world_novelty_claimed": False,
              "providers": game.players, "topics": game.topics,
              "unit_customers": sum(weights.values()), "nonempty_interest_masks": len(weights),
              "minimum_type_multiplicity": min(weights.values()),
              "maximum_type_multiplicity": max(weights.values()),
              "mobius_symmetric_offset": offset, "target_counts": list(target),
              "saved_policy_replay": replay, "theta": str(theta),
              "theta_minus_first_utility": str(theta - own), "theta_prefix_count": prefix_count,
              "theta_minimizer_count": len(minimizers),
              "theta_minimizing_count_vectors": [list(c) for c in minimizers],
              "largest_theme_K": largest, "optimum": optimum,
              "terminal_profiles_examined": len(terminals), "optimal_profile_count": len(optimal_counts),
              "one_optimal_count_vector": list(optimal_counts[0]),
              "spe_welfare_over_optimum": str(Fraction(replay["welfare"], optimum)),
              "twice_spe_welfare_minus_optimum": 2 * replay["welfare"] - optimum,
              "uploaded_root_spe_terminal_count": len(root_outcomes),
              "large_instance_comparison": "all terminal coverages and occupied-topic Fraction payoffs agree; saved policy separately replayed",
              "tiny_independent_crosschecks": tiny_crosschecks(uploaded, search),
              "python_version": platform.python_version(),
              "numpy_version": uploaded.np.__version__,
              "base_git_commit": subprocess.check_output(
                  ["git", "rev-parse", "8f9bcf4"], cwd=ROOT, text=True).strip(),
              "replay_commands": ["python3 tests/audits/customer_attraction_uploaded.py",
                                  "python3 tests/audits/customer_attraction_uploaded.py --output <new-output.json>"],
              "deterministic_parameters": {"random_sampling": False, "seed": None,
                                            "saved_strategy_replayed": True,
                                            "all_interest_masks_from_saved_input": True,
                                            "all_ordered_histories": True,
                                            "all_terminal_profiles": True,
                                            "all_last_move_prefix_profiles": True},
              "original_sha256_manifest_verified": True,
              "original_sha256_manifest": manifest,
              "original_sha256_manifest_file_sha256": sha256(manifest_path.read_bytes()).hexdigest(),
              "input_certificate_sha256": sha256(certificate_path.read_bytes()).hexdigest(),
              "uploaded_program_sha256": sha256(source_path.read_bytes()).hexdigest(),
              "audit_program_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError("refusing to overwrite frozen audit evidence")
    report = audit(args.source_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
