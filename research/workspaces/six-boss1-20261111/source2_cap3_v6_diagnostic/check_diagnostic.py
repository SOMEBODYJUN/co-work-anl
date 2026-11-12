#!/usr/bin/env python3
"""Independent standard-library verification of the completed v6 diagnostic.

This does not import diagnose.py, source builders, recovery code, or a solver.
All external data are read only through the explicit SHA-bound input binding.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
import traceback

P=Path(__file__).resolve().parent
F=Fraction
B=list(product((0,1),repeat=9))
R=list(product((0,1),repeat=4))


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p): return json.loads(p.read_text())


def exact(x):
    assert isinstance(x,(str,int)) and not isinstance(x,bool)
    if isinstance(x,str): assert "." not in x and "e" not in x.lower()
    return F(x)


def rationalize(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):rationalize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [rationalize(v) for v in x]
    return x


def write(name,obj): (P/name).write_text(json.dumps(rationalize(obj),ensure_ascii=False,indent=2)+"\n")


def run():
    binding=load(P/"input_binding.json")
    external={}
    for key,ref in binding["inputs"].items():
        p=Path(ref["path"])
        assert sha(p)==ref["sha256"]
        external[key]=load(p)
    source=Path(binding["source"]["path"])
    assert sha(source/"freeze_manifest.json")=="bc0d03e6cb05fc6c270fc14ec2e547a3333cf36b924dd883e8d25cd3ad450c8f"
    for rec in load(source/"freeze_manifest.json")["files"]: assert sha(source/rec["path"])==rec["sha256"]
    assert sha(source/"exact_family.json")=="4a31f3ff6847a355442807aa8d03fffad43c92c6849229f63299556da8c00c8b"
    family=load(source/"exact_family.json")["rows"]
    tables={v["vertex_key"]:v for v in load(source/"vertex_cost_tables.json")["vertices"]}
    registry={v["vertex_key"]:v for v in load(source/"vertex_registry.json")["records"]}
    assert len(family)==585 and len(tables)==len(registry)==225
    model=external["input"]
    cert=external["certificate"]
    face=external["face"]
    assert cert["input_sha256"]==binding["inputs"]["input"]["sha256"]
    assert face["certificate_sha256"]==binding["inputs"]["certificate"]["sha256"]
    assert face==load(P/"complete_face_parameter_domain.json")
    assert model["bit_order"]==["a1","a2","a3","a4","a5","a6","x","o","c"]
    assert model["K_column"]==512 and len(model["atom_columns"])==512
    for i,(atom,bits) in enumerate(zip(model["atom_columns"],B)):
        assert tuple(atom["a"])+(atom["x"],atom["o"],atom["c"])==bits
        assert i==atom["index"]==2*atom["old_index"]+atom["c"]
    assert len(face["all_raw_inequality_restrictions"])==4177
    assert len(face["all513_nonnegative_coordinate_restrictions"])==513
    point=[exact(x) for x in cert["primal"]]
    n=len(face["parameters"])
    assert n==9 and face["restricted_equation_rank"]==14 and len(face["zero_residual_columns"])==23
    origin=[F(0)]*513
    slopes=[[F(0)]*513 for _ in range(n)]
    for rec in face["coordinates"]:
        c=rec["column"]
        origin[c]=exact(rec["constant"])
        for j,v in enumerate(rec["parameter_coefficients"]): slopes[j][c]=exact(v)
    theta=[exact(x) for x in face["point_parameters"]]
    assert [origin[i]+sum(slopes[j][i]*theta[j] for j in range(n)) for i in range(513)]==point
    cached={}
    cost_count=0
    weak_count=0
    all_rebuilt={}
    payment_checks=0
    point_output={r["metadata"]["id"]:r for r in load(P/"point_slacks_all585.json")["rows"]}
    face_output={r["row_id"]:r for r in load(P/"face_affine_all585.json")["rows"]}
    assert len(point_output)==len(face_output)==585
    signs=Counter()
    zero=[]
    literal_matches=0
    for row in family:
        d,h,s,q0=(exact(row[k]) for k in ("delta","h","s","q0"))
        t4=F(5977,6912)-d
        t5=F(43,48)+d
        a=25+t4+t5-s
        caps=(q0/2+q0*t4/12+q0*t5/6-h,q0/2+t4+q0*t5/6,q0/2+t5,F(1))
        assert a==exact(row["real_budget"]["source_IC"])
        assert [exact(row["beta_actual"][str(j)]) for j in (3,4,5)]==list(caps[:3])
        assert [exact(row["tau"][str(j)]) for j in (3,4,5)]==[0,t4,t5]
        S=sum(caps)
        mu=S-s/5 if row["row_kind"]=="C-only" else F(0)
        assert (S,mu,S-mu)==tuple(exact(row[k]) for k in ("raw_K","free_EC","K"))
        assert row["divisor_applied"] is False and row["raw_scale"] is True
        payment_checks+=1
        key=row["vertex_key"]
        if key not in cached:
            minima={}
            weak={}
            for c in tables[key]["conditions"]:
                p,t,nn=c["p"],c["t"],c["n"]
                q=F(nn,6) if row["mode"]=="pure" else F(nn-t,5)
                values={}
                for r3,r4,r5,z in R:
                    L=p+t+r3+r4+r5+z
                    source=(a*t-t4*r4-t5*r5-z)/L if L else F(0)
                    caps_pay=caps[0]*r3+caps[1]*r4+caps[2]*r5+z
                    queries=q/(p+t+r3+r4+r5+1)+t4*q/(p+t+r3+3)+t5*q/(p+t+r3+r4+2)
                    label=f"{r3}{r4}{r5}{z}"
                    values[label]=source+caps_pay+queries
                    assert values[label]==exact(c["costs"][label])
                    cost_count+=1
                m=min(values.values())
                w=[label for label,v in values.items() if v==m]
                assert m==exact(c["minimum"]) and w==c["all_weak_tails"]
                minima[p,t,nn]=m
                weak[p,t,nn]=w
                weak_count+=1
            G={}
            if row["mode"]=="ordered":
                for p in (0,1):
                    values=[]
                    for nn in range(7):
                        v=(6-nn)*minima[p,0,nn] if nn<6 else F(0)
                        if nn: v+=nn*minima[p,1,nn]
                        v/=6
                        assert v==exact(tables[key]["f"][str(p)][str(nn)])
                        values.append(v)
                    assert values[0]==0 and values[1]<min(values[2:])
                    G[p]=values[1]
            cached[key]=minima,weak,G
        minima,weak,G=cached[key]
        if row["mode"]=="pure":
            T=row["target"]
            col=int(T[1:])-1 if T[0]=="A" else 6 if T=="X" else 8
        vector=[]
        for bits in B:
            actual_load=sum(bits[:6])
            u=F(bits[1],actual_load) if actual_load else F(0)
            tail=minima[bits[0],bits[col],bits[7]] if row["mode"]=="pure" else bits[7]*G[bits[0]]
            vector.append(a*u-tail+mu*bits[8])
        vector.append(S-mu)
        assert vector==[exact(v) for v in row["a"]]
        all_rebuilt[row["id"]]=vector
        value=sum(v*x for v,x in zip(vector,point))
        out=point_output[row["id"]]
        assert out["metadata"]=={k:v for k,v in row.items() if k!="a"}
        assert value==exact(out["slack"])
        status="negative" if value<0 else "zero" if value==0 else "positive"
        assert status==out["sign"]
        signs[status]+=1
        if value==0: zero.append(row["id"])
        const=sum(v*x for v,x in zip(vector,origin))
        co=[sum(v*x for v,x in zip(vector,direction)) for direction in slopes]
        fo=face_output[row["id"]]
        assert const==exact(fo["affine"]["constant"])
        assert co==[exact(v) for v in fo["affine"]["coefficients"]]
        assert not any(co) and const==value
        assert fo["classification"]["entire_face_excluded_by_negative_row"] is False
        for match in out["literal_input_row_matches"]:
            i=match["raw_index"]
            raw=model["raw_rows"][i]
            assert raw["name"]==match["name"] and raw["family"]==match["family"]
            assert [exact(raw["a"].get(str(c),"0")) for c in range(513)]==vector
            assert exact(raw.get("rhs","0"))==0
            assert exact(match["actual_raw_dual_weight"])==exact(cert["dual"]["raw_row_weights"][i])
            literal_matches+=1
    assert signs==Counter(positive=580,zero=5)
    obstruction=load(P/"shared_C_zero_SAFE4_obstruction.json")
    needed=obstruction["row_ids"]
    assert needed==["cap3full_pure_s0_v3_general_C","cap3full_pure_sstar_v6_C-only_C"]
    for rid in needed:
        assert rid in zero
        assert any(exact(rec["actual_raw_dual_weight"])>0 for rec in point_output[rid]["literal_input_row_matches"])
    classes={}
    for p,c,o in product((0,1),repeat=3):
        sets=[]
        for rid in needed:
            r=next(row for row in family if row["id"]==rid)
            sets.append(set(cached[r["vertex_key"]][1][p,c,o]))
        classes[p,c,o]=sorted(set.intersection(*sets))
    assert classes[0,1,1]==["1111"] and classes[1,1,1]==["1101","1110"]
    for rec in obstruction["all_common_weak_classes"]:
        assert rec["common_tails"]==classes[rec["p"],rec["c"],rec["o"]]
    C_without_O=[F(int(b[8] and not b[7])) for b in B]+[F(0)]
    assert sum(v*x for v,x in zip(C_without_O,origin))==0
    assert all(sum(v*x for v,x in zip(C_without_O,d))==0 for d in slopes)
    for p in (0,1):
        for tail in classes[p,1,1]:
            assert tail[0:2]=="11"
            assert F(int(tail[1]),p+1+sum(map(int,tail)))==F(1,5)
    functional=[F(b[7],6*(b[0]+2*b[8]+3)) for b in B]+[F(-1,5)]
    deficit=sum(v*x for v,x in zip(functional,point))
    assert deficit>0
    assert all(sum(v*x for v,x in zip(functional,d))==0 for d in slopes)
    assert deficit==sum(v*x for v,x in zip(functional,origin))
    out=obstruction["conditional_SAFE4_difference"]
    assert functional==[exact(v) for v in out["full_513_coefficients"]]
    assert deficit==exact(out["point_value"])
    assert deficit==F(709638185136480929581839920970892210591292722310716,67588301606736414838046729267264655707163775139064531)
    summary=load(P/"diagnostic_summary.json")
    assert summary["point_sign_counts"]==dict(signs)
    assert summary["zero_row_ids"]==zero
    assert summary["negative_raw_point_exclusions"]==summary["negative_raw_entire_face_exclusions"]==0
    result=dict(status="PASS_INDEPENDENT_DIAGNOSTIC_CHECK",agent_id="/root/source2_cap3_tradeoff",run="six-boss1-20261111",
        full_513_rows_rebuilt=585,raw_coefficient_checks=585*513,true_payment_metadata_checks=payment_checks,
        true_COST_values=cost_count,full_weak_minimum_sets=weak_count,source_vertices=len(cached),
        point_sign_counts=dict(signs),affine_constants=585,exact_zero_parameter_coefficients=585*n,
        literal_v6_row_occurrences_checked=literal_matches,retained_raw_domain_constraints=4177,retained_nonnegative_domain_constraints=513,
        conditional_true_SAFE4_deficit=deficit,zero_payment_obstruction="entire new v6 face",
        negative_new_raw_rows=0,unconditional_new_row_claimed=False,optimizer_calls=0,
        source_builder_imported=False,diagnose_imported=False,old_v5_read=False)
    write("independent_diagnostic_check.json",result)
    print(json.dumps(rationalize(result),ensure_ascii=False))


if __name__=="__main__":
    try: run()
    except Exception as exc:
        old=load(P/"failure_log.json") if (P/"failure_log.json").exists() else []
        old.append(dict(utc=datetime.now(timezone.utc).isoformat(),program="check_diagnostic.py",error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc()))
        write("failure_log.json",old)
        raise
