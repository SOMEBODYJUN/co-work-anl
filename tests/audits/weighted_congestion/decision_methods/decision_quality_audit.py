#!/usr/bin/env python3
"""Exact rational audit of decision_quality.md; no external dependencies.

Default prints JSON. --output PATH exclusively creates a new record.
--check PATH checks the reproducible payload, including this source's SHA256.
This is finite evidence, not the proof of the general theorem.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random


@dataclass(frozen=True)
class Game:
    weights: tuple[F, ...]
    actions: tuple[tuple[frozenset[int], ...], ...]
    coefficients: tuple[tuple[F, ...], ...]

    def states(self):
        return product(*(range(len(a)) for a in self.actions))

    def users(self, state, e):
        return tuple(i for i, a in enumerate(state) if e in self.actions[i][a])

    def latency(self, e, load):
        return sum((a * load**k for k, a in enumerate(self.coefficients[e])), F(0))

    def load(self, users):
        return sum((self.weights[i] for i in users), F(0))

    def costs(self, state):
        x = [self.load(self.users(state, e)) for e in range(len(self.coefficients))]
        return tuple(sum((self.latency(e, x[e]) for e in self.actions[i][a]), F(0))
                     for i, a in enumerate(state))

    def welfare(self, state):
        return sum((w * c for w, c in zip(self.weights, self.costs(state))), F(0))

    def deviations(self, state):
        c = self.costs(state)
        for i, aa in enumerate(self.actions):
            for a in range(len(aa)):
                t = state[:i] + (a,) + state[i + 1:]
                yield i, a, t, c[i], self.costs(t)[i]

    def potential_affine(self, state):
        total = F(0)
        for e, cc in enumerate(self.coefficients):
            assert len(cc) <= 2
            users = self.users(state, e)
            x = self.load(users)
            ell = cc[1] if len(cc) == 2 else F(0)
            total += ell * (x*x + sum((self.weights[i]**2 for i in users), F(0))) / 2
            total += cc[0] * x
        return total


def all_subsets(items):
    return (tuple(s) for n in range(len(items) + 1) for s in combinations(items, n))


def factor(g, s):
    alpha = F(1)
    for _, _, _, old, new in g.deviations(s):
        if new == 0:
            if old > 0:
                return None  # +infinity, never a floating-point ratio
        else:
            alpha = max(alpha, old / new)
    return alpha


def violation(g, s, alpha):
    return max([F(0)] + [old-alpha*new for _, _, _, old, new in g.deviations(s)])


def stable(g, s, alpha):
    return violation(g, s, alpha) == 0


def frontier(g):
    rows = [(s, factor(g, s), g.welfare(s)) for s in g.states()]
    def less_equal(a, b):
        return b is None or (a is not None and a <= b)
    return [(s, a, w) for s, a, w in rows
            if not any(less_equal(aa, a) and ww <= w and (aa != a or ww < w)
                       for _, aa, ww in rows)]


def stability_certificate(g, s, alpha):
    rows = []
    for i, a, t, old, new in g.deviations(s):
        slack = alpha*new-old
        assert slack >= 0
        rows.append(dict(player=i, action=a, after=t, old=old, new=new, slack=slack))
    return rows


def budget_certificate(g, alpha, budget):
    feasible = [s for s in g.states() if stable(g, s, alpha) and g.welfare(s) <= budget]
    if feasible:
        s = min(feasible, key=lambda t: (g.welfare(t), t))
        return dict(feasible=True, state=s, W=g.welfare(s), budget_slack=budget-g.welfare(s),
                    stability=stability_certificate(g, s, alpha))
    cover = []
    for s in g.states():
        if g.welfare(s) > budget:
            cover.append(dict(state=s, reason="budget", strict_margin=g.welfare(s)-budget))
        else:
            i, a, t, old, new = next(row for row in g.deviations(s) if row[3] > alpha*row[4])
            cover.append(dict(state=s, reason="strict_improvement", player=i, action=a,
                              after=t, old=old, new=new, strict_margin=old-alpha*new))
    assert len(cover) == len(list(g.states()))
    return dict(feasible=False, complete_state_cover=cover)


def stable_cost_lower_bound(g, alpha):
    ss = list(g.states())
    vv = {s: violation(g, s, alpha) for s in ss}
    feasible = [s for s in ss if vv[s] == 0]
    if not feasible:
        return dict(empty=True, strict_cover=[dict(state=s, V=vv[s]) for s in ss])
    lower = min(g.welfare(s) for s in feasible)
    mu = max([F(0)] + [(lower-g.welfare(s))/vv[s] for s in ss if vv[s] > 0])
    rows = [dict(state=s, V=vv[s], slack=g.welfare(s)+mu*vv[s]-lower) for s in ss]
    assert all(r["slack"] >= 0 for r in rows)
    return dict(lower=lower, mu=mu, rows=rows)


def path_peak(g, alpha, phi):
    """Full DAG DP; selected path preserves the actual game, no budget-filtered sinks."""
    ss = list(g.states())
    edges = {s: sorted({t for _, _, t, old, new in g.deviations(s) if old > alpha*new})
             for s in ss}
    value, choice = {}, {}
    for s in sorted(ss, key=lambda t: (phi(t), t)):
        for t in edges[s]:
            assert phi(t) < phi(s)
            assert t in value
        if edges[s]:
            t = min(edges[s], key=lambda t: (value[t], t))
            value[s] = max(g.welfare(s), value[t])
            choice[s] = t
        else:
            assert stable(g, s, alpha)
            value[s] = g.welfare(s)
            choice[s] = None
    rows = []
    for s in ss:
        path, t = [s], s
        while choice[t] is not None:
            t = choice[t]
            path.append(t)
        assert max(g.welfare(t) for t in path) == value[s]
        assert len(path) <= len(ss)
        bound = max(g.welfare(t) for t in ss if phi(t) <= phi(s))
        assert value[s] <= bound
        rows.append(dict(initial=s, K=value[s], path=path, sublevel_peak=bound))
    return rows


def tangent_bound(g, points):
    """Single-cut-per-resource valid dual certificate, theta=1."""
    beta, gamma = [], []
    for e, q in enumerate(points):
        f = q*g.latency(e, q)
        b = sum(((k+1)*a*q**k for k, a in enumerate(g.coefficients[e])), F(0))
        beta.append(b)
        gamma.append(q*b-f)
    lam = [min(w*sum((beta[e] for e in aa), F(0)) for aa in g.actions[i])
           for i, w in enumerate(g.weights)]
    lower = sum(lam, F(0))-sum(gamma, F(0))
    assert all(v >= 0 for v in gamma)
    for s in g.states():
        assert g.welfare(s) >= lower
        for i, a in enumerate(s):
            assert lam[i] <= g.weights[i]*sum((beta[e] for e in g.actions[i][a]), F(0))
    return dict(q=points, beta=beta, gamma=gamma, lambda_i=lam, lower=lower)


def fixture_record(g, tangent=None):
    ss = list(g.states())
    phi = g.potential_affine
    opt = min(g.welfare(s) for s in ss)
    rows = [dict(state=s, C=g.costs(s), W=g.welfare(s), U=sum(g.costs(s), F(0)),
                 Phi=phi(s), A=factor(g, s)) for s in ss]
    positive_ratios = [phi(s)/g.welfare(s) for s in ss if g.welfare(s) > 0]
    m, big_m = min(positive_ratios), max(positive_ratios)
    mixtures = []
    for eta in (F(0), F(1,5), F(1,3), F(1), F(2)):
        obj = lambda s: phi(s)+eta*g.welfare(s)
        mins = [s for s in ss if obj(s) == min(map(obj, ss))]
        beta = (1+2*eta)/(1+eta)
        ratio = (big_m+eta)/(m+eta)
        for s in mins:
            assert stable(g, s, beta)
            assert g.welfare(s) <= ratio*opt
        mixtures.append(dict(eta=eta, minimizers=mins, beta=beta, welfare_ratio_bound=ratio))
    return dict(input=dict(weights=g.weights, actions=g.actions, coefficients=g.coefficients),
                states=rows, OPT=opt, exact_frontier=frontier(g), m=m, M=big_m,
                mixtures=mixtures, exact_stable_cost=stable_cost_lower_bound(g, F(1)),
                repair_paths=path_peak(g, F(1), phi),
                tangent=tangent_bound(g, tangent) if tangent is not None else None)


def order_potential(g, e, users, ascending):
    x, total = F(0), F(0)
    for i in sorted(users, key=lambda i: (g.weights[i], i), reverse=not ascending):
        x += g.weights[i]
        total += g.weights[i]*g.latency(e, x)
    return total


def random_structural_audit():
    rng = random.Random(20261021)
    counter = dict(games=0, local_insertion_edges=0, state_deviations=0,
                   regularized_global_minimizers=0, theta_mixture_checks=0,
                   social_optimum_checks=0, zero_optimum_games=0,
                   target_stability_parameter_checks=0)
    for case in range(96):
        n = 2 + case % 3
        d = 2 + case % 2
        weights = tuple(F(2 if i % 2 == 0 else 1) for i in range(n))
        coeff = tuple(tuple(F(rng.randrange(4), rng.randrange(1, 4)) for _ in range(d+1))
                      for e in range(4))
        if case % 12 == 0:
            coeff = tuple(tuple(F(0) for _ in range(d+1)) for e in range(4))
        acts = []
        for i in range(n):
            aa = {frozenset(e for e in range(4) if rng.randrange(2)) for _ in range(3)}
            aa.add(frozenset({i % 4}))
            if case % 6 == 0:
                aa.add(frozenset())
            acts.append(tuple(sorted(aa, key=lambda x: tuple(sorted(x)))))
        g = Game(weights, tuple(acts), coeff)
        blend = (F(1,2), F(1), F(2))[case % 3]
        alpha = max((1+blend)/blend, (1+d*blend)/(1+blend))
        h = tuple(blend*w if w == 2 else (1+blend)*w for w in weights)
        def local(e, users):
            return order_potential(g, e, users, False)+blend*order_potential(g, e, users, True)
        def phi(s):
            return sum((local(e, g.users(s, e)) for e in range(4)), F(0))
        resource_ratios = []
        for e in range(4):
            potential_users = tuple(i for i in range(n) if any(e in a for a in acts[i]))
            for users in all_subsets(potential_users):
                load = g.load(users)
                cost = load*g.latency(e, load)
                pot = local(e, users)
                if cost:
                    resource_ratios.append(pot/cost)
                else:
                    assert pot == 0
                for i in potential_users:
                    if i in users:
                        continue
                    y = load+weights[i]
                    diff = local(e, users+(i,))-pot
                    c = g.latency(e, y)
                    assert h[i]*c <= diff <= alpha*h[i]*c
                    counter["local_insertion_edges"] += 1
        m = min(resource_ratios) if resource_ratios else F(1)
        big_m = max(resource_ratios) if resource_ratios else F(1)
        qmin, qmax = min(h[i]/weights[i] for i in range(n)), max(h[i]/weights[i] for i in range(n))
        if resource_ratios:
            assert qmin/(d+1) <= m <= big_m <= alpha*qmax
        ss = list(g.states())
        opt = min(g.welfare(s) for s in ss)
        counter["zero_optimum_games"] += opt == 0
        for s in ss:
            assert m*g.welfare(s) <= phi(s) <= big_m*g.welfare(s)
            for _, _, _, old, new in g.deviations(s):
                counter["state_deviations"] += 1
            if g.welfare(s) == opt:
                assert stable(g, s, F(d+1))
                counter["social_optimum_checks"] += 1
        for eta in (F(0), F(1,3), F(1), F(3)):
            beta = max((alpha*h[i]+eta*(d+1)*weights[i])/(h[i]+eta*weights[i])
                       for i in range(n))
            obj = lambda s: phi(s)+eta*g.welfare(s)
            value = min(obj(s) for s in ss)
            for s in ss:
                if obj(s) != value:
                    continue
                assert stable(g, s, beta)
                assert (m+eta)*g.welfare(s) <= (big_m+eta)*opt
                counter["regularized_global_minimizers"] += 1
        if alpha < d+1:
            target = (alpha+d+1)/2
            eta_max = min((target-alpha)*h[i]/((d+1-target)*weights[i]) for i in range(n))
            beta_at_max = max((alpha*h[i]+eta_max*(d+1)*weights[i])/(h[i]+eta_max*weights[i])
                              for i in range(n))
            assert beta_at_max == target
            counter["target_stability_parameter_checks"] += 1
        # Independent convex-combination-of-cuts check, not solver-derived.
        for e in range(4):
            qs = (F(0), F(1,2), F(3))
            theta = (F(1,5), F(2,5), F(1,5))
            b = sum((t*sum(((k+1)*a*q**k for k,a in enumerate(coeff[e])), F(0))
                     for t,q in zip(theta, qs)), F(0))
            gamma = sum((t*(q*sum(((k+1)*a*q**k for k,a in enumerate(coeff[e])), F(0))
                             -q*g.latency(e,q)) for t,q in zip(theta,qs)), F(0))
            for x in (F(0), F(1,3), F(1), F(5), F(20)):
                assert x*g.latency(e,x) >= b*x-gamma
                counter["theta_mixture_checks"] += 1
        counter["games"] += 1
    return counter


def insertion_boundary_audit():
    count = 0
    for d in range(9):
        for k in range(d+1):
            for old in (F(0), F(1,3), F(1), F(17)):
                for weight in (F(1,7), F(1), F(5)):
                    y = old+weight
                    diff = y**(k+1)-old**(k+1)
                    assert weight*y**k <= diff <= (d+1)*weight*y**k
                    count += 1
    return dict(monomial_insertion_checks=count, maximum_degree=8,
                includes_zero_old_load=True, includes_degree_zero=True)


def background_restoration_audit():
    """Fixed background is absent from optional potential, present in full welfare."""
    weights = (F(2), F(1), F(1))
    subset_checks = edge_checks = 0
    for d in range(1, 7):
        for blend in (F(1,2), F(1), F(2)):
            alpha = max((1+blend)/blend, (1+d*blend)/(1+blend))
            h = tuple(blend*w if w == 2 else (1+blend)*w for w in weights)
            qmin, qmax = min(h[i]/weights[i] for i in range(3)), max(h[i]/weights[i] for i in range(3))
            for background in (F(0), F(1,3), F(2)):
                for zero_cost in (False, True):
                    cc = tuple(F(0) if zero_cost else F(k+1,k+2) for k in range(d+1))
                    def c(x):
                        return sum((a*x**k for k,a in enumerate(cc)), F(0))
                    def ordered(users, ascending):
                        x, total = F(0), F(0)
                        for i in sorted(users, key=lambda i: (weights[i],i), reverse=not ascending):
                            x += weights[i]
                            total += weights[i]*c(background+x)
                        return total
                    def optional(users):
                        return ordered(users,False)+blend*ordered(users,True)
                    for users in all_subsets(tuple(range(3))):
                        x = background+sum((weights[i] for i in users),F(0))
                        w = x*c(x)
                        restored = optional(users)+qmin*background*c(background)
                        assert qmin*w/(d+1) <= restored <= alpha*qmax*w
                        assert (restored > 0) == (w > 0)
                        subset_checks += 1
                        for i in range(3):
                            if i in users:
                                continue
                            marginal = optional(users+(i,))-optional(users)
                            assert h[i]*c(x+weights[i]) <= marginal <= alpha*h[i]*c(x+weights[i])
                            edge_checks += 1
    # Mandatory-only positive-cost counterexample and its actual repair.
    mandatory_welfare, optional_potential, baseline = F(1),F(0),F(1)
    assert optional_potential == 0 < mandatory_welfare
    assert optional_potential+baseline == mandatory_welfare
    return dict(subset_checks=subset_checks, optional_insertion_edges=edge_checks,
                mandatory_only=dict(weight="1", latency="x", full_W=mandatory_welfare,
                                    compressed_optional_Phi=optional_potential,
                                    restored_baseline=baseline,
                                    restored_Phi=optional_potential+baseline),
                coarse_bounds_reproved_for_qmin_baseline=True)


def jsonable(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k,v in x.items()}
    if isinstance(x, (tuple, list, frozenset)):
        if isinstance(x, frozenset):
            x = sorted(x)
        return [jsonable(v) for v in x]
    return x


def run():
    fixed = Game((F(2),F(1)), ((frozenset({0}),), (frozenset({0}),frozenset({1}))),
                 ((F(0),F(1)), (F(7,2),)))
    objective = Game(fixed.weights, fixed.actions, ((F(0),F(1)), (F(9,2),)))
    selection = Game((F(1),F(1)),
                     ((frozenset({0,1}),frozenset({2,3})),
                      (frozenset({0,2}),frozenset({1,3}))),
                     ((F(0),F(1)),(F(0),F(1)),(F(0),F(1)),(F(7,4),)))
    a = fixture_record(fixed, (F(2),F(1)))
    b = fixture_record(selection, (F(7,8),F(1),F(1),F(9,8)))
    o = fixture_record(objective)
    assert a["OPT"] == F(15,2) and a["tangent"]["lower"] == F(15,2)
    assert b["OPT"] == F(11,2) and b["tangent"]["lower"] == F(303,64)
    assert factor(fixed, (0,1)) == F(7,6)
    assert a["states"][0]["Phi"] == 7
    assert min(fixed.states(), key=fixed.welfare) == (0,1)
    assert min(objective.states(), key=lambda s: sum(objective.costs(s), F(0))) == (0,0)
    assert min(objective.states(), key=objective.welfare) == (0,1)
    budget = {
        "alpha_1_budget_15_over_2": budget_certificate(fixed,F(1),F(15,2)),
        "alpha_7_over_6_budget_15_over_2": budget_certificate(fixed,F(7,6),F(15,2)),
        "alpha_7_over_6_minus_1_over_600_budget_15_over_2":
            budget_certificate(fixed,F(7,6)-F(1,600),F(15,2)),
        "alpha_1_budget_9": budget_certificate(fixed,F(1),F(9)),
    }
    assert budget["alpha_1_budget_15_over_2"]["feasible"] is False
    assert budget["alpha_7_over_6_budget_15_over_2"]["feasible"] is True
    assert budget["alpha_7_over_6_minus_1_over_600_budget_15_over_2"]["feasible"] is False
    zero_deviation = Game((F(1),), ((frozenset({0}),frozenset()),), ((F(1),),))
    assert factor(zero_deviation,(0,)) is None
    assert factor(zero_deviation,(1,)) == 1
    assert stable(zero_deviation,(1,),F(1))
    assert zero_deviation.welfare((1,)) == 0
    return jsonable(dict(
        schema="WC-decision-quality-exact-audit-v1", source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        evidence_kind="finite Fraction audit; general claims require the written proofs",
        social_objective="W=sum_i w_i*C_i=sum_e x_e*c_e(x_e)",
        two_state=a, four_state=b, objective_disagreement=o,
        budget_certificates=budget, insertion_boundaries=insertion_boundary_audit(),
        mandatory_background=background_restoration_audit(),
        zero_deviation_boundary=dict(positive_to_zero_factor="infinity", both_zero="satisfies inequality"),
        structural_random=random_structural_audit(),
        float_tolerances_used=False, external_solver_used=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        assert json.loads(args.check.read_text()) == result, "frozen record mismatch"
        print(json.dumps(dict(check="PASS", file=str(args.check), structural_random=result["structural_random"]),
                         ensure_ascii=False, indent=2))
    elif args.output:
        with args.output.open("x") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(json.dumps(dict(output=str(args.output), structural_random=result["structural_random"]),
                         ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
