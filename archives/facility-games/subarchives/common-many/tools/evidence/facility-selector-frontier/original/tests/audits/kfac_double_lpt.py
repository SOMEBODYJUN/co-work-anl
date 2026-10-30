"""Independent exact finite audit for the greedy dual-packing reset certificate.

This is not an implementation of the published polynomial Nashification
algorithm. Strict replies below check these two finite fixtures only.
"""

from fractions import Fraction as F
import json


def fixture(split=False, triangle=False):
    clients = [
        ("H1", 110, "H"), ("H2", 110, "H"), ("H3", 110, "H"),
        ("H4", 60, "H"), ("H5", 54 if triangle else 59, "H"),
        ("M1", 140, "M"), ("M2", 100, "M"), ("M3", 80, "M"),
        ("L1", 100, "L"),
    ]
    clients += [("X", 30, "HM"), ("Z", 20, "HM")] if split else [("X", 50, "HM")]
    clients += [("Y", 60, "ML")]
    if triangle:
        clients += [("Z", 5, "HL")]
    return [(name, F(w), set(options)) for name, w, options in clients]


def greedy(clients, sites=("H", "M", "L"), k=8):
    q = dict.fromkeys(sites, 0)
    pools = {s: [] for s in sites}
    covered, trace = set(), []
    for _ in range(k):
        scores = {
            s: (sum((clients[i][1] for i in pools[s]), F(0)) / (q[s] + 1)
                if q[s] else sum((w for i, (_, w, options) in enumerate(clients)
                                 if i not in covered and s in options), F(0)))
            for s in sites
        }
        s = max(sites, key=lambda t: scores[t])
        assert sum(value == scores[s] for value in scores.values()) == 1
        trace.append((s, scores[s]))
        if not q[s]:
            pools[s] = [i for i, (_, _, options) in enumerate(clients)
                        if i not in covered and s in options]
            covered.update(pools[s])
        q[s] += 1
    return q, pools, trace


def lpt(clients, pool, h):
    assert h > 0
    bins, loads = [[] for _ in range(h)], [F(0)] * h
    for i in sorted(pool, key=lambda i: (-clients[i][1], i)):
        f = min(range(h), key=lambda f: (loads[f], f))
        bins[f].append(i)
        loads[f] += clients[i][1]
    return bins, loads


def state(clients, layout, bins):
    loads = [sum((clients[i][1] for i in pool), F(0)) for pool in bins]
    served = [i for pool in bins for i in pool]
    assert len(served) == len(set(served))
    assert set(served) == {i for i, (_, _, options) in enumerate(clients)
                           if any(s in options for s in layout)}
    moves = []
    for f, pool in enumerate(bins):
        for i in pool:
            _, w, options = clients[i]
            assert layout[f] in options
            for g, s in enumerate(layout):
                if g != f and s in options and loads[g] + w < loads[f]:
                    moves.append((i, f, g))
    return loads, moves


def finite_equilibrate(clients, layout, bins, cap):
    bins = [list(pool) for pool in bins]
    seen, steps = set(), 0
    while True:
        key = tuple(tuple(sorted(pool)) for pool in bins)
        assert key not in seen
        seen.add(key)
        loads, moves = state(clients, layout, bins)
        assert max(loads) <= cap
        if not moves:
            return bins, loads, steps
        i, f, g = min(moves, key=lambda move: (move[0], move[2], move[1]))
        old_potential = sum(x * x for x in loads)
        bins[f].remove(i)
        bins[g].append(i)
        new_loads, _ = state(clients, layout, bins)
        assert sum(x * x for x in new_loads) < old_potential
        steps += 1


