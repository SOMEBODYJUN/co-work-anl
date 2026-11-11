"""Independent standard-library Fraction verifier for the ZZ19578 extension.

Imports no assembly, recovery, numerical solver, or cut discovery module.
Every inherited sparse row and every descriptor is compared to frozen inputs;
every primal row, dual column, and canonical auxiliary is checked exactly.
Mathematical validity of the inherited inequalities remains the source proof's
responsibility; this script certifies this finite system only.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
BASE=RUN/"zz_closure_lp"/"round2"
CUTS=RUN/"shared_source_deepening"/"selected_all_named_19556.json"


def read_matrix(path):
    with gzip.open(path,"rt",encoding="utf-8") as stream:
        return json.load(stream)


def decode(encoded,n):
    result={}
    for column,value in encoded:
        assert type(column) is int and 0 <= column < n and column not in result
        rational=Fraction(value)
        assert rational
        result[column]=rational
    return result


def dot(row,values):
    total=Fraction(0)
    for column,coefficient in row.items():
        total+=coefficient*values[column]
    return total


def main():
    start=time.time()
    inputs=json.loads((HERE/"inputs.json").read_text())
    for relative,digest in inputs["sha256"].items():
        assert sha256((RUN/relative).read_bytes()).hexdigest()==digest,relative
    for record in json.loads((HERE/"source_snapshots.json").read_text()):
        assert sha256((RUN/record["source"]).read_bytes()).hexdigest()==record["sha256"]
        assert sha256((HERE/record["snapshot"]).read_bytes()).hexdigest()==record["sha256"]
    assert sha256((BASE/"augmented_lp_exact.json").read_bytes()).hexdigest()=="bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3"
    assert sha256((BASE/"exact_matrix.json.gz").read_bytes()).hexdigest()=="353b1978b6c2ad46d28dc33a03b5ff8c3f71f273d9bf4d71cc15f5a9cf223f0c"
    assert sha256(CUTS.read_bytes()).hexdigest()=="3b373504be8593d6737433ea8341aac5eba67a153243392d173631e05f02e130"
    matrix=read_matrix(HERE/"exact_matrix.json.gz")
    baseline=read_matrix(BASE/"exact_matrix.json.gz")
    point=json.loads((HERE/"augmented_lp_exact.json").read_text())
    cuts=json.loads(CUTS.read_text())
    original_n,n,prior_m=4849,15593,19556
    assert len(baseline["rows"])==prior_m and len(baseline["columns"])==n
    assert matrix["columns"]==baseline["columns"]
    assert matrix["row_names"][:prior_m]==baseline["row_names"]
    assert matrix["objective"]==baseline["objective"]
    assert matrix["normalization"]==baseline["normalization"]
    assert matrix["rows"][:prior_m]==baseline["rows"]
    assert len(matrix["rows"])==len(matrix["row_names"])==19578
    assert len(matrix["rows"])==matrix["original_rows"]+matrix["appended_unique_rows"]
    assert [{k:v for k,v in c.items() if k!="weight"} for c in point["columns"]]==matrix["columns"]
    rows=[decode(encoded,n) for encoded in matrix["rows"]]
    old_signatures={tuple(sorted(row.items())) for row in rows[:prior_m]}
    new_signatures=set()
    records=json.loads((HERE/"cut_records.json").read_text())
    assert len(records)==len(cuts["selected_rows"])==22
    assert Counter((r["state_count"],r["theta"]) for r in cuts["selected_rows"])=={(2,"0"):11,(2,"1/4"):10,(4,"1/4"):1}
    input_point=json.loads((BASE/"augmented_lp_exact.json").read_text())
    old_values=[Fraction(c["weight"]) for c in input_point["columns"]]
    for offset,(source,record) in enumerate(zip(cuts["selected_rows"],records)):
        i=prior_m+offset
        expected=decode(source["coefficients"],n)
        assert rows[i]==expected and all(j < original_n for j in expected)
        assert record["row"]==i and record["name"]==source["name"]
        assert matrix["row_names"][i]=="named-at19556:"+source["name"]
        digest=sha256(json.dumps(source["coefficients"],separators=(",",":")).encode()).hexdigest()
        assert digest==source["vector_sha256"]==record["vector_sha256"]
        sig=tuple(sorted(expected.items()))
        assert sig not in old_signatures and sig not in new_signatures
        new_signatures.add(sig)
        value=dot(expected,old_values)
        assert value==Fraction(source["slack"])==Fraction(record["input_slack"]) < 0
    values=[Fraction(c["weight"]) for c in point["columns"]]
    assert len(values)==n and min(values)>=0
    assert point["positive_columns"]==sum(v>0 for v in values)
    epi=json.loads((HERE/"epigraph_structure.json").read_text())
    zz=json.loads((HERE/"zz_envelope_structure.json").read_text())
    for name in ("epigraph_structure.json","zz_envelope_structure.json"):
        assert (HERE/name).read_bytes()==(BASE/name).read_bytes()
    assert len(epi["thresholds"])==7954 and len(zz["auxiliaries"])==2790
    assert {j for j,i in epi["thresholds"]}==set(range(original_n,12803))
    for j,i in epi["thresholds"]:
        assert rows[i][j]==1 and all(k < original_n or k==j for k in rows[i])
        expression=sum((v*values[k] for k,v in rows[i].items() if k < original_n),Fraction(0))
        assert values[j]==max(Fraction(0),-expression)
    assert [r["column"] for r in zz["auxiliaries"]]==list(range(12803,n))
    for r in zz["auxiliaries"]:
        j=r["column"]
        upper=[]
        for i in (r["q_upper_row"],r["v_upper_row"]):
            assert rows[i][j]==-1 and all(k < original_n or k==j for k in rows[i])
            upper.append(sum((v*values[k] for k,v in rows[i].items() if k < original_n),Fraction(0)))
        assert values[j]==min(upper)
    objective=list(map(Fraction,matrix["objective"]))
    normalization=list(map(Fraction,matrix["normalization"]))
    assert len(objective)==len(normalization)==n
    assert not any(objective[original_n:]+normalization[original_n:])
    O=sum((a*b for a,b in zip(normalization,values)),Fraction(0))
    W=sum((a*b for a,b in zip(objective,values)),Fraction(0))
    assert O==Fraction(point["O"])==1 and W==Fraction(point["W"])
    assert Fraction(point["strict_half_gap"])==1-2*W
    slacks=[dot(row,values) for row in rows]
    assert min(slacks)>=0 and str(min(slacks))==point["minimum_slack"]
    assert point["verified_rows"]==len(rows)
    primal_audit=json.loads((HERE/"primal_exact_audit.json").read_text())
    assert slacks==list(map(Fraction,primal_audit["row_slacks"]))
    dual=json.loads((HERE/"exact_dual_certificate.json").read_text())
    matrix_hash=sha256((HERE/"exact_matrix.json.gz").read_bytes()).hexdigest()
    assert matrix_hash==dual["matrix_sha256"]
    lower=Fraction(dual["normalization_multiplier"])
    residuals=[c-lower*a for c,a in zip(objective,normalization)]
    seen=set()
    positive_dual_new_rows=[]
    complementarity=Fraction(0)
    for i,encoded in dual["row_multipliers"]:
        weight=Fraction(encoded)
        assert type(i) is int and 0 <= i < len(rows) and i not in seen and weight>0
        seen.add(i)
        for j,coefficient in rows[i].items():
            residuals[j]-=weight*coefficient
        complementarity+=weight*slacks[i]
        if i>=prior_m:
            positive_dual_new_rows.append([i,str(weight)])
    assert min(residuals)>=0 and residuals==list(map(Fraction,dual["residuals"]))
    assert lower==W and complementarity==0
    assert sum((a*b for a,b in zip(residuals,values)),Fraction(0))==0
    old_W=Fraction(input_point["W"])
    report={"scope":"independent standard-library all-row/all-column Fraction check of this finite necessary LP only; not SPE or universal bound",
            "rows":len(rows),"columns":n,"O":str(O),"W":str(W),"W_float":float(W),
            "below_half":W<Fraction(1,2),"strict_half_gap":str(1-2*W),
            "input_sha256_verified":True,"unchanged_baseline_rows":prior_m,"unchanged_baseline_columns":n,
            "appended_full_vectors_verified":22,"distinct_from_baseline_and_each_other":True,
            "canonical_max_auxiliaries_verified":7954,"canonical_min_auxiliaries_verified":2790,
            "exact_primal_verified":True,"primal_rows_checked":len(rows),"nonnegative_primal_columns_checked":n,
            "minimum_primal_slack":str(min(slacks)),"positive_original_columns":sum(v>0 for v in values[:original_n]),
            "positive_max_auxiliaries":sum(v>0 for v in values[original_n:12803]),
            "positive_min_auxiliaries":sum(v>0 for v in values[12803:]),
            "exact_dual_verified":True,"dual_columns_checked":n,"exact_optimum":str(lower),
            "minimum_dual_residual":str(min(residuals)),"positive_dual_rows":len(seen),
            "positive_dual_new_rows":positive_dual_new_rows,
            "exact_complementarity_verified":True,"strictly_above_old_W":W>old_W,
            "exact_optimum_increase":str(W-old_W),"optimum_increase_float":float(W-old_W),
            "new_row_slacks":[[i,matrix["row_names"][i],str(slacks[i])] for i in range(prior_m,len(rows))],
            "matrix_sha256":matrix_hash,"point_sha256":sha256((HERE/"augmented_lp_exact.json").read_bytes()).hexdigest(),
            "dual_sha256":sha256((HERE/"exact_dual_certificate.json").read_bytes()).hexdigest(),
            "verifier_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),"seconds":time.time()-start}
    (HERE/"certificate_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("new_row_slacks","positive_dual_new_rows")},indent=2))


if __name__=="__main__":
    main()
