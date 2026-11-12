#!/usr/bin/env python3
"""Independent standard-library verifier.

No generator or project Python module is imported.  True personal shares,
individual indexed queries and cap payments reconstruct the costs.  Geometry
uses bounded-box true-edge clipping, not boundary-intersection enumeration.
Only this package and the nine explicitly pinned mathematical sources are read.
"""
from fractions import Fraction as Rat
from itertools import product, combinations
from pathlib import Path
from collections import defaultdict
from math import gcd
import json
import hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
WS="research/workspaces/six-boss1-20261111"
INPUT_FILES=["source_pins.json","parameter_domains.json","state_halfspaces.json","necessary_facet_witnesses.json",
             "analytic_state_checks.json","conditional_minimum_tables.json","outer_average_tables.json",
             "all_64_pure_query_checks.json","all_64_ordered_menu_checks.json","exact_family.json",
             "coordinate_contract.json","old_row_column_identities.json","row_occurrences.json","family_generator_output.json","inputs.json"]


def read(name):
    return json.loads((HERE/name).read_text())


def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")


def verify_pins():
    pins=read("source_pins.json")
    for p in pins:
        b=(ROOT/p["repository_relative_path"]).read_bytes()
        assert len(b)==p["bytes"] and hashlib.sha256(b).hexdigest()==p["sha256"]
    return len(pins)


def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),Rat(0))


def at(h,v):
    return h[0]+dot(h[1:],v)


def matrix_rank(rows):
    basis={}
    for source in rows:
        row=list(map(Rat,source))
        for pivot in sorted(basis):
            if row[pivot]:
                coeff=row[pivot]
                row=[v-coeff*u for v,u in zip(row,basis[pivot])]
        lead=next((k for k,v in enumerate(row) if v),None)
        if lead is not None:
            coeff=row[lead]
            basis[lead]=[v/coeff for v in row]
    return len(basis)


