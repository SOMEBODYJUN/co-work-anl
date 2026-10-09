"""Independent finite attacks of the disjoint-maximal-petals proof.

No canonical customer_attraction model, solver, or verifier is imported.
All strategic continuations are enumerated as complete ordered-history policies;
different children of a history have independently selected full subgame SPEs.
Unit customers are literal bits, and all payoff comparisons use Fraction.
This is a finite audit, not a proof of any universal welfare statement.
"""

from argparse import ArgumentParser
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path


def all_full_spe(payoff, topics, players):
    """Enumerate full pure SPE policies by definition, retaining every tie.

    This deliberately enumerates the Cartesian product of complete child
    policies, rather than the canonical solver's count-state/minimum formula.
    """
    @lru_cache(None)
    def subgames(history):
        if len(history) == players:
            return ((history, ()),)
        children = [subgames(history + (action,)) for action in range(topics)]
        result = []
        for continuation in product(*children):
            values = [payoff(action, terminal)
                      for action, (terminal, _) in enumerate(continuation)]
            best = max(values)
            descendant_actions = tuple(item for _, policy in continuation
                                       for item in policy)
            for action, value in enumerate(values):
                if value == best:
                    result.append((continuation[action][0],
                                   ((history, action),) + descendant_actions))
        return tuple(result)
    return subgames(())


def verify_full(payoff, topics, players, path, items):
    """Recheck every ordered node and actual deviating continuation directly."""
    actions = dict(items)
    expected = {h for depth in range(players)
                for h in product(range(topics), repeat=depth)}
    assert len(items) == len(actions) and set(actions) == expected

    def follow(history):
        while len(history) < players:
            history += (actions[history],)
        return history

    assert follow(()) == path
    comparisons = 0
    for history in expected:
        selected = actions[history]
        actual = follow(history + (selected,))
        for alternative in range(topics):
            branch = follow(history + (alternative,))
            assert payoff(selected, actual) >= payoff(alternative, branch)
            comparisons += 1
    return actions, comparisons


def bit_payoff(catalog):
    unit_bits = tuple(1 << index for index in range(
        max(catalog, default=0).bit_length()))

    def payoff(action, path):
        return sum((F(1, sum(bool(catalog[choice] & bit) for choice in path))
                    for bit in unit_bits if catalog[action] & bit), F(0))
    return payoff


def bit_union(catalog, path):
    union = 0
    for action in path:
        union |= catalog[action]
    return union.bit_count()


def structure(catalog):
    core = catalog[0]
    for mask in catalog[1:]:
        core &= mask
    petals = tuple(mask & ~core for mask in catalog)
    distinct = set(petals)
    maxima = {mask for mask in distinct
              if not any(mask != other and mask & other == mask
                         for other in distinct)}
    if any(left & right for left, right in combinations(maxima, 2)):
        return None
    return core, petals, maxima


def check_catalog(catalog, players):
    core, petals, maxima = structure(catalog)
    topics = len(catalog)
    payoff = bit_payoff(catalog)
    optimum = max(bit_union(catalog, path)
                  for path in product(range(topics), repeat=players))
    equilibria = all_full_spe(payoff, topics, players)
    assert equilibria
    comparisons = histories = 0
    minimum = None
    for path, items in equilibria:
        actions, checked = verify_full(payoff, topics, players, path, items)
        comparisons += checked
        histories += len(actions)
        assert all(petals[action] in maxima for action in actions.values())
        welfare = bit_union(catalog, path)
        minimum = welfare if minimum is None else min(minimum, welfare)
        core_value = core.bit_count()
        assert optimum <= core_value + (F(2) - F(1, players)) * (
            welfare - core_value)
        # Full CAG static PNE follows too: sub-petals are weakly dominated by
        # the maximal petal containing them, with others held fixed.
        for index, action in enumerate(path):
            for alternative in range(topics):
                deviated = path[:index] + (alternative,) + path[index + 1:]
                assert payoff(action, path) >= payoff(alternative, deviated)
    return len(equilibria), histories, comparisons, optimum, minimum


def monotone_tables(players, levels=range(3)):
    return tuple(table for table in product(levels, repeat=players)
                 if all(left >= right for left, right in zip(table, table[1:])))


def singleton_payoff(tables):
    return lambda action, path: F(tables[action][path.count(action) - 1])


def is_pne(tables, counts):
    for resource, count in enumerate(counts):
        if not count:
            continue
        current = tables[resource][count - 1]
        for target, other_count in enumerate(counts):
            if target != resource and current < tables[target][other_count]:
                return False
    return True


