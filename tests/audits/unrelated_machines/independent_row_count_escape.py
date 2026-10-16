#!/usr/bin/env python3
"""共享逃逸紧凑族的独立计数、配置、双机及精确对称动态规划审计。

Independent implementation: imports no project matching or family implementation.
Fractions and integers only. Default output is stdout; no frozen evidence modified.
Finite checks are not proofs of the general family or of any approximation claim.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import platform


def build_family(k):
    if type(k) is not int or k < 2:
        raise ValueError('integer k >= 2 required')
    nblocks = 2*k*k
    kinds, edges, blocks = [], [], []
    def machine(kind, block=None):
        i = len(kinds); kinds.append((kind, block)); return i
    def job(times):
        j = len(edges); edges.append(times); return j
    vs = [machine('V', a) for a in range(nblocks)]
    gs = [machine('G') for _ in range(nblocks-2*k)]
    rs = [[machine('R', a) for _ in range(k+1)] for a in range(nblocks)]
    z = machine('z')
    for a in range(nblocks):
        x = job({vs[a]: F(1), **{g: F(1) for g in gs}})
        zs = [job({vs[a]: F(1,k), **{r: F(1) for r in rs[a]}}) for _ in range(k)]
        ys = [job({z: F(1,k), **{r: F(1) for r in rs[a]}}) for _ in range(k)]
        blocks.append({'v': vs[a], 'r': rs[a], 'x': x, 'z': zs, 'y': ys})
    serial = [[sorted((i, str(t)) for i,t in e.items())] for e in edges]
    digest = sha256(json.dumps(serial, separators=(',',':')).encode()).hexdigest()
    return {'k': k, 'N': nblocks, 'kinds': kinds, 'edges': edges,
            'blocks': blocks, 'g': gs, 'z': z, 'input_sha256': digest}


def row_capacities(f):
    rows = [[] for _ in f['kinds']]
    for e in f['edges']:
        for i,t in e.items(): rows[i].append(t)
    caps = [min(len(f['edges']), F(1)//min(row)) for row in rows]
    for i,(kind,_) in enumerate(f['kinds']):
        assert caps[i] == (f['k'] if kind in ('V','z') else 1)
    return rows,caps


def avoid_assignment(f, omitted):
    k,N = f['k'],f['N']; kind,a = f['kinds'][omitted]
    blocked = {a} if kind in ('V','R') else set()
    needed = 2*k + (kind == 'G')
    active = set([b for b in range(N) if b not in blocked][:needed])
    assert len(active) == needed
    available_g = iter(g for g in f['g'] if g != omitted)
    assignment = {}
    for b,block in enumerate(f['blocks']):
        v = block['v']; available_r = [r for r in block['r'] if r != omitted]
        assignment[block['x']] = v if b in active else next(available_g)
        if v == omitted:
            for j,r in zip(block['z'],available_r): assignment[j] = r
            for j in block['y'][:-1]: assignment[j] = f['z']
            assignment[block['y'][-1]] = available_r[k]
        else:
            if b in active:
                assignment[block['z'][0]] = available_r.pop(0)
                for j in block['z'][1:]: assignment[j] = v
            else:
                for j in block['z']: assignment[j] = v
            for j,r in zip(block['y'],available_r): assignment[j] = r
    assert len(assignment) == len(f['edges'])
    return assignment


def audit_avoidance(k):
    f = build_family(k); rows,caps = row_capacities(f)
    checked_assignments = 0; maximum_z = 0
    for omitted in range(len(f['kinds'])):
        sigma = avoid_assignment(f,omitted); counts = Counter(sigma.values())
        assert omitted not in counts
        for j,i in sigma.items(): assert i in f['edges'][j]
        assert all(counts[i] <= caps[i] for i in counts)
        maximum_z = max(maximum_z,counts[f['z']])
        checked_assignments += len(sigma)
    # Same finite inputs have no initial minimal-star, singleton or two-domain rule.
    assert all(sum(row,F(0))-min(row) > 1 for row in rows)
    assert all(len(e) > 2 for e in f['edges'])
    return {'k':k,'machines':len(f['kinds']),'jobs':len(f['edges']),
            'eligible_edges':sum(map(len,f['edges'])),
            'all_machine_avoidance_certificates':len(f['kinds']),
            'job_assignments_checked':checked_assignments,
            'maximum_z_count':maximum_z,'z_count_capacity':k,
            'no_initial_minimal_star_or_small_domain':True,
            'input_sha256':f['input_sha256']}


def configurations(f):
    k,N = f['k'],f['N']; configs = [{} for _ in f['kinds']]
    xs = [b['x'] for b in f['blocks']]
    for b in f['blocks']:
        configs[b['v']] = {(b['x'],):F(1,k),tuple(b['z']):F(k-1,k)}
        rc = {(j,):F(1,k+1) for j in b['y']}
        rc.update({(j,):F(1,k*(k+1)) for j in b['z']})
        for r in b['r']: configs[r] = dict(rc)
    for g in f['g']: configs[g] = {(j,):F(1,N) for j in xs}
    configs[f['z']] = {():F(1)}
    return configs


def check_pair(left,right,terms):
    lm = defaultdict(F); rm = defaultdict(F)
    for a,b,w in terms:
        assert w >= 0 and not (set(a)&set(b))
        lm[a] += w; rm[b] += w
    assert dict(lm) == left and dict(rm) == right


def audit_configurations_and_pairs(k):
    f = build_family(k); configs = configurations(f); coverage = defaultdict(F)
    for i,cs in enumerate(configs):
        assert sum(cs.values(),F(0)) == 1
        for c,w in cs.items():
            assert w >= 0 and len(set(c)) == len(c)
            assert sum((f['edges'][j][i] for j in c),F(0)) <= 1
            for j in c: coverage[j] += w
    assert all(coverage[j] == 1 for j in range(len(f['edges'])))
    N = f['N']; xs = [b['x'] for b in f['blocks']]; g0,g1 = f['g'][:2]
    check_pair(configs[g0],configs[g1],
               [((xs[a],),(xs[(a+1)%N],),F(1,N)) for a in range(N)])
    formula_instances = 1
    for a,b in enumerate(f['blocks']):
        r0,r1 = b['r'][:2]
        rr = []
        for label,weight in (('y',F(1,k+1)),('z',F(1,k*(k+1)))):
            rr += [((b[label][h],),(b[label][(h+1)%k],),weight) for h in range(k)]
        check_pair(configs[r0],configs[r1],rr)
        vr = [((b['x'],),(j,),F(1,k*(k+1))) for j in b['z']]
        vr += [((b['x'],),(j,),F(1,k*k*(k+1))) for j in b['y']]
        vr += [(tuple(b['z']),(j,),F(k-1,k*k)) for j in b['y']]
        check_pair(configs[b['v']],configs[r0],vr)
        vg = [((b['x'],),(j,),F(1,k*(N-1))) for j in xs if j != b['x']]
        vg += [(tuple(b['z']),(b['x'],),F(1,N))]
        vg += [(tuple(b['z']),(j,),F(1,N)-F(1,k*(N-1))) for j in xs if j != b['x']]
        check_pair(configs[b['v']],configs[g0],vg)
        formula_instances += 3
    # Every pair is classified. Nonintersecting support unions admit the product.
    unions = [set(j for c in cs for j in c) for cs in configs]
    counts = Counter()
    for i,j in combinations(range(len(configs)),2):
        ki,ai = f['kinds'][i]; kj,aj = f['kinds'][j]
        if not unions[i]&unions[j]: counts['disjoint_support_product'] += 1
        elif ki == kj == 'G': counts['G-G'] += 1
        elif ki == kj == 'R' and ai == aj: counts['same_block_R-R'] += 1
        elif {ki,kj} == {'V','G'}: counts['V-G'] += 1
        elif {ki,kj} == {'V','R'} and ai == aj: counts['same_block_V-R'] += 1
        else: raise AssertionError(('uncovered pair type',i,j))
    return {'k':k,'machine_configuration_distributions_checked':len(configs),
            'all_jobs_exactly_covered':len(f['edges']),
            'pair_formula_instances_checked':formula_instances,
            'all_machine_pairs_classified':dict(sorted(counts.items())),
            'pair_scope':'Shared-support pair formulas checked in each block; all identical G/R copies use relabeling; other pairs use disjoint-support product.',
            'input_sha256':f['input_sha256']}


def local_minimum_z(k,mu,active):
    """Exact quotient DP of all assignments of k labeled Z then k labeled Y.

    Times are measured in units 1/k; the active X consumes k center units.
    R machines are identical and their sorted occupancies quotient only their
    permutations. Every successor is a real task assignment, and every real
    assignment maps to one successor. The z count is retained, not rounded.
    """
    if type(active) is not bool: raise ValueError('active is boolean')
    start = (k*active,0,(0,)*(k+1))
    if start[0] > mu: return None,0
    rcap = mu//k
    states = {start}; states_seen = 1
    for label in ['Z']*k+['Y']*k:
        nxt = set()
        for vu,zc,rs in states:
            if label == 'Z' and vu+1 <= mu: nxt.add((vu+1,zc,rs))
            if label == 'Y' and zc+1 <= mu: nxt.add((vu,zc+1,rs))
            for index,load in enumerate(rs):
                if load < rcap:
                    changed = list(rs); changed[index] += 1
                    nxt.add((vu,zc,tuple(sorted(changed))))
        states = nxt; states_seen += len(states)
    return min((zc for _,zc,_ in states),default=None),states_seen


def audit_exact_optimum(k):
    N = 2*k*k; nG = N-2*k; trials = []; states_seen = 0
    # All schedules have loads integer multiples of 1/k. The known explicit
    # upper schedule is (2k-1)/k, so lower candidates are this complete grid.
    for mu in range(2*k):
        costs = []
        for active in (False,True):
            val,seen = local_minimum_z(k,mu,active); costs.append(val); states_seen += seen
        possible = []
        for active_count in range(N+1):
            if N-active_count > nG*(mu//k): continue
            if active_count and costs[1] is None: continue
            if N-active_count and costs[0] is None: continue
            zcost = active_count*(costs[1] or 0)+(N-active_count)*(costs[0] or 0)
            if zcost <= mu: possible.append((zcost,active_count))
        feasible = bool(possible)
        assert feasible == (mu == 2*k-1)
        trials.append({'target':str(F(mu,k)),'inactive_min_z':costs[0],
                       'active_min_z':costs[1],'globally_feasible':feasible,
                       'best_global_z_and_active':min(possible) if possible else None})
    return {'k':k,'claimed_and_DP_optimum':str(F(2*k-1,k)),
            'all_grid_targets_through_optimum':trials,
            'quotient_DP_states_visited':states_seen,
            'scope':'Exact symmetric assignment DP for this finite family, with all targets mu/k below and at the explicit upper bound; not exhaustive assignment enumeration.'}


def audit():
    return {'audit':'independent_row_count_escape','python':platform.python_version(),
            'arithmetic':'fractions.Fraction and arbitrary-precision integers; no tolerance',
            'seed':None,'seed_reason':'deterministic enumeration and explicit certificates',
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'import_contract':'standard library only; no project algorithm imported',
            'avoidance':[audit_avoidance(k) for k in range(2,6)],
            'configurations_and_GPC2':[audit_configurations_and_pairs(k) for k in range(2,5)],
            'exact_finite_OPT':[audit_exact_optimum(k) for k in range(2,9)],
            'limitations':['No generic approximation algorithm is tested or proved.',
                           'The symbolic all-k family proof is not replaced by finite audit.',
                           'Avoidance certificates respect domains and static row count capacities, not true loads on all other machines.',
                           'Pair consistency is pairwise only; no global joint distribution is certified.',
                           'Finite OPT uses an exact symmetry quotient; it is not full schedule enumeration.']}


if __name__ == '__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
