#!/usr/bin/env python3
"""单共享汇点构造的独立向下预算动态规划与实际分配枚举审计。

The independent constructor was reconstructed before reading the candidate.
It rounds every private sink time down with one global delta=eta*T/N,
keeps exact home loads, and combines local minimum integer budgets using
an integer min-cost residual-flow matcher.  It does not call the candidate's
covering FPTAS, Hungarian matcher, normalization, or enumeration oracle.

Pre-review obligations: zero T; no private jobs; forbidden/forced endpoints;
positive times rounded to zero; macros >T; dummy/empty-home contributions;
nonreused DP items; exact-rational bit complexity; one global error budget.

The actual-assignment oracle below is exponential and is used only in this
finite audit.  Default stdout is a new JSON report; frozen results are never
changed by this script.  All valid test data use exact Fractions.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import random

import shared_sink_joint_assignment as candidate

CANDIDATE_SHA256_AT_IMPORT=sha256(Path(candidate.__file__).read_bytes()).hexdigest()


def _integer_matching(rows, home_count):
    """Min-cost injection of row vertices into homes; integer residual flow."""
    row_count=len(rows)
    if row_count>home_count:
        return None
    source=row_count+home_count
    sink=source+1
    graph=[[] for _ in range(sink+1)]
    def edge(a,b,cost):
        forward=[b,len(graph[b]),1,cost]
        reverse=[a,len(graph[a]),0,-cost]
        graph[a].append(forward)
        graph[b].append(reverse)
        return forward
    indexed=[]
    for j in range(row_count):
        edge(source,j,0)
        indexed.append([None if cost is None else edge(j,row_count+h,cost)
                        for h,cost in enumerate(rows[j])])
    for h in range(home_count):
        edge(row_count+h,sink,0)
    for _ in range(row_count):
        distance=[None]*len(graph)
        previous=[None]*len(graph)
        distance[source]=0
        for _ in range(len(graph)-1):
            changed=False
            for a,edges in enumerate(graph):
                if distance[a] is None:
                    continue
                for k,e in enumerate(edges):
                    b,_,capacity,cost=e
                    if capacity and (distance[b] is None or distance[a]+cost<distance[b]):
                        distance[b]=distance[a]+cost
                        previous[b]=(a,k)
                        changed=True
            if not changed:
                break
        if distance[sink] is None:
            return None
        at=sink
        while at!=source:
            a,k=previous[at]
            e=graph[a][k]
            e[2]-=1
            graph[at][e[1]][2]+=1
            at=a
    answer=[]
    for options in indexed:
        used=[h for h,e in enumerate(options) if e is not None and e[2]==0]
        assert len(used)==1
        answer.append(used[0])
    return answer


def solve_floor_budget(home_count, macros, tinies, target, eta):
    """Independent polynomial constructor on already validated exact inputs.

    A dictionary DP stores, at each exact rounded sink budget, the smallest
    true home load and an immutable subset witness.  All sink times,
    including forced-sink tasks, use the same global rounding quantum.
    """
    T,eta=F(target),F(eta)
    N=len(tinies)
    if T==0:
        if macros:
            return None
        assignment=[]
        for h,a,c in tinies:
            if a==0:
                assignment.append(h)
            elif c==0:
                assignment.append(home_count)
            else:
                return None
        return assignment
    if len(macros)>home_count:
        return None
    if N==0:
        rows=[[0 if t is not None and t<=T else None for t in row] for row in macros]
        return _integer_matching(rows,home_count)
    delta=eta*T/N
    Q=int(T//delta)
    grouped=[[] for _ in range(home_count)]
    for label,(h,a,c) in enumerate(tinies):
        grouped[h].append((label,a,c))
    tables=[]
    for group in grouped:
        dp={0:(F(0),0)}
        for local,(_,a,c) in enumerate(group):
            new={}
            for q,(load,mask) in dp.items():
                options=[]
                if a is not None:
                    options.append((q,load+a,mask))
                if c is not None:
                    nq=q+int(c//delta)
                    if nq<=Q:
                        options.append((nq,load,mask|(1<<local)))
                for nq,nload,nmask in options:
                    if nq not in new or nload<new[nq][0]:
                        new[nq]=(nload,nmask)
            dp=new
        tables.append(dp)
    def option(h,cap):
        return min(((q,load,mask) for q,(load,mask) in tables[h].items() if load<=cap),default=None)
    baseline=[option(h,T) for h in range(home_count)]
    if any(item is None for item in baseline):
        return None
    base_cost=sum(item[0] for item in baseline)
    if base_cost>Q:
        return None
    witnesses=[]
    increments=[]
    for row in macros:
        options=[option(h,T-t) if t is not None and t<=T else None for h,t in enumerate(row)]
        witnesses.append(options)
        costs=[None if item is None else item[0]-baseline[h][0] for h,item in enumerate(options)]
        assert all(c is None or c>=0 for c in costs)
        increments.append(costs)
    matched=_integer_matching(increments,home_count)
    if matched is None:
        return None
    if base_cost+sum(increments[j][h] for j,h in enumerate(matched))>Q:
        return None
    selected=baseline[:]
    for j,h in enumerate(matched):
        selected[h]=witnesses[j][h]
    assignment=matched+[h for h,_,_ in tinies]
    for h,(group,record) in enumerate(zip(grouped,selected)):
        for local,(label,_,_) in enumerate(group):
            if record[2]>>local&1:
                assignment[len(macros)+label]=home_count
    return assignment


def loads_of(home_count,macros,tinies,assignment):
    """Check actual eligibility/job identity and compute exact actual loads."""
    assert len(assignment)==len(macros)+len(tinies)
    loads=[F(0)]*(home_count+1)
    for j,row in enumerate(macros):
        h=assignment[j]
        assert isinstance(h,int) and 0<=h<home_count and row[h] is not None
        loads[h]+=row[h]
    for j,(h,a,c) in enumerate(tinies,len(macros)):
        machine=assignment[j]
        assert machine in (h,home_count)
        p=a if machine==h else c
        assert p is not None
        loads[machine]+=p
    return loads


def exact_actual_oracle(home_count,macros,tinies,T):
    """Full original assignments, independent of both constructors."""
    choices=[[h for h,t in enumerate(row) if t is not None] for row in macros]
    choices += [[machine for machine,time in ((h,a),(home_count,c)) if time is not None]
                for h,a,c in tinies]
    optimum=None
    home_feasible_sink=None
    checked=0
    for assignment in product(*choices):
        checked+=1
        loads=loads_of(home_count,macros,tinies,assignment)
        makespan=max(loads,default=F(0))
        optimum=makespan if optimum is None else min(optimum,makespan)
        if all(x<=T for x in loads[:home_count]):
            home_feasible_sink=loads[-1] if home_feasible_sink is None else min(home_feasible_sink,loads[-1])
    return optimum,home_feasible_sink,checked


def run_audit(seed=0x51A9):
    rng=random.Random(seed)
    stats={"cases":0,"actual_assignments":0,"promised":0,
           "candidate_success":0,"independent_success":0,
           "candidate_success_without_T_feasibility":0,"independent_success_without_T_feasibility":0}
    def check(homes,macros,tinies,T,eta):
        optimum,best_sink,count=exact_actual_oracle(homes,macros,tinies,T)
        stats["cases"]+=1
        stats["actual_assignments"]+=count
        promised=optimum<=T
        stats["promised"]+=promised
        independent=solve_floor_budget(homes,macros,tinies,T,eta)
        tested=candidate.solve_shared_sink(homes,macros,tinies,T,eta)
        outputs=(("candidate",None if tested["status"]=="REJECT_TARGET" else tested["assignment"]),
                 ("independent",independent))
        for name,assignment in outputs:
            if assignment is None:
                assert not promised,("missed promised case",name,homes,macros,tinies,T,eta,optimum)
                continue
            stats[name+"_success"]+=1
            if not promised:
                stats[name+"_success_without_T_feasibility"]+=1
            loads=loads_of(homes,macros,tinies,assignment)
            assert all(x<=T for x in loads[:homes]),("home overload",name,loads)
            assert loads[-1]<=(1+eta)*T,("sink overload",name,loads,T,eta)
            if name=="candidate":
                assert loads==tested["loads"]
                assert best_sink is not None and loads[-1]<=(1+eta)*best_sink
                if optimum==0:
                    assert max(loads,default=F(0))==0
        return tested["status"], independent is not None
    values=[None,F(0),F(1,8),F(1,2),F(1),F(3,2)]
    private_types=[(a,b) for a,b in product(values,repeat=2) if a is not None or b is not None]
    macro_types=[row for row in product([None,F(3,4),F(1),F(3,2)],repeat=2) if any(t is not None for t in row)]
    for pairs in product(private_types,repeat=2):
        tinies=[(0,*pairs[0]),(1,*pairs[1])]
        for macros in [[],*[[row] for row in macro_types]]:
            for eta in [F(1),F(1,3)]:
                check(2,macros,tinies,F(1),eta)
    exhaustive_cases=stats["cases"]
    for _ in range(2000):
        homes=rng.randrange(1,5)
        T=rng.choice([F(0),F(1,3),F(1),F(7,4)])
        eta=rng.choice([F(1),F(1,2),F(1,7)])
        tinies=[]
        times=[None,F(0),F(1,11),F(1,2),F(1),F(2),F(7)]
        for h in range(homes):
            for _ in range(rng.randrange(3)):
                a=b=None
                while a is None and b is None:
                    a,b=rng.choice(times),rng.choice(times)
                tinies.append((h,a,b))
        macros=[]
        for _ in range(rng.randrange(homes+2)):
            row=[rng.choice([None,T+F(1,100),T+F(1),T*F(3,4)]) for _ in range(homes)]
            row=[x if x is None or x>T/2 else F(1) for x in row]
            if all(x is None for x in row):
                row[0]=T+F(1)
            macros.append(row)
        check(homes,macros,tinies,T,eta)
    huge=2**4096+1
    boundary=[
        ("no_home_empty",0,[],[],F(0),F(1)),
        ("no_private_with_feasible_macro",2,[[F(3,4),F(7,6)]],[],F(1),F(1,3)),
        ("no_private_infeasible_macros",1,[[F(3,4)],[F(3,4)]],[],F(1),F(1,3)),
        ("zero_global_optimum_positive_target",2,[],[(0,F(0),F(9)),(1,F(8),F(0))],F(1),F(1,3)),
        ("positive_sink_rounds_to_zero",1,[[F(1)]],[(0,F(9),F(1,1000))],F(1),F(1)),
        ("huge_denominators",2,[[F(huge+1,2*huge),F(1)]],[(0,F(huge-1,2*huge),F(1,huge)),(1,None,F(1,huge))],F(1),F(1,7)),
        ("empty_home_baseline_cost",2,[[F(1),F(1)]],[(0,F(3,2),F(1)),(1,F(1,2),F(1,10))],F(1),F(1,10)),
    ]
    boundary_results=[]
    for name,homes,macros,tinies,T,eta in boundary:
        status,independent=check(homes,macros,tinies,T,eta)
        boundary_results.append({"name":name,"candidate":status,"independent_success":independent})
    invalid_calls = [
        lambda: candidate.solve_shared_sink(True,[],[],F(1),F(1,3)),
        lambda: candidate.solve_shared_sink(1,[],[(False,F(0),F(0))],F(1),F(1,3)),
        lambda: candidate.solve_shared_sink(1,[],[],1.0,F(1,3)),
        lambda: candidate.solve_shared_sink(1,[],[],True,F(1,3)),
        lambda: candidate.solve_shared_sink(1,[],[],F(1),0.5),
        lambda: candidate.solve_shared_sink(1,[],[],F(1),True),
        lambda: candidate.solve_shared_sink(1,[[1.0]],[],F(1),F(1,3)),
        lambda: candidate.solve_shared_sink(1,[[True]],[],F(1),F(1,3)),
        lambda: candidate.solve_shared_sink(1,[],[(0,1.0,F(0))],F(1),F(1,3)),
        lambda: candidate.solve_shared_sink(1,[],[(0,F(0),True)],F(1),F(1,3)),
        lambda: candidate.covering_fptas([(F(1),F(1),0)],0.5,F(1,3)),
        lambda: candidate.covering_fptas([(F(1),F(1),0)],True,F(1,3)),
        lambda: candidate.minimum_assignment([[0.5]]),
        lambda: candidate.minimum_assignment([[True]]),
    ]
    for call in invalid_calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("float/bool API contract accepted")
    source=Path(candidate.__file__)
    assert sha256(source.read_bytes()).hexdigest()==CANDIDATE_SHA256_AT_IMPORT,"candidate changed during audit; rerun required"
    proof=Path(__file__).resolve().parents[3]/"research/current/unrelated_machines/shared_sink_joint_macro_assignment.md"
    return {"status":"passed","seed":seed,"python":platform.python_version(),
            "arithmetic":"exact Fraction loads and integer floor budgets; independent residual-flow matching",
            "candidate_sha256":CANDIDATE_SHA256_AT_IMPORT,
            "proof_sha256":sha256(proof.read_bytes()).hexdigest(),
            "independent_source_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
            "systematic_cases":exhaustive_cases,"random_cases":2000,"independent_invalid_contract_cases":len(invalid_calls),
            **stats,"boundary_cases":boundary_results,
            "limitations":"Finite tests do not prove the theorem or novelty. The independent constructor has an additive sink budget and need not return zero for an actual zero optimum when T>0; that stronger promise is tested only for the candidate."}


if __name__=="__main__":
    print(json.dumps(run_audit(),ensure_ascii=False,indent=2))
