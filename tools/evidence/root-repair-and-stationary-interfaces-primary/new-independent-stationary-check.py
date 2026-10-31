"""New independent finite recheck from the frozen Markdown input, not the absent original audit."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import re

def rank(rows):
    a=[list(map(F,r)) for r in rows];out=0
    for c in range(len(a[0])):
        p=next((i for i in range(out,len(a)) if a[i][c]),None)
        if p is None:continue
        a[out],a[p]=a[p],a[out]
        z=a[out][c];a[out]=[v/z for v in a[out]]
        for i in range(len(a)):
            if i!=out and a[i][c]:
                z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[out])]
        out+=1
        if out==len(a):break
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    assert not args.output.exists(),'output must be a new path'
    raw=args.source.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='6dd6633786a99b8a4fb18303c1268429b03dbec0f6018f30575d281772c4f643'
    pairs=[]
    for line in raw.decode().splitlines():
        if not re.fullmatch(r'\|(?:\d+\|){6}',line):continue
        v=list(map(int,line.strip('|').split('|')))
        pairs.extend(zip(v[::2],v[1::2]))
    assert len(pairs)==21 and len(dict(pairs))==21
    clients=[mask for mask,count in pairs for _ in range(count)]
    assert len(clients)==1274 and all(0<mask<64 and count>0 for mask,count in pairs)
    def likes(mask,a):return bool(mask&(1<<a))
    def action(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        assert len(h)==2
        base=0 if h[1]<3 else 3
        return next(t for t in range(base,base+3) if t not in h)
    def finish(h):
        h=tuple(h)
        while len(h)<3:h+=action(h),
        return h
    def payoff(z,i):
        return sum((F(1,sum(likes(mask,a) for a in z)) for mask in clients if likes(mask,z[i])),F())
    def welfare(z):return sum(any(likes(mask,a) for a in z) for mask in clients)
    all_histories=[h for d in range(3) for h in product(range(6),repeat=d)]
    decisions=[];nonself=0;ties=0
    for h in all_histories:
        i=len(h);chosen=action(h)
        values=[payoff(finish(h+(a,)),i) for a in range(6)]
        slacks=[values[chosen]-v for v in values]
        assert min(slacks)>=0,(h,chosen,values)
        ties+=sum(s==0 for s in slacks)
        nonself+=sum(a!=chosen for a in range(6))
        decisions.append({'history':h,'action':chosen,'terminal':finish(h),'all_action_values':[str(v) for v in values],'slacks':[str(v) for v in slacks]})
    assert len(decisions)==43 and nonself==215
    z=finish(())
    pay=[payoff(z,i) for i in range(3)]
    assert z==(0,3,4) and pay==[F(541,2),F(613,2),F(269)]
    w=welfare(z);opt=max(welfare(t) for t in product(range(6),repeat=3))
    assert w==846 and opt==1032 and sum(pay)==w
    roots=[finish((a,)) for a in range(6)]
    kernel=[[F(Counter(z[1:])[b],2) for b in range(6)] for z in roots]
    pi=[F(1,4),F(1,4),F(),F(1,4),F(1,4),F()]
    assert [sum(pi[a]*kernel[a][b] for a in range(6)) for b in range(6)]==pi
    eq=[[kernel[a][b]-int(a==b) for a in range(6)] for b in range(6)]+[[F(1)]*6]
    assert rank(eq)==6
    def frac_price(q,t):
        return sum((1/(F(1)+3*sum(q[a] for a in range(6) if likes(mask,a))) for mask in clients if likes(mask,t)),F())
    stationary=[frac_price(pi,t) for t in range(6)]
    assert stationary[2]==F(123652,455) and stationary[2]-pay[0]==F(1149,910)
    uniform=[frac_price([F(1,6)]*6,t) for t in range(6)]
    assert uniform==[F(2187,10),F(1789,10),F(5399,30),F(441,2),F(5279,30),F(1639,10)]
    static=[sum((F(1,1+likes(mask,0)+likes(mask,5)) for mask in clients if likes(mask,t)),F()) for t in range(6)]
    assert max(uniform)==F(441,2)<pay[0] and max(static)==252
    report={
        'implementation':'new independent standard-library Fraction checker; absent original audit not executed',
        'source_md_sha256':hashlib.sha256(raw).hexdigest(),
        'source_id':'c57e4ec366e7af1be467',
        'client_input':'all 21 positive mask multiplicities parsed from bound original Markdown; expanded to distinct unit clients',
        'positive_types':pairs,'unit_clients':len(clients),'players':3,'legal_labels':list(range(6)),
        'full_decision_histories':43,'all_action_comparisons':258,'self_comparisons':43,'nonself_comparisons':nonself,
        'total_ties_including_self':ties,'minimum_slack':str(min(F(s) for r in decisions for s in r['slacks'])),
        'actual':z,'payoffs':[str(v) for v in pay],'welfare':w,'optimal_3':opt,'half_slack':2*w-opt,
        'all_43_history_rows':decisions,
        'six_forced_root_terminals':roots,'tail_kernel':[[str(v) for v in row] for row in kernel],
        'stationary_pi':[str(v) for v in pi],'stationary_equations_plus_normalization_rank':6,
        'six_stationary_mean_fractional_query_prices':[str(v) for v in stationary],
        'stationary_cap':str(max(stationary)),'query2_minus_actual_root':str(stationary[2]-pay[0]),
        'six_free_uniform_fractional_query_prices':[str(v) for v in uniform],'free_uniform_cap':str(max(uniform)),
        'integer_static_background':[0,5],'six_integer_static_query_prices':[str(v) for v in static],
        'integer_static_cap':str(max(static)),'W_minus_3v3_lower_bound':str(w-3*max(static)),
        'scope':'finite exact counterexample to prescribed stationary-mean full-query cap only; no general half failure, novelty or external review',
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'histories':43,'all_comparisons':258,'unit_clients':1274,'welfare':w,'OPT3':opt,'stationary_cap':str(max(stationary)),'query2_gap':str(stationary[2]-pay[0]),'passed':True},ensure_ascii=False))

if __name__=='__main__':main()
