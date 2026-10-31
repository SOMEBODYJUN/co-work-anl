"""Unrestricted-history outcome witnesses on a symmetric INPUT class.

The last p-d themes are interchangeable in the customer input. This imposes
no equivariance on a pure strategy. Outcome pairs and marked-action triples
are quotiented by simultaneous permutations of those themes. The MILP is a
floating candidate generator; extracted complete strategies require exact
fixed-cone recovery and definition-level verification.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import importlib.util
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests/audits'))
from customer_attraction import (ExactSPESolver, StrategyCertificate,
                                verify_certificate)
from customer_attraction_strategy_lp import (StrategyCone, coverage_row,
    dot, integer_clones, instance_from_clones, payoff_row, serializable)


def compositions(p, total):
    if p == 1:
        yield (total,)
    else:
        for x in range(total + 1):
            for tail in compositions(p - 1, total - x):
                yield (x,) + tail


def inc(q, a):
    return q[:a] + (q[a] + 1,) + q[a + 1:]


class SymmetricDAG:
    def __init__(self, p, d, m):
        assert 1 <= d <= p and m >= 1
        self.p, self.d, self.m = p, d, m
        self.leaves = tuple(compositions(p, m))
        self.states = sorted({self.ck(k) for depth in range(m + 1)
                              for k in compositions(p, depth)},
                             key=lambda k: (sum(k), k))
        self.orbits = defaultdict(list)
        for mask in range(1, 1 << p):
            self.orbits[mask & ((1 << d) - 1), (mask >> d).bit_count()].append(mask)
        self.orbits = dict(sorted(self.orbits.items()))
        self.rkeys = tuple(self.orbits)
        self.mask_to_r = {mask: j for j, key in enumerate(self.rkeys)
                          for mask in self.orbits[key]}
        self.pairs = {}
        self.triples = {}
        for k in self.states:
            raw = [c for c in self.leaves if all(v <= w for v, w in zip(k, c))]
            self.pairs[k] = sorted({self.cp(k, c) for c in raw})
            if sum(k) < m:
                self.triples[k] = sorted({self.ct(k, c, a) for c in raw
                                         for a in range(p) if c[a] > k[a]})

    def ck(self, k):
        return tuple(k[:self.d]) + tuple(sorted(k[self.d:]))

    def cp(self, k, c):
        tail = sorted(zip(k[self.d:], c[self.d:]))
        return (tuple(k[:self.d]) + tuple(x for x, _ in tail),
                tuple(c[:self.d]) + tuple(x for _, x in tail))

    def ct(self, k, c, a):
        order = list(range(self.d)) + sorted(range(self.d, self.p),
            key=lambda b: (k[b], c[b], int(b == a)))
        return (tuple(k[b] for b in order), tuple(c[b] for b in order),
                order.index(a))

    def action_class(self, k, a):
        return (0, a) if a < self.d else (1, k[a])

    def reduce(self, full_row):
        row = [Fraction(0)] * len(self.rkeys)
        for mask, v in enumerate(full_row, 1):
            row[self.mask_to_r[mask]] += v
        return tuple(row)

    def build(self, q, J, seconds, fixed_clones=None, floor=None, path=None,
              outside_order=None, warm_start=False, noncontainment_floor=None):
        p, m = self.p, self.m
        q = tuple(q)
        assert len(q) == p and sum(q) == m and not any(q[self.d:])
        root = (0,) * p
        y, z, x, t = {}, {}, {}, {}
        idx = len(self.rkeys)
        for k in self.states:
            for pair in self.pairs[k]:
                y[pair] = idx
                idx += 1
            if sum(k) < m:
                t[k] = idx
                idx += 1
                for triple in self.triples[k]:
                    z[triple] = idx
                    x[triple] = idx + 1
                    idx += 2
        lo, hi = np.zeros(idx), np.ones(idx)
        if outside_order is not None:
            for j, key in enumerate(self.rkeys):
                if key[1] > outside_order:
                    hi[j] = 0
        integrality = np.zeros(idx, dtype=np.uint8)
        for j in (*y.values(), *z.values(), *x.values()):
            integrality[j] = 1
        for k in self.states:
            if sum(k) == m:
                lo[y[k, k]] = 1
        for pair in self.pairs[root]:
            lo[y[pair]] = hi[y[pair]] = int(pair[1] == q)
        if path is not None:
            k = root
            for a in path:
                lo[z[self.ct(k, q, a)]] = 1
                k = inc(k, a)
            assert k == q
        if fixed_clones is not None:
            scale = sum(v * fixed_clones[j] for j, v in
                        enumerate(coverage_row(p, [a for a, v in enumerate(q) if v])))
            assert scale > 0
            for j, key in enumerate(self.rkeys):
                vals = {fixed_clones[mask - 1] for mask in self.orbits[key]}
                assert len(vals) == 1, 'input is not symmetric'
                lo[j] = hi[j] = float(Fraction(vals.pop(), scale))
        rr, cc, vv, lb, ub = [], [], [], [], []

        def add(row, lower=-np.inf, upper=np.inf):
            i = len(lb)
            for j, v in row.items():
                if v:
                    rr.append(i); cc.append(j); vv.append(float(v))
            lb.append(lower); ub.append(upper)

        def indexed(row):
            return {j: v for j, v in enumerate(row) if v}

        welfare = self.reduce(coverage_row(p, [a for a, v in enumerate(q) if v]))
        add(indexed(welfare), 1, 1)
        objective = self.reduce(coverage_row(p, J))
        if floor is not None:
            add(indexed(objective), lower=floor)
        # Valid for every root SPE; all propagated payoffs are then <=1.
        for a in range(p):
            sizes = self.reduce(tuple(Fraction(bool(mask & (1 << a)))
                                      for mask in range(1, 1 << p)))
            add(indexed(sizes), upper=1)
        if noncontainment_floor is not None:
            for a in range(p):
                for b in range(p):
                    if a == b:
                        continue
                    separator = self.reduce(tuple(Fraction(bool(mask & (1 << a))
                        and not bool(mask & (1 << b))) for mask in range(1, 1 << p)))
                    add(indexed(separator), lower=noncontainment_floor)
        # Stronger on-path size guarantees, independent of credible replies.
        for a, n in enumerate(q):
            if not n:
                continue
            own = self.reduce(payoff_row(p, q, a))
            for b in range(p):
                row = self.reduce(tuple(Fraction(bool(mask & (1 << b)))
                                        for mask in range(1, 1 << p)))
                add(indexed(tuple(v - m * u for v, u in zip(row, own))), upper=0)
        for k in t:
            actions_per_pair = defaultdict(list)
            continuations_per_action = defaultdict(list)
            for triple in self.triples[k]:
                _, c, a = triple
                actions_per_pair[self.cp(k, c)].append(triple)
                continuations_per_action[self.action_class(k, a)].append(triple)
                child = self.cp(inc(k, a), c)
                row = self.reduce(payoff_row(p, c, a))
                add({z[triple]: 1, y[child]: -1}, upper=0)
                zz = {z[triple]: 1, t[k]: 1}
                for j, v in enumerate(row):
                    if v:
                        zz[j] = -v
                add(zz, upper=1)
                add({x[triple]: 1, y[child]: -1}, upper=0)
                xx = {x[triple]: 1, t[k]: -1}
                for j, v in enumerate(row):
                    if v:
                        xx[j] = v
                add(xx, upper=1)
            for pair in self.pairs[k]:
                row = {y[pair]: -1}
                row.update({z[triple]: 1 for triple in actions_per_pair[pair]})
                add(row, 0, 0)
            for triples in continuations_per_action.values():
                add({x[triple]: 1 for triple in triples}, 1, 1)
        cost = np.zeros(idx)
        cost[:len(self.rkeys)] = -np.array(objective, dtype=float)
        matrix = coo_matrix((vv, (rr, cc)), shape=(len(lb), idx)).tocsc()
        started = time.monotonic()
        seed_status = None
        if warm_start:
            # A complete feasible witness from the known all-big lower-bound
            # family, with the d distinguished labels sharing its big theme.
            # This is a numerical solver start, never a new mathematical bound.
            from scipy.optimize._highspy import _core
            clones = [0] * ((1 << p) - 1)
            clones[(1 << self.d) - 2] = m
            for a in range(self.d, p):
                clones[(1 << a) - 1] = 1
            if noncontainment_floor is not None:
                clones = [10 * a for a in clones]
                for a in range(self.d):
                    clones[(1 << a) - 1] += 1
            inst = instance_from_clones(p, m, clones)
            solver = ExactSPESolver(inst)
            assert q in solver.outcomes()
            scale = inst.welfare(q)
            seed = np.zeros(idx)
            for j, key in enumerate(self.rkeys):
                seed[j] = clones[self.orbits[key][0] - 1] / scale
            for k in self.states:
                outcomes = solver.outcomes(k)
                for pair in self.pairs[k]:
                    seed[y[pair]] = int(pair[1] in outcomes and (k != root or pair[1] == q))
                if sum(k) == m:
                    continue
                threshold = solver.threshold(k)
                seed[t[k]] = float(threshold / scale)
                for pair in self.pairs[k]:
                    if not seed[y[pair]]:
                        continue
                    c = pair[1]
                    eligible = [a for a in range(p) if c[a] > k[a]
                        and c in solver.outcomes(inc(k, a))
                        and inst.topic_payoff(a, c) >= threshold]
                    a = min(eligible)
                    seed[z[self.ct(k, c, a)]] = 1
                classes = {}
                for a in range(p):
                    classes.setdefault(self.action_class(k, a), a)
                for a in classes.values():
                    c = min(solver.outcomes(inc(k, a)),
                            key=lambda c: (inst.topic_payoff(a, c), c))
                    seed[x[self.ct(k, c, a)]] = 1
            residual = matrix @ seed
            feasible_seed = bool(np.all(seed >= lo - 1e-7) and np.all(seed <= hi + 1e-7)
                and np.all(residual >= np.array(lb) - 1e-7)
                and np.all(residual <= np.array(ub) + 1e-7))
            lp = _core.HighsLp()
            lp.num_col_, lp.num_row_ = idx, len(lb)
            lp.col_cost_, lp.col_lower_, lp.col_upper_ = cost, lo, hi
            lp.row_lower_, lp.row_upper_ = np.array(lb), np.array(ub)
            lp.integrality_ = [_core.HighsVarType.kInteger if v else
                               _core.HighsVarType.kContinuous for v in integrality]
            lp.a_matrix_.format_ = _core.MatrixFormat.kColwise
            lp.a_matrix_.num_col_, lp.a_matrix_.num_row_ = idx, len(lb)
            lp.a_matrix_.start_ = matrix.indptr.astype(np.int32)
            lp.a_matrix_.index_ = matrix.indices.astype(np.int32)
            lp.a_matrix_.value_ = matrix.data
            high = _core._Highs()
            high.setOptionValue('output_flag', False)
            high.setOptionValue('time_limit', float(seconds))
            high.setOptionValue('mip_rel_gap', 0.0)
            high.passModel(lp)
            if feasible_seed:
                high.setSolution(idx, np.arange(idx, dtype=np.int32), seed)
            high.run()
            solution, info = high.getSolution(), high.getInfo()
            result = SimpleNamespace(x=np.array(solution.col_value) if solution.value_valid else None,
                fun=info.objective_function_value if solution.value_valid else None,
                status=int(high.getModelStatus()), message=str(high.getModelStatus()))
            seed_status = {'provided': feasible_seed, 'objective': -float(cost @ seed)}
        else:
            result = milp(cost, integrality=integrality, bounds=Bounds(lo, hi),
                          constraints=LinearConstraint(matrix, lb, ub),
                          options={'time_limit': seconds, 'mip_rel_gap': 0.0})
        meta = {'topics': p, 'distinguished_topics': self.d, 'players': m,
                'root_counts': q, 'portfolio': J, 'path': path,
                'outside_order': outside_order,
                'noncontainment_floor': noncontainment_floor,
                'variables': idx, 'binary': len(y) + len(z) + len(x),
                'customer_orbits': len(self.rkeys), 'prefix_orbits': len(self.states),
                'rows': len(lb), 'status': int(result.status),
                'warm_start': seed_status,
                'message': result.message, 'seconds': time.monotonic() - started,
                'floating_value': float(-result.fun) if result.fun is not None else None,
                'floating_bound_not_a_certificate': True}
        if result.x is None:
            return None, meta
        actions = {}

        def expand(h, k, c):
            if len(h) == m:
                assert k == c
                return
            admissible = [a for a in range(p) if c[a] > k[a]]
            a = max(admissible, key=lambda a: result.x[z[self.ct(k, c, a)]])
            assert result.x[z[self.ct(k, c, a)]] > .9
            actions[h] = a
            for b in range(p):
                if a == b:
                    next_c = c
                else:
                    child = inc(k, b)
                    feasible = [v for v in self.leaves
                                if all(xx <= yy for xx, yy in zip(child, v))]
                    next_c = max(feasible, key=lambda v: result.x[x[self.ct(k, v, b)]])
                    assert result.x[x[self.ct(k, next_c, b)]] > .9
                expand(h + (b,), inc(k, b), next_c)

        expand((), root, q)
        cert = StrategyCertificate(actions, q)
        floats = [result.x[self.mask_to_r[mask]] for mask in range(1, 1 << p)]
        return (cert, floats), meta


def verify_fixed(dag, clones, q, seconds=5):
    inst = instance_from_clones(dag.p, dag.m, clones)
    canonical = q in ExactSPESolver(inst).outcomes()
    if not inst.welfare(q):
        assert not canonical and inst.optimal_welfare() > 0
        return {'q': q, 'canonical_reachable': False,
                'milp_status': 'excluded_by_zero_W_normalization',
                'verified_full_histories': 0}
    found, meta = dag.build(q, tuple(range(dag.p)), seconds, fixed_clones=clones)
    if found is not None:
        cert, _ = found
        ver = verify_certificate(inst, cert)
        ver.assert_valid()
    assert (found is not None) == canonical, (q, canonical, meta)
    return {'q': q, 'canonical_reachable': canonical, 'milp_status': meta['status'],
            'verified_full_histories': len(found[0].actions) if found else 0}


def regression():
    records = []
    for p, d, m in ((3, 1, 3), (4, 2, 3)):
        dag = SymmetricDAG(p, d, m)
        for kind in range(6):
            values = {key: 1 + ((7 * i + kind * 3) % 4)
                      for i, key in enumerate(dag.rkeys)}
            if kind == 3:
                values = {key: int(key == ((1 << d) - 1, p - d))
                          for key in dag.rkeys}
            if kind == 4:
                values = {key: (m if key == (1, 0) else
                                int(key == (0, 1))) for key in dag.rkeys}
            if kind == 5:
                values = {key: (m - 1 if key == (1, 0) else
                                int(key == (0, 1) or key == (2, 0)))
                          for key in dag.rkeys}
            clones = tuple(values[dag.rkeys[dag.mask_to_r[mask]]]
                           for mask in range(1, 1 << p))
            for q0 in compositions(d, m):
                q = q0 + (0,) * (p - d)
                records.append({'p': p, 'd': d, 'm': m, 'kind': kind,
                                **verify_fixed(dag, clones, q)})
    return records


def exact_symmetric_point(dag, cone, J, outside_order=None, noncontainment_floor=None):
    """Reoptimize a fixed extracted strategy while retaining input symmetry."""
    rows = set(dag.reduce(row) for row in cone.rows)
    w = dag.reduce(cone.welfare)
    v = dag.reduce(coverage_row(dag.p, J))
    if outside_order is not None:
        for j, key in enumerate(dag.rkeys):
            if key[1] > outside_order:
                rows.add(tuple(Fraction(-int(i == j)) for i in range(len(dag.rkeys))))
    if noncontainment_floor is not None:
        sep_floor = Fraction(str(noncontainment_floor))
        for a in range(dag.p):
            for b in range(dag.p):
                if a == b:
                    continue
                sep = dag.reduce(tuple(Fraction(bool(mask & (1 << a))
                    and not bool(mask & (1 << b))) for mask in range(1, 1 << dag.p)))
                rows.add(tuple(x - sep_floor * y for x, y in zip(sep, w)))
    rows = tuple(sorted(rows))
    reduced = SimpleNamespace(rows=rows, welfare=w)
    res = linprog(-np.array(v, dtype=float), A_ub=-np.array(rows, dtype=float),
                  b_ub=np.zeros(len(rows)), A_eq=[np.array(w, dtype=float)], b_eq=[1],
                  bounds=(0, None), method='highs')
    if not res.success:
        return {'certified': False, 'status': res.message}
    values = tuple(Fraction(float(a)).limit_denominator(10**7) for a in res.x)

    def feasible(z):
        return z is not None and all(a >= 0 for a in z) and dot(w, z) == 1 \
            and all(dot(row, z) >= 0 for row in rows)

    if not feasible(values):
        values = StrategyCone.recover_vertex(reduced, res.x)
    if not feasible(values):
        return {'certified': False, 'status': 'exact_symmetric_recovery_failed'}
    expanded = tuple(values[dag.mask_to_r[mask]] for mask in range(1, 1 << dag.p))
    clones = integer_clones(expanded)
    inst = instance_from_clones(dag.p, dag.m, clones)
    cert = StrategyCertificate(cone.actions, cone.root)
    verification = verify_certificate(inst, cert)
    verification.assert_valid()
    beta = Fraction(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
    mu = tuple(Fraction(float(-a)).limit_denominator(10**7)
               for a in res.ineqlin.marginals)
    dual_ok = all(a >= 0 for a in mu) and all(beta * w[j] - sum(
        a * row[j] for a, row in zip(mu, rows)) >= v[j] for j in range(len(w)))
    return {'certified': True, 'value': dot(v, values), 'integer_clones': clones,
            'instance': inst.to_dict(), 'same_strategy_as_exact_candidate': True,
            'welfare': inst.welfare(cone.root), 'optimal_welfare': inst.optimal_welfare(),
            'canonical_definition_verified': True, 'exact_dual_bound': beta if dual_ok else None,
            'dual_optimal': dual_ok and beta == dot(v, values),
            'outside_order': outside_order, 'noncontainment_floor': noncontainment_floor,
            'symmetric_orbit_values': [(key, a) for key, a in zip(dag.rkeys, values) if a]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--distinct', type=int, default=2)
    ap.add_argument('--root', default='3,2,0,0,0,0,0')
    ap.add_argument('--portfolio', default='2,3,4,5,6')
    ap.add_argument('--path')
    ap.add_argument('--outside-order', type=int)
    ap.add_argument('--warm-start', action='store_true')
    ap.add_argument('--noncontainment-floor', type=float)
    ap.add_argument('--floor', type=float)
    ap.add_argument('--seconds', type=float, default=30)
    ap.add_argument('--regression', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.regression:
        report = {'scope': 'finite fixed-input regression against canonical all-SPE BI',
                  'cases': regression()}
    else:
        dag = SymmetricDAG(args.topics, args.distinct,
                           sum(map(int, args.root.split(','))))
        q = tuple(map(int, args.root.split(',')))
        J = tuple(map(int, args.portfolio.split(',')))
        path = tuple(map(int, args.path.split(','))) if args.path else None
        found, meta = dag.build(q, J, args.seconds, floor=args.floor, path=path,
                                outside_order=args.outside_order, warm_start=args.warm_start,
                                noncontainment_floor=args.noncontainment_floor)
        exact = None
        symmetric_exact = None
        if found:
            cert, _ = found
            cone = StrategyCone(args.topics, sum(q), dict(cert.actions))
            source = ROOT / 'research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search/outcome_dag_milp.py'
            spec = importlib.util.spec_from_file_location('original_dag', source)
            old = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(old)
            exact = old.exact_optimize(cone, coverage_row(args.topics, J))
            if exact.get('certified'):
                inst = instance_from_clones(args.topics, sum(q), exact['integer_clones'])
                verification = verify_certificate(inst, cert)
                verification.assert_valid()
                exact['canonical_definition_verified'] = True
                exact['instance'] = inst.to_dict()
            symmetric_exact = exact_symmetric_point(dag, cone, J, args.outside_order,
                                                    args.noncontainment_floor)
        report = {'scope': 'symmetric input class; unrestricted ordered-history pure SPE witnesses',
                  'universal_claim_proved': False, 'milp': meta, 'exact_candidate': exact,
                  'exact_symmetric_candidate': symmetric_exact}
    args.output.write_text(json.dumps(serializable(report), indent=2) + '\n')
    summary = dict(report)
    if summary.get('exact_candidate'):
        summary['exact_candidate'] = {k: v for k, v in exact.items()
            if k not in ('strategy', 'integer_clones', 'dual_support', 'instance')}
    if summary.get('exact_symmetric_candidate'):
        summary['exact_symmetric_candidate'] = {k: v for k, v in symmetric_exact.items()
            if k not in ('integer_clones', 'instance')}
    print(json.dumps(serializable(summary)), flush=True)


if __name__ == '__main__':
    main()
