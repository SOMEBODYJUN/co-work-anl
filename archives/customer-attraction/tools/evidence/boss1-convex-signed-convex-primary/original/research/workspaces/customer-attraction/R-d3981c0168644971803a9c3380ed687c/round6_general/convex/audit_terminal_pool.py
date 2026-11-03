"""Exact independent finite arithmetic check of the general terminal pool formulas."""
from pooled_full_probe import ROOT,read_named
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate,verify_certificate
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json

def audit(name):
    raw=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    s=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    game=Instance.from_dict(raw);sd=s.get('strategy',s)
    policy={tuple(row['history']):row['action'] for row in sd['actions']}
    m=game.players;k=game.topic_count
    @lru_cache(None)
    def leaf(h):return h if len(h)==m else leaf(h+(policy[h],))
    z=leaf(());cert=StrategyCertificate(policy,game.counts(z))
    verified=verify_certificate(game,cert);verified.assert_valid()
    incidence=[[int(a in c.topics) for c in game.customers] for a in range(k)]
    weights=[c.multiplicity for c in game.customers];d=len(weights)
    def load(zz):return [sum(incidence[a][x] for a in zz) for x in range(d)]
    def U(T,B,beta):
        return sum(F(weights[x]*incidence[T][x],beta[x]+1+incidence[B][x]) for x in range(d))
    p=[F(1,k)]*k
    us=game.player_payoffs(z);W=sum(us)
    beta=load(z[:-2]);P=z[-2]
    reply=[leaf(z[:-2]+(a,))[-1] for a in range(k)]
    Cs=[[load(leaf(z[:i]+(a,))) for a in range(k)] for i in range(m)]
    J=[sum(p[a]*p[t]*sum(F(weights[x]*incidence[t][x],1+Cs[i][a][x]) for x in range(d))
           for a in range(k) for t in range(k)) for i in range(m)]
    Ipen=us[-2]-sum(p[a]*U(a,reply[a],beta) for a in range(k))
    Ilast=us[-1]-sum(p[t]*U(t,P,beta) for t in range(k))
    G=sum(p[a]*p[t]*(U(reply[a],a,beta)-U(reply[t],a,beta)) for a in range(k) for t in range(k))
    tp=sum(p[a]*p[t]*sum(F(weights[x]*incidence[a][x]*incidence[t][x],
                            (beta[x]+1+incidence[reply[a]][x])*(beta[x]+2+incidence[reply[a]][x]))
                         for x in range(d)) for a in range(k) for t in range(k))
    tm=sum(p[a]*p[t]*sum(F(weights[x]*incidence[a][x]*incidence[t][x],
                            (beta[x]+1+incidence[P][x])*(beta[x]+2+incidence[P][x]))
                         for x in range(d)) for a in range(k) for t in range(k))
    assert min(Ipen,Ilast,G,tp,tm)>=0
    assert us[-2]-J[-2]==Ipen+G+tp
    assert us[-1]-J[-1]==Ilast+tm
    L=[sum(p[a]*Cs[i][a][x] for i in range(m) for a in range(k))/m for x in range(d)]
    rho=[sum(p[t]*incidence[t][x] for t in range(k)) for x in range(d)]
    val=sum(F(weights[x])*rho[x]/(1+L[x]) for x in range(d))
    V=sum(J)-m*val
    assert V>=0
    early=sum(J[i]-us[i] for i in range(m-2))
    bank=Ipen+Ilast+G+tp+tm+V
    assert W-m*val==bank-early
    return dict(name=name,m=m,k=k,histories=verified.checked_histories,
                terminal_payments_verified=True,all_balance_checks=True,
                IC_pen=str(Ipen),IC_last=str(Ilast),cross_BR=str(G),
                tax_pen=str(tp),tax_last=str(tm),Jensen_pool=str(V),
                early_deficit=str(early),bank=str(bank),W_minus_mF=str(W-m*val))

if __name__=='__main__':
    names=['aggregate_theta_failure','individual_security_failure','root_tax_failure',
           'global_decorrelation_failure','fractional_actual_load_failure','eight_cce_welfare_gap']
    rows=[audit(name) for name in names]
    out=dict(scope='Exact arithmetic only; the general formulas are proved in the companion note',records=rows)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
