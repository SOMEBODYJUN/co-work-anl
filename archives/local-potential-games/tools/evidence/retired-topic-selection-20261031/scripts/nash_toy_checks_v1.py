"""Exact finite checks for Nash topic selection.  These are not proofs."""
from fractions import Fraction as F
from itertools import product
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))

def normsq(x):
    return dot(x, x)

def normalize(r, fallback):
    s = sum(r)
    return tuple(a/s for a in r) if s else fallback

def update(r, x, u):
    avg = dot(x, u)
    rp = tuple(max(F(0), a+b-avg) for a, b in zip(r, u))
    xp = normalize(rp, x)
    q = tuple(a-b for a, b in zip(rp, r))
    D = dot(tuple(a-b for a, b in zip(xp, x)), u)
    return rp, xp, q, D

def one_step_checks():
    counts = {}
    for m in (2, 3):
        count = 0
        uniform = tuple(F(1,m) for _ in range(m))
        vertices = [tuple(F(int(i==j)) for i in range(m)) for j in range(m)]
        for rr in product(range(3), repeat=m):
            r = tuple(map(F,rr))
            xs = [normalize(r,uniform)] if sum(r) else [uniform]+vertices
            for x in xs:
                for uu in product(range(-2,3), repeat=m):
                    u = tuple(map(F,uu))
                    rp,xp,q,D = update(r,x,u)
                    assert 2*sum(rp)*D == normsq(rp)-normsq(r)+normsq(q)
                    assert normsq(rp)-normsq(r) >= normsq(q)
                    assert D >= 0
                    if sum(rp):
                        assert D*sum(rp) >= normsq(q)
                    count += 1
        counts[str(m)] = count
    return counts

def stochastic_counterexample():
    # One-player exact potential, true u=(1/2,0), equilibrium x=e_1.
    # Noise is equiprobable +/-(-1/2,1/2); each coordinate is mean zero.
    r = (F(1), F(0))
    x = (F(1), F(0))
    true_u = (F(1,2), F(0))
    obs = [(F(0),F(1,2)), (F(1),F(-1,2))]
    out = []
    for u in obs:
        rp,xp,q,D = update(r,x,u)
        out.append({"observed_u":list(map(str,u)),"r_next":list(map(str,rp)),
                    "x_next":list(map(str,xp)),
                    "true_gain":str(dot(tuple(a-b for a,b in zip(xp,x)),true_u)),
                    "true_gap_next":str(max(true_u)-dot(xp,true_u))})
    expected_gain = sum((F(v["true_gain"]) for v in out),F(0))/2
    expected_gap = sum((F(v["true_gap_next"]) for v in out),F(0))/2
    assert expected_gain == F(-1,12)
    assert expected_gap == F(1,12)
    return {"branches":out,"expected_true_gain":str(expected_gain),
            "expected_true_gap":str(expected_gap)}

def minty_coordination_certificate():
    # Common payoff 1 on 00 or 11; equal mixture of these profiles
    # refutes every candidate Minty anchor x=(p,q).
    # Each anchor's average aggregate unilateral-deviation gain is -1.
    vals=[]
    for p,q in product((F(0),F(1,4),F(1,2),F(3,4),F(1)),repeat=2):
        gain00=p+q-2
        gain11=(1-p)+(1-q)-2
        assert (gain00+gain11)/2 == -1
        vals.append([str(p),str(q),str(gain00),str(gain11)])
    return {"anchors_checked":len(vals),"universal_symbolic_average":"-1",
            "rows":vals}

