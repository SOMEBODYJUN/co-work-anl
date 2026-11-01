"""Independent exact regression for uniform_shrink_full_tree_tax.md.

Read an existing complete ordered-history strategy, not the discovery code,
the exact solver, or the canonical certificate verifier. All calculations below
use Fraction on expanded unit customers. This is a regression, not a new search.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
name = "individual_security_failure"
raw = json.loads((REPO / "examples/customer_attraction" / (name + ".json")).read_text())
cert = json.loads((REPO / "evidence/certificates/customer_attraction" / (name + ".json")).read_text())["strategy"]
m, k = raw["players"], len(raw["topics"])
customers = tuple(frozenset(row["topics"]) for row in raw["customers"] for _ in range(row["multiplicity"]))
actions = {tuple(row["history"]): row["action"] for row in cert["actions"]}
histories = tuple(h for d in range(m) for h in product(range(k), repeat=d))
assert set(actions) == set(histories)

@lru_cache(None)
def leaf(h):
    return h if len(h) == m else leaf(h + (actions[h],))

def original(z, i):
    return sum((F(1, sum(a in t for a in z)) for t in customers if z[i] in t), F(0))

old_slacks = []
for h in histories:
    i = len(h)
    for a in range(k):
        old_slacks.append(original(leaf(h), i) - original(leaf(h + (a,)), i))
assert min(old_slacks) >= 0
assert tuple(leaf(()).count(a) for a in range(k)) == tuple(cert["terminal_counts"])

# Keep the first unit player as background. Both original tail positions are
# scaled, including one which has already moved at a later history.
def values(z, i, lam):
    old = new = tax = F(0)
    for t in customers:
        if z[i] not in t:
            continue
        b = int(z[0] in t)
        c = sum(a in t for a in z[1:])
        assert c >= 1
        old += F(1, b + c)
        new += lam / (b + lam * c)
        tax += F(b) * (1 - lam) / ((b + c) * (b + lam * c))
    assert old - new == tax
    return old, new, tax

def background_return(z, lam):
    total = F(0)
    for t in customers:
        b = int(z[0] in t)
        c = sum(a in t for a in z[1:])
        if b and c:
            total += F(b) * (1 / (b + lam * c) - F(1, b + c))
    return total

rows = []
for lam in (F(1, 2), F(2, 3), F(1)):
    regret, tax, credits = {}, {}, {}
    scaled_comparisons = 0
    for h in histories:
        if not h:
            continue
        i = len(h)
        z = leaf(h)
        old, chosen, tax[h] = values(z, i, lam)
        regrets = []
        for a in range(k):
            old_alt, new_alt, tax_alt = values(leaf(h + (a,)), i, lam)
            assert new_alt - chosen == old_alt - old + tax[h] - tax_alt
            assert new_alt - chosen <= tax[h]
            regrets.append(new_alt - chosen)
            scaled_comparisons += 1
        regret[h] = max(F(0), *regrets)
        credits[h] = sum((values(z, j, lam)[2] for j in range(i, m)), F(0))
        full_tax = sum((values(z, j, lam)[2] for j in range(1, m)), F(0))
        assert full_tax == background_return(z, lam)
        assert credits[h] <= full_tax
    path_sums = []
    for h in regret:
        z = leaf(h)
        prescribed = tuple(z[:j] for j in range(len(h), m))
        assert all(leaf(v) == z for v in prescribed)
        total_regret = sum((regret[v] for v in prescribed), F(0))
        assert total_regret <= credits[h] <= background_return(z, lam)
        nxt = h + (actions[h],)
        next_credit = credits[nxt] if len(nxt) < m else F(0)
        assert credits[h] == tax[h] + next_credit
        assert regret[h] + next_credit <= credits[h]
        path_sums.append(total_regret)
    rows.append({
        "lambda": str(lam), "scaled_nodes": len(regret),
        "comparisons_including_self": scaled_comparisons,
        "max_one_step_profit_regret": str(max(regret.values())),
        "max_prescribed_suffix_regret_sum": str(max(path_sums)),
        "max_tax_budget": str(max(background_return(leaf(h), lam) for h in regret)),
    })

answer = {
    "scope": "One existing complete strategy; exact expanded-unit regression, not proof by sampling or new search.",
    "source_instance": "examples/customer_attraction/individual_security_failure.json",
    "source_strategy": "evidence/certificates/customer_attraction/individual_security_failure.json",
    "imports_discovery_solver_or_canonical_verifier": False,
    "players": m, "topics": k, "unit_customers": len(customers),
    "original_ordered_nodes": len(histories),
    "original_comparisons_including_self": len(old_slacks),
    "original_minimum_IC_slack": str(min(old_slacks)), "scaled_checks": rows,
}
(HERE / "uniform_tax_independent_audit.json").write_text(json.dumps(answer, indent=2) + "\n")
print(json.dumps(answer, indent=2))
