"""Independent finite attack of weighted group token slots and real prefixes.

Its independent kernel uses no production solver or LP backend. For each fixture it
enumerates original macro placements and uses a memoized original-job DFS to
find true T schedules. Their convex mixture supplies an exact rational token
LP witness. A separately implemented integer augmenting flow chooses homes and
slots, and all actual output assignments are checked in the original matrix.
An optional candidate's output is checked against the same independent matrix.
Finite evidence, not a replacement for the general proof.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import deque
import argparse, hashlib, importlib.util, json, math, platform, random
from pathlib import Path

CANDIDATE = None


def verify_candidate(groups,eligible,macro,zcount,T,delta,x,y,d,home_x):
    if CANDIDATE is None:return
    cg=[{'weights':g,'eligible':list(e)} for g,e in zip(groups,eligible)]
    cm=[{h:p for h,p in enumerate(row) if p is not None} for row in macro]
    cf=[{h:v for h,v in enumerate(row) if v} for row in x]
    cy=[]
    for h,row in enumerate(y):
        cy.append({z:v for z,v in enumerate(row) if v} if d[h] else {None:home_x[h]})
    out=CANDIDATE.round_certificate(cg,zcount,cm,T,delta,cf,cy)
    assert len(out['macro_assignment'])==len(macro)
    assert len(out['private_assignment'])==len(groups)
    loads=[F()]*(len(groups)+zcount)
    for b,h in enumerate(out['macro_assignment']):
        assert isinstance(h,int) and not isinstance(h,bool) and 0<=h<len(groups)
        assert macro[b][h] is not None
        loads[h]+=macro[b][h]
    for h,(g,row) in enumerate(zip(groups,out['private_assignment'])):
        assert len(g)==len(row)
        for w,(kind,i) in zip(g,row):
            assert isinstance(i,int) and not isinstance(i,bool)
            assert (kind=='h' and i==h) or (kind=='z' and i in eligible[h])
            loads[i if kind=='h' else len(groups)+i]+=w
    assert max(loads,default=F())<=(F(3,2)+delta)*T
    assert max(loads[len(groups):],default=F())<=F(3,2)*T
    assert loads[:len(groups)]==out['home_loads']
    assert loads[len(groups):]==out['sink_loads']
    assert max(loads,default=F())==out['makespan']


def true_witnesses(groups, eligible, macro, zcount, T):
    hcount = len(groups)
    values = [T] + [w for g in groups for w in g] + [p for row in macro for p in row if p is not None]
    scale = math.lcm(*(v.denominator for v in values))
    cap = int(T * scale)
    private = [(h, j, int(w * scale)) for h, g in enumerate(groups) for j, w in enumerate(g)]
    private.sort(key=lambda a: (-a[2], a[0], a[1]))
    options = [[h for h,p in enumerate(row) if p is not None and p <= T] for row in macro]
    witnesses = []
    for homes in product(*options):
        if len(set(homes)) != len(homes):
            continue
        initial = [0]*(hcount+zcount)
        for b,h in enumerate(homes): initial[h] += int(macro[b][h]*scale)
        @lru_cache(None)
        def dfs(k, loads):
            if k == len(private): return ()
            h,j,w = private[k]
            targets = (h,) + tuple(hcount+z for z in eligible[h])
            if w == 0: targets = (h,)
            for i in targets:
                if loads[i]+w <= cap:
                    nxt = list(loads); nxt[i] += w
                    tail = dfs(k+1, tuple(nxt))
                    if tail is not None: return (i,) + tail
            return None
        choices = dfs(0, tuple(initial))
        if choices is not None:
            assignment = {(h,j): i for (h,j,w),i in zip(private,choices)}
            witnesses.append((tuple(homes), assignment))
    return witnesses


def integer_flow(edges, source, sink):
    adj={source:[],sink:[]}; residual={}; original={}
    def add(u,v,c):
        adj.setdefault(u,[]); adj.setdefault(v,[])
        if (u,v) not in residual:
            adj[u].append(v); adj[v].append(u)
            residual[u,v]=0; residual[v,u]=0
        residual[u,v] += c; original[u,v]=original.get((u,v),0)+c
    for u,v,c in edges: add(u,v,c)
    total=0
    while True:
        prev={source:None}; todo=deque([source])
        while todo and sink not in prev:
            u=todo.popleft()
            for v in adj[u]:
                if residual[u,v] and v not in prev: prev[v]=u;todo.append(v)
        if sink not in prev: break
        v=sink
        while v!=source:
            u=prev[v]; residual[u,v]-=1; residual[v,u]+=1; v=u
        total+=1
    return total, {e:c-residual[e] for e,c in original.items()}


def attack_case(groups, eligible, macro, zcount, T=F(1), delta=F(1,4)):
    hcount=len(groups); W=[sum(g,F()) for g in groups]
    assert T>=0 and 0<=delta<F(1,2)
    assert all(w>=0 and w<=delta*T for g in groups for w in g)
    assert all(w<=T for w in W)
    assert all(p is None or p>T/2 for row in macro for p in row)
    witnesses=true_witnesses(groups,eligible,macro,zcount,T)
    if not witnesses: return {"true_feasible":False}
    d=[max(w-T/2,F()) for w in W]
    x=[[F() for h in groups] for b in macro]
    y=[[F() for z in range(zcount)] for h in groups]
    mixture=F(1,len(witnesses))
    for homes,assign in witnesses:
        for b,h in enumerate(homes):
            x[b][h]+=mixture
            if d[h]:
                exports=[sum((w for j,w in enumerate(groups[h]) if assign[h,j]==hcount+z),F()) for z in range(zcount)]
                e=sum(exports,F()); assert e>=d[h] and e>0
                for z in range(zcount):y[h][z]+=mixture*exports[z]/e
    home_x=[sum((row[h] for row in x),F()) for h in range(hcount)]
    assert all(sum(row,F())==1 for row in x)
    assert all(a<=1 for a in home_x)
    for h in range(hcount):
        if d[h]:assert sum(y[h],F())==home_x[h]
    for z in range(zcount):assert sum((d[h]*y[h][z] for h in range(hcount)),F())<=T
    verify_candidate(groups,eligible,macro,zcount,T,delta,x,y,d,home_x)

    s=('s',); t=('t',); edges=[]; slots={}; fractional_edges={}
    for b,row in enumerate(macro):
        edges.append((s,('b',b),1))
        for h,p in enumerate(row):
            if p is not None and p<=T:edges.append((('b',b),('hi',h),1))
    for h in range(hcount):
        edges.append((('hi',h),('ho',h),1))
        if not d[h]:edges.append((('ho',h),t,1))
    partial_last=0
    for z in range(zcount):
        k=0; used=F(); slot_loads=[]
        for h in sorted(range(hcount),key=lambda h:(-d[h],h)):
            amount=y[h][z]
            while amount:
                if used==0:
                    slot_loads.append(F())
                    edges.append((('slot',z,k),t,1))
                take=min(amount,1-used)
                fractional_edges[h,z,k]=take
                edges.append((('ho',h),('slot',z,k),1))
                slot_loads[k]+=take*d[h]
                used+=take; amount-=take
                if used==1:k+=1;used=F()
        if used:partial_last+=1
        slots[z]=slot_loads
    value,flow=integer_flow(edges,s,t)
    assert value==len(macro)
    homes=[]; receiver={}; chosen_by_z=[[] for z in range(zcount)]
    for b,row in enumerate(macro):
        chosen=[h for h in range(hcount) if flow.get((('b',b),('hi',h)),0)]
        assert len(chosen)==1;homes.append(chosen[0])
    assert len(set(homes))==len(homes)
    for h in homes:
        if d[h]:
            chosen=[(z,k) for (hh,z,k) in fractional_edges if hh==h and flow.get((('ho',h),('slot',z,k)),0)]
            assert len(chosen)==1
            z,k=chosen[0]; assert z in eligible[h]
            if k:assert d[h]<=slots[z][k-1]
            receiver[h]=z;chosen_by_z[z].append(d[h])
    for z,demands in enumerate(chosen_by_z):
        assert sum(demands,F())<=T+max(demands,default=F())
        assert sum(demands,F())<=F(3,2)*T
    loads=[F() for i in range(hcount+zcount)]
    for b,h in enumerate(homes):loads[h]+=macro[b][h]
    tau=(F(1,2)+delta)*T
    for h,g in enumerate(groups):
        leave=W[h]; exported=F(); assignments=[]
        for j,w in enumerate(g):
            if h in homes and leave>tau:
                assert h in receiver
                leave-=w;exported+=w;assignments.append(hcount+receiver[h])
            else:assignments.append(h)
        if h in homes:
            assert leave<=tau
            assert exported<=d[h]
            if exported:assert exported<d[h]
        for w,i in zip(g,assignments):
            assert i==h or i-hcount in eligible[h]
            loads[i]+=w
    assert all(v<=(F(3,2)+delta)*T for v in loads)
    assert all(v<=F(3,2)*T for v in loads[hcount:])
    return {"true_feasible":True,"witnesses":len(witnesses),"partial_last_slots":partial_last,"maxload":str(max(loads,default=F()))}


def main():
    global CANDIDATE
    parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--candidate');args=parser.parse_args()
    if args.candidate:
        spec=importlib.util.spec_from_file_location('candidate',args.candidate)
        CANDIDATE=importlib.util.module_from_spec(spec);spec.loader.exec_module(CANDIDATE)
    stats={"cases":0,"true_feasible":0,"true_infeasible":0,"source_witnesses":0,"partial_last_slots":0,"families":{}}
    def run(label,groups,eligible,macro,zcount,T=F(1),delta=F(1,4)):
        result=attack_case(groups,eligible,macro,zcount,T,delta)
        stats['cases']+=1;stats['families'][label]=stats['families'].get(label,0)+1
        stats['true_feasible' if result['true_feasible'] else 'true_infeasible']+=1
        stats['source_witnesses']+=result.get('witnesses',0)
        stats['partial_last_slots']+=result.get('partial_last_slots',0)
    # Exhaustive original matrices, two homes, one sink, all group sizes 0..4,
    # all eligibility masks and one or two macros with 3/4, 1, or unavailable.
    for bcount in (0,1,2):
        for sizes in product(range(5),repeat=2):
            groups=[[F(1,4)]*size for size in sizes]
            for masks in product((False,True),repeat=2):
                eligible=[(0,) if m else () for m in masks]
                for times in product((None,F(3,4),F(1)),repeat=2*bcount):
                    macro=[list(times[2*b:2*b+2]) for b in range(bcount)]
                    if any(all(p is None for p in row) for row in macro):continue
                    run('two_home_one_sink_exhaustive',groups,eligible,macro,1)
    rng=random.Random(572991)
    for _ in range(400):
        hcount=3;zcount=2;groups=[]
        for h in range(hcount):
            remain=F(1);g=[]
            for _ in range(rng.randrange(9)):
                w=rng.choice((F(),F(1,8),F(1,4)))
                if w<=remain:g.append(w);remain-=w
            groups.append(g)
        eligible=[tuple(z for z in range(zcount) if rng.randrange(2)) for h in range(hcount)]
        macro=[]
        for b in range(rng.randrange(4)):
            row=[rng.choice((None,F(3,4),F(1),F(5,4))) for h in range(hcount)]
            if all(p is None for p in row):row[rng.randrange(hcount)]=F(5,4)
            macro.append(row)
        run('three_home_two_sink_seed572991',groups,eligible,macro,zcount)
    # Endpoints and huge denominators, explicit zero tasks and zero demand.
    run('zero_T',[[F(),F()]], [()], [],0,T=F(),delta=F())
    run('delta_zero_macro',[[F(),F()]], [()], [[F(3,4)]],0,delta=F())
    run('no_sinks_positive_small_group',[[F(1,4)]], [()], [[F(3,4)]],0)
    run('prune_above_T',[[F()]], [()], [[F(5,4)]],0)
    run('empty_homes',[],[],[],1)
    huge=F(1,2**127-1)
    run('huge_denominator',[[huge,F(1,4)-huge,F(1,4),F(1,4),F(1,4)]],[(0,)],[[F(3,4)]],1)
    run('delta_near_half',[[F(499,1000),F(499,1000),F(1,500)]],[(0,)],[[F(1)]],1,delta=F(499,1000))
    scale=F(2**131+17,2**127-1)
    run('large_rational_scale',[[scale/4]*4],[(0,)],[[3*scale/4]],1,T=scale)
    report={"status":"passed","python":platform.python_version(),"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"arithmetic":"Fraction and integer DFS/flow","seed":572991,"coverage":stats,"candidate_sha256":hashlib.sha256(Path(args.candidate).read_bytes()).hexdigest() if args.candidate else None,"limitations":"Finite fixtures; exact LP witnesses come from mixtures of enumerated true schedules, not an LP solver. Optional candidate only provides its final assignment, checked independently in the original matrix; its internal flow/LP is not used by this audit. No unknown-OPT solver is imported or tested."}
    txt=json.dumps(report,ensure_ascii=False,indent=2)
    if args.output:Path(args.output).write_text(txt+'\n')
    print(txt)

if __name__=='__main__':main()
