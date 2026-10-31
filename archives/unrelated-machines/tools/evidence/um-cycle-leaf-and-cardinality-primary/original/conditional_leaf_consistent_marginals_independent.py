"""Independent v3 MC transport and full-matching-mixture audit."""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json


def audit(resources,core,lam,z,epsilon,tag):
    groups=list(core)
    assert groups
    for c,states in core.items():
        assert sum(lam[c,s] for s in states)==1
        for s,row in states.items():
            assert sum(row.values())==1
            assert all(p>=0 for p in row.values()) and lam[c,s]>=0
            assert all(0<=z.get((c,s,u),F(0))<=lam[c,s] for u,p in row.items() if p>0)
            assert sum(p*z.get((c,s,u),F(0)) for u,p in row.items())>=epsilon*lam[c,s]
    blocks={}
    all_ports=[]
    leaves=[]
    y0={}
    q={}
    yc={}
    beta_one_cases=0
    for u in resources:
        neighbors=[c for c in groups if any(row.get(u,F(0))>0 for row in core[c].values())]
        d=len(neighbors)
        ports=[f"{u}:port:{i}" for i in range(d)]
        ell=[f"{u}:leaf:{i}" for i in range(d-1)]
        leaves+=ell
        all_ports+=ports or [f"{u}:unused"]
        beta=[sum(z.get((c,s,u),F(0)) for s in core[c]) for c in neighbors]
        assert sum(beta)<=1
        pi=list(beta)
        if d: pi[-1]+=1-sum(beta)
        blocks[u]={"neighbors":neighbors,"ports":ports,"leaves":ell,"beta":beta,"pi":pi}
        for i,e in enumerate(ell):
            y0[e,ports[i]]=sum(pi[i+1:])
            y0[e,ports[i+1]]=sum(pi[:i+1])
        if not d: continue
        for c,states in core.items():
            own=neighbors.index(c) if c in neighbors else None
            b=beta[own] if own is not None else F(0)
            for s in states:
                zz=z.get((c,s,u),F(0))
                assert own is not None or zz==0
                if b==1:
                    beta_one_cases+=1
                    assert own is not None and pi[own]==1 and zz==lam[c,s]
                    qq=[lam[c,s] if j==own else F(0) for j in range(d)]
                else:
                    residual=lam[c,s]-zz
                    qq=[
                        (zz if j==own else F(0))
                        +residual*(pi[j]-(b if j==own else F(0)))/(1-b)
                        for j in range(d)
                    ]
                assert all(x>=0 for x in qq) and sum(qq)==lam[c,s]
                if own is not None: assert qq[own]>=zz
                for j,value in enumerate(qq): q[c,s,u,j]=value
                for i,e in enumerate(ell):
                    yc[c,s,e,ports[i]]=sum(qq[i+1:])
                    yc[c,s,e,ports[i+1]]=sum(qq[:i+1])
            for j in range(d):
                assert sum(q[c,s,u,j] for s in states)==pi[j]
    for e in leaves:
        assert sum(y0.get((e,p),F(0)) for p in all_ports)==1
    for u,block in blocks.items():
        for i,p in enumerate(block["ports"]):
            assert block["beta"][i]+sum(y0.get((e,p),F(0)) for e in leaves)<=1
    mc_rows=0
    conditional_rows=0
    conditional_columns=0
    for c,states in core.items():
        for e in leaves:
            endpoints={p for (ee,p) in y0 if ee==e}
            assert len(endpoints)==2
            for p in endpoints:
                mc_rows+=1
                assert sum(yc.get((c,s,e,p),F(0)) for s in states)==y0[e,p]
        for s in states:
            for e in leaves:
                conditional_rows+=1
                assert sum(yc.get((c,s,e,p),F(0)) for p in all_ports)==lam[c,s]
            for u,block in blocks.items():
                for i,p in enumerate(block["ports"]):
                    conditional_columns+=1
                    zz=z.get((c,s,u),F(0)) if block["neighbors"][i]==c else F(0)
                    assert zz+sum(yc.get((c,s,e,p),F(0)) for e in leaves)<=lam[c,s]
    # Coupling local hole distributions by a common interval has only
    # polynomially many cuts; each piece is a full integral leaf matching.
    mixture={}
    for c,states in core.items():
        for s in states:
            cuts={F(0),lam[c,s]}
            for u,block in blocks.items():
                if not block["ports"]: continue
                running=F(0)
                for j in range(len(block["ports"])):
                    running+=q[c,s,u,j]
                    cuts.add(running)
                assert running==lam[c,s]
            cuts=sorted(cuts)
            pieces=[]
            reproduced=defaultdict(F)
            for left,right in zip(cuts,cuts[1:]):
                assert right>left
                mid=(left+right)/2
                matching={}
                for u,block in blocks.items():
                    if not block["ports"]: continue
                    running=F(0)
                    hole=None
                    for j in range(len(block["ports"])):
                        running+=q[c,s,u,j]
                        if mid<running:
                            hole=j;break
                    assert hole is not None
                    for i,e in enumerate(block["leaves"]):
                        matching[e]=block["ports"][i if i<hole else i+1]
                assert set(matching)==set(leaves)
                assert len(set(matching.values()))==len(leaves)
                weight=right-left
                for e,p in matching.items(): reproduced[e,p]+=weight
                pieces.append({"weight":str(weight),"matching":matching})
            assert sum((F(piece["weight"]) for piece in pieces),F(0))==lam[c,s]
            for e in leaves:
                for p in all_ports:
                    assert reproduced[e,p]==yc.get((c,s,e,p),F(0))
            assert len(pieces)<=1+sum(len(b["ports"]) for b in blocks.values())
            mixture[f"{c}|{s}"]=pieces
    output={
        "tag":tag,"epsilon":str(epsilon),"cores":len(core),
        "states":sum(map(len,core.values())),"resources":len(all_ports),"leaves":len(leaves),
        "MC_rows_checked":mc_rows,"conditional_rows_checked":conditional_rows,
        "conditional_columns_checked":conditional_columns,
        "beta_one_state_cases":beta_one_cases,
        "integral_matching_pieces":sum(map(len,mixture.values())),
        "max_pieces_per_state":max(map(len,mixture.values()),default=0),
        "hole_tables":[[c,s,u,j,str(v)] for (c,s,u,j),v in q.items()],
        "global_leaf_flow":[[e,p,str(v)] for (e,p),v in y0.items()],
        "conditional_leaf_flow":[[c,s,e,p,str(v)] for (c,s,e,p),v in yc.items()],
        "conditional_matching_mixtures":mixture,
    }
    return output


