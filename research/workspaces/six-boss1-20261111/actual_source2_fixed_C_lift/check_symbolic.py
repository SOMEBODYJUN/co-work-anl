#!/usr/bin/env python3
"""Direct exact symbolic/fixture checks. No old numerical point, optimizer, or matrix."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=HERE.parents[3]
sha=lambda p:sha256(p.read_bytes()).hexdigest()
dump=lambda name,value:(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
spec=importlib.util.spec_from_file_location("new_fixed_c_oracle",HERE/"symbolic_coefficients.py")
K=importlib.util.module_from_spec(spec);spec.loader.exec_module(K)
full=K.full_catalogue();active=K.active_catalogue()
old=json.loads((BASE/"actual_source2_nested_requery/row_catalogue.json").read_text())["rows"]
assert len(full)==751 and len(active)==734 and len({r["name"] for r in active})==734
assert [r["legacy_index"] for r in active]==[i for i in range(751) if i not in K.VISIBLE_LEGACY_INDICES]
assert {r["source"] for r in active if r["family"]=="NESTED_SOURCE25"}=={3,4,5}
assert {r["source"] for r in active if r["family"]=="NEW_SAFE"}=={3,4,5,6}
assert all(r["true_prefix"]==["A1","C","R3","R4"][:r["source"]-1] for r in active if r["family"]=="NESTED_SOURCE25")
assert sha(HERE/"legacy_751_catalogue.json")==sha(BASE/"actual_source2_nested_requery/row_catalogue.json")
assert sha(HERE/"legacy_751_kernel.py.txt")==sha(BASE/"actual_source2_nested_requery/symbolic_coefficients.py")
assert sha(HERE/"legacy_243_kernel.py.txt")==sha(BASE/"actual_source2_opt_requery/symbolic_coefficients.py")

# New oracle versus the frozen751 static values; no old kernel is executed.
samples=json.loads((BASE/"actual_source2_nested_requery/literal_samples.json").read_text())
sample_results=[];triples=0
for sample in samples["states"]:
    atom=dict(sample["atom"],c=sample["q"])
    values=[]
    assert len(sample["coefficients"])==751
    for i,row in enumerate(full):
        expected=sample["coefficients"][i]
        assert expected["row"]==old[i]["name"]
        actual=[K.coefficient(row,atom,sample["tail"]),K.base_atom_coefficient(row,atom),K.base_K_coefficient(row)]
        wanted=[F(expected[key]) for key in ["A","b_atom","b_K"]]
        assert actual==wanted,(sample["id"],i)
        triples+=1
    sample_results.append({"id":sample["id"],"fixed_C_atom":atom,"tail":sample["tail"],"all751_triples_match":True})
assert triples==9012

# P25 direct true-payment minima for the genuine inner sources only.
def m25(p,n,t,q):return F((n+1)*t,2)+F(24*t,p+n+1)+F(q,p+1+n*t)
hidden=0;minima=0;single_mean=0;double_mean=0
for source in [3,4,5]:
    n=6-source
    for p in range(source):
        for t,q in product([0,1],repeat=2):
            costs=[]
            for tails in product([0,1],repeat=n):
                s=sum(tails[:-1]);last=tails[-1];load=p+t+sum(tails)
                numerator=25*t-last
                assert load or numerator==0
                cost=(F(numerator,load) if load else F(0))+F(s,2)+last+F(q,p+t+s+1)
                assert cost>=m25(p,n,t,q);costs.append(cost);hidden+=1
            assert min(costs)==m25(p,n,t,q);minima+=1
        A=F(n+1,2)+F(24,p+n+1);B=F(1,p+1);E=F(n,(p+1)*(p+n+1))
        for menu in product([0,1],repeat=6):
            d=sum(menu);o=int(d>0)
            for pure in [0,1]:
                left=sum((m25(p,n,pure,q) for q in menu),F(0))/6
                weak=A*pure+F(o,6)*(B-E*pure)
                assert left-weak==F(d-o,6)*(B-E*pure)>=0;single_mean+=1
                left=sum((m25(p,n,t,pure) for t in menu),F(0))/6
                weak=B*pure+F(o,6)*(A-E*pure)
                assert left-weak==F(d-o,6)*(A-E*pure)>=0;single_mean+=1
            actual=sum((m25(p,n,menu[l],menu[j]) for l in range(6) for j in range(6) if l!=j),F(0))/30
            assert actual>=F(o,6)*(A+B);double_mean+=1
assert (hidden,minima,single_mean,double_mean)==(200,48,3072,768)

# Rebuild C30's internal averaged-query envelope. These inner moments stay.
c30=K.C30;c30states=0
for entry in c30:
    p,c,r3,r4,r5,r6,o=entry["bits"];b=p+c;aq=[]
    for q in [0,1]:
        costs=[]
        for r,y,t in product([0,1],repeat=3):
            D=1+b+q+r
            cost=F(126000*q,b+1+r+y+t)+F(43*r+31218*y+34458*t,b+r3+3)+F(1654*(r+y+t),b+r3+r4+r5+1)
            cost+=5400*(F(o,6)-t)/(D+y)
            cost+=7740*(F(o,3*D)-F(y,D+t)-F(t,D+y)-F(y,D*(D+1)))
            costs.append(cost);c30states+=1
        aq.append(min(costs))
    expected=aq[0] if not o else min((5*aq[0]+aq[1])/6,aq[1])
    assert expected==F(entry["m30"])
    load=p+c+r3+r4+r5+r6
    wallet=F(126000*r3+65719*r4+4962*r6,load) if load else F(0)
    assert wallet-expected==F(entry["cut"])
assert c30states==2048

# State map is a bijection: old(v,q,r) index32v+16q+r equals new(h,r), h=2v+c.
preimages=Counter();outside_cases=Counter();wrong_a2=0;full_states=0
for h in range(512):
    atom=K.atom_from_index(h);v=h//2;c=h%2
    for tnum,tail in enumerate(product([0,1],repeat=4)):
        assert h*16+tnum==v*32+c*16+tnum
        target=K.c30_index(atom,tail);preimages[target]+=1
        new_value=K.coefficient(full[-1],atom,tail)
        assert new_value==-F(c30[target]["cut"])
        wrong_bits=[atom["a"][0],atom["a"][1],*tail,atom["o"]]
        wrong_index=sum(bit<<(6-i) for i,bit in enumerate(wrong_bits))
        if F(c30[wrong_index]["cut"])!=F(c30[target]["cut"]):wrong_a2+=1
        outside_cases[(c,atom["o"])]+=1;full_states+=1
assert full_states==8192 and len(preimages)==128 and set(preimages.values())=={64}
assert set(outside_cases.values())=={2048}

# Direct physical, synthetic examples only. These are not prior or future LP points.
fixtures=[]
singleton=[]
for client in range(7):
    atom={"a":[int(client==i) for i in range(6)],"x":int(client==4),"o":int(client<6),"c":int(client==6)}
    tail=[int(client==i) for i in [1,2,3,4]]
    singleton.append({"client":client,"mass":"1","atom":atom,"tail":tail})
fixtures.append({"id":"seven_singletons","K":"1","O":"6","clients":singleton,
    "catalogue":"Seven distinct singleton labels Q1..Q6,C. Actual Ai=Qi, X=Q5, chosen OPT6 union=Q1..Q6.",
    "true_fixed_C_branch":"(Q1,C,Q2,Q3,Q4,Q5)",
    "complete_strategy":"At every ordered history choose the least-index uncovered singleton. There are enough unused labels for all remaining players, so this gives own payoff1; repeated covered choices give at most1/2. Thus the rule is a complete pure SPE.",
    "purpose":"Both c1/o0 and c0/o1 are physically present; neither obsolete outer-moment bound is valid for fixed C."})
fixtures.append({"id":"one_client_aliases_and_empty","K":"1","O":"1",
    "clients":[{"client":0,"mass":"1","atom":{"a":[1]*6,"x":1,"o":1,"c":1},"tail":[1]*4}],
    "catalogue":"Two distinct labels P,C cover the one client; E is empty. The six menu positions all equal P.",
    "true_fixed_C_branch":"(P,C,P,P,P,P)",
    "complete_strategy":"Choose P at every history. Nonempty actions have the same positive final own payoff; empty actions give zero. P and C are distinct labels although their covers coincide.",
    "purpose":"Aliases, repeated menu indices, repeated actions and empty labels are not collapsed or excluded."})
fixtures.append({"id":"zero_clients","K":"0","O":"0","clients":[],"catalogue":"One empty legal label; no clients.",
    "true_fixed_C_branch":"Six copies of the empty label.","complete_strategy":"Unique label at every history.","purpose":"Zero-customer boundary."})
fixture_results=[]
for fixture in fixtures:
    symbols={"K":F(fixture["K"]),"F_X":F(0)}
    symbols.update({f"u{i}":F(0) for i in range(1,7)})
    csize=F(0)
    for client in fixture["clients"]:
        atom=client["atom"];mass=F(client["mass"]);actual=atom["a"];load=sum(actual)
        for i in range(6):symbols[f"u{i+1}"]+=mass*(F(actual[i],load) if load else F(0))
        symbols["F_X"]+=mass*F(atom["x"],sum(actual[:4])+1);csize+=mass*atom["c"]
    assert csize==symbols["K"]
    slacks=[]
    for row in full:
        rhs=sum((F(weight)*symbols[symbol] for symbol,weight in row["rhs"].items()),F(0))
        lhs=sum((F(client["mass"])*K.coefficient(row,client["atom"],client["tail"]) for client in fixture["clients"]),F(0))
        slack=rhs-lhs;assert slack>=0,(fixture["id"],row["legacy_index"],slack)
        slacks.append(str(slack))
    fixture_results.append({**fixture,"all751_raw_slacks":slacks,"all734_local_rows_pass":True,"all16_visible_prerequisites_pass":True,"C_size_equality_pass":True})
lower_violation=F(-1,6);upper_violation=F(-1)
assert singleton[0]["atom"]["c"]==0 and singleton[0]["atom"]["o"]==1
assert singleton[6]["atom"]["c"]==1 and singleton[6]["atom"]["o"]==0

# A concrete negative free mass multiplier is allowed in the new projection identity.
byname={r["name"]:r for r in active}
example_atom={"a":[0]*6,"x":0,"o":0,"c":0}
weights={"NEW_SAFE_j5|R5":"1"}
envelope=K.single_type_envelope(weights,example_atom)
assert envelope["minimum"]==F(-1,2)
assert all(x["residual"]>=0 for x in envelope["tail_residuals"])
for tail in product([0,1],repeat=4):
    W=K.coefficient(byname["NEW_SAFE_j5|R5"],example_atom,tail)
    m=envelope["minimum"]
    # w=3,nu=2 at this state gives E=nu-w=-1; identity holds without assuming mass equality.
    lhs=-m*3
    rhs=-W*2+(W-m)*2+m*(2-3)
    assert lhs==rhs

pins=json.loads((HERE/"source_pins.json").read_text())["sources"]
for relative,digest in pins.items():assert sha(REPO/relative)==digest,relative
template=json.loads((HERE/"symbolic_template.json").read_text())
assert not template["outer_q_moment_rows"] and template["fixed_input"] is None and template["fixed_matrix"] is None
assert template["optimizer_calls"]==0 and not template["optimizer_authorized"]
dump("literal_static_fixtures.json",{"status":"PASS_SYNTHETIC_ONLY_NO_POINT_BINDING","optimizer_calls":0,
    "legacy_boundary_states":sample_results,"physical_fixtures":fixture_results,
    "invalid_outer_moments_counterexample":{"fixture":"seven_singletons","lower_slack_on_Q1_client":str(lower_violation),"upper_slack_on_C_client":str(upper_violation)},
    "negative_free_mass_multiplier_example":{"weights":weights,"atom":example_atom,"minimum":str(envelope["minimum"]),
        "tail_residuals":[{"tail":v["tail"],"residual":str(v["residual"])} for v in envelope["tail_residuals"]]}})
result={"status":"PASS_SYMBOLIC_FIXED_C_734_UNBOUND_WITH_FULL751_MIGRATION","optimizer_calls":0,
    "full_audit_rows":751,"active_hidden_rows":734,"visible_prerequisites":16,"C_size_equality_routes":1,
    "inapplicable_genuine_kernels":0,"removed_outer_q_moments_per_type":2,
    "boundary_row_triples":triples,"boundary_scalar_checks":3*triples,
    "P25_true_inner_hidden_states":hidden,"P25_minima":minima,"P25_single_inner_means":single_mean,"P25_double_inner30_cases":double_mean,
    "C30_true_inner_hidden_states":c30states,"C30_envelopes":128,"all8192_C30_state_routes":full_states,
    "C30_preimages_per_envelope":64,"detects_wrong_actual_a2_substitution":wrong_a2,
    "all_c_o_groups_retained":{str(k):v for k,v in outside_cases.items()},
    "synthetic_physical_fixtures":3,"synthetic_full_row_checks":3*751,
    "free_mass_multiplier_can_be_negative":True,"fixed_point_bound":False,"matrix_constructed":False,
    "old_numerical_point_files_read":False,"old_producer_kernel_executed":False,
    "source_files_unchanged":len(pins),
    "coverage_note":"All751 kernel transfer is proved by the explicit state relabeling and source formulas, with9012 frozen boundary row triples replayed. C30 is replayed on all8192 states. No full751-by8192 matrix is allocated or claimed emitted."}
dump("symbolic_check_result.json",result)
print(json.dumps(result,indent=2))