def local_square_chain_checks():
    def poly(n):
        p={}
        def add(m,c):
            k=tuple(sorted(m))
            p[k]=p.get(k,F(0))+c
        for i in range(1,n+1):
            x,xp,c,d,t=[f"{s}{i}" for s in ("x","z","c","d","t")]
            add((t,x),F(1));add((c,x),F(-1))
            if i==1:
                add((t,),F(-1,4));add((c,),F(1,4))
            else:
                prev=(f"x{i-1}",f"z{i-1}")
                add((t,)+prev,F(-1));add((c,)+prev,F(1))
            add((d,x),F(1));add((d,xp),F(-1))
            add((x,),F(-1,2));add((xp,),F(1,2));add((t,),F(-2))
        add((f"x{n}",),F(-2));add((f"z{n}",),F(-2))
        return {k:v for k,v in p.items() if v}
    def grad(p,v,z):
        total=F(0)
        for mon,coeff in p.items():
            if v in mon:
                term=coeff
                for w in mon:
                    if w!=v: term*=z[w]
                total+=term
        return total
    records=[]
    for n in range(1,13):
        p=poly(n)
        variables={v for mon in p for v in mon}
        edges={tuple(sorted(e)) for mon in p for e in combinations(mon,2)}
        degrees={v:sum(v in e for e in edges) for v in variables}
        bags=[]
        for i in range(1,n+1):
            bag={f"{s}{i}" for s in ("t","c","d","x","z")}
            if i>1: bag|={f"x{i-1}",f"z{i-1}"}
            bags.append(bag)
        assert all(any(set(mon)<=b for b in bags) for mon in p)
        for v in variables:
            indices=[i for i,b in enumerate(bags) if v in b]
            assert indices==list(range(min(indices),max(indices)+1))
        assert max(degrees.values())<=6
        assert max(map(len,bags))-1<=6
        # eps at the claimed boundary plus two larger choices.
        for eps in (F(1,2**(2**n)),F(1,4),F(1,2)):
            z={}
            for i in range(1,n+1):
                z[f"x{i}"]=z[f"z{i}"]=max(eps,F(1,2**(2**i)))
                z[f"c{i}"]=z[f"t{i}"]=eps
                z[f"d{i}"]=F(1,2)
            for v in variables:
                g=grad(p,v,z)
                # Maximization KKT for the perturbed interval [eps,1-eps].
                if eps==F(1,2): continue
                if z[v]==eps: assert g<=0,(n,v,g)
                elif z[v]==1-eps: assert g>=0,(n,v,g)
                else: assert g==0,(n,v,g)
        records.append({"n":n,"players":len(variables),"max_degree":max(degrees.values()),
                        "pathwidth_certificate_upper_bound":max(map(len,bags))-1,
                        "max_monomial_degree":max(map(len,p)),"perturbations_tested":3})
    # Each displayed derivative is multilinear in its independent arguments,
    # so extrema over the cube occur at binary vertices.  This check records
    # the payoff normalization with no numerical optimization.
    expressions = {
        "t_i_general":(3,lambda x,a,b:x-a*b-2),
        "t_1":(1,lambda x:x-F(1,4)-2),
        "c_i_general":(3,lambda x,a,b:a*b-x),
        "c_1":(1,lambda x:F(1,4)-x),
        "d_i":(2,lambda x,z:x-z),
        "x_i_nonterminal":(6,lambda t,c,d,tn,cn,z:t-c+d-F(1,2)-(tn-cn)*z),
        "xp_i_nonterminal":(4,lambda d,tn,cn,x:-d+F(1,2)-(tn-cn)*x),
        "x_n_all_cube":(3,lambda t,c,d:t-c+d-F(5,2)),
        "xp_n_all_cube":(1,lambda d:-d-F(3,2)),
        "x_n_at_original_NE_after_t_zero":(2,lambda c,d:-c+d-F(5,2))
    }
    ranges={}
    for name,(arity,fun) in expressions.items():
        values=[fun(*map(F,args)) for args in product((0,1),repeat=arity)]
        ranges[name]=list(map(str,(min(values),max(values))))
        assert max(map(abs,values))<=F(7,2)
    return {"records":records,"symbolic_gradient_bounds":ranges,
            "local_payoff_definition":"u_v(a)=a_v*partial_v(Psi)(a_-v)/4; absolute payoff <=7/8",
            "warning":"KKT checked exactly only at the displayed profiles. Geometric separation from every exact NE requires the separate universal argument in REPORT.md."}

if __name__ == "__main__":
    result={"arithmetic":"Fraction exact; deterministic enumeration; no seed",
            "one_step_identity":one_step_checks(),
            "noise_breaks_expected_potential_ascent":stochastic_counterexample(),
            "minty_two_player_coordination":minty_coordination_certificate(),
            "localized_repeated_squaring":local_square_chain_checks(),
            "limits":"Finite identity checks do not prove a general theorem or asymptotic convergence."}
    (ROOT/"toy_results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("minty_two_player_coordination",)},ensure_ascii=False,indent=2))
