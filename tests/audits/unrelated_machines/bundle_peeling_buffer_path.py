"""Polynomial given-target migration via bundles and incoming-weight peeling.

The target assignment is an input.  This is not a target finder or an
approximation algorithm.  Enumeration appears only in the separate audit.
"""
from fractions import Fraction as F


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise ValueError("exact integer or Fraction required")
    return F(value)


def bundle_peeling_path(edges, fixed, C, T):
    """Return a complete direct-migration order, never a feasibility verdict.

    Each edge is (source, target, source_time, target_time), with distinct
    endpoints.  Fixed loads represent jobs whose owner does not change.
    Invalid inputs raise ValueError; every valid input returns a path.
    """
    C, T = rational(C), rational(T)
    fixed = [rational(v) for v in fixed]
    m = len(fixed)
    if not m or not 0 <= T <= C <= 2*T or any(v < 0 for v in fixed):
        raise ValueError("invalid machines, scale, or fixed loads")
    normalized = []
    for edge in edges:
        if len(edge) != 4:
            raise ValueError("edge must have four fields")
        s, t, a, b = edge
        if (isinstance(s, bool) or isinstance(t, bool)
                or not isinstance(s, int) or not isinstance(t, int)
                or not 0 <= s < m or not 0 <= t < m or s == t):
            raise ValueError("invalid changing-job endpoints")
        a, b = rational(a), rational(b)
        if not 0 <= a <= T or not 0 <= b <= T:
            raise ValueError("unpruned or negative processing time")
        normalized.append((s, t, a, b))
    edges = normalized
    outgoing = [[] for _ in fixed]
    A, Q = [F(0)]*m, [F(0)]*m
    for j, (s, t, a, b) in enumerate(edges):
        outgoing[s].append(j)
        A[s] += a
        Q[t] += b
    S = [f+a for f, a in zip(fixed, A)]
    if max(S) > C or any(f+q > T for f, q in zip(fixed, Q)):
        raise ValueError("initial or supplied target exceeds its bound")
    U = max(2*T, C+T/2)
    h = [max(F(0), s+q-U) for s, q in zip(S, Q)]
    H = {i for i in range(m) if h[i] > 0}
    bundles = {}
    for i in sorted(H):
        eligible = [j for j in outgoing[i] if edges[j][2] >= h[i]]
        if eligible:
            chosen = [eligible[0]]
        else:
            chosen, total = [], F(0)
            for j in outgoing[i]:
                if edges[j][2] == 0:
                    continue
                chosen.append(j)
                total += edges[j][2]
                if total >= h[i]:
                    break
        amount = sum((edges[j][2] for j in chosen), F(0))
        assert h[i] <= amount <= T and A[i]-amount >= h[i]
        bundles[i] = chosen
    selected = {j for chosen in bundles.values() for j in chosen}
    W, removed, done, order = set(H), [], set(), []
    phase_ends = []

    def move(j):
        if j not in done:
            done.add(j)
            order.append(j)

    # Permanently safe receivers outside H may receive selected core exits.
    for j in sorted(selected):
        if edges[j][1] not in H:
            move(j)
    phase_ends.append(len(order))
    # A not-yet-peeled vertex has received no selected input in this phase.
    while W:
        candidates = []
        for v in sorted(W):
            incoming = [j for j in sorted(selected)
                        if edges[j][0] in W and edges[j][1] == v]
            if sum((edges[j][3] for j in incoming), F(0)) < h[v]:
                candidates.append((v, incoming))
        if not candidates:
            break
        v, incoming = candidates[0]
        W.remove(v)
        removed.append(v)
        for j in incoming:
            move(j)
    phase_ends.append(len(order))
    core = set(W)
    held = {j for j in selected if edges[j][0] in core and edges[j][1] in core}
    for v in reversed(removed):
        for j in bundles[v]:
            move(j)
    phase_ends.append(len(order))
    for j in range(len(edges)):
        if j not in selected:
            move(j)
    phase_ends.append(len(order))
    for j in sorted(held):
        move(j)
    phase_ends.append(len(order))
    assert len(order) == len(edges) and len(done) == len(edges)

    # Linear replay, separate from the combinatorial choice of order.
    current, evacuated, peak = S.copy(), [F(0)]*m, max(S)
    for k, j in enumerate(order):
        s, t, a, b = edges[j]
        current[s] -= a
        current[t] += b
        evacuated[s] += a
        assert min(current) >= 0 and max(current) <= U
        peak = max(peak, max(current))
        if k+1 == phase_ends[3]:
            assert all(evacuated[i] >= h[i] for i in H)
    assert current == [f+q for f, q in zip(fixed, Q)]
    return {"order": order, "peak": str(peak), "bound": str(U),
            "bundles": {str(i): js for i, js in bundles.items()},
            "peeling_order": removed, "held_core": sorted(core),
            "held_jobs": sorted(held), "phase_ends": phase_ends}
