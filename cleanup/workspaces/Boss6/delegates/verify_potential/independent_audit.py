import json
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import sys
base=Path(__file__).resolve().parent/'source'
src=base/'research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1'
sys.path.insert(0,str(base))
from customer_attraction import Instance, StrategyCertificate, verify_certificate
raw=json.loads((src/'potential_branch_obstruction.json').read_text())
inst=Instance.from_dict(raw['instance']); cert=StrategyCertificate.from_dict(raw['certificate'])
ver=verify_certificate(inst,cert)
# exact harmonic potential direct customer loads
def H(k): return sum((F(1,j) for j in range(1,k+1)),F(0))
def phi(counts):
    return sum((customer.multiplicity*H(sum(counts[t] for t in customer.topics)) for customer in inst.customers),F(0))
def terminal(h):
    h=tuple(h)
    while len(h)<inst.players: h += (cert.actions[h],)
    return h, inst.counts(h,terminal=True)
def expected_histories():
    out=[]
    def walk(h):
        if len(h)==inst.players:return
        out.append(h)
        for a in range(inst.topic_count):walk(h+(a,))
    walk(())
    return out
histories=expected_histories()
assert len(histories)==43 and set(histories)==set(cert.actions)
# evaluate every prescribed-vs-alternative action branch
branch_checks=0; potential_lower=[]; identity_fail=[]
for h in histories:
    i=len(h); chosen=cert.actions[h]
    ch,cc=terminal(h+(chosen,))
    for a in range(inst.topic_count):
        ah,ac=terminal(h+(a,)); branch_checks+=1
        u=inst.topic_payoff(a,ac)
        deleted=list(ac); deleted[a]-=1
        if phi(ac)-phi(tuple(deleted)) != u: identity_fail.append((h,a,str(u),str(phi(ac)-phi(tuple(deleted)))))
        if a!=chosen and phi(cc)<phi(ac): potential_lower.append({'history':h,'chosen':chosen,'alternative':a,'chosen_phi':str(phi(cc)),'alternative_phi':str(phi(ac)),'payoff_chosen':str(inst.topic_payoff(chosen,cc)),'payoff_alt':str(u)})
print(json.dumps({
 'certificate_valid':ver.valid,
 'checked_histories':ver.checked_histories,
 'checked_deviations':ver.checked_deviations,
 'expected_histories':len(histories),
 'branch_checks_including_prescribed':branch_checks,
 'identity_failures':identity_fail,
 'potential_lower_comparisons_count':len(potential_lower),
 'first_potential_lower_comparisons':potential_lower[:10],
 'actual':terminal(()),
 'forced_root':terminal((0,)),
 'actual_phi':str(phi(terminal(())[1])),
 'forced_phi':str(phi(terminal((0,))[1])),
},default=str,sort_keys=True))
