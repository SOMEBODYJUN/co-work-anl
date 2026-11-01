"""One independent Fraction reconstruction of the captured 29x32 small cone; no LP."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import hashlib
import time

ROOT = Path("/workspace/scratch/c0ab78c47566")
WORK = ROOT / "round21-terminal-envelope-work"
RUN = WORK / "original-small-event"
OUTPUT = WORK / "exact-small-cone.json"


def enc(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): enc(v) for k,v in x.items()}
    if isinstance(x, (tuple, list)):
        return [enc(v) for v in x]
    return x


def main():
    assert not OUTPUT.exists()
    started = time.perf_counter()
    seed = json.loads((RUN/"portfolio_matching_failure.json").read_text())
    cert = json.loads((RUN/"complete-policy.json").read_text())
    call = json.loads((RUN/"linprog-capture.json").read_text())[0]
    m,p = seed["players"],len(seed["topics"])
    assert (m,p) == (2,5)
    actions = {tuple(x["history"]): x["action"] for x in cert["actions"]}
    histories = [h for d in range(m) for h in product(range(p),repeat=d)]
    assert set(actions) == set(histories) and len(histories) == 6
    def terminal(h):
        h = tuple(h)
        while len(h)<m:
            h += (actions[h],)
        return h
    actual = terminal(())
    assert actual == (2,1)
    masks = tuple(range(1,1<<p))
    def likes(mask,a):
        return bool(mask & (1<<a))
    def atom_pay(mask,z,position):
        return F(1,sum(likes(mask,a) for a in z)) if likes(mask,z[position]) else F()
    def cover(mask,z):
        return F(int(any(likes(mask,a) for a in z)))
    wf = [cover(s,actual) for s in masks]
    rows,labels = [],[]
    for h in histories:
        own = terminal(h)
        for b in range(p):
            if b != actions[h]:
                dev = terminal(h+(b,))
                rows.append([atom_pay(s,dev,len(h))-atom_pay(s,own,len(h)) for s in masks]+[F()])
                labels.append({"kind":"ordered_IC","history":h,"chosen":actions[h],"alternative":b,
                               "actual_terminal":own,"deviated_terminal":dev})
    for h in combinations_with_replacement(range(p),m-1):
        r = []
        for s in masks:
            load = sum(likes(s,a) for a in h)
            br = F(int(likes(s,actions[h])),load+1)
            tax = F(load,load+1)
            r.append(2*cover(s,actual)-m*br-tax)
        rows.append(r+[F(1)])
        labels.append({"kind":"envelope","background":h,"selected_last":actions[h]})
    assert len(rows) == 29 and len(rows[0]) == 32
    args,res = call["arguments"],call["result"]
    compared = 0
    def exact_match(a,b):
        nonlocal compared
        if isinstance(b,list):
            assert len(a) == len(b)
            for x,y in zip(a,b):exact_match(x,y)
        else:
            assert F(str(a)) == b,(a,b)
            compared += 1
    objective = [F()]*31+[F(-1)]
    exact_match(args["A_ub"], rows)
    exact_match(args["b_ub"], [F()]*29)
    exact_match(args["A_eq"], [wf+[F()]])
    exact_match(args["b_eq"], [F(1)])
    exact_match(args["c"], objective)
    assert args["bounds"] == [[0,None]]*31+[[None,None]]
    assert args["method"] == "highs"
    assert all(args[k] is None for k in ["callback","options","x0","integrality"])
    assert res["success"] and res["status"] == 0
    x = [F(str(v)).limit_denominator(10**6) for v in res["x"]]
    lam = [F(str(v)).limit_denominator(10**6) for v in res["ineqlin"]["marginals"]]
    nu = F(str(res["eqlin"]["marginals"][0])).limit_denominator(10**6)
    assert all(a>=0 for a in x[:-1])
    assert sum(a*b for a,b in zip(wf,x)) == 1
    slacks = [-sum(a*b for a,b in zip(row,x)) for row in rows]
    assert min(slacks)>=0 and x[-1] == -F(1,2)
    assert all(v<=0 for v in lam)
    reduced = [objective[j]-sum(lam[i]*rows[i][j] for i in range(29))-nu*(wf+[F()])[j] for j in range(32)]
    assert all(v>=0 for v in reduced[:-1]) and reduced[-1] == 0
    primal = sum(a*b for a,b in zip(objective,x))
    assert primal == nu == F(1,2)
    assert all(lam[i]*slacks[i] == 0 for i in range(29))
    assert all(reduced[j]*x[j] == 0 for j in range(31))
    assert [(i,v) for i,v in enumerate(lam) if v] == [(25,-F(2,3)),(26,-F(1,3))]
    assert [(s,v) for s,v in zip(masks,x) if v] == [(14,F(1))]
    seed_clients = [sum(1<<a for a in t["topics"]) for t in seed["customers"] for _ in range(t["multiplicity"])]
    assert len(seed_clients) == 86
    checks=[]
    for name,clients in [("original_86_client_seed",seed_clients),("optimized_single_mask14_client",[14])]:
        ic=[]
        for h in histories:
            own = terminal(h)
            for b in range(p):
                if b == actions[h]:continue
                dev=terminal(h+(b,))
                u=sum((atom_pay(s,own,len(h)) for s in clients),F())
                v=sum((atom_pay(s,dev,len(h)) for s in clients),F())
                assert u>=v
                ic.append({"history":h,"alternative":b,"prescribed_payoff":u,"deviation_payoff":v,"slack":u-v})
        checks.append({"name":name,"unit_clients":len(clients),"IC_comparisons":ic,
                       "actual_payoffs":[sum((atom_pay(s,actual,i) for s in clients),F()) for i in range(m)],
                       "actual_W":sum(cover(s,actual) for s in clients)})
    backgrounds=[]
    for h in combinations_with_replacement(range(p),m-1):
        vals=[sum((F(int(likes(14,a)),1+sum(likes(14,b) for b in h)) for _ in range(1)),F()) for a in range(p)]
        tax=F(sum(likes(14,b) for b in h),1+sum(likes(14,b) for b in h))
        assert vals[actions[h]] == max(vals)
        backgrounds.append({"background":h,"all_query_values":vals,"tax":tax,"BR":max(vals),"E":m*max(vals)+tax})
    assert min(z["E"] for z in backgrounds) == F(3,2)
    # Exact coefficient identity for the two nonzero captured envelope dual rows.
    residual_by_mask=[]
    for j,s in enumerate(masks):
        e1=2*wf[j]-rows[25][j]
        e2=2*wf[j]-rows[26][j]
        residual=F(3,2)*wf[j]-F(2,3)*e1-F(1,3)*e2
        assert residual == F(int(likes(s,1) and not likes(s,2)),2)
        residual_by_mask.append(residual)
    out={"status":"PASS","scope":"one fixed m2/p5 policy cone; not the other 18 historical cones",
         "original_module_imports":0,"canonical_solver_calls":0,"LP_calls":0,"independent_exact_runs":1,
         "policy":cert,"actual_path":actual,"ordered_IC_rows":24,"envelope_rows":5,"columns":32,
         "matrix":rows,"row_labels":labels,"normalization":wf+[F()],"objective":objective,
         "captured_float_coefficients_matched_exactly":compared,
         "rational_reconstruction_denominator_limit":10**6,
         "primal":x,"inequality_dual":lam,"normalization_dual":nu,
         "primal_slacks":slacks,"dual_reduced_costs":reduced,
         "exact_min_objective":primal,"exact_max_epsilon":x[-1],
         "dual_support":[{"row":i,"multiplier":v,"row_identity":labels[i]} for i,v in enumerate(lam) if v],
         "pointwise_envelope_identity_residuals":residual_by_mask,
         "raw_client_policy_audits":checks,"optimized_point_backgrounds":backgrounds,
         "optimized_point_Estar":F(3,2),"optimized_point_W":1,
         "all_remaining_historical_cones_exactly_certified":False,
         "elapsed_seconds":time.perf_counter()-started,
         "inputs_sha256":{name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in
             ["portfolio_matching_failure.json","complete-policy.json","linprog-capture.json"]}}
    OUTPUT.write_text(json.dumps(enc(out),ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":"PASS","matrix":[29,32],"exact_coefficients":compared,
                      "primal_dual_epsilon":str(x[-1]),"raw_policy_comparisons":48,"LP_calls":0}))


if __name__ == "__main__":
    main()
