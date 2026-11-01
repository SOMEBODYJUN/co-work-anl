"""One frozen split.build(), exact whole saved-point audit, no optimization.

The separate runtime must already contain the shared frozen dependency tree.
Output is always outside that tree and, in the recorded event, outside Git.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import platform
import sys
import time

BASE = Path("research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5")
OLD = Path("research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra")
POINT_SHA = "b12c4aa6b3cd106f3fb8e8a56be7469988456c0cb6e02b1741db8c09d587b34a"


def key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def descriptors(columns):
    return [{k: v for k, v in c.items() if k != "weight"} for c in columns]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    raw = (args.runtime / BASE / "split_basic_exact.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == POINT_SHA
    point = json.loads(raw)
    sys.path.insert(0, str(args.runtime / BASE))
    split = importlib.import_module("split_basic_graph")
    build_start = time.perf_counter()
    cols, names, matrix, obj, norm = split.build()
    build_seconds = time.perf_counter() - build_start
    stored = point["columns"]
    assert len(cols) == len(stored) == 1905
    assert key(descriptors(cols)) == key(descriptors(stored))
    assert len(matrix) == len(names) == point["verified_rows"] == 3945
    weights = list(map(lambda c: F(c["weight"]), stored))
    assert min(weights) >= 0
    slacks = [sum(a * b for a, b in zip(row, weights)) for row in matrix]
    assert min(slacks) == F(point["minimum_slack"]) == 0
    assert all(len(row) == len(weights) for row in matrix)
    assert sum(a*b for a,b in zip(norm,weights)) == F(point["O"]) == 1
    W = sum(a*b for a,b in zip(obj,weights))
    assert W == F(point["W"]) < F(1,2)
    assert 1-2*W == F(point["strict_half_gap"])
    assert sum(w>0 for w in weights) == point["positive_columns"] == 165
    assert len(split.SPLIT) == point["additional_split_rows"] == 56
    assert point["base_rows"] == 702 and point["first_raw_rows"] == 37
    assert point["additional_index_class_rows"] == 100
    hist = {}
    groups = {}
    old_to_current = {}
    current = None
    for index, column in enumerate(stored):
        if column["kind"] == "hist":
            current = index
            hist[index] = column
            assert len(column["actual_bits"]) == 6
            assert set(column["actual_bits"]) <= {"0", "1"}
            assert len(column["hist"]) == 8 and sum(column["hist"]) == 6
            assert all(isinstance(x,int) and x>=0 for x in column["hist"])
            assert column["d"] == sum(column["hist"][4:]) == 1
        elif column["kind"] == "joint-reply":
            assert current is not None
            old = column["hist_column_old"]
            assert old_to_current.setdefault(old,current) == current
            group = (current,key(column["group"]))
            state = tuple(column["state"])
            assert state in ((0,1),(1,0),(1,1))
            assert state not in groups.setdefault(group,{})
            groups[group][state] = weights[index]
    assert len(hist) == 16 and len(groups) == 194 and len(old_to_current) == 16
    margins = {}
    for (hi,g), states in groups.items():
        assert set(states) == {(0,1),(1,0),(1,1)}
        h=weights[hi]
        assert h-sum(states.values())>=0
        margins[(hi,g)] = states[(1,0)]+states[(1,1)]
    lower_failures=[]
    upper_slacks=[]
    equal_min=0
    for index,c in enumerate(stored):
        if c["kind"] != "overlap": continue
        hi=c["hist_column"]
        r1,r2=(margins[(hi,key(g))] for g in c["groups"])
        v=weights[index];h=weights[hi]
        upper_slacks.extend([r1-v,r2-v])
        equal_min += v==min(r1,r2)
        low=max(F(0),r1+r2-h)
        if v<low:
            lower_failures.append({"column":index,"hist_column":hi,"groups":c["groups"],
                                   "hist_mass":str(h),"r1":str(r1),"r2":str(r2),
                                   "overlap":str(v),"lower_bound":str(low),"deficit":str(low-v)})
    assert len(upper_slacks)==2612 and min(upper_slacks)>=0
    payoffs=[F(0)]*6
    for hi,c in hist.items():
        bits=tuple(map(int,c["actual_bits"]));count=sum(bits)
        if count:
            for j in range(6):payoffs[j]+=weights[hi]*F(bits[j],count)
    assert sum(payoffs)==W
    assert sum(weights[hi] for hi in hist)==1
    old_raw=(args.runtime/OLD/"attractive_nested_exact.json").read_bytes()
    old=json.loads(old_raw)
    assert descriptors(old["columns"])==descriptors(stored)
    diffs=[{"column":i,"kind":c["kind"],"old_weight":old["columns"][i]["weight"],"new_weight":c["weight"]}
           for i,c in enumerate(stored) if F(c["weight"])!=F(old["columns"][i]["weight"])]
    prior=json.loads((args.runtime/"prior-independent-split-report.json").read_text())
    assert prior["split_point_W"]==point["W"] and len(prior["split_slacks"])==56
    for spec,value,saved in zip(split.SPLIT,slacks[-56:],prior["split_slacks"]):
        assert tuple(spec)==(saved["stage"],saved["diagonal"],saved["name"])
        assert value==F(saved["value"])
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    summary={"status":"passed-one-original-build-and-complete-exact-point-substitution",
             "python":platform.python_version(),"build_seconds":build_seconds,"seconds":time.perf_counter()-start,
             "original_build_calls":1,"original_CLI_calls":0,"optimizer_calls":0,
             "point_sha256":POINT_SHA,"rows":len(matrix),"columns":len(cols),
             "zero_slacks":sum(v==0 for v in slacks),"minimum_slack":str(min(slacks)),
             "W":str(W),"K":str(weights[0]),"actual_payoffs":list(map(str,payoffs)),
             "positive_columns":sum(w>0 for w in weights),
             "positive_by_kind":dict(Counter(c["kind"] for c,w in zip(stored,weights) if w>0)),
             "column_descriptors_all_equal":True,"joint_00_masses_nonnegative":True,
             "overlap_upper_bound_count":len(upper_slacks),"overlaps_equal_min":equal_min,
             "overlap_lower_bound_failures":len(lower_failures),
             "old_point_sha256":hashlib.sha256(old_raw).hexdigest(),"old_point_W":old["W"],
             "old_point_declared_rows":old["verified_rows"],"changed_columns":len(diffs),
             "changes_by_kind":dict(Counter(x["kind"] for x in diffs)),
             "prior_56_slacks_all_exactly_equal":True,
             "limits":"one original matrix implementation; independent prior 56-row audit reused; no full SPE or exact optimum"}
    for filename,data in [("summary.json",summary),("all-row-slacks.json",[{"row":i,"name":str(n),"slack":str(v)} for i,(n,v) in enumerate(zip(names,slacks))]),("overlap-lower-bound-failures.json",lower_failures),("old-point-coordinate-differences.json",diffs)]:
        (out/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
