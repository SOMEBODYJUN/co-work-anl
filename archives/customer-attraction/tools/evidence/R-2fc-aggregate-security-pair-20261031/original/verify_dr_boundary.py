"""Exact self-contained audit of an enlarged-model boundary, NOT a CAG instance."""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json

K=6
PHI={
 '':0,
 '0':240,'1':161,'2':225,'3':225,'4':176,'5':225,
 '00':345,'01':401,'02':401,'03':345,'04':296,'05':345,
 '11':161,'12':386,'13':281,'14':281,'15':281,
 '22':330,'23':345,'24':281,'25':345,
 '33':225,'34':401,'35':401,'44':296,'45':401,'55':345,
 '000':345,'001':506,'002':506,'003':401,'004':345,'005':401,
 '011':401,'012':506,'013':401,'014':401,'015':401,
 '022':506,'023':401,'024':401,'025':401,'033':345,'034':401,'035':401,
 '044':296,'045':401,'055':401,
 '111':161,'112':386,'113':281,'114':281,'115':281,
 '122':476,'123':386,'124':386,'125':386,'133':281,'134':401,'135':401,
 '144':296,'145':401,'155':345,
 '222':330,'223':401,'224':330,'225':401,'233':345,'234':401,'235':401,
 '244':296,'245':401,'255':401,
 '333':225,'334':401,'335':401,'344':521,'345':521,'355':521,
 '444':296,'445':521,'455':521,'555':345,
}

def phi(h):return PHI[''.join(map(str,sorted(h)))]
def marginal(h,a):return phi(tuple(h)+(a,))-phi(h)
def action(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    group=range(3) if h[1]<3 else range(3,6)
    return next(a for a in group if a not in h)
def terminal(h):
    while len(h)<3:h=tuple(h)+(action(h),)
    return tuple(h)
def utility(z,i):return phi(z)-phi(z[:i]+z[i+1:])

def main():
    expected={''.join(map(str,h)) for d in range(4) for h in combinations_with_replacement(range(K),d)}
    assert set(PHI)==expected
    mono=[];dr=[];deviations=[]
    for d in range(3):
        for h in combinations_with_replacement(range(K),d):
            for a in range(K):
                value=marginal(h,a);assert value>=0;mono.append(value)
    for d in range(2):
        for h in combinations_with_replacement(range(K),d):
            for a,b in product(range(K),repeat=2):
                value=marginal(h,a)-marginal(h+(b,),a)
                assert value>=0;dr.append(value)
    for d in range(3):
        for h in product(range(K),repeat=d):
            z=terminal(h);u=utility(z,d)
            for a in range(K):
                alt=terminal(h+(a,));slack=u-utility(alt,d)
                assert slack>=0;deviations.append(slack)
    p=(F(4,15),0,F(4,15),0,F(3,15),F(4,15))
    backgrounds=list(combinations_with_replacement(range(K),2))
    primal={''.join(map(str,h)):sum(p[a]*marginal(h,a) for a in range(K)) for h in backgrounds}
    assert min(primal.values())==56
    dual=tuple(marginal((0,3),a) for a in range(K));assert max(dual)==56
    z=terminal(());u=tuple(utility(z,i) for i in range(3));w=sum(u)
    assert z==(0,3,4) and u==(0,105,56) and w==161
    assert w<3*56 and sum(u[:2])<2*56
    # A customer-attraction harmonic potential must satisfy this equality.
    assert 2*phi((1,1))!=3*phi((1,))
    third=[]
    for acts in combinations_with_replacement(range(K),3):
        difference=0
        for bits in product((0,1),repeat=3):
            h=tuple(a for a,yes in zip(acts,bits) if yes)
            difference+=(-1)**(3-sum(bits))*phi(h)
        if difference<0:third.append((''.join(map(str,acts)),difference))
    report={'scope':'Exact counterexample in monotone DR marginal-potential games, NOT CAG',
      'players':3,'actions':6,'potential_states':len(PHI),'monotonicity_checks':len(mono),
      'DR_checks':len(dr),'ordered_SPE_nodes':43,'SPE_comparisons':len(deviations),
      'path':z,'utilities':u,'W':w,'security_value':56,'strong_gap_m_v_minus_W':7,
      'first_two_gap_2v_minus_pair':7,'weak_gap_W_minus_2.5v':21,
      'query':[str(x) for x in p],'primal_background_values':{k:str(v) for k,v in primal.items()},
      'dual_background':'03','dual_query_values':dual,
      'negative_third_differences':third,
      'non_CAG_witness':'Phi(11)=Phi(1)=161, violates 2Phi(11)=3Phi(1)'}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
