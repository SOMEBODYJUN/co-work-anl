"""Exact finite construction accompanying SC-K-2-E.

The on-path search is exponential. Pure improvement paths have no polynomial
iteration bound here. This module proves no complexity claim by its runtime.
All arithmetic is Fraction arithmetic; no NE oracle is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from typing import Iterable


@dataclass(frozen=True)
class Instance:
    weights: tuple[F, ...]
    covers: tuple[frozenset[int], ...]  # client -> accessible physical sites
    m: int
    k: int

    def __post_init__(self):
        if self.m < 1 or self.k < 1 or len(self.weights) != len(self.covers):
            raise ValueError("Invalid dimensions")
        if any(w <= 0 for w in self.weights):
            raise ValueError("Weights must be strictly positive")
        if any(s < 0 or s >= self.m for c in self.covers for s in c):
            raise ValueError("Site outside common catalog")

    @classmethod
    def from_json(cls, obj: dict) -> 'Instance':
        if not isinstance(obj, dict) or type(obj.get('m')) is not int or type(obj.get('k')) is not int:
            raise ValueError("m and k must be explicit integers")
        clients = obj.get('clients')
        if not isinstance(clients, list):
            raise ValueError("clients must be an explicit list")
        weights, covers = [], []
        for c in clients:
            if not isinstance(c, dict) or type(c.get('weight')) not in (str, int):
                raise ValueError("weight must be an integer or exact rational string, not a float")
            sites = c.get('sites')
            if not isinstance(sites, list) or any(type(s) is not int for s in sites):
                raise ValueError("sites must be a list of integer catalog indices")
            weights.append(F(c['weight']))
            covers.append(frozenset(sites))
        return cls(tuple(weights), tuple(covers), obj['m'], obj['k'])

    def to_json(self) -> dict:
        return dict(m=self.m, k=self.k,
                    clients=[dict(weight=str(w), sites=sorted(c))
                             for w, c in zip(self.weights, self.covers)])


def site_groups(layout: tuple[int, ...], omit: int | None = None) -> dict[int, list[int]]:
    groups: dict[int, list[int]] = {}
    for f, s in enumerate(layout):
        if f != omit:
            groups.setdefault(s, []).append(f)
    return groups


def uniform_profile(inst: Instance, layout: tuple[int, ...], assignment: tuple[int, ...]):
    groups = site_groups(layout)
    p = [[F(0)] * inst.k for _ in inst.weights]
    for i, s in enumerate(assignment):
        if s >= 0:
            for f in groups[s]:
                p[i][f] = F(1, len(groups[s]))
    return p


def pure_profile(inst: Instance, assignment: Iterable[int]):
    return [[F(int(f == g)) for f in range(inst.k)] for g in assignment]


def loads(inst: Instance, p) -> list[F]:
    return [sum((w * row[f] for w, row in zip(inst.weights, p)), F(0))
            for f in range(inst.k)]


def search_lexmax(inst: Instance):
    """Enumerate physical occupancies and all feasible pure-to-site assignments.

    Label permutations do not change the sorted objective. Enumeration of sorted
    layouts therefore attains exactly the same maximum as all labeled layouts.
    """
    best_key = None
    best = None
    evaluated = 0
    for layout in combinations_with_replacement(range(inst.m), inst.k):
        occupied = set(layout)
        choices = [sorted(c & occupied) or [-1] for c in inst.covers]
        groups = site_groups(layout)
        for assignment in product(*choices):
            mass = {s: F(0) for s in occupied}
            for i, s in enumerate(assignment):
                if s >= 0:
                    mass[s] += inst.weights[i]
            key = tuple(sorted(mass[s] / len(groups[s]) for s in layout))
            evaluated += 1
            if best_key is None or key > best_key:
                best_key = key
                best = (tuple(layout), tuple(assignment))
    assert best is not None
    return (*best, dict(site_allocations_evaluated=evaluated,
                       lex_key=[str(x) for x in best_key]))


def merge_pack(inst: Instance, jobs: list[int], q: int, a: F):
    """Pack W <= (q+1)a into q bins: singleton >2a or ordinary <=2a."""
    assert q >= 1 and a > 0
    assert sum((inst.weights[i] for i in jobs), F(0)) <= (q + 1) * a
    bins = [[i] for i in jobs]
    mass = [inst.weights[i] for i in jobs]
    while True:
        pair = next(((x, y) for x in range(len(bins))
                     for y in range(x + 1, len(bins))
                     if mass[x] + mass[y] <= 2 * a), None)
        if pair is None:
            break
        x, y = pair
        bins[x] += bins[y]
        mass[x] += mass[y]
        del bins[y]
        del mass[y]
    assert len(bins) <= q
    assert all(v <= 2 * a or len(b) == 1 for b, v in zip(bins, mass))
    return bins


def pure_improve(inst: Instance, layout: tuple[int, ...], assignment: list[int],
                 cap: F | None = None, deviator: int | None = None):
    """Strict pure best responses; finite, not asserted polynomial time."""
    assignment = list(assignment)
    L = [F(0)] * inst.k
    for i, f in enumerate(assignment):
        if f >= 0:
            L[f] += inst.weights[i]
    allowed = [[f for f, s in enumerate(layout) if s in c] for c in inst.covers]
    for i, choices in enumerate(allowed):
        assert (assignment[i] in choices) if choices else (assignment[i] == -1)
    initial_giants = {i: assignment[i] for i, w in enumerate(inst.weights)
                      if cap is not None and w > cap and assignment[i] >= 0}
    if cap is not None:
        assert all(L[f] == inst.weights[i] for i, f in initial_giants.items())
        giant_facilities = set(initial_giants.values())
        assert all(L[f] <= cap for f in range(inst.k) if f not in giant_facilities)
        if deviator is not None:
            assert deviator not in giant_facilities
    steps = 0
    while True:
        move = None
        for i, old in enumerate(assignment):
            if old < 0:
                continue
            options = [g for g in allowed[i] if g != old]
            if not options:
                continue
            g = min(options, key=lambda h: (L[h], h))
            if L[g] + inst.weights[i] < L[old]:
                move = (i, old, g)
                break
        if move is None:
            break
        i, old, g = move
        potential = sum(x * x for x in L)
        w = inst.weights[i]
        L[old] -= w
        L[g] += w
        assignment[i] = g
        assert sum(x * x for x in L) < potential
        if cap is not None:
            assert all(assignment[j] == f and L[f] == inst.weights[j]
                       for j, f in initial_giants.items())
            assert all(L[f] <= cap for f in range(inst.k) if f not in giant_facilities)
        # Strict decrease of the exact quadratic potential already rules out
        # repeated states. Do not store an exponentially long trajectory.
        steps += 1
    return assignment, dict(strict_improvement_steps=steps,
                           isolated_giants=len(initial_giants),
                           final_loads=[str(x) for x in L])


def deviation_witness(inst: Instance, layout: tuple[int, ...], assignment: tuple[int, ...],
                      f: int, r: int):
    assert r != layout[f] and 0 <= r < inst.m
    a = loads(inst, uniform_profile(inst, layout, assignment))[f]
    target = list(layout)
    target[f] = r
    target = tuple(target)
    if a == 0:
        assert all(not c for c in inst.covers), "Zero only allowed in all-zero-reach instance"
        return [-1] * len(inst.weights), dict(strict_improvement_steps=0, isolated_giants=0)
    old_groups = site_groups(layout)
    stationary = site_groups(layout, omit=f)
    jobs = {s: [] for s in stationary}
    to_deviator: list[int] = []
    for i, s in enumerate(assignment):
        if s in stationary:
            jobs[s].append(i)
        elif s >= 0:  # the departing facility was alone at its old site
            available_old = sorted(inst.covers[i] & set(stationary))
            if available_old:
                jobs[available_old[0]].append(i)
            elif r in inst.covers[i]:
                to_deviator.append(i)
        elif r in inst.covers[i]:  # newly covered client
            to_deviator.append(i)
    initial = [-1] * len(inst.weights)
    all_bins = []
    for s, facilities in sorted(stationary.items()):
        bins = merge_pack(inst, jobs[s], len(facilities), a)
        for g, clients in zip(facilities, bins):
            for i in clients:
                initial[i] = g
        all_bins.extend(bins)
    assert sum((inst.weights[i] for i in to_deviator), F(0)) <= a
    for i in to_deviator:
        initial[i] = f
    result, stats = pure_improve(inst, target, initial, cap=2 * a, deviator=f)
    stats.update(deviator=f, target_site=r, source_multiplicity=len(old_groups[layout[f]]),
                 departed_site_disappears=len(old_groups[layout[f]]) == 1,
                 target_previously_occupied=r in old_groups,
                 on_path_load=str(a), bins_used=len(all_bins))
    assert loads(inst, pure_profile(inst, result))[f] <= 2 * a
    return result, stats


def construct(inst: Instance):
    layout, assignment, search_stats = search_lexmax(inst)
    p = uniform_profile(inst, layout, assignment)
    deviations = []
    for f in range(inst.k):
        for r in range(inst.m):
            if r == layout[f]:
                continue
            q, stats = deviation_witness(inst, layout, assignment, f, r)
            deviations.append(dict(facility=f, site=r, pure_assignment=q, audit=stats))
    return dict(schema='SC-K-2-E/v1', instance=inst.to_json(), factor='2',
                on_path=dict(layout=list(layout), site_assignment=list(assignment),
                             probabilities=[[str(x) for x in row] for row in p]),
                deviations=deviations,
                default_rule='least-index initial pure assignment, then strict pure best responses',
                search_audit=search_stats,
                complexity='exhaustive finite construction; no polynomial-time claim')


def evaluate_continuation(certificate: dict, layout: Iterable[int]):
    """Evaluate the complete rule, including unlisted layouts; not polynomial time.

    Certificates are intended to be checked separately. This evaluator does
    not turn an unchecked external JSON document into a trusted theorem.
    """
    inst = Instance.from_json(certificate['instance'])
    layout = tuple(layout)
    if len(layout) != inst.k or any(type(s) is not int or s < 0 or s >= inst.m for s in layout):
        raise ValueError("Invalid labeled layout")
    on_path = tuple(certificate['on_path']['layout'])
    if layout == on_path:
        return [[F(x) for x in row] for row in certificate['on_path']['probabilities']]
    for deviation in certificate['deviations']:
        other = list(on_path)
        other[deviation['facility']] = deviation['site']
        if tuple(other) == layout:
            return pure_profile(inst, deviation['pure_assignment'])
    initial = [next((f for f, s in enumerate(layout) if s in cover), -1)
               for cover in inst.covers]
    result, _ = pure_improve(inst, layout, initial)
    return pure_profile(inst, result)
