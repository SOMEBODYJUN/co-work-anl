"""Exact finite attacks; none of these finite runs is a universal proof.

The generalized profile checker has its own constructor and reconstructs each
prefix from edge ownership.  The production checker imports only the canonical
path routine and independently reconstructs every load.
"""
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
from random import Random
import json
import platform


ROOT = Path(__file__).resolve().parents[3]
MODULE = ROOT/'tests/audits/unrelated_machines/bundle_peeling_buffer_path.py'
PROOF = ROOT/'research/current/unrelated_machines/bundle_inflow_peeling_and_pruned_transient_sharpness.md'
AUDIT = ROOT/'tests/audits/unrelated_machines/bundle_peeling_path_audit.py'
spec = spec_from_file_location('canonical_bundle_path', MODULE)
mod = module_from_spec(spec)
spec.loader.exec_module(mod)


def actual(edges, fixed, moved):
    load = list(fixed)
    for j, (s, t, a, b) in enumerate(edges):
        if j in moved:
            load[t] += b
        else:
            load[s] += a
    return load


def production_check(edges, fixed, C, T):
    result = mod.bundle_peeling_path(edges, fixed, C, T)
    order = result['order']
    assert sorted(order) == list(range(len(edges)))
    U = max(2*T, C+T/2)
    trace, moved = [actual(edges, fixed, set())], set()
    for j in order:
        assert j not in moved
        moved.add(j)
        trace.append(actual(edges, fixed, moved))
    assert all(0 <= v <= U for loads in trace for v in loads)
    assert F(result['peak']) == max(max(row) for row in trace)
    assert max(trace[-1]) <= T
    assert len(result['phase_ends']) == 5
    assert result['phase_ends'] == sorted(result['phase_ends'])
    assert result['phase_ends'][-1] == len(edges)
    return result, trace


def profile_order(edges, fixed, parts):
    """Integer inputs, doubled rational capacities; no uniform scale bounds."""
    m = len(fixed)
    out, q = [0]*m, [0]*m
    for s, t, a, b in edges:
        out[s] += a
        q[t] += b
    p = [sum(edges[j][2] for j in parts[i]) for i in range(m)]
    S = [fixed[i]+out[i] for i in range(m)]
    Fnl = [fixed[i]+q[i] for i in range(m)]
    M = [max(p[i], out[i]-p[i]) for i in range(m)]
    cap2 = [max(2*S[i]+q[i], 2*Fnl[i]+2*M[i]) for i in range(m)]
    h2 = [max(0, 2*S[i]+2*q[i]-cap2[i]) for i in range(m)]
    assert all(h2[i] == min(q[i], 2*min(p[i], out[i]-p[i])) for i in range(m))
    H = {i for i in range(m) if h2[i]}
    selected = set().union(*(set(parts[i]) for i in H)) if H else set()
    live, deleted, done, order = set(H), [], set(), []

    def push(j):
        if j not in done:
            done.add(j)
            order.append(j)

    for j in sorted(selected):
        if edges[j][1] not in H:
            push(j)
    while live:
        chosen = None
        for v in sorted(live):
            incoming = [j for j in selected if edges[j][0] in live and edges[j][1] == v]
            if 2*sum(edges[j][3] for j in incoming) < h2[v]:
                chosen = (v, sorted(incoming))
                break
        if chosen is None:
            break
        v, incoming = chosen
        for j in incoming:
            push(j)
        live.remove(v)
        deleted.append(v)
    held = {j for j in selected if edges[j][0] in live and edges[j][1] in live}
    for v in reversed(deleted):
        for j in sorted(parts[v]):
            push(j)
    for j in range(len(edges)):
        if j not in selected:
            push(j)
    before_release = len(order)
    for j in sorted(held):
        push(j)
    assert sorted(order) == list(range(len(edges)))
    moved = set()
    assert all(2*x <= u for x, u in zip(actual(edges, fixed, moved), cap2))
    for k, j in enumerate(order):
        moved.add(j)
        load = actual(edges, fixed, moved)
        assert all(0 <= 2*x <= u for x, u in zip(load, cap2))
        if k < before_release:
            assert moved.isdisjoint(held)
    return len(deleted), len(live), len(held)


