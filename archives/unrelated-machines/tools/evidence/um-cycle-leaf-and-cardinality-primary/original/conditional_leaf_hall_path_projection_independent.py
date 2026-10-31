"""Independent construction from the Exact-only v2 statement; no author imports."""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json


def lift(resources, core, lambdas, z, epsilon):
    groups=list(core)
    assert groups
    blocks={}
    lifted={g:{} for g in groups}
    lifted_z={}
    for u in resources:
        neighbors=[g for g in groups if any(row.get(u,0)>0 for row in core[g].values())]
        ports=[f"port:{u}:{i}" for i in range(len(neighbors))] or [f"unused:{u}"]
        blocks[u]={"neighbors":neighbors,"ports":ports,"leaves":[]}
    for g in groups:
        assert sum(lambdas[g,s] for s in core[g])==1
        for s,row in core[g].items():
            assert sum(row.values())==1 and all(p>=0 for p in row.values())
            lifted[g][s]={}
            for u,p in row.items():
                block=blocks[u]
                pos=block["neighbors"].index(g) if g in block["neighbors"] else 0
                port=block["ports"][pos]
                lifted[g][s][port]=p
                if p>0:
                    zz=z[g,s,u]
                    assert 0<=zz<=lambdas[g,s]
                    lifted_z[g,s,port]=zz
            assert sum(p*z.get((g,s,u),F(0)) for u,p in row.items())>=epsilon*lambdas[g,s]
    y0={}
    conditional={}
    leaf_groups=[]
    new_resources=[]
    for u,block in blocks.items():
        neighbors,ports=block["neighbors"],block["ports"]
        new_resources+=ports
        d=len(neighbors)
        beta=[
            sum(z.get((g,s,u),F(0)) for s in core[g])
            for g in neighbors
        ]
        assert sum(beta)<=1
        prefix=F(0)
        for i in range(d-1):
            ell=f"leaf:{u}:{i}"
            leaf_groups.append(ell)
            block["leaves"].append(ell)
            lifted[ell]={"left":{ports[i]:F(1)},"right":{ports[i+1]:F(1)}}
            prefix+=beta[i]
            y0[ell,ports[i]]=1-prefix
            y0[ell,ports[i+1]]=prefix
        for g in groups:
            omit=neighbors.index(g) if g in neighbors else 0
            for s in core[g]:
                for i,ell in enumerate(block["leaves"]):
                    port=ports[i] if i<omit else ports[i+1]
                    conditional[g,s,ell,port]=lambdas[g,s]
    # Every original state keeps its own coefficients and threshold type.
    for g in groups:
        oldH={u for u in resources if max(row.get(u,F(0)) for row in core[g].values())>=epsilon}
        oldb=max(sum(p for u,p in row.items() if u not in oldH) for row in core[g].values())
        newH={u for u in new_resources if max(row.get(u,F(0)) for row in lifted[g].values())>=epsilon}
        newb=max(sum(p for u,p in row.items() if u not in newH) for row in lifted[g].values())
        assert oldb==newb
    for ell in leaf_groups:
        assert sum(y0.get((ell,u),F(0)) for u in new_resources)==1
    for u in new_resources:
        assert sum(v for (g,s,uu),v in lifted_z.items() if uu==u)+sum(y0.get((ell,u),F(0)) for ell in leaf_groups)<=1
    for g in groups:
        for s in core[g]:
            lam=lambdas[g,s]
            for ell in leaf_groups:
                assert sum(conditional.get((g,s,ell,u),F(0)) for u in new_resources)==lam
            for u in new_resources:
                assert lifted_z.get((g,s,u),F(0))+sum(conditional.get((g,s,ell,u),F(0)) for ell in leaf_groups)<=lam
    return lifted,new_resources,blocks,leaf_groups,lifted_z,y0,conditional


