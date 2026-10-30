"""Exact scratch audit of fixed-hub, unique-light-side response potentials."""
from fractions import Fraction as Q
from itertools import product
import hashlib
import json
from pathlib import Path
import random
import sys

def poly(coeff, x):
    return sum((a * x**k for k, a in enumerate(coeff)), Q(0))

def sign(x):
    return (x > 0) - (x < 0)

def audit(inst):
    hubw, hubbits, lightw, sources, main, sides = inst
    n = len(lightw)
    states = list(product((0, 1), repeat=n))
    # Full literal resource table: hub moves remain frozen throughout this audit.
    def costs(bits):
        res = {}
        users = {}
        for v, coeff in enumerate(main):
            for b in (0, 1):
                key = ('A', v, b)
                res[key] = (coeff, hubw[v] if hubbits[v] == b else Q(0))
                users[key] = []
        for j, (ell, hubs, coeff) in enumerate(sides):
            for b in (0, 1):
                key = ('B', j, b)
                res[key] = (coeff, sum((hubw[v] for v in hubs if hubbits[v] == b), Q(0)))
                users[key] = []
        for i, b in enumerate(bits):
            for key in [('A', sources[i], b)] + [('B', j, 1-b) for j, (ell, _, _) in enumerate(sides) if ell == i]:
                coeff, load = res[key]
                res[key] = coeff, load + lightw[i]
                users[key].append(i)
        ans = [Q(0)] * n
        for key, (coeff, load) in res.items():
            val = poly(coeff, load)
            for i in users[key]:
                ans[i] += val
        return ans

    cc = {s: costs(s) for s in states}
    group = {v: [i for i in range(n) if sources[i] == v] for v in range(len(hubw))}
    threshold = {}
    constant = {}
    diffs = {}
    for v, ii in group.items():
        W = sum((lightw[i] for i in ii), Q(0))
        basebit = hubbits[v]
        for i in ii:
            offsets = []
            for b in (basebit, 1-basebit):
                offsets.append(sum((poly(coeff, lightw[i] + sum((hubw[h] for h in hubs if hubbits[h] == 1-b), Q(0)))
                                    for ell, hubs, coeff in sides if ell == i), Q(0)))
            other = [j for j in ii if j != i]
            xs = sorted({sum((lightw[j] for j, b in zip(other, zz) if b), Q(0)) for zz in product((0,1), repeat=len(other))})
            dd = {x: poly(main[v], hubw[v]+x+lightw[i])+offsets[0]-poly(main[v], W-x)-offsets[1] for x in xs}
            diffs[i] = dd
            if not any(main[v][1:]):
                constant[i] = offsets[0]-offsets[1]
            else:
                zeros = [x for x in xs if dd[x] == 0]
                neg = [x for x in xs if dd[x] < 0]
                pos = [x for x in xs if dd[x] > 0]
                if zeros:
                    assert len(zeros) == 1
                    threshold[i] = zeros[0]
                elif not neg:
                    threshold[i] = min(xs)-1
                elif not pos:
                    threshold[i] = max(xs)+1
                else:
                    threshold[i] = (max(neg)+min(pos))/2
                assert all(sign(x-threshold[i]) == sign(dd[x]) for x in xs)

    def potential(bits):
        ans = Q(0)
        for v, ii in group.items():
            chosen = [i for i in ii if bits[i] == hubbits[v]]
            if not any(main[v][1:]):
                ans += sum((constant[i] for i in chosen), Q(0))
            else:
                L = sum((lightw[i] for i in chosen), Q(0))
                ans += L*L/2-sum((lightw[i]*(threshold[i]+lightw[i]/2) for i in chosen), Q(0))
        return ans
    pp = {s: potential(s) for s in states}
    edge_count = 0
    pne = []
    minima = []
    for s in states:
        stable = local = True
        for i in range(n):
            t = s[:i]+(1-s[i],)+s[i+1:]
            cost_change = cc[t][i]-cc[s][i]
            pot_change = pp[t]-pp[s]
            assert sign(cost_change) == sign(pot_change), (inst, s, i, cost_change, pot_change)
            if cost_change < 0:
                stable = False
                edge_count += 1
            if pot_change < 0:
                local = False
            v = sources[i]
            x = sum((lightw[j] for j in group[v] if j != i and s[j] == hubbits[v]), Q(0))
            expected = diffs[i][x] * (1 if s[i] != hubbits[v] else -1)
            assert cost_change == expected
        if stable: pne.append(s)
        if local: minima.append(s)
    assert pne == minima and pne
    chosen = list(hubbits[sources[i]] for i in range(n))
    moved=[]
    for v, ii in group.items():
        if not any(main[v][1:]):
            for i in ii:
                if constant[i] > 0:
                    chosen[i] = 1-hubbits[v]
            continue
        L=sum((lightw[i] for i in ii),Q(0))
        removed=[]
        for i in sorted(ii,key=lambda q: (threshold[q],q)):
            if L > threshold[i]+lightw[i]:
                before=tuple(chosen)
                chosen[i]=1-hubbits[v]
                after=tuple(chosen)
                assert cc[before][i] > cc[after][i]
                moved.append(i)
                L-=lightw[i]
                removed.append(i)
                assert all(L>threshold[j] for j in removed)
    assert len(moved)==len(set(moved))
    assert tuple(chosen) in pne
    return {'states':len(states), 'directed_strict_edges':edge_count, 'exact_responses':len(pne), 'ordered_deletions':len(moved)}

