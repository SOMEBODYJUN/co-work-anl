"""Exact joint macro/home/q-receiver flow and prefix evacuation.
Audit oracles enumerate original task assignments, never network outcomes alone.
No output files are overwritten. Every numerical operation is integer or Fraction.
"""
from fractions import Fraction as F
from itertools import product, combinations
from collections import deque
import json
import argparse
import hashlib
import platform
import shlex
import sys
from pathlib import Path


def rational(value):
    if type(value) not in (int, F, str):
        raise TypeError('Exact int/Fraction/string only; booleans and floats are rejected')
    return F(value)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def maxflow(cap, source, target):
    flow = {}
    nbr = {}
    for u, v in cap:
        nbr.setdefault(u, set()).add(v)
        nbr.setdefault(v, set()).add(u)
        flow[u, v] = flow[v, u] = 0
    value = 0
    while True:
        pred = {source: None}
        todo = deque([source])
        while todo and target not in pred:
            u = todo.popleft()
            for v in sorted(nbr.get(u, ()), key=repr):
                if v not in pred and cap.get((u, v), 0) - flow[u, v] > 0:
                    pred[v] = u
                    todo.append(v)
        if target not in pred:
            return value, flow
        v = target
        amt = None
        while pred[v] is not None:
            u = pred[v]
            c = cap.get((u, v), 0) - flow[u, v]
            amt = c if amt is None else min(amt, c)
            v = u
        v = target
        while pred[v] is not None:
            u = pred[v]
            flow[u, v] += amt
            flow[v, u] -= amt
            v = u
        value += amt


def joint_flow(h, eligibility, macros, k, q, T):
    """Full macro coverage and group receiver choice in one integer network."""
    b=len(macros)
    source,target=('source',),('target',)
    cap={}
    for j,row in enumerate(macros):
        cap[source,('b',j)]=1
        for i,p in enumerate(row):
            if p is not None and p<=T:
                cap[('b',j),('hi',i)]=1
    for i in range(h):
        cap[('hi',i),('ho',i)]=1
        for z in eligibility[i]:
            cap[('ho',i),('z',z)]=1
    for z in range(k):
        cap[('z',z),target]=min(q,b)
    value,flow=maxflow(cap,source,target)
    return flow if value==b else None


def solve(groups, eligibility, macros, k, q, delta, T=F(1)):
    """groups[h]=list of job weights; eligibility[h]=common sink indices;
    macros[b][h]=time or None. Output actual endpoints ('h',i)/('z',i).
    Contract checked before the threshold network is used.
    """
    groups=[[rational(w) for w in G] for G in groups]
    macros=[[None if p is None else rational(p) for p in row] for row in macros]
    eligibility=[tuple(E) for E in eligibility]
    h = len(groups)
    require(type(q) is int and q >= 2, 'q must be an integer >= 2')
    require(type(k) is int and k >= 0, 'k must be a nonnegative integer')
    require(h+k >= 1, 'at least one actual machine is required')
    delta, T = rational(delta), rational(T)
    require(T >= 0 and 0 <= delta and q*delta < 2, 'need T,delta >= 0 and q*delta < 2')
    require(len(eligibility) == h, 'one common eligibility list per home')
    require(all(type(z) is int and 0 <= z < k for E in eligibility for z in E), 'invalid sink index')
    eligibility=[tuple(sorted(set(E))) for E in eligibility]
    require(all(len(row) == h for row in macros), 'macro row length must equal number of homes')
    require(all(any(p is not None for p in row) for row in macros), 'each macro needs a finite edge')
    require(all(p is None or p > T/2 for row in macros for p in row), 'finite macro times must exceed T/2')
    require(all(w >= 0 for G in groups for w in G), 'negative private processing time')
    require(all((F(1,2)+F(1,q))*T <= sum(G, F(0)) <= T for G in groups), 'group total outside promised interval')
    require(all(w <= delta*T for G in groups for w in G), 'private task exceeds delta*T')
    tau = F(q-1+q*delta, q+1)
    rho = F(2*q+q*delta, q+1)
    assert 1+tau == rho == q*(1-tau+delta)
    if T == 0:
        if macros:
            return None
        return {"assignment": [[('h', i)]*len(G) for i,G in enumerate(groups)],
                "macro_assignment": [], "loads": [F(0)]*(h+k), "rho": rho}
    flow=joint_flow(h,eligibility,macros,k,q,T)
    if flow is None:
        return None
    assigned_macros = []
    receiver = {}
    loads = [F(0)]*(h+k)
    for j, row in enumerate(macros):
        i = next(i for i in range(h) if flow.get((('b', j), ('hi', i))) == 1)
        assigned_macros.append(('h', i))
        loads[i] += row[i]
        receiver[i] = next(z for z in eligibility[i] if flow.get((('ho', i), ('z', z))) == 1)
    actual = []
    for i, G in enumerate(groups):
        retained = sum(G, F(0))
        A = []
        for w in G:
            if i in receiver and retained > tau*T:
                retained -= w
                z = receiver[i]
                loads[h+z] += w
                A.append(('z', z))
            else:
                loads[i] += w
                A.append(('h', i))
        actual.append(A)
    assert all(L <= rho*T for L in loads)
    return {"assignment": actual, "macro_assignment": assigned_macros,
            "loads": loads, "rho": rho}


