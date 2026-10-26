"""Independent literal SPE-query check of same-menu projected rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import random,json
from same_menu_reply import from_weights,TYPES,load_old,decode
HERE=Path(__file__).resolve().parent

def exact_cut_pair(a,d,L=6):
    """Independent closed form for the five-weight old-closure separator."""
    b=sum(a[:-2]);ell=sum(a[:-1]);anchor=a[1];p=F(d,L)
    alpha,beta,gamma,delta=F(13,288),F(11,288),F(11,12),F(1)
    cr=delta*((1-p)/F(b+1)+p/F(b+2))-gamma/F(b+anchor+1)
    psi=min(F(0),cr)
    for t,prob in ((0,1-p),(1,p)):
        v0=F(t,b+t) if t else F(0)
        v1=F(t,b+t+1)+beta+alpha/F(ell+1)+gamma/F(b+anchor+1)-delta/F(b+t+1)
        psi+=prob*min(v0,v1)
    s=sum(a)
    u5=F(a[4],s) if a[4] else F(0)
    u6=F(a[5],s) if a[5] else F(0)
    return u5+alpha*u6-psi

def game_checks(weights,seed):
    rnd=random.Random(seed);N=7;M=6
    menu=[set()]
    while len(menu)<4:
        S={x for x in range(N) if rnd.randrange(2)}
        if S not in menu:menu.append(S)
    def payoff(player,profile):
        S=menu[profile[player]]
        return sum(F(1,sum(x in menu[q] for q in profile)) for x in S)
    outcomes={}
    def solve(h):
        if len(h)==M:return h
        children=[solve(h+(q,)) for q in range(len(menu))]
        vals=[payoff(len(h),s) for s in children];mx=max(vals)
        choices=[q for q,v in enumerate(vals) if v==mx]
        # This explicitly permits history-dependent tie selection.
        chosen=choices[(sum((i+1)*q for i,q in enumerate(h))+seed)%len(choices)]
        outcomes[h]=children[chosen]
        return children[chosen]
    actual=solve(());h=actual[:4]
    # Arbitrary comparator indices, deliberately with repetitions and empty sets.
    opt=[rnd.randrange(len(menu)) for _ in range(M)]
    forces=list(actual)+[None]
    replies={j:[outcomes[h+(forces[j],)][-1]] for j in range(M)}
    replies[M]=[outcomes[h+(q,)][-1] for q in opt]
    def forced(j):return [forces[j]] if j<M else opt
    def avg(vals):return sum(vals,F(0))/len(vals)
    def U(q,f):
        return sum(F(1,sum(x in menu[z] for z in h)+int(x in menu[f])+1) for x in menu[q])
    def leader(q,R):
        return sum(F(1,sum(x in menu[z] for z in h)+1+int(x in menu[R])) for x in menu[q])
    def own(j):return avg([U(R,f) for R,f in zip(replies[j],forced(j))])
    r=payoff(4,actual);u6=payoff(5,actual);K=max(map(len,menu))
    ell=[sum(x in menu[z] for z in actual[:-1]) for x in range(N)]
    def primitive(spec):
        kind,j,*rest=spec
        if kind=='leader':return r-avg([leader(f,R) for R,f in zip(replies[j],forced(j))])
        if kind=='price':return u6-avg([sum(F(1,ell[x]+1) for x in menu[R]) for R in replies[j]])
        if kind=='cap':return F(K)-avg([F(len(menu[R])) for R in replies[j]])
        if kind=='queryA':return own(j)-avg([U(actual[rest[0]],f) for f in forced(j)])
        if kind=='queryO':return own(j)-avg([U(q,forces[j]) for q in opt])
        if kind=='queryOwn':return own(j)-avg([U(q,q) for q in opt])
        if kind=='queryOther':return own(j)-sum(U(q,f) for i,f in enumerate(opt) for k,q in enumerate(opt) if i!=k)/F(M*(M-1))
        q=rest[0]
        return own(j)-avg([U(R,f) for R in replies[q] for f in forced(j)])
    weighted=F(0)
    for w in weights:
        v=primitive(w['spec']);assert v>=0,(seed,w,v)
        weighted+=F(w['weight'])*v
    n={}
    for x in range(N):
        a=tuple(int(x in menu[q]) for q in actual)
        d=sum(x in menu[q] for q in opt)
        n[a,d]=n.get((a,d),0)+1
    row=from_weights(weights)
    value=sum(row[i]*n.get(t,0) for i,t in enumerate(TYPES))+row[-1]*K
    # The difference is precisely the nonnegative independent membership minimum slack.
    assert value>=weighted>=0,(seed,value,weighted)
    return len(outcomes),value,weighted

if __name__=='__main__':
    base=json.loads((HERE/'same_menu_reply.json').read_text())
    weights=base['old_387_closed'][1]['weights']
    row=from_weights(weights)
    for i,(a,d) in enumerate(TYPES):assert row[i]==exact_cut_pair(a,d)
    assert row[-1]==F(11,288)
    old=load_old();slacks={name:str(sum(v*x for v,x in zip(row,decode(rec,TYPES)))) for name,rec in old.items()}
    packages=[weights]+[v['weights'] for v in base['nested_587']]+[v['weights'] for v in json.loads((HERE/'iterate_same_menu.json').read_text())['cuts']]
    checks=0;nodes=0
    for seed in range(12):
        for weights in packages:
            ns,_,_=game_checks(weights,seed);checks+=1;nodes+=ns
    report={'all_448_type_coefficients_match_independent_pair_closed_form':True,'old_closed_pair_slacks':slacks,'complete_history_SPE_checks':checks,'true_nodes_checked':nodes,'scope':'implementation checks of general nonnegative-identity proof; not a half proof'}
    (HERE/'verify_same_menu.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
