"""Independent exact finite check of the profile-to-UM bridge.

Built from the statement received from root, before reading the author's proof.
Not a universal proof, and not an algorithm for the resource allocation problem.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json

def validate(values, profiles):
    assert len(values) >= 1
    assert len(values) == len(profiles)
    n = len(values[0])
    assert all(len(row) == n for row in values)
    assert all(v >= 0 for row in values for v in row)
    for fam in profiles:
        assert fam
        for c in fam:
            assert all(v >= 0 and isinstance(count, int) and 0 <= count <= n for v, count in c.items())
            assert sum(v*count for v, count in c.items()) > 0

def f(values, c, bundle):
    d = sum(v*count for v, count in c.items())
    return sum(v/d * min(count, sum(values[j] == v for j in bundle)) for v, count in c.items())

def frontier(values, profiles, owner):
    bundles = [{j for j, who in enumerate(owner) if who == i} for i in range(len(values))]
    return min(max(f(values[i], c, bundles[i]) for c in profiles[i]) for i in range(len(values)))

def build(values, profiles, keep_zero=True):
    validate(values, profiles)
    m, n = len(values), len(values[0])
    homes = {(i,k): n+sum(len(fam) for fam in profiles[:i])+k for i,fam in enumerate(profiles) for k,c in enumerate(fam)}
    jobs = []
    for i, fam in enumerate(profiles):
        for k, c in enumerate(fam):
            d = sum(v*count for v, count in c.items())
            for v, count in c.items():
                if not keep_zero and v == 0:
                    continue
                for t in range(count):
                    jobs.append({'kind':'copy','i':i,'k':k,'v':v,'w':v/d,'options':[(homes[i,k],v/d)]+[(j,F(1)) for j in range(n) if values[i][j] == v]})
    for i, fam in enumerate(profiles):
        jobs.append({'kind':'selector','i':i,'options':[(homes[i,k],F(1)) for k in range(len(fam))]})
    return homes, jobs, n+len(homes)

def forward(values, profiles, owner, homes, jobs, num_machines):
    m = len(values)
    bundles = [{j for j, who in enumerate(owner) if who == i} for i in range(m)]
    selected = [max(range(len(profiles[i])),key=lambda k: f(values[i],profiles[i][k],bundles[i])) for i in range(m)]
    available = [{v: sorted(j for j in bundles[i] if values[i][j] == v) for v in profiles[i][selected[i]]} for i in range(m)]
    loads = [F(0)]*num_machines
    for job in jobs:
        i = job['i']
        if job['kind'] == 'selector':
            dest, time = homes[i,selected[i]], F(1)
        elif job['k'] == selected[i] and available[i][job['v']]:
            dest, time = available[i][job['v']].pop(0), F(1)
        else:
            dest, time = homes[i,job['k']], job['w']
        assert (dest,time) in job['options']
        loads[dest] += time
    score = min(max(f(values[i],c,bundles[i]) for c in profiles[i]) for i in range(m))
    assert max(loads) <= 2-score

def inspect(values, profiles, keep_zero=True):
    homes, jobs, mm = build(values,profiles,keep_zero)
    m, n = len(values), len(values[0])
    val = F(0)
    resource_allocations = 0
    for owner in product(range(-1,m), repeat=n):
        val = max(val, frontier(values,profiles,owner))
        forward(values,profiles,owner,homes,jobs,mm)
        resource_allocations += 1
    best = F(2)
    all_actual = 0
    sub2_actual = 0
    # Full enumeration is deliberately confined to the tiny fixtures.
    for choices in product(*(range(len(job['options'])) for job in jobs)):
        all_actual += 1
        loads = [F(0)]*mm
        selected = [None]*m
        assignment = []
        for job, choice in zip(jobs, choices):
            dest, time = job['options'][choice]
            assignment.append(dest)
            loads[dest] += time
            if job['kind'] == 'selector':
                selected[job['i']] = next(k for k in range(len(profiles[job['i']])) if homes[job['i'],k] == dest)
        cmax = max(loads)
        best = min(best,cmax)
        if cmax >= 2:
            continue
        sub2_actual += 1
        bundles = [set() for i in range(m)]
        escaped = [F(0)]*m
        for job,dest in zip(jobs,assignment):
            i = job['i']
            if job['kind'] == 'copy' and job['k'] == selected[i] and dest < n:
                bundles[i].add(dest)
                escaped[i] += job['w']
        assert sum(map(len,bundles)) == len(set().union(*bundles))
        for i in range(m):
            assert f(values[i],profiles[i][selected[i]],bundles[i]) == escaped[i]
            assert loads[homes[i,selected[i]]] == 2-escaped[i]
            assert max(f(values[i],p,bundles[i]) for p in profiles[i]) >= 2-cmax
    assert best == 2-val, (values,profiles,best,val)
    return {'V':str(val),'OPT':str(best),'resource_allocations':resource_allocations,'all_actual':all_actual,'sub2_actual':sub2_actual}

fixtures = [
    ([[F(1)]], [[{F(1):1}]]),
    ([[F(1)],[F(1)]], [[{F(1):1}],[{F(1):1}]]),
    ([[F(1),F(1)],[F(1),F(1)]], [[{F(1):2}],[{F(1):2}]]),
    ([[F(0),F(2)]], [[{F(0):1,F(2):1},{F(1):0,F(2):2}]]),
    ([[F(1),F(2)],[F(2),F(1)]], [[{F(1):1},{F(2):1}],[{F(1):1},{F(2):1}]]),
    ([[F(1),F(2)]], [[{F(3):1}]]),
    ([[F(1,2**257),F(3,2**259)]], [[{F(1,2**257):1,F(3,2**259):1,F(2**263):0}]]),
    ([[F(1),F(1)]], [[{F(1):1},{F(1):1}]]),
]
results = [inspect(values,profiles,keep_zero) for values,profiles in fixtures for keep_zero in (True,False)]
catalog = [{F(1):1},{F(2):1},{F(1):1,F(2):1},{F(0):1,F(1):1}]
generated = 0
for vv in product(range(3), repeat=2):
    for pa,pb in combinations(range(len(catalog)),2):
        for keep_zero in (True,False):
            results.append(inspect([[F(v) for v in vv]],[[catalog[pa],catalog[pb]]],keep_zero))
        generated += 1
invalid = [([],[]), ([[F(1)]],[[]]), ([[F(1)]],[[{}]]), ([[F(1)]],[[{F(0):1}]]), ([[F(1)]],[[{F(1):0}]])]
for values,profiles in invalid:
    try:
        validate(values,profiles)
    except AssertionError:
        pass
    else:
        raise AssertionError('invalid domain accepted')
# The author's final non-submodularity fixture is independently evaluated by
# enumerating the complete finite count menu, rather than using its argument.
vv = [F(1,4),F(1,2),F(1,2),F(3,4)]
menu = []
for a,b,d in product(range(2),range(3),range(2)):
    c = {F(1,4):a,F(1,2):b,F(3,4):d}
    if sum(v*count for v,count in c.items()) >= 1:
        menu.append(c)
four = [max(f(vv,c,bundle) for c in menu) for bundle in ({0,1},{0,2},{0,1,2},{0})]
assert four == [F(3,5),F(3,5),F(1),F(1,4)]
assert four[0]+four[1] < four[2]+four[3]
print(json.dumps({'fixed_fixtures':results[:2*len(fixtures)], 'generated_fixture_structures':generated, 'zero_token_variants':2, 'total_fixture_variants':len(results), 'total_actual_assignments':sum(r['all_actual'] for r in results),'total_sub2_decodings':sum(r['sub2_actual'] for r in results),'invalid_domains_rejected':len(invalid),'non_submodular_values':list(map(str,four)), 'status':'exact finite checks only; statement-first core plus read-after edge checks'}))