def solve_promise(groups, eligibility, macros, k, q, delta):
    """Unknown-OPT promise version. Outside the promise it may raise ValueError.

    Required at OPT: W_h in [(1/2+1/q)OPT,OPT], w_j<=delta*OPT,
    and every finite macro time > OPT/2. The promise is not tested using OPT.
    Structural input conventions and rejection of floats match solve().
    """
    groups=[[rational(w) for w in G] for G in groups]
    macros=[[None if p is None else rational(p) for p in row] for row in macros]
    eligibility=[tuple(E) for E in eligibility]
    h=len(groups)
    require(type(q) is int and q>=2,'q must be an integer >= 2')
    require(type(k) is int and k>=0,'k must be a nonnegative integer')
    require(h+k>=1,'at least one actual machine is required')
    delta=rational(delta)
    require(delta>=0 and q*delta<2,'need delta>=0 and q*delta<2')
    require(len(eligibility)==h,'one common eligibility list per home')
    require(all(type(z) is int and 0<=z<k for E in eligibility for z in E),'invalid sink index')
    eligibility=[tuple(sorted(set(E))) for E in eligibility]
    require(all(len(row)==h and any(p is not None for p in row) for row in macros),'invalid macro row')
    require(all(p is None or p>=0 for row in macros for p in row),'negative macro time')
    require(all(w>=0 for G in groups for w in G),'negative private time')
    rho=F(2*q+q*delta,q+1)
    if all(w==0 for G in groups for w in G) and all(any(p==0 for p in row) for row in macros):
        return {'assignment':[[('h',i)]*len(G) for i,G in enumerate(groups)],
                'macro_assignment':[('h',next(i for i,p in enumerate(row) if p==0)) for row in macros],
                'loads':[F(0)]*(h+k),'rho':rho,'threshold':F(0)}
    require(delta>0,'nonzero input violates the delta=0 promise')
    if not macros:
        bottleneck=F(0)
    else:
        values=sorted({p for row in macros for p in row if p is not None})
        require(joint_flow(h,eligibility,macros,k,q,values[-1]) is not None,
                'no joint macro/receiver matching; unknown-OPT promise is violated')
        lo,hi=-1,len(values)-1
        while hi-lo>1:
            mid=(lo+hi)//2
            if joint_flow(h,eligibility,macros,k,q,values[mid]) is None:
                lo=mid
            else:
                hi=mid
        bottleneck=values[hi]
    target=max([F(0),bottleneck]+[sum(G,F(0)) for G in groups]
               +[w/delta for G in groups for w in G])
    result=solve(groups,eligibility,macros,k,q,delta,target)
    require(result is not None,'unknown-OPT promise violated during threshold recovery')
    result['threshold']=target
    return result


def exact_feasible(groups, eligibility, macros, k, T=F(1)):
    """Independent full actual-assignment recursion, no Hall/network oracle."""
    h = len(groups)
    jobs = []
    for row in macros:
        jobs.append([(i, p) for i, p in enumerate(row) if p is not None])
    for i,G in enumerate(groups):
        for w in G:
            jobs.append([(i,w)]+[(h+z,w) for z in eligibility[i]])
    jobs.sort(key=lambda choices: (len(choices), -max((w for _,w in choices), default=0)))
    loads = [F(0)]*(h+k)
    def rec(t):
        if t == len(jobs):
            return True
        for i,w in jobs[t]:
            if loads[i]+w <= T:
                loads[i] += w
                yes = rec(t+1)
                loads[i] -= w
                if yes:
                    return True
        return False
    return rec(0)


