"""Bounded documentary inputs/certificates and frozen-data arithmetic only.
No original-program imports or original main execution; no network or Git.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, floor, ceil
import hashlib
import json

HERE = Path(__file__).resolve().parent
STAGE = HERE.parents[4]
def read(p):
    return json.loads((HERE/p).read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj):
    q=HERE/p
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
def enc(v):
    if isinstance(v,F):
        return str(v)
    if isinstance(v,(tuple,list)):
        return [enc(x) for x in v]
    if isinstance(v,dict):
        return {str(k):enc(x) for k,x in v.items()}
    return v
def load(P,s):
    assert len(P)==len(s)
    out=[F(0)]*len(P[0]) if P else [F(0)]
    for row,i in zip(P,s):
        assert row[i] is not None
        out[i]+=row[i]
    return out

def documentary_row_inputs():
    old=read("comparison/evidence/runs/unrelated_machines/marginal_row_independent.json")
    docs=[]
    for rec in old["cases"]:
        r,k=rec["r"],rec["k"]
        P=[[F(1)]*r+[None]*r]
        for i in range(r):
            for t in range(k):
                row=[None]*(2*r);row[i]=row[r+i]=F(1,k);P.append(row)
        schedules=[[h]+[r+i if i==h else i for i in range(r) for _ in range(k)] for h in range(r)]
        x=[[sum(s[j]==i for s in schedules)*F(1,r) for i in range(2*r)] for j in range(1+r*k)]
        assert all(max(load(P,s))==1 for s in schedules)
        ell=[sum((row[i]*xj[i] for row,xj in zip(P,x) if xj[i]),F(0)) for i in range(2*r)]
        assert ell==[F(1)]*r+[F(1,r)]*r
        assert rec["legal_assignments"]==r*2**(r*k)
        for z in rec["row_results"]:
            q=min(k,floor(F(z["a"])*k/r+F(z["b"])))
            assert z["q"]==q and F(z["best"])==2-F(q,k)
        for z in rec["count_results"]:
            q=min(k,ceil(F(k,r))+z["b0"])
            assert z["q"]==q and F(z["best"])==2-F(q,k)
        docs.append(enc({"r":r,"k":k,"P_job_major":P,"optimal_sigma_list":schedules,
                         "optimal_weights":[F(1,r)]*r,"x_job_major":x}))
    assert sum(d["legal_assignments"] for d in old["cases"])==281090
    for z in old["formula_checks"]:
        k,r=z["k"],z["r"]
        q=min(k,floor(F(z["a"])*k/r+F(z["b"])))
        assert r==k*k and z["q"]==q and F(z["ratio"])==2-F(q,k)
    save("inputs/row-five-full-matrices-and-optimal-hull-points.json",
         {"identity":"new documentary expansion of literal original inputs; not historical stdout", "cases":docs})
    return {"five_full_matrices":5,"old_legal_assignment_total":281090,"new_full_281090_enumeration":False}

def pair_distribution():
    old=read("comparison/evidence/runs/unrelated_machines/marginal_pairwise_independent.json")
    specs=[]
    for z in old["cases"]:
        r,k,q=z["r"],z["k"],z["q"]
        p=F(comb(k,2),r*comb(q,2))
        collision=r*comb(k,q)*comb(r-1,k-q)*k**(k-q)
        single=comb(r,k)*k**k*k if p<1 else 0
        assert z["support_outcomes_counted"]==collision+single
        expect=2-F(1,k)-p*F(q-1,k)
        assert F(z["expected_C"])==expect and F(z["success_probability"])==p
        assert F(z["expected_lower_bound"])==2-F(1,k)-F(k-1,2*r)
        assert z["expected_bound_attained"]==(q==2)
        specs.append(enc({"r":r,"k":k,"q":q,"collision_mass":p,"collision_atoms":collision,
                          "singleton_atoms":single,"collision_weight":p/collision,
                          "singleton_weight":(1-p)/single if single else F(0)}))
    # Expand just the small named (r,k,q)=(4,2,2) certificate, not all six old runs.
    r,k=4,2;atoms=[]
    for h in range(r):
        atoms.append({"weight":F(1,16),"h":h,"sink_tasks":{h:{0,1}}})
    for groups in combinations(range(r),k):
        for ts in product(range(k),repeat=k):
            for h in groups:
                atoms.append({"weight":F(1,64),"h":h,"sink_tasks":{i:{t} for i,t in zip(groups,ts)}})
    assert len(atoms)==52
    docs=read("inputs/row-five-full-matrices-and-optimal-hull-points.json")["cases"]
    case=next(d for d in docs if (d["r"],d["k"])==(4,2))
    P=[[None if x is None else F(x) for x in row] for row in case["P_job_major"]]
    marg=[[F(0)]*8 for _ in P];joint=[F(0)]*4;expect=success=total=F(0);out=[]
    for a in atoms:
        w,h,groups=a["weight"],a["h"],a["sink_tasks"]
        s=[h]+[r+i if t in groups.get(i,set()) else i for i in range(r) for t in range(k)]
        loads=load(P,s);c=max(loads);total+=w;expect+=w*c
        if c<=F(5,4):success+=w
        for j,i in enumerate(s):marg[j][i]+=w
        for i in range(r):
            if s[1+2*i]==s[2+2*i]==r+i:joint[i]+=w
        out.append(enc({"weight":w,"sigma":s,"loads":loads}))
    assert total==1 and expect==F(11,8) and success==F(1,4)
    assert marg==[[F(v) for v in row] for row in case["x_job_major"]]
    assert joint==[F(1,16)]*4
    save("inputs/pair-six-exact-mode-specifications.json",specs)
    save("inputs/pair-k2-r4-documentary-52-atoms.json",
         {"identity":"new explicit certificate expansion, not falsely relabeled historical program output",
          "P_job_major":enc(P),"atoms":out,"expected_C":str(expect),"success_C_le_5over4":str(success)})
    return {"old_distribution_support_occurrences":sum(z["support_outcomes_counted"] for z in old["cases"]),
            "new_explicit_atoms_verified":52,"new_original_job_checks":52*len(P)}

def nested():
    P=[[F(2,3),F(2,3),F(1)],[F(2,3),F(2,3),F(1)],[None,F(2,3),F(1)]]
    sigma=[1,0,2];assert max(load(P,sigma))==1
    best=min(max(load(P,s)) for s in product(range(3),range(3),(1,2)))
    assert best==1
    records=[{"v":0,"children":[0,1],"representative":3,"argmin_by_machine":{"1":0,"2":0}},
             {"v":1,"children":[2,3],"representative":4,"argmin_by_machine":{"2":2}}]
    save("inputs/minimal-star-forced-nested-full-matrix.json",
         enc({"identity":"literal original forced fixture plus new hand-derived two-step records and lifted sigma",
              "T":F(1),"P_job_major":P,"records":records,"residual_sigma":{"4":2},
              "lifted_original_sigma":sigma,"lifted_original_loads":load(P,sigma),"exact_optimum":best}))
    old=read("comparison/evidence/runs/unrelated_machines/minimal_star_capacity_audit.json")
    z=old["reports"]["independent_star_reproduced.json"]
    assert [z[k] for k in ["legal_fixtures","contractions","rejected_fixtures","residual_schedules_lifted",
                           "nested_residual_fixtures","nested_schedules_lifted"]]==[1095,92,369,7486,7,8]
    return {"new_forced_fixture_assignments_checked":18,"forced_nested_steps":2,
            "historical_independent_fixtures":1095,"historical_lifts":7486}

def subdivision_inputs():
    vals=[F(0),F(1,3),F(1),F(5,3)]
    rows=[{"machines":3,"jobs":[[(0,a),(1,b)],[(1,c),(2,d)]]}
          for a,b,c,d in product(vals,repeat=4)]
    rows += [{"machines":2,"jobs":[[(0,F(0)),(1,F(7))]]},
             {"machines":2,"jobs":[[(0,F(1,97)),(1,F(13,101))]]},
             {"machines":3,"jobs":[[(0,F(1))],[(1,F(1,3)),(2,F(4,3))]]},
             {"machines":1,"jobs":[]}]
    assert len(rows)==260
    save("inputs/subdivision-all-260-literal-inputs.json",
         enc({"identity":"literal input documentary expansion only; no new 260-case optimality run",
              "H":F(1),"cases":rows,"OPT_below_H_counterexample":
              {"old_jobs":[[(0,F(0)),(1,F(7))]],"new_jobs":[[(0,F(0)),(2,F(1))],[(1,F(7)),(2,F(1))]],
               "old_sigma":[0],"old_OPT":F(0),"new_sigma":[0,2],"new_OPT":F(1)}}))
    reports=read("comparison/evidence/runs/unrelated_machines/bundle_subdivision_audit.json")
    z=reports["reports"]["independent_final.json"]
    assert z["subdivision_instances_exhaustively_solved"]==260
    assert z["equality_instances_H_le_OPT_le_2H"]==113 and z["pair_coupling_cases"]==5
    for rec in z["local_moment_cut"]:
        k=rec["k"]
        assert F(rec["integer_threshold"])==2-F(1,k)
        assert F(rec["old_T"])==1+F(1,k)
        assert F(rec["old_aggregate_residual"])==F(k-2,2)
        assert rec["breakpoints_and_interiors_checked"]==4*k-2
    return {"documented_original_subdivision_inputs":260,"old_equality_cases":113,
            "old_local_moment_parameter_points":9,"new_original_main_runs":0}

def dilution():
    d=read("comparison/evidence/runs/unrelated_machines/independent_dilution_audit.json")
    for z in d["results"]:
        k,h=z["k"],z["h"];a=F(1,k-1);hh=1
        while a<F(1,2):a*=F(k,k-1);hh+=1
        assert hh==h
        I=2*sum(k**t for t in range(h));G=2*k**(h-1);N=k*(k-1)
        assert z["machines"]==I+G*N and z["jobs"]==1+k*I+(N-1)*G
        assert z["all_edges"]==2+2*k*I+N*(N-1)*G==z["all_star_edges_checked"]
        rootcols=2*k if k==2 else k+1 if a==F(1,2) else 1+2*k
        assert z["config_columns"]==(I-2)*(k+1)+2*rootcols+G*(N*(N-1)+k)
        assert F(z["independently_constructed_integer_value"])==2-F(1,k)
    f=[1,3,6,10]
    assert d["generic_star_safety_2machine_3job"]==[15**3,4**3*sum(comb(3,j)*f[j]*f[3-j] for j in range(4))]
    assert d["results"][2]["actual_probe_vectors_checked"]==58
    return {"frozen_expanded_points":3,"star_edges":[14,74,4562],"actual_probe_vectors":[14,74,58],
            "generic_matrices":3375,"generic_feasible_schedule_occurrences":8192}

def versions():
    out={}
    paths=[
      ("comparison/research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md",
       "## 7.","be27a3e92dc1da3050cedb911798fb35b78a370afc011fbe5dde519f7cf31837"),
      ("comparison/research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md",
       "## 10.","f666b407757a58a856f0b76def86707da54ba4868430f9af5ccbaeb5aa2cdf21")]
    for p,marker,want in paths:
        head=(HERE/p).read_text().split(marker)[0].rstrip()
        matches=[n for n in range(1,6) if hashlib.sha256((head+"\n"*n).encode()).hexdigest()==want]
        assert len(matches)==1,(p,matches)
        out[p]={"old_sha256_recovered":want,"trailing_newlines":matches[0],"boundary":marker}
    old=HERE/"comparison/history/source/notes/unrelated_machines/bundle_subdivision_pre_cross_reference.md"
    cur=(HERE/"comparison/research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md").read_text()
    assert old.read_text().rstrip()==cur.split("共同更强边界现已入库：")[0].rstrip()
    out["bundle"]={"frozen_pre_cross_reference_sha256":sha(old),"only_current_suffix":"共同更强边界现已入库"}
    save("version-relations.json",out)
    return out

def main():
    inv=read("primary-inventory.json")+read("comparison-inventory.json")
    for d in inv:
        p=STAGE/d["preserved_repo_path"]
        assert p.stat().st_size==d["size"] and sha(p)==d["sha256"]
    by={d["path"]:d["sha256"] for d in inv}
    d=read("comparison/evidence/runs/unrelated_machines/independent_dilution_audit.json")
    assert d["audit_code_sha256"]==by["tests/audits/unrelated_machines/independent_dilution_audit.py"]
    assert d["submitted_code_sha256"]==by["tests/audits/unrelated_machines/diluted_sink_probe_gap.py"]
    for report,code in [("minimal_star_capacity_audit.json","independent_minimal_star.py"),
                        ("bundle_subdivision_audit.json","independent_pair_coupling.py")]:
        raw=read("comparison/evidence/runs/unrelated_machines/"+report)
        assert raw["sha256"]["tests/audits/unrelated_machines/"+code]==by["tests/audits/unrelated_machines/"+code]
    review=(HERE/"comparison/research/reviews/unrelated_machines/optimal_hull_marginal_review.md").read_text()
    for p in ["tests/audits/unrelated_machines/independent_marginal_row_oracle.py",
              "tests/audits/unrelated_machines/independent_marginal_pairwise_oracle.py",
              "evidence/runs/unrelated_machines/marginal_row_independent.json",
              "evidence/runs/unrelated_machines/marginal_pairwise_independent.json"]:
        assert p in review and by[p] in review
    result={"status":"passed","new_original_main_runs":0,"inventory_files":len(inv),
            "row":documentary_row_inputs(),"pairwise":pair_distribution(),"minimal_star":nested(),
            "subdivision":subdivision_inputs(),"dilution":dilution(),"versions":versions()}
    save("data-selfcheck.json",result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
