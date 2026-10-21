"""Self-contained exact eight-unit-customer counterexample to W >= Z_3.

Z_3 is the coverage of the iid distribution maximizing the concave harmonic
potential, not a free choice of an arbitrary static mixed profile.
No LP, canonical solver, or floating comparison enters the certificate.
"""
from fractions import Fraction as F
from itertools import product
import json
from decimal import Decimal, getcontext
from pathlib import Path

# Different customers are expanded individually.
sets = ({'a1','a2'}, {'b1','b2','b3','b4'},
        {'a1','a2','c'}, {'a1','a2','d'})
last = ((1,1,1,1),(1,2,3,2),(1,3,1,1),(1,2,1,1))

def action(h):
    return 0 if not h else 1 if len(h)==1 else last[h[0]][h[1]]

def finish(h):
    while len(h)<3:h=h+(action(h),)
    return h

def utility(z,i):
    return sum((F(1,sum(x in sets[a] for a in z)) for x in sets[z[i]]),F(0))

def coverage(z):return len(set().union(*(sets[a] for a in z)))

nodes=[]
for d in range(3):
 for h in product(range(4),repeat=d):
    z=finish(h);u=utility(z,d)
    deviations=[utility(finish(h+(a,)),d) for a in range(4)]
    assert u==max(deviations)
    nodes.append(dict(history=h,action=action(h),outcome=z,payoff=str(u),deviations=list(map(str,deviations))))
z=finish(())
assert z==(0,1,1)
assert [utility(z,i) for i in range(3)]==[F(2)]*3
assert coverage(z)==6
assert max(coverage(z) for z in product(range(4),repeat=3))==8

# Exact quadratic field Q(t), t positive root of 7t^2+23t-5=0.
# Represent a+b*t as (a,b); all formula checks remain rational.
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def mul(x,y):
    a,b=x;c,d=y
    return(a*c+F(5,7)*b*d,a*d+b*c-F(23,7)*b*d)
def scale(c,x):return(c*x[0],c*x[1])
def g(x):return add(add((F(1),F(0)),neg(x)),scale(F(1,3),mul(x,x)))
q=((F(0),F(0)),(F(1),F(-2)),(F(0),F(1)),(F(0),F(1)))
t=(F(0),F(1));two_t=scale(F(2),t)
U0=scale(F(2),g(two_t))
U1=scale(F(4),g(q[1]))
U2=add(g(t),scale(F(2),g(two_t)))
assert U1==U2
assert add(U2,neg(U0))==g(t)
assert U1==(F(36,7),F(-104,7))
# 0<t<11/52<1/2, certified by the increasing defining polynomial.
def P(x):return 7*x*x+23*x-5
assert P(F(0))<0<P(F(11,52))
assert F(11,52)<F(1,2)
# Thus q is a probability vector, all q1,q2,q3 positive. On [0,1],
# g(s)>=1/3>0, so U0<U2=U1. KKT proves global potential optimality.
# Z=3U1>6 iff t<11/52, already certified.
Z=scale(F(3),U1)
assert Z==(F(108,7),F(-312,7))
def cov(x):
    one_minus=add((F(1),F(0)),neg(x))
    return add((F(1),F(0)),neg(mul(mul(one_minus,one_minus),one_minus)))
Zcoverage=add(add(scale(F(4),cov(q[1])),scale(F(2),cov(t))),scale(F(2),cov(two_t)))
assert Zcoverage==Z
assert P(F(1,5))<0 and F(1,5)>F(12,65)
# t>1/5>12/65 proves Z<36/5, hence (5/6)Z<6: weak iid survives.
# Also independently reproduce the known security value by matching rational
# primal p and nonadaptive opponent distribution Q.
pstar=(F(0),F(15,23),F(4,23),F(4,23))
Q={ (1,1):F(3,23),(1,2):F(10,23),(1,3):F(10,23)}
def fbg(a,bg):
    return sum((F(1,1+sum(x in sets[b] for b in bg)) for x in sets[a]),F(0))
assert min(sum((pstar[a]*fbg(a,bg) for a in range(4)),F(0)) for bg in product(range(4),repeat=2))==F(44,23)
assert max(sum((pr*fbg(a,bg) for bg,pr in Q.items()),F(0)) for a in range(4))==F(44,23)
assert 6-3*F(44,23)==F(6,23)>0

assert (F(108,7)-6)/F(312,7)==F(11,52)
# Independent radical expression Z=(4344-156 sqrt669)/49.
assert 675**2-26**2*669==3381>0

getcontext().prec=40
sqrt669=Decimal(669).sqrt();tv=(sqrt669-23)/14
zv=(Decimal(4344)-156*sqrt669)/49
report=dict(status='EXACT_COUNTEREXAMPLE_TO_STRONG_IID_ONLY',instance=dict(players=3,topic_sets=[sorted(s) for s in sets],customer_count=8),actual_outcome=z,actual_payoffs=['2']*3,W=6,OPT3=8,ordered_nodes=len(nodes),comparisons=4*len(nodes),all_spe_comparisons=nodes,q_definition='q=(0,1-2t,t,t), t=(sqrt(669)-23)/14',iid_potential_definition='F(q)=4 f(q1)+f(q2)+f(q3)+2 f(q0+q2+q3); f(s)=3s-3s^2/2+s^3/3',iid_potential_global_optimality='f is strictly concave on [0,1], all active action derivatives 3U coincide, inactive U0<U; simplex KKT sufficient; unique q',t_approx=str(tv),Z3_exact='(4344-156*sqrt(669))/49',Z3_approx=str(zv),Z3_minus_W_approx=str(zv-6),strict_sign_certificate='t is the positive root of increasing P=7t^2+23t-5; P(0)<0<P(11/52)=483/2704; hence t<11/52 iff Z3>6',not_refuted=['W >= 3 v3, with v3=44/23','W >= (1-1/6) Z3','2 W >= OPT3'])
print(json.dumps({k:v for k,v in report.items() if k!='all_spe_comparisons'},indent=2))
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args()
    if args.output:
        with open(args.output,'x') as f:json.dump(report,f,indent=2);f.write('\n')
