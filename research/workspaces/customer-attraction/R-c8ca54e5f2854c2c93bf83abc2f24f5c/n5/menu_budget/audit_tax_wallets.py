"""Fraction checks of reset/OPT-private-block tax wallets; no HALF5 claim."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

cases=0;exception_equalities=0
for b in range(3):
    for t,r,s,c,d,e,l in product(range(2),repeat=7):
        tax=F(4,5)*F(r*(1-s),(b+t+1)*(b+t+2))
        reset=F(r,b+c+1+l)
        exceptional=int(b==0 and c==1 and t==0 and l==1 and r==1 and s==0)
        assert tax<=reset+F(exceptional,15)
        actual_share=F(c,max(b+c+d+e,1))
        assert tax<=reset+actual_share/5
        if exceptional and tax-reset==F(1,15):exception_equalities+=1
        cases+=1
private=[]
for b in range(3):
    val=F(1,b+2)+F(3,8)*F(b,b+3)
    assert val>=F(2,5)
    private.append(dict(b=b,query_floor=str(F(1,b+2)),past_share_floor=str(F(b,b+3)),total=str(val)))

# Six genuine disjoint unit-client themes, complete exact five-player SPE.
k=6;n=5
@lru_cache(None)
def utility(a,z):return F(1,z.count(a))
@lru_cache(None)
def finish(h):
    if len(h)==n:return h
    a=max((utility(a,finish(h+(a,))),a)for a in range(k))[1]
    return finish(h+(a,))
z=finish(());C,D,E=z[2:]
T=tuple(a for a in range(k)if a!=D);O=set(T)
opt=max(len(set(v))for v in combinations_with_replacement(range(k),n))
assert len(O)==opt==5
ic=[]
for depth in range(n):
    for h in product(range(k),repeat=depth):
        out=finish(h);a=out[depth]
        ic.extend(utility(a,out)-utility(t,finish(h+(t,)))for t in range(k))
assert min(ic)>=0
R=[];S=[];L=[]
tax=reset=private_d=matched_past=F(0)
static_rows=[]
for a in T:
    leaf=finish(z[:2]+(a,));r,s=leaf[-2:];l=finish(z[:3]+(r,))[-1]
    R.append(r);S.append(s);L.append(l)
    b=z[:2].count(r)
    tau=F(int(r!=s),(b+int(r==a)+1)*(b+int(r==a)+2))
    tax+=F(4,25)*tau
    reset+=F(1,5)*utility(r,z[:3]+(r,l))
    private_set={a}-{r}
    outside={r}-O
    assert len(outside)<=len(private_set)
    static_rows.append(dict(query=a,follower=r,private=list(private_set),outside=list(outside)))
    private_d+=F(1,5)*sum((F(1,z[:2].count(x)+1+int(s==x))for x in private_set),F(0))
    matched_past+=F(3,40)*sum((F(z[:2].count(x),max(z.count(x),1))for x in private_set),F(0))
outside_tax=F(0)
for a,r,s in zip(T,R,S):
    if r not in O:
        b=z[:2].count(r)
        outside_tax+=F(4,25)*F(int(r!=s),(b+1)*(b+2))
past=sum((utility(z[i],z)for i in range(2)),F(0))
assert outside_tax<=private_d+matched_past<=private_d+F(3,40)*past
u3=utility(C,z);u4=utility(D,z)
assert tax<=reset+u3/5<=u4+u3/5
out=dict(status='passed',pointwise_reset_cases=cases,exception_equalities=exception_equalities,private_client_budget=private,fixture=dict(actual=z,comparators=T,OPT5=opt,ordered_ic_rows=len(ic),minimum_ic=str(min(ic)),R=R,S=S,L=L,weighted_total_tax=str(tax),mean_reset_query_payoff=str(reset),reset_wallet_bound=str(u4+u3/5),weighted_outside_OPT_tax=str(outside_tax),private_query_profit=str(private_d),matched_past_credit=str(matched_past),past_credit_bound=str(F(3,40)*past),outside_wallet_bound=str(private_d+F(3,40)*past),replacement_rows=static_rows),scope='Exact wallet identities/inequalities only; no combined M3+M4 payment or HALF5.')
Path(__file__).with_name('tax_wallets_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
