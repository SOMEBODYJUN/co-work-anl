"""Verify the frozen q32 actual-position menus in exact type coordinates."""
import hashlib
import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path


def main(source):
    raw = Path(source).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == "d69e034266cf14279ce3de3ed9ebfadd9bb0ae79df9d35a89ad5fddbe5b32fe9"
    report = json.loads(raw)
    players = report["milp"]["players"]
    labels = tuple(range(report["milp"]["topics"]))
    candidate = report["exact_candidate"]
    actions = candidate["strategy"]["actions"]
    policy = {tuple(item["history"]): item["action"] for item in actions}
    histories = {h for depth in range(players) for h in product(labels, repeat=depth)}
    assert len(policy) == len(actions) and set(policy) == histories
    assert all(action in labels for action in policy.values())

    def finish(prefix):
        while len(prefix) < players:
            prefix += (policy[prefix],)
        return prefix

    def load(mask, background):
        return sum(bool(mask & (1 << label)) for label in background)

    def query_value(action, background, weights):
        return sum(
            Fraction(mass, 1 + load(mask, background))
            for mask, mass in enumerate(weights, 1)
            if mask & (1 << action)
        )

    actual = finish(())
    assert actual == (0, 0, 0, 1, 1)
    assert finish((1,)) == (1, 0, 0, 0, 0)
    common_background = actual[:-1]
    masks = tuple(range(1, 1 << len(labels)))
    alias_masks = tuple(mask for mask in masks if (mask & 3) in (0, 3))
    clone = tuple(candidate["integer_clones"])
    assert len(clone) == len(masks)
    assert all(mass == 0 or mask in alias_masks for mask, mass in enumerate(clone, 1))

    def digits(history):
        return "".join(map(str, history))

    menu_rows = []
    for index in range(players):
        prefix = actual[:index]
        assert policy[prefix] == actual[index]
        columns = []
        for forced in labels:
            leaf = finish(prefix + (forced,))
            assert leaf[:index] == prefix and leaf[index] == forced
            rivals = leaf[:index] + leaf[index + 1:]
            assert len(rivals) == players - 1 and set(rivals) <= {0, 1}
            assert all(load(mask, rivals) == load(mask, common_background) for mask in alias_masks)
            columns.append({
                "forced_action": forced,
                "true_terminal": digits(leaf),
                "deleted_background": digits(rivals),
            })
        menu_rows.append({
            "position": index + 1,
            "actual_prefix": digits(prefix),
            "actual_action": actual[index],
            "columns": columns,
        })
    assert menu_rows[3]["columns"][0]["true_terminal"] == "00001"
    assert menu_rows[4]["columns"][0]["true_terminal"] == "00010"

    # For each actual prefix, fill every remaining rival slot by 0 for the cap.
    # The lower bound on 0's query includes every legal ordered rival background.
    alias_cover_masks = tuple(mask for mask in alias_masks if mask & 1)
    legal_counts = []
    for index in range(players):
        prefix = actual[:index]
        rivals_remaining = players - index - 1
        cap = prefix + (0,) * rivals_remaining
        assert all(load(mask, cap) == load(mask, common_background) for mask in alias_masks)
        count = 0
        for rivals in product(labels, repeat=rivals_remaining):
            assert all(1 + load(mask, prefix + rivals) <= players for mask in alias_cover_masks)
            count += 1
        legal_counts.append(count)

    common_values = [query_value(action, common_background, clone) for action in labels]
    frozen_welfare = sum(mass for mask, mass in enumerate(clone, 1) if mask & 3)
    frozen_security = Fraction(frozen_welfare, players)
    assert common_values == [frozen_security] * len(labels)
    pure_2_security = min(
        query_value(2, background, clone)
        for background in product(labels, repeat=players - 1)
    )
    assert pure_2_security == query_value(2, (2,) * (players - 1), clone) == Fraction(8, 5)
    assert pure_2_security < frozen_security

    return {
        "source_sha256": digest,
        "all_ordered_histories": len(policy),
        "actual_terminal": digits(actual),
        "root_forced_1_terminal": digits(finish((1,))),
        "common_background": digits(common_background),
        "admissible_nonempty_types_after_alias": len(alias_masks),
        "actual_position_forced_columns": players * len(labels),
        "exact_menu_load_identities": players * len(labels) * len(alias_masks),
        "menu_rows": menu_rows,
        "all_legal_ordered_background_counts_by_actual_position": legal_counts,
        "frozen_clone_welfare": frozen_welfare,
        "frozen_clone_common_background_values": list(map(str, common_values)),
        "frozen_clone_true_static_value": str(frozen_security),
        "frozen_clone_pure_2_static_guarantee": str(pure_2_security),
        "frozen_clone_pure_2_budget": str(frozen_welfare - players * common_values[2]),
    }


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1]), ensure_ascii=False, indent=2))
