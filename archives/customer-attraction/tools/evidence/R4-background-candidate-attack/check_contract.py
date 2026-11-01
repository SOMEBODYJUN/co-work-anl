"""Exact definition-level reconciliation of R4's BG/DEFECT/PRIVATE-LOSS.

No solver, optimizer, or anonymous-history restriction is used.  The 52-client
input and complete ordered policy are read from their previously preserved
frozen originals; two smaller comparison certificates are transcribed from
the fully read source tables.  This is a finite check, not a universal proof.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
FROZEN = ROOT / "archives/customer-attraction/tools/evidence/global-actual-prefix/original/research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background"
INPUT_SHA = "5a87b05ce169cdfcb9be404871841ff6ff8b430fc707f4d5a6fa64fbd5b4f263"
POLICY_SHA = "d6c01c7f18969bbfee52c657075736b19feabe21ca04f75f3719b1a51438fa3f"


def read_pinned(name, expected):
    data = (FROZEN / name).read_bytes()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"Frozen dependency hash mismatch: {name}")
    return json.loads(data)


def run_case(name, labels, rows, players, policy, prefix):
    customers = [frozenset(label_set) for label_set, count in rows for _ in range(count)]
    topics = {a: {x for x, interests in enumerate(customers) if a in interests} for a in labels}
    expected_histories = {h for d in range(players) for h in product(labels, repeat=d)}
    if set(policy) != expected_histories:
        raise ValueError("Policy does not specify exactly all ordered decision histories")

    def leaf(h):
        h = tuple(h)
        while len(h) < players:
            h += (policy[h],)
        return h

    def cover(actions):
        return set().union(*(topics[a] for a in actions))

    def pay(actions, position, restrict=None):
        total = Fraction(0)
        for x in topics[actions[position]]:
            if restrict is None or x in restrict:
                total += Fraction(1, sum(x in topics[a] for a in actions))
        return total

    def optimal(h):
        r = players - len(h)
        values = [(len(cover(h + tail)), tail) for tail in product(labels, repeat=r)]
        best = max(v for v, _ in values)
        return best, [tail for v, tail in values if v == best]

    checks = 0
    for h in sorted(expected_histories, key=lambda z: (len(z), z)):
        actual = pay(leaf(h), len(h))
        for a in labels:
            if actual < pay(leaf(h + (a,)), len(h)):
                raise ValueError(f"SPE comparison fails at {h}, action {a}")
            checks += 1

    h = tuple(prefix)
    z = leaf(h)
    i = len(h)
    action = z[i]
    old = cover(h)
    w = len(cover(z))
    added = len(cover(z) - old)
    u = pay(z, i)
    tail = sum((pay(z, p) for p in range(i + 1, players)), Fraction(0))
    old_profit = sum((pay(z, p, old) for p in range(i, players)), Fraction(0))
    c, opt_tuples = optimal(h)
    c_child, _ = optimal(h + (action,))
    delta = c - c_child
    slack = w + tail - c_child
    defect = c - w - u - tail
    assert u + tail == added + old_profit
    assert defect == delta - u - slack

    private_rows = []
    branch_rows = {}
    for opt in opt_tuples:
        union = cover(opt)
        extra = len(topics[action] - (old | union))
        for j, a in enumerate(opt):
            private = topics[a] - (old | cover(opt[:j] + opt[j + 1:]))
            residual = len(private - topics[action])
            assert delta <= residual - extra
            if slack >= 0 and defect > 0:
                assert residual > u + slack + extra
            private_rows.append({"tuple": opt, "slot": j, "private_size": len(private),
                                 "residual_size": residual, "external_added": extra,
                                 "private_loss_bound": residual - extra})
            y = leaf(h + (a,))
            new_y = len(cover(y) - old)
            b_y = sum((pay(y, p, old) for p in range(i, players)), Fraction(0))
            d_y = pay(y, i)
            v_y = sum((pay(y, p) for p in range(i + 1, players)), Fraction(0))
            assert new_y + b_y == d_y + v_y
            child_opt, _ = optimal(h + (a,))
            child_slack = len(cover(y)) + v_y - child_opt
            ind_bound = d_y + 2 * v_y - b_y
            if child_slack >= 0:
                assert c - len(old) <= ind_bound
            branch_rows[a] = {"leaf": y, "new_coverage": new_y, "old_active_profit": b_y,
                              "current_profit": d_y, "tail_profit": v_y,
                              "child_BG_slack": child_slack,
                              "IND_bound": ind_bound, "SWITCH_left": 2 * v_y - b_y,
                              "SWITCH_right": added + tail}

    return {"name": name, "unit_customers": len(customers), "players": players,
            "ordered_nodes": len(expected_histories), "comparisons_including_self": checks,
            "root_leaf": leaf(()), "root_optimum": optimal(())[0],
            "prefix": h, "leaf": z, "old_coverage": len(old), "W": w,
            "A_h": added, "B_h": old_profit, "u": u, "V_tail": tail,
            "C": c, "C_child": c_child, "delta": delta, "S": slack, "defect": defect,
            "optimal_tuples": opt_tuples, "private_rows": private_rows,
            "comparison_branches": branch_rows}


def main():
    labels14 = tuple("ABTDE")
    rows14 = [("B", 3), ("T", 3), ("AD", 2), ("AE", 2), ("BDE", 2), ("TDE", 2)]
    p14 = {(): "A", **{(a,): b for a, b in zip(labels14, "BDDED")}}
    labels11 = tuple("ABTDE")
    rows11 = [("A", 2), ("B", 2), ("T", 1), ("TD", 1), ("TE", 1), ("ADE", 3), ("BDE", 1)]
    replies11 = ("BDDED", "DAAAA", "DAAAA", "EAAAA", "DAAAA")
    p11 = {(): "A", **{(a,): "A" for a in labels11},
           **{(a, b): reply for a, row in zip(labels11, replies11) for b, reply in zip(labels11, row)}}
    data = read_pinned("global_actual_prefix_instance.json", INPUT_SHA)
    cert = read_pinned("global_actual_prefix_complete_spe.json", POLICY_SHA)
    labels52 = tuple(data["topics"])
    rows52 = [(tuple(labels52[i] for i in row["topics"]), row["multiplicity"])
              for row in data["customers"]]
    p52 = {tuple(labels52[i] for i in row["history"]): labels52[row["action"]]
           for row in cert["actions"]}
    cases = [run_case("fourteen-client residual", labels14, rows14, 2, p14, ()),
             run_case("eleven-client opportunity", labels11, rows11, 3, p11, ("A",)),
             run_case("fifty-two-client GLOBAL", labels52, rows52, 4, p52, ("A", "B"))]
    assert [(c["delta"], c["u"], c["S"], c["defect"]) for c in cases] == [
        (1, 4, 5, -8), (3, Fraction(5, 2), 3, Fraction(-5, 2)), (9, 8, 0, 1)]
    final = cases[-1]
    assert final["optimal_tuples"] == [("T", "Q"), ("Q", "T")]
    assert all(row["SWITCH_left"] == 12 and row["SWITCH_right"] == 9
               for row in final["comparison_branches"].values())
    result = {"status": "PASS", "scope": "three explicit complete policies; no universal search",
              "frozen_instance_sha256": INPUT_SHA, "frozen_policy_sha256": POLICY_SHA,
              "total_ordered_nodes": sum(c["ordered_nodes"] for c in cases),
              "total_comparisons_including_self": sum(c["comparisons_including_self"] for c in cases),
              "cases": cases}
    (HERE / "review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                               default=lambda v: str(v) if isinstance(v, Fraction) else v) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "total_ordered_nodes", "total_comparisons_including_self")}))


if __name__ == "__main__":
    main()
