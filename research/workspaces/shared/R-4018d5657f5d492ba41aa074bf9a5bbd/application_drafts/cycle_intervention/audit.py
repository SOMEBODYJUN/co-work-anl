"""Finite rational checks, not a general proof."""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path


def ordered(a,b,d,m,n,kind):
    if kind=='D':
        return a*sum((j*a)**d for j in range(1,m+1))+b*sum((m*a+k*b)**d for k in range(1,n+1))
    return b*sum((k*b)**d for k in range(1,n+1))+a*sum((n*b+j*a)**d for j in range(1,m+1))


def local(a,b,na,nb,d,beta):
    A=min(F(ordered(a,b,d,m+1,n,'D')-ordered(a,b,d,m,n,'D'),a*((m+1)*a+n*b)**d)
          for m in range(na) for n in range(nb+1))
    B=max(F(ordered(a,b,d,m,n+1,'U')-ordered(a,b,d,m,n,'U'),b*(m*a+(n+1)*b)**d)
          for m in range(na+1) for n in range(nb))
    lm=max(F(0),(1/beta-A)/(1-A)) if A<1 else F(0)
    lp=min(F(1),(beta-1)/(B-1)) if B>1 else F(1)
    if lm>lp:
        return A,B,None,None
    la=lm if A*B>=1 else lp
    ss=1/(A+(1-A)*la)
    x,y=ss*(1-la),ss*la
    ell=(x+B*y)/beta
    assert A*x+y>=1 and x+y<=beta and ell<=x+y and x+B*y<=beta*ell
    return A,B,ell,(x,y)


def feasible(n,resources,deleted):
    # Multiplicative Bellman-Ford, all-source distance 1.
    ds=[F(1)]*n
    arcs=[]
    for name,a,b,ell,be,q in resources:
        if name not in deleted:
            arcs.extend([(a,b,be),(b,a,1/ell)])
    for k in range(n):
        changed=False
        old=ds[:]
        for a,b,mult in arcs:
            if old[a]*mult<ds[b]:
                ds[b]=old[a]*mult
                changed=True
        if not changed:
            return True,ds
    return False,None


def conflict_audit():
    be=F(179,100)
    records=[]
    res=[]
    for name,ia,ib,a,b,q in [('ab',0,1,100,10,3),('bc',1,2,10,1,5),('ac0',0,2,100,1,1),('ac1',0,2,100,1,1)]:
        A,B,ell,xy=local(a,b,4,20,5,be)
        assert ell is not None
        res.append((name,ia,ib,ell,be,q))
        records.append(dict(name=name,A=str(A),B=str(B),lower=str(ell),upper=str(be),mix=list(map(str,xy)),cost=q))
    assert not feasible(3,res,set())[0]
    assert not feasible(3,res,{'ac0'})[0]
    assert not feasible(3,res,{'ac1'})[0]
    best=None
    for k in range(5):
        for sub in combinations([r[0] for r in res],k):
            if feasible(3,res,set(sub))[0]:
                cost=sum(r[-1] for r in res if r[0] in sub)
                if best is None or cost<best[0]:best=(cost,list(sub))
    assert best==(2,['ac0','ac1'])
    assert res[0][3]*res[1][3]>be
    return dict(resources=records,chain_product=str(res[0][3]*res[1][3]),shortcut_upper=str(be),minimum_cost=best[0],optimal_deleted=best[1],single_parallel_delete_fails=True)


def small_game_audit():
    be=F(6,5)
    weights=[3,2,1]
    menus=[({'ab'},{'ac'}),({'ab'},{'bc'}),({'bc'},{'ac'})]
    Aab,Bab,lab,mab=local(3,2,1,1,2,be)
    Abc,Bbc,lbc,mbc=local(2,1,1,1,2,be)
    assert lab is not None and lbc is not None
    ts=[F(1),lab,lab*lbc]
    p=F(16)+be
    p/=be+1
    assert p==F(86,11)
    def load(state,e):return sum(weights[i] for i in range(3) if e in menus[i][state[i]])
    def cost(state,i,modified):
        return sum((p if e=='ac' and modified else load(state,e)**2) for e in menus[i][state[i]])
    def phi(state):
        val=F(0)
        for e,hi,lo,mix in [('ab',0,1,mab),('bc',1,2,mbc)]:
            m=int(e in menus[hi][state[hi]])
            n=int(e in menus[lo][state[lo]])
            a,b=weights[hi],weights[lo]
            val+=ts[hi]*(mix[0]*ordered(a,b,2,m,n,'D')+mix[1]*ordered(a,b,2,m,n,'U'))
        val+=p*sum(weights[i]*ts[i] for i in (0,2) if 'ac' in menus[i][state[i]])
        return val
    localmins=[]
    allstates=list(product(range(2),repeat=3))
    for state in allstates:
        if any(phi(state[:i]+(1-state[i],)+state[i+1:])<phi(state) for i in range(3)):continue
        localmins.append(state)
        for i in range(3):
            nxt=state[:i]+(1-state[i],)+state[i+1:]
            A,T=menus[i][state[i]],menus[i][1-state[i]]
            leave=sum((p if e=='ac' else load(state,e)**2) for e in A-T)
            join=sum((p if e=='ac' else load(nxt,e)**2) for e in T-A)
            assert leave<=be*join
            radius=F(0)
            if 'ac' in A-T:radius+=16-p
            if 'ac' in T-A:radius+=be*(p-1)
            assert cost(state,i,False)-be*cost(nxt,i,False)<=radius
    assert localmins
    return dict(beta=str(be),scales=list(map(str,ts)),fixed_fee=str(p),single_resource_radius=str(be*(16-1)/(be+1)),number_states=len(allstates),local_minima=[list(s) for s in localmins],all_strengthened_and_original_bounds_pass=True)


def common_resource_counterexample():
    # Literal costs: player 1 always uses r; player 2 currently empty.
    be=F(2);m=F(1);M=F(4);p=(M+be*m)/(be+1)
    old=F(1)+4;new=F(1)+1
    oldmod=p+4;newmod=p+1
    assert p==2 and oldmod<=be*newmod and old>be*new
    assert old-be*new==(be-1)*(p-m)==1
    assert 4>be*1
    return dict(beta=str(be),range=[str(m),str(M)],optimal_fixed_fee=str(p),modified_costs=[str(oldmod),str(newmod)],original_costs=[str(old),str(new)],original_residual=str(old-be*new),D_symmetric_difference=[],shared_error=str((be-1)*(p-m)),fails_strengthened_condition=True)


if __name__=='__main__':
    out={'scope':'finite exact rational checks; not a general proof', 'parallel_conflict':conflict_audit(),'small_game':small_game_audit(),'common_resource_counterexample':common_resource_counterexample()}
    dest=Path(__file__).with_name('audit.json')
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'saved':str(dest),'optimal_conflict_deletion':out['parallel_conflict']['optimal_deleted'],'small_game_states':out['small_game']['number_states'],'small_game_local_minima':out['small_game']['local_minima'],'shared_counterexample_residual':out['common_resource_counterexample']['original_residual']},ensure_ascii=False))
