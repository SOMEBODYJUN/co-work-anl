#!/usr/bin/env python3
"""Independent exact verifier: standard library, original E, no solver import.

Rebuilds the affine row coefficients using basis evaluations of the displayed
per-customer remainder; also checks the payment identity directly. No discovery
module, numerical LP output, fixed game point, or strategy selector is loaded.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import csv
import hashlib
import json

F = Fraction
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def dot(a, b):
    assert len(a) == len(b)
    return sum((v*w for v,w in zip(a,b)), F(0))


def remainder(r, typ, p):
    n,k,x,*end = typ
    ys,t,q = end[:-2],end[-2],end[-1]
    m = r-2
    assert len(ys) == m and len(p) == 2*r
    alpha = p[0]
    safe = p[1:r]
    maximum = p[r:2*r-1]
    delta = p[-1]
    C = alpha + sum(safe,F(0))
    D = n+r-1
    ans = alpha*F(x,n+sum(ys)+t)
    ans += dot(safe,[F(y,D) for y in ys]+[F(t,D)])
    ans -= (C-1)*F(x,D)
    ans -= q*(F(x,D)+F(1-x,n))
    ans -= dot(maximum,[F(x-y,n+k) for y in ys]+[F(x-t,n+k)])
    ans -= delta*F(t-q,n+x+sum(ys))
    return ans


def paid_remainder(r,typ,p,u):
    """Target minus separately reconstructed IC, SAFE, MAX, terminal budgets."""
    n,k,x,*end = typ
    ys,t,q = end[:-2],end[-2],end[-1]
    rbits = ys+[t]
    b = n-1
    C = sum(p[:r],F(0))
    kappa = F(x,b+r)
    query = q*(F(x,b+r)+F(1-x,b+1))
    forced_source_income = F(x,b+1+sum(rbits))
    target = C*u-(C-1)*kappa-query
    paid = p[0]*(u-forced_source_income)
    for z,s,a in zip(rbits,p[1:r],p[r:2*r-1]):
        paid += s*(u-F(z,b+r))
        paid += a*F(x-z,b+k+1)
    terminal_income = F(t,b+x+sum(ys)+1)
    terminal_deviation = F(q,b+x+sum(ys)+1)
    paid += p[-1]*(terminal_income-terminal_deviation)
    return target-paid


def base(r,n,j,x,t,p):
    m = r-2
    alpha,s,st,a,at,delta = p[0],p[1],p[r-1],p[r],p[-2],p[-1]
    assert p[1:r-1] == [s]*m and p[r:2*r-2] == [a]*m
    assert st == r and at == 0 and delta == 1
    C = alpha+m*s+st
    D = n+r-1
    if x == 0:
        return (s*j+r*t)/D + F(a*j,n+m) + F(1-t,n+j)-F(1,n)
    return (alpha/F(n+j+t)+(s*j+r*t-C+1)/D
            -a*F(m-j,n)-F(t,n+1+j))


summaries = []
source_checks = []
for item in read("source_manifest.json")["sources"]:
    actual = hashlib.sha256((ROOT/item["path"]).read_bytes()).hexdigest()
    assert actual == item["sha256"], (item["path"],"SOURCE_CHANGED")
    source_checks.append({"path":item["path"],"sha256":actual,"match":True})
main_json = json.loads((ROOT/"research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.json").read_text())
main_atoms = {(a["r"],a["b"]+1,a["k"],*a["bits"]):F(a["remainder"])
              for a in main_json["atoms"] if a["r"] in (5,6)}
assert len(main_atoms) == 1152

for r in (5,6):
    m = r-2
    cert = read(f"exact_certificate_r{r}.json")
    table = read(f"all_types_r{r}.json")
    assert cert["status"] == "EXACT_PRIMAL_DUAL_PASS"
    p = list(map(F,cert["primal"]))
    sym = list(map(F,cert["symmetric_primal"]))
    guard = list(map(F,cert["main_primal"]))
    cost = [F(1)]*r+[F(0)]*r
    assert len(p) == len(sym) == len(guard) == 2*r
    assert min(p) >= 0 and min(sym) >= 0 and min(guard) >= 0
    assert table["objective"] == cost
    assert dot(cost,p) == dot(cost,sym) == dot(cost,guard) == F(cert["C"])
    assert F(cert["improvement_from_main"]) == 0
    assert F(cert["C"]) == {5:F(121,4),6:F(206,5)}[r]
    zero = [F(0)]*(2*r)
    basis = [zero]
    for j in range(2*r):
        e = zero.copy()
        e[j] = F(1)
        basis.append(e)
    expected_types = [[n,k,*bits] for n in range(1,8-r) for k in range(r-1)
                      for bits in product((0,1),repeat=r+1)]
    assert len(expected_types) == len(table["rows"]) == {5:512,6:640}[r]
    G,h,slacks,sym_slacks = [],[],[],[]
    payment_checks,coefficient_checks,reduction_checks = 0,0,0
    csvrows = []
    for i,(typ,row) in enumerate(zip(expected_types,table["rows"])):
        assert row["index"] == i and row["type"] == typ
        constant = remainder(r,typ,zero)
        g = [remainder(r,typ,e)-constant for e in basis[1:]]
        rhs = -constant
        assert g == list(map(F,row["G"])) and rhs == F(row["h"])
        coefficient_checks += len(g)+1
        for e in basis:
            expected = remainder(r,typ,e)
            for u in (F(0),F(1)):
                assert paid_remainder(r,typ,e,u) == expected
                payment_checks += 1
        pE,sE,mE = [remainder(r,typ,weights) for weights in (p,sym,guard)]
        assert min(pE,sE,mE) >= 0
        assert pE == dot(g,p)-rhs == F(row["primal_E"])
        assert sE == dot(g,sym)-rhs == F(row["symmetric_E"])
        assert mE == F(row["main_guard_E"]) == main_atoms[(r,*typ)]
        n,k,x,*end = typ
        ys,t,q = end[:-2],end[-2],end[-1]
        j,D,a = sum(ys),n+r-1,sym[r]
        H = base(r,n,j,x,t,sym)
        if x == 0:
            add1 = a*j*(F(1,n+k)-F(1,n+m))
            add2 = F((1-q)*j,n*(n+j))
        else:
            add1 = a*(m-j)*(F(1,n)-F(1,n+k))
            add2 = F(q*(m-j),(n+1+j)*D)
        assert min(H,add1,add2) >= 0 and sE == H+add1+add2
        reduction_checks += 1
        G.append(g); h.append(rhs); slacks.append(pE); sym_slacks.append(sE)
        csvrows.append([i,*typ,*map(str,g),str(rhs),str(mE),str(pE),str(sE),str(H)])
    lam = [F(0)]*len(G)
    for support in cert["dual_nonzero"]:
        index = support["index"]
        assert expected_types[index] == support["type"] and lam[index] == 0
        lam[index] = F(support["lambda"])
    assert min(lam) >= 0
    gt = [sum((lam[i]*G[i][j] for i in range(len(G))),F(0)) for j in range(2*r)]
    reduced = [c-z for c,z in zip(cost,gt)]
    assert gt == cost
    assert reduced == [F(0)]*(2*r) == list(map(F,cert["dual_reduced_cost"]))
    assert dot(h,lam) == dot(cost,p) == F(cert["dual_objective"])
    assert all(v*z == 0 for v,z in zip(lam,slacks))
    assert all(v*z == 0 for v,z in zip(p,reduced))
    assert sum(v == 0 for v in slacks) == cert["primal_zero_count"]
    assert sum(v == 0 for v in sym_slacks) == cert["symmetric_zero_count"]
    assert min(v for v in sym_slacks if v > 0) == F(cert["symmetric_min_positive_E"])
    # The dual identity is checked coefficientwise, hence for every p, not just p*.
    identity_checks = 0
    for e in basis:
        left = dot(cost,e)-F(cert["C"])
        right = sum((lam[i]*remainder(r,typ,e) for i,typ in enumerate(expected_types)),F(0))
        assert left == right
        identity_checks += 1
    # All feasible weights force delta=1 using two rows independent of every other weight.
    for e in basis:
        lower_type = [1,0,0]+[0]*m+[0,1]
        upper_type = [1,0,1]+[1]*m+[1,0]
        assert remainder(r,lower_type,e) == e[-1]-1
        assert remainder(r,upper_type,e) == (1-e[-1])/r
    reduced_table = [{"r":r,"n":n,"j":j,
        "H00":str(base(r,n,j,0,0,sym)),"H01":str(base(r,n,j,0,1,sym)),
        "H10":str(base(r,n,j,1,0,sym)),"H11":str(base(r,n,j,1,1,sym))}
        for n in range(1,8-r) for j in range(m+1)]
    write(f"reduced_table_r{r}.json",reduced_table)
    with (HERE/f"all_types_r{r}.csv").open("w",newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["index",*table["row_type_order"],*["G_"+v for v in table["variable_order"]],
                         "h","main_guard_E","primal_E","symmetric_E","H"])
        writer.writerows(csvrows)
    summaries.append({"r":r,"actual_player":7-r,"status":"PASS_EXACT_FULL_CONE",
        "C":cert["C"],"variables":2*r,"types":len(G),"coefficient_checks":coefficient_checks,
        "payment_identity_checks":payment_checks,"reduction_checks":reduction_checks,
        "reduced_table_values":4*len(reduced_table),"dual_support":sum(v != 0 for v in lam),
        "dual_identity_basis_checks":identity_checks,"dual_objective":str(dot(h,lam)),
        "GT_lambda":list(map(str,gt)),"reduced_cost":list(map(str,reduced)),
        "zero_count":sum(v == 0 for v in slacks),"min_positive_E":str(min(v for v in slacks if v > 0)),
        "delta_forced_to_one":True,"main_rows_matched":len(G)})

result = {"status":"PASS_R5_R6_EXACT_CONE_OPTIMA","summaries":summaries,
          "source_sha256_checks":source_checks,"optimizer_calls":0,"game_point_reads":0,
          "discovery_module_imports":0,"arithmetic":"standard-library fractions.Fraction",
          "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
write("independent_verification.json",result)
print(json.dumps(result,ensure_ascii=False,indent=2))
