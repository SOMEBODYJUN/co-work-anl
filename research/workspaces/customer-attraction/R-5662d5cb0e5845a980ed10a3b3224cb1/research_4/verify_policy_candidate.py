"""Independent integer audit of a numerical search candidate.

Rationalizing a numerical vertex is discovery only until every IC passes.
All n=6 shares become integers after scaling utilities by lcm(1,...,6)=60.
"""
import argparse,json,math
from fractions import Fraction
from pathlib import Path
from itertools import combinations

def compositions(n,k):
    if k==1:yield (n,);return
    for v in range(n+1):
        for q in compositions(n-v,k-1):yield (v,)+q

def main():
    ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('--denominator',type=int,default=1000000)
    ap.add_argument('--output');a=ap.parse_args();data=json.loads(Path(a.candidate).read_text())
    k,m=data['k'],data['m']; assert m==6
    rational={int(b):Fraction(v).limit_denominator(a.denominator) for b,v in data['weights'].items()}
    scale=math.lcm(*[v.denominator for v in rational.values()])
    weights={b:int(v*scale) for b,v in rational.items() if v>0}
    common=math.gcd(*weights.values());weights={b:v//common for b,v in weights.items()}
    distinct=all(any(v and bool(b&(1<<i))!=bool(b&(1<<j)) for b,v in weights.items()) for i,j in combinations(range(k),2))
    leaves=list(compositions(m,k));util={}; welfare={}
    for q in leaves:
        vals=[0]*k;W=0
        for b,v in weights.items():
            load=sum(q[j] for j in range(k) if b&(1<<j))
            if not load:continue
            W+=v
            for j in range(k):
                if b&(1<<j):vals[j]+=v*(60//load)
        util[q]=vals;welfare[q]=W
    violations=[];checked=0
    if 'ordered_policy' in data:
        acts={int(t):vals for t,vals in data['ordered_policy'].items()}
        counts=[[(0,)*k]]
        for t in range(m):
            counts.append([q[:j]+(q[j]+1,)+q[j+1:] for q in counts[-1] for j in range(k)])
        terminals=counts[m]
        for t in range(m-1,-1,-1):
            assert len(acts[t])==len(counts[t])
            parent=[]
            for idx,q in enumerate(counts[t]):
                chosen=acts[t][idx];kids=terminals[k*idx:k*(idx+1)]
                own=util[kids[chosen]][chosen]
                for alt in range(k):
                    if alt==chosen:continue
                    checked+=1
                    slack=own-util[kids[alt]][alt]
                    if slack<0:violations.append((t,idx,chosen,alt,slack))
                parent.append(kids[chosen])
            terminals=parent
        actual=terminals[0]
    else:
        acts={tuple(map(int,q.split(','))):j for q,j in data['policy'].items()}
        terminals={q:q for q in leaves}
        for t in range(m-1,-1,-1):
            for q in compositions(t,k):
                chosen=acts[q]
                kids=[terminals[q[:j]+(q[j]+1,)+q[j+1:]] for j in range(k)]
                own=util[kids[chosen]][chosen]
                for alt in range(k):
                    if alt==chosen:continue
                    checked+=1;slack=own-util[kids[alt]][alt]
                    if slack<0:violations.append((q,chosen,alt,slack))
                terminals[q]=kids[chosen]
        actual=terminals[(0,)*k]
    opt=0;optsets=None
    for count in range(1,min(m,k)+1):
        for ts in combinations(range(k),count):
            mask=sum(1<<j for j in ts)
            val=sum(v for b,v in weights.items() if b&mask)
            if val>opt:opt,optsets=val,ts
    W=welfare[actual]
    report={'m':m,'topics':k,'distinct_topic_sets':distinct,'unit_customers':sum(weights.values()),
            'support_types':len(weights),'checked_IC':checked,'negative_IC_count':len(violations),
            'first_negative_IC':violations[:5],'actual_counts':actual,'welfare':W,'OPT6':opt,
            'optimal_topics':optsets,'ratio':str(Fraction(opt,W)) if W else None,
            'strict_original_counterexample':bool(distinct and not violations and opt>2*W),
            'integer_weights':weights}
    print(json.dumps(report,indent=2))
    if a.output:Path(a.output).write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
