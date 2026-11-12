#!/usr/bin/env python3
"""Independent exact verifier.  Does not import the generator or project code.

Rebuilds literal individual-share budgets, enumerates independent active
boundary systems, and compares every monomial in all 513 coefficient columns.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parents[2]
ATOMS=list(product((0,1),repeat=9))
TARGETS=["A1","A2","A3","A4","A5","A6","X","C"]


def load(name):
    return json.loads((HERE/name).read_text())


def convert(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {str(k):convert(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [convert(v) for v in x]
    return x


def save(name,x):
    (HERE/name).write_text(json.dumps(convert(x),ensure_ascii=False,indent=2)+"\n")


def verify_pins():
    for p in load("source_pins.json")["sources"]:
        assert hashlib.sha256((ROOT/p["path"]).read_bytes()).hexdigest()==p["sha256"],p["path"]


def add(a,b): return [x+y for x,y in zip(a,b)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def scale(a,c): return [x*c for x in a]
def dot(a,x): return sum((v*w for v,w in zip(a,x)),Q(0))
def ev(a,x): return a[0]+dot(a[1:],x)
def vec(n,c=0,j=None):
    a=[Q(0)]*(n+1);a[0]=Q(c)
    if j is not None:a[j+1]=Q(1)
    return a


def linear_solve(matrix,rhs):
    n=len(rhs)
    if not n:return ()
    a=[list(map(Q,row))+[Q(b)] for row,b in zip(matrix,rhs)]
    for col in range(n):
        pivot=next((r for r in range(col,n) if a[r][col]),None)
        if pivot is None:return None
        a[col],a[pivot]=a[pivot],a[col]
        d=a[col][col];a[col]=[x/d for x in a[col]]
        for r in range(n):
            if r!=col and a[r][col]:
                d=a[r][col];a[r]=[x-d*y for x,y in zip(a[r],a[col])]
    return tuple(a[k][-1] for k in range(n))


def rank(rows):
    if not rows:return 0
    a=[list(map(Q,r)) for r in rows]
    pivot=0
    for c in range(len(a[0])):
        r=next((r for r in range(pivot,len(a)) if a[r][c]),None)
        if r is None:continue
        a[pivot],a[r]=a[r],a[pivot]
        d=a[pivot][c];a[pivot]=[x/d for x in a[pivot]]
        for s in range(len(a)):
            if s!=pivot and a[s][c]:
                d=a[s][c];a[s]=[x-d*y for x,y in zip(a[s],a[pivot])]
        pivot+=1
        if pivot==len(a):break
    return pivot


def vertices(ineqs,n):
    got=set();attempts=0
    for combo in combinations(range(len(ineqs)),n):
        attempts+=1
        x=linear_solve([ineqs[k][1:] for k in combo],[-ineqs[k][0] for k in combo])
        if x is not None and all(ev(a,x)>=0 for a in ineqs):got.add(x)
    return got,attempts


def literal_affine(i,q0,p,t,q,r,z,terminal=Q(1)):
    js=list(range(i+1,6));n=len(js)+1
    lam=vec(n,25,0)
    tau={j:vec(n,0,k+1) for k,j in enumerate(js)}
    a=lam
    for j in js:a=add(a,tau[j])
    beta={}
    for j in js:
        beta[j]=add(vec(n,terminal*q0/2),tau[j])
        for l in js:
            if l>j:beta[j]=add(beta[j],scale(tau[l],q0/((7-l)*(8-l))))
    L=p+t+sum(r.values())+z
    # Add each real wallet term separately, avoiding the displayed compressed rho.
    total=vec(n)
    if L:
        total=add(total,scale(a,Q(t,L)))
        total=add(total,vec(n,-terminal*Q(z,L)))
        for j in js:total=sub(total,scale(tau[j],Q(r[j],L)))
    for j in js:total=add(total,scale(beta[j],r[j]))
    total=add(total,vec(n,terminal*z))
    total=add(total,vec(n,terminal*q/(p+t+sum(r.values())+1)))
    for j in js:
        denominator=p+t+sum(r[h] for h in js if h<j)+7-j
        total=add(total,scale(tau[j],q/denominator))
    return total,beta,tau,lam


def literal_numeric(i,q0,lam,tau,p,t,q,r,z,terminal=Q(1)):
    a=lam+sum(tau.values(),Q(0))
    beta={j:terminal*q0/2+tau[j]+sum((q0*tau[h]/((7-h)*(8-h)) for h in tau if h>j),Q(0)) for j in tau}
    L=p+t+sum(r.values())+z
    total=Q(0)
    if L:
        total+=a*Q(t,L)
        for j in tau:total-=tau[j]*Q(r[j],L)
        total-=terminal*Q(z,L)
    for j in tau:total+=beta[j]*r[j]
    total+=terminal*z
    total+=terminal*q/(p+t+sum(r.values())+1)
    for j in tau:total+=tau[j]*q/(p+t+sum(r[h] for h in tau if h<j)+7-j)
    return total


def states_and_geometry():
    cert=load("all_state_certificates.json")
    domains=load("parameter_domains.json")["domains"]
    records=[];boundary_attempts=0;ray_attempts=0;facet_checks=0
    for dom in domains:
        i=dom["source"];q0=Q(dom["q0"]);js=dom["middle_sources"];n=len(js)+1
        facets=[]
        for f in dom["facets"]:
            a=list(map(Q,f["affine_in_delta_tau"]))
            if f["id"]=="lambda_ge_25": expected=vec(n,0,0)
            elif f["id"].startswith("tau"):
                j=int(f["id"].split("_")[0][3:]);expected=vec(n,0,js.index(j)+1)
            else:
                j=int(f["id"].split("_")[0][1:]);r={h:int(h!=j) for h in js}
                value,beta,tau,lam=literal_affine(i,q0,i-1,1,Q(0),r,1)
                W=vec(n,1)
                for b in beta.values():W=add(W,b)
                W=add(W,scale(sub(lam,vec(n,1)),Q(1,6)))
                expected=sub(value,W)
            assert a==expected
            facets.append(a)
        got,count=vertices(facets,n);boundary_attempts+=count
        stored={(Q(0),)+tuple(map(Q,v["tau"])) for v in dom["vertices"]}
        assert got==stored
        # Independent ray slice: delta_lambda=1 in the homogeneous inequalities.
        rayineq=[[a[1]]+a[2:] for a in facets[1:]]
        rays,count=vertices(rayineq,n-1);ray_attempts+=count
        stored_rays={tuple(map(Q,r["delta_tau"])) for r in dom["extreme_rays"]}
        assert rays==stored_rays
        # No nonzero recession vector has delta_lambda=0: each tau is >=0 and
        # each positive diagonal cap is <=0.  Thus this slice is complete.
        for a in facets:
            support=[x for x in got if ev(a,x)==0]
            assert support
            dirs=[sub(x,support[0]) for x in support[1:]]
            dirs += [[Q(1)]+list(v) for v in rays if dot(a[1:],[Q(1)]+list(v))==0]
            assert rank(dirs)==n-1
            facet_checks+=1
        strict=(Q(1),)+tuple(Q(1,100) for _ in js)
        assert all(ev(a,strict)>0 for a in facets)
        records.append({"source":i,"q0":q0,"vertices":len(got),"rays":len(rays),"facets":len(facets),"all_facets_support_rank":n-1,"strict_interior":strict})
    zero_counts={key:0 for key in cert if isinstance(cert[key],list)}
    for item in cert["t1_zero_query"]:
        i=item["source"];q0=Q(item["q0"]);js=list(range(i+1,6));n=len(js)+1
        p=item["p"];D=item["D"];r=dict(zip(js,item["middle_bits"]));z=item["z"]
        value,beta,tau,lam=literal_affine(i,q0,p,1,Q(0),r,z)
        W=vec(n,1)
        for b in beta.values():W=add(W,b)
        W=add(W,scale(sub(lam,vec(n,1)),Q(1,D)))
        rho=sub(value,W)
        assert rho==list(map(Q,item["rho"]))
        paid=list(map(Q,item["remaining_nonnegative_affine"]))
        assert all(x>=0 for x in paid)
        for j,w in item["g_weights"].items():
            j=int(j)
            g=sub(add(scale(sub(lam,vec(n,1)),Q(1,30)),scale(tau[j],Q(1,5))),beta[j])
            paid=add(paid,scale(g,Q(w)))
        assert paid==rho
        zero_counts["t1_zero_query"]+=1
    for item in cert["t0_zero_tail"]:
        i=item["source"];q0=Q(item["q0"]);js=list(range(i+1,6));n=len(js)+1;p=item["p"];q=Q(item["q"])
        r=dict(zip(js,item["middle_bits"]));z=item["z"]
        value,beta,tau,lam=literal_affine(i,q0,p,0,q,r,z)
        Z=vec(n,q/(p+1))
        for j in js:Z=add(Z,scale(tau[j],q/(p+7-j)))
        residual=sub(value,Z)
        assert residual==list(map(Q,item["nonnegative_affine"])) and all(x>=0 for x in residual)
        zero_counts["t0_zero_tail"]+=1
    for item in cert["t1_query_slope"]:
        i=item["source"];q0=Q(item["q0"]);js=list(range(i+1,6));n=len(js)+1;p=item["p"];D=p+7-i
        r=dict(zip(js,item["middle_bits"]));z=item["z"]
        v1,_,tau,_=literal_affine(i,q0,p,1,Q(1),r,z)
        v0,_,_,_=literal_affine(i,q0,p,1,Q(0),r,z)
        anchor=vec(n,Q(1,D))
        for a in tau.values():anchor=add(anchor,scale(a,Q(1,D)))
        delta=sub(sub(v1,v0),anchor)
        assert delta==list(map(Q,item["nonnegative_slope_difference"])) and all(x>=0 for x in delta)
        zero_counts["t1_query_slope"]+=1
    save("literal_geometry_checks.json",{"domains":records,"active_boundary_combinations":boundary_attempts,"ray_slice_boundary_combinations":ray_attempts,"facet_rank_checks":facet_checks,"literal_state_counts":zero_counts})
    return boundary_attempts,ray_attempts,facet_checks,zero_counts


def polynomial_product(a,b):
    """Coefficient array for degree <=2, directly from affine arrays."""
    n=len(a)-1
    terms={():a[0]*b[0]}
    for j in range(n):terms[(j,)]=a[0]*b[j+1]+a[j+1]*b[0]
    for j in range(n):
        for k in range(j,n):
            terms[(j,k)]=a[j+1]*b[k+1]+(a[k+1]*b[j+1] if j!=k else 0)
    return terms


def polynomial_add(a,b):
    keys=set(a)|set(b)
    return {key:a.get(key,Q(0))+b.get(key,Q(0)) for key in keys}


def polynomial_affine(a):
    return {():a[0],**{(j,):a[j+1] for j in range(len(a)-1)}}


def symbolic_columns():
    report=[];scalars=0;columns=0
    for i in range(1,6):
        for kind,target in [("pure",t) for t in TARGETS]+[("C-only","C"),("ordered","C")]:
            q0=Q(1,5) if kind=="ordered" else Q(1,6)
            js=list(range(i+1,6));m=len(js);S0=1+m*q0/2;L=24-15*q0
            b=[1+(j-i-1)*q0/((7-j)*(8-j)) for j in js]
            H=[S0]+[L*x for x in b]
            V=[Q(0)]+b
            s=[S0]+[-15*q0*x for x in b]
            e=[Q(0)]+[S0-x for x in b]
            all_slack=[]
            for p in range(i):
                for j,bj in zip(js,b):
                    D=p+7-i
                    bracket=bj/(p+1)+(S0-bj)/D-S0/(p+7-j)
                    assert bracket>=0 and bj>=S0/2
                    assert 2*(j-i)*(p+1)<=(6-i)*(p+7-j)
                    all_slack.append(bracket)
            count=0
            digest=hashlib.sha256()
            for col,atom in enumerate(ATOMS+[None]):
                K=int(atom is None)
                if atom is None:
                    p=t=o=c=0;u=Q(0);D=7-i
                else:
                    p=sum(atom[:i-1]);D=p+7-i;o=atom[7];c=atom[8]
                    t=atom[int(target[1:])-1] if target.startswith("A") else atom[6 if target=="X" else 8]
                    u=Q(atom[i-1],sum(atom[:6])) if sum(atom[:6]) else Q(0)
                safeT=u-Q(t,D);safeO=u-Q(o,6*D);EQ=Q(c-K)
                if kind=="ordered":
                    derivative=[u+bj*(K-Q(o,6))-Q(o,6*(p+7-j)) for j,bj in zip(js,b)]
                    ray=[safeO]+derivative
                    endpoint=[25*u+S0*(K-Q(o,6))-Q(4*o,D)-Q(o,6*(p+1))]+[L*x for x in derivative]
                    known=scale(add(s,e),safeO)
                else:
                    derivative=[u+bj*(K-t)-Q(o,6*(p+(j-i)*t+7-j)) for j,bj in zip(js,b)]
                    ray=[safeT]+derivative
                    endpoint=[25*u+S0*(K-t)-Q(24*t,D)-Q(o,6*(p+1+(6-i)*t))]+[L*x for x in derivative]
                    known=add(scale(s,safeT),scale(e,safeO))
                    if kind=="C-only":
                        ray=add(ray,scale(V,EQ))
                        endpoint=add(endpoint,scale([S0-1]+[L*x for x in b],EQ))
                        known=add(known,scale(V,EQ))
                rem=[Q(0)]+[Q(o,6)*(bj/(p+1)+(S0-bj)/D-S0/(p+7-j))*(1 if kind=="ordered" else 1-t) for j,bj in zip(js,b)]
                assert all(x>=0 for x in rem)
                left=polynomial_product(H,ray)
                right=polynomial_add(polynomial_product(V,endpoint),polynomial_affine(add(known,rem)))
                assert left==right,(i,kind,target,col,left,right)
                count+=len(left)
                digest.update(json.dumps([col,[(str(k),str(left[k])) for k in sorted(left)]],sort_keys=True).encode()+b"\n")
            assert count==513*(m+1)*(m+2)//2
            report.append({"source":i,"kind":kind,"target":target,"all_columns":513,"all_monomial_coefficients":count,"left_equals_right":True,"lhs_sha256":digest.hexdigest(),"minimum_slack_bracket":min(all_slack) if all_slack else None})
            scalars+=count;columns+=513
    expected=load("symbolic_column_checks.json")["checks"]
    assert sum(r["all_degree_at_most_two_coefficients"] for r in expected)==scalars
    assert len(expected)==len(report)
    save("literal_symbolic_column_checks.json",{"method":"independent affine coefficient arrays and explicit quadratic multiplication; every monomial compared, no point sampling","checks":report})
    return columns,scalars


def literal_minimum(i,q0,lam,tau,p,t,q,terminal):
    values=[];js=list(tau)
    for bit in product((0,1),repeat=len(js)+1):
        r=dict(zip(js,bit[:-1]))
        value=literal_numeric(i,q0,lam,tau,p,t,q,r,bit[-1],terminal)
        values.append((value,bit))
    low=min(x for x,_ in values)
    return low,[bit for value,bit in values if value==low],len(values)


def numeric_weak_states_and_endpoints():
    domains=load("parameter_domains.json")["domains"]
    minima=[];hidden=0;attainers=0;ordered_outer=0
    base_min={}
    for dom in domains:
        i=dom["source"];q0=Q(dom["q0"]);js=dom["middle_sources"]
        for is_ray in (False,True):
            for item in dom["extreme_rays"] if is_ray else dom["vertices"]:
                tau=dict(zip(js,map(Q,item["delta_tau"] if is_ray else item["tau"])))
                lam=Q(1) if is_ray else Q(25);terminal=Q(0) if is_ray else Q(1)
                tables={}
                for p in range(i):
                    conditions=[(t,d) for t in (0,1) for d in (range(t,6+t) if q0==Q(1,5) else range(7))]
                    for t,d in conditions:
                        q=Q(d-t,5) if q0==Q(1,5) else Q(d,6)
                        low,weak,number=literal_minimum(i,q0,lam,tau,p,t,q,terminal)
                        hidden+=number;attainers+=len(weak)
                        tables[p,t,d]=low
                        minima.append({"parameter_id":item["id"],"ray_budget":is_ray,"p":p,"t":t,"d":d,"q":q,"minimum":low,"all_attaining_tails":weak})
                    if q0==Q(1,5):
                        G=(5*tables[p,0,1]+tables[p,1,1])/6
                        for d in range(7):
                            f=(Q(6-d)*tables[p,0,d] if d<6 else Q(0))+(Q(d)*tables[p,1,d] if d>0 else Q(0))
                            f/=6
                            assert f==0 if d==0 else (f==G if d==1 else f>G)
                            ordered_outer+=1
                if not is_ray:base_min[item["id"]]=(dom,tau,tables)
    save("literal_minimum_tables.json",{"all_weak_attainers_preserved":True,"tables":minima})
    links=load("endpoint_correspondence.json")["links"]
    rows={}
    for link in links:
        p=link["old_package"]
        if p not in rows:rows[p]={r["name"]:r for r in json.loads((ROOT/p).read_text())["rows"]}
    checked=0
    for link in links:
        dom,tau,tables=base_min[link["new_base_vertex"]]
        i=dom["source"];q0=Q(dom["q0"]);target=link["target"]
        caps={j:q0/2+tau[j]+sum((q0*tau[h]/((7-h)*(8-h)) for h in tau if h>j),Q(0)) for j in tau}
        S=1+sum(caps.values(),Q(0));a=25+sum(tau.values(),Q(0))
        old=rows[link["old_package"]][link["old_row_name"]]
        digest=hashlib.sha256()
        for col,atom in enumerate(ATOMS+[None]):
            if atom is None:value=S
            else:
                p=sum(atom[:i-1]);o=atom[7]
                u=Q(atom[i-1],sum(atom[:6])) if sum(atom[:6]) else Q(0)
                if target=="ordered":lower=o*(5*tables[p,0,1]+tables[p,1,1])/6
                else:
                    t=atom[int(target[1:])-1] if target.startswith("A") else atom[6 if target=="X" else 8]
                    lower=tables[p,t,o]
                value=a*u-lower
            assert value==Q(old["a"][str(col)])
            digest.update((str(value)+"\n").encode());checked+=1
        assert digest.hexdigest()==link["raw_coefficients_sha256"]
    return len(minima),hidden,attainers,ordered_outer,checked


def main():
    verify_pins()
    a,b,c,state_counts=states_and_geometry()
    columns,scalars=symbolic_columns()
    tables,hidden,weak,outer,old=numeric_weak_states_and_endpoints()
    # Index exclusion and SAFE projection are checked again directly per menu.
    menus=0;inner=0
    for i in range(1,6):
        for p in range(i):
            D=p+7-i
            for bits in product((0,1),repeat=6):
                d=sum(bits);o=int(d>0)
                assert sum((Q(x,6*D) for x in bits),Q(0))-Q(o,6*D)==Q(d-o,6*D)>=0
                for k,t in enumerate(bits):
                    assert sum((Q(bits[l],5) for l in range(6) if l!=k),Q(0))==Q(d-t,5)
                    inner+=1
                menus+=1
    verify_pins()
    result={"status":"PASS","independent_of_generator_imports":True,"optimizer_calls":0,"global_candidate_or_optimal_face_reads":0,"full_geometry_boundary_combinations":a,"ray_slice_boundary_combinations":b,"facet_rank_checks":c,"all_literal_state_certificates":state_counts,"symbolic_full_columns":columns,"symbolic_all_monomial_coefficients":scalars,"literal_physical_minimum_tables":tables,"literal_hidden_tail_costs":hidden,"all_weak_attainer_occurrences":weak,"ordered_multiplicity_values":outer,"existing_endpoint_literal_columns":old,"actual_SAFE_projection_menus":menus,"actual_inner5_index_checks":inner,"source_pins_unchanged":True,"new_raw_matrix_materialized":False}
    save("literal_checker_output.json",result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":main()
