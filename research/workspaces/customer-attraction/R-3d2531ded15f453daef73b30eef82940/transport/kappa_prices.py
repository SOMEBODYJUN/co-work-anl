"""Exact free-start capture prices on a fixed full-history SPE certificate.

No claim that the sufficient kappa budget always holds is made.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver


def finish(cert,h,m):
    h=tuple(h)
    while len(h)<m:
        h=h+(cert.actions[h],)
    return h


def prices(inst,cert):
    m=inst.players
    path=finish(cert,(),m)
    u=inst.player_payoffs(path)
    leaves={}
    D={}
    for i in range(m):
        for a in range(inst.topic_count):
            z=finish(cert,path[:i]+(a,),m)
            leaves[i,a]=z
            D[i,a]=inst.player_payoffs(z)[i]
    answer={}
    detail={}
    for ci,cust in enumerate(inst.customers):
        if any(a in cust.topics for a in path) or not cust.topics:
            continue
        V={}
        costs={}
        for i in reversed(range(m)):
            for a in cust.topics:
                followers=[j for j in range(i+1,m) if leaves[i,a][j] in cust.topics]
                costs[i,a]=(u[i]/D[i,a]+sum(V[j] for j in followers))/(1+len(followers))
            V[i]=min(costs[i,a] for a in cust.topics)
        answer[ci]=min(V.values())
        detail[ci]=(V,costs)
    return path,u,leaves,D,answer,detail


def optimal_residual(inst,path,kappa):
    optimum=inst.optimal_welfare()
    actual={ci for ci,c in enumerate(inst.customers) if any(a in c.topics for a in path)}
    reports=[]
    for size in range(1,min(inst.players,inst.topic_count)+1):
        for ts in combinations(range(inst.topic_count),size):
            covered={ci for ci,c in enumerate(inst.customers) if any(a in c.topics for a in ts)}
            if sum(inst.customers[ci].multiplicity for ci in covered)!=optimum:
                continue
            R=covered-actual
            G=sum(inst.customers[ci].multiplicity for ci in actual-covered)
            residual=F(0)
            cancelled=G
            for ci in sorted(R,key=lambda ci:kappa[ci],reverse=True):
                n=inst.customers[ci].multiplicity
                cancel=min(cancelled,n)
                cancelled-=cancel
                residual+=(n-cancel)*kappa[ci]
            assert cancelled==0
            reports.append((residual,ts,G,R))
    return min(reports),reports


def audit_bellman(inst,cert,limit=1000):
    path,u,z,D,kappa,detail=prices(inst,cert)
    checked=0
    for ci,(V,costs) in detail.items():
        sig=inst.customers[ci].topics
        if len(sig)**inst.players>limit:
            continue
        for start in range(inst.players):
            for first in sig:
                values=[]
                for policy in product(sig,repeat=inst.players-start-1):
                    choices={start:first,**{j:policy[j-start-1] for j in range(start+1,inst.players)}}
                    flow={j:F(int(j==start)) for j in range(start,inst.players)}
                    fee=F(0)
                    absorbed=F(0)
                    for i in range(start,inst.players):
                        a=choices[i]
                        followers=[j for j in range(i+1,inst.players) if z[i,a][j] in sig]
                        share=flow[i]/(1+len(followers))
                        fee+=share*u[i]/D[i,a]
                        absorbed+=share
                        for j in followers:
                            flow[j]+=share
                    assert absorbed==1
                    values.append(fee)
                assert min(values)==costs[start,first]
                checked+=1
    return checked


def main():
    names=['root_tax_failure','individual_security_failure','collision_free_occupancy',
           'fractional_actual_load_failure','dynamic_iid_local','portfolio_matching_failure',
           'worst_cce_welfare_failure','eight_cce_welfare_gap','prefix_balance_failure']
    report=[]
    for name in names:
        obj=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
        inst=Instance.from_dict(obj)
        solver=ExactSPESolver(inst)
        for target in sorted(solver.worst_outcomes())[:2]:
            cert=solver.certificate(target)
            path,u,z,D,kappa,detail=prices(inst,cert)
            best,allreports=optimal_residual(inst,path,kappa)
            welfare=sum(u)
            report.append({'name':name,'path':path,'W':str(welfare),'OPT':inst.optimal_welfare(),
                           'cheapest_residual_cost':str(best[0]),'best_optimum':best[1],
                           'G':best[2],'bridge_holds':best[0]<=welfare,
                           'bellman_bruteforce_checks':audit_bellman(inst,cert),
                           'kappa':{str(ci):str(v) for ci,v in kappa.items()}})
            print(name,path,best[0],welfare,'PASS' if best[0]<=welfare else 'BRIDGE FAIL',flush=True)
    output=Path(__file__).with_name('kappa_existing_audit.json')
    output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
