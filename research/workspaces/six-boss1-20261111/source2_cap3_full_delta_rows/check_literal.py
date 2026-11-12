#!/usr/bin/env python3
"""Independent all-16-state, individual-share and full-column checker.

Imports no materializer or prior project program.  Every coefficient is
reconstructed in Fraction from the physical cost, including the independent K.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import traceback

P=Path(__file__).resolve().parent
TAILS=tuple(product((0,1),repeat=4))
CLIENTS=tuple(product((0,1),repeat=9))
TARGETS=[f"A{i}" for i in range(1,7)]+["X","C"]
COUNTS={}


def count(key,n=1): COUNTS[key]=COUNTS.get(key,0)+n
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name,obj):
    def ser(x):
        if isinstance(x,Q): return str(x)
        if isinstance(x,dict): return {str(k):ser(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)): return [ser(v) for v in x]
        return x
    (P/name).write_text(json.dumps(ser(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def vector_sha(values): return hashlib.sha256(("\n".join(str(Q(x)) for x in values)+"\n").encode()).hexdigest()


def budget(mode,s,delta,h):
    q0=Q(1,6) if mode=="pure" else Q(1,5)
    tau={3:Q(0),4:Q(5977,6912)-delta,5:Q(43,48)+delta}
    caps={j:q0/2+tau[j]+sum((q0*tau[k]/((7-k)*(8-k)) for k in range(j+1,6)),Q(0)) for j in range(3,6)}
    original=dict(caps)
    caps[3]-=h
    a=25+sum(tau.values())-s
    return a,caps,tau,1+sum(caps.values()),q0,original


@lru_cache(None)
def payment(mode,s,delta,h,p,t,q,tail):
    a,caps,tau,S,q0,original=budget(mode,s,delta,h)
    r3,r4,r5,z=tail
    load=p+t+sum(tail)
    shares=[Q(member,load) if load else Q(0) for member in (t,r3,r4,r5,z)]
    source=a*shares[0]
    subtract_last=shares[4]
    subtract_safe=sum(tau[j]*shares[j-2] for j in range(3,6))
    caps_paid=sum(caps[j]*tail[j-3] for j in range(3,6))+z
    last_query=q/Q(p+t+r3+r4+r5+1)
    safe_queries=sum(tau[j]*q/Q(p+t+sum(tail[:j-3])+7-j) for j in range(3,6))
    return source-subtract_last-subtract_safe+caps_paid+last_query+safe_queries


@lru_cache(None)
def m(mode,s,delta,h,p,t,q):
    values=[payment(mode,s,delta,h,p,t,q,tail) for tail in TAILS]
    minimum=min(values)
    active=tuple("".join(map(str,tail)) for tail,z in zip(TAILS,values) if z==minimum)
    return minimum,active


@lru_cache(None)
def f(mode,s,delta,h,p,d):
    assert mode=="ordered"
    value=Q(0)
    if d<6: value+=Q(6-d,6)*m(mode,s,delta,h,p,0,Q(d,5))[0]
    if d>0: value+=Q(d,6)*m(mode,s,delta,h,p,1,Q(d-1,5))[0]
    return value


@lru_cache(None)
def full_vector(mode,s,delta,h,kind,target):
    a,caps,tau,S,q0,original=budget(mode,s,delta,h)
    mu=S-s/5 if kind=="C-only" else Q(0)
    if mode=="pure":
        index=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
        minima={(p,t,o):m(mode,s,delta,h,p,t,Q(o,6))[0] for p,t,o in product((0,1),repeat=3)}
    else:
        G={p:min(f(mode,s,delta,h,p,d) for d in range(1,7)) for p in (0,1)}
    values=[]
    for c in CLIENTS:
        actual_share=Q(c[1],sum(c[:6])) if sum(c[:6]) else Q(0)
        rhs=minima[(c[0],c[index],c[7])] if mode=="pure" else c[7]*G[c[0]]
        values.append(a*actual_share-rhs+mu*c[8])
    return tuple(values+[S-mu])


def metadata(row,sl,vertex,binding):
    mode,s,delta,h=sl["mode"],Q(sl["s"]),Q(vertex["point"][0]),Q(vertex["point"][1])
    a,caps,tau,S,q0,original=budget(mode,s,delta,h)
    assert row["slice_id"]==sl["id"] and row["source_vertex_id"]==vertex["id"]
    assert row["vertex_key"]==f"{sl['id']}:v{vertex['id']}"
    assert row["source"]==2 and row["run"]=="six-boss1-20261111" and row["boss"]=="Boss1"
    assert row["agent_id"]=="/root/source2_cap3_tradeoff"
    assert (Q(row["delta"]),Q(row["h"]),Q(row["s"]),Q(row["q0"]))==(delta,h,s,q0)
    assert row["mode"]==mode and row["column_count"]==513 and row["raw_scale"] is True
    assert Q(row["numerical_divisor"])==25 and row["divisor_applied"] is False
    assert a!=25 and a>0 and min(caps.values())>=0 and min(tau.values())>=0
    for field,expected in (("tau",tau),("beta_original",original),("beta_actual",caps)):
        assert {int(j):Q(z) for j,z in row[field].items()}==expected
    real=row["real_budget"]
    assert Q(real["source_IC"])==a
    assert {int(j):Q(z) for j,z in real["intermediate_CAP"].items()}==caps
    assert {int(j):Q(z) for j,z in real["internal_SAFE"].items()}==tau
    assert Q(real["terminal_CAP"])==Q(real["terminal_BR"])==1
    assert Q(real["inner_query_average"])==q0
    assert real["outer_average"] is None if mode=="pure" else Q(real["outer_average"])==Q(1,6)
    mu=S-s/5 if row["row_kind"]=="C-only" else Q(0)
    assert Q(row["free_EC"])==mu and Q(row["raw_K"])==S and Q(row["K"])==S-mu
    src=binding["two_dimensional_package"]
    assert row["source_bundle_manifest_sha256"]==src["freeze_manifest_sha256"]
    assert row["source_envelopes_sha256"]==src["envelopes_sha256"]
    assert row["source_row_recipe_sha256"]==src["recipe_sha256"]
    count("complete_row_metadata_checks")


def main():
    assert not (P/"freeze_manifest.json").exists(),"Frozen: replay separately."
    binding=json.loads((P/"source_binding.json").read_text())
    srcinfo=binding["two_dimensional_package"]
    src=Path(srcinfo["path"])
    assert sha(src/"freeze_manifest.json")==srcinfo["freeze_manifest_sha256"]=="bb47717a8dd60995b0c314c5f5801f50612e4e585ca841211f9c98c5a6613e9a"
    source_manifest=json.loads((src/"freeze_manifest.json").read_text())
    assert all(sha(src/r["path"])==r["sha256"] for r in source_manifest["files"])
    for key,file in (("SHA256SUMS_sha256","SHA256SUMS"),("proof_sha256","proof.md"),
                     ("envelopes_sha256","exact_envelopes_2d.json"),("recipe_sha256","row_recipe.json")):
        assert sha(src/file)==srcinfo[key]
    assert (P/"bound_row_recipe.json").read_bytes()==(src/"row_recipe.json").read_bytes()
    geometry=json.loads((src/"exact_envelopes_2d.json").read_text())
    sources={f"{sl['id']}:v{vertex['id']}":(sl,vertex) for sl in geometry["slices"] for vertex in sl["vertices"]}
    assert len(sources)==225
    registry=json.loads((P/"vertex_registry.json").read_text())["records"]
    tables=json.loads((P/"vertex_cost_tables.json").read_text())["vertices"]
    assert len(registry)==len(tables)==225
    table_index={r["vertex_key"]:r for r in tables}
    assert len(table_index)==225 and set(table_index)==set(sources)
    isolated_count=0
    for record in registry:
        key=record["vertex_key"]
        sl,vertex=sources[key]
        assert record["source_vertex_record"]==vertex
        expected_header={k:sl[k] for k in ("id","mode","s","q0","domain_vertices","domain_constraints","B_affine","internal_boundary_lines")}
        assert record["source_slice_header"]==expected_header
        assert record["source_cell_ids"]==[c["id"] for c in sl["cells"] if vertex["id"] in c["vertices"]]
        assert record["source_edge_ids"]==[e["id"] for e in sl["edges"] if vertex["id"] in e["vertices"]]
        isolated=[dict(condition=c["key"],tail=r["tail"]) for c in sl["conditions"] for r in c["states"]
                  if r["weak_region_dimension"]==0 and r["weak_region_vertices"]==[vertex["point"]]]
        assert record["isolated_weak_states"]==isolated
        isolated_count+=len(isolated)
        mode,s=sl["mode"],Q(sl["s"])
        delta,h=map(Q,vertex["point"])
        tab=table_index[key]
        assert tab["source_slice_id"]==sl["id"] and tab["source_vertex_id"]==vertex["id"]
        assert (Q(tab["delta"]),Q(tab["h"]),Q(tab["s"]))==(delta,h,s)
        assert len(tab["conditions"])==len(sl["conditions"])
        for c,tc in zip(sl["conditions"],tab["conditions"]):
            p,t,n=c["p"],c["t"],c["n"]
            q=Q(n,6) if mode=="pure" else Q(n-t,5)
            assert (tc["key"],tc["p"],tc["t"],tc["n"],Q(tc["q"]))==(c["key"],p,t,n,q)
            if mode=="ordered": assert (t==0 and 0<=n<=5) or (t==1 and 1<=n<=6)
            vals={"".join(map(str,r)):payment(mode,s,delta,h,p,t,q,r) for r in TAILS}
            assert vals=={name:Q(z) for name,z in tc["costs"].items()}
            minimum,active=m(mode,s,delta,h,p,t,q)
            assert Q(tc["minimum"])==minimum and tuple(tc["all_weak_tails"])==active
            original=vertex["conditions"][c["key"]]
            assert minimum==Q(original["value"]) and active==tuple(original["tails"])
            count("all_real_tail_cost_checks",16)
            count("complete_vertex_weak_minimum_sets")
        if mode=="pure":
            a,caps,tau,S,q0,old=budget(mode,s,delta,h)
            assert tab["f"]==tab["G"]==tab["G_active_d"]=={}
            for p,t in product((0,1),repeat=2):
                for r in TAILS:
                    slope=Q(1,p+t+sum(r[:3])+1)+sum(tau[j]/Q(p+t+sum(r[:j-3])+7-j) for j in range(3,6))
                    assert slope>0
                    for d in range(7):
                        o=int(d>0)
                        assert payment(mode,s,delta,h,p,t,Q(d,6),r)-payment(mode,s,delta,h,p,t,Q(o,6),r)==Q(d-o,6)*slope>=0
                        count("true_six_query_weakening_identities")
        else:
            for p in (0,1):
                values={d:f(mode,s,delta,h,p,d) for d in range(7)}
                assert values=={int(d):Q(z) for d,z in tab["f"][str(p)].items()}
                assert values[0]==0
                active=[d for d in range(1,7) if values[d]==min(values[e] for e in range(1,7))]
                assert active==tab["G_active_d"][str(p)]==[1]
                assert Q(tab["G"][str(p)])==values[1]
                for d in range(1,6):
                    assert values[d+1]-values[d]>=Q(8567,82944)>0
                    count("strict_adjacent_multiplicity_checks")
                for menu in product((0,1),repeat=6):
                    d=sum(menu)
                    average=sum((m(mode,s,delta,h,p,t,Q(d-t,5))[0] for t in menu),Q(0))/6
                    assert average==values[d]
                    count("all_64_menu_vertex_averages")
        count("complete_source_vertex_metadata_checks")
    assert isolated_count==9
    family=json.loads((P/"exact_family.json").read_text())
    rows=family["rows"]
    assert len(rows)==585 and len({r["id"] for r in rows})==585
    expected_specs={(key,kind,target) for key,(sl,vx) in sources.items()
                    for kind,target in ([("general",t) for t in TARGETS]+[("C-only","C")] if sl["mode"]=="pure" else [("ordered",None)])}
    actual_specs=[(r["vertex_key"],r["row_kind"],r["target"]) for r in rows]
    assert len(expected_specs)==len(actual_specs)==585 and set(actual_specs)==expected_specs
    index={(r["slice_id"],Q(r["delta"]),Q(r["h"]),r["row_kind"],r["target"]):r for r in rows}
    row_reports=[]
    C_records=[]
    h_shift_reports=[]
    for row in rows:
        sl,vertex=sources[row["vertex_key"]]
        mode,s,delta,h=sl["mode"],Q(sl["s"]),Q(row["delta"]),Q(row["h"])
        kind,target=row["row_kind"],row["target"]
        expected=full_vector(mode,s,delta,h,kind,target)
        actual=tuple(Q(x) for x in row["a"])
        assert len(actual)==513 and actual==expected
        assert vector_sha(expected)==row["vector_sha256"]
        metadata(row,sl,vertex,binding)
        count("full_row_coefficient_checks",513)
        baseline=index[(sl["id"],delta,Q(0),kind,target)]
        base=tuple(Q(x) for x in baseline["a"])
        a,caps,tau,S,q0,orig=budget(mode,s,delta,h)
        H=q0*(Q(1,3)+tau[4]/30+tau[5]/12)
        plus=max(Q(0),h-H)
        correction=[]
        if mode=="pure":
            col=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
            for bits in CLIENTS:
                p,t,o=bits[0],bits[col],bits[7]
                z=h*t+h*(1-t)*(1-p)*o+plus*(1-t)*p*o
                if kind=="C-only": z-=h*bits[8]
                correction.append(z)
            correction.append(Q(0) if kind=="C-only" else -h)
        else:
            correction=[bits[7]*(h*(1-bits[0])+bits[0]*(h/6+Q(5,6)*plus)) for bits in CLIENTS]+[-h]
        assert tuple(v-b for v,b in zip(expected,base))==tuple(correction)
        count("full_h_shift_identity_columns",513)
        if kind=="C-only":
            general=index[(sl["id"],delta,h,"general","C")]
            mu=S-s/5
            ec=tuple(Q(bits[8]) for bits in CLIENTS)+(Q(-1),)
            assert expected==tuple(Q(z)+mu*e for z,e in zip(general["a"],ec))
            assert all(z>=0 for z in correction) and correction[512]==0
            C_records.append(dict(row_id=row["id"],baseline_row_id=baseline["id"],slice_id=sl["id"],delta=delta,h=h,H6=H,
                free_EC=mu,K=s/5,identity_columns=513,
                nonnegative_remainder=[dict(column=i,value=z) for i,z in enumerate(correction) if z],
                status="PASS",scope="This row is its same-delta h=0 C-only row plus the displayed nonnegative customer-mass vector."))
            count("C_only_free_equality_columns",513)
            count("C_only_redundancy_columns",513)
        row_reports.append(dict(row_id=row["id"],vertex_key=row["vertex_key"],coefficients_checked=513,
                                vector_sha256=vector_sha(expected),status="PASS"))
        h_shift_reports.append(dict(row_id=row["id"],baseline_row_id=baseline["id"],columns=513,status="PASS"))
    # Independently reconstruct both requested literal-comparison indexes.
    previous={}
    for name,info in binding["previous_families"].items():
        file=Path(info["path"])
        assert sha(file)==info["sha256"]
        old=json.loads(file.read_text())["rows"]
        assert len(old)==(186 if name=="cap3_186" else 180)
        ix={}
        for pos,r in enumerate(old):
            key=tuple(Q(x) for x in r["a"])
            assert len(key)==513
            ix.setdefault(key,[]).append(dict(id=r.get("id"),position=pos))
        previous[name]=ix
    stored_comparisons=json.loads((P/"literal_coincidences.json").read_text())
    old_counts={name:0 for name in previous}
    union_count=0
    internal={}
    for row,stored in zip(rows,stored_comparisons["comparisons"]):
        values=tuple(Q(x) for x in row["a"])
        hits={name:ix.get(values,[]) for name,ix in previous.items()}
        assert stored["row_id"]==row["id"] and stored["matches"]==hits
        for name in previous: old_counts[name]+=bool(hits[name])
        union_count+=any(hits.values())
        internal.setdefault(values,[]).append(row["id"])
        count("old_family_full_vector_comparisons",2)
    assert stored_comparisons["matched_record_counts"]==old_counts
    assert stored_comparisons["matched_any_previous"]==union_count
    assert stored_comparisons["internal_distinct_vectors"]==len(internal)
    expected_duplicate_groups=[dict(vector_sha256=vector_sha(v),row_ids=ids) for v,ids in internal.items() if len(ids)>1]
    assert stored_comparisons["internal_duplicate_groups"]==expected_duplicate_groups
    assert old_counts["delta_180"]==180
    assert len(C_records)==45 and sum(r["h"]==0 for r in C_records)==15 and sum(r["h"]>0 for r in C_records)==30
    for record in C_records:
        baseline=next(row for row in rows if row["id"]==record["baseline_row_id"])
        matches=previous["delta_180"].get(tuple(Q(x) for x in baseline["a"]),[])
        assert matches
        record["baseline_matches_old_delta180"]=matches
    save("independent_row_checks.json",row_reports)
    save("h_shift_identity_checks.json",h_shift_reports)
    save("C_only_redundancy.json",dict(total_C_only_records=45,bottom_records=15,positive_h_records=30,
        rows_deleted=0,global_scope="The frozen two-dimensional theorem pays the whole C-only domain by its 15 old-delta bottom rows and nonnegative customer masses.",
        general_and_ordered_status="No overall-cone redundancy decision is made.",records=C_records))
    save("literal_checker_output.json",dict(status="PASS",counts=COUNTS,rows=585,columns=513,source_vertices=225,
        isolated_weak_state_records_preserved=isolated_count,old_literal_matches=old_counts,
        matched_any_previous=union_count,internal_distinct_vectors=len(internal),duplicate_groups=len(expected_duplicate_groups),
        rows_deleted=0,divisor_applied=False,all_source_metadata_preserved=True,
        source_bundle_manifest_sha256=srcinfo["freeze_manifest_sha256"],source_pins_unchanged=True,
        optimization_calls=0,LP_points_or_faces_read=0))
    if not (P/"failure_log.json").exists(): save("failure_log.json",[])
    print(json.dumps(dict(counts=COUNTS,old_matches=old_counts,matched_any_previous=union_count,
                          distinct_vectors=len(internal),duplicate_groups=len(expected_duplicate_groups)),ensure_ascii=False,indent=2))


if __name__=="__main__":
    try: main()
    except BaseException as exc:
        file=P/"failure_log.json"
        records=json.loads(file.read_text()) if file.exists() else []
        records.append(dict(stage="check_literal",type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
        save("failure_log.json",records)
        raise
