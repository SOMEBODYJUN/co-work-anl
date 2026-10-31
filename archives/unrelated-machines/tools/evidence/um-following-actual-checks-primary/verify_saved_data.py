"""Independent bounded input/certificate checks. No original imports/main calls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from math import floor, ceil
import hashlib
import json

E=Path(__file__).resolve().parent
STAGE=E.parents[4]
def read(p):return json.loads((E/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    return x
def save(p,v):
    q=E/p;q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(encode(v),ensure_ascii=False,indent=2)+"\n")
def loads(P,sigma):
    m=len(P[0]) if P else 0;out=[F(0)]*m
    assert len(P)==len(sigma)
    for j,i in enumerate(sigma):
        assert P[j][i] is not None;out[i]+=P[j][i]
    return out
def rank(rows):
    rows=[list(map(F,r)) for r in rows]
    if not rows:return 0
    r=0
    for c in range(len(rows[0])):
        pivot=next((j for j in range(r,len(rows)) if rows[j][c]),None)
        if pivot is None:continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        d=rows[r][c];rows[r]=[v/d for v in rows[r]]
        for j in range(r+1,len(rows)):
            t=rows[j][c]
            if t:rows[j]=[a-t*b for a,b in zip(rows[j],rows[r])]
        r+=1
        if r==len(rows):break
    return r

def activation():
    docs=[]
    a=[F(2,5)]*6;b=[F(3,10)]*6
    source=[0,0,0,1,1,1];target=[1,1,1,0,0,0]
    P=[[a[j] if i==source[j] else b[j] for i in range(2)] for j in range(6)]
    current=source[:];prefix=[]
    for j in [0,3,1,4,2,5]:
        current[j]=target[j];prefix.append(loads(P,current));assert max(prefix[-1])<=2
    docs.append({"name":"static_cover","P_job_major":P,"sigma":source,"tau":target,
                 "T":F(1),"C":F(6,5),"U":F(2),"R":[0,3],"order":[0,3,1,4,2,5],"prefix_loads":prefix})
    P=[[F(1,2),F(5,4)],[F(1),F(3,4)],[F(1,4),None]]
    sigma=[1,0,0];tau=[0,1,0]
    assert max(loads(P,sigma))==F(5,4) and max(loads(P,tau))==F(3,4)
    assert [max(loads(P,[0,0,0])),max(loads(P,[1,1,0]))]==[F(7,4),F(2)]
    docs.append({"name":"no_first_move","P_job_major":P,"sigma":sigma,"tau":tau,"T":F(3,4),"C":F(5,4),"U":F(13,8)})
    source=[0,0,1,1,2,2];target=[1,2,0,2,0,1]
    b=[F(3,5),F(3,5),F(3,10),F(1,5),F(3,10),F(1,5)]
    P=[[F(1) if i==source[j] else b[j] if i==target[j] else None for i in range(3)] for j in range(6)]
    h=[F(1,10),F(3,10),F(3,10)]
    for mask in range(64):
        outgoing=[sum(F(1) for j in range(6) if mask>>j&1 and source[j]==i) for i in range(3)]
        incoming=[sum((b[j] for j in range(6) if mask>>j&1 and target[j]==i),F(0)) for i in range(3)]
        assert not (all(d>=v for d,v in zip(outgoing,h)) and all(p<=F(1,2) for p in incoming))
    current=source[:];prefix=[]
    for j in [2,0,3,4,1,5]:
        current[j]=target[j];prefix.append(loads(P,current))
    assert max(map(max,prefix))==F(23,10)
    docs.append({"name":"static_not_necessary","P_job_major":P,"sigma":source,"tau":target,
                 "T":F(1),"C":F(2),"U":F(5,2),"order":[2,0,3,4,1,5],"prefix_loads":prefix})
    replication=[{"k":k,"F_assignment_LP":F(3,2),"exact_integer_OPT":(3*k+1)//2,
                  "float_half_exact_on_this_range":F(3*k/2)==F(3*k,2)} for k in range(1,13)]
    assert all(d["float_half_exact_on_this_range"] for d in replication)
    save("inputs/activation-three-full-fixtures-and-replication.json",
         {"identity":"documentary expansion and independent bounded arithmetic, not additional original main",
          "fixtures":docs,"zero_time_case":{"P":[[0,0],[0,None]],"sigma":[0,0]},
          "q_zero_h_positive_original_check":"literal assertion only; no flow algorithm is executed",
          "replication_two_identical_machines_three_unit_jobs":replication})
    event=read("runs/activation-original/execution.json")
    assert event["exit_code"]==0 and event["stdout_sha256"]==sha(E/"runs/activation-original/stdout")
    assert (E/"runs/activation-original/stdout").read_text()=="multi_activation_cover_replication: PASS\n"
    return {"documented_fixtures":3,"static_subset_checks":64,"replication_parameters":12,
            "only_new_original_main_run":1}

def fanout():
    raw=read("comparison/evidence/runs/unrelated_machines/weighted_fanout_profile_boundary_audit.json")
    records=[]
    concrete=read("comparison/examples/unrelated_machines/weighted_fanout_profile_star.json")
    out=raw["root_actual_runs"]["concrete_original_matrix"]["result"]
    records.append((concrete,out))
    for q,z in zip((2,3),raw["root_actual_runs"]["normative_actual"]["examples"]):
        p=[[F(1,q)]*q]+[[F(1) if j==i else None for j in range(q)] for i in range(q)]
        records.append(({"p":p,"S1":[0]*q,"S2":list(range(1,q+1)),"T":F(1),"a":0,
                         "outputs":list(range(1,q+1)),"missing_subset":list(range(1,q+1))},z))
    checked=0
    for case,out in records:
        matrix=[[None if v is None else F(v) for v in row] for row in case["p"]]
        P=list(map(list,zip(*matrix)));T=F(case["T"]);K=out["candidate_outputs"]
        got=loads(P,out["sigma"]);checked+=len(P)
        assert got==list(map(F,out["task_loads"]))
        pre=[F(0)]*len(matrix)
        for i in [case["a"]]+[v for v in K if v!=out["chosen"]]:pre[i]=T
        assert pre==list(map(F,out["preloads"]))
        assert [a+b for a,b in zip(got,pre)]==list(map(F,out["loads"]))
        assert max(a+b for a,b in zip(got,pre))<=F(out["bound"])==(2-F(out["beta_chosen"]))*T
        for j in range(len(P)):
            expected=case["S2"][j] if case["S1"][j] in out["W"] and case["S2"][j] in out["W"] else case["S1"][j]
            assert out["sigma"][j]==expected
        for v in range(len(matrix)):
            row=sum((matrix[v][j] for j in range(len(P)) if case["S1"][j]==v),F(0))
            own=sum((matrix[v][j] for j in range(len(P)) if case["S1"][j]==v
                     and out["colors"][v]==out["colors"][case["S2"][j]]),F(0))
            assert own==F(out["row_weight_to_own_color"][v])
            assert own>=F(out["beta"][out["colors"][v]])*row
    save("inputs/fanout-three-full-input-output-pairs.json",
         {"identity":"frozen concrete input plus documentary q2/q3 inputs for original saved outputs","pairs":records})
    assert raw["process_exit_codes"]==[0,0,0]
    counts=raw["root_actual_runs"]["normative_actual"]["counts"]
    assert counts["random_weighted_actual_constructions"]==3*counts["random_exact_subset_profile_sum_checks"]==8118
    return {"full_saved_output_jobs_checked":checked,"input_output_pairs":3,
            "old_normative_constructions":8118,"new_original_runs":0}

def outer():
    old=read("comparison/evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json")
    coefficients=[[[F(3,4),F(1,4)],[F(1,4),F(3,4)]],
                  [[F(1,2),F(1,2)],[F(1),F(0)]],
                  [[F(1,3),F(2,3)],[F(2,3),F(1,3)]]]
    groups=[0,0,1];weights=[F(1,2),F(1,2),F(1)]
    rules=[[F(1,3),F(2,3)],[F(2,3),F(1,3)]]
    docs=[];total=0
    for al,rate,saved in zip((F(1,2),F(1,4)),(F(1,3),F(1,2)),old["cases"]):
        opts=[]
        for h in range(3):
            a=[]
            for state,prior in [(0,al),(1,al),(None,1-2*al)]:
                for bits in product((0,1),repeat=2):
                    p=prior
                    for bit in bits:
                        z=rate if state is not None else F(0);p*=z if bit else 1-z
                    if p:a.append((state,bits,p))
            opts.append(a)
        mean=[F(0)]*2;second=[F(0)]*2;mass=F(0);count=0;witness=None
        target=list(map(F,saved["final_values"]))
        for profile in product(*opts):
            p=profile[0][2]*profile[1][2]*profile[2][2]/4
            for orders in product(range(2),repeat=2):
                values=[F(0)]*2
                for u,r in enumerate(orders):
                    candidates=[]
                    for h,(st,bits,pr) in enumerate(profile):
                        if st is not None and bits[u] and coefficients[h][st][u]>0:
                            value=weights[h]*coefficients[h][st][u]
                            candidates.append((-rules[r][groups[h]]*value,h,st,value))
                    if candidates:
                        _,h,st,v=min(candidates);values[groups[h]]+=v
                for i,v in enumerate(values):mean[i]+=p*v;second[i]+=p*v*v
                mass+=p;count+=1
                if values==target and witness is None:
                    witness={"states":[x[0] for x in profile],"requests":[x[1] for x in profile],
                             "rules":orders,"values":values,"identity":"new value-compatible witness; not historical CE decisions"}
        assert mass==1 and count==saved["brute_outcomes"]
        assert mean==list(map(F,saved["means"])) and second==list(map(F,saved["seconds"]))
        initial=sum((v-m*m for m,v in zip(mean,second)),F(0))
        final=sum(((v-m)**2 for v,m in zip(target,mean)),F(0))
        assert initial==F(saved["initial_potential"]) and final==F(saved["final_potential"])<=initial
        assert saved["CE_steps"]==3+3*2+2==11 and witness is not None
        docs.append({"alpha":[[al,al]]*3,"coefficients":coefficients,"groups":groups,
                     "weights":weights,"multipliers":rules,"request_rate":rate,
                     "old_report":saved,"new_value_witness":witness})
        total+=count
    save("inputs/outer-two-full-random-experiments.json",
         {"identity":"literal input expansion and new direct finite probability arithmetic, no original imports",
          "cases":docs,"does_not_reexecute_historical_11_CE_choices":True})
    return {"new_direct_outcomes_checked":total,"shared_state_cases":2,
            "whole_scheduling_algorithm_or_tiny_domain_checked":False,"new_original_runs":0}

def fee():
    raw=read("comparison/evidence/runs/unrelated_machines/multiwitness_shared_job_fee_audit.json")
    totals=[0,0,0,0];docs=[];witnesses=0
    for rec in raw["cases"]:
        p=rec["p"];a=list(map(F,rec["a"]));b=list(map(F,rec["b"]));c=F(rec["c"])
        assert len(a)==len(b)==p and all(0<x<=1 for x in a+b+[c]) and c+sum(b)>=1
        jobs=[[(r,a[r]),(p+r,F(1))] for r in range(p)]
        jobs += [[(p+r,F(1)),(2*p,b[r])] for r in range(p)]
        jobs += [[(2*p,c),(2*p+1,F(1))]]
        docs.append({"name":rec["name"],"machines":2*p+2,"jobs_two_endpoints":jobs})
        fees=trade=0
        for pattern in range(1<<p):
            B=sum((b[r] for r in range(p) if pattern>>r&1),F(0))
            by=[min(F(2),max(F(1),B+c)),min(F(2),max(F(1),B))]
            betas={F(1),F(5,4),F(3,2),F(7,4),F(199,100)}
            for endpoint in {B,B+c}|set(by):
                if 1<=endpoint<2:betas.update((endpoint,(1+endpoint)/2,(2+endpoint)/2))
            fees+=len(betas)
            for beta in betas:
                inds=[r for r in range(p) if pattern>>r&1]
                if inds and B<=1 and all(c+b[r]>beta for r in inds):
                    assert len(inds)*(beta-c)<B
                    if beta>=F(3,2):assert len(inds)<=1
                    trade+=1
        assert fees==rec["closed_threshold_fee_checks"] and trade==rec["nonempty_tradeoff_checks"]
        for z in rec["small_pattern_certificates"]:
            for f,mask in enumerate(z["original_assignment_masks"]):
                out=[F(0)]*(2*p+2)
                for j,options in enumerate(jobs):
                    i,t=options[mask>>j&1];out[i]+=t;witnesses+=1
                assert max(out)==F(z["best_peak_fee"+str(f)])
                assert mask&((1<<p)-1)==z["pattern"] and mask>>(2*p)&1==f
        totals=[t+v for t,v in zip(totals,[1,1<<(2*p+1),1<<p,fees])]
    assert totals==[113,287104,3004,19832]
    assert [raw[k] for k in ["case_count","assignment_count","pattern_count","closed_threshold_fee_checks"]]==totals
    save("inputs/fee-all-113-original-sparse-matrices.json",
         {"identity":"complete actual inputs reconstructed from preserved old parameter rows; not new full assignment audit",
          "cases":docs})
    return {"old_cases_semantically_checked":113,"old_pattern_count":3004,
            "old_fee_threshold_count":19832,"saved_witness_job_checks":witnesses,
            "new_full_287104_assignment_enumeration":False}

def hs():
    old=read("comparison/evidence/runs/unrelated_machines/near_flat_hs_independent_audit.json")
    outputs=atoms=allassignments=passing=0
    for rec in old["instances"]:
        jobs=[{int(i):F(t) for i,t in j.items()} for j in rec["jobs"]];n=len(jobs)
        machines=sorted({i for j in jobs for i in j});T=F(rec["T"]);eta=F(rec["eta"])
        def actual(s):
            out={i:F(0) for i in machines}
            for j,i in enumerate(s):assert i in jobs[j];out[i]+=jobs[j][i]
            return out
        support=rec["support_atoms"];assert sum((F(x["weight"]) for x in support),F(0))==1
        assert all(F(x["weight"])>0 and max(actual(x["assignment"]).values())<=T for x in support)
        atoms+=len(support)
        feasible={tuple(a) for a in product(*(sorted(j) for j in jobs)) if max(actual(a).values())<=T}
        allassignments+=2**n
        assert {tuple(x["assignment"]) for x in support}==feasible
        if "feasible_schedules" in rec:assert rec["feasible_schedules"]==len(feasible)
        variables=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
        mon1=[()]+[(e,) for e in variables]
        mon2=mon1+[pair for pair in combinations(variables,2) if pair[0][1]!=pair[1][1]]
        features=lambda mon:[[int(all(x["assignment"][j]==i for i,j in S)) for S in mon] for x in support]
        assert rank(features(mon1))==rec["rank_M1"] and rank(features(mon2))==rec["rank_M2"]
        threshold=min(F(1,64*n*len(variables)*rec["rank_M1"]),eta/16)
        assert F(rec["threshold"])==threshold
        assert rec["certificate_passed"]==(F(rec["delta"])<=threshold)
        out=actual(rec["assignment"]);outputs+=n
        assert {str(i):str(t) for i,t in out.items()}==rec["loads"] and max(out.values())==F(rec["makespan"])
        assert F(rec["denominator_HS_squared"])==F(rec["prefix"][-1]["HS_squared"])
        if rec["certificate_passed"]:
            passing+=1;assert max(out.values())<=(1+3*F(rec["delta"]))*T<=(1+eta)*T
            assert all(F(z["loss"])<=3*F(z["delta_e"]) for z in rec["selected_losses"])
        assert all(F(z["loss"])==0 for z in rec["selected_losses"] if F(z["delta_e"])==0)
    assert passing==old["certificate_pass_cases"]==old["genuinely_nonflat_certificate_pass_cases"]==2
    assert old["total_cases"]==21 and old["ordinary_large_defect_cases"]==19
    return {"all_saved_input_atoms_checked":atoms,"new_small_input_assignments_for_support":allassignments,
            "output_job_checks":outputs,"feature_rank_pairs_checked":21,
            "trace_delta_and_PSD_not_recomputed_from_scratch":True,"new_original_runs":0}

def main():
    inv=read("primary-inventory.json")+read("comparison-inventory.json")
    for d in inv:
        p=STAGE/d["preserved_repo_path"];assert p.stat().st_size==d["size"] and sha(p)==d["sha256"]
    by={d["path"]:d["sha256"] for d in inv}
    fan=read("comparison/evidence/runs/unrelated_machines/weighted_fanout_profile_boundary_audit.json")
    assert fan["source_hashes"]["tests/audits/unrelated_machines/multi_host_weighted_fanout.py"]==by["tests/audits/unrelated_machines/multi_host_weighted_fanout.py"]
    outer_scope=read("comparison/evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_root_replay_scope.json")
    assert outer_scope["code_sha256"]==by["tests/audits/unrelated_machines/multi_outer_request_winner_pair_backend.py"]
    assert outer_scope["exit_code"]==0 and outer_scope["stdout_sha256"]==by["evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json"]
    raw=read("comparison/evidence/runs/unrelated_machines/multiwitness_shared_job_fee_audit.json")
    assert set(raw["source_sha256"].values())=={by["tests/audits/unrelated_machines/multiwitness_shared_job_fee.py"]}
    raw=read("comparison/evidence/runs/unrelated_machines/near_flat_hs_independent_audit.json")
    assert raw["source_sha256"]==by["tests/audits/unrelated_machines/near_flat_hs_independent_audit.py"]
    assert raw["helper_sha256"]==by["tests/audits/unrelated_machines/global_assignment_flat_moment_audit.py"]
    result={"status":"passed","inventory_files":len(inv),"new_original_main_runs":1,
            "only_new_original_main":"multi_activation_cover_replication.py",
            "activation":activation(),"fanout":fanout(),"outer":outer(),"fee":fee(),"HS":hs()}
    save("data-selfcheck.json",result);print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
