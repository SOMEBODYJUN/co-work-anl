"""Independent literal audit of the frozen actual clock candidate and fixture.
Only input JSON is read; no author implementation or output is imported.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from random import Random
from pathlib import Path
import argparse, hashlib, json, platform, sys

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=None)
args=parser.parse_args()
REPO=Path(__file__).resolve().parents[4]
FIXTURE=REPO/'examples/weighted_congestion/anchored_actual_clock_degree43.json'
CANDIDATE=REPO/'research/current/weighted_congestion/anchored_clock_actual_margins.md'
EXPECTED='e98f382e8c16cc2ea343f5c58e4f150e311fb3300a8462130a41d21c8c7a0908'
CANONICAL_SHA=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
inp=json.loads(FIXTURE.read_text())
w=list(map(Q,inp['weights']))
a=Q(inp['alpha'])
n=len(w)

# Each tuple is (incidence[(player, action-0 resource)], coefficient, degree).
# A signature 0 means absent; +1 uses resource 0 on action 0; -1 uses 1.
base=[]
for pair in inp['base_pairs']:
    incidence=[(i, 0 if sig==1 else 1) for i,sig in enumerate(pair['signature']) if sig]
    base.append((incidence,Q(pair['coefficient']),int(pair['degree'])))
clock=[]
for pair in inp['clock_pairs']:
    ids=[0]+pair['pair']
    incidence=list(zip(ids,pair['target']))
    total=sum((w[i] for i in ids),Q(0))
    degree=int(pair['degree'])
    clock.append((incidence,Q(pair['amplitude'])/total**degree,degree))


def literal_cost(resources,state,i):
    total=Q(0)
    for incidence,coef,degree in resources:
        own=[initial^state[k] for k,initial in incidence if k==i]
        if not own:
            continue
        load=sum((w[k] for k,initial in incidence if (initial^state[k])==own[0]),Q(0))
        total+=coef*load**degree
    return total


def literal_margin(resources,state,i):
    after=list(state);after[i]^=1
    return literal_cost(resources,state,i)-a*literal_cost(resources,after,i)

ring={}
s=[0]*n
for turn in range(2*n):
    i=turn%n
    ring[tuple(s)]=i
    s[i]^=1
assert s==[0]*n and len(ring)==2*n
allstates=list(product((0,1),repeat=n))
B=max(literal_cost(base,s,i) for s in allstates for i in range(n))
eta=min(literal_margin(base,s,i) for s,i in ring.items())
assert B>0 and eta>0
rows=[]
for s in allstates:
    if s in ring:
        i=ring[s];kind='legal'
    else:
        i=next(k for k in range(1,n) if s[k]!=s[0]);kind='illegal_first_opposite'
        assert any(s[j]==s[0] for j in range(i+1,n))
    bm=literal_margin(base,s,i)
    cm=literal_margin(clock,s,i)
    margin=literal_margin(base+clock,s,i)
    assert margin==bm+cm and margin>0
    rows.append({'state':''.join(map(str,s)),'player':i,'kind':kind,
                 'base_margin':str(bm),'clock_margin':str(cm),'total_margin':str(margin)})
assert sum(r['kind']=='legal' for r in rows)==8
assert sum(r['kind']!='legal' for r in rows)==8
minimum_margin=min(Q(row['total_margin']) for row in rows)
assert minimum_margin>Q(1,4000)
assert all(literal_margin(base+clock,s,i)==literal_margin(base+clock,tuple(1-x for x in s),i)
           for s in allstates for i in range(n))

L=(n-1)*(n-2)//2
delta=max(1-min(w[0],w[i],w[j])/(w[0]+w[i]+w[j]) for i,j in combinations(range(1,n),2))
threshold=eta/(4*a*a*B*L)
D=0
while delta**D>threshold:
    D+=1
assert delta==Q(12,13) and D==91
assert delta**91<=threshold<delta**90

# Audit the new ordered-weight inequalities directly against literal resource margins.
rng=Random(20261015)
ordered_checks=0
for _ in range(200):
    ws=sorted([Q(rng.randint(1,9),rng.randint(1,9)) for _ in range(3)],reverse=True)
    wa,b,c=ws
    alpha=Q(rng.randint(2,20))
    maxdegree=rng.randint(0,8)
    coeff=[Q(rng.randint(0,7),rng.randint(1,7)) for _ in range(maxdegree+1)]
    def f(x):return sum((v*x**k for k,v in enumerate(coeff)),Q(0))
    ell=alpha*f(wa+b)-f(wa+c)
    gain=f(wa+b+c)-f(wa+b)+alpha*(f(b+c)-f(b))
    ratios=[]
    for k in range(maxdegree+1):
        num=(wa+b+c)**k-(wa+b)**k+alpha*((b+c)**k-b**k)
        denom=alpha*(wa+b)**k-(wa+c)**k
        assert denom>0
        ratios.append(num/denom)
    exact=max(ratios)
    r=c/(wa+b)
    bound=((1+r)**maxdegree-1+alpha*maxdegree*r)/(alpha-1)
    assert exact<=bound and gain<=exact*ell
    assert ell>0 or not any(coeff)
    ordered_checks+=1

# Author's distinct highest-degree counterexample, exactly recomputed.
wa,b,c,alpha=Q(10),Q(1),Q(1),Q(2)
ratios=[((wa+b+c)**k-(wa+b)**k+alpha*((b+c)**k-b**k))/
        ((wa+b)**k+(wa+c)**k+(b+c)**k) for k in range(3)]
assert ratios==[Q(0),Q(1,8),Q(29,246)] and ratios[1]>ratios[2]

# All-player conditional barrier: recompute each monomial column by actual
# current/post-flip loads; evaluate the explicit fixture's preconditions.
bstate=(0,1,0,1)
gamma=[]
s=[0]*n
for i in range(n):
    gamma.append(literal_margin(base,s,i))
    s[i]^=1
Gamma=sum(gamma,Q(0))
K=[-literal_margin(base,bstate,i) for i in range(n)]
assert all(x>=0 for x in K)
conditional_barriers=[]
for degree in range(8):
    kappas=[Q(0)]*n
    for i,j in combinations(range(1,n),2):
        incidence=[(0,0),(i,1),(j,0)]
        pairloads=[w[0]+w[i],w[0]+w[j],w[i]+w[j]]
        for player in (0,i,j):
            own=next(bit^bstate[h] for h,bit in incidence if h==player)
            current=sum((w[h] for h,bit in incidence if (bit^bstate[h])==own),Q(0))
            after=w[player]+sum((w[h] for h,bit in incidence if h!=player and (bit^bstate[h])!=own),Q(0))
            for k in range(degree+1):
                value=(current**k-a*after**k)/sum((load**k for load in pairloads),Q(0))
                # Cross-check the column against literal resource evaluation.
                assert value==literal_margin([(incidence,Q(1),k)],bstate,player)/sum((load**k for load in pairloads),Q(0))
                kappas[player]=max(kappas[player],value)
    preconditions=[K[i]>=kappas[i]*Gamma/(a-1) for i in range(n)]
    conditional_barriers.append({'D':degree,'kappas':list(map(str,kappas)),
                                 'preconditions_by_player':preconditions})
assert [all(row['preconditions_by_player']) for row in conditional_barriers]==[True,True,False,False,False,False,False,False]

# Positive-part full-trigger efficiency is nondecreasing in monomial degree.
fulltrigger_checks=0
for _ in range(100):
    wt=[Q(rng.randint(1,9),rng.randint(1,9)) for _ in range(3)]
    alpha=Q(rng.randint(1,20))
    W=sum(wt,Q(0)); pairloads=[W-x for x in wt]
    for player in range(3):
        efficiencies=[max(Q(0),(W**k-alpha*wt[player]**k)/sum((x**k for x in pairloads),Q(0))) for k in range(10)]
        assert all(efficiencies[k]<=efficiencies[k+1] for k in range(9))
        fulltrigger_checks+=1

# In a nontrigger state even positive actual-margin efficiency can peak below D.
current,after,third,alpha=Q(11),Q(3),Q(12),Q(2)
nontrigger=[max(Q(0),(current**k-alpha*after**k)/(current**k+after**k+third**k)) for k in range(5)]
assert nontrigger==[Q(0),Q(5,26),Q(103,274),Q(1277,3086),Q(14479,35458)]
assert max(nontrigger)==nontrigger[3] and nontrigger[3]>nontrigger[4]

output={'reviewed_candidate_sha256':EXPECTED,'canonical_manuscript_sha256':CANONICAL_SHA,
        'fixture_sha256':hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':platform.python_version(),'command':' '.join(sys.argv),
        'arithmetic':'fractions.Fraction, no floating point',
        'seed':20261015,'ordered_efficiency_checks':ordered_checks,
        'fixture':{'B':str(B),'eta':str(eta),'L':L,'delta':str(delta),
                   'uniform_budget_threshold':str(threshold),'uniform_budget_minimum_D':D,
                   'delta_power_91':str(delta**91),'delta_power_90':str(delta**90),
                   'degree':max(r[2] for r in base+clock),
                   'minimum_selected_margin':str(minimum_margin),
                   'minimum_margin_states':[row['state'] for row in rows if Q(row['total_margin'])==minimum_margin],
                   'minimum_margin_strictly_above':'1/4000',
                   'all_selected_margins_positive':True,'all_state_rows':rows},
        'highest_degree_counterexample':list(map(str,ratios)),
        'all_player_conditional_barrier':{'Gamma':str(Gamma),'base_stability_gaps_K':list(map(str,K)),
                                         'fixture_degree_checks':conditional_barriers,
                                         'fulltrigger_efficiency_checks':fulltrigger_checks,
                                         'nontrigger_efficiencies':list(map(str,nontrigger))},
        'result':'PASS; fixed fixture and finite formula audits only'}
data=json.dumps(output,ensure_ascii=False,indent=2)+'\n'
if args.output:
    with args.output.open('x') as stream:stream.write(data)
    print(json.dumps({'output':str(args.output),'result':output['result']}))
else:
    print(data,end='')