def normalize(h):
    den=1
    for v in h:
        den=den*v.denominator//gcd(den,v.denominator)
    ints=[int(v*den) for v in h]
    common=0
    for v in ints:
        common=gcd(common,abs(v))
    return tuple(v//common for v in ints) if common else tuple(ints)


def coefficients(fn,dimension):
    origin=(Rat(0),)*dimension
    c=fn(origin)
    v=[c]
    for k in range(dimension):
        point=tuple(Rat(j==k) for j in range(dimension))
        v.append(fn(point)-c)
    return tuple(v)


def budgets(source,qbase,point):
    tau={j:point[j-source-1] for j in range(source+1,6)}
    hats={}
    for j in tau:
        hats[j]=qbase/2+tau[j]
        for ell in tau:
            if ell>j:
                hats[j]+=qbase*tau[ell]/Rat((7-ell)*(8-ell))
    source_weight=point[-1]+sum(tau.values(),Rat(0))
    return tau,hats,source_weight


def literal_cost(source,qbase,point,p,t,q,tail,query_bits=None):
    tau,hats,source_weight=budgets(source,qbase,point)
    total_load=p+t+sum(tail)
    share=lambda present:Rat(present,total_load) if total_load else Rat(0)
    out=source_weight*share(t)
    for k,j in enumerate(tau):
        out-=tau[j]*share(tail[k])
        out+=hats[j]*tail[k]
    out-=share(tail[-1])
    out+=tail[-1]
    terminal_denom=p+t+sum(tail[:-1])+1
    internal_denoms={j:p+t+sum(tail[:k])+7-j for k,j in enumerate(tau)}
    if query_bits is None:
        out+=q/Rat(terminal_denom)
        for j in tau:
            out+=tau[j]*q/Rat(internal_denoms[j])
    else:
        # Actual legal indices, including repetitions; no union surrogate here.
        for present in query_bits:
            out+=Rat(present,len(query_bits)*terminal_denom)
            for j in tau:
                out+=tau[j]*Rat(present,len(query_bits)*internal_denoms[j])
    return out


def clipping(cell,forms):
    d=cell["dimension"]
    low,high=map(Rat,cell["window"])
    upper=Rat(cell["bounded_box_tau_upper"])
    intervals=[(Rat(0),upper)]*(d-1)+[(low,high)]
    vertices=set(product(*intervals))
    processed=[]
    for k,(lo,hi) in enumerate(intervals):
        h=[-lo]+[Rat(0)]*d;h[k+1]=1;processed.append(tuple(map(Rat,h)))
        h=[hi]+[Rat(0)]*d;h[k+1]=-1;processed.append(tuple(map(Rat,h)))
    trace=[]
    for h in forms:
        before=sorted(vertices)
        vals={v:at(h,v) for v in before}
        keep={v for v in before if vals[v]>=0}
        crossings=0
        for u,v in combinations(before,2):
            if vals[u]*vals[v]>=0:
                continue
            common=[g[1:] for g in processed if at(g,u)==0 and at(g,v)==0]
            if matrix_rank(common)!=d-1:
                continue
            crossing=tuple((vals[u]*v[k]-vals[v]*u[k])/(vals[u]-vals[v]) for k in range(d))
            assert at(h,crossing)==0 and all(at(g,crossing)>=0 for g in processed)
            keep.add(crossing);crossings+=1
        assert keep
        vertices=keep;processed.append(h)
        trace.append(dict(primitive_form=list(map(str,h)),before=len(before),after=len(vertices),true_edge_crossings=crossings))
    assert all(all(at(h,v)>=0 for h in forms) for v in vertices)
    return vertices,trace


def verify_geometry(cells,counters):
    raw=read("state_halfspaces.json")["raw"]
    bycell=defaultdict(list)
    for row in raw:
        cid=row["id"].split("_P")[0] if row["kind"]=="true_t1_q0_state" else row["id"].split("_TAU")[0] if row["kind"]=="nonnegative_internal_SAFE_weight" else row["id"].split("_WINDOW")[0]
        bycell[cid].append(row)
    output=[]
    for cell in cells:
        i=cell["source"];q=Rat(cell["q0"]);dim=cell["dimension"];m=dim-1
        observed={(r["p"],tuple(r["tail"])) for r in bycell[cell["id"]] if r["kind"]=="true_t1_q0_state"}
        assert observed=={(p,tail) for p in range(i) for tail in product((0,1),repeat=6-i)}
        assert len(bycell[cell["id"]])==i*2**(6-i)+(5-i)+2
        groups=defaultdict(list)
        for row in bycell[cell["id"]]:
            if row["kind"]=="true_t1_q0_state":
                p=row["p"];tail=tuple(row["tail"]);az=row["anchor_terminal_on_window_interior"]
                full_middle=(1,)*m+(az,)
                fn=lambda x:literal_cost(i,q,x,p,1,Rat(0),tail)-literal_cost(i,q,x,p,1,Rat(0),full_middle)
                h=coefficients(fn,dim)
                assert list(map(str,h))==row["form"]
                assert row["D"]==p+7-i
                assert row["missing_sources"]==[j for k,j in enumerate(range(i+1,6)) if not tail[k]]
                counters["true_affine_rho_states"]+=1
            else:
                h=tuple(map(Rat,row["form"]))
                if row["kind"]=="nonnegative_internal_SAFE_weight":
                    j=int(row["id"].split("_TAU")[1].split("_")[0]);expect=[Rat(0)]*(dim+1);expect[j-i]=Rat(1)
                elif row["id"].endswith("_LOW"):
                    expect=[-Rat(cell["window"][0])]+[Rat(0)]*m+[Rat(1)]
                else:
                    expect=[Rat(cell["window"][1])]+[Rat(0)]*m+[Rat(-1)]
                assert tuple(expect)==h
            key=normalize(h)
            assert list(key)==row["primitive_form"]
            scale=Rat(row["positive_scale_to_primitive"])
            assert all(a==scale*b for a,b in zip(h,key)) and (scale>0 or not any(key))
            groups[key].append(row["id"])
        declared={tuple(g["primitive_form"]):g["raw_ids"] for g in cell["halfspaces"]}
        assert dict(groups)==declared
        forms=[tuple(map(Rat,h)) for h in sorted(groups) if any(h[1:])]
        # The D=6 single-missing, terminal-1 real state supplies this box.
        upper=(Rat(4,5)-q/2)/Rat(4,5)
        assert upper==Rat(cell["bounded_box_tau_upper"])
        for j in range(i+1,6):
            row=next(r for r in bycell[cell["id"]] if r["kind"]=="true_t1_q0_state" and r["D"]==6 and r["missing_sources"]==[j] and r["terminal"]==1)
            expected=[Rat(4,5)-q/2]+[-Rat(4,5) if ell==j else -q/Rat((7-ell)*(8-ell)) if ell>j else Rat(0) for ell in range(i+1,6)]+[Rat(0)]
            assert tuple(map(Rat,row["form"]))==tuple(expected)
            counters["real_state_bounded_box_identities"]+=1
        got,trace=clipping(cell,forms)
        saved={tuple(map(Rat,v["coordinates"])) for v in cell["vertices"]}
        assert got==saved
        counters["independent_clipped_vertex_occurrences"]+=len(got)
        assert matrix_rank([tuple(a-b for a,b in zip(v,next(iter(got)))) for v in got])==dim
        facets=[]
        for h in forms:
            on=[v for v in got if at(h,v)==0]
            r=matrix_rank([tuple(a-b for a,b in zip(v,on[0])) for v in on[1:]]) if on else -1
            if r==dim-1:
                facets.append(normalize(h))
            for v in got:
                assert at(h,v)>=0
        assert set(facets)=={tuple(h["primitive_form"]) for h in cell["facets"]}
        counters["irreducible_facets"]+=len(facets)
        center=tuple(map(Rat,cell["strict_interior_point"]))
        assert all(at(tuple(map(Rat,h)),center)>0 for h in facets)
        for vrow in cell["vertices"]:
            v=tuple(map(Rat,vrow["coordinates"]));active=[]
            for h in cell["halfspaces"]:
                if not h["is_constant"] and at(tuple(map(Rat,h["primitive_form"])),v)==0:
                    active.append(h["id"])
            assert active==vrow["active_primitive_halfspaces"]
            for p in range(i):
                allvalues={r:literal_cost(i,q,v,p,1,Rat(0),r) for r in product((0,1),repeat=6-i)}
                minimum=min(allvalues.values())
                anchors=[literal_cost(i,q,v,p,1,Rat(0),(1,)*m+(z,)) for z in (0,1)]
                assert minimum==min(anchors)
                att=[list(r) for r,val in allvalues.items() if val==minimum]
                assert att==vrow["all_query_zero_attaining_tails"][str(p)]
                counters["full_vertex_true_query_zero_states"]+=len(allvalues)
        output.append(dict(cell=cell["id"],status="PASS",dimension=dim,facets=len(facets),vertices=len(got),trace=trace))
        print("independent geometry",cell["id"],"PASS",flush=True)
    witnesses=read("necessary_facet_witnesses.json")
    cellmap={c["id"]:c for c in cells}
    for w in witnesses:
        c=cellmap[w["cell"]];pt=tuple(map(Rat,w["point"]))
        for f in c["facets"]:
            v=at(tuple(map(Rat,f["primitive_form"])),pt)
            if f["id"]==w["facet_id"]:
                assert v<0 and v==Rat(w["violated_slack"])
            else:
                assert v>=0 and v==Rat(w["other_facet_slacks"][f["id"]])
        counters["facet_necessity_witnesses"]+=1
    write("literal_geometry_checks.json",output)


def verify_analytic(counters):
    for record in read("analytic_state_checks.json"):
        kind=record["kind"]
        if kind=="source5_strict_multiplicity_identity":
            p,d=record["p"],record["d"]
            def ff(k,w):
                return (Rat((6-k)*k,5*(p+1))+Rat(k)*w+Rat(k*(k-1),5*(p+2)))/6
            h=coefficients(lambda x:ff(d,x[0])-ff(1,x[0]),1)
            assert list(map(str,h))==record["affine_in_w"]
            for w in (Rat(0),Rat(1)):
                delta=Rat(5,6)*w+Rat(1,p+2)-Rat(1,6*(p+1))
                assert delta>0
                correction=Rat((d-1)*(6-d),30*(p+1)*(p+2))
                assert ff(d,w)-ff(1,w)==Rat(d-1,5)*delta+correction>0
            counters["source5_continuous_multiplicity_identities"]+=1
            continue
        i=record["source"];qbase=Rat(record["q0"]);dim=6-i
        if kind=="free_cap_necessity":
            js=list(range(i+1,6));m=len(js);chosen=record["middle_source"]
            def free_fn(x):
                hats=dict(zip(js,x[:m]));tau=dict(zip(js,x[m:2*m])); tail=[int(j==chosen) for j in js]
                cost=-tau[chosen]+hats[chosen]+qbase/2
                for k,j in enumerate(js):
                    cost+=tau[j]*qbase/Rat(sum(tail[:k])+7-j)
                zero=qbase+sum((qbase*tau[j]/Rat(7-j) for j in js),Rat(0))
                return cost-zero
            h=coefficients(free_fn,2*m+1)
            counters["free_cap_necessity_checks"]+=1
        else:
            p=record["p"];tail=tuple(record["tail"])
            if kind=="t0_all_nonnegative_tau":
                query=Rat(record["q"])
                zero=(0,)*(6-i)
                fn=lambda x:literal_cost(i,qbase,x,p,0,query,tail)-literal_cost(i,qbase,x,p,0,query,zero)
                h=coefficients(fn,dim)
                counters["t0_affine_quadrant_checks"]+=1
            else:
                fn=lambda x:literal_cost(i,qbase,x,p,1,Rat(1),tail)-literal_cost(i,qbase,x,p,1,Rat(0),tail)-(1+sum(x[:-1],Rat(0)))/Rat(p+7-i)
                h=coefficients(fn,dim)
                counters["t1_query_slope_checks"]+=1
            assert h[-1]==0 and all(v>=0 for v in h[:-1])
        assert list(map(str,h))==record["form"]
    write("literal_analytic_checks.json",dict(status="PASS",t0_for_all_nonnegative_tau=True,t1_for_all_nonnegative_queries=True,
          source5_m0_all_q="q/(p+1)",source5_m1_all_q="w_lambda(p+2)+q/(p+2)",
          source5_f_quadratic_coefficient="-1/[30(p+1)(p+2)]",source5_positive_endpoint_difference="5w/6+1/(p+2)-1/[6(p+1)]",
          source3_4_ordered_continuous_bound="W-Z >= 1/5 + m/10 + (9/10) sum(tau) > 0; lambda>=2 from a real D6 state",
          source5_W_minus_Z_not_assumed_nonnegative=True))


def verify_minima_and_menus(cells,counters):
    cmap={c["id"]:c for c in cells}
    params={v["id"]:(c,tuple(map(Rat,v["coordinates"]))) for c in cells for v in c["vertices"]}
    minima={}
    for tab in read("conditional_minimum_tables.json"):
        cell,x=params[tab["vertex_id"]];i=cell["source"];qb=Rat(cell["q0"]);p,t,q=tab["p"],tab["t"],Rat(tab["q"])
        tails=list(product((0,1),repeat=6-i));costs=[literal_cost(i,qb,x,p,t,q,r) for r in tails]
        low=min(costs);att=[r for r,c in zip(tails,costs) if c==low]
        assert tab["cell"]==cell["id"] and Rat(tab["minimum"])==low
        assert tab["all_attaining_tails"]==list(map(list,att)) and len(tab["states"])==len(tails)
        for saved,r,cost in zip(tab["states"],tails,costs):
            assert saved["tail"]==list(r) and Rat(saved["cost"])==cost and Rat(saved["gap"])==cost-low
        if t==0 and q in (Rat(0),qb):
            assert low==literal_cost(i,qb,x,p,t,q,(0,)*(6-i))
        if t==1:
            candidates=[literal_cost(i,qb,x,p,1,q,(1,)*(5-i)+(z,)) for z in (0,1)]
            assert min(candidates)==low
        if i==5 and t==0:assert low==q/Rat(p+1)
        minima[tab["vertex_id"],p,t,q]=(low,att)
        counters["physical_minimum_tables"]+=1;counters["physical_hidden_state_costs"]+=len(costs)
        counters["weak_tie_attainer_occurrences"]+=len(att);counters["maximum_attainer_count"]=max(counters["maximum_attainer_count"],len(att))
    outer={}
    for row in read("outer_average_tables.json"):
        vid,p,d=row["vertex_id"],row["p"],row["d"]
        c,x=params[vid];i=c["source"]
        f=Rat(0)
        if d<6:f+=Rat(6-d,6)*minima[vid,p,0,Rat(d,5)][0]
        if d>0:f+=Rat(d,6)*minima[vid,p,1,Rat(d-1,5)][0]
        Z=minima[vid,p,0,Rat(1,5)][0];W=minima[vid,p,1,Rat(0)][0];G=(5*Z+W)/6
        assert Rat(row["value"])==f and Rat(row["G"])==G and Rat(row["gap"])==f-int(d>0)*G>=0
        if d>1:assert f>G
        if i in (3,4):
            tau,_,_=budgets(i,Rat(1,5),x)
            assert x[-1]>=2 and W-Z>=Rat(1,5)+Rat(5-i,10)+Rat(9,10)*sum(tau.values(),Rat(0))>0
        outer[vid,p,d]=f
        counters["ordered_multiplicity_checks"]+=1
    for context in read("all_64_pure_query_checks.json"):
        vid,p,t=context["vertex_id"],context["p"],context["t"]
        cell,x=params[vid];i=cell["source"];qb=Rat(cell["q0"])
        assert len(context["patterns"])==64
        for record,mask in zip(context["patterns"],product((0,1),repeat=6)):
            d=sum(mask);o=int(d>0);q=Rat(d,6)
            actual,att=minima[vid,p,t,q];weak=minima[vid,p,t,Rat(o,6)][0]
            assert record["mask"]=="".join(map(str,mask)) and Rat(record["actual_minimum"])==actual
            assert Rat(record["union_minimum"])==weak and Rat(record["gap"])==actual-weak>=0
            for r in att:
                cost=literal_cost(i,qb,x,p,t,Rat(0),r,query_bits=mask)
                assert cost==actual
                counters["literal_six_query_attaining_tail_costs"]+=1
            counters["all_64_pure_menu_contexts"]+=1
    for context in read("all_64_ordered_menu_checks.json"):
        vid,p=context["vertex_id"],context["p"]
        cell,x=params[vid];i=cell["source"];qb=Rat(cell["q0"])
        G=Rat(context["G"])
        assert len(context["patterns"])==64
        for record,mask in zip(context["patterns"],product((0,1),repeat=6)):
            d=sum(mask);average=Rat(0)
            assert record["mask"]=="".join(map(str,mask)) and len(record["inner"])==6
            for k,t in enumerate(mask):
                queries=tuple(mask[j] for j in range(6) if j!=k)
                actualq=sum((Rat(v,5) for v in queries),Rat(0))
                assert actualq==Rat(d-t,5)
                low,att=minima[vid,p,t,actualq]
                rinner=record["inner"][k]
                assert rinner["outer_index"]==k+1 and rinner["t"]==t and Rat(rinner["actual_five_mean"])==actualq and Rat(rinner["minimum"])==low
                for tail in att:
                    real=literal_cost(i,qb,x,p,t,Rat(0),tail,query_bits=queries)
                    assert real==low
                    counters["literal_five_query_attaining_tail_costs"]+=1
                average+=low/6;counters["actual_inner_five_means"]+=1
            assert average==outer[vid,p,d]==Rat(record["outer_mean"])
            assert average-int(d>0)*G==Rat(record["gap"])>=0
            counters["all_64_ordered_menu_contexts"]+=1
    expected_keys=set()
    for vid,(cell,x) in params.items():
        i=cell["source"];den=Rat(cell["q0"]).denominator
        pairs=[(t,Rat(d,6)) for t in (0,1) for d in range(7)] if den==6 else [(t,Rat(d-t,5)) for d in range(7) for t in (0,1) if (t==0 and d<6) or (t==1 and d>0)]
        expected_keys.update((vid,p,t,q) for p in range(i) for t,q in pairs)
    assert set(minima)==expected_keys and len(minima)==counters["physical_minimum_tables"]
    return minima,params,outer


def verify_rows(cells,minima,params,outer,counters):
    family=read("exact_family.json")
    columns=read("coordinate_contract.json")
    bitstrings=list(product((0,1),repeat=9))
    assert columns["K_column"]==512 and columns["total_columns"]==513 and len(columns["customer_columns"])==512
    for k,(declared,bits) in enumerate(zip(columns["customer_columns"],bitstrings)):
        assert declared["index"]==k and declared["bits"]==list(bits)
    oldrows={}
    for den,pkg in [(6,"all_source_minimal_cap_safe"),(5,"ordered_minimal_cap")]:
        data=json.loads((ROOT/WS/pkg/"exact_family.json").read_text())
        for row in data["rows"]:
            i=row["source"]
            if i not in (3,4,5):continue
            tau=row["tau_by_true_source" if den==6 else "tau_by_source"]
            pt=tuple(Rat(tau[str(j)]) for j in range(i+1,6))+(25-Rat(row["s"]),)
            key=(den,i,pt,row["forced_target"] if den==6 else "ORDERED")
            oldrows[key]=row
    old_saved={r["row_id"]:r for r in read("old_row_column_identities.json")}
    cidentities=[];seen=defaultdict(list);row_keys=set()
    with (HERE/"full_column_checks.tsv").open("w") as out:
        out.write("row_id\tcolumn\tliteral_raw\tsaved_raw\tresidual\tliteral_divided_by_25\n")
        for index,row in enumerate(family["rows"]):
            assert row["raw_row_index"]==index and len(row["a"])==513 and Rat(row["numeric_positive_divisor"])==25
            vid=row["vertex_id"];cell,x=params[vid];i=cell["source"];qb=Rat(cell["q0"])
            row_key=(vid,row["kind"],row["forced_target"])
            assert row_key not in row_keys
            row_keys.add(row_key)
            tau,hats,a=budgets(i,qb,x);B=sum(hats.values(),Rat(0));S=1+B
            assert Rat(row["source_IC_weight"])==a and Rat(row["K_weight"])==(1 if row["kind"]=="six_C_only" else S)
            vector=[];cproof=[]
            for k,bits in enumerate(bitstrings):
                p=sum(bits[:i-1]);total=sum(bits[:6]);actual_share=Rat(bits[i-1],total) if total else Rat(0)
                if row["kind"]=="ordered":
                    positive=[outer[vid,p,d] for d in range(1,7)]
                    G=min(positive)
                    assert G==outer[vid,p,1] and all(v>G for v in positive[1:])
                    expected=a*actual_share-bits[7]*G
                else:
                    target=row["forced_target"]
                    pos=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
                    t=bits[pos]
                    weak=minima[vid,p,t,Rat(bits[7],6)][0]
                    expected=a*actual_share-weak
                    if row["kind"]=="six_C_only":
                        expected+=B*bits[8]
                        cproof.append(str(B*bits[8]))
                vector.append(expected)
            vector.append(Rat(1) if row["kind"]=="six_C_only" else S)
            if row["kind"]=="six_C_only":
                cproof.append(str(-B))
                cidentities.append(dict(row_id=row["id"],free_equality="|C|-K",multiplier=str(B),full_513_equality_vector=cproof))
                counters["C_only_full_column_equalities"]+=513
            for k,expected in enumerate(vector):
                saved=Rat(row["a"][str(k)])
                assert saved==expected
                out.write(f"{row['id']}\t{k}\t{expected}\t{saved}\t0\t{expected/25}\n")
            counters["full_columns"]+=513;counters["rows"]+=1
            if x[-1]>=16:
                key=(qb.denominator,i,x,"ORDERED" if row["kind"]=="ordered" else row["forced_target"])
                old=oldrows[key];check=old_saved[row["id"]]
                assert old["name"]==check["old_row_id"] and Rat(check["s"])==25-x[-1]
                for k,expected in enumerate(vector):
                    correction=B*(Rat(bitstrings[k][8]) if k<512 else Rat(-1)) if row["kind"]=="six_C_only" else Rat(0)
                    residual=expected-Rat(old["a"][str(k)])-correction
                    assert residual==0 and Rat(check["all_513_column_residuals"][k])==0
                counters["old_parameter_row_identities"]+=1;counters["old_parameter_column_identities"]+=513
            normalized=tuple(map(str,vector));seen[normalized].append(row["id"])
    counters["distinct_exact_row_vectors"]=len(seen)
    expected_rows=set()
    for vid,(cell,x) in params.items():
        if Rat(cell["q0"])==Rat(1,6):
            expected_rows.update((vid,"six_general",t) for t in ["A1","A2","A3","A4","A5","A6","X","C"])
            expected_rows.add((vid,"six_C_only","C"))
        else:
            expected_rows.add((vid,"ordered","ORDERED"))
    assert row_keys==expected_rows
    occurrence=read("row_occurrences.json")
    assert occurrence["raw_rows"]==len(family["rows"]) and occurrence["distinct_exact_vectors"]==len(seen)
    assert sorted(tuple(v) for v in seen.values())==sorted(tuple(g["row_ids"]) for g in occurrence["groups"])
    # Verify the old domains by their frozen halfspaces and vertices directly.
    identity=[]
    for den,pkg in [(6,"all_source_minimal_cap_safe"),(5,"ordered_minimal_cap")]:
        data=json.loads((ROOT/WS/pkg/"parameter_domains.json").read_text())
        ds=data["sources" if den==6 else "domains"]
        for c in cells:
            if Rat(c["q0"]).denominator!=den or not c["old_window"]:continue
            od=next(d for d in ds if d["source"]==c["source"])
            ov={tuple(map(Rat,v["parameters"][:-1]))+(25-Rat(v["parameters"][-1]),) for v in od["vertices"]}
            nv={tuple(map(Rat,v["coordinates"])) for v in c["vertices"]}
            assert ov==nv
            hf=[]
            for h in od["complete_domain_halfspaces" if den==6 else "facets"]:
                cc=list(map(Rat,h["coefficients"])) if den==6 else [-Rat(v) for v in h["normal"]]
                constant=Rat(h["constant"] if den==6 else h["rhs"])
                hf.append(normalize(tuple([constant+25*cc[-1]]+cc[:-1]+[-cc[-1]])))
            assert set(hf)=={tuple(h["primitive_form"]) for h in c["facets"]}
            identity.append(dict(cell=c["id"],exact_facet_identity=True,exact_vertex_identity=True))
    write("literal_old_family_checks.json",dict(status="PASS",domain_identities=identity,row_identities=counters["old_parameter_row_identities"],column_identities=counters["old_parameter_column_identities"]))
    write("literal_C_equality_checks.json",cidentities)


def main():
    input_hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUT_FILES}
    pin_count=verify_pins()
    counters=defaultdict(int)
    cells=read("parameter_domains.json")["cells"]
    assert len(cells)==24
    windows={3:[(0,9),(9,16),(16,25)],4:[(0,4),(4,9),(9,16),(16,25)],5:[(0,1),(1,4),(4,9),(9,16),(16,25)]}
    actual_keys={(c["source"],Rat(c["q0"]),tuple(map(Rat,c["window"]))) for c in cells}
    expected_keys={(i,q,tuple(map(Rat,w))) for i in windows for q in (Rat(1,6),Rat(1,5)) for w in windows[i]}
    assert actual_keys==expected_keys
    verify_geometry(cells,counters)
    verify_analytic(counters)
    minima,params,outer=verify_minima_and_menus(cells,counters)
    print("literal minima and indexed menus PASS",flush=True)
    verify_rows(cells,minima,params,outer,counters)
    assert verify_pins()==pin_count
    assert input_hashes=={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUT_FILES}
    counts=dict(counters)
    generated=read("family_generator_output.json")["counts"]
    for k in ["physical_minimum_tables","physical_hidden_state_costs","weak_tie_attainer_occurrences","maximum_attainer_count",
              "all_64_pure_menu_contexts","all_64_ordered_menu_contexts","actual_inner_five_means","ordered_multiplicity_checks",
              "rows","full_columns","distinct_exact_row_vectors","old_parameter_row_identities","old_parameter_column_identities",
              "t0_affine_quadrant_checks","t1_query_slope_checks","free_cap_necessity_checks","source5_continuous_multiplicity_identities"]:
        assert counts[k]==generated[k],k
    output=dict(status="PASS",method="independent literal costs, indexed legal queries, bounded-box true-edge clipping",
                imports_generator_or_project_python=False,optimizer_calls=0,global_LP_inputs_points_faces_read=False,
                pinned_sources_unchanged=pin_count,verified_input_sha256=input_hashes,
                verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),counts=counts)
    write("literal_checker_output.json",output)
    print(json.dumps(output,ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
