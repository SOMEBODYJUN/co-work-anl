"""Definition-level global-trigger example; no canonical SPE solver imported."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def utility(topic, terminal):
    return sum((F(1, sum(x in s for s in terminal)) for x in topic), F(0))


def component(include_empty=False):
    themes = {"A": frozenset(("x1", "x2")),
              "B": frozenset(("x1", "x2", "y")),
              "C": frozenset(("y", "z"))}
    if include_empty:
        themes["E"] = frozenset()
    return themes


def inspect(include_empty=False):
    themes = component(include_empty)
    names = tuple(themes)
    replies, ell = {}, {}
    for a in names:
        values = {b: utility(themes[b], (themes[a], themes[b])) for b in names}
        best = max(values.values())
        replies[a] = tuple(b for b in names if values[b] == best)
        ell[a] = min(utility(themes[a], (themes[a], themes[b])) for b in replies[a])
        assert "B" in replies[a]
        assert utility(themes[a], (themes[a], themes["B"])) == ell[a]
    threshold = max(ell.values())
    assert threshold == F(3, 2)
    scripts = (("A", "B"), ("A", "C"))
    root_payoffs = [utility(themes[a], (themes[a], themes[b])) for a, b in scripts]
    deficits = [u - threshold for u in root_payoffs]
    assert deficits == [F(-1, 2), F(1, 2)]
    for a, b in scripts:
        last_best = max(utility(themes[q], (themes[a], themes[q])) for q in names)
        assert utility(themes[b], (themes[a], themes[b])) == last_best

    actions = tuple(product(names, repeat=2))
    intended_root, intended_last = ("A", "A"), ("B", "C")

    def joint_pay(a, b, role):
        return sum((utility(themes[(a, b)[role][c]], (themes[a[c]], themes[b[c]]))
                    for c in range(2)), F(0))

    def correct_reply(a):
        return intended_last if a == intended_root else ("B", "B")

    slacks = []
    for a in actions:
        b = correct_reply(a)
        slacks.extend(joint_pay(a, b, 1) - joint_pay(a, q, 1) for q in actions)
    actual_root_pay = joint_pay(intended_root, intended_last, 0)
    slacks.extend(actual_root_pay - joint_pay(a, correct_reply(a), 0) for a in actions)
    assert min(slacks) >= 0
    assert actual_root_pay == 3

    changed_only_root = ("B", "A")
    changed_only_reply = ("B", "C")
    changed_only_gain = joint_pay(changed_only_root, changed_only_reply, 0)-actual_root_pay
    assert changed_only_gain == F(1, 2)
    assert all(changed_only_reply[c] in replies[changed_only_root[c]] for c in range(2))

    return {
        "include_empty_topic": include_empty,
        "component_last_best_replies": replies,
        "component_ell": {k: str(v) for k, v in ell.items()},
        "component_root_threshold": str(threshold),
        "root_deficits": list(map(str, deficits)),
        "script": {"root": intended_root, "last": intended_last},
        "joint_actions": len(actions),
        "decision_histories": 1 + len(actions),
        "including_self_spe_comparisons": len(slacks),
        "minimum_spe_slack": str(min(slacks)),
        "actual_root_payoff": str(actual_root_pay),
        "changed_only_trigger_profitable_deviation": {
            "root": changed_only_root, "reply": changed_only_reply,
            "gain": str(changed_only_gain), "reply_still_last_best": True},
    }


if __name__ == "__main__":
    output = {"scope": "Finite definition-level example, not a half theorem or a necessity proof",
              "no_imported_solver": True, "cases": [inspect(False), inspect(True)]}
    # The all-empty, zero-client, arbitrary-m boundary has one physical action.
    for m in (1, 2, 5):
        assert utility(frozenset(), (frozenset(),) * m) == 0
    output["zero_client_single_empty_topic_players"] = [1, 2, 5]
    path = Path(__file__).with_name("global_trigger_audit.json")
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"cases": len(output["cases"]),
                      "all_spe_checks_passed": True,
                      "changed_only_gain": "1/2", "output": str(path)}, ensure_ascii=False))
