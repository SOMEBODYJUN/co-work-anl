"""One exact definition audit of TWO stored single-customer endpoints only.
No original imports, sampling, LP, canonical solver, or equilibrium enumeration.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import datetime,hashlib,json,time
BASE=Path("/workspace/scratch/c0ab78c47566")
OUT=BASE/"r20-uniform-stored-points-audit"
OUT.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[
("r20-uniform-5-3.json","df97ae17488f04f0bbd552fd10ce473a6db0ba1bdb6e03308feb6c7721c4dba2"),
("r20-uniform-6-4.json","d6d61c660fa78f7220415854c9355efc54d69bb575d2bad6e5b7bfbc3bbc4786")]
program=BASE/"r20-uniform-interface-attack.py"
assert sha(program)=="65ed83e4f6366412d8506623e71b4b14061240eebcf7bbf4e24c51e6b4ed6d89"
before={name:sha(BASE/name) for name,_ in sources}
before[program.name]=sha(program)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
results=[];ledgers=[]
for name,digest in sources:
    path=BASE/name;assert sha(path)==digest
    data=json.loads(path.read_text());p=data["topics"];m=data["players"];best=data["best"]
    assert set(data)=={"scope","topics","players","best","completed_trials"}
    assert set(best)=={"trial","objective","m_minus_one","path","portfolio","weights","strategy"}
    w=[F(x) for x in best["weights"]]
    assert len(w)==2**p-1 and all(x>=0 for x in w)
    support=[(i+1,x) for i,x in enumerate(w) if x]
    assert len(support)==1 and support[0][1]==1
    mask=support[0][0];active=[a for a in range(p) if mask>>a&1]
    rows=best["strategy"];actions={tuple(row["history"]):row["action"] for row in rows}
    assert all(set(row)=={"history","action"} for row in rows)
    assert len(actions)==len(rows)
    required={h for d in range(m) for h in product(range(p),repeat=d)}
    assert set(actions)==required and all(a in range(p) for a in actions.values())
    assert all(a in active for a in actions.values())
    def finish(h):
        h=tuple(h)
        while len(h)<m:h+=actions[h],
        return h
    def payoff(h,a):
        z=finish(h)
        if a not in active:return F()
        return F(1,sum(b in active for b in z))
    actual=finish(())
    assert tuple(best["path"])==actual and all(a in active for a in actual)
    W=F(int(any(a in active for a in actual)))
    assert W==1
    # With one unit customer, coverage is at most 1; selecting any active topic attains it.
    OPT=F(1)
    node_rows=[];strict=ties=self_comparisons=0
    for h in sorted(required):
        a=actions[h];u=payoff(h+(a,),a);values=[]
        for b in range(p):
            dev=payoff(h+(b,),b);gap=u-dev
            assert gap>=0
            values.append(str(dev))
            strict+=gap>0;ties+=gap==0;self_comparisons+=b==a
        formula=F(1,sum(b in active for b in h)+m-len(h))
        assert u==formula
        assert all(F(v)==(formula if b in active else F()) for b,v in enumerate(values))
        node_rows.append({"history":list(h),"action":a,"actual_profit":str(u),"all_action_profits":values})
    J=best["portfolio"]
    assert len(J)==m and len(set(J))==m and all(a in range(p) for a in J)
    assert len(set(J)&set(active))==1
    V=[]
    for i in range(m):
        h=actual[:i]
        V.append([payoff(h+(a,),a) for a in J])
    total=sum((x for row in V for x in row),F())
    C=F(int(any(a in active for a in J)))
    objective=m*C-total
    assert total==1 and C==1 and objective==m-1==best["m_minus_one"]
    result={"source":name,"source_sha256":digest,"topics":p,"players":m,
        "weights_entries":len(w),"positive_customer_mask":mask,"unit_customers":1,
        "active_labels":active,"empty_labels":[a for a in range(p) if a not in active],
        "strategy_nodes":len(required),"full_ordered_history_domain":True,
        "all_prescribed_actions_cover_the_customer":True,"actual_path":list(actual),
        "root_profits":[str(F(1,m))]*m,"W":str(W),"OPT":str(OPT),
        "OPT_justification":"one unit customer gives global upper bound 1; an active topic attains it",
        "portfolio":J,"portfolio_coverage":str(C),"V_matrix":[[str(x) for x in row] for row in V],
        "sum_V":str(total),"exact_interface_objective":str(objective),
        "exact_interface_slack":str((m-1)*W+total-m*C),
        "stored_float_objective":best["objective"],"stored_trial":best["trial"],
        "declared_completed_trials":data["completed_trials"],
        "all_action_comparisons":len(required)*p,"strict_to_empty_labels":strict,
        "ties_including_self":ties,"self_comparisons":self_comparisons,
        "proper_deviations":len(required)*(p-1),
        "proper_ties":ties-self_comparisons,
        "scope":"This stored point is a complete-history pure SPE and exact interface equality. No upper certificate for its cone or earlier search is inferred."}
    results.append(result);ledgers.append({"source":name,"nodes":node_rows})
elapsed=time.perf_counter()-t
after={name:sha(BASE/name) for name,_ in sources};after[program.name]=sha(program)
assert before==after
report={"status":"pass","method":"Independent direct unit-customer fractions plus analytic single-customer OPT bound",
"cases":results,"total_history_nodes":sum(x["strategy_nodes"] for x in results),
"total_all_action_comparisons":sum(x["all_action_comparisons"] for x in results),
"original_main_calls":0,"original_helper_calls":0,"LP_calls":0,"SPE_solver_calls":0,
"new_random_searches":0,"independent_stored_point_audit_events":1}
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
(OUT/"case-ledger.json").write_text(json.dumps(ledgers,ensure_ascii=False,indent=2)+"\n")
event={"started_utc":started,"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"wall_seconds":elapsed,"audit_script_sha256":sha(Path(__file__)),
"inputs_sha256_before":before,"inputs_sha256_after":after,
"status":"pass","original_main_calls":0,"original_helper_calls":0,"LP_calls":0,
"SPE_solver_calls":0,"new_random_searches":0,"independent_stored_point_audit_events":1,
"outputs":{n:{"bytes":(OUT/n).stat().st_size,"sha256":sha(OUT/n)} for n in ["report.json","case-ledger.json"]}}
(OUT/"execution.json").write_text(json.dumps(event,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":"pass","wall_seconds":elapsed,"history_nodes":report["total_history_nodes"],
"all_action_comparisons":report["total_all_action_comparisons"],
"objectives":[x["exact_interface_objective"] for x in results],"original_main_or_LP":0}))
