"""Exact audit of the chronological deletion identity; no new SPE search.

Uses existing complete-SPE root-tax evidence and one explicit local-bridge
counterexample. General validity rests on the coefficient proof in the report.
Run from the repository root. Writes only next to this script.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))

from customer_attraction.certificate import StrategyCertificate, verify_certificate
from customer_attraction.exact import ExactSPESolver
from customer_attraction.model import CustomerType, Instance


def continuation(instance, actions, history):
    history = tuple(history)
    while len(history) < instance.players:
        history += (actions[history],)
    return history


def kernel(instance, prefix, remaining):
    """r+1 is the number of remaining movers and comparison slots."""
    n = instance.players - len(prefix)
    if not n:
        assert not remaining
        return F(0)
    value = F(0)
    for client in instance.customers:
        h = sum(a in client.topics for a in prefix)
        d = sum(a in client.topics for a in remaining)
        if d:
            value += client.multiplicity * (F(1, h + 1) + F(d - 1, h + n))
    return value


def identity(instance, certificate, comparison):
    path = continuation(instance, certificate.actions, ())
    m = instance.players
    assert len(comparison) == m
    payoff = instance.player_payoffs(path)
    W = sum(payoff)
    q = R = C = S = P = B = Phat = D = F(0)
    step_rows = []
    root_overlap = F(0)
    coverage = 0
    for client in instance.customers:
        d = sum(t in client.topics for t in comparison)
        coverage += client.multiplicity * bool(d)
        root_overlap += client.multiplicity * max(d - 1, 0)

    for i, theme in enumerate(comparison):
        r = m - i - 1
        dev = continuation(instance, certificate.actions, path[:i] + (theme,))
        v = instance.player_payoffs(dev)[i]
        slack = payoff[i] - v
        assert slack >= 0
        qi = Ri = Ci = Pi = Bi = Phi = Di = F(0)
        for client in instance.customers:
            w = client.multiplicity
            h = sum(t in client.topics for t in path[:i])
            d = sum(t in client.topics for t in comparison[i:])
            a = int(theme in client.topics)
            z = int(path[i] in client.topics)
            e = sum(t in client.topics for t in dev[i + 1:])
            c = sum(t in client.topics for t in path)
            if a:
                assert h + 1 + e == sum(t in client.topics for t in dev)
                qi += F(w, h + (1 if d == 1 else r + 1))
                if d == 1:
                    Pi += w * (F(1, h + 1) - F(1, h + 1 + e))
                    Phi += w * (F(1, h + 1) - F(1, c + 1 - z))
                    Di += w * (F(1, c + 1 - z) - F(1, h + 1 + e))
                else:
                    Bi += w * (F(1, h + 1 + e) - F(1, h + r + 1))
            dp = d - a
            if r:
                if z and dp:
                    Ri += F(w, (h + 1) * (h + 2))
                if not z and dp > 1:
                    Ci += F(w * (dp - 1), (h + r) * (h + r + 1))
        assert min(Ri, Ci, Pi, Bi, Phi) >= 0
        assert qi == payoff[i] - slack + Pi - Bi
        assert Pi == Phi + Di
        before = kernel(instance, path[:i], comparison[i:])
        after = kernel(instance, path[:i + 1], comparison[i + 1:])
        assert before - after == qi + Ri - Ci
        q += qi
        R += Ri
        C += Ci
        S += slack
        P += Pi
        B += Bi
        Phat += Phi
        D += Di
        step_rows.append({"i": i + 1, "T": instance.topics[theme],
                          "q": str(qi), "R": str(Ri), "C": str(Ci),
                          "S": str(slack), "P": str(Pi), "B": str(Bi),
                          "P_hat": str(Phi), "D": str(Di)})

    chi = F(0)
    for client in instance.customers:
        owners = [i for i, t in enumerate(comparison) if t in client.topics]
        if not owners:
            continue
        owner = owners[-1]
        c = sum(t in client.topics for t in path)
        z = int(path[owner] in client.topics)
        xchi = 1 - F(1, c + 1 - z)
        assert 0 <= xchi <= int(c > 0)
        chi += client.multiplicity * xchi
    O_over_m = root_overlap / m
    credit = S + B + C + O_over_m
    Vlast = coverage - chi
    assert coverage + O_over_m == q + R - C
    assert R + Phat == chi
    assert coverage == W + chi + D - credit
    assert D - credit == Vlast - W
    assert 2 * W - coverage == W - chi + credit - D
    return {"comparison": [instance.topics[t] for t in comparison],
            "coverage": coverage, "W": str(W), "O_over_m": str(O_over_m),
            "q": str(q), "R": str(R), "C": str(C), "S": str(S),
            "P": str(P), "B": str(B), "P_hat": str(Phat), "D": str(D),
            "chi": str(chi), "A": str(credit),
            "last_owner_frozen_query": str(Vlast),
            "unused_actual_capacity": str(W - chi),
            "strong_bridge_margin_A_minus_D": str(credit - D),
            "half_margin": str(2 * W - coverage), "steps": step_rows}


def coefficient_audit():
    checks = 0
    for h in range(8):
        for r in range(7):
            n = r + 1
            for d in range(n + 1):
                for a in range(2):
                    if a > d or d - a > r:
                        continue
                    for z in range(2):
                        old = (F(1, h + 1) + F(d - 1, h + n)) if d else F(0)
                        dp = d - a
                        new = ((F(1, h + z + 1) + F(dp - 1, h + z + r))
                               if dp else F(0))
                        q = F(a, h + (1 if d == 1 else n))
                        R = F(z * bool(dp), (h + 1) * (h + 2)) if r else F(0)
                        C = (F((1 - z) * max(dp - 1, 0), (h + r) * (h + r + 1))
                             if r else F(0))
                        assert old - new == q + R - C
                        checks += 1
    return checks


def main():
    report = {"status": "exact identity and actual clock budget only; Q-CAG-HALF OPEN",
              "coefficient_checks": coefficient_audit()}

    instance = Instance.from_dict(json.loads(
        (ROOT / 'examples/customer_attraction/root_tax_failure.json').read_text()))
    source = json.loads((ROOT / 'evidence/certificates/customer_attraction/root_tax_failure.json').read_text())
    certificate = StrategyCertificate.from_dict(dict(
        source['strategy'], terminal_counts=instance.counts(source['expected']['outcome'])))
    valid = verify_certificate(instance, certificate)
    valid.assert_valid()
    rows = [identity(instance, certificate, Ts) for Ts in permutations((0, 1, 2, 3))]
    assert {row['coverage'] for row in rows} == {61}
    assert min(F(row['chi']) for row in rows) == 23
    assert max(F(row['chi']) for row in rows) == F(53, 2)
    assert min(F(row['strong_bridge_margin_A_minus_D']) for row in rows) == 0
    path = valid.terminal_history
    full_tax = sum((client.multiplicity * F(c, c + 1)
                    for client in instance.customers
                    for c in [sum(t in client.topics for t in path)]), F(0))
    assert full_tax == F(271, 10)
    report['existing_root_tax_SPE'] = {
        'source_instance': 'examples/customer_attraction/root_tax_failure.json',
        'source_strategy': 'evidence/certificates/customer_attraction/root_tax_failure.json',
        'checked_histories': valid.checked_histories,
        'checked_nonself_deviations': valid.checked_deviations,
        'actual_path': [instance.topics[t] for t in path],
        'OPT': 61, 'W': 38, 'old_prefix_tax': '45/2',
        'full_final_tax': str(full_tax), 'chi_min': '23', 'chi_max': '53/2',
        'strong_bridge': 'holds for all 24 orders; equality when C is last',
        'orders': rows}

    local = Instance(('C', 'A', 'B', 'D'), tuple(
        CustomerType(frozenset(t), w) for t, w in
        [([1], 8), ([0, 1], 7), ([2], 7), ([0, 2], 14), ([3], 5), ([0, 3], 7)]), 3)
    solver = ExactSPESolver(local)
    certificate = solver.certificate(on_path=(0, 0, 2))
    valid = verify_certificate(local, certificate)
    valid.assert_valid()
    rows = [identity(local, certificate, Ts) for Ts in permutations((1, 2, 3))]
    assert local.optimal_welfare() == 48
    assert solver.threshold((0,) * 4) == F(35, 3)
    assert min(F(row['steps'][0]['q']) for row in rows) == 12
    report['local_toll_bridge_counterexample'] = {
        'tested_false_bridge': 'at every actual node some remaining comparison source has q_i(T)<=u_i',
        'instance': local.to_dict(), 'actual_path': ['C', 'C', 'B'],
        'actual_payoffs': ['35/3'] * 3, 'OPT': 48, 'W': 35,
        'optimal_sources': ['A', 'B', 'D'], 'root_tolls': ['15', '21', '12'],
        'root_min_toll_excess': '1/3',
        'checked_histories': valid.checked_histories,
        'checked_nonself_deviations': valid.checked_deviations,
        'strategy': certificate.to_dict(), 'orders': rows}

    collision = Instance.from_dict(json.loads(
        (ROOT / 'examples/customer_attraction/collision_free_occupancy.json').read_text()))
    certificate = StrategyCertificate.from_dict(json.loads(
        (ROOT / 'evidence/certificates/customer_attraction/collision_free_occupancy.json').read_text()))
    valid = verify_certificate(collision, certificate)
    valid.assert_valid()
    rows = [identity(collision, certificate, Ts) for Ts in ((0, 3), (3, 0))]
    assert rows[0]['chi'] == '0'
    assert rows[0]['strong_bridge_margin_A_minus_D'] == '-1'
    assert rows[1]['chi'] == '2'
    assert rows[1]['strong_bridge_margin_A_minus_D'] == '1'
    report['collision_free_order_obstruction'] = {
        'source_instance': 'examples/customer_attraction/collision_free_occupancy.json',
        'source_strategy': 'evidence/certificates/customer_attraction/collision_free_occupancy.json',
        'checked_histories': valid.checked_histories,
        'checked_nonself_deviations': valid.checked_deviations,
        'OPT': 5, 'W': 4, 'actual_path': ['C', 'D'],
        'scope': 'this family refutes arbitrary-order D<=A; selectable-order bridge is separately refuted by PFR-OPT',
        'orders': rows}

    partition = Instance(('A', 'B', 'T', 'S', 'Q', 'R'), tuple(
        CustomerType(frozenset(t), w) for t, w in [
            ([3], 2), ([3, 4], 1), ([2], 2), ([2, 5], 1),
            ([1], 2), ([1, 5], 1), ([1, 4], 1),
            ([0, 3, 4, 5], 2), ([0, 2, 4, 5], 2)]), 2)
    replies = (1, 4, 4, 5, 5, 4)
    certificate = StrategyCertificate(
        {(): 0, **{(a,): reply for a, reply in enumerate(replies)}},
        partition.counts((0, 1)))
    valid = verify_certificate(partition, certificate)
    valid.assert_valid()
    opt = partition.optimal_welfare()
    optimal_pairs = [pair for pair in combinations_with_replacement(range(6), 2)
                     if partition.welfare(partition.counts(pair)) == opt]
    assert optimal_pairs == [(2, 3)]
    rows = [identity(partition, certificate, Ts) for Ts in ((2, 3), (3, 2))]
    assert all(row['chi'] == '1' and row['D'] == '1'
               and row['A'] == '0' and row['last_owner_frozen_query'] == '9'
               and row['unused_actual_capacity'] == '7' for row in rows)
    report['existing_optimal_partition_counterexample'] = {
        'source': 'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_boss/partition_attack/optimal_partition_counterexample.md',
        'instance': partition.to_dict(), 'strategy': certificate.to_dict(),
        'checked_histories': valid.checked_histories,
        'checked_nonself_deviations': valid.checked_deviations,
        'unique_optimal_unordered_pair': ['T', 'S'], 'OPT': opt, 'W': 8,
        'scope': 'even selectable optimal source multiset/order D<=A is false',
        'orders': rows}

    target = HERE / 'single_kernel_audit.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in
                      ('existing_root_tax_SPE', 'local_toll_bridge_counterexample',
                       'collision_free_order_obstruction',
                       'existing_optimal_partition_counterexample')}, ensure_ascii=False))
    print('root-tax SPE: 259 histories, 1295 nonself deviations; chi in [23,53/2]')
    print('local bridge: q_min=12 > u_1=35/3; exact complete SPE verified')
    print('collision-free: aligned optimal order chi=0, D-A=1; swapped order chi=2')
    print('PFR-OPT: both unique optimal orders chi=1, V_last=9>W=8, D-A=1')


if __name__ == '__main__':
    main()
