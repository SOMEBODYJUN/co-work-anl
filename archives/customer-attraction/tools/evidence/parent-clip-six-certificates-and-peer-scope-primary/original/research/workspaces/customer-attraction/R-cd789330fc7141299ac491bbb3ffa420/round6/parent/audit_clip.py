"""Exact old-certificate regression, not a new game or capacity proof."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def run(name):
    data=json.loads(Path(f'examples/customer_attraction/{name}.json').read_text())
    cert=json.loads(Path(f'evidence/certificates/customer_attraction/{name}.json').read_text())
    m,k=data['players'],len(data['topics'])
    clients=[set(c['topics']) for c in data['customers'] for _ in range(c.get('multiplicity',1))]
    topics=[{x for x,t in enumerate(clients) if a in t} for a in range(k)]
    sigma={tuple(t['history']):t['action'] for t in cert.get('strategy',cert)['actions']}
    histories=[h for i in range(m) for h in product(range(k),repeat=i)]
    assert set(histories)==set(sigma)
    def finish(h):
        h=tuple(h)
        while len(h)<m:h+=(sigma[h],)
        return h
    def loads(z):return [sum(a in t for a in z) for t in clients]
    def pay(z,i):
        c=loads(z)
        return sum((F(1,c[x]) for x in topics[z[i]]),F())
    z=finish(())
    u=[pay(z,i) for i in range(m)]
    rows={};ic=0;clipped=0
    for h in histories:
        i=len(h);a=sigma[h];b=finish(h);aa=finish(z[:i]+(a,))
        cb,ca=loads(b),loads(aa);v,d=pay(b,i),pay(aa,i)
        for action in range(k):
            assert v>=pay(finish(h+(action,)),i);ic+=1
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
        assert sum((q for j,x,q in keep),F())==max(v-u[i],F())
        assert min(v,u[i])+sum((q for j,x,q in keep),F())==v
        clipped+=bool(p and refund)
        rows[h]=(i,v,edges,keep,aa,n)
    # Arbitrary unit profit injections exercise the identities, not OPT budgets.
    seed={h:F(1) for h in histories if rows[h][1]}
    answer={};results={}
    for mode in ['gross','net','clip']:
        mass=defaultdict(F,seed);out=defaultdict(F);betas={}
        for h in histories:
            if not mass[h]:continue
            i,v,edges,kept,aa,n=rows[h]
            assert v>0 and u[i]>0
            beta=mass[h]/v;betas[h]=beta
            if mode=='clip':
                current=beta*min(v,u[i]);used=kept
            elif mode=='net':
                current=beta*(u[i]-n-(u[i]-pay(aa,i)));used=edges
            else:current=beta*u[i];used=edges
            for x in topics[z[i]]:
                out[i,x]+=current/u[i]*F(1,loads(z)[x])
            for j,x,q in used:
                if j<i:
                    assert x in topics[z[j]];out[j,x]+=beta*q
                else:
                    dest=aa[:j]
                    assert len(dest)>len(h) and finish(dest)==aa
                    mass[dest]+=beta*q
        results[mode]=(betas,out)
        answer[mode]=str(sum(out.values(),F()))
    total=sum(seed.values(),F())
    assert sum(results['net'][1].values(),F())==total
    assert sum(results['clip'][1].values(),F())==total
    for h,beta in results['clip'][0].items():assert beta<=results['gross'][0][h]
    for coupon,value in results['clip'][1].items():assert value<=results['gross'][1][coupon]
    raised=sum(results['clip'][1][c]>results['net'][1][c] for c in results['clip'][1])
    return dict(name=name,histories=len(histories),complete_ic_checks=ic,
                contexts_with_nonzero_scalar_cancellation=clipped,
                arbitrary_profit_source=str(total),terminal_totals=answer,
                coupons_above_old_net=raised,
                warning='arbitrary injection is not OPT initialization; no cap claim')


if __name__=='__main__':
    names=['portfolio_matching_failure','root_tax_failure','individual_security_failure',
           'eight_cce_welfare_gap','coverage_opportunity_failure','prefix_balance_failure']
    result=[run(name) for name in names]
    print(json.dumps(dict(status='PASS',arithmetic='Fraction',scope='old full-SPE definition regression only',cases=result),indent=2))
