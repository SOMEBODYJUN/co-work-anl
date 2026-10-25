"""Full-original-strategy input QA for the actual-third 747-row interface.

Inputs are frozen complete-strategy JSONs, never author constructors or the
canonical game/solver. Unit customers, all continuations, optimal tuples,
menus and per-customer atoms are reconstructed here. The tested rows() is
imported only to compare its aggregated coefficients with direct semantics.
This is finite implementation QA, not a universal theorem or search.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import importlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE / 'certificate'))
tested = importlib.import_module('two_real_weighted_branches')
LABELS = 'ABCDEUVWXY'
OLD_NODES = {'actual': range(5), 'second': range(2, 5), 'third': range(3, 5)}
TYPES3 = list(product((0, 1), repeat=3))
TYPES4 = list(product((0, 1), repeat=4))


class Strategy:
    def __init__(self, obj):
        inst = obj['instance']
        self.p = len(inst['topics'])
        self.names = inst['topics']
        self.m = inst['players']
        assert self.m == 5
        self.clients = tuple(frozenset(c['topics'])
                             for c in inst['customers']
                             for _ in range(c['multiplicity']))
        cert = obj['certificate']
        self.sigma = {tuple(a['history']): a['action'] for a in cert['actions']}
        assert len(self.sigma) == len(cert['actions'])
        assert set(self.sigma) == {h for d in range(5)
                                  for h in product(range(self.p), repeat=d)}
        assert all(a in range(self.p) for a in self.sigma.values())
        self.topics = tuple(frozenset(x for x, c in enumerate(self.clients) if a in c)
                            for a in range(self.p))
        self.checked = 0
        self.slacks = []
        for h, a in self.sigma.items():
            z = self.follow(h)
            for b in range(self.p):
                self.slacks.append(self.utility(z, len(h))
                                   - self.utility(self.follow(h + (b,)), len(h)))
                self.checked += 1
        assert min(self.slacks) >= 0

    @lru_cache(None)
    def follow(self, h):
        return h if len(h) == 5 else self.follow(h + (self.sigma[h],))

    @lru_cache(None)
    def loads(self, h):
        return tuple(sum(a in c for a in h) for c in self.clients)

    @lru_cache(None)
    def utility(self, z, role):
        a = z[role]
        load = self.loads(z)
        return sum((F(1, load[x]) for x in self.topics[a]), F())

    def coverage(self, z):
        return sum(n > 0 for n in self.loads(z))

    def weighted_size(self, a, prefix, remaining):
        old = self.loads(prefix)
        return sum((F(1, old[x] + remaining) for x in self.topics[a]), F())

    def floor_account(self, prefix, action):
        """Check a literal original-sigma deviation before using its floor."""
        role = len(prefix)
        real = self.utility(self.follow(prefix), role)
        deviated = self.utility(self.follow(prefix + (action,)), role)
        floor = self.weighted_size(action, prefix, 5 - role)
        assert real >= deviated >= floor
        return real - floor, real - deviated, deviated - floor


def make_input(name, obj, source_path=None):
    game = Strategy(obj)
    actual = game.follow(())
    A, B, C, D, E = actual
    second = game.follow((A, E))
    third = game.follow((A, B, E))
    oldpaths = {'actual': actual, 'second': second, 'third': third}
    labels = dict(zip('ABCDE', actual))
    labels.update(dict(zip('UVW', second[2:])))
    labels.update(dict(zip('XY', third[3:])))
    candidates = list(combinations_with_replacement(range(game.p), 5))
    optimum = max(game.coverage(z) for z in candidates)
    optimal = next(z for z in candidates if game.coverage(z) == optimum)
    # One canonical bare maximum suffices. All weighted-H ties are replayed.
    M = max(range(game.p), key=lambda a: (len(game.topics[a]), -a))
    maxpath = game.follow((M,))
    abpaths = [game.follow((A, B, t)) for t in optimal]
    aepaths = [game.follow((A, E, t)) for t in optimal]
    sbpaths = [game.follow((A, t)) for t in optimal]
    menus = {
        'AB': {'mX': tuple(z[3] for z in abpaths), 'mY': tuple(z[4] for z in abpaths)},
        'AE': {'mX': tuple(z[3] for z in aepaths), 'mY': tuple(z[4] for z in aepaths)},
        'Sbranch': {'mU': tuple(z[2] for z in sbpaths),
                    'mV': tuple(z[3] for z in sbpaths), 'mW': tuple(z[4] for z in sbpaths)},
    }
    last_menus = [tuple(game.sigma[path[:3] + (t,)] for t in optimal)
                  for path in (actual, second, third)]
    prefix = actual[:2]
    max_weight = max(game.weighted_size(a, prefix, 3) for a in range(game.p))
    Hties = [a for a in range(game.p) if game.weighted_size(a, prefix, 3) == max_weight]
    cases = []
    for H in Hties:
        child = game.follow(prefix + (H,))
        HQR = child[2:]
        atoms = []
        for client in game.clients:
            bit = lambda a: int(a in client)
            hist3 = lambda paths: [sum((bit(t), bit(z[3]), bit(z[4])) == pat
                                      for t, z in zip(optimal, paths)) for pat in TYPES3]
            hist4 = [sum((bit(t), bit(z[2]), bit(z[3]), bit(z[4])) == pat
                         for t, z in zip(optimal, sbpaths)) for pat in TYPES4]
            atom = {
                'bits': ''.join(str(bit(labels[t])) for t in LABELS),
                'AB_hist': hist3(abpaths), 'AE_hist': hist3(aepaths),
                'second_hist': hist4,
                'menus_lh': [[sum(bit(l) for l in ls),
                              sum(bit(t) * bit(l) for t, l in zip(optimal, ls))]
                             for ls in last_menus],
                'max_bits': ''.join(str(bit(a)) for a in maxpath),
            }
            atoms.append((atom, tuple(bit(a) for a in HQR)))

        dummy = {'bits': '0' * 10, 'AB_hist': [5] + [0] * 7,
                 'AE_hist': [5] + [0] * 7, 'second_hist': [5] + [0] * 15,
                 'menus_lh': [[0, 0]] * 3, 'max_bits': '0' * 5}
        names = tuple(tested.rows(dummy, (0, 0, 0), 'actual'))
        assert len(names) == 747
        aggregate = {n: F() for n in names}
        for atom, hidden in atoms:
            coeffs = tested.rows(atom, hidden, 'actual')
            assert tuple(coeffs) == names
            for n in names:
                aggregate[n] += coeffs[n]

        def query(token, tag=None):
            if tag is not None and token in menus[tag]:
                return menus[tag][token]
            if token == 'opt':
                return optimal
            if token.startswith('z'):
                return (maxpath[int(token[1:])],)
            if token.startswith('f'):
                return (HQR[int(token[1:])],)
            return (labels[token],)

        source_u = game.utility(actual, 2)
        vh, vq, vr = [game.utility(child, i) for i in range(2, 5)]
        qprefix, rprefix = child[:3], child[:4]
        background = game.loads(qprefix)
        taxQ = sum((F(1, (background[x] + 1) * (background[x] + 2))
                    for x in game.topics[HQR[1]]), F())
        Htax = vq + vr + taxQ
        floor_details = []
        ap_details = []

        @lru_cache(None)
        def tax_pair(t, s):
            """Three actual-sigma ICs plus genuine set-intersection remainder."""
            reply = game.sigma[qprefix + (t,)]
            zt = qprefix + (t, reply)
            zts = qprefix + (t, s)
            zqr = qprefix + (HQR[1], reply)
            ic1 = vq - game.utility(zt, 3)
            ic2 = game.utility(zt, 4) - game.utility(zts, 4)
            ic3 = vr - game.utility(zqr, 4)
            assert min(ic1, ic2, ic3) >= 0
            g = lambda a, b: sum((F(1, (background[x] + 1) * (background[x] + 2))
                                  for x in game.topics[a] & game.topics[b]), F())
            remainder = g(HQR[1], HQR[1]) - g(HQR[1], reply) + g(t, s)
            assert remainder >= 0
            direct = Htax - game.utility(zts, 3) - game.utility(zts, 4)
            assert direct == ic1 + ic2 + ic3 + remainder >= 0
            return direct

        @lru_cache(None)
        def ap_pair(t, s):
            """Original Q node, arbitrary legal C=t,D=s, k=2 background AP."""
            # Source Q is a true optimizer. Its deviation and every theme's
            # conservative weighted size are independently checked from sigma.
            vdiff, ic, floor_gap = game.floor_account(qprefix, t)
            assert vdiff >= 0
            csize = game.weighted_size(t, qprefix, 2)
            inter = game.topics[t] & game.topics[s]
            outside = game.topics[s] - game.topics[t]
            Fcs = (sum((F(1, background[x] + 2) for x in inter), F())
                   + sum((F(1, background[x] + 1) for x in outside), F()))
            # Open the actual C-deviation in the original full strategy.
            # Its AP amount is paid by true IC and missing-seat/outside
            # accounts, rather than merely matching a coefficient formula.
            reply = game.sigma[qprefix + (t,)]
            forced_C = qprefix + (t, reply)
            vc = game.utility(forced_C, 3)
            last = game.utility(forced_C, 4)
            missing = sum((F(1, background[x] + 2)
                           for x in game.topics[t] - game.topics[reply]), F())
            eta = vq - csize
            gd = 4 * (vc - csize) - missing
            outside_residual = vc + F(3, 4) * missing + 2 * eta - last
            last_IC = last - Fcs
            assert min(eta, gd, outside_residual, last_IC, vq - vc) >= 0
            game.floor_account(qprefix, reply)
            # Twice the independently stated arbitrary-theme background AP
            # margin, using actual new Q profit, never an ancestor profit.
            direct = 2 * (6 * vq - 5 * csize - Fcs)
            assert direct == 2 * (4 * (vq - vc) + F(3, 4) * gd
                                  + outside_residual + last_IC) >= 0
            ap_details.append({'C': t, 'D': s, 'current_Q': str(vq),
                               'current_Q_IC': str(ic), 'floor_residual': str(floor_gap),
                               'forced_C_path': list(forced_C),
                               'missing_seat_account': str(gd),
                               'outside_incidence_account': str(outside_residual),
                               'true_response_last_IC': str(last_IC),
                               'AP_margin': str(direct)})
            return direct

        def semantic(name):
            parts = name.split(':')
            if parts[0] == 'trueH':
                kind = parts[1]
                if kind == 'source-IC':
                    return source_u - vh
                if kind == 'global-size':
                    return F(len(game.topics[M]) - len(game.topics[HQR[int(parts[2])]]))
                if kind == 'oldK':
                    pn, i, j = parts[2], int(parts[3]), int(parts[4])
                    assert i in OLD_NODES[pn]
                    path = oldpaths[pn]
                    value, ic, rest = game.floor_account(path[:i], HQR[j])
                    floor_details.append((name, value, ic, rest))
                    return value
                if kind == 'maxK':
                    i, j = int(parts[2]), int(parts[3])
                    assert i in range(1, 5)
                    value, ic, rest = game.floor_account(maxpath[:i], HQR[j])
                    floor_details.append((name, value, ic, rest))
                    return value
                if kind == 'weighted-cap':
                    qs = query(parts[2])
                    return len(qs) * max_weight - sum((game.weighted_size(t, prefix, 3) for t in qs), F())
                if kind in ('Q', 'R'):
                    assert parts[2] == 'K'
                    pr = qprefix if kind == 'Q' else rprefix
                    return sum((game.floor_account(pr, t)[0] for t in query(parts[3])), F())
                assert kind == 'tax'
                return sum((tax_pair(t, s) for t in query(parts[2]) for s in query(parts[3])), F())
            tag, marker, kind = parts[:3]
            assert tag in menus and marker == 'trueH'
            if kind == 'weighted-cap':
                qs = query(parts[3], tag)
                return len(qs) * max_weight - sum((game.weighted_size(t, prefix, 3) for t in qs), F())
            if kind in ('Q', 'R'):
                if parts[3] == 'K':
                    pr = qprefix if kind == 'Q' else rprefix
                    return sum((game.floor_account(pr, t)[0] for t in query(parts[4], tag)), F())
                assert kind == 'Q' and parts[3] == 'AP'
                return sum((ap_pair(t, s) for t in query(parts[4], tag)
                            for s in query(parts[5], tag)), F())
            assert kind == 'tax'
            return sum((tax_pair(t, s) for t in query(parts[3], tag)
                        for s in query(parts[4], tag)), F())

        direct = {n: semantic(n) for n in names}
        assert direct == aggregate, [(n, direct[n], aggregate[n]) for n in names if direct[n] != aggregate[n]]
        assert min(aggregate.values()) >= 0
        source_last_to_H = game.floor_account(actual[:4], H)[0]
        forced_last_to_H = game.floor_account(rprefix, H)[0]
        assert aggregate['trueH:oldK:actual:4:0'] == source_last_to_H
        assert aggregate['trueH:R:K:f0'] == forced_last_to_H
        cases.append({
            'weighted_max_H': H, 'weighted_max_value': str(max_weight),
            'genuine_forced_H_path': list(child),
            'forced_H_Q_R_profits': list(map(str, (vh, vq, vr))),
            'row_count': len(names), 'minimum_row_slack': str(min(aggregate.values())),
            'zero_rows': sum(v == 0 for v in aggregate.values()),
            'direct_semantic_row_matches': len(direct),
            'old_and_max_floor_accounts': len(floor_details),
            'minimum_real_IC_in_floor_accounts': str(min((r[2] for r in floor_details), default=F())),
            'minimum_floor_remainder': str(min((r[3] for r in floor_details), default=F())),
            'distinct_true_Q_AP_pairs': len(ap_details),
            'minimum_AP_missing_seat_account': str(min((F(a['missing_seat_account']) for a in ap_details), default=F())),
            'minimum_AP_outside_incidence_account': str(min((F(a['outside_incidence_account']) for a in ap_details), default=F())),
            'minimum_AP_true_last_IC': str(min((F(a['true_response_last_IC']) for a in ap_details), default=F())),
            'source_last_to_H_slack': str(source_last_to_H),
            'forced_last_R_to_H_slack': str(forced_last_to_H),
            'old_root_source_profit': str(game.utility(actual, 0)),
            'old_root_profit_in_forced_child': str(game.utility(child, 0)),
            'oldK_root_H_floor_slack': str(aggregate['trueH:oldK:actual:0:0']),
            'oldK_root_H_conservative_floor': str(game.weighted_size(H, (), 5)),
            'per_customer_atoms': [dict(a, hidden_HQR=list(s)) for a, s in atoms],
            'true_Q_AP_kernel_accounts': ap_details,
            'exact_row_slacks': {n: str(v) for n, v in aggregate.items()},
        })
    return {
        'name': name, 'source_path': str(source_path) if source_path else 'inline zero-customer singleton-empty game',
        'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest() if source_path else None,
        'unit_customers': len(game.clients), 'topics': game.p,
        'full_strategy_histories': len(game.sigma), 'full_strategy_comparisons_including_self': game.checked,
        'minimum_full_strategy_IC_slack': str(min(game.slacks)),
        'actual_path': list(actual), 'actual_profits': [str(game.utility(actual, i)) for i in range(5)],
        'OPT_5': optimum, 'optimal_five_tuple': list(optimal),
        'bare_max_theme': M, 'genuine_max_root_path': list(maxpath),
        'old_second_E_path': list(second), 'old_third_E_path': list(third),
        'weighted_max_H_ties_checked': Hties,
        'reconstructed_indexed_menus': menus,
        'cases': cases,
    }


def main():
    paths = [BASE / 'direct' / 'weighted_maximum_old_refund_obstruction.json',
             HERE / 'terminal_share_padding_exact.json']
    inputs = [make_input(p.stem, json.loads(p.read_text()), p) for p in paths]
    empty = {'instance': {'topics': ['empty'], 'customers': [], 'players': 5},
             'certificate': {'terminal_counts': [5],
                             'actions': [{'history': [0] * d, 'action': 0} for d in range(5)]}}
    inputs.append(make_input('zero_customers_unique_empty', empty))
    cases = [c for inp in inputs for c in inp['cases']]
    report = {
        'scope': 'Finite full-original-sigma implementation QA for all 747 actual-third HQR rows; not a universal proof, catalogue search, or HALF5 certificate.',
        'independence': 'Standard-library reconstruction from complete-strategy JSON; no canonical model/solver/verifier or author input constructor. Tested rows interface imported only after ground input reconstruction rules were fixed.',
        'tested_row_module_sha256': hashlib.sha256(Path(tested.__file__).read_bytes()).hexdigest(),
        'input_games': len(inputs), 'genuine_weighted_H_cases': len(cases),
        'total_747_row_aggregations_and_semantic_matches': sum(c['row_count'] for c in cases),
        'total_full_strategy_comparisons_including_self': sum(i['full_strategy_comparisons_including_self'] for i in inputs),
        'all_exact_aggregates_nonnegative': True,
        'all_direct_semantic_matches': True,
        'inputs': inputs,
    }
    out = HERE / 'audit_full_actual_branch_inputs.json'
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'inputs'}, indent=2))
    for inp in inputs:
        print(json.dumps({k: v for k, v in inp.items() if k not in ('cases', 'reconstructed_indexed_menus')}, indent=2))


if __name__ == '__main__':
    main()
