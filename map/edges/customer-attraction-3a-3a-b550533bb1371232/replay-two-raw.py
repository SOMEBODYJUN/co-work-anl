from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

rawbase = Path("archives/customer-attraction/tools/evidence/reserve-probes-and-cone-records-four-primary/related-original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general")
paths = [rawbase / "equilibrium/fractional_global_raw.json", rawbase / "exchange/copy2_counterexample_audit.json"]
for path in paths:
    raw = path.read_bytes()
    print(path.name, len(raw), sha256(raw).hexdigest())
    print("keys", list(json.loads(raw)))
first, second = (json.loads(p.read_bytes()) for p in paths)
pol817 = {tuple(d["history"]): d["action"] for d in first["policy"]}
pol35 = {tuple(d["history"]): d["action"] for d in second["strategy"]}
weights817 = {int(mask): w for mask, w in first["customer_mask_multiplicities"].items()}
sets817 = [{(mask, i) for mask,w in weights817.items() if mask & (1 << a) for i in range(w)} for a in range(6)]
sets35 = [set(row) for row in second["expanded_topics"]]
assert set().union(*sets35) == set().union(*second["expanded_customers"].values())

def verify(sets, policy):
    labels = range(len(sets))
    histories = [h for d in range(3) for h in product(labels, repeat=d)]
    assert list(policy) == histories
    def leaf(h):
        while len(h) < 3:
            h += (policy[h],)
        return h
    def members(z):
        return set().union(*(sets[t] for t in z))
    def u(i, z):
        return sum((F(1,sum(x in sets[t] for t in z)) for x in sets[z[i]]), F())
    opt3 = max(len(members(z)) for z in product(labels, repeat=3))
    gains, margins, reserve = {}, {}, {}
    for h in histories:
        i = len(h)
        actual = leaf(h)
        gains[h] = tuple(u(i, leaf(h+(a,))) for a in labels)
        margins[h] = tuple(gains[h][policy[h]]-v for v in gains[h])
        assert min(margins[h]) == 0
        opt = max(len(members(h + z)) for z in product(labels, repeat=3-i))
        welfare = len(members(actual))
        u_past = sum((u(j,actual) for j in range(i)),F())
        reserve[h] = opt-2*welfare+u_past, opt, welfare, u_past, actual
    print("nodecount, strictly positive IC, opt3", len(histories),sum(v>0 for row in margins.values() for v in row),opt3)
    print("root and payoffs",leaf(()),tuple(u(i,leaf(())) for i in range(3)),reserve[()])
    print("reserve maxima",[(h,v) for h,v in reserve.items() if v[0]==max(w[0] for w in reserve.values())])
    return gains, u, leaf

gains817, u817, leaf817 = verify(sets817,pol817)
gains35, u35, leaf35 = verify(sets35,pol35)
for row in second["strategy"]:
    assert tuple(F(s) for s in row["true_deviation_utilities"]) == gains35[tuple(row["history"])]
assert len(second["strategy"]) * len(sets35) == 155
assert sum(weights817.values()) == 817 and len(set().union(*sets35)) == 35
bg = [tuple(leaf817(leaf817(())[:i]+(t,))[j] for j in range(3) if j!=i) for i in range(3) for t in [2,5]]
f = [sum(((F(x in sets817[2])+F(x in sets817[5]))/2 / (1+F(sum(x in sets817[a] for z in bg[2*i:2*i+2] for a in z),2)) for x in set().union(*sets817)),F()) for i in range(3)]
assert sum(f)-597 == F(199,60)
print("817 backgrounds and payment",bg,f,sum(f)-597)
print("35 copied",leaf35((0,0)),tuple(u35(i,leaf35((0,0))) for i in range(3)))
print("all exact comparisons verified")
