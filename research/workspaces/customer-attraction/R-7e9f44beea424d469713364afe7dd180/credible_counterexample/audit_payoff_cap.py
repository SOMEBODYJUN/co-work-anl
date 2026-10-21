#!/usr/bin/env python3
"""Self-contained definition-level replay; no canonical implementation imports."""
import json
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path

HERE=Path(__file__).parent

def audit(name):
    d=json.loads((HERE/name).read_text());inst=d['instance'];p=len(inst['topics']);m=inst['players']
    clients=[set(t['topics']) for t in inst['customers'] for _ in range(t['multiplicity'])]
    action={tuple(t['history']):t['action'] for t in d['strategy']['actions']}
    assert set(action)=={h for k in range(m) for h in product(range(p),repeat=k)}
    def utilities(path):
        pay=[Q(0)]*m
        for likes in clients:
            who=[j for j,a in enumerate(path) if a in likes]
            for j in who:pay[j]+=Q(1,len(who))
        return pay
    ends={};comparisons=[]
    def replay(h):
        if len(h)==m:ends[h]=h;return h
        branches={a:replay(h+(a,)) for a in range(p)}
        actual=branches[action[h]];own=utilities(actual)[len(h)]
        vals=[utilities(branches[a])[len(h)] for a in range(p)]
        assert own==max(vals),(h,action[h],vals)
        comparisons.append({'history':h,'action':action[h],'deviation_payoffs':list(map(str,vals))})
        ends[h]=actual;return actual
    path=replay(());pay=utilities(path);w=sum(any(a in likes for a in path) for likes in clients)
    opt=max(sum(any(a in likes for a in S) for likes in clients) for S in combinations(range(p),min(m,p)))
    assert list(path)==d['path'] and list(map(str,pay))==d['payoffs']
    assert w==d['welfare']==23 and opt==d['optimum']==23
    assert (m+1)*pay[-1]>2*w and pay[-1]>2*pay[0]
    root_table=[str(utilities(ends[(a,)])[0]) for a in range(p)]
    second_table=[[str(utilities(ends[(a,b)])[1]) for b in range(p)] for a in range(p)]
    last_max=[[str(max(utilities((a,b,c))[2] for c in range(p))) for b in range(p)] for a in range(p)]
    markov=all(action[h]==action[tuple(reversed(h))] for h in action if len(h)==2)
    return {'input':name,'players':m,'topics':p,'unit_customers':len(clients),'path':path,'payoffs':list(map(str,pay)),
      'welfare':w,'optimum':opt,'complete_histories':len(action),'all_action_comparisons':len(action)*p,
      'strict_deviation_inequalities':sum(Q(x)<utilities(ends[tuple(c['history'])])[len(c['history'])] for c in comparisons for x in c['deviation_payoffs']),
      'root_deviation_payoffs':root_table,'second_deviation_payoffs':second_table,'last_maxima':last_max,
      'count_markov':markov,'all_comparisons':sorted(comparisons,key=lambda z:(len(z['history']),z['history']))}

def main():
    reports=[audit(n) for n in ('payoff_cap_failure.json','payoff_cap_failure_markov.json')]
    out={'identity':'counterexample to aggregate payoff cap and pairwise factor-two cap only; Q-CAG-HALF remains open','reports':reports}
    (HERE/'payoff_cap_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in reports[-1].items() if k!='all_comparisons'},indent=2))

if __name__=='__main__':main()
