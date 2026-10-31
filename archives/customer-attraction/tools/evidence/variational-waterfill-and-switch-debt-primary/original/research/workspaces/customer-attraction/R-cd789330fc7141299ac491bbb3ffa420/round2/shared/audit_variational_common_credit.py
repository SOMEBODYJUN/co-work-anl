"""Exact rational KKT certificates for the variational common-credit state.
No numerical optimizer, author imports, SPE solver or weighted-player game.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from functools import lru_cache
import json


@lru_cache(None)
def log_bounds(q):
    assert q>=1
    z=(q-1)/(q+1)
    power=z
    total=F(0)
    terms=80
    for k in range(terms):
        total+=2*power/(2*k+1)
        power*=z*z
    remainder=2*power/((2*terms+1)*(1-z*z))
    return total,total+remainder


def certificate(name,N,b,A,tails,t,w):
    N=tuple(N);A=frozenset(A);tails=tuple(frozenset(T) for T in tails)
    t=F(t);w=tuple(F(v) for v in w);one=(F(1),)*len(tails)
    b={x:F(b.get(x,0)) for x in N}
    assert t>0 and len(w)==len(tails) and all(0<=v<=1 for v in w)
    def c(x,v):return sum((v[j] for j,T in enumerate(tails) if x in T),F(0))
    def L(x,v):return b[x]+int(x in A)+c(x,v)
    K=[x for x in N if L(x,one)>0]
    assert all(L(x,w)>0 for x in K)
    def U(j,v):return sum((1/L(x,v) for x in tails[j]),F(0))
    u=[U(j,one) for j in range(len(tails))]
    end=[U(j,w) for j in range(len(tails))]
    for j,v in enumerate(w):
        if v==0:assert end[j]<=t
        elif v==1:assert end[j]>=t
        else:assert end[j]==t
        if u[j]>=t:assert v==1
    J=[j for j,v in enumerate(w) if v<1]
    D=sum((max(F(0),t-v) for v in u),F(0))
    delta=sum((end[j]-u[j] for j in J),F(0))
    def Q(T,v):return sum((1/(b[x]+1+c(x,v)) for x in T),F(0))
    H=Q(N,w)-Q(N,one)
    assert 0<=H<=delta<=D
    if len(N)<=6:
        queries=[T for sz in range(len(N)+1) for T in combinations(N,sz)]
    else:
        queries=[(),N,A,*tails,*( (x,) for x in N)]
    for T in queries:assert 0<=Q(T,w)-Q(T,one)<=H
    M=sum(w,F(0));loss=F(len(w))-M
    stretch=sum((L(x,one)/L(x,w)-1 for x in K),F(0))
    assert stretch==sum(((1-w[j])*end[j] for j in range(len(w))),F(0))
    assert stretch<=t*loss
    for x in K:assert L(x,w)>=L(x,one)/(1+t*loss)
    def R(v):return sum((1/L(x,v) for x in A),F(0))
    def B(v):return sum((b[x]/L(x,v) for x in N if b[x]),F(0))
    def V(v):return sum((c(x,v)/L(x,v) for x in N if c(x,v)),F(0))
    gamma=R(w)-R(one);db=B(w)-B(one)
    assert V(w)==sum((w[j]*end[j] for j in range(len(w))),F(0))
    assert gamma+db+V(w)==V(one)
    assert gamma+db+t*M<=V(one)
    log_lo=sum((log_bounds(L(x,one)/L(x,w))[0] for x in K),F(0))
    log_hi=sum((log_bounds(L(x,one)/L(x,w))[1] for x in K),F(0))
    free_lo=t*loss-log_hi
    free_hi=t*loss-log_lo
    assert 0<=free_lo<=free_hi<=D
    assert max(H,gamma+db)<=log_lo
    assert max(H,gamma+db)+free_hi+t*M<=t*len(w)
    if V(one)>=t*len(w):
        assert max(H,gamma+db)+free_hi+t*M<=V(one)
    return {'name':name,'unit_customers':len(N),'t':str(t),'w':list(map(str,w)),
            'u_initial':list(map(str,u)),'u_final':list(map(str,end)),
            'D':str(D),'sum_reduced_unit_increase':str(delta),'H':str(H),
            'mass':str(M),'mass_loss':str(loss),'stretch':str(stretch),
            't_mass_loss':str(t*loss),'free_energy_lower':str(free_lo),'free_energy_upper':str(free_hi),'root_gain':str(gamma),'background_gain':str(db),
            'query_count':len(queries)}

out=[]
out.append(certificate('private_positive_stop',['x'],{},[],[['x']],2,[F(1,2)]))
out.append(certificate('root_shared_zero',['x'],{},['x'],[['x']],1,[0]))
out.append(certificate('mixed_shared_private',['x','y'],{},['x'],[['x','y']],F(8,3),[F(1,2)]))
out.append(certificate('initial_equal_high_preserved',['x'],{},[],[['x']],1,[1]))
out.append(certificate('empty_tail',[],{},[],[[]],1,[0]))
out.append(certificate('aggregate_high_low_joint',['x','y'],{},['x'],[['x'],['x','y']],F(1,2),[0,1]))
out.append(certificate('no_tails',['x'],{},['x'],[],2,[]))
for w in ([F(1,2),F(1,2)],[1,0],[0,1]):
    out.append(certificate('duplicate_decomposition_'+str(w),['x'],{},['x'],[['x'],['x']],F(1,2),w))
for k in [1,7,100]:
    out.append(certificate('background_zero_'+str(k),['x','z'],{'x':k},['z'],[['x']],F(1,k),[0]))

Y=['y'+str(i) for i in range(205)]
N=['x','z','u',*Y]
b={'x':1,'z':1,'u':99,**{y:401 for y in Y}}
state=certificate('nonmonotone_root_credit',N,b,['u'],[['x','z','u'],['z',*Y],['x',*Y]],F(203,201),[F(1,2)]*3)
out.append(state)
dx=F(1,4);dy=F(205,402**2);du=F(4,201**2)
det=(2*dx+du)*(dx+2*dy)-2*dx*dx
alpha_prime=(dx-2*dy)/det
beta_prime=-(dx+du)/det
root_prime=-du*alpha_prime
mass_prime=alpha_prime+2*beta_prime
assert det>0 and alpha_prime>0 and beta_prime<0 and mass_prime<0
assert root_prime==F(-159964,8445449)<0
result={'status':'pass','scope':'exact finite KKT and algebra certificates; universal assertions use analytic proof',
        'cases':out,'nonmonotone_derivatives':{'determinant':str(det),'w1_prime':str(alpha_prime),
        'w2_prime':str(beta_prime),'root_credit_prime':str(root_prime),'mass_prime':str(mass_prime)}}
Path(__file__).with_name('variational_common_credit_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','KKT_certificates':len(out),'nonmonotone_root_derivative':str(root_prime),
                  'mass_derivative':str(mass_prime),'largest_unit_instance':len(N)}))
