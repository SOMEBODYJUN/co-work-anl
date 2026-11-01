"""Attack a specific signed-query route, not Q-CAG-HALF.
Candidate: some optimal tuple has a permutation whose true continuation-payoff
sum pays Q_full_actual - |C_actual\\O|. LP imposes every permutation at once.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations
import sys,json,math
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,dot,integer_clones,instance_from_clones,independently_verify
from customer_attraction import Instance,StrategyCertificate,verify_certificate
HERE=Path(__file__).resolve().parent


def rows_for(cone,z):
    k,m=cone.topics,cone.players
    query=[];outside=[]
    for mask in range(1,1<<k):
        c=sum(cone.root[a] for a in range(k) if mask>>a&1)
        d=sum(mask>>a&1 for a in z)
        query.append(F(d,1+c));outside.append(F(c>0 and d==0))
    h=();v=[]
    for i in range(m):
        v.append([payoff_row(k,cone.terminals[h+(a,)],a) for a in z])
        h=h+(cone.actions[h],)
    sums=[]
    for pi in set(permutations(range(m))):
        sums.append(tuple(sum((v[i][pi[i]][j] for i in range(m)),F()) for j in range((1<<k)-1)))
    return tuple(query),tuple(outside),sums


def evaluate(cone,weights,z):
    Q,G,vs=rows_for(cone,z)
    return dot(Q,weights)-dot(G,weights)-max(dot(v,weights) for v in vs)


def main():
    uniform = "--uniform" in sys.argv
    suffix = "uniform" if uniform else "net"
    records=[]
    sources=[]
    for ep in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        cp=ROOT/'evidence/certificates/customer_attraction'/ep.name
        if not cp.exists():continue
        try:
            I=Instance.from_dict(json.loads(ep.read_text()))
            raw=json.loads(cp.read_text());raw=raw.get('strategy',raw)
            actions={tuple(x['history']):x['action'] for x in raw['actions']}
            if I.players>4 or I.topic_count>6 or I.players>I.topic_count:continue
            cone=StrategyCone(I.topic_count,I.players,actions)
            sources.append((ep.name,cone))
        except (KeyError,ValueError):pass
    for name in ('thirteen','strict_forty'):
        raw=json.loads((HERE/f'{name}_m3_certificate.json').read_text())
        sources.append((name,StrategyCone(4,3,{tuple(x['history']):x['action'] for x in raw['actions']})))
    for name,cone in sources:
        k,m=cone.topics,cone.players;n=(1<<k)-1
        supports=[z for r in range(1,m+1) for z in combinations(range(k),r)]
        cov={z:coverage_row(k,z) for z in supports}
        for J in combinations(range(k),m):
            Q,G,vs=rows_for(cone,J)
            if uniform:
                vs=[tuple(sum((v[j] for v in vs),F())/len(vs) for j in range(n))]
            signed=np.array([float(q-g) for q,g in zip(Q,G)])
            optimal=np.array([[float(a-b) for a,b in zip(cov[z],cov[J])] for z in supports if z!=J])
            matching=np.array([[float(v)-s for v,s in zip(row,signed)]+[1] for row in vs])
            Aub=np.vstack([np.c_[-cone.matrix,np.zeros(len(cone.rows))],np.c_[optimal,np.zeros(len(optimal))],matching])
            obj=np.zeros(n+1);obj[-1]=-1
            r=linprog(obj,A_ub=Aub,b_ub=np.zeros(len(Aub)),A_eq=[list(map(float,cone.welfare))+[0]],b_eq=[1],bounds=[(0,None)]*n+[(None,None)],method='highs')
            if not r.success:continue
            rec={'uniform':uniform,'source':name,'actual':cone.root,'comparison':J,'max_min_gap_float':-r.fun}
            records.append(rec)
            if -r.fun>1e-7:
                w=tuple(F(float(x)).limit_denominator(10**6) for x in r.x[:n])
                if not cone.verify(w):continue
                allz=list(combinations_with_replacement(range(k),m))
                maxcov=max(dot(coverage_row(k,set(z)),w) for z in allz)
                opt=[z for z in allz if dot(coverage_row(k,set(z)),w)==maxcov]
                mingap=min(evaluate(cone,w,z) for z in opt) if not uniform else min(dot(rows_for(cone,z)[0],w)-dot(rows_for(cone,z)[1],w)-sum((dot(v,w) for v in rows_for(cone,z)[2]),F())/len(rows_for(cone,z)[2]) for z in opt)
                rec.update({'exact_comparison_gap':str(evaluate(cone,w,J)),'minimum_over_all_optimal_tuples':str(mingap),'optimal_tuple_count':len(opt)})
                if mingap>0:
                    clones=integer_clones(w);I=instance_from_clones(k,m,clones)
                    assert independently_verify(cone,clones)
                    verify_certificate(I,StrategyCertificate(cone.actions,cone.root)).assert_valid()
                    payload={'scope':('Uniform assignment candidate only' if uniform else 'Adaptive matching-net candidate only')+'; signed harmonic/query budgets and half not refuted','record':rec,'instance':I.to_dict(),'strategy':StrategyCertificate(cone.actions,cone.root).to_dict()}
                    (HERE/f'signed_matching_{suffix}_counterexample.json').write_text(json.dumps(payload,indent=2)+'\n')
                    (HERE/f'signed_matching_{suffix}_report.json').write_text(json.dumps({'found':True,'records':records},indent=2)+'\n')
                    print(json.dumps(rec),flush=True);return
        print(json.dumps({'source_done':name,'cones':len(records),'best':max([r['max_min_gap_float'] for r in records],default=0)}),flush=True)
    (HERE/f'signed_matching_{suffix}_report.json').write_text(json.dumps({'found':False,'scope':'Finite archived policies only; no universal assertion','records':records},indent=2)+'\n')
    print(json.dumps({'status':'finite_no_counterexample','comparisons':len(records)}))

if __name__=='__main__':main()
