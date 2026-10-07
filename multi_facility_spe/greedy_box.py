"""Exact finite greedy-box construction; no polynomial iteration bound.

The on-path dynamics uses a threshold-interleaved lexicographic potential.
Every strict improvement and every home-return is checked with exact rational
arithmetic. Off-path completion reuses finite capped pure best responses, not
the published polynomial Nashification algorithm (which is not implemented
here). No trajectory or full table of all labeled layouts is stored.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import prod

from .two_exists import (Instance, loads, merge_pack, pure_improve, pure_profile,
                         site_groups, uniform_profile)


def _instance(inst: Instance) -> Instance:
    """Validate direct Python inputs as strictly as the JSON entry point."""
    if not isinstance(inst, Instance):
        raise ValueError("Expected a multi_facility_spe.two_exists.Instance")
    if type(inst.m) is not int or type(inst.k) is not int:
        raise ValueError("m and k must be explicit integers")
    if any(type(w) not in (int, F) for w in inst.weights):
        raise ValueError("Weights must be exact integers or Fractions, not floats")
    if any(type(s) is not int for c in inst.covers for s in c):
        raise ValueError("Sites must be integer catalog indices")
    return Instance(tuple(F(w) for w in inst.weights),
                    tuple(frozenset(c) for c in inst.covers), inst.m, inst.k)


def canonical_greedy(inst: Instance):
    """Return (labeled layout, initial site assignment, gamma, opening order).

    Facility labels are insertion indices. Equal scores choose the smaller
    physical-site index; opening a site serves every still-uncovered client.
    """
    inst = _instance(inst)
    q = [0] * inst.m
    mass = [F(0)] * inst.m
    home = [-1] * len(inst.weights)
    layout, opening = [], []
    gamma = F(0)
    for _ in range(inst.k):
        scores = [mass[t] / (q[t] + 1) if q[t] else
                  sum((w for i, w in enumerate(inst.weights)
                       if home[i] < 0 and t in inst.covers[i]), F(0))
                  for t in range(inst.m)]
        t = min(range(inst.m), key=lambda s: (-scores[s], s))
        gamma = scores[t]
        if q[t] == 0:
            opening.append(t)
            for i, w in enumerate(inst.weights):
                if home[i] < 0 and t in inst.covers[i]:
                    home[i] = t
                    mass[t] += w
        q[t] += 1
        layout.append(t)
    return tuple(layout), tuple(home), gamma, tuple(opening)


def _site_loads(inst: Instance, layout, assignment):
    mass = {t: F(0) for t in layout}
    if len(assignment) != len(inst.weights):
        raise ValueError("One site assignment is required for every client")
    for i, t in enumerate(assignment):
        options = inst.covers[i] & mass.keys()
        if type(t) is not int or (t not in options if options else t != -1):
            raise ValueError("Site assignment violates coverage or compulsory service")
        if t >= 0:
            mass[t] += inst.weights[i]
    return mass


def verify_on_path(inst: Instance, layout, assignment, *, gamma=None, home=None):
    """Check the canonical layout, full boxes, frozen clients, H and exact NE.

    Raises ValueError on a failed check. All original occupied alternatives
    are checked, including deviations that would leave the load box.
    """
    inst = _instance(inst)
    expected, initial, score, _ = canonical_greedy(inst)
    layout, assignment = tuple(layout), tuple(assignment)
    if len(layout) != inst.k or any(type(t) is not int for t in layout):
        raise ValueError("A layout must contain k integer site indices")
    if layout != expected:
        raise ValueError("Layout is not the canonical greedy insertion layout")
    if gamma is not None and gamma != score:
        raise ValueError("Incorrect final greedy score")
    if home is not None:
        home = tuple(home)
        if any(type(t) is not int for t in home) or home != initial:
            raise ValueError("Incorrect initial greedy assignment")
    gamma, home = score, initial
    q = {t: len(fs) for t, fs in site_groups(layout).items()}
    mass = _site_loads(inst, layout, assignment)
    if any(not q[t] * gamma <= mass[t] <= (q[t] + 1) * gamma for t in q):
        raise ValueError("A full greedy load box is violated")
    for i, s in enumerate(assignment):
        options = inst.covers[i] & q.keys()
        if s < 0:
            continue
        if (len(options) == 1 or inst.weights[i] >= gamma) and s != home[i]:
            raise ValueError("A frozen client changed its initial site")
        e = (mass[s] - inst.weights[i]) / q[s]
        if any(e > mass[t] / q[t] for t in options):
            raise ValueError("An original client deviation strictly improves")
        if gamma > 0 and len(options) > 1 and inst.weights[i] < gamma:
            if e - gamma > (gamma - inst.weights[i]) / q[home[i]]:
                raise ValueError("The additional home inequality H is violated")
    return dict(exact_ne=True, full_boxes=True, frozen_clients=True,
                home_inequality=True, gamma=str(gamma),
                site_loads={str(t): str(mass[t]) for t in sorted(q)})


def construct_on_path(inst: Instance):
    """Return (layout, site_assignment, audit) after finite guarded dynamics.

    No artificial iteration limit is imposed. Arithmetic and working storage
    have polynomial bit size; the number of moves is not bounded polynomially.
    """
    inst = _instance(inst)
    layout, home, gamma, opening = canonical_greedy(inst)
    a = list(home)
    groups = site_groups(layout)
    q = {t: len(fs) for t, fs in groups.items()}
    mass = _site_loads(inst, layout, a)
    options = {i: tuple(sorted(inst.covers[i] & q.keys()))
               for i in range(len(inst.weights))}
    variable = [i for i in range(len(inst.weights))
                if len(options[i]) > 1 and inst.weights[i] < gamma]
    opening_index = {t: j for j, t in enumerate(opening)}
    order = tuple(sorted(q, key=lambda t: (-q[t], opening_index[t])))
    rank = {t: j for j, t in enumerate(order)}
    for i in variable:
        if any(rank[home[i]] > rank[t] for t in options[i]):
            raise ArithmeticError("Greedy home is not the first occupied option")
    x = {t: mass[t] / gamma - q[t] for t in q} if gamma else {t: F(0) for t in q}
    w = {i: inst.weights[i] / gamma for i in variable}
    r = {i: (1 - w[i]) / q[home[i]] for i in variable}
    levels = tuple(sorted(set(r.values())))
    by_level = {z: tuple(i for i in variable if r[i] == z) for z in levels}
    priority = tuple(sorted(variable, key=lambda i: (r[i], i)))

    def potential():
        values = []
        for z in levels:
            values.extend(sorted(min(x[t] / q[t], z) for t in q))
            values.append(-sum(a[i] != home[i] for i in by_level[z]))
        return tuple(values)

    def valid_batch():
        return (all(0 <= v <= 1 for v in x.values()) and
                all((x[a[i]] - w[i]) / q[a[i]] <= r[i] for i in variable))

    def move(i, target):
        before = potential()
        source = a[i]
        x[source] -= w[i]
        x[target] += w[i]
        a[i] = target
        if any(v < 0 for v in x.values()):
            raise ArithmeticError("A microstep violated the lower box")
        if not potential() > before:
            raise ArithmeticError("A microstep failed strict lexicographic progress")

    if not valid_batch():
        raise ArithmeticError("Initial greedy state violates full boxes or H")
    improvements = repairs = batches = max_repairs = 0
    while True:
        chosen = None
        for i in priority:
            target = min(options[i], key=lambda t: (x[t] / q[t], t))
            if x[target] / q[target] < (x[a[i]] - w[i]) / q[a[i]]:
                chosen = i, target
                break
        if chosen is None:
            break
        mover, destination = chosen
        move(mover, destination)
        improvements += 1
        batch_repairs = 0
        for source in reversed(order):
            while True:
                returning = next((i for i in priority
                                  if a[i] == source and home[i] != source and
                                  (x[source] - w[i]) / q[source] > r[i]), None)
                if returning is None:
                    break
                move(returning, home[returning])
                repairs += 1
                batch_repairs += 1
        if not valid_batch() or a[mover] != destination:
            raise ArithmeticError("Home repair failed its batch invariants")
        batches += 1
        max_repairs = max(max_repairs, batch_repairs)
    checked = verify_on_path(inst, layout, a, gamma=gamma, home=home)
    bound = prod(len(options[i]) for i in variable) - 1
    if improvements + repairs > bound:
        raise ArithmeticError("Distinct-state movement bound was exceeded")
    return layout, tuple(a), dict(
        gamma=str(gamma), opening_order=list(opening), repair_order=list(reversed(order)),
        initial_site_assignment=list(home), variable_clients=variable,
        thresholds=[str(z) for z in levels], strict_improvements=improvements,
        home_returns=repairs, batches=batches, max_returns_per_batch=max_repairs,
        microsteps=improvements + repairs, assignment_move_bound=str(bound),
        every_microstep_potential_checked=True, final_verification=checked,
        complexity='finite; polynomial space; no polynomial total-time bound')


def deviation_witness(inst: Instance, layout, assignment, home, gamma, f, target):
    """BOX-TO-2: capped finite pure NE, with singleton original-pool reset."""
    if type(f) is not int or not 0 <= f < inst.k:
        raise ValueError("Invalid deviating facility")
    if type(target) is not int or not 0 <= target < inst.m or target == layout[f]:
        raise ValueError("Invalid deviation target")
    changed = list(layout)
    changed[f] = target
    changed = tuple(changed)
    groups = site_groups(layout)
    stationary = site_groups(layout, omit=f)
    a = loads(inst, uniform_profile(inst, layout, assignment))[f]
    singleton = len(groups[layout[f]]) == 1
    scale = gamma if singleton else a
    initial = [-1] * len(inst.weights)
    if scale == 0:
        if any(inst.covers):
            raise ArithmeticError("Zero score with a covered client")
        return initial, dict(strict_improvement_steps=0, isolated_giants=0,
                             deviator=f, target_site=target, on_path_load=str(a),
                             singleton_reset=singleton, cap='0', bins_used=0)
    reset = home if singleton else assignment
    jobs = {t: [] for t in stationary}
    to_deviator = []
    for i, source in enumerate(reset):
        if source in stationary:
            jobs[source].append(i)
        elif source >= 0:
            available = sorted(inst.covers[i] & stationary.keys())
            if available:
                jobs[available[0]].append(i)
            elif target in inst.covers[i]:
                to_deviator.append(i)
        elif target in inst.covers[i]:
            to_deviator.append(i)
    bins_used = 0
    for t, facilities in sorted(stationary.items()):
        # For singleton reset, a surviving original singleton's pooled mass
        # is at most 2 gamma, also exactly the one-bin merge_pack premise.
        bins = merge_pack(inst, jobs[t], len(facilities), scale)
        bins_used += len(bins)
        for g, clients in zip(facilities, bins):
            for i in clients:
                initial[i] = g
    cap = 2 * scale
    if sum((inst.weights[i] for i in to_deviator), F(0)) > cap:
        raise ArithmeticError("The initial deviator exceeds its proven cap")
    for i in to_deviator:
        initial[i] = f
    result, stats = pure_improve(inst, changed, initial, cap=cap, deviator=f)
    if loads(inst, pure_profile(inst, result))[f] > 2 * a:
        raise ArithmeticError("Completed continuation exceeds factor two")
    stats.update(deviator=f, target_site=target, on_path_load=str(a),
                 singleton_reset=singleton, cap=str(cap), bins_used=bins_used,
                 source_multiplicity=len(groups[layout[f]]),
                 departed_site_disappears=singleton,
                 target_previously_occupied=target in groups,
                 method='finite capped strict pure best responses')
    return result, stats


def construct(inst: Instance):
    """Construct a complete factor-two rule with polynomial-size description.

    Actual one-facility deviations are explicit; all other labeled layouts use
    the existing finite default rule. Evaluation is finite, not polynomial-time.
    """
    inst = _instance(inst)
    layout, assignment, audit = construct_on_path(inst)
    home = tuple(audit['initial_site_assignment'])
    gamma = F(audit['gamma'])
    p = uniform_profile(inst, layout, assignment)
    deviations = []
    for f in range(inst.k):
        for target in range(inst.m):
            if target == layout[f]:
                continue
            pure, stats = deviation_witness(inst, layout, assignment, home,
                                            gamma, f, target)
            deviations.append(dict(facility=f, site=target,
                                   pure_assignment=pure, audit=stats))
    return dict(schema='SC-K-GREEDY-BOX-2/v1', instance=inst.to_json(), factor='2',
                on_path=dict(layout=list(layout), site_assignment=list(assignment),
                             probabilities=[[str(v) for v in row] for row in p]),
                deviations=deviations, greedy_box_audit=audit,
                default_rule='least-index initial pure assignment, then strict pure best responses',
                complexity=('finite polynomial-space construction and evaluation; '
                            'polynomial-size rule; no polynomial total-time bound; '
                            'published polynomial Nashification not implemented'))
