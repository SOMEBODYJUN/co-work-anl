"""Exact bit-polynomial box NE construction for equal movable weights.

SC-K-EQUAL-LIGHT-FLOW-BOX: q is nonincreasing, 0 <= c <= 1, each
nonempty allowed set has home min(A_i), and all movable weights are one
rational delta in (0, 1).  The empty-client case is included.  Negative
b_t = c_t - delta * H_t are permitted; b is not a physical load.

The optimizer minimizes Psi over ALL legal assignments, without box or H
constraints.  The equal-weight exchange theorem then supplies both boxes,
all original-option NE inequalities and H.  The output is independently
rechecked below.  General unequal weights are rejected, not enumerated.

The residual network has n+m+2 vertices and n+2E forward unit arcs, where
E=sum_i |A_i|.  Exactly n shortest-path augmentations send one indivisible
client each.  Bellman--Ford uses O((n+m+2)(n+E)) integer operations per
augmentation, even when initial slot costs are negative.  Its min-cost
invariant follows from the absence of negative residual cycles, initially
true because the zero-flow forward graph is acyclic.  Costs alone are
scaled, by L=lcm(denominators)*lcm(q); capacities never depend on q, delta
or a denominator.  log L is bounded by the sum of input bit lengths.
Slot costs, simple-path labels and n-unit total costs have polynomial bit
length.  Construction, exact validation and all n stages consequently have
polynomial total bit complexity; no numerical-size loop expands q.

This module supplies only the normalized on-path selector.  The repository's
complete executable continuation uses a separate finite off-path procedure;
its running time is not upgraded by this selector's polynomial bound.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm
import re
from typing import Sequence

Rational = int | str | Fraction


def _integer_text(value: int) -> str:
    """Decimal output without Python's process-wide integer digit limit.

    q is binary encoded and may have more than 4300 decimal digits.  Chunk
    conversion is polynomial and leaves the interpreter's safety setting
    unchanged.  The ordinary-size fast path is below its minimum limit.
    """
    if value.bit_length() <= 1000:
        return str(value)
    sign, value = ('-', -value) if value < 0 else ('', value)
    chunks = []
    while value:
        value, remainder = divmod(value, 10 ** 9)
        chunks.append(remainder)
    return sign + str(chunks[-1]) + ''.join(f'{z:09d}' for z in reversed(chunks[:-1]))


def _fraction_text(value: Fraction) -> str:
    numerator = _integer_text(value.numerator)
    return numerator if value.denominator == 1 else numerator + '/' + _integer_text(value.denominator)


def _integer_from_text(value: str) -> int:
    """Read a signed decimal integer in small chunks, for large fractions."""
    value = value.strip()
    if re.fullmatch(r'[+-]?[0-9]+(?:_[0-9]+)*', value) is None:
        raise ValueError("Invalid rational integer component")
    negative = value.startswith('-')
    digits = value.lstrip('+-').replace('_', '')
    result = 0
    for index in range(0, len(digits), 9):
        chunk = digits[index:index + 9]
        result = result * (10 ** len(chunk)) + int(chunk)
    return -result if negative else result


def _rational(value: Rational) -> Fraction:
    if type(value) not in (int, str, Fraction):
        raise ValueError("Use integers, Fraction, or exact rational strings; no floats or bools")
    try:
        return Fraction(value)
    except ValueError as exc:
        # Fraction's decimal-to-int conversion has the same digit limit as
        # str(int).  Preserve exact large numerator/denominator inputs too.
        if type(value) is str and value.count('/') == 1:
            numerator, denominator = value.split('/')
            try:
                return Fraction(_integer_from_text(numerator), _integer_from_text(denominator))
            except (ValueError, ZeroDivisionError):
                pass
        raise ValueError("Invalid rational input") from exc
    except ZeroDivisionError as exc:
        raise ValueError("Invalid rational input") from exc


def _inputs(q, c, w, allowed):
    try:
        q, c, w, allowed = tuple(q), tuple(c), tuple(w), tuple(allowed)
    except TypeError as exc:
        raise ValueError("q, c, w and A must be finite sequences") from exc
    m, n = len(q), len(w)
    if len(c) != m or len(allowed) != n:
        raise ValueError("Dimension mismatch")
    if any(type(z) is not int or z < 1 for z in q):
        raise ValueError("q must contain positive integers")
    if any(left < right for left, right in zip(q, q[1:])):
        raise ValueError("q must be nonincreasing")
    c, w = tuple(map(_rational, c)), tuple(map(_rational, w))
    if any(not 0 <= z <= 1 for z in c):
        raise ValueError("c must lie in [0,1]")
    if any(not 0 < z < 1 for z in w):
        raise ValueError("Each movable weight must lie in (0,1)")
    if w and any(z != w[0] for z in w):
        raise ValueError("This constructor requires equal movable weights")
    choices = []
    for row in allowed:
        try:
            row = tuple(row)
        except TypeError as exc:
            raise ValueError("Each allowed set must be a nonempty site sequence") from exc
        if not row or any(type(t) is not int or not 0 <= t < m for t in row):
            raise ValueError("Each allowed set must be nonempty and contain valid integer sites")
        choices.append(tuple(sorted(set(row))))
    return q, c, w, tuple(choices)


@dataclass
class _Arc:
    target: int
    reverse: int
    capacity: int
    cost: int
    assignment_reverse: bool = False


def _add_arc(graph, source, target, cost, *, assignment=False):
    index, reverse = len(graph[source]), len(graph[target])
    graph[source].append(_Arc(target, reverse, 1, cost))
    graph[target].append(_Arc(source, index, 0, -cost, assignment))
    return index


def _shortest_path(graph, source, sink):
    """Return a minimum-cost residual path using signed integer arithmetic."""
    size = len(graph)
    distance: list[int | None] = [None] * size
    parent: list[tuple[int, int] | None] = [None] * size
    distance[source] = 0
    for _ in range(size - 1):
        changed = False
        for u, arcs in enumerate(graph):
            if distance[u] is None:
                continue
            for j, arc in enumerate(arcs):
                if not arc.capacity:
                    continue
                candidate = distance[u] + arc.cost
                if distance[arc.target] is None or candidate < distance[arc.target]:
                    distance[arc.target] = candidate
                    parent[arc.target] = (u, j)
                    changed = True
        if not changed:
            break
    # A violated optimal-flow invariant must fail visibly, never produce a
    # purported NE by truncating the shortest-path relaxation count.
    for u, arcs in enumerate(graph):
        if distance[u] is not None:
            for arc in arcs:
                if arc.capacity and (distance[arc.target] is None or
                                     distance[u] + arc.cost < distance[arc.target]):
                    raise ArithmeticError("Negative reachable residual cycle")
    if distance[sink] is None:
        raise ArithmeticError("Unexpected infeasibility of a nonempty allowed set")
    path, seen, vertex = [], set(), sink
    while vertex != source:
        if vertex in seen or parent[vertex] is None:
            raise ArithmeticError("Invalid shortest-path predecessor chain")
        seen.add(vertex)
        u, j = parent[vertex]
        path.append((u, j))
        vertex = u
    if sum(graph[u][j].cost for u, j in path) != distance[sink]:
        raise ArithmeticError("Path cost differs from the shortest-path label")
    return path, distance[sink]


def equal_weight_box_ne(
    q: Sequence[int], c: Sequence[Rational], w: Sequence[Rational],
    A: Sequence[Sequence[int]],
) -> dict:
    """Return an indivisible assignment, exact X and Psi, and flow audit.

    Sites are zero-based and q must already be nonincreasing.  Inputs are
    exact integers/Fractions/rational strings; floats and general unequal
    weights raise ValueError.  Repeated entries within an allowed set are
    deduplicated.  Empty clients, including the completely empty network,
    yield zero augmentations and X=c.  Every legal original option is checked
    in the final NE certificate, even if moving there would exit the box.
    """
    q, c, w, choices = _inputs(q, c, w, A)
    m, n = len(q), len(w)
    delta = w[0] if n else Fraction(1, 2)
    homes = tuple(row[0] for row in choices)
    home_count, degree = [0] * m, [0] * m
    for home, row in zip(homes, choices):
        home_count[home] += 1
        for t in row:
            degree[t] += 1
    base = tuple(c[t] - delta * home_count[t] for t in range(m))
    denominator = lcm(delta.denominator, *(z.denominator for z in c))
    scale = denominator * lcm(1, *q)
    source, sink = n + m, n + m + 1
    graph: list[list[_Arc]] = [[] for _ in range(n + m + 2)]
    assignment_arcs = []
    slot_arcs = []
    maximum_cost_bits = 0
    for i, row in enumerate(choices):
        _add_arc(graph, source, i, 0)
        assignment_arcs.append([
            (t, _add_arc(graph, i, n + t, 0, assignment=True)) for t in row])
    for t in range(m):
        slots = []
        for ell in range(degree[t]):
            scaled = (base[t] + ell * delta) * scale / q[t]
            if scaled.denominator != 1:
                raise ArithmeticError("Cost scaling failed")
            cost = scaled.numerator
            maximum_cost_bits = max(maximum_cost_bits, abs(cost).bit_length())
            slots.append(_add_arc(graph, n + t, sink, cost))
        slot_arcs.append(slots)

    total_cost = 0
    reroutes, path_lengths = [], []
    for _ in range(n):
        path, cost = _shortest_path(graph, source, sink)
        reroutes.append(sum(graph[u][j].assignment_reverse for u, j in path))
        path_lengths.append(len(path))
        for u, j in path:
            arc = graph[u][j]
            if arc.capacity != 1:
                raise ArithmeticError("A unit augmentation encountered a nonunit residual arc")
            arc.capacity -= 1
            graph[arc.target][arc.reverse].capacity += 1
        total_cost += cost

    assignment, count = [], [0] * m
    for i, refs in enumerate(assignment_arcs):
        selected = [t for t, j in refs if graph[i][j].capacity == 0]
        if len(selected) != 1:
            raise ArithmeticError("Incomplete or nonintegral client assignment")
        assignment.append(selected[0])
        count[selected[0]] += 1
    for t, refs in enumerate(slot_arcs):
        used = [graph[n + t][j].capacity == 0 for j in refs]
        if used != [ell < count[t] for ell in range(len(refs))]:
            raise ArithmeticError("The minimum-cost flow does not use a prefix of site slots")
    x = tuple(base[t] + delta * count[t] for t in range(m))
    if any(not 0 <= z <= 1 for z in x):
        raise ArithmeticError("Full-box certificate failed")
    for i, s in enumerate(assignment):
        external = (x[s] - delta) / q[s]
        if external > (1 - delta) / q[homes[i]]:
            raise ArithmeticError("Home inequality H certificate failed")
        if any(external > x[t] / q[t] for t in choices[i]):
            raise ArithmeticError("Original-option exact NE certificate failed")
    objective = sum(((base[t] * count[t] +
                      delta * count[t] * (count[t] - 1) / 2) / q[t]
                     for t in range(m)), Fraction(0))
    if Fraction(total_cost, scale) != objective:
        raise ArithmeticError("Flow/objective identity failed")
    incidence = sum(degree)
    return dict(
        assignment=assignment, X=list(map(_fraction_text, x)), objective=_fraction_text(objective),
        augmentations=n,
        reverse_assignment_traversals=sum(reroutes),
        max_assignment_reroutes_per_augmentation=max(reroutes, default=0),
        flow_audit=dict(
            vertices=len(graph), forward_arcs=n + 2 * incidence,
            allowed_incidence=incidence, cost_scale=_integer_text(scale),
            cost_scale_bits=scale.bit_length(), maximum_integer_cost_bits=maximum_cost_bits,
            scaled_total_cost=_integer_text(total_cost),
            negative_base_sites=[t for t in range(m) if base[t] < 0],
            augmentation_path_lengths=path_lengths,
            assignment_reroutes_per_augmentation=reroutes,
            exact_ne=True, full_boxes=True, home_inequality=True,
            indivisible_clients=True, prefix_slots=True,
            complexity='bit-polynomial normalized equal-weight on-path selector'))
