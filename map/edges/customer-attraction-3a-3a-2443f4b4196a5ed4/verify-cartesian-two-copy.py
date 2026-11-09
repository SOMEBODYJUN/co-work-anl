"""Recompute the pinned four-label menu and verify the saved two-copy strategy."""
from argparse import ArgumentParser
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

parser = ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, default=Path.cwd())
root = parser.parse_args().repo.resolve()
ref = root / "archives/customer-attraction/tools/evidence/cartesian-finite-convexification/original/cartesian_two_copy_exact.json"
raw = ref.read_bytes()
assert sha256(raw).hexdigest() == "e9a781adc3e16b788c1a18942290287fcf82fc5014afe8e1a12356629b1b2f91"
report = json.loads(raw)
base = tuple(report["base_weights"])
assert base == (0, 0, 5, 9, 5, 4, 7, 9, 6, 3, 8, 9, 1, 6, 0)
A = tuple(range(4))
P = tuple(product(A, repeat=2))


def payoff(z, clients):
    u = [F(0)] * len(z)
    for mask, number in clients:
        hits = [i for i, a in enumerate(z) if mask & (1 << a)]
        if hits:
            for i in hits:
                u[i] += F(number, len(hits))
    return tuple(u)


u = {z: payoff(z, enumerate(base, 1)) for z in product(A, repeat=3)}
best = {}
for a, b in P:
    m = max(u[a, b, c][2] for c in A)
    best[a, b] = tuple(c for c in A if u[a, b, c][2] == m)
phi = {a: max(min(u[a, b, c][1] for c in best[a, b]) for b in A) for a in A}
menu = {a: [(a, b, c) for b in A for c in best[a, b]] for a in A}
gamma = {a: min(u[z][0] for z in menu[a] if u[z][1] >= phi[a]) for a in A}
G1 = max(gamma.values())
assert tuple(phi.values()) == (F(161, 6), F(55, 2), F(55, 3), F(161, 6))
assert G1 == F(161, 6)
dual = (F(9, 26), F(26, 83), F(1), F(0))
g = (F(55, 3), F(18), F(55, 3), F(55, 3))
witness = ({(2, 3): F(1)}, {(3, 2): F(1)},
           {(2, 3): F(17, 18), (3, 0): F(1, 18)}, {(2, 3): F(1)})
for a in A:
    assert all(u[z][0] - dual[a] * (u[z][1] - phi[a]) >= g[a] for z in menu[a])
    probs = witness[a]
    assert sum(probs.values()) == 1 and min(probs.values()) > 0
    assert all((a, *pair) in menu[a] for pair in probs)
    assert sum(probs[pair] * u[a, *pair][1] for pair in probs) >= phi[a]
    assert sum(probs[pair] * u[a, *pair][0] for pair in probs) == g[a]


def totals(z):
    return tuple(x + y for x, y in zip(u[z[0]], u[z[1]]))


joint = {(a, b): [z for z in product(menu[a], menu[b]) if totals(z)[1] >= phi[a] + phi[b]]
         for a, b in P}
mins = {p: min(totals(z)[0] for z in joint[p]) for p in P}
G2 = max(mins.values())
assert G2 == F(271, 6) and 2 * G1 - G2 == F(17, 2)
root_menu = [z for p in P for z in joint[p] if totals(z)[0] >= G2]
Wmin = min(sum(totals(z)) for z in root_menu)
root_violator = next(z for z in joint[2, 3] if totals(z)[0] == mins[2, 3])
assert totals(root_violator)[0] == F(217, 6) < G2

game = report["game"]
assert game["players"] == 3 and game["topics"] == [str(pair) for pair in P]
customers = []
for side in range(2):
    for mask, num in enumerate(base, 1):
        allowed = [i for i, pair in enumerate(P) if mask & (1 << pair[side])]
        customers.extend({"topics": allowed, "multiplicity": 1} for _ in range(num))
assert customers == game["customers"] and len(customers) == 144
joint_counts = {}
for record in customers:
    mask = sum(1 << a for a in record["topics"])
    joint_counts[mask] = joint_counts.get(mask, 0) + 1
policy = {tuple(row["history"]): row["action"] for row in report["policy"]}
L = tuple(range(16))
assert set(policy) == {h for n in range(3) for h in product(L, repeat=n)}
assert len(policy) == len(report["policy"]) == 273 and set(policy.values()) <= set(L)


@cache
def joint_pay(z):
    return payoff(z, joint_counts.items())


@cache
def finish(h):
    return h if len(h) == 3 else finish(h + (policy[h],))


actual = finish(())
actual_pay = joint_pay(actual)
nonself_zeros = 0
slacks = []
for h in policy:
    i = len(h)
    for a in L:
        slack = joint_pay(finish(h))[i] - joint_pay(finish(h + (a,)))[i]
        assert slack >= 0
        slacks.append(slack)
        nonself_zeros += int(a != policy[h] and slack == 0)
opt = max(sum(joint_pay(z)) for z in product(L, repeat=3))
root_pay = [joint_pay(finish((a,)))[0] for a in L]
assert len(slacks) == 4368 and min(slacks) == F(report["min_slack"])
assert list(actual) == report["actual_labels"] == [11, 14, 15]
assert list(map(str, actual_pay)) == report["payoffs"] == ["146/3", "146/3", "110/3"]
assert list(map(str, root_pay)) == report["root_deviation_values"]
assert Wmin == sum(actual_pay) == F(report["W"]) == 134 and opt == 144
assert F(report["base_root_minimum_guarantee"]) == G1
assert F(report["joint_root_minimum_guarantee"]) == G2

print(json.dumps({
    "input_sha256": sha256(raw).hexdigest(),
    "phi": list(map(str, phi.values())),
    "g_by_first": list(map(str, g)),
    "G1": str(G1),
    "G2": str(G2),
    "joint_menus_sizes": [len(joint[p]) for p in P],
    "joint_menus_root_minima": [str(mins[p]) for p in P],
    "joint_root_menu_size": len(root_menu),
    "second_only_example": {
        "component_paths": root_violator,
        "U2": str(totals(root_violator)[1]),
        "required_U2": str(phi[2] + phi[3]),
        "U1": str(totals(root_violator)[0]),
        "required_U1": str(G2),
    },
    "policy_root_payoffs": list(map(str, root_pay)),
    "comparisons": len(slacks),
    "nonself_zero_slacks": nonself_zeros,
    "Wmin": int(Wmin),
    "OPT": int(opt),
}, indent=2))