def run():
    stats = {'production_random_cases': 0, 'profile_exhaustive_cases': 0,
             'profile_random_cases': 0, 'profile_nonempty_cores': 0,
             'profile_peeling_cases': 0, 'lpt_integer_cases': 0}
    rng = Random(6199027)
    for _ in range(800):
        m = rng.randrange(2, 9)
        denom = 24
        T, C = F(1), F(rng.randrange(24, 49), denom)
        fints = [rng.randrange(0, 13) if rng.randrange(3) == 0 else 0 for i in range(m)]
        a_used, b_used, edges = [0]*m, [0]*m, []
        for j in range(rng.randrange(0, 41)):
            s = rng.randrange(m)
            t = rng.randrange(m-1)
            t += t >= s
            a = rng.randrange(min(denom, int(C*denom)-fints[s]-a_used[s])+1)
            b = rng.randrange(denom-fints[t]-b_used[t]+1)
            a_used[s] += a
            b_used[t] += b
            edges.append((s, t, F(a, denom), F(b, denom)))
        scale = F(1, 2**521+1) if stats['production_random_cases'] % 53 == 0 else F(1)
        production_check([(s,t,a*scale,b*scale) for s,t,a,b in edges],
                         [F(f,denom)*scale for f in fints], C*scale, T*scale)
        stats['production_random_cases'] += 1

    # Reverse deletion may have unbounded depth; no fixed-depth inference.
    m = 96
    deep = [(s, (s+1) % m, F(3,8), b)
            for s in range(m)
            for b in ([F(1,8)]*2+[F(3,8)]*2 if s == m-1
                      else [F(3,8)]*2+[F(1,8)]*2)]
    result, trace = production_check(deep, [F(0)]*m, F(3,2), F(1))
    assert result['peeling_order'] == list(range(m)) and not result['held_core']
    stats['deep_peeling'] = {'vertices': m, 'arcs': len(deep),
                              'deletion_depth': len(result['peeling_order']),
                              'peak': result['peak'], 'bound': result['bound']}

    # Two-machine input grid; all 16 designated source partitions, including
    # empty halves, and all 3^8 choices of four source/target endpoint pairs.
    endpoints = [(0,1), (0,1), (1,0), (1,0)]
    for vals in product(range(3), repeat=8):
        edges = [(s,t,vals[2*j],vals[2*j+1]) for j,(s,t) in enumerate(endpoints)]
        for mask in range(16):
            parts = [[j for j in range(4) if endpoints[j][0] == i and mask >> j & 1]
                     for i in range(2)]
            profile_order(edges, [3,7], parts)
            stats['profile_exhaustive_cases'] += 1

    for _ in range(1200):
        m = rng.randrange(2, 21)
        parts, edges = [[] for i in range(m)], []
        for j in range(rng.randrange(0, 121)):
            s = rng.randrange(m)
            t = rng.randrange(m-1)
            t += t >= s
            edges.append((s,t,rng.randrange(51),rng.randrange(51)))
            if rng.randrange(2):
                parts[s].append(j)
        deleted, core, held = profile_order(edges, [rng.randrange(31) for i in range(m)], parts)
        stats['profile_random_cases'] += 1
        stats['profile_nonempty_cores'] += bool(core)
        stats['profile_peeling_cases'] += bool(deleted)

    # Exhaustive short integer multisets, deterministic LPT tie to bin zero.
    for n in range(8):
        for sizes in product(range(4), repeat=n):
            bins = [0, 0]
            for a in sorted(sizes, reverse=True):
                bins[0 if bins[0] <= bins[1] else 1] += a
            M, A, amax = max(bins), sum(sizes), max(sizes, default=0)
            assert M <= amax or 3*M <= 2*A
            stats['lpt_integer_cases'] += 1

    sharp = []
    for T in [F(1), F(7,13), F(1,2**509+33)]:
        for ratio in [F(1),F(5,4),F(3,2),F(7,4),F(2)]:
            C = ratio*T
            if C <= 3*T/2:
                edges = [(0,1,T,2*T-C),(1,0,T,2*T-C)]
                fixed = [C-T]*2
            else:
                edges = [(s,1-s,C/2,T/2) for s in range(2) for j in range(2)]
                fixed = [F(0),F(0)]
            result, trace = production_check(edges, fixed, C, T)
            U = max(2*T,C+T/2)
            assert all(max(actual(edges,fixed,{j})) == U for j in range(len(edges)))
            assert F(result['peak']) == U
            assert sum(fixed)+sum(min(a,b) for s,t,a,b in edges) == 2*T
            sharp.append({'T':str(T), 'C_over_T':str(ratio), 'peak':str(U)})
    stats['sharp_cases'] = sharp
    stats['m_zero_contract'] = 'canonical API intentionally raises ValueError; mathematical model assumes m>=1'
    stats['sha256'] = {str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest()
                       for p in [MODULE, AUDIT, PROOF]}
    stats['seed'] = 6199027
    stats['python'] = platform.python_version()
    stats['arithmetic'] = 'integer doubled capacities and fractions.Fraction'
    stats['audit_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    stats['status'] = 'passed'
    stats['scope'] = 'Finite attacks and exact replay only; not a proof, a target finder, or an instance-optimality claim.'
    return stats


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
