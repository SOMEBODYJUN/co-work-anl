"""独立有限核验：私有模式 DP、占用基扩展 face、支持舍入；不证明一般定理。

单文件运行，无第三方依赖。完全枚举各列出的局部实例及各小多面体活跃约束组；
没有调用或验证通用多项式 LP 求解器，没有实现全部 heavy 猜测分支的生产调度器。
默认 JSON 写 stdout；重跑请写 scratch 新文件，不覆盖冻结证据。
"""
from fractions import Fraction as F
from itertools import product, combinations
import hashlib
import json
import platform
import random

SEED = 910217
rng = random.Random(SEED)


def ceilq(x):
    return -((-x.numerator) // x.denominator)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def rank(rows, n):
    a = [list(map(F, r)) for r in rows]
    pivot = 0
    for j in range(n):
        k = next((i for i in range(pivot, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        v = a[pivot][j]
        a[pivot] = [x/v for x in a[pivot]]
        for i in range(pivot+1, len(a)):
            v = a[i][j]
            if v:
                a[i] = [x-v*y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def solve_unique(rows, rhs, n):
    a = [list(map(F, r))+[F(b)] for r, b in zip(rows, rhs)]
    pivots = []
    for j in range(n):
        k = next((i for i in range(len(pivots), len(a)) if a[i][j]), None)
        if k is None:
            continue
        p = len(pivots)
        a[p], a[k] = a[k], a[p]
        v = a[p][j]
        a[p] = [x/v for x in a[p]]
        for i in range(len(a)):
            v = a[i][j] if i != p else F(0)
            if v:
                a[i] = [x-v*y for x, y in zip(a[i], a[p])]
        pivots.append(j)
    if any(not any(row[:n]) and row[n] for row in a):
        return None
    if len(pivots) != n:
        return None
    out = [F(0)]*n
    for i, j in enumerate(pivots):
        out[j] = a[i][n]
    return tuple(out)


def dp_menu(times, K, gamma, N):
    T = F(1)
    s = gamma*T/N
    nh = len(times)
    sinkcap = T//s+nh
    homecaps = [T, T/2]
    rounded = [[None if p is None or p>T else (p if end==0 else ceilq(p/s))
                for end,p in enumerate(row)] for row in times]
    states = {(0,)*K: (F(0), ())}
    for row in rounded:
        new = {}
        for u, (home, path) in states.items():
            for end, a in enumerate(row):
                if a is None:
                    continue
                v = list(u)
                cost = home
                if end == 0:
                    cost += a
                else:
                    v[end-1] += a
                v = tuple(v)
                if any(z>sinkcap for z in v) or cost>homecaps[0]:
                    continue
                candidate = (cost, path+(end,))
                if v not in new or candidate < new[v]:
                    new[v] = candidate
        states = new
    menus = []
    for u, (home, path) in sorted(states.items()):
        for occ, cap in enumerate(homecaps):
            if home <= cap:
                menus.append((occ, u, home, path))
    return s, rounded, sinkcap, homecaps, states, menus


def audit_local():
    palette = [None, F(0), F(1,6), F(1,3), F(2,3), F(1), F(6,5),
               F(1, (1<<40)+87)]
    cases = []
    cases.extend([
        (0, [], 1),
        (1, [], 1),
        (2, [[F(0), None, F(0)]], 1),
        (2, [[None, F(1,3), F(2,3)], [F(1,3), None, F(0)]], 5),
        (1, [[F(1,3), F(1,3)]]*4, 8),
        (2, [[F(1, (1<<40)+87), F(1,2), None]]*3, 3),
        (1, [[None, F(6,5)]], 1),
    ])
    for K in [0,1,2]:
        for _ in range(35):
            nh = rng.randrange(0,5)
            times = [[rng.choice(palette) for _ in range(K+1)] for _ in range(nh)]
            cases.append((K, times, max(1,nh+rng.randrange(0,4))))
    allocations = 0
    modes = 0
    witnesses = 0
    for K, times, N in cases:
        gamma = F(1,4)
        s, rounded, sinkcap, homecaps, states, menus = dp_menu(times,K,gamma,N)
        oracle = {}
        for path in product(range(K+1), repeat=len(times)):
            allocations += 1
            if any(rounded[j][end] is None for j,end in enumerate(path)):
                continue
            actual = [F(0)]*(K+1)
            integers = [0]*(K+1)
            for j,end in enumerate(path):
                actual[end] += times[j][end]
                integers[end] += rounded[j][end]
            u = tuple(integers[1:])
            if integers[0] <= homecaps[0] and all(z<=sinkcap for z in u):
                cand = (integers[0], path)
                if u not in oracle or cand<oracle[u]:
                    oracle[u] = cand
            for occ in [0,1]:
                c = F(1) if occ==0 else F(1,2)
                if actual[0] <= c and all(z<=1 for z in actual[1:]):
                    witnesses += 1
                    assert u in states
                    assert states[u][0] <= homecaps[occ]
        assert states == oracle
        for occ,u,home,path in menus:
            modes += 1
            actual = [F(0)]*(K+1)
            for j,end in enumerate(path):
                actual[end] += times[j][end]
            c = F(1) if occ==0 else F(1,2)
            assert actual[0] <= c
            assert all(actual[k+1] <= s*u[k] for k in range(K))
    return {'cases':len(cases), 'all_assignments_examined':allocations,
            'actual_modes_checked':modes,'feasible_local_witnesses_preserved':witnesses,
            'arithmetic':'fractions.Fraction; complete assignment enumeration per case'}


def audit_zero_target():
    """完整枚举小非负矩阵，独立比较零边条件与实际零负载全分配。"""
    cases=0
    assignments=0
    palette=[None,F(0),F(1),F(1,(1<<40)+87)]
    for machines in [1,2]:
        for jobs in range(4):
            for flat in product(palette,repeat=machines*jobs):
                cases+=1
                rows=[flat[j*machines:(j+1)*machines] for j in range(jobs)]
                zero_edges=all(any(p==0 for p in row) for row in rows)
                actual_zero=False
                for schedule in product(range(machines),repeat=jobs):
                    assignments+=1
                    if any(rows[j][i] is None for j,i in enumerate(schedule)):
                        continue
                    loads=[F(0)]*machines
                    for j,i in enumerate(schedule):
                        loads[i]+=rows[j][i]
                    actual_zero |= max(loads,default=F(0))==0
                assert zero_edges==actual_zero
    return {'matrices':cases,'complete_assignments':assignments,
            'arithmetic':'fractions.Fraction; all listed matrices and all assignments'}


def matching_bases(edges, H):
    B = len(edges)
    return sorted({tuple(sorted(p)) for p in product(*edges)
                   if len(set(p))==B})


def vectors_of_patterns(modes, bases):
    H = len(modes)
    offsets = []
    d = 0
    for qs in modes:
        offsets.append(d)
        d += len(qs)
    out = []
    for chosen in product(*(range(len(qs)) for qs in modes)):
        occ = tuple(h for h in range(H) if modes[h][chosen[h]][0])
        if occ not in bases:
            continue
        vec = [F(0)]*d
        for h,q in enumerate(chosen):
            vec[offsets[h]+q]=1
        out.append(tuple(vec))
    return out, offsets, d


def audit_polytope_case(edges, modes, K, budgets, actual=None):
    H = len(modes)
    beta = F(1,8*K)
    bases = matching_bases(edges,H)
    assert bases
    integral, offsets, d = vectors_of_patterns(modes,bases)
    E=[]; erhs=[]
    for h in range(H):
        row=[F(0)]*d
        for q in range(len(modes[h])):
            row[offsets[h]+q]=1
        E.append(row); erhs.append(F(1))
    occrow=[F(0)]*d
    for h in range(H):
        for q,(o,w) in enumerate(modes[h]):
            occrow[offsets[h]+q]=o
            assert sum(w)<=beta
    E.append(occrow); erhs.append(F(len(edges)))
    P=[]
    for t in range(d):
        row=[F(0)]*d; row[t]=-1
        P.append((row,F(0)))
    for mask in range(1,(1<<H)-1):
        subset={h for h in range(H) if (mask>>h)&1}
        row=[F(0)]*d
        for h in subset:
            for q,(o,w) in enumerate(modes[h]):
                row[offsets[h]+q]=o
        r=max(len(set(base)&subset) for base in bases)
        P.append((row,F(r)))
    resources=[]
    for k in range(K):
        row=[F(0)]*d
        for h in range(H):
            for q,(o,w) in enumerate(modes[h]):
                row[offsets[h]+q]=w[k]
        resources.append(row)
    allc=P+list(zip(resources,budgets))
    neq=rank(E,d)
    vertices=set()
    intersections=0
    for active in combinations(range(len(allc)),d-neq):
        intersections+=1
        rows=E+[allc[t][0] for t in active]
        rhs=erhs+[allc[t][1] for t in active]
        y=solve_unique(rows,rhs,d)
        if y is None or any(dot(row,y)>b for row,b in allc):
            continue
        vertices.add(y)
    checked_roundings=0
    restored_schedules=0
    maxR=0
    for y in vertices:
        R=sum(sum(y[offsets[h]+q]>0 for q in range(len(modes[h])))>1
              for h in range(H))
        maxR=max(maxR,R)
        tight=[row for row,b in P if dot(row,y)==b]
        dimP=d-rank(E+tight,d)
        assert dimP<=K
        assert R<=2*dimP<=2*K
        face_integral=[v for v in integral if all(dot(row,v)==dot(row,y) for row in tight)]
        assert face_integral
        span=[[v[t]-face_integral[0][t] for t in range(d)] for v in face_integral[1:]]
        assert rank(span,d)==dimP
        supported=[v for v in integral if all(not v[t] or y[t]>0 for t in range(d))]
        assert supported
        for v in supported:
            checked_roundings+=1
            changed=sum(any(v[offsets[h]+q] != y[offsets[h]+q]
                            for q in range(len(modes[h]))) for h in range(H))
            assert changed==R
            for row,b in zip(resources,budgets):
                assert dot(row,v)<=dot(row,y)+R*beta<=b+2*K*beta
            if actual is not None:
                selected=[next(q for q in range(len(modes[h]))
                               if v[offsets[h]+q]) for h in range(H)]
                active={h for h,q in enumerate(selected) if modes[h][q][0]}
                matching=next(p for p in product(*edges)
                              if len(set(p))==len(edges) and set(p)==active)
                loads=[F(0)]*(H+K)
                placed=[]
                for h,q in enumerate(selected):
                    path=actual['paths'][(h,q)]
                    assert len(path)==len(actual['times'][h])
                    for j,end in enumerate(path):
                        target=h if end==0 else H+end-1
                        p=actual['times'][h][j][end]
                        assert p is not None
                        loads[target]+=p
                        placed.append(('private',h,j))
                for b,h in enumerate(matching):
                    loads[h]+=F(1)
                    placed.append(('macro',b))
                assert len(placed)==len(set(placed))
                assert len(placed)==sum(len(rows) for rows in actual['times'])+len(edges)
                assert all(load<=F(3,2) for load in loads[:H])
                assert all(loads[H+k]<=budgets[k]+2*K*beta for k in range(K))
                restored_schedules+=1
    return {'vertices':len(vertices),'active_systems':intersections,
            'support_roundings':checked_roundings,'max_fractional_homes':maxR,
            'actual_schedules_restored':restored_schedules}


def audit_faces():
    result=[]
    # Exact dimension bound is attained: a direct sum of K rank-one pairs.
    for K in [1,2]:
        H=2*K; beta=F(1,8*K)
        edges=[(2*k,2*k+1) for k in range(K)]
        modes=[]
        actual={'times':[],'paths':{}}
        for h in range(H):
            w=[F(0)]*K
            if h%2==0:
                w[h//2]=beta
            modes.append([(0,(F(0),)*K),(1,tuple(w))])
            row=[None]*(K+1)
            row[0]=F(3,4)
            row[1+h//2]=beta if h%2==0 else F(0)
            actual['times'].append([row])
            s,rounded,scap,hcaps,states,menu=dp_menu([row],K,F(1,4),H)
            for q,(o,ws) in enumerate(modes[h]):
                u=tuple(int(z/s) for z in ws)
                candidates=[entry for entry in menu if entry[0]==o and entry[1]==u]
                assert candidates
                actual['paths'][(h,q)]=candidates[0][3]
        r=audit_polytope_case(edges,modes,K,[beta/2]*K,actual)
        assert r['max_fractional_homes']==2*K
        result.append(r)
    for K in [1,2]:
        for case in range(12):
            H=3
            edges=[tuple(h for h in range(H) if rng.randrange(3)>0) for _ in range(1+case%2)]
            edges=[e if e else (rng.randrange(H),) for e in edges]
            bases=matching_bases(edges,H)
            if not bases:
                edges=[tuple(range(H)) for _ in edges]
                bases=matching_bases(edges,H)
            beta=F(1,8*K)
            modes=[]
            for h in range(H):
                qs=[]
                for o in [0,1]+([case%2] if h==0 and case%3==0 else []):
                    shares=[rng.randrange(5) for _ in range(K)]
                    denom=max(1,sum(shares))
                    w=tuple(beta*F(s,denom)*F(rng.randrange(1,5),4) for s in shares)
                    qs.append((o,w))
                modes.append(qs)
            iv,offs,d=vectors_of_patterns(modes,bases)
            a=rng.choice(iv); b=rng.choice(iv)
            budgets=[]
            for k in range(K):
                row=[F(0)]*d
                for h in range(H):
                    for q,(o,w) in enumerate(modes[h]):
                        row[offs[h]+q]=w[k]
                budgets.append((dot(row,a)+dot(row,b))/2)
            result.append(audit_polytope_case(edges,modes,K,budgets))
    return {'cases':len(result),
            'vertices':sum(r['vertices'] for r in result),
            'active_systems':sum(r['active_systems'] for r in result),
            'support_roundings':sum(r['support_roundings'] for r in result),
            'actual_schedules_restored':sum(r['actual_schedules_restored'] for r in result),
            'max_fractional_homes':max(r['max_fractional_homes'] for r in result),
            'tight_count_examples':result[:2],
            'arithmetic':'fractions.Fraction; exhaustive active-constraint vertex enumeration'}


def audit_one_sided_bisection():
    """All listed nonmonotone accept/reject tables, independent of any LP.

    This checks the logical threshold-search wrapper only, not a scheduling
    implementation. All q >= optimum must accept; lower q may do either.
    """
    tables = 0
    for optimum in range(1, 13):
        for upper in range(optimum, optimum + 4):
            for mask in range(1 << (optimum - 1)):
                def accepts(q):
                    return q >= optimum or (q > 0 and bool(mask >> (q - 1) & 1))
                lo, hi = 0, upper
                assert not accepts(lo) and accepts(hi)
                steps = 0
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if accepts(mid):
                        hi = mid
                    else:
                        lo = mid
                    assert lo < optimum and accepts(hi)
                    steps += 1
                assert hi <= optimum and accepts(hi)
                assert steps <= upper.bit_length()
                tables += 1
    contract_cases = 0
    for a_scaled in range(1, 33):
        upper = 2 * a_scaled - 1
        for optimum in range(1, upper + 1):
            assert upper >= optimum
            for target in range(upper + 1):
                assert F(a_scaled) > F(target, 2)
            contract_cases += 1
    # Independent geometric-series and odd-sum count reversals.
    assert tables == 4 * ((1 << 12) - 1)
    assert contract_cases == 32 * 32
    return {'acceptance_tables': tables, 'scaled_macro_contract_cases': contract_cases,
            'scope': 'Only finite one-sided threshold logic; not the LP or full scheduler.'}


def main():
    out={'scope':'finite independent audits, not the general proof',
         'python':platform.python_version(),'seed':SEED,
         'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
         'local_menus':audit_local(), 'zero_target':audit_zero_target(),
         'occupation_faces':audit_faces(),
         'one_sided_bisection':audit_one_sided_bisection()}
    parameters=[]
    for K in [1,2,3,10,100]:
        gamma=F(1,4); beta=F(1,8*K)
        sink=1+gamma+2*K*beta
        heavy=K*(1+gamma)/beta
        assert sink==F(3,2)
        assert heavy==10*K*K
        assert (sink-1-gamma)/(2*K)==beta
        assert heavy*beta==K*(1+gamma)
        parameters.append({'K':K,'gamma':str(gamma),'beta':str(beta),
                           'sink_bound':str(sink),'heavy_limit':int(heavy)})
    out['exact_parameter_checks']=parameters
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