def run():
    catalog_cases = catalog_equilibria = histories = comparisons = 0
    # Every distinct unit-mask catalog of <=4 topics on 3 literal unit clients
    # satisfying the structural condition; all players=1,2 and <=2-topic m=3.
    for size in range(1, 5):
        for catalog in combinations(range(8), size):
            if structure(catalog) is None:
                continue
            for players in (1, 2) + ((3,) if size <= 2 else ()):
                count, nodes, checks, _, _ = check_catalog(catalog, players)
                catalog_cases += 1
                catalog_equilibria += count
                histories += nodes
                comparisons += checks

    duplicate_catalogs = ((0, 0, 0), (3, 3, 3), (1, 1, 2),
                          (3, 3, 4, 0), (3, 3, 7), (5, 5, 3))
    for catalog in duplicate_catalogs:
        assert structure(catalog) is not None
        count, nodes, checks, _, _ = check_catalog(catalog, 2)
        catalog_cases += 1
        catalog_equilibria += count
        histories += nodes
        comparisons += checks

    # Independent sharp-family checks against ALL full SPE policies for m<=3.
    sharp = []
    for players in range(1, 4):
        catalog = ((1 << players) - 1,) + tuple(
            1 << (players + index) for index in range(players - 1))
        count, nodes, checks, optimum, minimum = check_catalog(catalog, players)
        assert optimum == 2 * players - 1 and minimum == players
        all_big = (0,) * players
        assert any(path == all_big for path, _ in all_full_spe(
            bit_payoff(catalog), len(catalog), players))
        sharp.append({"players": players, "full_spe_policies": count,
                      "welfare": minimum, "optimum": optimum})
        histories += nodes
        comparisons += checks

    singleton_cases = singleton_equilibria = 0
    for players in range(1, 4):
        for tables in product(monotone_tables(players), repeat=2):
            payoff = singleton_payoff(tables)
            equilibria = all_full_spe(payoff, 2, players)
            for path, items in equilibria:
                verify_full(payoff, 2, players, path, items)
                counts = tuple(path.count(action) for action in range(2))
                assert is_pne(tables, counts)
            singleton_cases += 1
            singleton_equilibria += len(equilibria)

    perturbation_cases = perturbation_pairs = 0
    for players in range(1, 4):
        tables = monotone_tables(players, range(4))
        allocations = tuple((count, players - count)
                            for count in range(players + 1))
        for old, new, unchanged in product(tables, repeat=3):
            if not all(low < high for low, high in zip(new, old)):
                continue
            old_equilibria = tuple(q for q in allocations
                                   if is_pne((old, unchanged), q))
            new_equilibria = tuple(q for q in allocations
                                   if is_pne((new, unchanged), q))
            assert old_equilibria and new_equilibria
            for q, changed in product(old_equilibria, new_equilibria):
                assert changed[0] <= q[0]
                perturbation_pairs += 1
            perturbation_cases += 1

    return {
        "audit": "customer_attraction_disjoint_maxima",
        "arithmetic": "fractions.Fraction; literal unit-client masks",
        "scope": "Finite independent full ordered-policy attacks; no universal result inferred",
        "unit_mask_catalogs": {
            "cases": catalog_cases, "full_spe_policies": catalog_equilibria,
            "customers": "three bits", "distinct_topics": "one through four",
            "players": "1,2; also 3 when topics <=2",
            "duplicate_label_cases": len(duplicate_catalogs),
            "all_off_path_actions_maximal": True,
            "all_terminal_profiles_pne": True,
            "all_affine_core_welfare_bounds_hold": True,
        },
        "ordered_histories_checked_including_sharp_cases": histories,
        "spe_action_comparisons_including_sharp_cases": comparisons,
        "sharp_family": sharp,
        "singleton_nonincreasing_tables": {
            "cases": singleton_cases, "full_spe_policies": singleton_equilibria,
            "resources": 2, "players": "1 through 3", "values": [0, 1, 2],
            "all_spe_terminal_profiles_pne": True,
        },
        "single_resource_strict_lowering": {
            "cases": perturbation_cases, "pne_pairs": perturbation_pairs,
            "resources": 2, "players": "1 through 3", "values": [0, 1, 2, 3],
            "every_new_resource_count_no_larger": True,
        },
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        if args.output.exists():
            raise SystemExit("Refusing to overwrite frozen audit output")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")
