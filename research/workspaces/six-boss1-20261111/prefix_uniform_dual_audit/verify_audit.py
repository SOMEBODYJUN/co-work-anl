#!/usr/bin/env python3
"""Independent audit from target minus true budgets; standard library only.

No Main script or other verifier is imported or executed. No optimizer or game
point is read. Gaussian elimination is exact arithmetic on the support equations.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
WS = OUT.parent
ROOT = OUT.parents[3]
SOURCES = [
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.md",
    "research/workspaces/six-boss1-20261111/main_prefix_cone_uniform_dual.md",
    "research/workspaces/six-boss1-20261111/main_prefix_cone_uniform_dual.py",
    "research/workspaces/six-boss1-20261111/main_prefix_cone_uniform_dual.json",
    "research/workspaces/six-boss1-20261111/early3_pair_cone.md",
    "research/workspaces/six-boss1-20261111/early3_pair_cone/exact_certificate.json",
    "research/workspaces/six-boss1-20261111/early3_pair_cone/old_dual_extension.json",
]


def dump(name, value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")


def dot(a,b):
    assert len(a)==len(b)
    return sum((x*y for x,y in zip(a,b)),F(0))


def true_budget_residual(r,typ,p,source_income=F(0)):
    """Direct payment, not the published affine coefficient formula."""
    n,k,x,*tail=typ
    middle,t,q=tail[:-2],tail[-2],tail[-1]
    assert len(middle)==r-2 and len(p)==2*r
    old=n-1
    continuation=middle+[t]
    C=sum(p[:r],F(0))
    kappa=F(x,old+r)
    query=q*(F(x,old+r)+F(1-x,old+1))
    target=C*source_income-(C-1)*kappa-query
    source_on_X=F(x,old+1+sum(continuation))
    paid=p[0]*(source_income-source_on_X)
    for pos,member in enumerate(continuation):
        paid+=p[1+pos]*(source_income-F(member,old+r))
        paid+=p[r+pos]*F(x-member,old+k+1)
    terminal_income=F(t,old+x+sum(middle)+1)
    terminal_query=F(q,old+x+sum(middle)+1)
    paid+=p[-1]*(terminal_income-terminal_query)
    return target-paid


def displayed_E(r,typ,p):
    n,k,x,*tail=typ
    middle,t,q=tail[:-2],tail[-2],tail[-1]
    j,D=sum(middle),n+r-1
    C=sum(p[:r],F(0))
    return (p[0]*F(x,n+j+t)
            +sum((p[1+l]*F(y,D) for l,y in enumerate(middle)),F(0))+p[r-1]*F(t,D)
            -(C-1)*F(x,D)-q*(F(x,D)+F(1-x,n))
            -sum((p[r+l]*F(x-y,n+k) for l,y in enumerate(middle)),F(0))
            -p[-2]*F(x-t,n+k)-p[-1]*F(t-q,n+x+j))


def affine_row(r,typ):
    zero=[F(0)]*(2*r)
    offset=true_budget_residual(r,typ,zero)
    coeff=[]
    for c in range(2*r):
        e=zero.copy(); e[c]=F(1)
        coeff.append(true_budget_residual(r,typ,e)-offset)
    return coeff,-offset


def solve_square(A,b):
    """Exact Gauss-Jordan; returns rank, determinant and unique solution."""
    n=len(A)
    assert n==len(b) and all(len(row)==n for row in A)
    M=[list(row)+[rhs] for row,rhs in zip(A,b)]
    rank=0
    determinant=F(1)
    for col in range(n):
        pivot=next((row for row in range(rank,n) if M[row][col]),None)
        if pivot is None:
            determinant=F(0)
            continue
        if pivot!=rank:
            M[pivot],M[rank]=M[rank],M[pivot]
            determinant=-determinant
        scale=M[rank][col]
        determinant*=scale
        M[rank]=[v/scale for v in M[rank]]
        for row in range(n):
            if row!=rank and M[row][col]:
                scale=M[row][col]
                M[row]=[a-scale*z for a,z in zip(M[row],M[rank])]
        rank+=1
    assert rank==n and determinant!=0
    assert all(M[row][col]==int(row==col) for row in range(n) for col in range(n))
    return rank,determinant,[row[-1] for row in M]


def support_closed(r,name,p):
    a,st,at,delta=p[0],p[r-1],p[-2],p[-1]
    if name=="A": return delta-1
    if name=="G": return st/r+at/(r-1)-delta
    if name=="H": return a/30-st/6+F(1,6)-at/(7-r)
    ell=int(name[1:])-1
    s,am=p[1+ell],p[r+ell]
    if name[0]=="B": return a/F(r*(r-1))-s/r-am+F(1,r)-delta/(r-1)
    assert name[0]=="D"
    return s/r+am/(r-1)+delta/2-1


def f(d,a): return F(a,d)
def g(d,a,b): return F(a*b,d*(d+1))
def U(d,a,b): return F(a,d+b)


def pair_terms(typ):
    n,k,x,y,z,t,q=typ
    d=n+x+y
    result=[]
    for L,R in ((q,x),(q,q),(x,x)):
        result.append(U(d,z,t)+U(d,t,z)+g(d,z,z)-f(d,L)-f(d,R)+g(d,L,R))
    return result


source_manifest={"sources":[{"path":path,"sha256":hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
                            for path in SOURCES]}
dump("source_manifest.json",source_manifest)
main_result=json.loads((WS/"main_prefix_cone_uniform_dual.json").read_text())
pair_cert=json.loads((WS/"early3_pair_cone/exact_certificate.json").read_text())
assert main_result["script_sha256"]==hashlib.sha256((WS/"main_prefix_cone_uniform_dual.py").read_bytes()).hexdigest()
assert main_result["source_proof_sha256"]==hashlib.sha256((WS/"main_prefix_safety_maxx_family.md").read_bytes()).hexdigest()
main_by_r={z["r"]:z for z in main_result["results"]}
results=[]
support_output=[]
r4_data=None

for r in (4,5,6):
    m,N=r-2,7-r
    types=[(n,k,*bits) for n in range(1,N+1) for k in range(m+1)
           for bits in product((0,1),repeat=r+1)]
    index={typ:i for i,typ in enumerate(types)}
    weights={"A":F(r*(-r*r+14*r-21),2*(r-1)),"G":F(r*(6*r-11),r-1),
             "H":F(30*m,r-1),"B":F(r,m),"D":F(r*(r-1),m)}
    rho=F(30*m,N*(r-1))-F(r*(6*r-11),(r-1)**2)
    star=F(r**3+10*r*r-31*r+22,2*(r-1))
    assert min([rho]+list(weights.values()))>0
    support=[("A",(1,0,0,*([0]*m),0,1)),
             ("G",(1,m,0,*([0]*m),1,0)),
             ("H",(N,0,1,*([1]*m),0,0))]
    for ell in range(m):
        e=[int(l==ell) for l in range(m)]
        support.append((f"B{ell+1}",(1,0,1,*(1-y for y in e),1,0)))
        support.append((f"D{ell+1}",(1,m,0,*e,0,1)))
    assert len(support)==2*r-1 and len(set(typ for _,typ in support))==2*r-1
    assert all(typ in index for _,typ in support)
    zero=[F(0)]*(2*r)
    basis=[zero]+[[F(int(c==j)) for c in range(2*r)] for j in range(2*r)]
    cost=[F(1)]*r+[F(0)]*r
    matrix,rhs,lambda_vec=[],[],[]
    for name,typ in support:
        row,h=affine_row(r,typ)
        matrix.append(row); rhs.append(h); lambda_vec.append(weights[name[0]])
        for p in basis:
            assert true_budget_residual(r,typ,p)==support_closed(r,name,p)
            assert true_budget_residual(r,typ,p)==true_budget_residual(r,typ,p,F(1))
        support_output.append({"r":r,"name":name,"type":list(typ),"row_index":index[typ],
                               "G":list(map(str,row)),"h":str(h),"lambda":str(weights[name[0]])})
    gt=[sum((w*row[c] for w,row in zip(lambda_vec,matrix)),F(0)) for c in range(2*r)]
    reduced=[cost[c]-gt[c] for c in range(2*r)]
    assert reduced==[F(0)]*(2*r-2)+[rho,F(0)]
    assert dot(rhs,lambda_vec)==star
    # The coefficient and constant tests establish UD for every real p.
    for p in basis:
        rhs_ud=sum((w*true_budget_residual(r,typ,p) for (_,typ),w in zip(support,lambda_vec)),F(0))
        rhs_ud+=rho*p[-2]
        assert dot(cost,p)-star==rhs_ud
    # Equalities forced at optimum: every support E=0, plus a_T=0.
    at_row=[F(0)]*(2*r);at_row[-2]=F(1)
    rank,det,unique=solve_square(matrix+[at_row],rhs+[F(0)])
    expected_a=F(-r*r+11*r-12,2*r*(r-2))
    expected_s=F(r,2)-F(r,r-1)*expected_a
    expected=[F(5*(r-1))]+[expected_s]*m+[F(r)]+[expected_a]*m+[F(0),F(1)]
    assert unique==expected and min(unique)>=0 and dot(cost,unique)==star
    assert unique[-2]==0 and unique[-1]==1 and unique[r-1]==r and unique[0]==5*(r-1)
    for ell in range(m):
        assert unique[1+ell]/r+unique[r+ell]/(r-1)==F(1,2)
        assert unique[1+ell]+r*unique[r+ell]==(unique[0]-1)/(r-1)
    determinant_middle=F(1,r)*r-F(1,r-1)
    assert determinant_middle==F(r-2,r-1)>0
    vals=[]
    payment_checks=0
    for typ in types:
        for p in basis:
            true_e=true_budget_residual(r,typ,p)
            assert true_e==displayed_E(r,typ,p)
            assert true_e==true_budget_residual(r,typ,p,F(1))
            payment_checks+=2
        vals.append(true_budget_residual(r,typ,unique))
    assert min(vals)>=0
    assert all(true_budget_residual(r,typ,unique)==0 for _,typ in support)
    saved=main_by_r[r]
    assert saved["variables"]==2*r and saved["types"]==len(types)
    assert saved["unique_primal"]==list(map(str,unique)) and saved["C"]==str(star)
    assert saved["positive_reduced_cost_for_terminal_MAX"]==str(rho)
    assert saved["zero_types"]==sum(v==0 for v in vals)
    assert saved["min_positive_remainder"]==str(min(v for v in vals if v>0))
    assert saved["uniqueness_determinant"]==str(determinant_middle)
    main_support={z["name"]:z for z in saved["support"]}
    for (name,typ),w in zip(support,lambda_vec):
        assert main_support[name]=={"name":name,"type":list(typ),"row_index":index[typ],"weight":str(w)}
    results.append({"r":r,"status":"PASS_UNIFORM_DUAL_AND_UNIQUENESS","types":len(types),
        "variables":2*r,"support_count":len(support),"all_support_types_legal_and_distinct":True,
        "C":str(star),"rho":str(rho),"reduced_cost":list(map(str,reduced)),
        "support_equations_plus_aT_zero_rank":rank,"equality_matrix_determinant":str(det),
        "middle_2by2_determinant":str(determinant_middle),"unique_weights":list(map(str,unique)),
        "affine_UD_checks":len(basis),"support_closed_form_checks":len(basis)*len(support),
        "all_type_payment_basis_checks":payment_checks,"all_type_primal_nonnegative":True,
        "zero_types":sum(v==0 for v in vals),"min_positive_remainder":str(min(v for v in vals if v>0)),
        "main_json_matches":True})
    if r==4:
        r4_data=(types,support,lambda_vec,matrix,rhs,unique,rho)

# Independently audit the exact four-term real PAIR payment, allowing arbitrary
# response bit J, on the complete possible d range and all five Boolean bits.
pair_payment_checks=0
for d in range(1,6):
    for z,t,L,R,J in product((0,1),repeat=5):
        pair=U(d,z,t)+U(d,t,z)+g(d,z,z)-f(d,L)-f(d,R)+g(d,L,R)
        paid=(U(d,z,t)-U(d,L,J))+(U(d,J,L)-U(d,R,L))
        paid+=(U(d,t,z)-U(d,J,z))+(g(d,z,z)-g(d,z,J))
        assert pair==paid and g(d,z,z)-g(d,z,J)>=0
        pair_payment_checks+=1

types,support,uniform_lam,matrix,rhs,unique,rho=r4_data
all_pair_rows=[]
all_pair_rhs=[]
for typ in types:
    row,h=affine_row(4,typ)
    T=pair_terms(typ)
    n,k,x,y,z,t,q=typ
    d=n+x+y
    H=F(z,d+t)+F(t,d+z)+F(z,d*(d+1))
    claimed_T=[H-F(q+x,d)+F(q*x,d*(d+1)),H-F(2*q,d)+F(q,d*(d+1)),
               H-F(2*x,d)+F(x,d*(d+1))]
    assert T==claimed_T
    all_pair_rows.append(row+[-v for v in T])
    all_pair_rhs.append(h)
pair_cost=[F(1)]*4+[F(0)]*7
old_lam=[F(0)]*len(types)
for v in pair_cert["dual_nonzero"]:
    assert list(types[v["index"]])==v["type"]
    old_lam[v["index"]]=F(v["lambda"])
old_gt=[sum((old_lam[i]*all_pair_rows[i][c] for i in range(len(types))),F(0)) for c in range(11)]
old_reduced=[c-z for c,z in zip(pair_cost,old_gt)]
eta_reduced=[F(6),F(1,3),F(139,6)]
assert old_reduced==[F(0)]*8+eta_reduced
assert old_reduced==list(map(F,pair_cert["dual_reduced_cost"]))
assert dot(all_pair_rhs,old_lam)==F(61,3)

# The new seven-support dual also extends directly, with positive aT and eta
# reduced costs; this is stronger than merely composing the two old conclusions.
indices=[types.index(typ) for _,typ in support]
uniform_gt=[sum((w*all_pair_rows[index][c] for w,index in zip(uniform_lam,indices)),F(0)) for c in range(11)]
uniform_reduced=[c-z for c,z in zip(pair_cost,uniform_gt)]
assert uniform_reduced==[F(0)]*6+[F(8,9),F(0)]+eta_reduced
assert dot([all_pair_rhs[i] for i in indices],uniform_lam)==F(61,3)
extended_basis=[[F(0)]*11]+[[F(int(c==j)) for c in range(11)] for j in range(11)]
for p in extended_basis:
    lhs=dot(pair_cost,p)-F(61,3)
    right=sum((w*(true_budget_residual(4,typ,p[:8])-dot(p[8:],pair_terms(typ)))
               for (_,typ),w in zip(support,uniform_lam)),F(0))
    right+=F(8,9)*p[6]+dot(eta_reduced,p[8:])
    assert lhs==right
pair_matrix=[all_pair_rows[i] for i in indices]
pair_rhs=[all_pair_rhs[i] for i in indices]
for c in (6,8,9,10):
    row=[F(0)]*11;row[c]=F(1)
    pair_matrix.append(row);pair_rhs.append(F(0))
pair_rank,pair_det,pair_unique=solve_square(pair_matrix,pair_rhs)
assert pair_unique==unique+[F(0)]*3==list(map(F,pair_cert["primal"]))
assert all(dot(row,pair_unique)-h>=0 for row,h in zip(all_pair_rows,all_pair_rhs))
pair_result={"status":"PASS_SPECIFIED_THREE_PAIR_UNIQUE_OPTIMUM","variables":11,"types":288,
    "pair_payment_identity_checks":pair_payment_checks,"pair_local_coefficients":3*len(types),
    "old_dual_eta_reduced_cost":list(map(str,old_reduced[8:])),
    "uniform_seven_support_extended_reduced_cost":list(map(str,uniform_reduced)),
    "uniform_pair_affine_identity_checks":len(extended_basis),
    "extended_equality_rank":pair_rank,"extended_equality_determinant":str(pair_det),
    "unique_weights":list(map(str,pair_unique)),"C":"61/3",
    "composition_claim_correct":True,"direct_uniform_extension_also_valid":True,
    "scope":"Only TP(Q,X), TP(Q,Q), TP(X,X) at h=(A1,A2,X,Y), with d=n+x+y"}
for source in source_manifest["sources"]:
    assert hashlib.sha256((ROOT/source["path"]).read_bytes()).hexdigest()==source["sha256"]
dump("support_coefficients.json",support_output)
result={"status":"PASS_INDEPENDENT_UNIFORM_DUAL_UNIQUENESS_AND_PAIR_AUDIT",
    "results":results,"specified_three_PAIR":pair_result,"optimizer_calls":0,"game_point_reads":0,
    "other_program_imports_or_executions":0,"source_hashes_stable":True,
    "arithmetic":"Python standard-library fractions.Fraction",
    "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope":"Specified certificate cones only; no actual SPE sharpness or six-player half claim"}
dump("audit_result.json",result)
print(json.dumps(result,ensure_ascii=False,indent=2))
