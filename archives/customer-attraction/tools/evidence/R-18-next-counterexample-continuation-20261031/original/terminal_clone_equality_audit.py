"""Definition-level exact audit for the two-topic equality family."""
import json
from pathlib import Path
from customer_attraction import CustomerType, Instance, StrategyCertificate, verify_certificate
from itertools import product
from fractions import Fraction

def build(m):
 inst=Instance(('A','B'),(CustomerType(frozenset({0}),m-1),CustomerType(frozenset({1}),2)),m)
 actions={h:(int(h.count(1)<=1) if len(h)==m-1 else 0) for k in range(m) for h in product(range(2),repeat=k)}
 return inst,StrategyCertificate(actions,(m-1,1))
def main():
 reports=[]
 for m in range(2,11):
  inst,cert=build(m);audit=verify_certificate(inst,cert);audit.assert_valid()
  path=(0,)*(m-1)+(1,);u=inst.player_payoffs(path);W=inst.welfare(cert.terminal_counts)
  assert all(2*x==u[-1] for x in u[:-1]);assert 2*W==(m+1)*u[-1]
  reports.append({'m':m,'customers':inst.customer_count,'welfare':W,'OPT':inst.optimal_welfare(),'u':[str(x) for x in u],'histories':audit.checked_histories,'deviations':audit.checked_deviations,'valid':audit.valid})
  if m==5:
   Path(__file__).with_name('terminal_clone_equality_m5_instance.json').write_text(json.dumps(inst.to_dict(),indent=2))
   Path(__file__).with_name('terminal_clone_equality_m5_certificate.json').write_text(json.dumps(cert.to_dict(),indent=2))
 out={'scope':'finite exact regression; general proof is analytic in README','reports':reports}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
