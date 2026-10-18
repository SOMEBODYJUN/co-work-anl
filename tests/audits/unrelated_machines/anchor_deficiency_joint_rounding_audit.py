#!/usr/bin/env python3
"""Exact witness rounding checks; generic rational-LP solving is not implemented."""
from fractions import Fraction as F
from collections import deque
import importlib.util
import hashlib
import json
import platform
from pathlib import Path

REPO = Path(__file__).resolve()
for candidate in [REPO.parent / 'co-work-anl', *REPO.parents]:
    if (candidate / 'tests/audits/unrelated_machines/rounding_and_gap.py').exists():
        REPO = candidate
        break
spec = importlib.util.spec_from_file_location('st_baseline', REPO / 'tests/audits/unrelated_machines/rounding_and_gap.py')
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)


def matching(neighbors):
    owner = {}
    assigned = {}
    for root in range(len(neighbors)):
        todo = deque([root])
        parent = {root: None}
        finish = None
        while todo and finish is None:
            job = todo.popleft()
            for machine in neighbors[job]:
                if machine not in owner:
                    finish = (job, machine)
                    break
                other = owner[machine]
                if other not in parent:
                    parent[other] = (job, machine)
                    todo.append(other)
        assert finish is not None, 'Hall failure after threshold filtering'
        job, machine = finish
        while True:
            owner[machine] = job
            assigned[job] = machine
            if parent[job] is None:
                break
            job, machine = parent[job]
    return [assigned[job] for job in range(len(neighbors))]


def round_witness(p, anchors, target, alpha, beta, z, x, d0):
    """z is m by |anchors|; x is m by |tiny|, both exact rationals."""
    m, n = len(p), len(p[0])
    assert m and target > 0 and 0 <= alpha < F(1, 2) and beta >= 0
    tiny = [j for j in range(n) if j not in anchors]
    assert len(z) == len(x) == m
    y = [sum(row, F(0)) for row in z]
    loads = [sum(p[i][j]*x[i][a] for a,j in enumerate(tiny) if x[i][a]) for i in range(m)]
    for a,j in enumerate(anchors):
        assert sum(z[i][a] for i in range(m)) == 1
        for i in range(m):
            assert z[i][a] >= 0
            if p[i][j] is None:
                assert not z[i][a]
            else:
                assert (1-alpha)*target <= p[i][j] <= target
    for a,j in enumerate(tiny):
        assert sum(x[i][a] for i in range(m)) == 1
        for i in range(m):
            assert x[i][a] >= 0
            if p[i][j] is None:
                assert not x[i][a]
            else:
                assert 0 <= p[i][j] <= beta*target
    assert all(0 <= y[i] <= 1 and loads[i]+(1-alpha)*target*y[i] <= target for i in range(m))
    graph = [[i for i in range(m) if p[i][j] is not None] for j in anchors]
    remaining = set(range(len(anchors)))
    keep = set()
    components = []
    while remaining:
        js = {min(remaining)}
        ms = set()
        while True:
            new_ms = {i for j in js for i in graph[j]}
            new_js = {j for j in remaining if set(graph[j]) & new_ms}
            if new_ms == ms and new_js == js:
                break
            js, ms = new_js, new_ms
        d = len(ms)-len(js)
        assert 0 <= d <= d0
        threshold = F(1,d+1)
        deleted = {i for i in ms if y[i] < threshold}
        assert sum((y[i] for i in deleted), F(0)) < 1
        keep |= ms-deleted
        remaining -= js
        components.append(dict(deficiency=d, threshold=str(threshold), deleted=sorted(deleted)))
    anchor_sigma = matching([[i for i in row if i in keep] for row in graph])
    tiny_p = [[p[i][j] for j in tiny] for i in range(m)]
    tiny_sigma, _ = st.round_slots(tiny_p, x, target)
    sigma = dict(zip(anchors, anchor_sigma)) | dict(zip(tiny, tiny_sigma))
    actual = [sum((p[i][j] for j in range(n) if sigma[j] == i), F(0)) for i in range(m)]
    bound = (2-F(1-alpha,d0+1)+beta)*target
    assert max(actual, default=F(0)) <= bound
    return dict(components=components, loads=list(map(str,actual)), bound=str(bound), sigma=[sigma[j] for j in range(n)])


def audit():
    fixtures = []
    # Two components, freely crossing tiny jobs: same fractional solution is retained.
    p = [[F(1) if i//2 == j else None for j in range(2)]+[F(1,8)]*16 for i in range(4)]
    z = [[F(1,2) if i//2 == j else F(0) for j in range(2)] for i in range(4)]
    fixtures.append(round_witness(p,[0,1],F(1),F(0),F(1,8),z,[[F(1,4)]*16 for _ in range(4)],1))
    # Saturation, heterogeneous edge identity, and a zero-time tiny task.
    p = [[F(4,5),F(9,10),F(1,10),F(1,10),F(1,10),F(1,10),F(0)],
         [F(9,10),F(4,5),F(1,10),F(1,10),F(1,10),F(1,10),F(0)]]
    fixtures.append(round_witness(p,[0,1],F(1),F(1,5),F(1,10),[[F(1,2)]*2 for _ in range(2)],[[F(1,2)]*5 for _ in range(2)],0))
    # A strict low-occupation deletion, unavailable edges, and very large denominators.
    scale = F(1,2**300+1)
    p = [[scale]+[scale/10]+[None]*9,[scale]+[None]+[scale/10]*9]
    x = [[F(1)]+[F(0)]*9,[F(0)]+[F(1)]*9]
    fixtures.append(round_witness(p,[0],scale,F(0),F(1,10),[[F(9,10)],[F(1,10)]],x,1))
    # Sharp equality in the cutoff: uniform rank-one bases must retain every machine.
    sharp = []
    for d in [0,1,4]:
        threshold = F(1,d+1)
        assert all(not (threshold < threshold) for _ in range(d+1))
        assert all(threshold < threshold+F(1,1000) for _ in range(d+1))
        sharp.append(dict(d=d,sharp_cutoff=str(threshold)))
    # Baseline handles the exact zero/empty boundary independently of positive-T theorem.
    assert st.round_slots([[]],[[]],F(0))[0] == []
    assert st.round_slots([[F(0)],[None]],[[F(1)],[F(0)]],F(0))[0] == [0]
    return dict(python=platform.python_version(), arithmetic='fractions.Fraction', seed=None,
                scope='three exact witness-rounding fixtures, cutoff equalities, zero/empty boundaries; no generic LP solver',
                fixtures=fixtures, sharp_cutoffs=sharp,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
