#!/usr/bin/env python3
"""Exact rational counterexample to aggregate-degree4 token-label lifting."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json

ROOT=Path.cwd()
k,n=4,10
delta=F(1,100)
worlds=[frozenset(S) for S in combinations(range(n),k)]
assert len(worlds)==210


def exact_psd(matrix):
    # Author Fraction Schur-elimination, same routine used in earlier audits.
    a=[[F(x) for x in row] for row in matrix];rank=0
    for j in range(len(a)):
        if a[j][j]<0:return False,rank
        if not a[j][j]:
            if any(a[j][h] for h in range(j+1,len(a))):return False,rank
            continue
        rank+=1;pivot=a[j][j]
        for h in range(j+1,len(a)):
            for t in range(h,len(a)):
                a[h][t]-=a[h][j]*a[j][t]/pivot;a[t][h]=a[h][t]
    return True,rank


def bad_weight(S):
    a=sum(i<5 for i in S)
    if a in [0,4]:return F(1,8)
    if a==2:return -F(1,400)
    return F(0)


def moment(S):
    S=frozenset(S);hasY=n in S;T=S-{n}
    if hasY:return delta*sum((bad_weight(W) for W in worlds if T<=W),F(0))
    return F(sum(T<=W for W in worlds),len(worlds))


def falling(a,t):
    v=1
    for i in range(t):v*=a-i
    return v


def lifted_moment(requests,hasY=False):
    # Each request (a,w) means original token a goes to head w.
    req=set(requests)
    labels=[a for a,_ in req];heads=[w for _,w in req]
    if len(set(labels))<len(req) or len(set(heads))<len(req):return F(0)
    assert len(req)<=k
    args=set(heads)
    if hasY:args.add(n)
    return moment(args)/falling(k,len(req))


def main():
    assert sum((bad_weight(W) for W in worlds),F(0))==1
    basis=[frozenset()]+[frozenset([i]) for i in range(n+1)]+[frozenset(S) for S in combinations(range(n+1),2)]
    M=[[moment(S|T) for T in basis] for S in basis]
    psd,rank=exact_psd(M);assert psd
    original_singletons=[None,"Y",*[(a,w) for a in range(k) for w in range(n)],*[('home',a) for a in range(k)]]
    def original_pair(v,w):
        req=[];hasY=False
        for z in [v,w]:
            if z is None:continue
            if z=="Y":hasY=True
            elif z[0]=='home':return F(0)  # fixed active A=1,h=0
            else:req.append(z)
        return lifted_moment(req,hasY)
    original_M1=[[original_pair(v,w) for w in original_singletons] for v in original_singletons]
    labelled_M1_psd,labelled_M1_rank=exact_psd(original_M1)
    assert labelled_M1_psd
    # Full original source first/second moments are a genuine uniform matching
    # row law. The context-conditioned contrast norm is the degree4 obstruction.
    signs=[1]*5+[-1]*5
    terms=[((a,w),signs[w]*(1 if a==0 else -1)) for a in [0,1] for w in range(n)]
    negative=sum((ca*cb*lifted_moment([va,vb],True)
                  for va,ca in terms for vb,cb in terms),F(0))
    assert negative==-F(1,150)
    Mbad=[[sum((bad_weight(W) for W in worlds if i in W and j in W),F(0))
           for j in range(n)] for i in range(n)]
    D=[[210*sum((bad_weight(W)**2 for W in worlds if i in W and j in W),F(0))
        for j in range(n)] for i in range(n)]
    schur=[[Mbad[i][j]-delta*D[i][j] for j in range(n)] for i in range(n)]
    assert exact_psd(Mbad)==(True,10)
    assert exact_psd(schur)==(True,10)
    expected_M=[F(8,5),F(2),F(1,20)]
    expected_D=[F(5271,100),F(105,2),F(5313,1600)]
    assert [Mbad[0][0]+4*Mbad[0][1]+5*Mbad[0][5],
            Mbad[0][0]+4*Mbad[0][1]-5*Mbad[0][5],Mbad[0][0]-Mbad[0][1]]==expected_M
    assert [D[0][0]+4*D[0][1]+5*D[0][5],
            D[0][0]+4*D[0][1]-5*D[0][5],D[0][0]-D[0][1]]==expected_D
    # All aggregate linear equality moments through degree4 (Boolean is built
    # into the set-indexed moment function).
    multipliers=[frozenset(S) for t in range(4) for S in combinations(range(n+1),t)]
    for S in multipliers:
        assert sum((moment(S|{i}) for i in range(n)),F(0))==k*moment(S)
    # Genuine ordinary native matrix that contains this identical-token group
    # and an independent endpoint context Y, under one external fixed root.
    jobs=[{"job":"g","finite_endpoints":{"r":"1"},"sigma":"r"}]
    for a in range(4):
        jobs.append({"job":f"f:{a}","finite_endpoints":{"r":"1/8",**{f"z:{w}":"1" for w in range(10)}},"sigma":f"z:{a}"})
    jobs.append({"job":"y","finite_endpoints":{"r":"1/2","y:0":"1","y:1":"1"},"sigma":"y:0"})
    loads={m:F(0) for m in ["r",*[f"z:{w}" for w in range(10)],"y:0","y:1"]}
    for job in jobs:loads[job["sigma"]]+=F(job["finite_endpoints"][job["sigma"]])
    assert max(loads.values())==1
    out={"ClaimVersion":"SCRATCH-TOKEN-LABEL-M1-POSITIVE-M2-NO-CP-v1",
         "status":"author exact counterexample and audit; not a scheduling integrality gap or independent review",
         "aggregate_variables":[*[f"X:{i}" for i in range(n)],"Y"],
         "moment_rule":{"pure_X":"uniform 4-subsets of 10", "with_Y":"delta times signed bad 4-subset law", "delta":str(delta)},
         "signed_bad_weights":{"pure_half_subset":"1/8","two_from_each_half":"-1/400","other":"0"},
         "input_M2":{"dimension":len(M),"exact_PSD":psd,"rank":rank},
         "labelled_M1":{"dimension":len(original_M1),"exact_PSD":labelled_M1_psd,"rank":labelled_M1_rank},
         "bad_M1_eigenvalues":{"ones":str(expected_M[0]),"sign":str(expected_M[1]),"within_half":str(expected_M[2])},
         "Schur_D_eigenvalues":{"ones":str(expected_D[0]),"sign":str(expected_D[1]),"within_half":str(expected_D[2])},
         "Schur_difference_positive":True,
         "aggregate_cardinality_ideal_all_degree_le_4_checked":len(multipliers),
         "negative_original_norm":{"polynomial":"Y * sum_w sign(w) (x[0,w]-x[1,w])","square_expectation":str(negative)},
         "input_M2_monomials":[sorted(S) for S in basis],
         "input_M2_matrix":[[str(x) for x in row] for row in M],
         "ordinary_matrix_context":{"machines":13,"jobs":6,"finite_endpoints":48,
             "original_jobs":jobs,"complete_actual_peak":1,
             "scope":"input aggregate point is not a valid full-original M2 point; the ordinary instance has OPT1"}}
    actual_endpoints=sum(len(j["finite_endpoints"]) for j in jobs)
    out["ordinary_matrix_context"]["finite_endpoints"]=actual_endpoints
    path=ROOT/"sol_token_label_hypergeometric_lift_audit.json"
    encoded=json.dumps(out,indent=2)+"\n"
    if path.exists():
        # Existing bytes may be frozen; replays compare and never overwrite.
        previous=json.loads(path.read_text())
        if "labelled_M1" in previous:assert path.read_text()==encoded
        else:raise RuntimeError("older pre-freeze audit exists; choose a new version rather than overwrite it")
    else:path.write_text(encoded)
    print(json.dumps({"input_M2_dimension":len(M),"exact_PSD":psd,"rank":rank,
                      "labelled_M1_dimension":len(original_M1),"labelled_M1_rank":labelled_M1_rank,
                      "negative_lifted_norm":str(negative),"original_finite_endpoints":actual_endpoints},indent=2))


if __name__=="__main__":main()