def matrix_audit(menu,resources,chosen,bundles,target):
    jobs={}
    machines={f"res:{u}" for u in resources}
    for g,states in menu.items():
        jobs[f"selector:{g}"]={f"root:{g}:{s}":F(1) for s in states}
        for s,row in states.items():
            root=f"root:{g}:{s}"
            machines.add(root)
            for u,p in row.items():
                jobs[f"inc:{g}:{s}:{u}"]={root:p,f"res:{u}":F(1)}
    assignment={}
    loads={m:F(0) for m in machines}
    for g,states in menu.items():
        assignment[f"selector:{g}"]=f"root:{g}:{chosen[g]}"
        for s,row in states.items():
            for u,p in row.items():
                job=f"inc:{g}:{s}:{u}"
                assignment[job]=f"res:{u}" if s==chosen[g] and u in bundles[g] and p>0 else f"root:{g}:{s}"
    assert set(assignment)==set(jobs)
    for j,m in assignment.items():
        assert m in jobs[j]
        loads[m]+=jobs[j][m]
    assert max(loads.values())==target
    assert all(sum(row.get(u,F(0)) for u in bundles[g])>=2-target
               for g,states in menu.items() for s,row in states.items() if s==chosen[g])
    return jobs,assignment,loads


def main():
    t=2
    D=t*t
    resources=[f"g{a}_{j}" for a in range(D) for j in range(D)]
    resources +=[f"A{a}_{h}" for a in range(D) for h in range(t)]
    core={"M":{str(a):{f"g{a}_{j}":F(1,D) for j in range(D)} for a in range(D)}}
    lambdas={("M",str(a)):F(1,D) for a in range(D)}
    for a in range(D):
        for j in range(D):
            g=f"H{a}_{j}"
            core[g]={"home":{f"g{a}_{j}":F(1)},"parking":{f"A{a}_{h}":F(1,t) for h in range(t)}}
            lambdas[g,"home"]=1-F(1,D)
            lambdas[g,"parking"]=F(1,D)
    z={(g,s,u):lambdas[g,s] for g,states in core.items() for s,row in states.items() for u,p in row.items() if p>0}
    lifted,ports,blocks,leaves,lifted_z,y0,conditional=lift(resources,core,lambdas,z,F(1))
    chosen={"M":"0"}
    oldbundles={"M":{f"g0_{j}" for j in range(t)}}
    for a in range(D):
        for j in range(D):
            g=f"H{a}_{j}"
            chosen[g]="parking" if a==0 and j<t else "home"
            oldbundles[g]={f"A0_{j}"} if a==0 and j<t else {f"g{a}_{j}"}
    ownership={u:g for g,B in oldbundles.items() for u in B}
    assert len(ownership)==sum(map(len,oldbundles.values()))
    bundles={g:set() for g in core}
    for u,block in blocks.items():
        owner=ownership.get(u)
        omit=block["neighbors"].index(owner) if owner is not None else 0
        if owner is not None: bundles[owner].add(block["ports"][omit])
        for i,ell in enumerate(block["leaves"]):
            endpoint=i if i<omit else i+1
            chosen[ell]="left" if endpoint==i else "right"
            bundles[ell]={block["ports"][endpoint]}
    assert sum(map(len,bundles.values()))==len(set().union(*bundles.values()))
    jobs,sigma,loads=matrix_audit(lifted,ports,chosen,bundles,2-F(1,t))
    # All-group positive-support FSLP(1), including the added two-state leaves.
    all_lam=dict(lambdas)
    for ell in leaves:
        for s,row in lifted[ell].items():
            u=next(iter(row))
            all_lam[ell,s]=y0[ell,u]
    assert all(sum(all_lam[g,s] for s in states)==1 for g,states in lifted.items())
    assert all(sum(all_lam[g,s] for g,states in lifted.items() for s,row in states.items() if row.get(u,F(0))>0)<=1 for u in ports)
    K=1+D*D
    SC=D+2*D*D
    P0=D*D*(t+2)
    L0=D*D+D*t*(D-1)
    I=P0+2*L0
    assert (len(core),len(leaves),len(ports),sum(map(len,lifted.values())))==(K,L0,P0,SC+2*L0)
    assert sum(len(row) for states in lifted.values() for row in states.values())==I
    assert (len(loads),len(jobs),sum(map(len,jobs.values())))==(180,201,404)

    # A separate complete normalized menu with partial z, a zero-lambda
    # duplicate indexed state, d=0/d=1/d=2 blocks, and explicit zero jobs.
    toy_resources=[f"u{i}" for i in range(6)]
    toy={
        "A":{"a0":{"u1":F(1,3),"u2":F(1,3),"u4":F(1,3),"u0":F(0),"u3":F(0)},
             "a1":{"u1":F(1,3),"u2":F(1,3),"u4":F(1,3),"u0":F(0)}},
        "B":{"b0":{"u2":F(1,3),"u3":F(1,3),"u5":F(1,3),"u1":F(0)}}
    }
    toy_lam={("A","a0"):F(1),("A","a1"):F(0),("B","b0"):F(1)}
    toy_z={("A","a0","u1"):F(2,3),("A","a0","u2"):F(1,3),("A","a0","u4"):F(2,3),
           ("A","a1","u1"):F(0),("A","a1","u2"):F(0),("A","a1","u4"):F(0),
           ("B","b0","u2"):F(1,2),("B","b0","u3"):F(1,2),("B","b0","u5"):F(1,2)}
    toy_lift,toy_ports,toy_blocks,toy_leaves,tz,ty0,tyc=lift(toy_resources,toy,toy_lam,toy_z,F(2,5))
    assert len(toy_blocks["u0"]["neighbors"])==0
    assert len(toy_blocks["u1"]["neighbors"])==1
    assert len(toy_blocks["u2"]["neighbors"])==2
    assert all(v==0 for (g,s,ell,u),v in tyc.items() if s=="a1")
    assert sum(p==0 for states in toy_lift.values() for row in states.values() for p in row.values())==4
    toy_chosen={g:next(iter(states)) for g,states in toy_lift.items()}
    toy_jobs,toy_sigma,toy_loads=matrix_audit(
        toy_lift,toy_ports,toy_chosen,{g:set() for g in toy_lift},F(2))
    out={
        "scope":"independent exact audit from statement-only v2; no author-proof/checker imports",
        "family":{"t":t,"D":D,"cores":K,"leaves":L0,"resources":P0,"states":SC+2*L0,"incidences":I,
                  "machines":len(loads),"jobs":len(jobs),"finite_entries":sum(map(len,jobs.values())),"peak":str(max(loads.values()))},
        "toy":{"old_resources":len(toy_resources),"new_resources":len(toy_ports),"new_leaves":len(toy_leaves),
               "epsilon":"2/5","partial_z":True,"zero_lambda_duplicate":True,"explicit_zero_jobs":4,"d0_d1_d2":True,
               "complete_tail_schedule_machines":len(toy_loads),"complete_tail_schedule_jobs":len(toy_jobs),"complete_tail_schedule_peak":"2"},
        "matrix":{j:{m:str(p) for m,p in row.items()} for j,row in jobs.items()},
        "assignment":sigma,"all_machine_loads":{m:str(v) for m,v in loads.items()},
        "lambda":[[g,s,str(v)] for (g,s),v in lambdas.items()],
        "z":[[g,s,u,str(v)] for (g,s,u),v in lifted_z.items()],
        "global_leaf_flow":[[ell,u,str(v)] for (ell,u),v in y0.items()],
        "conditional_leaf_flows":[[g,s,ell,u,str(v)] for (g,s,ell,u),v in conditional.items()],
        "toy_matrix":{j:{m:str(p) for m,p in row.items()} for j,row in toy_jobs.items()},
        "toy_assignment":toy_sigma,"toy_all_machine_loads":{m:str(v) for m,v in toy_loads.items()},
    }
    Path("sol_conditional_leaf_hall_independent_audit.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k in {"scope","family","toy"}}))


if __name__=="__main__": main()
