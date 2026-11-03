"""One fixed audit of saved decimal points; no search, LP, or original main."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json, hashlib, itertools, time

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'original/research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/early_opportunity'

def compositions(k,n):
    if k==1:
        yield (n,); return
    for a in range(n+1):
        for tail in compositions(k-1,n-a): yield (a,)+tail

def audit(rec,k,m,bg=None):
    count=bg is not None
    bg=tuple(bg or [0]*k)
    remaining=m-sum(bg)
    raw=rec['actions'] if count else rec['cert']['actions']
    key='counts' if count else 'history'
    actions={tuple(a[key]):a['action'] for a in raw}
    assert len(actions)==len(raw)
    if count:
        expected={tuple(a+b for a,b in zip(bg,q)) for d in range(remaining) for q in compositions(k,d)}
    else:
        expected={h for d in range(m) for h in itertools.product(range(k),repeat=d)}
    assert set(actions)==expected
    assert all(type(a) is int and 0<=a<k for a in actions.values())
    weights={int(mask):F(str(w)).limit_denominator(10**6) for mask,w in rec['weights'].items()}
    assert all(0<mask<1<<k and w>=0 for mask,w in weights.items())
    @lru_cache(None)
    def terminal(q):
        if (sum(q) if count else len(q))==m:
            return q if count else tuple(q.count(a) for a in range(k))
        return terminal(child(q,actions[q]))
    def child(q,a):
        if count:
            t=list(q);t[a]+=1;return tuple(t)
        return q+(a,)
    @lru_cache(None)
    def pay(q,a):
        return sum((w/F(sum(q[b] for b in range(k) if mask>>b&1)) for mask,w in weights.items() if mask>>a&1),F())
    minimum=None;bad=[];comparisons=0
    for q,a in actions.items():
        own=pay(terminal(q),a)
        for b in range(k):
            if b==a:continue
            slack=own-pay(terminal(child(q,b)),b);comparisons+=1
            if minimum is None or slack<minimum:minimum=slack
            if slack<0:bad.append({'node':q,'chosen':a,'deviation':b,'slack':str(slack)})
    root=terminal(bg if count else ())
    assert tuple(rec['root'])==root
    if not count:
        q=();path=[]
        while len(q)<m:
            a=actions[q];path.append(a);q=child(q,a)
        assert path==rec['path']
    a=rec['target_action'];assert root[a]>0
    def coverage(support):
        return sum((w for mask,w in weights.items() if any(mask>>a&1 for a in support)),F())
    welfare=coverage([a for a,c in enumerate(root) if c])
    comparison=coverage(rec['comparison'])
    coefficient=m if count else m-1
    gap=comparison-welfare-coefficient*pay(root,a)
    return {'nodes':len(actions),'nonself_comparisons':comparisons,'represented_ordered_nodes':sum(k**d for d in range(remaining)),
            'weights_count':len(weights),'mass':str(sum(weights.values(),F())),
            'root':root,'W':str(welfare),'comparison_coverage':str(comparison),'u':str(pay(root,a)),
            'coefficient':coefficient,'exact_fixed_gap':str(gap),'original_float_value':rec['value'],
            'minimum_ic_slack':str(minimum),'violations':bad,'rational_recovery_rule':'Fraction(str(float)).limit_denominator(1000000)',
            'normalized_mass_is_one':sum(weights.values(),F())==1,'scope':'fixed legal suffix SPE; old players unoptimized' if count else 'fixed full-history root policy'}

if __name__=='__main__':
    started=time.monotonic();output={'scope':'all saved fixed points only; no LP optimum or universal claim','original_searches':0,'records':{}}
    for name in ['bg_m5r4k6.json','canonical_strong.json']:
        p=SOURCE/name;x=json.loads(p.read_text());rows=[]
        for i,r in enumerate(x['records']):
            if name.startswith('bg_'):
                row=audit(r,x['parameters']['topics'],x['parameters']['old']+x['parameters']['future'],r['background'])
            else:row=audit(r,len(r['root']),len(r['path']))
            row['index']=i;row['label_or_trial']=r.get('label',r.get('trial'));rows.append(row)
        output['records'][name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'points':rows}
    output['elapsed_seconds']=time.monotonic()-started
    (BASE/'saved-point-audit.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    for name,group in output['records'].items():
        print(name,'points',len(group['points']),'nodes',sum(a['nodes'] for a in group['points']),
              'nonself',sum(a['nonself_comparisons'] for a in group['points']),
              'negative IC',sum(len(a['violations']) for a in group['points']),
              'mass failures',sum(not a['normalized_mass_is_one'] for a in group['points']))
    print('seconds',output['elapsed_seconds'])
