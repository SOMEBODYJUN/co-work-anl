#!/usr/bin/env python3
"""Exact post-checks for an explicitly supplied, SHA-bound full4177 v6 input.

No solver, file discovery, old-point fallback, or implicit certificate reading.
The prepare/self-test commands never accept or read a live solver certificate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from functools import lru_cache
import argparse
import hashlib
import json
import re
import traceback
from collections import Counter
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=Path("/workspace/scratch/b0fef5ec503f/cap3_full_delta_rows_stage")
EXPECTED_MANIFEST="bc0d03e6cb05fc6c270fc14ec2e547a3333cf36b924dd883e8d25cd3ad450c8f"
EXPECTED_FAMILY="4a31f3ff6847a355442807aa8d03fffad43c92c6849229f63299556da8c00c8b"
BITS=tuple(product((0,1),repeat=9))
TAILS=tuple(product((0,1),repeat=4))
ORDER=["".join(map(str,b)) for b in BITS]+["K"]
RUN="six-boss1-20261111"
SOLVE="full4177_v6"


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [serial(v) for v in x]
    return x


def save(directory,name,obj):
    directory.mkdir(parents=True,exist_ok=True)
    (directory/name).write_text(json.dumps(serial(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def digest(data): return hashlib.sha256(data).hexdigest()
def file_sha(path): return digest(path.read_bytes())


def exact(x):
    if isinstance(x,bool): raise ValueError("Boolean is not an exact coordinate.")
    if isinstance(x,int): return F(x)
    if isinstance(x,str) and re.fullmatch(r"[+-]?\d+(?:/[+]?[1-9]\d*)?",x): return F(x)
    if isinstance(x,dict) and set(x)=={"numerator","denominator"}:
        if not isinstance(x["numerator"],int) or isinstance(x["numerator"],bool): raise ValueError("Integer numerator required.")
        if not isinstance(x["denominator"],int) or isinstance(x["denominator"],bool) or x["denominator"]<=0: raise ValueError("Positive integer denominator required.")
        return F(x["numerator"],x["denominator"])
    raise ValueError("Only integers or exact rational strings/objects are accepted; floats and decimal strings are rejected.")


def pointer(data,path):
    if path in ("",None): return data
    if not path.startswith("/"): raise ValueError("A JSON pointer must start with '/'.")
    obj=data
    for raw in path.split("/")[1:]:
        token=raw.replace("~1","/").replace("~0","~")
        obj=obj[int(token)] if isinstance(obj,list) else obj[token]
    return obj


def optional_pointer(data,path):
    try: return pointer(data,path)
    except (KeyError,IndexError,TypeError,ValueError): return None


def read_bound_json(path,expected_sha):
    if not re.fullmatch(r"[0-9a-f]{64}",expected_sha or ""): raise ValueError("An explicit lowercase SHA256 is required.")
    data=path.read_bytes()
    actual=digest(data)
    if actual!=expected_sha: raise ValueError(f"SHA256 mismatch for explicit input {path}: expected {expected_sha}, got {actual}")
    return json.loads(data),dict(path=str(path.resolve()),sha256=actual,bytes=len(data))


def coordinate_vector(value,order,contract_assertion,expected_contract):
    if isinstance(value,dict) and set(value)==set(ORDER): return tuple(exact(value[k]) for k in ORDER)
    if not isinstance(value,list) or len(value)!=513: raise ValueError("Expected exactly 513 coordinates, or a map keyed by all 512 bit strings plus K.")
    if order is not None:
        normalized=["".join(map(str,z)) if isinstance(z,list) else z for z in order]
        if normalized!=ORDER: raise ValueError("The supplied coordinate order does not match the frozen full-513 contract.")
    elif contract_assertion!=expected_contract:
        raise ValueError("An array requires explicit coordinate_order or --coordinate-contract-sha256 matching the frozen source contract.")
    return tuple(exact(x) for x in value)


def plain_vector(value,length):
    if not isinstance(value,list) or len(value)!=length: raise ValueError(f"Expected a rational vector of length {length}.")
    return tuple(exact(x) for x in value)


def dot(a,b):
    if len(a)!=len(b): raise ValueError("Dot-product dimensions differ.")
    return sum((x*y for x,y in zip(a,b) if x and y),F(0))


def add_vectors(a,b): return tuple(x+y for x,y in zip(a,b))
def scale_vector(a,w): return tuple(w*x for x in a)
def sign(x): return "negative" if x<0 else "zero" if x==0 else "positive"


def affine_form(row,origin,directions):
    return dict(constant=dot(row,origin),coefficients=[dot(row,d) for d in directions])


def evaluate_form(form,parameters): return form["constant"]+dot(form["coefficients"],parameters)


def solve_coordinates(origin,directions,point):
    """Exact affine membership. A redundant basis is allowed and reported."""
    k=len(directions)
    if point==origin: return dict(status="member",parameters=[F(0)]*k,rank=None,method="origin_matches_certificate")
    if not k: return dict(status="not_in_affine_hull",parameters=None,rank=0)
    rows=[[directions[j][i] for j in range(k)]+[point[i]-origin[i]] for i in range(len(origin))]
    pivots=[]
    at=0
    for col in range(k):
        pivot=next((i for i in range(at,len(rows)) if rows[i][col]),None)
        if pivot is None: continue
        rows[at],rows[pivot]=rows[pivot],rows[at]
        z=rows[at][col]
        rows[at]=[v/z for v in rows[at]]
        for i in range(len(rows)):
            if i!=at and rows[i][col]:
                w=rows[i][col]
                rows[i]=[x-w*y for x,y in zip(rows[i],rows[at])]
        pivots.append(col)
        at+=1
    if any(not any(r[:k]) and r[k] for r in rows): return dict(status="not_in_affine_hull",parameters=None,rank=len(pivots))
    theta=[F(0)]*k
    for i,col in enumerate(pivots): theta[col]=rows[i][k]
    assert tuple(origin[i]+sum(directions[j][i]*theta[j] for j in range(k)) for i in range(len(origin)))==point
    return dict(status="member",parameters=theta,rank=len(pivots),method="rational_elimination",redundant_basis=len(pivots)<k)


class Source:
    def __init__(self,path):
        self.path=path
        if file_sha(path/"freeze_manifest.json")!=EXPECTED_MANIFEST: raise ValueError("The source 585-row frozen manifest is not the authorized one.")
        manifest=json.loads((path/"freeze_manifest.json").read_text())
        for rec in manifest["files"]:
            if file_sha(path/rec["path"])!=rec["sha256"]: raise ValueError(f"Frozen source file mismatch: {rec['path']}")
        if file_sha(path/"exact_family.json")!=EXPECTED_FAMILY: raise ValueError("585-row family SHA mismatch.")
        self.rows=json.loads((path/"exact_family.json").read_text())["rows"]
        self.by_id={r["id"]:r for r in self.rows}
        self.vectors={r["id"]:tuple(exact(z) for z in r["a"]) for r in self.rows}
        self.tables={t["vertex_key"]:t for t in json.loads((path/"vertex_cost_tables.json").read_text())["vertices"]}
        self.registry={r["vertex_key"]:r for r in json.loads((path/"vertex_registry.json").read_text())["records"]}
        self.coordinate_contract_sha=file_sha(path/"coordinate_contract.json")
        contract=json.loads((path/"coordinate_contract.json").read_text())
        if contract["columns"]!=ORDER: raise ValueError("Unexpected frozen coordinate contract.")
        if len(self.rows)!=585 or len(self.tables)!=225 or len(self.registry)!=225: raise ValueError("Incomplete frozen source.")
        self.binding=dict(path=str(path.resolve()),manifest_sha256=EXPECTED_MANIFEST,family_sha256=EXPECTED_FAMILY,
                          coordinate_contract_sha256=self.coordinate_contract_sha,
                          vertex_registry_sha256=file_sha(path/"vertex_registry.json"),
                          vertex_cost_tables_sha256=file_sha(path/"vertex_cost_tables.json"),
                          source_binding=json.loads((path/"source_binding.json").read_text()),rows=585,source_vertices=225)
        self._minima_cache={}

    @staticmethod
    def cost(row,p,t,q,r):
        a=exact(row["real_budget"]["source_IC"])
        tau={int(j):exact(z) for j,z in row["tau"].items()}
        caps={int(j):exact(z) for j,z in row["beta_actual"].items()}
        L=p+t+sum(r)
        share=lambda z:F(z,L) if L else F(0)
        return (a*share(t)-share(r[3])-sum(tau[j]*share(r[j-3]) for j in range(3,6))
                +sum(caps[j]*r[j-3] for j in range(3,6))+r[3]
                +q/(p+t+sum(r[:3])+1)
                +sum(tau[j]*q/(p+t+sum(r[:j-3])+7-j) for j in range(3,6)))

    def minima(self,row,p,t,q):
        key=(row["vertex_key"],p,t,q)
        if key in self._minima_cache: return self._minima_cache[key]
        values={"".join(map(str,r)):self.cost(row,p,t,q,r) for r in TAILS}
        value=min(values.values())
        result=value,[r for r,z in values.items() if z==value]
        self._minima_cache[key]=result
        return result

    def condition(self,row,p,t,n):
        record=next(c for c in self.tables[row["vertex_key"]]["conditions"] if (c["p"],c["t"],c["n"])==(p,t,n))
        q=F(n,6) if row["mode"]=="pure" else F(n-t,5)
        value,tails=self.minima(row,p,t,q)
        if value!=exact(record["minimum"]) or tails!=record["all_weak_tails"]: raise ValueError("True COST no longer matches the complete frozen weak-state table.")
        return dict(p=p,t=t,n=n,q=q,minimum=value,all_weak_tails=tails)


def contract_checks(point):
    checks=[]
    negative=[i for i,x in enumerate(point) if x<0]
    checks.append(dict(id="nonnegative_customer_masses_and_K",pass_=not negative,negative_columns=negative))
    K=point[512]
    sizes={name:sum(point[i]*bits[col] for i,bits in enumerate(BITS)) for name,col in
           [(f"A{j}",j-1) for j in range(1,7)]+[("X",6),("C",8)]}
    residual=sizes["C"]-K
    checks.append(dict(id="E_C_equals_zero",pass_=residual==0,residual=residual))
    for name,size in sizes.items(): checks.append(dict(id=f"K_caps_{name}",pass_=K>=size,residual=K-size))
    O=sum(point[i]*bits[7] for i,bits in enumerate(BITS))
    checks.append(dict(id="six_legal_query_union_at_most_6K",pass_=O<=6*K,residual=6*K-O))
    return dict(all_pass=all(c["pass_"] for c in checks),checks=checks,K=K,observed_label_sizes=sizes,O=O,
                note="These are observable physical prerequisites, not a verification of all full4177 constraints or an SPE construction.")


def true_budget_blueprint(row):
    a=exact(row["real_budget"]["source_IC"])
    caps={int(j):exact(z) for j,z in row["beta_actual"].items()}
    tau={int(j):exact(z) for j,z in row["tau"].items()}
    actual_source=row["mode"]=="pure" and row["target"]=="A2"
    n=6 if row["mode"]=="pure" else 5
    outer=1 if row["mode"]=="pure" else 6
    terms=[]
    if not actual_source:
        terms.append(dict(kind="source_IC",player=2,weight=a,outer_branches=outer,
                          query="forced legal T" if outer==1 else "each outer menu index k",
                          equality="v2_after_forcing=u2_actual"))
    for j,w in caps.items():
        if w>0: terms.append(dict(kind="CAP",player=j,weight=w,outer_branches=outer,equality=f"size(R{j})=K"))
    terms.append(dict(kind="CAP",player=6,weight=F(1),outer_branches=outer,equality="size(R6)=K"))
    terms.append(dict(kind="terminal_BR",player=6,weight=F(1),query_index_count=n,outer_branches=outer,
        equality="each legal queried label gives exactly v6 at this terminal prefix"))
    for j,w in tau.items():
        if w>0:
            terms.append(dict(kind="internal_SAFE",player=j,weight=w,query_index_count=n,outer_branches=outer,
                equality="for each queried index: current vj = its actual deviation payoff = its SAFE lower bound",
                continuation_owner="the given strategy at the new ordered history after that query",
                saturation="every remaining player covers each positive-mass customer of that queried label",
                remaining_players=list(range(j+1,7))))
    zeros=[dict(kind="CAP",player=j,weight=w) for j,w in caps.items() if w==0]
    zeros += [dict(kind="internal_SAFE",player=j,weight=w) for j,w in tau.items() if w==0]
    return dict(row_id=row["id"],mode=row["mode"],target=row["target"],source_vertex=row["vertex_key"],
        terms=terms,zero_weight_terms_with_no_equality_demand=zeros,
        source_A2_is_actual_history=actual_source,
        source_IC_identity="u2=v2 identically; no source deviation to A2" if actual_source else None,
        indexed_query_routing="all six legal query indices" if outer==1 else "outer k=1..6; inner l!=k (index exclusion)",
        terminal_CAP=F(1),terminal_BR_weight=F(1),raw_K=exact(row["raw_K"]),final_K=exact(row["K"]),
        free_EC=exact(row["free_EC"]),free_EC_requires="E_C=0; it is not a nonnegative budget term",
        original_scale=True,numerical_divisor_applied=False)


def deviation_obligation(row,slack,physical):
    blueprint=true_budget_blueprint(row)
    if slack>=0: raise ValueError("A negative raw slack is required.")
    if not physical["all_pass"]:
        return dict(status="observable_model_contract_failed",slack=slack,blueprint=blueprint,
                    conclusion="Arithmetic row violation is recorded; a genuine-deviation interpretation is conditional on the failed physical prerequisites being repaired.")
    a=exact(row["real_budget"]["source_IC"])
    tau=sum(exact(z) for z in row["tau"].values())
    W=(F(0) if blueprint["source_A2_is_actual_history"] else a)+tau+1
    routes=[t for t in blueprint["terms"] if t["kind"] in ("source_IC","internal_SAFE","terminal_BR")]
    return dict(status="definite_true_deviation_disjunction",slack=slack,deficit=-slack,
        strategic_weight_sum=W,guaranteed_minimum_gain=(-slack)/W,routes=routes,blueprint=blueprint,
        quantifier="Any complete strategy claimed to realize these aggregate coordinates must admit at least one actual legal deviation on a listed real branch with gain at least the displayed bound.",
        units="the same homogeneous scale as the supplied exact certificate",
        not_an_SPE_counterexample=True)


def a2_equality_forms(source,row):
    if not (row["mode"]=="pure" and row["target"]=="A2" and row["row_kind"]=="general"): return []
    result=[]
    for j in range(3,7):
        weight=F(1) if j==6 else exact(row["beta_actual"][str(j)])
        if weight:
            vec=tuple(-F(bits[j-1]) for bits in BITS)+(F(1),)
            result.append(dict(id=f"actual_CAP{j}",kind="CAP",player=j,weight=weight,coefficients=vec,
                               required="zero",nonnegative_for_SPE=True))
    for j in (3,4,5,6):
        weight=F(1) if j==6 else exact(row["tau"][str(j)])
        if not weight: continue
        vals=[]
        for bits in BITS:
            load=sum(bits[:6])
            payoff=F(bits[j-1],load) if load else F(0)
            denominator=sum(bits[:j-1])+7-j
            vals.append(payoff-F(bits[7],6*denominator))
        kind="terminal_BR" if j==6 else "internal_SAFE"
        result.append(dict(id=f"actual_{kind}{j}_weak_o6",kind=kind,player=j,weight=weight,
            coefficients=tuple(vals)+(F(0),),required="zero",nonnegative_for_SPE=True,
            negative_value_means="some one of the six actual legal query labels gives a true gain at least minus this value"))
    vals=[]
    for bits in BITS:
        actual=source.cost(row,bits[0],bits[1],F(bits[7],6),tuple(bits[2:6]))
        smallest,_=source.minima(row,bits[0],bits[1],F(bits[7],6))
        vals.append(actual-smallest)
    result.append(dict(id="actual_tail_projection_gap",kind="tail_projection",weight=F(1),
                       coefficients=tuple(vals)+(F(0),),required="zero",nonnegative_for_SPE=True))
    reconstructed=tuple(sum(term["weight"]*term["coefficients"][i] for term in result) for i in range(513))
    if reconstructed!=source.vectors[row["id"]]: raise ValueError("The mechanical actual-A2 true-budget identity failed.")
    return result


def equality_checklist(source,row,point,physical):
    blueprint=true_budget_blueprint(row)
    requirements=[]
    if row["mode"]=="pure":
        target=row["target"]
        col=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
        for p,t,o in product((0,1),repeat=3):
            mass=sum(point[i] for i,bits in enumerate(BITS) if (bits[0],bits[col],bits[7])==(p,t,o))
            if mass>0: requirements.append(dict(customer_class=dict(p=p,t=t,o=o),mass=mass,
                condition=source.condition(row,p,t,o),scope="each positive-mass customer on the real T-forced branch"))
    else:
        for p,o in product((0,1),repeat=2):
            mass=sum(point[i] for i,bits in enumerate(BITS) if (bits[0],bits[7])==(p,o))
            if mass<=0: continue
            if o==0:
                cases=[dict(outer_membership=0,outer_index_count=6,condition=source.condition(row,p,0,0))]
            else:
                cases=[dict(outer_membership=1,outer_index_count=1,condition=source.condition(row,p,1,1)),
                       dict(outer_membership=0,outer_index_count=5,condition=source.condition(row,p,0,1))]
            requirements.append(dict(customer_class=dict(p=p,o=o),mass=mass,cases=cases,
                scope="each actual outer branch; the unique covering menu index is not chosen independently of the strategy"))
    observed=[]
    known_deviations=[]
    for term in a2_equality_forms(source,row):
        value=dot(term["coefficients"],point)
        observed.append({k:v for k,v in term.items() if k!="coefficients"}|dict(value=value,equality_pass=value==0))
        if term["kind"] in ("terminal_BR","internal_SAFE") and value<0 and physical["all_pass"]:
            known_deviations.append(dict(player=term["player"],node="actual path prefix for this player",
                true_query_gain_at_least=-value,query="one of the six legal query indices",source_term=term["id"]))
    return dict(status="necessary_equalities_for_an_SPE_realization",physical_prerequisites_pass=physical["all_pass"],
        blueprint=blueprint,indexed_menu_coverage_requirement="d_x=o_x for every positive-mass customer; the six indexed query coverages are pairwise disjoint",
        minimum_tail_requirements=requirements,actual_A2_observable_equalities=observed,
        actual_A2_equality_failure=bool(observed and any(not x["equality_pass"] for x in observed)),
        actual_A2_certified_query_deviations=known_deviations,
        warning="These are necessary conditions under an SPE realization; a zero aggregate row alone does not establish them or construct jointly consistent tails.")


def require(condition,message):
    if not condition: raise ValueError(message)


def sparse_vector(value):
    require(isinstance(value,dict),"Expected a sparse exact 513-coordinate object.")
    out={}
    for name,x in value.items():
        require(re.fullmatch(r"0|[1-9]\d*",name) is not None,"Noncanonical column index.")
        i=int(name)
        require(0<=i<513,"Column index is outside 0..512.")
        out[i]=exact(x)
    return out


def sparse_dot(row,point): return sum((x*point[i] for i,x in row.items() if x and point[i]),F(0))


def sparse_affine(row,origin,directions,rhs=F(0)):
    return dict(constant=sparse_dot(row,origin)-rhs,
                coefficients=[sparse_dot(row,d) for d in directions])


def same_form(left,right):
    return left["constant"]==exact(right["constant"]) and left["coefficients"]==[exact(x) for x in right["parameter_coefficients"]]


def rational_rank(rows):
    work=[list(r) for r in rows]
    if not work: return 0
    rank=0
    for col in range(len(work[0])):
        pivot=next((i for i in range(rank,len(work)) if work[i][col]),None)
        if pivot is None: continue
        work[rank],work[pivot]=work[pivot],work[rank]
        z=work[rank][col]
        work[rank]=[v/z for v in work[rank]]
        for i in range(rank+1,len(work)):
            if work[i][col]:
                w=work[i][col]
                work[i]=[x-w*y for x,y in zip(work[i],work[rank])]
        rank+=1
        if rank==len(work): break
    return rank


def verify_source(source):
    """Rebuild all coefficients from the 16 true COST states, never from an anchor."""
    vertices=[]
    reconstructed={}
    count=Counter()
    for row in source.rows:
        s,delta,h,q0=(exact(row[k]) for k in ("s","delta","h","q0"))
        require(s in (F(0),F(61273,6912),F(9)),"Wrong source s.")
        require(q0==(F(1,6) if row["mode"]=="pure" else F(1,5)),"Wrong indexed query weight.")
        tau={3:F(0),4:F(5977,6912)-delta,5:F(43,48)+delta}
        a=F(25)+sum(tau.values())-s
        original={j:q0/2+tau[j]+sum(q0*tau[l]/((7-l)*(8-l)) for l in range(j+1,6)) for j in (3,4,5)}
        beta=original|{3:original[3]-h}
        S=F(1)+sum(beta.values())
        require(0<=delta<=F(5977,6912) and 0<=h<=original[3],"Source parameter is outside the closed domain.")
        for name,want in (("tau",tau),("beta_original",original),("beta_actual",beta)):
            require({int(j):exact(z) for j,z in row[name].items()}==want,"Actual source weight mismatch: "+name)
        require(exact(row["real_budget"]["source_IC"])==a,"Source IC was incorrectly scaled.")
        require(exact(row["raw_K"])==S,"Independent K coefficient mismatch.")
        require(row["raw_scale"] and row["divisor_applied"] is False,"Raw scale was not preserved.")
        free=S-s/5 if row["row_kind"]=="C-only" else F(0)
        require(exact(row["free_EC"])==free and exact(row["K"])==S-free,"Free EC identity mismatch.")
        key=row["vertex_key"]
        if key not in reconstructed:
            table=source.tables[key]
            registry=source.registry[key]
            require([delta,h]==[exact(z) for z in registry["source_vertex_record"]["point"]],"Source registry coordinate mismatch.")
            condition_checks=[]
            minima={}
            for cond in table["conditions"]:
                p,t,n=cond["p"],cond["t"],cond["n"]
                q=F(n,6) if row["mode"]=="pure" else F(n-t,5)
                costs={"".join(map(str,r)):source.cost(row,p,t,q,r) for r in TAILS}
                require(set(costs)==set(cond["costs"]),"A tail state was deleted.")
                require(all(v==exact(cond["costs"][r]) for r,v in costs.items()),"A literal true COST value disagrees.")
                smallest=min(costs.values())
                weak=[r for r,z in costs.items() if z==smallest]
                require(smallest==exact(cond["minimum"]) and weak==cond["all_weak_tails"],"A weak minimizing state was omitted.")
                source._minima_cache[(key,p,t,q)]=(smallest,weak)
                minima[p,t,n]=smallest
                condition_checks.append(dict(p=p,t=t,n=n,q=q,costs=costs,minimum=smallest,all_weak_tails=weak))
                count["true_COST_values"]+=16
                count["condition_minima_and_full_weak_sets"]+=1
            f={}
            G={}
            if row["mode"]=="ordered":
                for p in (0,1):
                    f[p]={}
                    for d in range(7):
                        value=((6-d)*minima[p,0,d] if d<6 else F(0))+(d*minima[p,1,d] if d>0 else F(0))
                        f[p][d]=value/6
                        require(f[p][d]==exact(table["f"][str(p)][str(d)]),"An actual ordered multiplicity value disagrees.")
                    G[p]=min(f[p][d] for d in range(1,7))
                    active=[d for d in range(1,7) if f[p][d]==G[p]]
                    require(G[p]==exact(table["G"][str(p)]) and active==table["G_active_d"][str(p)],"An ordered multiplicity switch was omitted.")
                    require(active==[1] and f[p][0]==0,"The full-domain ordered d1 theorem failed at a vertex.")
            reconstructed[key]=dict(minima=minima,f=f,G=G)
            vertices.append(dict(vertex_key=key,source_registry_record=registry,conditions=condition_checks,f=f,G=G))
        minima=reconstructed[key]["minima"]
        G=reconstructed[key]["G"]
        expected=[]
        if row["mode"]=="pure":
            target=row["target"]
            column=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
        for bits in BITS:
            load=sum(bits[:6])
            u2=F(bits[1],load) if load else F(0)
            minimum=minima[bits[0],bits[column],bits[7]] if row["mode"]=="pure" else bits[7]*G[bits[0]]
            expected.append(a*u2-minimum+free*bits[8])
        expected.append(S-free)
        require(tuple(expected)==source.vectors[row["id"]],"Raw 513-column row reconstruction failed: "+row["id"])
        count["raw_coefficients_reconstructed"]+=513
        count["metadata_and_true_payment_records"]+=1
    identity_count=0
    for row in source.rows:
        if a2_equality_forms(source,row): identity_count+=513
    return dict(status="PASS_TRUE_COST_FULL_WEAK_STATES_RAW_513",source=source.binding,
                counts=dict(count),source_vertices=len(vertices),actual_A2_budget_identity_columns=identity_count,
                optimizer_calls=0,vertices=vertices)


def validate_v6_core(model,certificate,face,certificate_check,face_check,bindings,source):
    """Independently verify the supplied full input, exact primal/dual, and full face."""
    input_sha=bindings["input"]["sha256"]
    cert_sha=bindings["certificate"]["sha256"]
    face_sha=bindings["face"]["sha256"]
    require(model["variables"]==513 and model["K_column"]==512,"The independent K coordinate is missing.")
    require(model["bit_order"]==["a1","a2","a3","a4","a5","a6","x","o","c"],"The v6 bit order is wrong.")
    require(len(model["atom_columns"])==512,"Incomplete v6 atom columns.")
    for i,(atom,bits) in enumerate(zip(model["atom_columns"],BITS)):
        actual=tuple(atom["a"])+(atom["x"],atom["o"],atom["c"])
        require(actual==bits and atom["index"]==i and i==2*atom["old_index"]+atom["c"],"Atom bit/index mismatch.")
    require(model["nonnegative_columns"]==list(range(513)),"The model dropped a nonnegative coordinate.")
    require(certificate["schema"]=="visible_maximum_joint_exact_certificate_v6","Only the explicitly authorized v6 schema is accepted.")
    for obj in (certificate,face,certificate_check,face_check): require(obj["input_sha256"]==input_sha,"Core input SHA cross-binding failed.")
    for obj in (face,certificate_check,face_check): require(obj["certificate_sha256"]==cert_sha,"Core certificate SHA cross-binding failed.")
    require(face_check["face_sha256"]==face_sha,"Face-check SHA cross-binding failed.")
    require(face_check["independent_certificate_check_sha256"]==bindings["certificate_check"]["sha256"],"Independent-check SHA cross-binding failed.")
    point=plain_vector(certificate["primal"],513)
    require(all(x>=0 for x in point),"The v6 point has a negative coordinate.")
    require(exact(certificate["K"])==point[512],"K field disagrees with the independent K column.")
    require(certificate["primal_support"]==[i for i,x in enumerate(point) if x>0],"The stated primal support is wrong.")
    objective=sparse_vector(model["objective"])
    value=sparse_dot(objective,point)
    require(value==exact(certificate["objective"])==exact(face["objective"]),"Primal objective mismatch.")
    rows=model["raw_rows"]
    require(len(rows)==4177==model["raw_inequality_count"]==len(face["all_raw_inequality_restrictions"]),"The full 4177-row family was not retained.")
    require(len(face["all513_nonnegative_coordinate_restrictions"])==513,"The face dropped coordinate conditions.")
    y=plain_vector(certificate["dual"]["raw_row_weights"],4177)
    eta=plain_vector(certificate["dual"]["equality_multipliers"],2)
    require(all(w>=0 for w in y),"A dual inequality weight is negative.")
    positive=[i for i,w in enumerate(y) if w>0]
    require(positive==certificate["dual"]["positive_raw_indices"]==face["positive_dual_raw_indices"],"Positive dual support mismatch.")
    residual=[objective.get(i,F(0)) for i in range(513)]
    k=len(face["parameters"])
    require(k==9==face["unconstrained_affine_parameter_count"],"Unexpected full-face affine parameter count.")
    origin=[F(0)]*513
    directions=[[F(0)]*513 for _ in range(k)]
    present=set()
    for rec in face["coordinates"]:
        i=rec["column"]
        require(0<=i<513 and i not in present,"Repeated or invalid face coordinate.")
        present.add(i)
        origin[i]=exact(rec["constant"])
        for j,w in enumerate(plain_vector(rec["parameter_coefficients"],k)): directions[j][i]=w
    origin=tuple(origin)
    directions=tuple(tuple(d) for d in directions)
    parameters=plain_vector(face["point_parameters"],k)
    require(tuple(origin[i]+sum(d[i]*parameters[j] for j,d in enumerate(directions)) for i in range(513))==point,"The certificate is not the stated face point.")
    for j,param in enumerate(face["parameters"]):
        i=param["column"]
        require(param["position"]==j and origin[i]==0 and [d[i] for d in directions]==[F(int(l==j)) for l in range(k)],"The named face parameter is not its declared free coordinate.")
    base_equations=[]
    equation_rhs=[]
    equation_names=[]
    dual_objective=F(0)
    for eq,w in zip(model["equalities"],eta):
        vec=sparse_vector(eq["a"])
        rhs=exact(eq["rhs"])
        require(sparse_dot(vec,point)==rhs,"An original equality fails at the point.")
        form=sparse_affine(vec,origin,directions,rhs)
        require(form["constant"]==0 and not any(form["coefficients"]),"An original equality fails on the face affine hull.")
        for i,x in vec.items(): residual[i]-=w*x
        dual_objective+=w*rhs
        base_equations.append(vec);equation_rhs.append(rhs);equation_names.append(eq["name"])
    require(len(base_equations)==2,"Unexpected original equality count.")
    source_lookup={v:r["id"] for r in source.rows for v in [source.vectors[r["id"]]]}
    matches={r["id"]:[] for r in source.rows}
    point_slacks=[]
    all_restrictions=[]
    positive_payments=[]
    literal_hashes_verified=0
    for i,(raw,w,provided) in enumerate(zip(rows,y,face["all_raw_inequality_restrictions"])):
        vec=sparse_vector(raw["a"])
        rhs=exact(raw.get("rhs","0"))
        slack=sparse_dot(vec,point)-rhs
        require(slack>=0 and slack==exact(certificate["raw_row_slacks"][i])==exact(certificate_check["all_raw_row_slacks"][i]),"A v6 raw point slack disagrees.")
        require(w*slack==0,"Raw-row complementarity failed.")
        form=sparse_affine(vec,origin,directions,rhs)
        require(provided["raw_index"]==i and provided["name"]==raw["name"] and provided["family"]==raw["family"] and exact(provided["original_rhs"])==rhs,"A face row lost its original identity.")
        require(same_form(form,provided),"A full raw parameter inequality is wrong.")
        canonical=digest(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
        if canonical==provided["literal_raw_row_sha256"]: literal_hashes_verified+=1
        point_slacks.append(slack)
        all_restrictions.append(dict(raw_index=i,name=raw["name"],family=raw["family"],original_rhs=rhs,**form))
        dense=tuple(vec.get(c,F(0)) for c in range(513))
        if rhs==0 and dense in source_lookup:
            matches[source_lookup[dense]].append(dict(raw_index=i,name=raw["name"],family=raw["family"],actual_raw_dual_weight=w))
        if w:
            for c,x in vec.items(): residual[c]-=w*x
            dual_objective+=w*rhs
            require(form["constant"]==0 and not any(form["coefficients"]),"A positive-payment equality fails on the face affine hull.")
            base_equations.append(vec);equation_rhs.append(rhs);equation_names.append(raw["name"])
            positive_payments.append(dict(raw_index=i,weight=w,point_slack=slack,
                raw_metadata={name:z for name,z in raw.items() if name!="a"},
                literal_585_row_id=source_lookup.get(dense),face_form=form))
    require(all(x>=0 for x in residual),"The dual column residual is negative.")
    require(residual==[exact(x) for x in certificate["dual"]["nonnegative_column_residual"]],"Dual stationarity residual mismatch.")
    require(all(point[i]*residual[i]==0 for i in range(513)),"Column complementarity failed.")
    require(dual_objective==value,"Exact primal-dual gap is nonzero.")
    zero_columns=[i for i,x in enumerate(residual) if x==0]
    forced=[i for i,x in enumerate(residual) if x>0]
    require(zero_columns==face["zero_residual_columns"]==sorted(present),"The full zero-residual support is not preserved.")
    require(forced==face["forced_zero_columns"],"The forced-zero columns are wrong.")
    require(face["nonnegative_coordinates_required"]==zero_columns,"A potentially nonzero face column was excluded.")
    for i,provided in enumerate(face["all513_nonnegative_coordinate_restrictions"]):
        require(provided["column"]==i and provided["forced_zero"]==(i in forced),"A coordinate condition lost its identity.")
        require(origin[i]==exact(provided["constant"]) and [d[i] for d in directions]==[exact(x) for x in provided["parameter_coefficients"]],"A nonnegative coordinate parameter condition is wrong.")
    rank=rational_rank([[vec.get(i,F(0)) for i in zero_columns] for vec in base_equations])
    require(rank==14==face["restricted_equation_rank"] and len(zero_columns)-rank==k,"The full complementary equation rank is wrong.")
    require(face["equation_names"]==equation_names and [exact(x) for x in face["equation_rhs"]]==equation_rhs,"The face equation identities differ.")
    require(rational_rank(directions)==k,"Face parameter directions are not independent.")
    for rec in face.get("diagnostic_functionals",[]):
        form=sparse_affine(sparse_vector(rec["full_coefficients"]),origin,directions)
        require(same_form(form,rec),"A supplied diagnostic functional is wrong.")
    report=dict(status="PASS_INDEPENDENT_FULL_V6_PRIMAL_DUAL_AND_FACE",bindings=bindings,
        bit_columns_checked=512,independent_K_checked=True,raw_point_slacks_checked=4177,
        all_raw_parameter_restrictions_checked=4177,all_nonnegative_coordinate_conditions_checked=513,
        original_equalities_checked=2,positive_raw_payments=len(positive),zero_residual_columns=zero_columns,
        forced_zero_columns=forced,restricted_equation_rank=rank,unconstrained_affine_parameters=k,
        relative_feasible_dimension="not asserted",objective=value,duality_gap=value-dual_objective,
        raw_row_literal_hashes_verified=literal_hashes_verified,actual_positive_payments=positive_payments,
        optimizer_calls=0,source_builder_imported=False,solver_imported=False,
        scope="The entire optimal face is exactly this affine parametrization intersected with every retained 4177 raw and 513 coordinate inequality; no realization as an SPE is implied.")
    return point,origin,directions,parameters,matches,report


def classify_face_form(form,point_slack):
    fixed=not any(form["coefficients"])
    if fixed:
        return dict(affine_hull_status="identically_"+sign(form["constant"]),
                    point_excluded_by_negative_row=point_slack<0,
                    entire_face_excluded_by_negative_row=form["constant"]<0,
                    proof="All parameter coefficients vanish exactly.")
    return dict(affine_hull_status="nonconstant",point_excluded_by_negative_row=point_slack<0,
                entire_face_excluded_by_negative_row=None,
                proof="No sign over the whole constrained face is inferred from one point. The full 4177+513 parameter domain is retained; no optimizer is invoked.")


def face_equality_checklist(source,row,origin,directions):
    result=dict(row_id=row["id"],blueprint=true_budget_blueprint(row),classes=[])
    if row["mode"]=="pure":
        target=row["target"]
        col=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
        for p,t,o in product((0,1),repeat=3):
            vector=tuple(F(int((b[0],b[col],b[7])==(p,t,o))) for b in BITS)+(F(0),)
            result["classes"].append(dict(p=p,t=t,o=o,mass=affine_form(vector,origin,directions),
                minimum_condition=source.condition(row,p,t,o),
                requirement="Every positive-mass customer must use one of these complete weak minima on this same actual forced history."))
    else:
        for p,o in product((0,1),repeat=2):
            vector=tuple(F(int((b[0],b[7])==(p,o))) for b in BITS)+(F(0),)
            conditions=[source.condition(row,p,0,0)] if not o else [source.condition(row,p,0,1),source.condition(row,p,1,1)]
            result["classes"].append(dict(p=p,o=o,mass=affine_form(vector,origin,directions),conditions=conditions))
    result["actual_A2_observable_forms"]=[{k:v for k,v in term.items() if k!="coefficients"}|dict(affine=affine_form(term["coefficients"],origin,directions)) for term in a2_equality_forms(source,row)]
    return result


def shared_C_zero_obstruction(source,zero_rows,point,origin,directions,matches):
    """Conditional real-history contradiction, kept distinct from a new raw row."""
    needed=["cap3full_pure_s0_v3_general_C","cap3full_pure_sstar_v6_C-only_C"]
    if not set(needed).issubset({r["id"] for r in zero_rows}):
        return dict(status="NOT_APPLICABLE",reason="The two independently required C zero rows are not both present.")
    selected=[source.by_id[rid] for rid in needed]
    for row in selected:
        require(all(exact(row["beta_actual"][str(j)])>0 for j in (3,4)),"A zero CAP weight cannot force a capacity equality.")
        require(any(rec["actual_raw_dual_weight"]>0 for rec in matches[row["id"]]),"The stated positive dual payment does not support this exact raw row.")
    outside=tuple(F(int(b[8] and not b[7])) for b in BITS)+(F(0),)
    outside_form=affine_form(outside,origin,directions)
    require(outside_form["constant"]==0 and not any(outside_form["coefficients"]),"C outside O does not vanish on the complete affine face.")
    classes=[]
    common={}
    for p,c,o in product((0,1),repeat=3):
        all_sets=[source.minima(row,p,c,F(o,6))[1] for row in selected]
        intersection=sorted(set.intersection(*(set(tails) for tails in all_sets)))
        common[p,c,o]=intersection
        vec=tuple(F(int((b[0],b[8],b[7])==(p,c,o))) for b in BITS)+(F(0),)
        classes.append(dict(p=p,c=c,o=o,each_complete_weak_set=all_sets,
                            common_tails=intersection,mass_point=dot(vec,point),mass_affine=affine_form(vec,origin,directions)))
    require(common[0,1,1]==["1111"] and common[1,1,1]==["1101","1110"],"The actual common C tails differ from the asserted obstruction.")
    for p in (0,1):
        for tail in common[p,1,1]:
            require(tail[:2]=="11","C coverage by R3,R4 is not forced.")
            r=tuple(map(int,tail))
            require(F(r[1],p+1+sum(r))==F(1,5),"The real player-4 payoff on C is not 1/5.")
    require(all(exact(row["tau"]["4"])>0 for row in selected),"The original SAFE4 weight is not positive.")
    safe_vector=tuple(F(b[7],6*(b[0]+2*b[8]+3)) for b in BITS)+(F(-1,5),)
    safe_form=affine_form(safe_vector,origin,directions)
    safe_point=dot(safe_vector,point)
    require(safe_point==safe_form["constant"] and not any(safe_form["coefficients"]),"The SAFE4 obstruction is not constant on the new complete face.")
    require(safe_point>0,"The conditional SAFE4 obstruction is not strictly positive.")
    expected=F(709638185136480929581839920970892210591292722310716,67588301606736414838046729267264655707163775139064531)
    require(safe_point==expected,"The independently rebuilt SAFE4 deficit differs from the announced diagnostic.")
    return dict(status="PASS_CONDITIONAL_TRUE_HISTORY_EXCLUSION_OF_ENTIRE_V6_OPTIMAL_FACE",
        row_ids=needed,actual_positive_raw_payments={rid:matches[rid] for rid in needed},
        all_common_weak_classes=classes,C_outside_O_affine=outside_form,
        deductions=[
            "Assume an SPE realizes a point in the full face. Each paid zero raw row has its own nonnegative true-budget and projection decomposition.",
            "Both rows force the same source-2 action C and therefore the same complete-strategy successor. Their weak tail sets must be intersected, not chosen on separate histories.",
            "C is contained in O up to zero customer mass. On C outside A1 the common tail is 1111; on C inside A1 it is 1101 or 1110.",
            "Consequently R3 and R4 contain C. Their strictly positive CAP weights force size(R3)=size(R4)=K=size(C), hence R3=R4=C up to zero mass.",
            "The actual player-4 payoff on this C successor is exactly K/5: each customer of C has total load five, and R4 has no customers outside C.",
            "At the true player-4 prefix the six-query SAFE lower bound is at least N4=sum_x o_x/[6(p_x+2c_x+3)]. It uses the given strategy at each new query history.",
            "The displayed N4-K/5 is strictly positive throughout the full face. Some legal query index therefore gives a true player-4 gain at least this amount under the zero-budget deductions, contradicting SPE."
        ],
        conditional_SAFE4_difference=dict(full_513_coefficients=safe_vector,point_value=safe_point,affine=safe_form,
            interpretation="N4-K/5 only after the paid-zero C-history deductions; this vector is not asserted to be an unconditional valid model inequality."),
        raw_585_negative_rows=0,raw_585_halfspace_exclusion=False,
        SPE_realization_exclusion=True,scope="entire exact v6 optimal face, with all 4177 raw and 513 coordinate conditions retained",
        not_an_SPE_counterexample=True,new_unconditional_row_constructed=False)


def synthetic_self_test():
    require(exact("-7/12")==F(-7,12),"Rational parsing test failed.")
    rejected=0
    for x in (0.25,"0.25",True,"1/0"):
        try: exact(x)
        except (ValueError,ZeroDivisionError): rejected+=1
    require(rejected==4,"Inexact or invalid coordinate was accepted.")
    negative=classify_face_form(dict(constant=F(-1),coefficients=[F(0)]),F(-1))
    variable=classify_face_form(dict(constant=F(-1),coefficients=[F(1)]),F(-1))
    require(negative["entire_face_excluded_by_negative_row"] is True,"Constant negative-face test failed.")
    require(variable["entire_face_excluded_by_negative_row"] is None,"A negative point was incorrectly promoted to a face exclusion.")
    require(rational_rank([[F(1),F(2)],[F(2),F(4)]])==1,"Rational rank test failed.")
    mem=solve_coordinates((F(1),F(0)),((F(0),F(1)),),(F(1),F(3)))
    require(mem["parameters"]==[F(3)],"Exact affine membership test failed.")
    return dict(status="PASS_SYNTHETIC_ARITHMETIC_AND_SCOPE_TESTS",inexact_inputs_rejected=4,
                point_vs_face_distinction_tested=True,optimizer_calls=0,LP_point_files_used=False)


def safe_output_directory(path):
    resolved=path.resolve()
    require(resolved==HERE or HERE in resolved.parents,"All new output must remain in this isolated diagnostic stage.")
    require(not (resolved/"freeze_manifest.json").exists(),"This diagnostic output is already frozen; do not overwrite it.")
    return resolved


def run(args):
    output=safe_output_directory(args.output_dir)
    source=Source(args.source_package)
    save(output,"synthetic_self_test.json",synthetic_self_test())
    source_report=verify_source(source)
    save(output,"source_true_COST_recheck.json",source_report)
    if args.command=="prepare":
        ready=dict(status="READY_AWAITING_EXPLICIT_V6_REFERENCE",diagnostic_completed=False,
                   run=RUN,boss="Boss1",agent_id="/root/source2_cap3_tradeoff",source=source.binding,
                   optimizer_calls=0,LP_point_or_face_read=False)
        save(output,"status.json",ready)
        print(json.dumps(ready,ensure_ascii=False))
        return
    require(args.solve_id==SOLVE,"The authorized solve id must be full4177_v6.")
    inputs={}
    bindings={}
    for key in ("input","certificate","face","certificate_check","face_check"):
        path=getattr(args,key)
        sha=getattr(args,key+"_sha256")
        require(path is not None and sha is not None,"An explicit path and SHA are required for "+key)
        inputs[key],bindings[key]=read_bound_json(path,sha)
    point,origin,directions,parameters,matches,core=validate_v6_core(inputs["input"],inputs["certificate"],inputs["face"],inputs["certificate_check"],inputs["face_check"],bindings,source)
    physical=contract_checks(point)
    require(physical["all_pass"],"The v6 point fails observable catalog prerequisites.")
    save(output,"input_binding.json",dict(run=RUN,boss="Boss1",agent_id="/root/source2_cap3_tradeoff",solve=SOLVE,
        inputs=bindings,source=source.binding,coordinate_order=ORDER,bit_order=inputs["input"]["bit_order"],
        explicit_new_v6_only=True,old_v5_read=False,optimizer_calls=0))
    save(output,"full_v6_core_recheck.json",core)
    save(output,"complete_face_parameter_domain.json",inputs["face"])
    save(output,"point_physical_contract.json",physical)
    point_rows=[]
    face_rows=[]
    zero_rows=[]
    negatives=[]
    equalities=[]
    face_equalities=[]
    counts=Counter()
    grouped=Counter()
    min_positive=None
    min_positive_ids=[]
    for row in source.rows:
        vec=source.vectors[row["id"]]
        slack=dot(vec,point)
        counts[sign(slack)]+=1
        grouped[(row["row_kind"],sign(slack))]+=1
        metadata={k:v for k,v in row.items() if k!="a"}
        record=dict(metadata=metadata,slack=slack,sign=sign(slack),source_513_vector_sha256=row["vector_sha256"],
                    literal_input_row_matches=matches[row["id"]])
        point_rows.append(record)
        form=affine_form(vec,origin,directions)
        require(evaluate_form(form,parameters)==slack,"585 row point and affine values disagree.")
        classification=classify_face_form(form,slack)
        face_rows.append(dict(row_id=row["id"],source_vertex=row["vertex_key"],delta=row["delta"],h=row["h"],s=row["s"],
            mode=row["mode"],target=row["target"],row_kind=row["row_kind"],affine=form,classification=classification))
        if slack<0: negatives.append(deviation_obligation(row,slack,physical))
        elif slack==0:
            zero_rows.append(row)
            equalities.append(equality_checklist(source,row,point,physical))
            face_equalities.append(face_equality_checklist(source,row,origin,directions))
        elif min_positive is None or slack<min_positive:
            min_positive=slack;min_positive_ids=[row["id"]]
        elif slack==min_positive: min_positive_ids.append(row["id"])
    obstruction=shared_C_zero_obstruction(source,zero_rows,point,origin,directions,matches)
    all_constant=all(not any(rec["affine"]["coefficients"]) for rec in face_rows)
    summary=dict(status="PASS_COMPLETED_NEW_V6_TRUE_DIAGNOSTIC",run=RUN,boss="Boss1",agent_id="/root/source2_cap3_tradeoff",
        solve=SOLVE,diagnostic_completed=True,rows=585,raw_columns_per_row=513,raw_point_coefficient_products=585*513,
        source_vertices=225,all_full_weak_state_tables_rebuilt=True,point_sign_counts=dict(counts),
        counts_by_row_kind=[dict(row_kind=k[0],sign=k[1],count=v) for k,v in sorted(grouped.items())],
        all_585_face_forms_constant=all_constant,exact_parameter_coefficients_checked=585*len(directions),
        zero_row_ids=[r["id"] for r in zero_rows],minimum_positive_slack=min_positive,minimum_positive_row_ids=min_positive_ids,
        negative_raw_point_exclusions=len(negatives),negative_raw_entire_face_exclusions=sum(rec["classification"]["entire_face_excluded_by_negative_row"] is True for rec in face_rows),
        conditional_zero_payment_true_history_obstruction=obstruction["status"],
        full_face_SPE_realization_excluded_by_zero_payment=obstruction.get("SPE_realization_exclusion",False),
        new_unconditional_inequality_constructed=False,
        affine_parameters=len(directions),relative_feasible_dimension="not asserted",retained_face_raw_inequalities=4177,
        retained_face_nonnegative_conditions=513,optimizer_calls=0,old_v5_read=False,
        distinction="All 585 linear rows pass on the full new face. The separate paid-zero true-history argument excludes SPE realization of that face; its conditional SAFE4 functional is not yet a new universal raw row.")
    save(output,"point_slacks_all585.json",dict(count=585,raw_scale=True,rows=point_rows))
    save(output,"face_affine_all585.json",dict(count=585,parameters=inputs["face"]["parameters"],domain_file="complete_face_parameter_domain.json",rows=face_rows))
    save(output,"negative_true_deviation_obligations.json",dict(count=len(negatives),records=negatives))
    save(output,"zero_point_true_equalities.json",dict(count=len(equalities),records=equalities))
    save(output,"zero_face_true_equalities.json",dict(count=len(face_equalities),records=face_equalities))
    save(output,"shared_C_zero_SAFE4_obstruction.json",obstruction)
    save(output,"diagnostic_summary.json",summary)
    save(output,"status.json",summary)
    print(json.dumps(serial(summary),ensure_ascii=False))


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=("prepare","run"))
    p.add_argument("--source-package",type=Path,default=DEFAULT_SOURCE)
    p.add_argument("--output-dir",type=Path,default=HERE)
    p.add_argument("--solve-id")
    for key in ("input","certificate","face","certificate-check","face-check"):
        p.add_argument("--"+key,type=Path)
        p.add_argument("--"+key+"-sha256")
    return p


if __name__=="__main__":
    args=parser().parse_args()
    try:
        run(args)
    except Exception as exc:
        directory=safe_output_directory(args.output_dir)
        path=directory/"failure_log.json"
        old=json.loads(path.read_text()) if path.exists() else []
        old.append(dict(utc=datetime.now(timezone.utc).isoformat(),error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc()))
        save(directory,"failure_log.json",old)
        raise
