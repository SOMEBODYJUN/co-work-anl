"""Exact scratch audit: forced-load/cardinality bundle closure for R||Cmax.

No LP or knapsack oracle is used.  Every bound and threshold uses Fraction.
This is a sound infeasibility filter, not a scheduling approximation algorithm.
"""

from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib
import json
import platform
from pathlib import Path
from math import prod


def closure(m, jobs, T, trace=False):
    """jobs[j] maps allowed machines to nonnegative Fraction processing times.

    At each synchronous round, D[j] is the surviving domain.  F_i sums the
    loads of singleton-domain jobs.  For the candidate j -> i and v != i,
    B consists of other jobs with domain {i,v}; v has residual capacity
    R_v=T-F_v.  For every q=0,...,|B|, K={h in B:p_vh>R_v/(q+1)}.
    At most q jobs in K can go to v, so i must receive at least the sum of
    the |K|-q smallest p_ih values.  The maximum over q is r_iv.  Delete
    j -> i if p_ij+F_i(excluding j)+sum_v r_iv>T.  A negative R_v means
    forced overload.  Empty domains mean infeasibility.
    """
    T = F(T)
    if not jobs:
        return True, [], []
    active = sorted({i for job in jobs for i in job})
    D = [{i for i, p in job.items() if p <= T} for job in jobs]
    rounds = []
    if any(not d for d in D):
        return False, D, rounds
    while True:
        forced = {i:F(0) for i in active}
        pairs = defaultdict(list)
        for h, d in enumerate(D):
            if len(d) == 1:
                i = next(iter(d))
                forced[i] += jobs[h][i]
            elif len(d) == 2:
                a, b = sorted(d)
                pairs[a, b].append(h)
        if any(a > T for a in forced.values()):
            rounds.append({'forced_overload': [i for i,a in forced.items() if a>T]})
            return False, D, rounds
        deletions = []
        for j, d in enumerate(D):
            for i in sorted(d):
                lower = jobs[j][i] + forced[i]
                if d == {i}:
                    lower -= jobs[j][i]
                witness = []
                for v in active:
                    if v == i:
                        continue
                    B = [h for h in pairs[min(i,v),max(i,v)] if h != j]
                    if not B:
                        continue
                    cap = T - forced[v]
                    best, best_q, best_K = F(0), None, None
                    for q in range(len(B)+1):
                        K = [h for h in B if jobs[h][v] > cap/(q+1)]
                        sizes = sorted((jobs[h][i] for h in K), reverse=True)
                        reserve = sum(sizes[q:], F(0))
                        if reserve > best:
                            best, best_q, best_K = reserve, q, K
                    lower += best
                    if best and trace:
                        witness.append({'other':v,'q':best_q,'K':best_K,'reserve':str(best)})
                if lower > T:
                    item = {'job':j,'machine':i,'lower':str(lower)}
                    if trace:
                        item['reserves'] = witness
                    deletions.append(item)
        if not deletions:
            return True, D, rounds
        rounds.append({'deletions':deletions})
        for item in deletions:
            D[item['job']].remove(item['machine'])
        if any(not d for d in D):
            return False, D, rounds


def schedules(m, jobs):
    for assignment in product(*(sorted(job) for job in jobs)):
        load = [F(0) for _ in range(m)]
        for j,i in enumerate(assignment):
            load[i] += jobs[j][i]
        yield assignment, max(load, default=F(0))


def lower_bound(m, jobs):
    """Integer target bisection after exact common-denominator scaling."""
    if not jobs:
        return F(0)
    den=prod(p.denominator for job in jobs for p in job.values())
    scaled=[{i:F(int(p*den)) for i,p in job.items()} for job in jobs]
    upper=sum(min(job.values()) for job in scaled)
    low,high=-1,int(upper)
    while high-low>1:
        middle=(low+high)//2
        accepted,_,_=closure(m,scaled,F(middle))
        if accepted:
            high=middle
        else:
            low=middle
    return F(high,den)


def boundary_audit():
    cases=[
        ('empty_binary_m',2**100,[],F(0)),
        ('zero',2,[{0:F(0),1:F(0)},{0:F(0),1:F(5)}],F(0)),
        ('single_eligible',2,[{0:F(2,7)},{0:F(3,11)},{1:F(1,10**30+3)}],F(43,77)),
        ('large_denominator',1,[{0:F(1,10**50+151)},{0:F(3,10**47+53)}],F(1,10**50+151)+F(3,10**47+53)),
    ]
    rows=[]
    for name,m,jobs,opt in cases:
        result=lower_bound(m,jobs)
        assert result==opt,(name,result,opt)
        assert closure(m,jobs,opt)[0]
        rows.append({'name':name,'lower_bound':str(result),'known_opt':str(opt)})
    return rows


