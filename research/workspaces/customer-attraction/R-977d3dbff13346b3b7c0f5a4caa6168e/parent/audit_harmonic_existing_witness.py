"""Rebuild the inherited four-player witness directly from customer types."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json


def main():
    root = Path(__file__).resolve().parents[5]
    source = root / "history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json"
    data = json.loads(source.read_text())
    labels, players = data["m"], data["n"]
    assert (labels, players) == (12, 4)
    weights = [(int(mask), int(w)) for mask, w in data["weights"].items()]
    assert all(w > 0 and 0 < mask < 1 << labels for mask, w in weights)
    actions = {tuple(row["history"]): row["action"] for row in data["policy"]}
    assert len(actions) == len(data["policy"])
    assert set(actions) == {h for d in range(players) for h in product(range(labels), repeat=d)}

    @lru_cache(None)
    def play(history):
        if len(history) == players:
            return history
        return play(history + (actions[history],))

    @lru_cache(None)
    def profit_scaled(terminal):
        answer = [0] * labels
        for mask, w in weights:
            c = sum((mask >> t) & 1 for t in terminal)
            if c:
                for t in set(terminal):
                    if (mask >> t) & 1:
                        answer[t] += w * (12 // c)
        return tuple(answer)

    comparisons = 0
    for h, a in actions.items():
        assert 0 <= a < labels
        u = profit_scaled(tuple(sorted(play(h))))[a]
        for b in range(labels):
            assert u >= profit_scaled(tuple(sorted(play(h+(b,)))))[b]
            comparisons += 1
    actual = play(())
    assert actual == (8, 4, 5, 0)
    tails = {t: play((t,))[1:] for t in (4, 9)}

    def potential(query, tail):
        total = F(0)
        for mask, w in weights:
            a = (mask >> query) & 1
            k = sum((mask >> t) & 1 for t in tail)
            total += w * sum((F(1, a+j) for j in range(1, k+1)), F(0))
        return total

    psi = potential(8, actual[1:])
    reg = sum((potential(t, tails[t]) for t in (4, 9)), F(0))/2-sum(
        (potential(t, tails[q]) for t in (4, 9) for q in (4, 9)), F(0))/4
    zet = psi-sum((potential(8, tails[t]) for t in (4, 9)), F(0))/2
    u = F(profit_scaled(tuple(sorted(actual)))[8], 12)
    diagonal = sum((F(profit_scaled(tuple(sorted((t,)+tails[t])))[t], 12)
                    for t in (4, 9)), F(0))
    slack = 2*u-diagonal
    combination = 2*reg+F(1, 2)*zet
    all_with_slack = slack+combination
    assert (psi, reg, zet, slack, combination, all_with_slack) == (
        F(70761167, 3), F(-11, 4), F(3), F(3), F(-4), F(-1))
    report = {"source": str(source.relative_to(root)), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "ordered_histories": len(actions), "all_action_comparisons": comparisons,
              "actual": actual, "query_distribution": {"4": "1/2", "9": "1/2"},
              "Psi": str(psi), "R": str(reg), "Z": str(zet), "S_z": str(slack),
              "tau_R_plus_eta_Z": str(combination), "G": str(all_with_slack),
              "tau": 2, "eta": "1/2", "status": "definition-level independent exact replay passed",
              "scope": "Inherited SPE refutes nonnegative combined menu debt, including leader slack; not half coverage."}
    Path(__file__).with_name("harmonic_existing_witness_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
