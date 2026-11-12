#!/usr/bin/env python3
"""Build every original-scale row and every physical local minimum.

The finite row family retains all closed-window occurrences, all old rows,
all zero entries, all nine-bit columns, and every weak-tie tail.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib
import json

from derive_geometry import HERE, ROOT, WS, dump, weights, actual_cost, anchor, affine, primitive, pin_sources


def load(name):
    return json.loads((HERE / name).read_text())


def zvalue(i, q0, x, p):
    tau, _, _, _ = weights(i,q0,x)
    return q0 * (F(1,p+1) + sum((v/F(p+7-j) for j,v in tau.items()),F(0)))


def six_minimum(i, q0, x, p, t, o):
    tau, _, _, _ = weights(i,q0,x)
    return t*anchor(i,q0,x,p) + F(o,6*(p+1+(6-i)*t)) + sum((v*F(o,6*(p+(j-i)*t+7-j)) for j,v in tau.items()),F(0))


def affine_checks():
    out, counts = [], defaultdict(int)
    for i in (3,4,5):
        m, dim = 5-i, 6-i
        for q0 in (F(1,6),F(1,5)):
            for p in range(i):
                for r in product((0,1),repeat=6-i):
                    for q in (F(0),q0):
                        h=affine(lambda x: actual_cost(i,q0,x,p,0,q,r) - (zvalue(i,q0,x,p) if q else 0),dim)
                        assert h[-1]==0 and all(v>=0 for v in h[:-1])
                        out.append(dict(kind="t0_all_nonnegative_tau",source=i,q0=str(q0),p=p,q=str(q),tail=list(r),form=list(map(str,h))))
                        counts["t0_affine_quadrant_checks"]+=1
                    h=affine(lambda x: actual_cost(i,q0,x,p,1,F(1),r)-actual_cost(i,q0,x,p,1,F(0),r)
                             -(1+sum(x[:-1],F(0)))/F(p+7-i),dim)
                    assert h[-1]==0 and all(v>=0 for v in h[:-1])
                    out.append(dict(kind="t1_query_slope",source=i,q0=str(q0),p=p,tail=list(r),form=list(map(str,h))))
                    counts["t1_query_slope_checks"]+=1
            for j in range(i+1,6):
                # Free beta coordinates first, then tau, lambda. Recover the
                # one-middle-member necessity without substituting minimal hats.
                js=list(range(i+1,6)); k=js.index(j)
                def free_residual(y):
                    beta=dict(zip(js,y[:m])); tau=dict(zip(js,y[m:2*m]))
                    source=F(0)
                    actual=source-tau[j]
                    caps=beta[j]
                    query=q0/F(2)+sum((tau[l]*q0/F(7-l+(1 if j<l else 0)) for l in js),F(0))
                    zero=q0*(1+sum((tau[l]/F(7-l) for l in js),F(0)))
                    return actual+caps+query-zero
                h=affine(free_residual,2*m+1)
                expected=[-q0/2]+[F(l==j) for l in js]+[-F(l==j)-(q0/F((7-l)*(8-l)) if l>j else 0) for l in js]+[F(0)]
                assert list(h)==expected
                out.append(dict(kind="free_cap_necessity",source=i,q0=str(q0),middle_source=j,coordinate_order=[f"beta{l}" for l in js]+[f"tau{l}" for l in js]+["lambda"],form=list(map(str,h))))
                counts["free_cap_necessity_checks"]+=1
    # Source 5 is handled at the true minimum, not by W-Z (which can be negative).
    for p in range(5):
        for d in range(2,7):
            def f(dd, ww):
                return F(dd,6)*ww + F(dd*(6-dd),30*(p+1)) + F(dd*(dd-1),30*(p+2))
            for ww in (F(0),F(1)):
                left=f(d,ww)-f(1,ww)
                endpoint=F(5,6)*ww+F(1,p+2)-F(1,6*(p+1))
                right=F(d-1,5)*endpoint+F((d-1)*(6-d),30*(p+1)*(p+2))
                assert left==right and endpoint>0 and left>0
            out.append(dict(kind="source5_strict_multiplicity_identity",p=p,d=d,
                            affine_in_w=[str(f(d,F(0))-f(1,F(0))),str(F(d-1,6))],
                            positive_chord_correction=str(F((d-1)*(6-d),30*(p+1)*(p+2)))))
            counts["source5_continuous_multiplicity_identities"]+=1
    dump("analytic_state_checks.json",out)
    return counts


def old_source_data():
    out={}
    for qd,pkg in [(6,"all_source_minimal_cap_safe"),(5,"ordered_minimal_cap")]:
        family=json.loads((ROOT/WS/pkg/"exact_family.json").read_text())
        rows={}
        for row in family["rows"]:
            i=row["source"]
            if i not in (3,4,5):
                continue
            td=row["tau_by_true_source" if qd==6 else "tau_by_source"]
            x=tuple(F(td[str(j)]) for j in range(i+1,6))+(25-F(row["s"]),)
            key=(i,x,row["forced_target"] if qd==6 else "ORDERED")
            assert key not in rows
            rows[key]=row
        ds=json.loads((ROOT/WS/pkg/"parameter_domains.json").read_text())
        domains=ds["sources" if qd==6 else "domains"]
        selected={d["source"]:d for d in domains if d["source"] in (3,4,5)}
        out[qd]=dict(package=pkg,rows=rows,domains=selected)
    return out


def main():
    pins=load("source_pins.json")
    assert pins==pin_sources()
    cells=load("parameter_domains.json")["cells"]
    counts=affine_checks()
    old=old_source_data()
    types=list(product((0,1),repeat=9))
    dump("coordinate_contract.json",dict(bit_order=["a1","a2","a3","a4","a5","a6","x","o","c"],
         customer_columns=[dict(index=k,bits=list(b)) for k,b in enumerate(types)],K_column=512,total_columns=513,
         column_order="lexicographic all nine-bit tuples, then independent K",zero_load_share="0",all_zero_and_repeated_columns_retained=True))
    minimums=[]; outers=[]; pure_menus=[]; ordered_menus=[]
    all_rows=[]; old_checks=[]; domain_identities=[]; low_checks=[]
    menu_bits=list(product((0,1),repeat=6))
    dump("menu_index_contract.json",dict(outer_indices=[1,2,3,4,5,6],pure_inner_indices=[1,2,3,4,5,6],
         ordered_exclusion="same index, not same label",patterns=[dict(mask="".join(map(str,b)),bits=list(b),d=sum(b)) for b in menu_bits],
         physical_ordered_pairs=[dict(d=d,t=t,q=str(F(d-t,5))) for d in range(7) for t in (0,1) if (t==0 and d<6) or (t==1 and d>0)]))
    for cell in cells:
        i,q0=cell["source"],F(cell["q0"])
        qd=q0.denominator
        js=list(range(i+1,6)); m=len(js)
        if cell["old_window"]:
            olddom=old[qd]["domains"][i]
            oldverts={tuple(map(F,v["parameters"][:-1]))+(25-F(v["parameters"][-1]),) for v in olddom["vertices"]}
            hereverts={tuple(map(F,v["coordinates"])) for v in cell["vertices"]}
            assert oldverts==hereverts
            old_forms=[]
            for h in olddom["complete_domain_halfspaces" if qd==6 else "facets"]:
                if qd==6:
                    c=F(h["constant"]); cc=list(map(F,h["coefficients"]))
                else:
                    c=F(h["rhs"]); cc=[-F(v) for v in h["normal"]]
                old_forms.append(primitive(tuple([c+25*cc[-1]]+cc[:-1]+[-cc[-1]]))[0])
            hereforms={tuple(h["primitive_form"]) for h in cell["facets"]}
            assert set(old_forms)==hereforms
            domain_identities.append(dict(cell=cell["id"],old_package=old[qd]["package"],substitution="s=25-lambda",
                                          exact_facet_set_identity=True,exact_vertex_set_identity=True,
                                          facets=cell["facet_count"],vertices=cell["vertex_count"]))
        if i in (3,4) and cell["window"][0]=="0":
            expected=[]
            for k,j in enumerate(js):
                h=[F(0)]*(m+2);h[k+1]=F(1);expected.append(primitive(tuple(h))[0])
                h=[-q0/2]+[-F(3,4) if l==j else -(q0/F((7-l)*(8-l))) if l>j else F(0) for l in js]+[F(1,20)]
                expected.append(primitive(tuple(h))[0])
            expected.append(primitive(tuple([F(cell["window"][1])]+[F(0)]*m+[F(-1)]))[0])
            assert set(expected)=={tuple(h["primitive_form"]) for h in cell["facets"]}
            assert min(F(v["lambda_value"]) for v in cell["vertices"])==10*q0
            low_checks.append(dict(cell=cell["id"],conjecture_exact=True,minimum_lambda=str(10*q0),vertices=cell["vertex_count"],facets=cell["facet_count"]))
        for vertex in cell["vertices"]:
            x=tuple(map(F,vertex["coordinates"])); tau,beta,a,S=weights(i,q0,x); B=S-1
            assert a>=0 and all(v>0 for v in beta.values())
            if qd==5 and i in (3,4):
                assert x[-1]>=2
            tables={}
            tails=list(product((0,1),repeat=6-i))
            for p in range(i):
                pairs=[(t,F(d,6)) for t in (0,1) for d in range(7)] if qd==6 else [(t,F(d-t,5)) for d in range(7) for t in (0,1) if (t==0 and d<6) or (t==1 and d>0)]
                for t,q in pairs:
                    costs=[actual_cost(i,q0,x,p,t,q,r) for r in tails]
                    low=min(costs); att=[list(r) for r,c in zip(tails,costs) if c==low]
                    if t==1:
                        expected=anchor(i,q0,x,p)+(1+sum(tau.values(),F(0)))*q/F(p+7-i)
                        assert low==expected
                    if t==0 and q in (F(0),q0):
                        assert low==(zvalue(i,q0,x,p) if q else 0)
                    if i==5 and t==0:
                        assert low==q/F(p+1)
                    tab=dict(cell=cell["id"],vertex_id=vertex["id"],p=p,t=t,q=str(q),minimum=str(low),
                             all_attaining_tails=att,states=[dict(tail=list(r),cost=str(c),gap=str(c-low)) for r,c in zip(tails,costs)])
                    minimums.append(tab);tables[p,t,q]=tab
                    counts["physical_minimum_tables"]+=1;counts["physical_hidden_state_costs"]+=len(costs)
                    counts["weak_tie_attainer_occurrences"]+=len(att)
                    counts["maximum_attainer_count"]=max(counts["maximum_attainer_count"],len(att))
                if qd==6:
                    for t in (0,1):
                        checks=[]
                        for mb in menu_bits:
                            d=sum(mb);o=int(d>0)
                            actual=F(tables[p,t,F(d,6)]["minimum"])
                            weak=F(tables[p,t,F(o,6)]["minimum"])
                            assert weak==six_minimum(i,q0,x,p,t,o) and actual>=weak
                            checks.append(dict(mask="".join(map(str,mb)),d=d,o=o,actual_query_mean=str(F(d,6)),actual_minimum=str(actual),
                                               union_minimum=str(weak),gap=str(actual-weak)))
                        pure_menus.append(dict(cell=cell["id"],vertex_id=vertex["id"],p=p,t=t,patterns=checks))
                        counts["all_64_pure_menu_contexts"]+=64
                else:
                    W=anchor(i,q0,x,p);Z=zvalue(i,q0,x,p);G=(5*Z+W)/6
                    if i in (3,4):
                        lower=F(1,5)+F(m,10)+F(9,10)*sum(tau.values(),F(0))
                        assert W-Z>=lower>0
                    f={}
                    for d in range(7):
                        vv=F(0)
                        if d<6:vv+=F(6-d,6)*F(tables[p,0,F(d,5)]["minimum"])
                        if d>0:vv+=F(d,6)*F(tables[p,1,F(d-1,5)]["minimum"])
                        f[d]=vv;gap=vv-int(d>0)*G
                        assert gap>=0 and (d<=1 or gap>0)
                        assert (d!=1 or vv==G) and (d!=0 or vv==0)
                        outers.append(dict(cell=cell["id"],vertex_id=vertex["id"],p=p,d=d,value=str(vv),G=str(G),gap=str(gap),W_minus_Z=str(W-Z)))
                        counts["ordered_multiplicity_checks"]+=1
                    checks=[]
                    for mb in menu_bits:
                        d=sum(mb);averaged=F(0);inner=[]
                        for k,t in enumerate(mb):
                            q=sum((F(mb[l],5) for l in range(6) if l!=k),F(0))
                            assert q==F(d-t,5)
                            v=F(tables[p,t,q]["minimum"])
                            averaged+=v/6
                            inner.append(dict(outer_index=k+1,t=t,actual_five_mean=str(q),minimum=str(v)))
                        assert averaged==f[d]
                        checks.append(dict(mask="".join(map(str,mb)),d=d,inner=inner,outer_mean=str(averaged),gap=str(averaged-int(d>0)*G)))
                    ordered_menus.append(dict(cell=cell["id"],vertex_id=vertex["id"],p=p,G=str(G),patterns=checks))
                    counts["all_64_ordered_menu_contexts"]+=64;counts["actual_inner_five_means"]+=64*6
            kinds=[("six_general",t) for t in ["A1","A2","A3","A4","A5","A6","X","C"]]+[("six_C_only","C")] if qd==6 else [("ordered","ORDERED")]
            for kind,target in kinds:
                co=[]
                for bits in types:
                    p=sum(bits[:i-1]); actual_load=sum(bits[:6]);u=F(bits[i-1],actual_load) if actual_load else F(0);o=bits[7]
                    if kind=="ordered":
                        G=(5*zvalue(i,q0,x,p)+anchor(i,q0,x,p))/6
                        v=a*u-o*G
                    else:
                        ti=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
                        t=bits[ti]
                        v=a*u-six_minimum(i,q0,x,p,t,o)+(B*bits[8] if kind=="six_C_only" else 0)
                    co.append(v)
                co.append(F(1) if kind=="six_C_only" else S)
                rid=f"{vertex['id']}_{kind}_{target}"
                row=dict(raw_row_index=len(all_rows),id=rid,cell=cell["id"],vertex_id=vertex["id"],source=i,q0=str(q0),
                         kind=kind,forced_target=target,coordinates=list(map(str,x)),tau_by_true_source={str(j):str(v) for j,v in tau.items()},
                         lambda_value=str(x[-1]),source_IC_weight=str(a),middle_CAP_weights={str(j):str(v) for j,v in beta.items()},
                         terminal_CAP_weight="1",terminal_query_average_weight="1",K_weight=str(co[-1]),
                         free_C_equality_multiplier=str(B) if kind=="six_C_only" else "0",numeric_positive_divisor="25",
                         old_window_occurrence=cell["old_window"],old_parameter=x[-1]>=16,
                         raw_parameter_occurrences_retained=True,a={str(k):str(v) for k,v in enumerate(co)},rhs="0")
                all_rows.append(row)
                if x[-1]>=16:
                    oldkey=(i,x,"ORDERED" if kind=="ordered" else target)
                    oldrow=old[qd]["rows"][oldkey]
                    diffs=[]
                    for k,v in enumerate(co):
                        previous=F(oldrow["a"][str(k)])
                        correction=B*(F(types[k][8]) if k<512 else F(-1)) if kind=="six_C_only" else F(0)
                        diffs.append(v-previous-correction)
                    assert not any(diffs)
                    old_checks.append(dict(row_id=rid,old_package=old[qd]["package"],old_row_id=oldrow["name"],s=str(25-x[-1]),
                                           free_C_equality_multiplier=str(B) if kind=="six_C_only" else "0",all_513_column_residuals=list(map(str,diffs)),
                                           classification="old family identity; no new-family claim"))
                    counts["old_parameter_row_identities"]+=1;counts["old_parameter_column_identities"]+=513
            print(cell["id"],vertex["id"],"verified",flush=True)
    dump("conditional_minimum_tables.json",minimums)
    dump("outer_average_tables.json",outers)
    dump("all_64_pure_query_checks.json",pure_menus)
    dump("all_64_ordered_menu_checks.json",ordered_menus)
    dump("old_window_domain_identity.json",domain_identities)
    dump("old_row_column_identities.json",old_checks)
    dump("low_segment_conjecture_checks.json",low_checks)
    exact_groups=defaultdict(list)
    for row in all_rows:
        digest=hashlib.sha256(json.dumps(row["a"],sort_keys=True,separators=(",",":")).encode()).hexdigest()
        exact_groups[digest].append(row["id"])
    dump("row_occurrences.json",dict(raw_rows=len(all_rows),distinct_exact_vectors=len(exact_groups),
         all_duplicates_retained=True,groups=[dict(coefficient_sha256=k,row_ids=v) for k,v in exact_groups.items()]))
    dump("exact_family.json",dict(schema="later-source-anchor-cells-full-raw-family/v1",status="EXACT_GENERATED",rows=all_rows,
         raw_rows=len(all_rows),columns=513,K_column=512,numerical_positive_divisor="25",inequality="sum(a[column]*column) >= 0",
         optimizer_calls=0,global_LP_inputs_or_points_read=False,current_3056_plan_modified=False,
         no_row_pruning=True,old_window_identity_only=True))
    dump("row_catalog.json",[{k:v for k,v in r.items() if k!="a"} for r in all_rows])
    counts.update(rows=len(all_rows),full_columns=len(all_rows)*513,distinct_exact_row_vectors=len(exact_groups),
                  old_window_rows=sum(r["old_window_occurrence"] for r in all_rows),new_parameter_raw_occurrences=sum(not r["old_parameter"] for r in all_rows),
                  all_source_pins_unchanged=int(pins==pin_sources()))
    assert counts["all_source_pins_unchanged"]
    dump("family_generator_output.json",dict(status="PASS",counts=dict(counts),optimizer_calls=0))
    print(json.dumps(dict(counts),ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
