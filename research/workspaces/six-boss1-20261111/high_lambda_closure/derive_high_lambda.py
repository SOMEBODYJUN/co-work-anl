#!/usr/bin/env python3
"""Exact high-lambda domain and closure certificates; Python standard library only.

This script never opens a global LP, candidate, optimum, or external package.
All writes stay beside this script.  Frozen packages must be replayed in a copy.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = WS.parents[2]
TARGETS = ["A1", "A2", "A3", "A4", "A5", "A6", "X", "C"]
BITS = list(product((0, 1), repeat=9))
SOURCES = [
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "archives/customer-attraction/state/引理/联合内部偏离的完整参数域与同菜单条件投影--引理.md",
    "archives/customer-attraction/state/引理/真实前缀全目录单步偏离行--引理.md",
    "research/workspaces/six-boss1-20261111/source1_lambda_complete/proof.md",
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/proof.md",
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/proof.md",
    "research/workspaces/six-boss1-20261111/all_source_minimal_cap_safe/proof.md",
    "research/workspaces/six-boss1-20261111/all_source_minimal_cap_safe/exact_family.json",
    "research/workspaces/six-boss1-20261111/all_source_minimal_cap_safe/coordinate_contract.json",
    "research/workspaces/six-boss1-20261111/ordered_minimal_cap/proof.md",
    "research/workspaces/six-boss1-20261111/ordered_minimal_cap/exact_family.json",
    "research/workspaces/six-boss1-20261111/ordered_minimal_cap/coordinate_contract.json",
]


def enc(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    return x


def save(name, obj):
    (HERE / name).write_text(json.dumps(enc(obj), ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin_sources():
    got = [{"path": p, "sha256": sha(ROOT / p)} for p in SOURCES]
    prior = HERE / "source_pins.json"
    if prior.exists():
        assert json.loads(prior.read_text())["sources"] == got, "Source bytes changed"
    else:
        save("source_pins.json", {"schema": "high_lambda_sources_v1", "sources": got})
    return got


# Sparse multivariate polynomials, with tuple exponent keys.  Only degree <= 2
# is used, but multiplication is literal and does not assume the identities.
class Poly:
    def __init__(self, dim, terms=None):
        self.dim = dim
        self.t = {k: F(v) for k, v in (terms or {}).items() if v}

    @classmethod
    def const(cls, dim, value):
        return cls(dim, {(0,) * dim: F(value)})

    @classmethod
    def var(cls, dim, j):
        k = [0] * dim
        k[j] = 1
        return cls(dim, {tuple(k): F(1)})

    def coerce(self, other):
        return other if isinstance(other, Poly) else Poly.const(self.dim, other)

    def __add__(self, other):
        other = self.coerce(other)
        terms = self.t.copy()
        for k, v in other.t.items():
            terms[k] = terms.get(k, F(0)) + v
        return Poly(self.dim, terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.dim, {k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        terms = {}
        for a, x in self.t.items():
            for b, y in other.t.items():
                k = tuple(v + w for v, w in zip(a, b))
                terms[k] = terms.get(k, F(0)) + x * y
        return Poly(self.dim, terms)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (F(1) / scalar)

    def equal(self, other):
        return not (self - other).t

    def affine(self):
        assert all(sum(k) <= 1 for k in self.t)
        out = [self.t.get((0,) * self.dim, F(0))]
        for j in range(self.dim):
            k = [0] * self.dim
            k[j] = 1
            out.append(self.t.get(tuple(k), F(0)))
        return out

    def at(self, point):
        ans = F(0)
        for mon, coeff in self.t.items():
            for x, power in zip(point, mon):
                coeff *= x ** power
            ans += coeff
        return ans


def beta_weights(i, q0, tau, terminal=F(1)):
    return {
        j: terminal * q0 / 2 + tau[j]
        + sum((q0 * tau[l] / ((7-l)*(8-l)) for l in tau if l > j), F(0))
        for j in tau
    }


def cost(i, q0, lam, tau, p, t, q, r, z, terminal=F(1)):
    beta = beta_weights(i, q0, tau, terminal)
    a = lam + sum(tau.values(), F(0))
    load = p + t + sum(r.values()) + z
    numerator = a*t - terminal*z - sum((tau[j]*r[j] for j in tau), F(0))
    first = numerator/load if load else 0*numerator
    value = first + sum((beta[j]*r[j] for j in tau), F(0)) + terminal*z
    value += terminal*q/(p+t+sum(r.values())+1)
    for j in tau:
        value += tau[j]*q/(p+t+sum(r[l] for l in tau if l < j)+7-j)
    return value


def corners(i, q0, h):
    js = list(range(i+1, 6))
    result = []
    for eps in product((0, 1), repeat=len(js)):
        tau = {}
        for j, e in reversed(list(zip(js, eps))):
            upper = F(5, 4) * (h - sum((q0*tau[l]/((7-l)*(8-l)) for l in tau if l > j), F(0)))
            assert upper > 0
            tau[j] = e * upper
        result.append((eps, tuple(tau[j] for j in js)))
    return result


def domain(i, q0):
    js = list(range(i+1, 6))
    m = len(js)
    dim = m + 1
    delta = Poly.var(dim, 0)
    tau = {j: Poly.var(dim, k+1) for k, j in enumerate(js)}
    beta = beta_weights(i, q0, tau)
    g = {j: (24+delta)/30 + tau[j]/5-beta[j] for j in js}
    facets = [{"id": "lambda_ge_25", "affine_in_delta_tau": delta.affine(), "origin": "specified_high_lambda_halfspace"}]
    facets.extend({"id": f"tau{j}_ge_0", "affine_in_delta_tau": tau[j].affine(), "origin": "internal_SAFE_weight"} for j in js)
    facets.extend({"id": f"g{j}_ge_0", "affine_in_delta_tau": g[j].affine(), "origin": {"p": i-1, "D": 6, "missing": [j], "z": 1}} for j in js)
    L = 24-15*q0
    base = corners(i, q0, L/30)
    rays = corners(i, q0, F(1, 30))
    vertices = []
    ray_out = []
    for number, ((eps, x), (epsr, v)) in enumerate(zip(base, rays)):
        assert eps == epsr and all(a == L*b for a, b in zip(x, v))
        tag = f"q{q0.denominator}_i{i}_e{''.join(map(str, eps)) or 'empty'}"
        vertices.append({"id": tag+"_v", "epsilon": eps, "lambda": 25, "tau": x})
        ray_out.append({"id": tag+"_r", "epsilon": eps, "delta_lambda": 1, "delta_tau": v})
    return {"source": i, "q0": q0, "middle_sources": js, "coordinates": ["delta=lambda-25"]+[f"tau{j}" for j in js], "dimension": dim, "facets": facets, "vertices": vertices, "extreme_rays": ray_out, "L": L}


def state_certificates(i, q0):
    js = list(range(i+1, 6))
    dim = len(js)+1
    delta = Poly.var(dim, 0)
    lam = 25+delta
    tau = {j: Poly.var(dim, k+1) for k, j in enumerate(js)}
    beta = beta_weights(i, q0, tau)
    g = {j: (lam-1)/30+tau[j]/5-beta[j] for j in js}
    one = Poly.const(dim, 1)
    out = []
    zeros = []
    slopes = []
    for p in range(i):
        D = p+7-i
        for bits in product((0, 1), repeat=len(js)):
            r = dict(zip(js, bits))
            missing = [j for j in js if not r[j]]
            k = len(missing)
            U = sum((tau[j] for j in missing), 0*one)
            for z in (0, 1):
                rho = cost(i,q0,lam,tau,p,1,F(0),r,z) - sum(beta.values(),0*one)-1-(lam-1)/D
                # rho(D,M,1)=sum g_j + nonnegative affine remainder;
                # rho(D,M,0) adds the exact same-tail last-bit difference.
                extra = (lam-1)*k*(F(1,D*(D-k))-F(1,6*(6-k)))
                extra += U*(F(1,D-k)-F(1,6-k))
                if k >= 1:
                    extra += F(k-1,6-k)*(k*(lam-1)/30+U/5)
                if z == 0:
                    extra += (delta+U+25-(D-k-1)**2)/((D-k)*(D-k-1))
                certified = sum((g[j] for j in missing), 0*one)+extra
                assert rho.equal(certified)
                ex = extra.affine()
                assert all(v >= 0 for v in ex)
                out.append({"source":i,"q0":q0,"p":p,"D":D,"middle_bits":bits,"z":z,"missing":missing,"rho":rho.affine(),"g_weights":{j:1 for j in missing},"remaining_nonnegative_affine":ex})
                query_slope = cost(i,q0,lam,tau,p,1,F(1),r,z)-cost(i,q0,lam,tau,p,1,F(0),r,z)-(1+sum(tau.values(),0*one))/D
                assert all(v >= 0 for v in query_slope.affine())
                slopes.append({"source":i,"q0":q0,"p":p,"middle_bits":bits,"z":z,"nonnegative_slope_difference":query_slope.affine()})
                for q in (F(0), q0):
                    anchor = q*(F(1,p+1)+sum((tau[j]/(p+7-j) for j in js),0*one))
                    residual = cost(i,q0,lam,tau,p,0,q,r,z)-anchor
                    assert all(v >= 0 for v in residual.affine())
                    zeros.append({"source":i,"q0":q0,"p":p,"middle_bits":bits,"z":z,"q":q,"nonnegative_affine":residual.affine()})
    return out, zeros, slopes


def atom_values(i, target, atom):
    if atom is None:
        return 0,0,0,0,0
    p = sum(atom[:i-1])
    t = atom[int(target[1:])-1] if target.startswith("A") else atom[6 if target=="X" else 8]
    actual_load = sum(atom[:6])
    ui = F(atom[i-1],actual_load) if actual_load else F(0)
    return p,t,atom[7],atom[8],ui


def pure_column(i,q0,lam,tau,target,atom,terminal=F(1)):
    beta = beta_weights(i,q0,tau,terminal)
    S = terminal+sum(beta.values(),F(0))
    if atom is None:
        return S
    p,t,o,_,ui = atom_values(i,target,atom)
    D = p+7-i
    W = S+(lam-terminal)/D
    m = t*W+terminal*F(o,6*(p+1+(6-i)*t))
    m += sum((tau[j]*F(o,6*(p+(j-i)*t+7-j)) for j in tau),F(0))
    return (lam+sum(tau.values(),F(0)))*ui-m


def ordered_column(i,q0,lam,tau,atom,terminal=F(1)):
    beta = beta_weights(i,q0,tau,terminal)
    S = terminal+sum(beta.values(),F(0))
    if atom is None:
        return S
    p,_,o,_,ui = atom_values(i,"C",atom)
    D = p+7-i
    G = (S+(lam-terminal)/D+terminal*F(1,p+1)+sum((tau[j]/(p+7-j) for j in tau),F(0)))/6
    return (lam+sum(tau.values(),F(0)))*ui-o*G


def symbolic_closure(i,q0,family,target):
    js = list(range(i+1,6))
    m = len(js)
    v = {j:Poly.var(m,k) for k,j in enumerate(js)}
    z = Poly.const(m,0)
    Theta = sum(v.values(),z)
    sj = {j:1+F(j-i-1)*q0/((7-j)*(8-j)) for j in js}
    V = sum((sj[j]*v[j] for j in js),z)
    S0 = 1+F(m)*q0/2
    L = 24-15*q0
    H = S0+L*V
    aT = S0-15*q0*V
    aO = S0*Theta-V
    assert all(S0-sj[j]>=0 for j in js)
    endpoint_tau = {j:L*v[j] for j in js}
    fingerprint = hashlib.sha256()
    checks = 0
    slack_checks = []
    for p in range(i):
        D=p+7-i
        for j in js:
            Qj = sj[j]/(p+1)+(S0-sj[j])/D-S0/F(p+7-j)
            assert Qj >= 0
            assert 2*(j-i)*(p+1) <= (6-i)*(p+7-j)
            slack_checks.append({"p":p,"j":j,"coefficient":Qj})
    for col,atom in enumerate(BITS+[None]):
        if atom is None:
            safeT=safeO=F(0)
            equality=F(-1)
            slack=z
        else:
            p,t,o,c,ui=atom_values(i,target,atom)
            D=p+7-i
            safeT=ui-F(t,D)
            safeO=ui-F(o,6*D)
            equality=F(c)
            slack=sum((v[j]*(sj[j]/(p+1)+(S0-sj[j])/D-S0/F(p+7-j)) for j in js),z)*F(o,6)
            if family in ("pure","C-only"):
                slack *= 1-t
        if family=="ordered":
            ray=ordered_column(i,q0,F(1),v,atom,F(0))
            endpoint=ordered_column(i,q0,F(25),endpoint_tau,atom)
            rhs=V*endpoint+(aT+aO)*safeO+slack
        else:
            ray=pure_column(i,q0,F(1),v,target,atom,F(0))
            endpoint=pure_column(i,q0,F(25),endpoint_tau,target,atom)
            if family=="C-only":
                ray += V*equality
                endpoint += (H-1)*equality
            rhs=V*endpoint+aT*safeT+aO*safeO+slack
            if family=="C-only":
                rhs += V*equality
        difference=H*ray-rhs
        assert not difference.t, (i,q0,family,target,col,difference.t)
        # Hash the actual polynomial LHS and RHS, not only an all-zero summary.
        packet=[col,sorted((str(k),str(x)) for k,x in (H*ray).t.items()),sorted((str(k),str(x)) for k,x in rhs.t.items())]
        fingerprint.update(json.dumps(packet).encode()+b"\n")
        checks += (m+1)*(m+2)//2
    return {"source":i,"q0":q0,"family":family,"target":target,"columns":513,"all_degree_at_most_two_coefficients":checks,"identity_sha256":fingerprint.hexdigest(),"zero_polynomial_columns":513,"slack_coefficients":slack_checks}


def endpoint_links(domains):
    pure_path=WS/"all_source_minimal_cap_safe/exact_family.json"
    ord_path=WS/"ordered_minimal_cap/exact_family.json"
    pure=json.loads(pure_path.read_text())["rows"]
    ordered=json.loads(ord_path.read_text())["rows"]
    result=[]
    for dom in domains:
        i=dom["source"];q0=dom["q0"];js=dom["middle_sources"]
        pool=pure if q0==F(1,6) else ordered
        taukey="tau_by_true_source" if q0==F(1,6) else "tau_by_source"
        for vertex in dom["vertices"]:
            tau=dict(zip(js,vertex["tau"]))
            for target in TARGETS if q0==F(1,6) else ["ordered"]:
                matching=[row for row in pool if row["source"]==i and F(row["s"])==0 and {int(k):F(v) for k,v in row[taukey].items()}==tau and (target=="ordered" or row["forced_target"]==target)]
                assert len(matching)==1,(vertex,target,len(matching))
                old=matching[0]
                h=hashlib.sha256()
                for col,atom in enumerate(BITS+[None]):
                    value=ordered_column(i,q0,F(25),tau,atom) if target=="ordered" else pure_column(i,q0,F(25),tau,target,atom)
                    assert value==F(old["a"][str(col)]),(old["name"],col,value,old["a"][str(col)])
                    h.update((str(value)+"\n").encode())
                result.append({"new_base_vertex":vertex["id"],"source":i,"q0":q0,"target":target,"old_package":str((ord_path if target=="ordered" else pure_path).relative_to(ROOT)),"old_row_name":old["name"],"columns_checked":513,"raw_coefficients_sha256":h.hexdigest()})
    return result


def menu_checks():
    out=[]
    for i in range(1,6):
        for p in range(i):
            D=p+7-i
            count=0
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(d>0)
                assert sum(F(t,6*D) for t in menu)-F(o,6*D)==F(d-o,6*D)>=0
                for k,t in enumerate(menu):
                    assert sum(F(menu[l],5) for l in range(6) if l!=k)==F(d-t,5)
                count+=1
            out.append({"source":i,"p":p,"all_menus":count,"actual_SAFE_average_union_identity":"PASS","outer6_inner5_index_identity":"PASS"})
    return out


def main():
    pins=pin_sources()
    domains=[domain(i,q) for q in (F(1,6),F(1,5)) for i in range(1,6)]
    all_t1=[];all_t0=[];slopes=[]
    for q in (F(1,6),F(1,5)):
        for i in range(1,6):
            a,b,c=state_certificates(i,q)
            all_t1+=a;all_t0+=b;slopes+=c
    symbolic=[]
    for i in range(1,6):
        for target in TARGETS:
            symbolic.append(symbolic_closure(i,F(1,6),"pure",target))
        symbolic.append(symbolic_closure(i,F(1,6),"C-only","C"))
        symbolic.append(symbolic_closure(i,F(1,5),"ordered","C"))
    links=endpoint_links(domains)
    menus=menu_checks()
    save("inputs.json",{"schema":"high_lambda_closure_inputs_v1","model":"finite unit customers, finite nonempty labelled common catalogue, six players, every complete-history pure SPE","sources":[1,2,3,4,5],"q0":["1/6","1/5"],"lambda_range":"[25,infinity)","tau":"all nonnegative","all_ordered_histories_and_weak_ties":True,"empty_duplicate_and_zero_customer_cases":True,"columns":["a1","a2","a3","a4","a5","a6","x","o","c"],"atom_columns":512,"independent_K_column":512,"pure_targets":TARGETS,"new_raw_matrix_materialized":False,"optimizer_calls":0,"candidate_or_optimal_face_files_read":0})
    save("parameter_domains.json",{"schema":"all_high_lambda_facets_vertices_rays_v1","domains":domains,"total_facets":sum(len(x["facets"]) for x in domains),"total_vertices":sum(len(x["vertices"]) for x in domains),"total_extreme_rays":sum(len(x["extreme_rays"]) for x in domains)})
    save("all_state_certificates.json",{"affine_order":"constant, delta=lambda-25, tau in increasing true-source order","t1_zero_query":all_t1,"t0_zero_tail":all_t0,"t1_query_slope":slopes})
    save("symbolic_column_checks.json",{"scope":"Polynomial identities in every v, before imposing the recession cone; all 513 columns, no sample-point inference","checks":symbolic})
    save("endpoint_correspondence.json",{"existing_rows_only":True,"links":links})
    save("menu_index_checks.json",{"checks":menus})
    summary={"status":"PASS","domains":len(domains),"facets":sum(len(x["facets"]) for x in domains),"vertices":sum(len(x["vertices"]) for x in domains),"rays":sum(len(x["extreme_rays"]) for x in domains),"all_t1_state_certificates":len(all_t1),"all_t0_affine_certificates":len(all_t0),"query_slope_certificates":len(slopes),"symbolic_513_column_identities":len(symbolic)*513,"symbolic_scalar_coefficients":sum(x["all_degree_at_most_two_coefficients"] for x in symbolic),"old_endpoint_rows":len(links),"old_endpoint_columns":len(links)*513,"actual_menu_patterns":sum(x["all_menus"] for x in menus),"inner5_index_checks":6*sum(x["all_menus"] for x in menus),"new_inequality_information":"NONE relative to existing lambda=25 endpoint rows, actual SAFE_i(legal T), customer nonnegativity, and the genuine C equality where used","optimizer_calls":0,"source_pins_unchanged":pins==pin_sources()}
    save("generator_output.json",summary)
    lines=["# λ≥25：全部基顶点和极端退化射线","", "每行基顶点为 `(λ,τ)=(25,Lv)`，射线为 `(δλ,δτ)=(1,v)`；L=24−15q₀。零 ε 与全部重复来源均保留。", "", "| q₀ | 源 i | ε | 基顶点 τ | 归一射线 v |", "|---|---:|---|---|---|"]
    for d in domains:
        for a,b in zip(d["vertices"],d["extreme_rays"]):
            lines.append(f"| {d['q0']} | {d['source']} | {''.join(map(str,a['epsilon'])) or '∅'} | ({', '.join(map(str,a['tau']))}) | ({', '.join(map(str,b['delta_tau']))}) |")
    (HERE/"endpoint_table.md").write_text("\n".join(lines)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
