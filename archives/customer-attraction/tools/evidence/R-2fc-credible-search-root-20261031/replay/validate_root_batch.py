import json, hashlib, pathlib, ast
root=pathlib.Path(__file__).resolve().parents[1]
errs=[]
def load(n):
    p=root/"source"/n
    return json.loads(p.read_text())
def check(c,ok,msg):
    if not ok: errs.append(msg)
for n in ("m5p7_2210000.json","m5p7_3200000.json"):
    d=load(n); m=d["milp"]
    check(c:=d, c["universal_claim_proved"] is False, n+" universal")
    check(c, c["exact_candidate"] is None, n+" exact_candidate")
    check(c, m["status"]==1 and m["floating_bound_not_a_certificate"] is True, n+" timeout boundary")
for n in ("tight_markov_00011.json","tight_markov_00112.json"):
    d=load(n); m=d["milp"]; x=d["exact_candidate"]
    check(d, d["universal_claim_proved"] is False, n+" universal")
    check(d, d["valid_conditional_big_M"]==1, n+" M")
    check(d, m["status"]==1 and m["floating_bound_not_certificate"] is True, n+" timeout boundary")
    check(d, x is not None and x["ratio"]=="1" and x["objective_value"]=="1", n+" exact candidate")
d=load("largest_incumbent_n3p6_best.json")
check(d,d["source_claimed_verified"] is True,"legacy flag")
check(d,d["full_history_SPE"] is False and len(d["bad_comparisons"])==5 and d["nonroot_bad_comparisons"]==0,"root correction")
check(d,d["welfare"]==750 and d["optimum"]==963,"welfare")
script=(root/"source/tight_markov_probe.py").read_text()
for s in ("valid W=1 bounds", "count-Markov subclass", "universal_claim_proved"):
    check(d,s in script,"script marker "+s)
try: ast.parse(script)
except SyntaxError as e: errs.append("script syntax "+repr(e))
if errs:
    print("FAIL")
    print("\n".join(errs))
    raise SystemExit(1)
print("PASS root batch validator")
print("restricted_timeout=2")
print("tight_markov_exact_candidates=2")
print("legacy_root_bad_comparisons=5")
print("legacy_full_history_SPE=false")
