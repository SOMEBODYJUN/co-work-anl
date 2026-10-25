"""Definition-level m=5 audit of a proposed four-tail joint payment failure.

The game and policy originate in R-d398.../round5_general/security/
global_extra_individual_counterfamily.md. No solver, author code, or LP imported.
All 20^d ordered histories d=0,...,4 and all 20 actions are checked.
"""
from fractions import Fraction as F
import json
from pathlib import Path

M = 5
SCALE = 60
TOPICS = tuple((a, b) for a in range(5) for b in range(4))
counts = {"histories": 0, "comparisons": 0, "strict": 0, "tied": 0}


def fresh(xs):
    return xs.index(0)


def prescribed(t, ec, bc, state):
    if t == 0:
        return (0, 0)
    mode, anchor, bank = state
    if mode == "BASE":
        return (anchor, fresh(bc)) if t < 4 else (fresh(ec), bank)
    if mode == "PUNISH":
        return (fresh(ec), fresh(bc)) if t < 4 else (fresh(ec), bank)
    assert mode == "EXIT"
    return (fresh(ec), fresh(bc))


def transition(t, ec, bc, state, action, chosen):
    a, b = action
    if t == 0:
        return ("BASE", a, b)
    mode, anchor, bank = state
    if mode == "EXIT":
        return state
    if mode == "BASE" and action == chosen:
        return state
    if bc[b]:
        return ("EXIT", -1, -1)
    if mode == "BASE":
        return ("PUNISH", -1, b)
    assert mode == "PUNISH"
    return state


def dfs(t, ec, bc, state):
    if t == M:
        return ec, bc
    counts["histories"] += 1
    chosen = prescribed(t, ec, bc, state)
    actual_terminal = None
    alternatives = []
    for action in TOPICS:
        a, b = action
        ec1 = ec[:a] + (ec[a] + 1,) + ec[a + 1:]
        bc1 = bc[:b] + (bc[b] + 1,) + bc[b + 1:]
        child_state = transition(t, ec, bc, state, action, chosen)
        ect, bct = dfs(t + 1, ec1, bc1, child_state)
        payoff = SCALE // ect[a] + 2 * SCALE // bct[b]
        if action == chosen:
            actual_terminal = (ect, bct)
            actual_payoff = payoff
        else:
            alternatives.append(payoff)
    assert actual_terminal is not None
    for payoff in alternatives:
        assert actual_payoff >= payoff, (t, ec, bc, state, actual_payoff, payoff)
        counts["comparisons"] += 1
        counts["strict" if actual_payoff > payoff else "tied"] += 1
    return actual_terminal


def follow(first):
    ec = (0,) * 5
    bc = (0,) * 4
    state = None
    path = []
    for t in range(5):
        chosen = prescribed(t, ec, bc, state)
        action = first if t == 0 else chosen
        state = transition(t, ec, bc, state, action, chosen)
        a, b = action
        ec = ec[:a] + (ec[a] + 1,) + ec[a + 1:]
        bc = bc[:b] + (bc[b] + 1,) + bc[b + 1:]
        path.append(action)
    welfare = sum(bool(c) for c in ec) + 2 * sum(bool(c) for c in bc)
    utilities = tuple(F(1, ec[a]) + F(2, bc[b]) for a, b in path)
    return path, welfare, utilities


def main():
    terminal = dfs(0, (0,) * 5, (0,) * 4, None)
    assert counts["histories"] == sum(20**d for d in range(5)) == 168421
    assert counts["comparisons"] == 3199999
    branches = [follow(topic) for topic in TOPICS]
    assert all(w == 10 and u == (F(5, 4), F(9, 4), F(9, 4), F(9, 4), F(2))
               for path, w, u in branches)
    optimal = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 0))
    assert len({a for a, b in optimal}) + 2 * len({b for a, b in optimal}) == 13
    W, O, J, u1 = F(10), F(13), F(15), F(5, 4)
    zsum, Vsum = 5 * u1, 5 * (W - u1)
    exact_lhs = 5997 * Vsum + 997 * zsum - 997 * J
    coarse_lhs = 5997 * Vsum + 4985 * u1
    assert exact_lhs - 24000 * W == 13645
    assert coarse_lhs - 25994 * W == 8660
    out = {
        "status": "PASS", "scope": "m=5 exact proposed-payment counterexample; not HALF counterexample",
        "origin": "R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md",
        "independent_reconstruction": "raw 5 economic unit customers plus 4 disjoint two-unit banks, full ordered-history BASE/PUNISH/EXIT policy",
        **counts,
        "actual_terminal_economic_counts": list(terminal[0]),
        "actual_terminal_bank_counts": list(terminal[1]),
        "root_action_count": len(branches), "every_root_branch_W": "10",
        "every_root_branch_z": "5/4", "every_root_branch_V4": "35/4",
        "optimal_indexed_tuple": [list(x) for x in optimal],
        "W": str(W), "OPT_5": str(O), "J": str(J),
        "sum_z": str(zsum), "sum_V4": str(Vsum),
        "joint_lhs": str(exact_lhs), "joint_rhs": str(24000 * W),
        "joint_violation": "13645",
        "coarse_lhs": str(coarse_lhs), "coarse_rhs": str(25994 * W),
        "coarse_violation": "8660",
    }
    target = Path(__file__).with_name("joint_payment_audit.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