def main():
    rng = random.Random(17201)
    instances = []
    # Boundary: zero and constant F; exact ties; empty lights; no sides.
    for coeff in ([Q(0)], [Q(3)], [Q(0),Q(1)], [Q(2),Q(0),Q(1)]):
        for ll in ([], [Q(1)], [Q(1),Q(1)], [Q(1,7),Q(2,3),Q(5)]):
            instances.append(([Q(2)], [0], ll, [0]*len(ll), [coeff], []))
    for rep in range(180):
        nh = rng.randint(1,3)
        nl = rng.randint(0,6)
        hw = [Q(rng.randint(1,9),rng.randint(1,5)) for _ in range(nh)]
        hb = [rng.randrange(2) for _ in range(nh)]
        lw = [Q(rng.randint(1,9),rng.randint(1,7)) for _ in range(nl)]
        src = [rng.randrange(nh) for _ in range(nl)]
        fs = [[Q(rng.randint(0,3),rng.randint(1,5)) for _ in range(rng.randint(0,4)+1)] for _ in range(nh)]
        sides=[]
        for _ in range(rng.randint(0,10)):
            if not nl: break
            ell=rng.randrange(nl)
            hs=[v for v in range(nh) if rng.randrange(2)]
            gg=[Q(rng.randint(0,3),rng.randint(1,5)) for _ in range(rng.randint(0,4)+1)]
            sides.append((ell,hs,gg))
        instances.append((hw,hb,lw,src,fs,sides))
    results=[audit(inst) for inst in instances]
    # The unique-light hypothesis is substantive, even when all hubs are inert.
    ws=[1,2,3]
    ee=[((0,1),2,2100),((0,2),2,1130),((1,2),2,499)]
    def multi_cost(s):
        ans=[Q(0)]*3
        for pair,k,a in ee:
            for i in pair:
                ans[i]+=a*sum(ws[j] for j in pair if s[i]==s[j])**k
        return ans
    rows=[]
    for s in product((0,1),repeat=3):
        current=multi_cost(s)
        ratios=[current[i]/multi_cost(s[:i]+(1-s[i],)+s[i+1:])[i] for i in range(3)]
        assert max(ratios)>1
        rows.append({'state':s,'costs':[str(c) for c in current], 'max_ratio':str(max(ratios))})
    assert min(Q(row['max_ratio']) for row in rows)==Q(20896,20875)
    def serial(x):
        if isinstance(x,Q): return str(x)
        if isinstance(x,(list,tuple)): return [serial(y) for y in x]
        return x
    out={'status':'all exact checks passed','seed':17201,'instances':len(instances),
         'states':sum(x['states'] for x in results), 'strict_edges':sum(x['directed_strict_edges'] for x in results),
         'ordered_deletions':sum(x['ordered_deletions'] for x in results),
         'finite_scope':'hub count at most 3; light count at most 6; degree at most 4; all literal full-resource costs and all light unilateral moves',
         'multi_light_counterexample':rows,
         'arithmetic':'fractions.Fraction; exact sign, no tolerance',
         'python':sys.version,
         'input_schema':['hub_weights','hub_bits','light_weights','source_ids','main_coefficient_vectors','sides [light_id,hub_ids,coefficient_vector]'],
         'actual_inputs':serial(instances),
         'instance_results':results,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
