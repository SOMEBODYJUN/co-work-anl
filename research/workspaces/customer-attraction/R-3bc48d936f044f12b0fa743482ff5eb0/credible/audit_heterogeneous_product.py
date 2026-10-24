"""A full unit-customer regression for two unequal credible deficits.

Original m3 target AAB, |A|=1,|B|=4; all customers scaled6.
delta=(5,9), layer sets {1,2} at scale5 and {2} at scale4.
No repository model or solver imports. This is not a target attack witness.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

m,j=3,2
oldsize=(Q(6),Q(24))
layers=(((0,1),Q(5)),((1,),Q(4)))
oldnormal=(0,0,1)

def inc(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
def counts(h,p):return tuple(h.count(a) for a in range(p))
def pay(size,c,a):return size[a]/c[a] if c[a] else Q(0)

@lru_cache(None)
def oldout(c):
    if sum(c)==m:return frozenset((c,))
    children=[oldout(inc(c,a)) for a in range(2)]
    floor=max(min(pay(oldsize,t,a) for t in ch) for a,ch in enumerate(children))
    return frozenset(t for a,ch in enumerate(children) for t in ch if pay(oldsize,t,a)>=floor)

def oldrho(i,A):
    h=oldnormal[:i]+(A,)
    target=min(oldout(counts(h,2)),key=lambda t:(pay(oldsize,t,A),t))
    acts={}
    def expand(h,t):
        if len(h)==m:return
        c=counts(h,2)
        children=[oldout(inc(c,a)) for a in range(2)]
        threshold=max(min(pay(oldsize,z,a) for z in ch) for a,ch in enumerate(children))
        a=next(a for a,ch in enumerate(children) if t in ch and pay(oldsize,t,a)>=threshold)
        acts[h]=a
        for b,ch in enumerate(children):
            other=t if b==a else min(ch,key=lambda z:(pay(oldsize,z,b),z))
            expand(h+(b,),other)
    expand(h,target)
    return acts,pay(oldsize,target,A)

def bankdata(marks,s):
    k=len(marks);d=m-k
    size=(2*s,)*k+(d*s,)+(s,)*(d-1)
    marked={i:a for a,i in enumerate(marks)}
    normal=tuple(marked.get(i,k) for i in range(m))
    @lru_cache(None)
    def bi(c):
        if sum(c)==m:return c
        return bi(inc(c,bia(c)))
    @lru_cache(None)
    def bia(c):
        return max(range(m),key=lambda a:(pay(size,bi(inc(c,a)),a),-a))
    def low(i,T):
        prefix=normal[:i];prior=counts(prefix,m)
        mode='BI' if T>k or (T<k and prior[T]) else 'Y' if T==k else 'F'
        acts={}
        def expand(h,permanent=False):
            if len(h)==m:return
            c=counts(h,m)
            if permanent or mode=='BI':a=bia(c)
            else:
                empty=[a for a in range(k) if not c[a]]
                a=empty[0] if empty else k if mode=='Y' or c[k]<d-1 else T
            acts[h]=a
            for b in range(m):
                nxt=h+(b,);cc=counts(nxt,m)
                bad=permanent or mode=='BI' or any(v>1 for v in cc[:k]) or any(cc[k+1:]) or cc[k]>(d if mode=='Y' else d-1)
                expand(nxt,bad)
        expand(prefix+(T,))
        return acts
    return size,normal,low

oldr={};floor={}
for i in range(j):
    for A in range(2):oldr[i,A],floor[i,A]=oldrho(i,A)
ou=tuple(pay(oldsize,counts(oldnormal,2),a) for a in oldnormal)
delta=tuple(max(Q(0),max(floor[i,A] for A in range(2))-ou[i]) for i in range(j))
assert delta==(Q(5),Q(9))
banks=[bankdata(*layer) for layer in layers]
bankr=[{(i,T):low(i,T) for i in range(j) for T in range(m)} for size,normal,low in banks]
normal=tuple((oldnormal[i],)+(tuple(bank[1][i] for bank in banks)) for i in range(m))
joint=list(product(range(2),range(m),range(m)))
actions={}
for length in range(m):
    for h in product(joint,repeat=length):
        first=next((i for i in range(min(j,length)) if h[i]!=normal[i]),None)
        if first is None:
            a=normal[length]
        else:
            original=oldr[first,h[first][0]][tuple(a[0] for a in h)]
            insurance=tuple(bankr[l][first,h[first][l+1]][tuple(a[l+1] for a in h)] for l in range(len(layers)))
            a=(original,)+insurance
        actions[h]=a

# Every mass is now represented by distinct unit customers.
blocksets=[];nxt=0
for sizes in (oldsize,)+(tuple(bank[0] for bank in banks)):
    component=[]
    for size in sizes:
        assert size.denominator==1
        component.append(set(range(nxt,nxt+int(size))))
        nxt+=int(size)
    blocksets.append(component)
cover={a:set().union(*(blocksets[l][a[l]] for l in range(len(a)))) for a in joint}
assert nxt==75
def terminal(h):
    while len(h)<m:h=h+(actions[h],)
    return h
def utilities(z):
    load={x:sum(x in cover[a] for a in z) for x in range(nxt)}
    return tuple(sum((Q(1,load[x]) for x in cover[a]),Q(0)) for a in z)
checks=0;minmargin=None
for h,a in actions.items():
    base=utilities(terminal(h))[len(h)]
    for b in joint:
        margin=base-utilities(terminal(h+(b,)))[len(h)]
        assert margin>=0,(h,a,b,margin)
        checks+=1;minmargin=margin if minmargin is None else min(minmargin,margin)
z=terminal(());u=utilities(z)
W=len(set().union(*(cover[a] for a in z)))
O=max(len(set().union(*(cover[a] for a in zz))) for zz in product(joint,repeat=m))
assert u==(Q(17),Q(21),Q(33)) and W==71 and O==75
D=max(delta);R=sum(delta)
assert O-2*W==30-2*30-(2*R+D)==-67
report={'m':m,'old_original':'disjoint A size1,B size4,target AAB; every customer scaled6','original_target_payoffs':[str(x) for x in ou],'credible_deficits':[str(x) for x in delta],'D':str(D),'R':str(R),'heterogeneous_half_gap_loss':str(2*R+D),'old_uniform_half_gap_loss':str((2*j+1)*D),'layer_marked_positions_zero_based':[list(I) for I,s in layers],'layer_scales':[str(s) for I,s in layers],'customers':nxt,'topics':len(joint),'full_ordered_decision_histories':len(actions),'all_joint_action_IC_comparisons':checks,'minimum_IC_margin':str(minmargin),'actual_joint_path':z,'actual_payoffs':[str(x) for x in u],'W_new':W,'OPT_new':O,'half_gap':O-2*W,'target_counterexample':False,'actions':[{'history':h,'action':a} for h,a in actions.items()]}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='actions'}))
