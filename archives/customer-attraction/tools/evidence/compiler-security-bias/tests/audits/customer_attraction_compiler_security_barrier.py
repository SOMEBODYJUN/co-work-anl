"""Independent exact arithmetic audit for the uniform-bias security obstruction."""
import argparse,itertools,json,math,random
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,help='new JSON report path; existing files are rejected')
args=parser.parse_args()
if args.output is not None and args.output.exists():
    parser.error(f'refusing to overwrite existing output: {args.output}')

def coeffs(p,n):
    masks=np.arange(1,1<<p,dtype=np.int32)
    mem=((masks[:,None]>>np.arange(p))&1).astype(np.int64)
    D=math.lcm(*range(1,n+1))
    def payoff(profile,a):
        q=np.bincount(profile,minlength=p)
        den=mem@q
        return np.where(mem[:,a],D//np.maximum(den,1),0)
    return mem,D,payoff

reports=[]
for p in range(2,9):
 for n in range(2,p+1):
    mem,D,payoff=coeffs(p,n)
    backgrounds=list(itertools.combinations(range(p),n-1));L=len(backgrounds)
    duals=np.stack([sum((payoff(bg+(a,),a) for bg in backgrounds),np.zeros((1<<p)-1,dtype=np.int64)) for a in range(p)])
    b=Fraction((1<<p)-(1<<(p-n)),n)
    c=Fraction((1<<(p-n))*((1<<n)-n-1),n*p)
    assert c>=Fraction(1,4)
    assert all(Fraction(int(v.sum()),D*L)==b-c for v in duals)
    rng=random.Random(100*p+n)
    x=np.array([rng.randint(-4,4) for _ in range((1<<p)-1)],dtype=np.int64)
    M=int(np.abs(x).sum());K=4*M+1;r=x+K
    assert r.min()>0
    cap=Fraction(int(max(duals@r)),D*L)
    bound=K*c-M
    checked=0;min_gap=None
    for s in itertools.combinations(range(p),n):
     for a in s:
        own=Fraction(int(payoff(s,a)@r),D)
        gap=own-cap
        assert gap>=bound
        assert gap>=Fraction(1,4)
        min_gap=gap if min_gap is None else min(min_gap,gap)
        checked+=1
    reports.append({'p':p,'n':n,'backgrounds':L,'profile_player_checks':checked,'c':str(c),'min_actual_gap':str(min_gap),'theoretical_gap':str(bound)})

# Exact fixed-certificate cap, independent of its SPE verification.
d=json.loads((ROOT/'history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json').read_text())
p=d['m'];n=d['n'];mem,D,payoff=coeffs(p,n)
policy={tuple(e['history']):e['action'] for e in d['policy']}
path=()
while len(path)<n:path=path+(policy[path],)
r=np.array([d['weights'][str(B)] for B in range(1,1<<p)],dtype=np.int64)
backgrounds=list(itertools.combinations(range(p),n-1));L=len(backgrounds)
rowvalues=[]
for a in range(p):
 v=sum(int(payoff(bg+(a,),a)@r) for bg in backgrounds)
 rowvalues.append(Fraction(v,D*L))
cap=max(rowvalues)
values=[Fraction(int(payoff(path,a)@r),D) for a in path]
assert all(v>cap for v in values)
assert cap==Fraction(138250151,24)
assert values==[6135345,6135380,6135380,6135371]
existing={'p':p,'n':n,'path':path,'dual_backgrounds':L,'dual_row_values':list(map(str,rowvalues)),'dual_cap':str(cap),'actual_player_payoffs':list(map(str,values)),'actual_minus_cap':list(map(str,[v-cap for v in values]))}
result={'status':'exact_checks_passed','formula_cases':reports,'saved_counterexample_security_cap':existing}
if args.output is not None:
    with args.output.open('x') as handle:
        json.dump(result,handle,indent=2)
        handle.write('\n')
print(json.dumps({'formula_cases':len(reports),'distinct_profile_player_checks':sum(r['profile_player_checks'] for r in reports),'saved_counterexample':existing},indent=2))
