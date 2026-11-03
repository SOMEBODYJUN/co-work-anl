"""Definition-level full-tree construction for a five-player helper counterexample.

No customer-attraction solver imported. Not a counterexample to HALF(5).
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
PREF=(0,1,1,1,0)

def run():
    sigma={}
    def build(h):
        if len(h)==5:return h
        choices=[]
        for t in (0,1):
            z=build(h+(t,));choices.append((F(1,z.count(t)),t,z))
        value=max(v for v,t,z in choices)
        tied=[(t,z) for v,t,z in choices if v==value]
        t,z=next(((t,z) for t,z in tied if t==PREF[len(h)]),tied[0])
        sigma[h]=t;return z
    actual=build(())
    def finish(h):
        while len(h)<5:h=h+(sigma[h],)
        return h
    checks=0;bycount={}
    for depth in range(5):
        for h in product((0,1),repeat=depth):
            c=h.count(0);key=(depth,c)
            if key in bycount:assert bycount[key]==sigma[h]
            bycount[key]=sigma[h];z=finish(h);v=F(1,z.count(z[depth]))
            for t in (0,1):
                zz=finish(h+(t,));assert v>=F(1,zz.count(t));checks+=1
    assert actual==(0,1,1,1,0)
    u=[F(1,actual.count(t)) for t in actual]
    harmonic=lambda n:sum((F(1,j) for j in range(1,n+1)),F(0))
    q=[actual[:3].count(t) for t in (0,1)]
    phi_actual=sum(harmonic(actual.count(t)) for t in (0,1))
    candidates=[harmonic(q[0]+a)+harmonic(q[1]+2-a) for a in range(3)]
    gamma=max(candidates)-phi_actual;gap=sum(u[:3])+gamma-3*u[-1]
    assert gamma==0 and gap==F(-1,3)
    result={'status':'passed','scope':__doc__,'themes':[[0],[1]],'actual':actual,'payoffs':list(map(str,u)),
            'Gamma2_definition':'maximum harmonic terminal potential after two slots at actual three-prefix minus actual terminal potential',
            'Gamma2':str(gamma),'gap':str(gap),'tie_preferences':PREF,'count_consistent':True,'complete_histories':len(sigma),'all_action_comparisons':checks,
            'policy_by_depth_and_previous_zero_count':{str(d):[bycount[d,c] for c in range(d+1)] for d in range(5)},
            'actions':[{'history':h,'action':t} for h,t in sorted(sigma.items(),key=lambda x:(len(x[0]),x[0]))]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='actions'}))
if __name__=='__main__':run()