def vw(k, subdivide=False):
    """The canonical two-tree instance, optionally subdividing every job.

    Each original job (u:a,v:b) becomes two jobs
    (u:a,w:1) and (w:1,v:b), with a private new machine w.
    """
    alpha, h = F(1,k-1), 1
    while alpha < F(1,2):
        alpha *= F(k,k-1)
        h += 1
    jobs = []
    machines = []
    def machine(name):
        machines.append(name)
        return len(machines)-1
    def tree(name):
        root=machine(name+'-root')
        frontier=[root]
        for level in range(h-1):
            following=[]
            for u in frontier:
                for branch in range(k):
                    v=machine(f'{name}-{level}-{u}-{branch}')
                    following.append(v)
                    jobs.append({u:F(1,k),v:F(1)})
            frontier=following
        for u in frontier:
            v=machine(f'{name}-terminal-{u}')
            for branch in range(k):
                jobs.append({u:F(1,k),v:F(1)})
        return root
    a,b=tree('left'),tree('right')
    jobs.append({a:F(1),b:F(1)})
    if subdivide:
        replaced=[]
        for e,job in enumerate(jobs):
            u,v=sorted(job)
            w=machine(f'subdiv-{e}')
            replaced.append({u:job[u],w:F(1)})
            replaced.append({w:F(1),v:job[v]})
        jobs=replaced
    return len(machines),jobs,h


def exhaustive_audit():
    values=[F(0),F(1),F(2),None]
    targets=[F(0),F(1,2),F(1),F(3,2),F(2),F(5,2),F(3)]
    counts={'matrices':0,'matrix_targets':0,'feasible_schedules_checked':0,
            'accepted_infeasible':0,'deletions':0,'monotonic_target_checks':0}
    for m,max_n in [(1,3),(2,3),(3,2)]:
        types=[]
        for col in product(values,repeat=m):
            if any(p is not None for p in col):
                types.append({i:p for i,p in enumerate(col) if p is not None})
        for n in range(max_n+1):
            for jobs in product(types,repeat=n):
                counts['matrices']+=1
                sch=list(schedules(m,jobs))
                previous_accepted=False
                for T in targets:
                    counts['matrix_targets']+=1
                    ok,D,rounds=closure(m,jobs,T)
                    feasible=[a for a,c in sch if c<=T]
                    counts['feasible_schedules_checked']+=len(feasible)
                    counts['deletions']+=sum(len(r.get('deletions',[])) for r in rounds)
                    if feasible:
                        assert ok,(m,jobs,T,rounds)
                        for a in feasible:
                            assert all(i in D[j] for j,i in enumerate(a)),(jobs,T,a,D)
                    elif ok:
                        counts['accepted_infeasible']+=1
                    if previous_accepted:
                        assert ok,('acceptance_not_monotone',m,jobs,T)
                    previous_accepted=ok
                    counts['monotonic_target_checks']+=1
    return counts


def family_audit():
    rows=[]
    for k in [2,3,4]:
        exact_opt=F(2)-F(1,k)
        config=F(1)+F(1,k)
        low=exact_opt-F(1,10*k)
        for subdivide in [False,True]:
            m,jobs,h=vw(k,subdivide)
            for T in sorted(set([F(1),config,low,exact_opt])):
                accepted,D,rounds=closure(m,jobs,T,trace=True)
                if subdivide and T>=1:
                    assert accepted and not rounds
                if not subdivide:
                    assert accepted == (T>=exact_opt),(k,T,accepted,rounds)
                row={'k':k,'subdivided':subdivide,'m':m,'n':len(jobs),'h':h,
                     'target':str(T),'known_opt':str(exact_opt),'accepted':accepted,
                     'rounds':len(rounds),'deletions':sum(len(r.get('deletions',[])) for r in rounds)}
                if k in [2,3]:
                    # Independent enumeration is finite evidence only; k=4 is huge.
                    oracle=min(c for _,c in schedules(m,jobs))
                    assert oracle==exact_opt,(k,subdivide,oracle)
                    row['independent_opt']=str(oracle)
                rows.append(row)
            bound=lower_bound(m,jobs)
            assert bound==(F(1) if subdivide else exact_opt)
            rows[-1]['binary_search_lower_bound']=str(bound)
    return rows


if __name__=='__main__':
    report={
        'purpose':'soundness/finite target-monotonicity/cardinality closure vs VW and subdivided VW',
        'arithmetic':'fractions.Fraction; exact; no floating arithmetic; no randomness',
        'python':platform.python_version(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exhaustive':exhaustive_audit(),
        'boundaries':boundary_audit(),
        'two_tree_family':family_audit(),
        'limitations':'finite tests are not the general soundness/complexity proofs; filter is not an approximation algorithm; k=4 OPT uses the explicit mathematical family proof rather than exhaustive enumeration'
    }
    print(json.dumps(report,indent=2,ensure_ascii=False))
