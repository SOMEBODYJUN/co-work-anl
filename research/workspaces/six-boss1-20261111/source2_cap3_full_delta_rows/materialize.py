#!/usr/bin/env python3
"""Materialize every original-scale row at the 225 frozen physical vertices.

Boss1 / six-boss1-20261111 / agent /root/source2_cap3_tradeoff.
No source mutation, optimization, LP-point access, or row deletion occurs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import traceback

P=Path(__file__).resolve().parent
DEFAULT_SOURCE=Path("/workspace/scratch/b0fef5ec503f/cap3_full_delta_stage")
DEFAULT_REPO=Path("/workspace/scratch/b0fef5ec503f/co-work-anl-boss1")
EXPECTED_MANIFEST="bb47717a8dd60995b0c314c5f5801f50612e4e585ca841211f9c98c5a6613e9a"
TAILS=tuple(product((0,1),repeat=4))
BITS=tuple(product((0,1),repeat=9))
TARGETS=[f"A{i}" for i in range(1,7)]+["X","C"]


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [serial(v) for v in x]
    return x


def save(name,obj):
    (P/name).write_text(json.dumps(serial(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ev(line,point): return F(line[0])+F(line[1])*point[0]+F(line[2])*point[1]
def vector_hash(values): return hashlib.sha256(("\n".join(str(F(x)) for x in values)+"\n").encode()).hexdigest()


def weights(mode,s,delta,h):
    q0=F(1,6 if mode=="pure" else 5)
    x=F(5977,6912)-delta
    y=F(43,48)+delta
    original=(q0/2+q0*x/12+q0*y/6,q0/2+x+q0*y/6,q0/2+y)
    actual=(original[0]-h,original[1],original[2])
    return dict(q0=q0,tau=(F(0),x,y),original=original,actual=actual,
                source_ic=25+x+y-s,S=1+sum(actual))


def cost(w,p,t,q,r):
    r3,r4,r5,z=r
    L=p+t+r3+r4+r5+z
    numerator=w["source_ic"]*t-z-w["tau"][1]*r4-w["tau"][2]*r5
    assert L or not numerator
    return ((numerator/L if L else F(0))+sum(w["actual"][j]*r[j] for j in range(3))+z
            +q/(p+t+r3+r4+r5+1)+w["tau"][1]*q/(p+t+r3+3)
            +w["tau"][2]*q/(p+t+r3+r4+2))


def point_costs(sl,vertex):
    mode,s=sl["mode"],F(sl["s"])
    delta,h=map(F,vertex["point"])
    w=weights(mode,s,delta,h)
    out=[]
    mm={}
    for c in sl["conditions"]:
        p,t,n=c["p"],c["t"],c["n"]
        q=F(n,6) if mode=="pure" else F(n-t,5)
        values={"".join(map(str,r)):cost(w,p,t,q,r) for r in TAILS}
        m=min(values.values())
        active=[r for r,z in values.items() if z==m]
        old=vertex["conditions"][c["key"]]
        assert m==F(old["value"]) and active==old["tails"]
        out.append(dict(key=c["key"],p=p,t=t,n=n,q=q,costs=values,minimum=m,all_weak_tails=active))
        mm[(p,t,n)]=m
    ff={}
    gg={}
    gd={}
    if mode=="ordered":
        for p in (0,1):
            ff[p]={}
            for d in range(7):
                value=F(0)
                if d<6: value+=F(6-d,6)*mm[(p,0,d)]
                if d>0: value+=F(d,6)*mm[(p,1,d)]
                ff[p][d]=value
            gg[p]=min(ff[p][d] for d in range(1,7))
            gd[p]=[d for d in range(1,7) if ff[p][d]==gg[p]]
            assert ff[p][0]==0 and gd[p]==[1]
    return w,out,mm,ff,gg,gd


def vector(w,mode,s,kind,target,mm,gg):
    mu=w["S"]-s/5 if kind=="C-only" else F(0)
    if mode=="pure":
        target_col=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
    result=[]
    for bits in BITS:
        actual=F(bits[1],sum(bits[:6])) if sum(bits[:6]) else F(0)
        projected=mm[(bits[0],bits[target_col],bits[7])] if mode=="pure" else bits[7]*gg[bits[0]]
        result.append(w["source_ic"]*actual-projected+mu*bits[8])
    result.append(w["S"]-mu)
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-package",type=Path,default=DEFAULT_SOURCE)
    ap.add_argument("--source-repo",type=Path,default=DEFAULT_REPO)
    args=ap.parse_args()
    assert not (P/"freeze_manifest.json").exists(),"Frozen: replay in a separate copy."
    src=args.source_package
    assert sha(src/"freeze_manifest.json")==EXPECTED_MANIFEST
    manifest=json.loads((src/"freeze_manifest.json").read_text())
    assert manifest["status"]=="FROZEN-PASS"
    for rec in manifest["files"]:
        assert sha(src/rec["path"])==rec["sha256"]
    geometry=json.loads((src/"exact_envelopes_2d.json").read_text())
    recipe_bytes=(src/"row_recipe.json").read_bytes()
    recipe=json.loads(recipe_bytes)
    recipes={r["slice_id"]:r for r in recipe["parameters"]}
    (P/"bound_row_recipe.json").write_bytes(recipe_bytes)
    rel=Path("research/workspaces/six-boss1-20261111")
    old_paths={"cap3_186":args.source_repo/rel/"source2_cap3_tradeoff/exact_family.json",
               "delta_180":args.source_repo/rel/"source2_conditional_redistribution/exact_family.json"}
    binding=dict(run="six-boss1-20261111",boss="Boss1",agent_id="/root/source2_cap3_tradeoff",
                 two_dimensional_package=dict(path=str(src),freeze_manifest_sha256=sha(src/"freeze_manifest.json"),
                     SHA256SUMS_sha256=sha(src/"SHA256SUMS"),proof_sha256=sha(src/"proof.md"),
                     envelopes_sha256=sha(src/"exact_envelopes_2d.json"),recipe_sha256=sha(src/"row_recipe.json"),
                     all_manifest_files_verified=len(manifest["files"])),
                 previous_families={k:dict(path=str(path),sha256=sha(path)) for k,path in old_paths.items()},
                 source_access="read-only",optimization_calls=0,LP_point_inputs_read=0)
    save("source_binding.json",binding)
    save("coordinate_contract.json",dict(bits=[f"a{i}" for i in range(1,7)]+["x","o","c"],
         columns=["".join(map(str,z)) for z in BITS]+["K"],customer_count=512,K_column=512,total=513,
         order="lexicographic, 0 before 1",actual_u2="a2/(a1+...+a6); zero actual load gives zero",
         inequality="dot(row.a,coordinates)>=0",raw_scale=True,numerical_divisor="25",
         divisor_applied=False,source_IC="each row.real_budget.source_IC, not 25"))
    rows=[]
    registry=[]
    tables=[]
    for sl in geometry["slices"]:
        mode,s=sl["mode"],F(sl["s"])
        spec=recipes[sl["id"]]
        slice_header={k:sl[k] for k in ("id","mode","s","q0","domain_vertices","domain_constraints","B_affine","internal_boundary_lines")}
        for vertex in sl["vertices"]:
            vid=vertex["id"]
            delta,h=map(F,vertex["point"])
            key=f"{sl['id']}:v{vid}"
            w,conditions,mm,ff,gg,gd=point_costs(sl,vertex)
            assert w["source_ic"]==ev(spec["source_IC_affine"],(delta,h))
            assert w["S"]==ev(spec["S_affine"],(delta,h))
            assert all(w["actual"][j]==ev(spec["intermediate_CAP_affines"][str(j+3)],(delta,h)) for j in range(3))
            assert all(w["tau"][j]==ev(spec["internal_SAFE_affines"][str(j+3)],(delta,h)) for j in range(3))
            isolated=[dict(condition=c["key"],tail=r["tail"]) for c in sl["conditions"] for r in c["states"]
                      if r["weak_region_dimension"]==0 and r["weak_region_vertices"]==[vertex["point"]]]
            registry.append(dict(vertex_key=key,source_slice_header=slice_header,source_vertex_record=vertex,
                source_cell_ids=[c["id"] for c in sl["cells"] if vid in c["vertices"]],
                source_edge_ids=[e["id"] for e in sl["edges"] if vid in e["vertices"]],
                isolated_weak_states=isolated,source_bundle_manifest_sha256=EXPECTED_MANIFEST))
            tables.append(dict(vertex_key=key,source_slice_id=sl["id"],source_vertex_id=vid,mode=mode,
                s=s,delta=delta,h=h,q0=w["q0"],conditions=conditions,f=ff,G=gg,G_active_d=gd))
            specs=[("general",t) for t in TARGETS]+[("C-only","C")] if mode=="pure" else [("ordered",None)]
            for kind,target in specs:
                mu=w["S"]-s/5 if kind=="C-only" else F(0)
                coefficients=vector(w,mode,s,kind,target,mm,gg)
                rows.append(dict(id=f"cap3full_{sl['id']}_v{vid}_{kind}_{target or 'menu'}",
                    family="source2_cap3_full_delta_vertices",run="six-boss1-20261111",boss="Boss1",
                    agent_id="/root/source2_cap3_tradeoff",slice_id=sl["id"],source_vertex_id=vid,vertex_key=key,
                    source_bundle_manifest_sha256=EXPECTED_MANIFEST,
                    source_envelopes_sha256=binding["two_dimensional_package"]["envelopes_sha256"],
                    source_row_recipe_sha256=binding["two_dimensional_package"]["recipe_sha256"],
                    mode=mode,row_kind=kind,target=target,source=2,delta=delta,h=h,s=s,q0=w["q0"],
                    tau={str(j+3):x for j,x in enumerate(w["tau"])},
                    beta_original={str(j+3):x for j,x in enumerate(w["original"])},
                    beta_actual={str(j+3):x for j,x in enumerate(w["actual"])},
                    real_budget=dict(source_IC=w["source_ic"],intermediate_CAP={str(j+3):x for j,x in enumerate(w["actual"])},
                        terminal_CAP=F(1),terminal_BR=F(1),internal_SAFE={str(j+3):x for j,x in enumerate(w["tau"])},
                        outer_average=F(1,6) if mode=="ordered" else None,inner_query_average=w["q0"]),
                    raw_K=w["S"],K=w["S"]-mu,free_EC=mu,equality_definition="E_C=sum_x c_x-K=0",
                    numerical_divisor=F(25),divisor_applied=False,column_count=513,raw_scale=True,
                    customer_formula="a*actual_u2-m(p,t,o/6)+free_EC*c" if mode=="pure" else "a*actual_u2-o*G(p)",
                    vector_sha256=vector_hash(coefficients),a=coefficients))
    assert len(rows)==585 and len(registry)==225 and sum(len(r["isolated_weak_states"]) for r in registry)==9
    save("exact_family.json",dict(schema="source2-cap3-full-delta-585x513-v1",source_bundle_manifest_sha256=EXPECTED_MANIFEST,
                                  original_scale=True,row_count=585,column_count=513,rows=rows))
    save("vertex_registry.json",dict(source_binding="source_binding.json",records=registry))
    save("vertex_cost_tables.json",dict(derivation="direct all-16-state actual COST at each source vertex",vertices=tables))
    previous={}
    for name,path in old_paths.items():
        old=json.loads(path.read_text())["rows"]
        assert len(old)==(186 if name=="cap3_186" else 180)
        ix={}
        for pos,r in enumerate(old):
            key=tuple(F(x) for x in r["a"])
            ix.setdefault(key,[]).append(dict(id=r.get("id"),position=pos))
        previous[name]=ix
    comparisons=[]
    internal={}
    for row in rows:
        key=tuple(row["a"])
        internal.setdefault(key,[]).append(row["id"])
        comparisons.append(dict(row_id=row["id"],vertex_key=row["vertex_key"],h=row["h"],
                                matches={name:ix.get(key,[]) for name,ix in previous.items()}))
    duplicates=[dict(vector_sha256=vector_hash(key),row_ids=ids) for key,ids in internal.items() if len(ids)>1]
    compare_summary={name:sum(bool(rec["matches"][name]) for rec in comparisons) for name in previous}
    save("literal_coincidences.json",dict(definition="Equality of every one of 513 original-scale coefficients; no rows removed.",
        previous_families=binding["previous_families"],matched_record_counts=compare_summary,
        matched_any_previous=sum(any(rec["matches"].values()) for rec in comparisons),
        internal_distinct_vectors=len(internal),internal_duplicate_groups=duplicates,comparisons=comparisons,
        cone_status="No general-T or ordered cone-redundancy decision is inferred from literal comparisons."))
    summary=dict(source_vertex_records=225,rows=585,columns_per_row=513,total_coefficient_records=585*513,
        kind_counts={kind:sum(r["row_kind"]==kind for r in rows) for kind in ("general","C-only","ordered")},
        h0_rows=sum(r["h"]==0 for r in rows),positive_h_rows=sum(r["h"]>0 for r in rows),
        raw_tail_cost_records=sum(16*len(t["conditions"]) for t in tables),
        isolated_weak_state_records=sum(len(r["isolated_weak_states"]) for r in registry),
        per_slice=[dict(slice_id=sl["id"],vertex_count=len(sl["vertices"]),row_count=sum(r["slice_id"]==sl["id"] for r in rows)) for sl in geometry["slices"]],
        previous_literal_matches=compare_summary,matched_any_previous=sum(any(r["matches"].values()) for r in comparisons),
        internal_distinct_vectors=len(internal),internal_duplicate_groups=len(duplicates),rows_deleted=0,
        source_bundle_manifest_sha256=EXPECTED_MANIFEST)
    save("materialization_summary.json",summary)
    assert sha(src/"freeze_manifest.json")==EXPECTED_MANIFEST
    assert all(sha(old_paths[name])==rec["sha256"] for name,rec in binding["previous_families"].items())
    print(json.dumps(serial(summary),ensure_ascii=False,indent=2))


if __name__=="__main__":
    try: main()
    except BaseException as exc:
        path=P/"failure_log.json"
        data=json.loads(path.read_text()) if path.exists() else []
        data.append(dict(stage="materialize",type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
        save("failure_log.json",data)
        raise
