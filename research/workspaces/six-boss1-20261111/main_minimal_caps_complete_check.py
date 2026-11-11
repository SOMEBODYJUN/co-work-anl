"""Main independent q=1/6 and q=1/5 minimal-cap geometry and true-cost check.

No project imports, no optimizer and no candidate-point reads. Rebuilds all
halfspaces, complete vertices, real tail costs, and every exported coefficient.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from hashlib import sha256
import json
import math

W = Path(__file__).resolve().parent
ATOMS = list(product((0, 1), repeat=9))

def read(p):
    return json.loads(p.read_text())

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def solve(rows):
    n = len(rows)
    a = [[F(v) for v in cs] + [-F(c)] for c, cs in rows]
    for k in range(n):
        h = next((h for h in range(k, n) if a[h][k]), None)
        if h is None:
            return None
        a[k], a[h] = a[h], a[k]
        d = a[k][k]
        a[k] = [v / d for v in a[k]]
        for h in range(n):
            if h != k:
                d = a[h][k]
                a[h] = [x - d * y for x, y in zip(a[h], a[k])]
    return tuple(row[-1] for row in a)

def rank(rows):
    if not rows:
        return 0
    a = [list(map(F, row)) for row in rows]
    n, m, k = len(a), len(a[0]), 0
    for j in range(m):
        h = next((h for h in range(k, n) if a[h][j]), None)
        if h is None:
            continue
        a[k], a[h] = a[h], a[k]
        d = a[k][j]
        a[k] = [v / d for v in a[k]]
        for h in range(n):
            if h != k:
                d = a[h][j]
                a[h] = [x - d * y for x, y in zip(a[h], a[k])]
        k += 1
        if k == n:
            break
    return k

def planes(i, q0):
    js = list(range(i + 1, 6)); dim = len(js) + 1
    out = []
    for k in range(dim):
        v = [F(0)] * dim; v[k] = F(1)
        out.append((F(0), tuple(v)))
    if i != 1:
        out.append((F(9), (F(0),) * (dim - 1) + (F(-1),)))
    for k, j in enumerate(js):
        for own, c, sc in [(F(4, 5), F(4, 5) - q0 / 2, F(0)),
                            (F(3, 4), (F(5, 4) if i == 1 else F(6, 5)) - q0 / 2, F(-1, 20))]:
            v = [F(0)] * dim; v[k] = -own; v[-1] = sc
            for l in js:
                if l > j:
                    v[l - i - 1] = -q0 / ((7 - l) * (8 - l))
            out.append((c, tuple(v)))
    if i == 1:
        for pair in combinations(js, 2):
            v = [F(0)] * dim; v[-1] = F(-1, 20)
            for j in pair:
                v[j - i - 1] -= F(3, 4)
                for l in js:
                    if l > j:
                        v[l - i - 1] -= q0 / ((7 - l) * (8 - l))
            out.append((2 - q0, tuple(v)))
    return out

def ev(plane, x):
    c, v = plane
    return c + sum(a * b for a, b in zip(v, x))

def weights(i, q0, x):
    tau = {j: x[j - i - 1] for j in range(i + 1, 6)}
    beta = {j: q0 / 2 + tau[j] + sum((q0 * tau[l] / ((7 - l) * (8 - l))
            for l in tau if l > j), F(0)) for j in tau}
    return tau, beta, 25 + sum(tau.values()) - x[-1], 1 + sum(beta.values())

def cost(i, p, t, q, tail, tau, beta, a):
    js = list(tau); z = tail[-1]; r = dict(zip(js, tail[:-1]))
    load = p + t + sum(tail)
    num = a * t - z - sum(tau[j] * r[j] for j in js)
    assert load or num == 0
    v = num / load if load else F(0)
    v += sum(beta[j] * r[j] for j in js) + z
    v += q / (p + t + sum(r.values()) + 1)
    v += sum((tau[j] * q / (p + t + sum(r[h] for h in js if h < j) + 7 - j)
              for j in js), F(0))
    return v

def check_family(package, q0, ordered):
    pth = W / package
    data = read(pth / ('parameter_domains.json' if ordered else 'parameter_families.json'))
    sources = data['domains' if ordered else 'sources']
    family = read(pth / 'exact_family.json')
    all_params = {}; minima = {}; gs = {}
    geometry = []; state_count = 0; cond_count = 0; tied = 0; cols = 0; menus = 0
    for src in sources:
        i = src['source']; dim = 6 - i; pl = planes(i, q0)
        vertices = set()
        for basis in combinations(pl, dim):
            x = solve(basis)
            if x is not None and all(ev(h, x) >= 0 for h in pl):
                vertices.add(x)
        supplied = {v['id']: tuple(map(F, v['parameters'])) for v in src['vertices']}
        assert vertices == set(supplied.values()), (package, i, len(vertices))
        assert len(vertices) == {1: 90, 2: 28, 3: 12, 4: 5, 5: 2}[i]
        for h in pl:
            on = [x for x in vertices if ev(h, x) == 0]
            assert on and rank([[a-b for a,b in zip(x,on[0])] for x in on[1:]]) == dim-1
        assert all(ev(h, (F(1,100),)*(dim-1)+(F(1),)) > 0 for h in pl)
        geometry.append({'source':i, 'facets':len(pl), 'boundary_combinations':math.comb(len(pl),dim),
                         'complete_vertices':len(vertices), 'all_facet_ranks':dim-1})
        for vid, x in supplied.items():
            all_params[vid] = (i, x)
            tau, beta, a, S = weights(i, q0, x)
            assert a >= (F(2) if ordered else F(5,3)) if i == 1 else a >= 16
            for p in range(i):
                D = p + 7 - i
                Wv = S + F(24,D) - x[-1]/min(D,5)
                Zv = q0*(F(1,p+1)+sum((tau[j]/(p+7-j) for j in tau),F(0)))
                conditions = ([(0,F(d,5)) for d in range(6)] + [(1,F(d-1,5)) for d in range(1,7)]
                              if ordered else [(t,q0*o) for t,o in product((0,1),repeat=2)])
                for t, q in conditions:
                    vals = [cost(i,p,t,q,tail,tau,beta,a) for tail in product((0,1),repeat=6-i)]
                    mv = min(vals); state_count += len(vals); cond_count += 1
                    tied += vals.count(mv); minima[vid,p,t,q] = mv
                    if t:
                        assert mv == Wv + (1+sum(tau.values()))*q/D
                    elif q in (F(0),q0):
                        assert mv == (Zv if q else F(0))
                    if not ordered:
                        anchor = t*Wv+q/(p+1+(6-i)*t)
                        anchor += sum((tau[j]*q/(p+(j-i)*t+7-j) for j in tau),F(0))
                        assert mv == anchor
                if ordered:
                    assert Wv > Zv
                    fs = {}
                    for d in range(7):
                        fs[d] = ((6-d)*minima[vid,p,0,F(d,5)] if d<6 else F(0))
                        fs[d] += (d*minima[vid,p,1,F(d-1,5)] if d>0 else F(0))
                        fs[d] /= 6
                    G = (5*Zv+Wv)/6
                    assert fs[0] == 0 and fs[1] == G and all(fs[d]>G for d in range(2,7))
                    assert min(fs[d] for d in range(1,7)) == G
                    gs[vid,p] = G
                    for menu in product((0,1),repeat=6):
                        d = sum(menu); v = F(0)
                        for k,t in enumerate(menu):
                            q = sum((F(menu[l],5) for l in range(6) if l!=k),F(0))
                            assert q == F(d-t,5)
                            v += minima[vid,p,t,q]/6
                        assert v == fs[d] and v >= bool(d)*G
                        menus += 1
    for row in family['rows']:
        vid = row['vertex_id']; i,x = all_params[vid]
        tau,beta,a,S=weights(i,q0,x)
        assert F(row['source_IC_weight'])==a and F(row['numerical_divisor'])==25
        assert F(row['terminal_BR_average_weight'])==1 and F(row['terminal_CAP_weight'])==1
        assert {int(k):F(v) for k,v in row['middle_CAP_weights'].items()} == beta
        assert F(row['rhs'])==0
        if not ordered:
            target=row['forced_target']; ti=int(target[1:])-1 if target.startswith('A') else {'X':6,'C':8}[target]
        for h,bits in enumerate(ATOMS):
            actual=bits[:6]; p=sum(actual[:i-1]); load=sum(actual)
            ui=F(actual[i-1],load) if load else F(0)
            if ordered:
                want=a*ui-bits[7]*gs[vid,p]
            else:
                want=a*ui-minima[vid,p,bits[ti],q0*bits[7]]
            assert F(row['a'].get(str(h),'0'))==want,(package,row['name'],h)
            cols+=1
        assert F(row['a']['512'])==S; cols+=1
    expect=137 if ordered else 1096
    assert len(family['rows'])==expect and cols==expect*513
    assert state_count==(49968 if ordered else 16656)
    assert cond_count==(2544 if ordered else 848)
    result={'status':'PASS_MAIN_COMPLETE_MINIMAL_CAP_DOMAIN_TRUE_COSTS_AND_ALL_COLUMNS',
            'package':package,'q0':str(q0),'optimizer_calls':0,'candidate_points_read':0,
            'geometry':geometry,'full_parameter_vertices':len(all_params),
            'complete_hidden_states':state_count,'physical_minima':cond_count,'all_weak_tie_occurrences':tied,
            'full_menu_contexts':menus,'raw_rows':expect,'all_coefficients':cols,
            'source_proof_personally_read_complete':True,
            'source_proof_sha256':digest(pth/'proof.md'),'source_family_sha256':digest(pth/'exact_family.json'),
            'source_manifest_sha256':digest(pth/'freeze_manifest.json'),
            'scope':'Complete specified parameter domain; true-history necessary rows only. No SPE construction or half theorem.'}
    output=W/('main_'+package+'_check.json'); assert not output.exists()
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':
    check_family('all_source_minimal_cap_safe',F(1,6),False)
    check_family('ordered_minimal_cap',F(1,5),True)