def main():
    t=2;D=t*t
    resources=[f"g{a}_{j}" for a in range(D) for j in range(D)]
    resources +=[f"A{a}_{h}" for a in range(D) for h in range(t)]
    core={"M":{str(a):{f"g{a}_{j}":F(1,D) for j in range(D)} for a in range(D)}}
    lam={("M",str(a)):F(1,D) for a in range(D)}
    for a in range(D):
        for j in range(D):
            c=f"H{a}_{j}"
            core[c]={"home":{f"g{a}_{j}":F(1)},"parking":{f"A{a}_{h}":F(1,t) for h in range(t)}}
            lam[c,"home"]=1-F(1,D);lam[c,"parking"]=F(1,D)
    z={(c,s,u):lam[c,s] for c,states in core.items() for s,row in states.items() for u,p in row.items() if p>0}
    family=audit(resources,core,lam,z,F(1),"family_t2")
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
    partial=audit(toy_resources,toy,toy_lam,toy_z,F(2,5),"partial_z_zero_lambda_d0_d1_d2")
    boundary_core={
        "A":{"home":{"u":F(1)},"alt":{"a1":F(1,2),"a2":F(1,2)}},
        "B":{"park":{"b1":F(1,2),"b2":F(1,2),"unused":F(0)},"home":{"u":F(1)}}
    }
    boundary_lam={("A","home"):F(1),("A","alt"):F(0),("B","park"):F(1),("B","home"):F(0)}
    boundary_z={(c,s,u):boundary_lam[c,s] for c,states in boundary_core.items() for s,row in states.items() for u,p in row.items() if p>0}
    boundary=audit(["u","a1","a2","b1","b2","unused"],boundary_core,boundary_lam,boundary_z,F(1),"beta_one_with_d2_and_zero_states")
    assert boundary["beta_one_state_cases"]>0
    result={"scope":"new-clause v3 independent audit; no author Proof or checker read",
            "fixtures":[family,partial,boundary]}
    Path("sol_conditional_leaf_consistent_marginals_independent_audit.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    fields={"tag","cores","states","resources","leaves","MC_rows_checked","conditional_rows_checked",
            "conditional_columns_checked","beta_one_state_cases","integral_matching_pieces","max_pieces_per_state"}
    print(json.dumps([{k:v for k,v in fixture.items() if k in fields} for fixture in result["fixtures"]]))


if __name__=="__main__": main()
