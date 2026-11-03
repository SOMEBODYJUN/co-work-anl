"""Independent Fraction audit of finite-layer concavification and the C22 lift.

Does not import the previous author implementation or the parent audit.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


N = 22
A = tuple(range(N))
M, L = 21, 43
D = L - 2 * M


def adjacent(a, b):
    return (a - b) % N in (1, N - 1)


def f3(v):
    return Q(0 if any(adjacent(a, b) for a, b in combinations_with_replacement(v, 2)) else 11)


def phi(v):
    v = tuple(v)
    if len(v) <= 1:
        return Q(0)
    if len(v) == 2:
        a, b = v
        if a == b:
            return Q(21)
        if adjacent(a, b):
            return Q(10)
        return Q(11) + sum((f3((a, b, t)) for t in A), Q(0)) / N
    if len(v) == 3:
        return Q(22) + f3(v)
    raise ValueError(v)


def psi(v):
    k = len(v)
    return phi(v) + L * k - M * k * (k - 1) // 2


def choose(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return (h[0] + 1) % N
    if len(h) == 2:
        a, b = h
        return b if adjacent(a, b) else a
    raise ValueError(h)


def finish(h):
    h = tuple(h)
    while len(h) < 3:
        h += (choose(h),)
    return h


def payoff(pot, z, i):
    return pot(z) - pot(z[:i] + z[i + 1 :])


def gp(pot, v):
    return sum((pot(v + (t,)) - pot(v) for t in A), Q(0)) / N


def fmt(v):
    return str(v) if isinstance(v, Q) else v


def values(xs):
    return [fmt(v) for v in sorted(set(xs))]


layers = {k: tuple(combinations_with_replacement(A, k)) for k in range(4)}
layer_values = {k: values(psi(v) for v in vs) for k, vs in layers.items()}
first_ranges = {}
second_ranges = {}
for k in range(3):
    ds = [psi(v + (a,)) - psi(v) for v in layers[k] for a in A]
    assert min(ds) >= 0
    first_ranges[k] = dict(min=fmt(min(ds)), max=fmt(max(ds)), count=len(ds))
for k in range(2):
    ds = [
        psi(v + (a, b)) - psi(v + (a,)) - psi(v + (b,)) + psi(v)
        for v in layers[k]
        for a, b in product(A, repeat=2)
    ]
    assert max(ds) <= 0
    second_ranges[k] = dict(min=fmt(min(ds)), max=fmt(max(ds)), count=len(ds))
assert all(psi(v) >= 0 for vs in layers.values() for v in vs)
assert phi(()) == psi(()) == 0
assert psi((0, 0)) != Q(3, 2) * psi((0,))

terminal_count = 0
for z in product(A, repeat=3):
    for i in range(3):
        assert payoff(psi, z, i) == payoff(phi, z, i) + D
    terminal_count += 1

ic_count = 0
histories = 0
min_ic = None
for k in range(3):
    for h in product(A, repeat=k):
        histories += 1
        z = finish(h)
        base_phi = payoff(phi, z, k)
        base_psi = payoff(psi, z, k)
        for a in A:
            altered = finish(h + (a,))
            slack_phi = base_phi - payoff(phi, altered, k)
            slack_psi = base_psi - payoff(psi, altered, k)
            assert slack_phi == slack_psi >= 0
            min_ic = slack_phi if min_ic is None else min(min_ic, slack_phi)
            ic_count += 1

query_values = {}
query_shift_count = 0
for pot, name in ((phi, "original"), (psi, "lifted")):
    query_values[name] = values(gp(pot, v) for v in layers[2])
for v in layers[2]:
    assert gp(psi, v) == gp(phi, v) + D
    query_shift_count += 1

# Uniform pure diagonal competitor columns give the matching upper certificate.
diagonal_upper_original = []
diagonal_upper_lifted = []
for t in A:
    original = sum((phi((a, a, t)) - phi((a, a)) for a in A), Q(0)) / N
    lifted = sum((psi((a, a, t)) - psi((a, a)) for a in A), Q(0)) / N
    assert original == 11
    assert lifted == 12
    diagonal_upper_original.append(original)
    diagonal_upper_lifted.append(lifted)

actual = finish(())
menus = {"original": [], "lifted": []}
menu_columns = 0
for i in range(3):
    h = actual[:i]
    for pot, name in ((phi, "original"), (psi, "lifted")):
        qs = []
        for a in A:
            altered = finish(h + (a,))
            competitor = altered[:i] + altered[i + 1 :]
            qs.append(gp(pot, competitor))
            menu_columns += 1
        menus[name].append(min(qs))

u_phi = [payoff(phi, actual, i) for i in range(3)]
u_psi = [payoff(psi, actual, i) for i in range(3)]
gap_phi = sum(menus["original"]) - sum(u_phi)
gap_psi = sum(menus["lifted"]) - sum(u_psi)
assert gap_phi == gap_psi == 9
assert 3 * Q(11) - sum(u_phi) == 3 * Q(12) - sum(u_psi) == 8
all_same_payoff = payoff(psi, (0, 0, 0), 0)
required_theme_size = 3 * all_same_payoff
neighbor_query_payoff = psi((0, 0, 1)) - psi((0, 0))
assert all_same_payoff == 13
assert required_theme_size == 39
assert neighbor_query_payoff == 2 < required_theme_size / 3
assert sum(u_psi) == 28 < required_theme_size

out = dict(
    status="all exact assertions passed",
    parameters=dict(actions=N, players=3, M=M, L=L, terminal_shift=D),
    total_multisets_by_layer={k: len(vs) for k, vs in layers.items()},
    lifted_layer_values=layer_values,
    first_difference_ranges_by_base_size=first_ranges,
    second_difference_ranges_by_base_size=second_ranges,
    ordered_terminals_checked=terminal_count,
    ordered_histories_checked=histories,
    true_IC_comparisons_checked=ic_count,
    minimum_IC_slack=fmt(min_ic),
    competitor_multisets_checked=query_shift_count,
    uniform_query_values=query_values,
    matching_security_upper_certificate=dict(
        distribution="uniform on the 22 diagonal competitor multisets (a,a)",
        original_query_values=values(diagonal_upper_original),
        lifted_query_values=values(diagonal_upper_lifted),
        exact_security_original="11",
        exact_security_lifted="12",
    ),
    actual_terminal=actual,
    original_payoffs=[fmt(v) for v in u_phi],
    lifted_payoffs=[fmt(v) for v in u_psi],
    original_total=fmt(sum(u_phi)),
    lifted_total=fmt(sum(u_psi)),
    original_free_column_minima=[fmt(v) for v in menus["original"]],
    lifted_free_column_minima=[fmt(v) for v in menus["lifted"]],
    menu_columns_checked_for_both_potentials=menu_columns,
    AFC_gap_original=fmt(gap_phi),
    AFC_gap_lifted=fmt(gap_psi),
    aggregate_security_gap_original="8",
    aggregate_security_gap_lifted="8",
    CAG_diagonal_necessary_identity=dict(
        singleton_value=fmt(psi((0,))),
        repeated_pair_value=fmt(psi((0, 0))),
        CAG_required_pair_value=fmt(Q(3, 2) * psi((0,))),
        equality_holds=False,
    ),
    CAG_terminal_payoff_representation_obstruction=dict(
        payoff_in_all_same_terminal=fmt(all_same_payoff),
        required_size_of_every_theme=fmt(required_theme_size),
        neighbor_query_against_repeated_competitor=fmt(neighbor_query_payoff),
        necessary_CAG_query_floor=fmt(required_theme_size / 3),
        actual_total_if_CAG_would_be_coverage=fmt(sum(u_psi)),
        actual_coverage_would_have_to_be_at_least=fmt(required_theme_size),
    ),
)
target = Path(__file__).with_name("concavification_audit.json")
target.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(out, indent=2, ensure_ascii=False))