def full_matrix(groups, eligibility, macros, k):
    """Independent explicit original processing matrix, job major."""
    h=len(groups)
    rows=[]
    for row in macros:
        rows.append(list(row)+[None]*k)
    for i,G in enumerate(groups):
        for w in G:
            row=[None]*(h+k)
            row[i]=w
            for z in eligibility[i]:
                row[h+z]=w
            rows.append(row)
    return rows


def matrix_optimum(matrix, machine_count):
    """Full original matrix branch enumeration with exact incumbent pruning."""
    choices=[[(i,p) for i,p in enumerate(row) if p is not None] for row in matrix]
    if any(not C for C in choices):
        return None
    loads=[F(0)]*machine_count
    for C in choices:
        i,p=C[0]
        loads[i]+=p
    best=max(loads,default=F(0))
    loads=[F(0)]*machine_count
    choices.sort(key=lambda C:(len(C),-max((p for _,p in C),default=0)))
    def rec(t, current):
        nonlocal best
        if t==len(choices):
            best=min(best,current)
            return
        for i,p in choices[t]:
            nextmax=max(current,loads[i]+p)
            if nextmax>=best:
                continue
            loads[i]+=p
            rec(t+1,nextmax)
            loads[i]-=p
    rec(0,F(0))
    return best


def matrix_check(groups, eligibility, macros, k, T, result):
    """Check concrete algorithm output directly against the original matrix."""
    if result is None:
        return
    h=len(groups)
    matrix=full_matrix(groups,eligibility,macros,k)
    sigma=list(result['macro_assignment'])
    assert len(result['assignment'])==h
    for G,A in zip(groups,result['assignment']):
        assert len(G)==len(A)
        sigma.extend(A)
    assert len(sigma)==len(matrix)
    loads=[F(0)]*(h+k)
    for row,(kind,i) in zip(matrix,sigma):
        endpoint=i if kind=='h' else h+i
        assert kind in {'h','z'} and 0<=endpoint<h+k
        assert row[endpoint] is not None
        loads[endpoint]+=row[endpoint]
    assert loads==result['loads']
    if T:
        assert max(loads,default=F(0))<=result['rho']*T
    else:
        assert max(loads,default=F(0))==0


def input_and_certificate(groups, eligibility, macros, k, q, delta, T):
    result=solve(groups,eligibility,macros,k,q,delta,T)
    matrix_check(groups,eligibility,macros,k,T,result)
    matrix=full_matrix(groups,eligibility,macros,k)
    sigma=None
    if result is not None:
        endpoints=list(result['macro_assignment'])+[a for A in result['assignment'] for a in A]
        sigma=[i if kind=='h' else len(groups)+i for kind,i in endpoints]
    return {"input":{"groups":groups,"eligibility":eligibility,"macros":macros,
                     "k":k,"q":q,"delta":delta,"T":T},
            "original_matrix_job_major":matrix,"output":result,"sigma_machine_indices":sigma,
            "exact_optimum":matrix_optimum(matrix,len(groups)+k)}


