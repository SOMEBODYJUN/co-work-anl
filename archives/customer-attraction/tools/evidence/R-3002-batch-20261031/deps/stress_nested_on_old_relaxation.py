"""Exact check of the newly pasted same-source requery against old m=6 data.
Only a necessary-row stress test: the input is a relaxation point, not SPE.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[5]
INPUT=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5/six_copy_free_results.json'

def sh(n,d):
    return F(n,d) if n else F(0)

@lru_cache(None)
def phi(p,ell,t,q):
    vals=[]
    for b,c,j,v in product((0,1),repeat=4):
        z1=p+t+b+c;z2=p+c+j+v
        value=(sh(2*t-c,z1)+sh(3*c-v,2*z2)+F(b,2*(p+c+j+1))
               +F(j,4*(ell+1))+F(5*v,12*(ell+1))+F(v,12)
               +F(q,p+t+b+1))
        vals.append(value)
    return -min(vals)

def query_distribution(a,d,ti,qi):
    m=len(a)
    if isinstance(ti,int) and isinstance(qi,int):return [(F(1),a[ti],a[qi])]
    if isinstance(ti,int):return [(F(d if q else m-d,m),a[ti],q) for q in (0,1)]
    if isinstance(qi,int):return [(F(d if t else m-d,m),t,a[qi]) for t in (0,1)]
    if ti=='diag':return [(F(d,m),1,1),(F(m-d,m),0,0)]
    return [(F(v,m*(m-1)),t,q) for (t,q),v in { (1,1):d*(d-1),(1,0):d*(m-d),(0,1):d*(m-d),(0,0):(m-d)*(m-d-1)}.items()]

def main():
    data=json.loads(INPUT.read_text());point=data['final'];m=point['m'];K=F(point['K'])
    support=[(tuple(map(int,z['actual_bits'])),z['d'],F(z['weight'])) for z in point['support']]
    queries=[(i,j) for i in range(m) for j in range(m)]+[(i,'avg') for i in range(m)]+[('avg',i) for i in range(m)]+[('diag','diag'),('off','off')]
    source=m-3
    usrc=sum(n*sh(a[source],sum(a)) for a,d,n in support)
    ulast=sum(n*sh(a[-1],sum(a)) for a,d,n in support)
    budget=F(7,2)*usrc+F(2,3)*ulast+K/12
    scores=[]
    for ti,qi in queries:
        slack=budget+sum(n*sum(prob*phi(sum(a[:source]),sum(a[:-1]),t,q) for prob,t,q in query_distribution(a,d,ti,qi)) for a,d,n in support)
        scores.append({'T':ti,'Q':qi,'slack':str(slack)})
    worst=min(scores,key=lambda z:F(z['slack']))
    report={'status':'exactly evaluated','claim':'new necessary rows evaluated at an old relaxation point, not SPEs','input_W_over_O':point['W'],'m':m,'source_provider':source+1,'u_source':str(usrc),'u_last':str(ulast),'K':str(K),'queries':len(scores),'negative_rows':[z for z in scores if F(z['slack'])<0],'worst':worst,'all_slacks':scores}
    target=Path(__file__).with_suffix('.json');target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('all_slacks','negative_rows')},indent=2));print('negative rows',len(report['negative_rows']))

if __name__=='__main__':main()
