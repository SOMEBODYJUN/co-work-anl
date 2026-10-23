"""Exact symbolic audit of a strict unique-SPE population-decrease family.
No project solver is imported. A frozen complete policy's comparison slacks
are computed as affine functions of integer q; coefficient signs prove all q>=22.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
TYPES=((0,1),(2,),(1,2),(0,3),(0,1,3),(2,3))
BASE=(3,1,2,1,3,3)
OFFSET=(1,-10,-12,-11,-7,-11)
P2={():0,(0,):2,(1,):3,(2,):1,(3,):1}
P3={():3,(0,):2,(1,):3,(2,):1,(3,):1}
LAST=((2,2,1,1),(2,3,0,1),(1,0,0,1),(1,1,1,1))
for a in range(4):
    for b in range(4):P3[a,b]=LAST[a][b]


def utility(weights,history,i):
    a=history[i]
    return sum((F(w,sum(b in t for b in history)) for t,w in zip(TYPES,weights) if a in t),F(0))


def audit(m,policy):
    expected={h for d in range(m) for h in product(range(4),repeat=d)}
    assert set(policy)==expected
    def follow(h):
        while len(h)<m:h+=(policy[h],)
        return h
    rows=[]
    for h in sorted(expected,key=lambda x:(len(x),x)):
        chosen=policy[h];z=follow(h+(chosen,));i=len(h)
        for b in range(4):
            if b==chosen:continue
            zz=follow(h+(b,))
            alpha=utility(BASE,z,i)-utility(BASE,zz,i)
            beta=utility(OFFSET,z,i)-utility(OFFSET,zz,i)
            assert alpha>=0
            assert alpha*22+beta>0
            if alpha==0:assert beta>0
            rows.append({'history':list(h),'chosen':chosen,'deviation':b,'alpha':str(alpha),'beta':str(beta),'slack_q22':str(alpha*22+beta)})
    threshold=max((-F(x['beta'])/F(x['alpha']) for x in rows if F(x['alpha'])>0),default=None)
    return {'players':m,'nodes':len(expected),'path':list(follow(())),'all_strict_for_q_ge':22,'exact_threshold_q_strictly_greater_than':str(threshold),'minimum_slack_q22':str(min(F(x['slack_q22']) for x in rows)),'rows':rows}


def main():
    report={'scope':'Auxiliary population-exchange boundary only; Q-CAG-HALF remains OPEN','parameter':'integer q>=22','type_order':[[a for a in t] for t in TYPES],'multiplicities':['3q+1','q-10','2q-12','q-11','3q-7','3q-11'],'total_and_OPT':'13q-50','minimum_SPE_W2':'13q-50','minimum_SPE_W3':'12q-40','decrease':'q-10','W3_over_W2_limit':'12/13','policies':[audit(2,P2),audit(3,P3)]}
    assert all(22*a+b>0 for a,b in zip(BASE,OFFSET))
    assert sum(BASE)==13 and sum(OFFSET)==-50
    assert report['policies'][0]['path']==[0,2]
    assert report['policies'][1]['path']==[3,1,1]
    (HERE/'strict_population_family_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'passed','all_integer_q_ge':22,'population_decrease':'q-10','strict_unique_full_SPE':True,'thresholds':[x['exact_threshold_q_strictly_greater_than'] for x in report['policies']]}))

if __name__=='__main__':main()