def audit(split=False, triangle=False):
    assert not (split and triangle)
    clients = fixture(split, triangle)
    sites = ("H", "M", "L")
    q, pools, trace = greedy(clients, sites)
    assert q == {"H": 4, "M": 3, "L": 1}
    assert trace == [("H", F(499)), ("M", F(380)), ("H", F(499, 2)),
                     ("M", F(190)), ("H", F(499, 3)), ("M", F(380, 3)),
                     ("H", F(499, 4)), ("L", F(100))]
    gamma = trace[-1][1]
    layout, on_bins = [], []
    normal, deletion = {}, {}
    for s in sites:
        normal[s], loads = lpt(clients, pools[s], q[s])
        assert min(loads) >= gamma
        assert max(loads) <= 2 * gamma
        layout.extend([s] * q[s])
        on_bins.extend(normal[s])
        if q[s] > 1:
            deletion[s], delete_loads = lpt(clients, pools[s], q[s] - 1)
            assert max(delete_loads) <= 2 * gamma
    _, moves = state(clients, layout, on_bins)
    assert len(moves) == (2 if split or triangle else 1)
    on_bins = [list(pool) for pool in on_bins]
    if triangle:
        z_id = next(i for i, (name, _, _) in enumerate(clients) if name == "Z")
        z_moves = [move for move in moves if move[0] == z_id]
        assert len(z_moves) == 1
        i, f, g = z_moves[0]
        on_bins[f].remove(i)
        on_bins[g].append(i)
        _, moves = state(clients, layout, on_bins)
        assert len(moves) == 1
    x_id = next(i for i, (name, _, _) in enumerate(clients) if name == "X")
    x_moves = [move for move in moves if move[0] == x_id]
    assert len(x_moves) == 1
    i, f, g = x_moves[0]
    on_bins[f].remove(i)
    on_bins[g].append(i)
    on_loads, moves = state(clients, layout, on_bins)
    assert not moves
    assert min(on_loads) >= gamma
    totals = {s: sum(load for t, load in zip(layout, on_loads) if t == s) for s in sites}
    assert totals["M"] == (F(410) if split else F(430))
    assert totals["M"] > (q["M"] + 1) * gamma
    # Old RANGE fails at Y. The light chain's center M opens after H.
    assert F(380 - 60, 3) > gamma
    # In the split fixture the HM edge has two unequal light weights.
    if split:
        assert {w for _, w, options in clients if options == {"H", "M"}} == {F(20), F(30)}
    if triangle:
        assert on_loads == list(map(F, [110, 110, 110, 114, 140, 150, 140, 105]))
        assert {frozenset(options) for _, w, options in clients
                if len(options) == 2 and w < gamma} == {
                    frozenset({"H", "M"}), frozenset({"M", "L"}), frozenset({"H", "L"})}
    deviation_report = []
    for f, u in enumerate(layout):
        for r in sites:
            if r == u:
                continue
            new_layout = list(layout)
            new_layout[f] = r
            bins = [[] for _ in new_layout]
            for t in sites:
                stationary = [g for g, s in enumerate(layout) if s == t and g != f]
                if t == u and q[u] == 1:
                    # Here L1 is the only original singleton-pool client and
                    # becomes unserved after L disappears.
                    assert all(not any(s in clients[i][2] for s in new_layout)
                               for i in pools[t])
                    continue
                packing = deletion[t] if t == u else normal[t]
                assert len(packing) == len(stationary)
                for g, pool in zip(stationary, packing):
                    bins[g] = list(pool)
            assert not bins[f]
            _, loads, steps = finite_equilibrate(clients, new_layout, bins, 2 * gamma)
            assert loads[f] <= 2 * on_loads[f]
            deviation_report.append({"facility": f, "target": r,
                                     "deviator_load": str(loads[f]), "steps": steps})
    assert len(deviation_report) == 16
    return {
        "split_HM_edge": split,
        "triangle_light_graph": triangle,
        "greedy_trace": [(s, str(score)) for s, score in trace],
        "on_path_loads": list(map(str, on_loads)),
        "site_totals": {s: str(total) for s, total in totals.items()},
        "actual_deviations_checked": len(deviation_report),
        "max_deviation_load": str(max(F(row["deviator_load"]) for row in deviation_report)),
        "deviations": deviation_report,
    }


if __name__ == "__main__":
    print(json.dumps([audit(triangle=True)], indent=2))
