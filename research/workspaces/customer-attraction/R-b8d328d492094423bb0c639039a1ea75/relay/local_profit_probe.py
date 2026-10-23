"""Attack the F_r(b)-F_{r-1}(b+A)<=2u local profit bridge on fixed full SPEs."""
import json
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cwr
from pathlib import Path
from functools import lru_cache
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate,verify_certificate
ROOT=Path(__file__).resolve().parents[5]

def run(name):
    ex=ROOT/'examples/customer_attraction'/f'{name}.json'
    ce=ROOT/'evidence/certificates/customer_attraction'/f'{name}.json'
    ins=Instance.from_dict(json.loads(ex.read_text())); raw=json.loads(ce.read_text());data=raw.get('strategy',raw)
    if 'terminal_counts' not in data:
        acts={tuple(v['history']):v['action'] for v in data['actions']};h=()
        while len(h)<ins.players:h+=(acts[h],)
        data=dict(data,terminal_counts=ins.counts(h))
    st=StrategyCertificate.from_dict(data);verify_certificate(ins,st).assert_valid()
    k=ins.topic_count;m=ins.players
    @lru_cache(None)
    def F(h):
        b=tuple(sum(t in c.topics for t in h) for c in ins.customers)
        r=m-len(h)
        best=Q(0);arg=()
        for ts in cwr(range(k),r):
            v=Q(0)
            for c,bx in zip(ins.customers,b):
                z=sum(t in c.topics for t in ts)
                if z:v+=Q(c.multiplicity*z,bx+z)
            if v>best:best,arg=v,ts
        return best,arg
    def tail(h):
        h=tuple(h)
        while len(h)<m:h+=st.actions[h],
        return h
    actual=tail(())
    nodes=[h for h in st.actions if len(h)<m]
    # Same-count prefix F is cached by sorted history. Continuation stays ordered.
    worst=None
    for h in nodes:
        a=st.actions[h];out=tail(h);u=ins.player_payoffs(out)[len(h)]
        f,arg=F(tuple(sorted(h)));g,arg2=F(tuple(sorted(h+(a,))))
        gap=f-g-2*u
        row={'history':h,'action':a,'outcome':out,'F':str(f),'F_next':str(g),'u':str(u),'gap':str(gap),'maximizer':arg,'next_maximizer':arg2,'on_actual':h==actual[:len(h)]}
        if worst is None or gap>worst[0]:worst=gap,row
    return {'name':name,'players':m,'topics':k,'nodes':len(nodes),'actual':actual,'worst':worst[1]}

if __name__=='__main__':
    names=['individual_security_failure','aggregate_theta_failure','prefix_balance_failure','root_tax_failure','coverage_opportunity_failure','five_individual_security']
    for n in names:print(json.dumps(run(n)))
