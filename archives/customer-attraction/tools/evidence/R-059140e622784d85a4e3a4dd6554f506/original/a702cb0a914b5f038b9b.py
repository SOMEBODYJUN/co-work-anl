"""Test a precise general beta-packing candidate on old complete SPEs.

No search for new games, and a negative finite test is not a HALF result.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def run(name):
    data=json.loads(Path(f'examples/customer_attraction/{name}.json').read_text())
    cert=json.loads(Path(f'evidence/certificates/customer_attraction/{name}.json').read_text())
    m,k=data['players'],len(data['topics'])
    clients=[frozenset(c['topics']) for c in data['customers'] for _ in range(c.get('multiplicity',1))]
    topics=[frozenset(x for x,t in enumerate(clients) if a in t) for a in range(k)]
    sigma={tuple(t['history']):t['action'] for t in cert.get('strategy',cert)['actions']}
    hs=[h for i in range(m) for h in product(range(k),repeat=i)]
    assert set(hs)==set(sigma)
    @lru_cache(None)
    def finish(h):
        while len(h)<m:h+=(sigma[h],)
        return h
    @lru_cache(None)
    def loads(z):return tuple(sum(a in t for a in z) for t in clients)
    @lru_cache(None)
    def pay(z,i):
        c=loads(z)
        return sum((F(1,c[x]) for x in topics[z[i]]),F())
    z=finish(())
    u=[pay(z,i) for i in range(m)]
    rows={};ics=0
    for h in hs:
        i=len(h);a=sigma[h];b=finish(h);aa=finish(z[:i]+(a,))
        cb,ca=loads(b),loads(aa);v,d=pay(b,i),pay(aa,i)
        for action in range(k):
            assert v>=pay(finish(h+(action,)),i);ics+=1
        assert d<=u[i]
        edges=[];n=F()
        for x in topics[a]:
            ja={j for j in range(m) if j!=i and x in topics[aa[j]]}
            jb={j for j in range(m) if j!=i and x in topics[b[j]]}
            unit=F(1,ca[x]*cb[x]);n+=len(jb-ja)*unit
            for j in sorted(ja-jb):edges.append((j,x,unit))
        p=sum((q for j,x,q in edges),F());refund=n+u[i]-d
        assert v==u[i]+p-refund and 0<=refund<=u[i]
        keep=[];cancel=min(p,refund)
        for j,x,q in sorted(edges,key=lambda e:(e[0]>=i,e[0],e[1])):
            removed=min(cancel,q);cancel-=removed
            if q>removed:keep.append((j,x,q-removed))
        assert cancel==0
        assert min(v,u[i])+sum((q for j,x,q in keep),F())==v
        rows[h]=(i,v,keep,aa)
        if aa!=z:
            assert next(j for j in range(m) if aa[j]!=z[j])==i
        for j,x,q in keep:
            if j>i:
                dest=aa[:j]
                assert finish(dest)==aa
                if aa!=z:
                    assert next(l for l in range(m) if aa[l]!=z[l])==i
    opt=max(sum(c>0 for c in loads(tup)) for tup in product(range(k),repeat=m))
    opt_tuples=[tup for tup in product(range(k),repeat=m) if sum(c>0 for c in loads(tup))==opt]
    maxima={'role':F(),'action':F(),'cap2':F()}; witnesses={}
    # The first-containing-owner convention is a fully specified legal owner.
    for tup in opt_tuples:
        owner={x:next(i for i,a in enumerate(tup) if x in topics[a]) for x,c in enumerate(loads(tup)) if c}
        mass=defaultdict(F);terminal=defaultdict(F)
        for x,i in owner.items():
            leaf=finish(z[:i]+(tup[i],));c=loads(leaf)[x]
            assert c>0
            for j,a in enumerate(leaf):
                if x not in topics[a]:continue
                if j<=i:terminal[j]+=F(1,c)
                else:mass[leaf[:j]]+=F(1,c)
        role=defaultdict(F);action=defaultdict(F)
        for h in hs:
            if not mass[h]:continue
            i,v,edges,aa=rows[h]
            assert v>0
            beta=mass[h]/v
            role[i]+=beta;action[i,sigma[h]]+=beta
            terminal[i]+=beta*min(v,u[i])
            for j,x,q in edges:
                if j<i:terminal[j]+=beta*q
                else:mass[aa[:j]]+=beta*q
        assert sum(terminal.values(),F())==opt
        vals={'role':max(role.values(),default=F()),'action':max(action.values(),default=F()),
              'cap2':max((terminal[i]/u[i] for i in range(m) if u[i]),default=F())}
        for field,value in vals.items():
            if value>maxima[field]:
                maxima[field]=value
                witnesses[field]={'tuple':list(tup),'value':str(value),'role_beta':{str(i):str(v) for i,v in role.items()},
                                  'action_beta':{str(ia):str(v) for ia,v in action.items()},
                                  'terminal':{str(i):str(v) for i,v in terminal.items()},'u':list(map(str,u))}
    return {'name':name,'IC_checks':ics,'optimal_tuples':len(opt_tuples),'maxima':{q:str(v) for q,v in maxima.items()},'witnesses':witnesses}


if __name__=='__main__':
    names=['portfolio_matching_failure','root_tax_failure','individual_security_failure',
           'eight_cce_welfare_gap','coverage_opportunity_failure','prefix_balance_failure']
    print(json.dumps({'status':'computed','scope':'old complete SPEs; tests beta-packing and fixed legal owners only',
                      'cases':[run(name) for name in names]},indent=2))