def audit(export_dir=None):
    counts = {"all_instances":0,"T_feasible":0,"successful_outputs":0,"reliable_rejections":0}
    promise_checks=0
    def check_promise(groups,E,M,k,q,delta,opt):
        nonlocal promise_checks
        theta=F(1,2)+F(1,q)
        in_promise=(all(p is None or p>opt/2 for row in M for p in row)
                    and all(theta*opt<=sum(G,F(0))<=opt for G in groups)
                    and all(w<=delta*opt for G in groups for w in G))
        if in_promise:
            out=solve_promise(groups,E,M,k,q,delta)
            matrix_check(groups,E,M,k,opt,out)
            assert out['threshold']<=opt
            promise_checks+=1
    # Exhaust all eligibility and macro support graphs through 3 homes, 2 sinks,
    # 2 macros; all private groups have two half-jobs, macro times 3/4.
    q,delta = 2,F(1,2)
    for h in range(1,4):
        for k in range(0,3):
            subsets = [tuple(z for z in range(k) if mask>>z&1) for mask in range(1<<k)]
            supports = [tuple(F(3,4) if mask>>i&1 else None for i in range(h)) for mask in range(1,1<<h)]
            for Es in product(subsets,repeat=h):
                groups = [[F(1,2),F(1,2)] for _ in range(h)]
                for b in range(min(2,h)+1):
                    for Ms in product(supports, repeat=b):
                        counts['all_instances'] += 1
                        optimum = matrix_optimum(full_matrix(groups,Es,Ms,k),h+k)
                        feasible = optimum <= 1
                        assert feasible == exact_feasible(groups, Es, Ms, k)
                        result = solve(groups, Es, Ms, k, q, delta)
                        matrix_check(groups,Es,Ms,k,F(1),result)
                        check_promise(groups,Es,Ms,k,q,delta,optimum)
                        counts['T_feasible'] += feasible
                        counts['successful_outputs'] += result is not None
                        assert not feasible or result is not None
                        if result is None:
                            counts['reliable_rejections'] += 1
                            assert not feasible
    # q=3, nonuniform near-full groups and zero jobs; arbitrary eligibility.
    extra = 0
    for h in range(1,4):
        groups = [[F(0),F(1,3),F(1,3),F(1,6)] for _ in range(h)]
        for masks in product(range(4), repeat=h):
            Es = [tuple(z for z in range(2) if mask>>z&1) for mask in masks]
            for i in range(h):
                Ms = [tuple(F(2,3) if j==i else None for j in range(h))]
                optimum=matrix_optimum(full_matrix(groups,Es,Ms,2),h+2)
                feasible=optimum<=1
                assert feasible==exact_feasible(groups,Es,Ms,2)
                result = solve(groups,Es,Ms,2,3,F(1,3))
                matrix_check(groups,Es,Ms,2,F(1),result)
                check_promise(groups,Es,Ms,2,3,F(1,3),optimum)
                assert not feasible or result is not None
                if result is not None:
                    assert result['rho'] == F(7,4)
                extra += 1
    # Full macro time variations, including finite p>T edges that must be pruned.
    varying={"instances":0,"T_feasible":0,"outputs":0}
    for q,delta,G in [(2,F(1,2),[F(1,2),F(1,2)]),
                      (3,F(1,3),[F(1,3),F(1,3),F(1,6)])]:
        h=2
        for k in range(3):
            Eall=[tuple(z for z in range(k) if mask>>z&1) for mask in range(1<<k)]
            Mall=[row for row in product([None,F(3,5),F(1),F(5,4)],repeat=h)
                  if any(p is not None for p in row)]
            for E in product(Eall,repeat=h):
                for b in range(3):
                    for M in product(Mall,repeat=b):
                        groups=[G,G]
                        opt=matrix_optimum(full_matrix(groups,E,M,k),h+k)
                        yes=opt<=1
                        out=solve(groups,E,M,k,q,delta)
                        assert not yes or out is not None
                        matrix_check(groups,E,M,k,F(1),out)
                        check_promise(groups,E,M,k,q,delta,opt)
                        varying['instances']+=1
                        varying['T_feasible']+=yes
                        varying['outputs']+=out is not None
    # Huge rational denominators, 1 available home, q encoded far above h.
    denominator = 2**521-1
    groups = [[F(1,denominator)]*3 + [F(1,2), F(1,2)-F(3,denominator)]]
    huge_q = 2**200
    delta = F(1,2)
    # Huge q forces delta < 2/q, so use a huge-q case with zero homes instead.
    assert solve([],[],[],1,huge_q,F(1,huge_q),F(1)) is not None
    huge = solve(groups,[(0,)],[(F(3,4),)],1,2,delta)
    assert huge is not None
    matrix_check(groups,[(0,)],[(F(3,4),)],1,F(1),huge)
    assert solve([[F(0)]],[()],[],0,2,F(1,2),F(0)) is not None
    assert solve([],[],[],1,2,F(1,2),F(0)) is not None
    assert solve([],[],[],1,2,F(0),F(1)) is not None
    assert solve([[F(0)]],[()],[],0,2,F(0),F(0)) is not None
    assert solve([[F(1,2),F(1,2)]],[(0,)],[(F(2),)],1,2,F(1,2)) is None
    almost=F(2-F(1,2**100),3)
    close=solve([[F(1,2),F(1,2)]]*3,[(0,)]*3,[(F(3,4),None,None),(None,F(3,4),None),(None,None,F(3,4))],1,3,almost)
    assert close is not None and close['rho']<2
    matrix_check([[F(1,2),F(1,2)]]*3,[(0,)]*3,[(F(3,4),None,None),(None,F(3,4),None),(None,None,F(3,4))],1,F(1),close)
    # Exact-string input and explicit API rejection of invalid encodings/contracts.
    assert solve([['1/2','1/2']],[(0,)],[['3/4']],1,2,'1/2','1') is not None
    rejection_calls=[
        lambda: solve([[0.5,F(1,2)]],[(0,)],[[F(3,4)]],1,2,F(1,2)),
        lambda: solve([[True,F(1)]],[(0,)],[[F(3,4)]],1,2,F(1,2)),
        lambda: solve([],[],[],-1,2,F(1,2)),
        lambda: solve([],[],[],0,2,F(1,2)),
        lambda: solve([],[],[],1,True,F(1,2)),
        lambda: solve([[F(0)]],[()],[[None]],0,2,F(1,2),F(0)),
        lambda: solve([[F(1)]],[()],[],0,2,F(1,2),F(0)),
        lambda: solve([[F(1,2),F(1,2)]],[()],[],0,2,F(1)),
        lambda: solve_promise([[F(1)]],[()],[],0,2,F(0)),
    ]
    for call in rejection_calls:
        try:
            call()
        except (ValueError,TypeError):
            pass
        else:
            raise AssertionError('invalid API input accepted')
    # Independently enumerate every subset for a failed real-capacity matroid lift.
    E = [{0,2},{0,1},{2,3}]
    independent=[]
    for mask in range(8):
        I = {i for i in range(3) if mask>>i&1}
        ok=True
        for r in range(len(I)+1):
            for A in combinations(I,r):
                N=set().union(*(E[i] for i in A)) if A else set()
                ok &= len(A) <= F(len(N),2)
        if ok:
            independent.append(sorted(I))
    assert [0] in independent and [1,2] in independent
    assert [0,1] not in independent and [0,2] not in independent
    # Formula check over rational parameter grid, including limiting endpoint.
    formulas=0
    for q in range(2,101):
        for numerator in range(21):
            delta=F(2*numerator,20*q)
            tau=F(q-1+q*delta,q+1)
            rho=F(2*q+q*delta,q+1)
            assert rho==1+tau==q*(1-tau+delta)
            assert (rho<2)==(q*delta<2)
            assert (tau<=1)==(q*delta<=2)
            assert 2-rho == F(2-q*delta,q+1)
            formulas+=1
    cases={
        "joint_reselection":input_and_certificate([[F(1,4)]*4 for _ in range(3)],
            [(),(0,),(1,)],[[F(1),F(1),None],[None,F(1),F(1)]],2,2,F(1,4),F(1)),
        "zero_target":input_and_certificate([[F(0)]],[()],[],0,2,F(0),F(0)),
        "zero_target_positive_macro":input_and_certificate([[F(0)]],[()],[[F(1)]],0,2,F(0),F(0)),
        "zero_macro":input_and_certificate([[F(1,2),F(1,2)]],[()],[],0,2,F(1,2),F(1)),
        "pruned_only_macro_edge":input_and_certificate([[F(1,2),F(1,2)]],[(0,)],[[F(2)]],1,2,F(1,2),F(1)),
        "large_denominator":input_and_certificate([[F(1,denominator)]*3+[F(1,2),F(1,2)-F(3,denominator)]],[(0,)],[[F(3,4)]],1,2,F(1,2),F(1)),
        "huge_q_empty_jobs":input_and_certificate([],[],[],1,huge_q,F(1,huge_q),F(1)),
        "near_factor_two":input_and_certificate([[F(1,2),F(1,2)]]*3,[(0,)]*3,
            [[F(3,4),None,None],[None,F(3,4),None],[None,None,F(3,4)]],1,3,almost,F(1)),
    }
    assert cases['joint_reselection']['exact_optimum']==1
    assert cases['joint_reselection']['output']['loads']==[F(1),F(3,2),F(3,2),F(1,2),F(1,2)]
    promise_G=[[F(1,4)]*4 for _ in range(3)]
    promise_E=[(),(0,),(1,)]
    promise_M=[[F(11,10),F(11,10),None],[None,F(11,10),F(11,10)]]
    promise_opt=matrix_optimum(full_matrix(promise_G,promise_E,promise_M,2),5)
    assert promise_opt==F(11,10)
    check_promise(promise_G,promise_E,promise_M,2,3,F(1,4),promise_opt)
    promise_out=solve_promise(promise_G,promise_E,promise_M,2,3,F(1,4))
    assert promise_out['threshold']==F(11,10)
    cases['unknown_opt_bottleneck']={
        'input':{'groups':promise_G,'eligibility':promise_E,'macros':promise_M,
                 'k':2,'q':3,'delta':F(1,4)},
        'original_matrix_job_major':full_matrix(promise_G,promise_E,promise_M,2),
        'exact_optimum':promise_opt,'output':promise_out,
        'sigma_machine_indices':[i if kind=='h' else 3+i for kind,i in
            list(promise_out['macro_assignment'])+[a for A in promise_out['assignment'] for a in A]]}
    promise_zero=solve_promise([[F(0)]],[()],[],0,2,F(0))
    assert promise_zero['threshold']==0 and promise_zero['loads']==[F(0)]
    exported=[]
    if export_dir is not None:
        directory=Path(export_dir)
        directory.mkdir(parents=True,exist_ok=False)
        for name,case in cases.items():
            path=directory/(name+'.json')
            with path.open('x') as handle:
                json.dump(case,handle,default=str,indent=2)
                handle.write('\n')
            exported.append(str(path.resolve()))
    code=Path(__file__).resolve()
    command=[sys.executable,str(code)]
    if export_dir is not None:
        command+=['--export-dir',str(Path(export_dir).resolve())]
    return {**counts,"nonuniform_zero_job_cases":extra,"varying_macro_times":varying,
            "unknown_opt_promise_cases":promise_checks,"promise_zero_optimum_fixture":True,
            "formula_cases":formulas,"nonmatroid_independent_sets":independent,
            "original_matrix_optimum":"all_instances, nonuniform_zero_job_cases, varying_macro_times, and all named fixtures; independent exact branch enumeration",
            "metadata":{"python":sys.version,"python_version":platform.python_version(),
                        "source_path":str(code),"source_sha256":hashlib.sha256(code.read_bytes()).hexdigest(),
                        "command":shlex.join(command),"precision":"exact Python Fraction/integer; no float",
                        "seed":None,"fixtures":list(cases),"invalid_input_rejections":len(rejection_calls),
                        "range":{"base":"h=1..3,k=0..2,b=0..min(2,h),all macro support/common group eligibility graphs,q=2,delta=1/2,W=1,two half jobs,macro=3/4",
                                 "nonuniform":"h=1..3,k=2,b=1 all forced-home macros and all group eligibility graphs,q=3,delta=1/3,group=(0,1/3,1/3,1/6),macro=2/3",
                                 "varying":"h=2,k=0..2,b=0..2,all eligibility graphs; all macro rows over [None,3/5,1,5/4] except all-None row; q2 half groups and q3 (1/3,1/3,1/6) groups",
                                 "unknown_opt":"Every instance in the three finite domains whose independently enumerated original OPT satisfies the full promise; plus zero OPT and actual bottleneck 11/10 fixtures",
                                 "formulas":"q=2..100,delta=2*a/(20*q),a=0..20; includes qdelta=2 only for algebraic endpoint checks"},
                        "unverified":"No exhaustive unbounded-input test; finite tests do not replace the stated-scope proof; no general UM structure extraction or uniform epsilon for unbounded q"},
            "exported_files":exported,"arithmetic":"Python Fraction/integer; no float", "status":"PASS"}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export-dir',help='new directory for actual input matrices and sigma certificates; refuses overwrite')
    args=parser.parse_args()
    print(json.dumps(audit(args.export_dir),indent=2))
