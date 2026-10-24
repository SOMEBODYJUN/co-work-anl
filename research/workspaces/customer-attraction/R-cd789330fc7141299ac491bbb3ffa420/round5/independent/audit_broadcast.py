"""Definition-level audit for the reviewed broadcast identities.

The general proof is in review_broadcast.md. This independent unit-customer
example deliberately has nonzero fresh propagation and a terminal past-C
coupon. It is neither a search nor evidence for a universal welfare bound.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


LABELS = ('H','A','B','T','D','E')
H,A,B,T,D,E = range(6)
members = {}
def block(name, size, topics):
    for k in range(size):
        members[f'{name}{k}'] = frozenset(topics)
block('H',8,[H])
block('B',3,[B])
block('T',3,[T])
block('AD',2,[A,D])
block('AE',2,[A,E])
block('BDE',2,[B,D,E])
block('TDE',2,[T,D,E])
topics = tuple(frozenset(x for x,s in members.items() if a in s) for a in range(6))


def payoff(z, i):
    return sum((F(1,sum(x in topics[a] for a in z)) for x in topics[z[i]]),F())


last = {}
legacy = {A:B,B:D,T:D,D:E,E:D}
for a,b in product(range(6),repeat=2):
    values = [payoff((a,b,c),2) for c in range(6)]
    choices = [c for c,v in enumerate(values) if v==max(values)]
    chosen = legacy[b] if a==H and b!=H else min(choices)
    assert chosen in choices
    last[a,b] = chosen

second = {}
for a in range(6):
    values = [payoff((a,b,last[a,b]),1) for b in range(6)]
    choices = [b for b,v in enumerate(values) if v==max(values)]
    chosen = A if a==H else T if a==D else min(choices)
    assert chosen in choices
    second[a] = chosen

strategy = {():H}
strategy.update({(a,):b for a,b in second.items()})
strategy.update(last)
def finish(g):
    z=tuple(g)
    while len(z)<3:
        z += (strategy[z],)
    return z
Z=finish(())
C=set().union(*(topics[a] for a in Z))
actual = tuple(payoff(Z,i) for i in range(3))
ic_checks=0
for g,a in strategy.items():
    own=payoff(finish(g),len(g))
    for d in range(6):
        assert own>=payoff(finish(g+(d,)),len(g))
        ic_checks+=1


def row(g, fresh=False):
    i=len(g)
    a=strategy[g]
    zb=finish(g)
    za=finish(Z[:i]+(a,))
    out={}
    past={}
    negative=F()
    retained=F()
    signed_difference=F()
    full_v=payoff(zb,i)
    full_d=payoff(za,i)
    for x in topics[a]:
        if fresh and x in C:
            continue
        ja={j for j in range(3) if j!=i and x in topics[za[j]]}
        jb={j for j in range(3) if j!=i and x in topics[zb[j]]}
        ca,cb=1+len(ja),1+len(jb)
        price=F(1,ca*cb)
        plus=ja-jb
        minus=jb-ja
        assert F(1,cb)-len(plus)*price==(1+len(ja&jb))*price
        assert F(1,ca)-len(minus)*price==(1+len(ja&jb))*price
        signed_difference+=F(1,cb)-F(1,ca)
        retained+=(1+len(ja&jb))*price
        negative+=len(minus)*price
        for j in plus:
            if j>i:
                target=za[:j]
                assert strategy[target]==za[j]
                assert finish(target)==za
                assert payoff(za,j)>0
                out[target]=out.get(target,F())+price
            else:
                assert x in topics[Z[j]]
                past[j,x]=past.get((j,x),F())+price
    positive=sum(out.values(),F())+sum(past.values(),F())
    assert signed_difference==positive-negative
    if not fresh:
        assert full_v-positive==retained==full_d-negative
    else:
        xcovered=sum((F(1,sum(x in topics[a] for a in zb))
                      for x in topics[a] if x in C),F())
        assert not past
        assert full_v-positive==xcovered+retained
    if full_v:
        future_roles=tuple(range(i+1,3))
        for k in range(1<<len(future_roles)):
            selected={future_roles[j] for j in range(len(future_roles)) if k>>j&1}
            amount=sum((w for h,w in out.items() if len(h) in selected),F())
            assert amount/full_v<=F(len(selected),len(selected)+1)
    assert actual[i]-full_d>=0
    return {'i':i,'v':full_v,'d':full_d,'out':out,'past':past,
            'n':negative,'retained':retained,'e':actual[i]-full_d,
            'A':za,'B':zb}


rows_all={g:row(g) for g in strategy}
rows_fresh={g:row(g,True) for g in strategy}

# A single legal forced OPT/source query at position one: query D, and retain
# only its two actual-uncovered TDE customers, rho=1 for each.
source_query=D
source_leaf=finish((D,))
source_customers=topics[D]-C
assert source_customers=={'TDE0','TDE1'}
source_absorption=sum((F(1,sum(x in topics[a] for a in source_leaf))
                       for x in source_customers),F())
injection={}
for j in range(1,3):
    amount=sum((F(1,sum(x in topics[a] for a in source_leaf))
                for x in source_customers if x in topics[source_leaf[j]]),F())
    if amount:
        g=source_leaf[:j]
        assert finish(g)==source_leaf
        injection[g]=injection.get(g,F())+amount
assert source_absorption+sum(injection.values(),F())==len(source_customers)


def flow(rows):
    h=dict(injection)
    beta={}
    for g in sorted(rows,key=lambda h:(len(h),h)):
        r=rows[g]
        amount=h.get(g,F())
        if not amount:
            beta[g]=F()
            continue
        assert r['v']>0
        beta[g]=amount/r['v']
        for target,q in r['out'].items():
            assert len(target)>len(g)
            h[target]=h.get(target,F())+beta[g]*q
    input_mass=sum(injection.values(),F())
    mass=sum((beta[g]*(r['v']-sum(r['out'].values(),F()))
              for g,r in rows.items()),F())
    assert input_mass==mass
    return beta,mass


beta_all,mass_all=flow(rows_all)
beta_fresh,mass_fresh=flow(rows_fresh)
coupon={}
for j in range(3):
    for x in topics[Z[j]]:
        cz=sum(x in topics[a] for a in Z)
        coefficient=sum((beta_all[g] for g in rows_all if len(g)==j),F())
        coefficient+=cz*sum((beta_all[g]*r['past'].get((j,x),F())
                             for g,r in rows_all.items() if len(g)>j),F())
        coupon[j,x]=coefficient
positive_coupons=sum((v/F(sum(x in topics[a] for a in Z))
                      for (j,x),v in coupon.items()),F())
refund=sum((beta_all[g]*(r['n']+r['e']) for g,r in rows_all.items()),F())
assert positive_coupons-refund==mass_all
assert beta_all[(D,)]==F(1,4)
assert rows_fresh[(D,)]['out'][(H,T)]==F(1,2)
assert beta_all[(H,T)]==F(1,40)
assert sum(rows_all[(H,T)]['past'].values(),F())==1

result={
    'scope':'One complete unit-customer SPE implementation audit; no universal computational evidence.',
    'customers':len(members),'topics':list(LABELS),'players':3,
    'actual_path':[LABELS[a] for a in Z],'actual_payoffs':list(map(str,actual)),
    'complete_histories':len(strategy),'ic_checks_including_self':ic_checks,
    'source_leaf':[LABELS[a] for a in source_leaf],
    'source_rho_total':len(source_customers),'source_absorption':str(source_absorption),
    'injected_mass':str(sum(injection.values(),F())),
    'positive_fresh_edge':{'from':['D'],'to':['H','T'],'raw_price':'1/2',
                           'beta_from':str(beta_all[(D,)]),'transmitted_profit':'1/8'},
    'terminal_past_coupon_raw':str(sum(rows_all[(H,T)]['past'].values(),F())),
    'all_flow_mass':str(mass_all),'fresh_flow_mass':str(mass_fresh),
    'positive_coupon_profit':str(positive_coupons),'signed_refunds':str(refund),
    'status':'passed'
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
