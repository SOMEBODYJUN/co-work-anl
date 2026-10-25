"""Independent, definition-level two-singleton complete SPE replay."""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json
root=Path(__file__).parent
x=json.loads((root/'weighted_maximum_old_refund_obstruction.json').read_text())
pol={tuple(a['history']):a['action'] for a in x['certificate']['actions']}
histories=[h for n in range(5) for h in product((0,1),repeat=n)]
assert set(pol)==set(histories)
for h in histories:
 assert pol[h]==(0 if len(h)<=2 or h.count(0)<2 else 1)
def end(h):
 while len(h)<5:h=h+(pol[h],)
 return h
def pay(a,z):return F(1,z.count(a))
comparisons=0
for h in histories:
 own=pay(pol[h],end(h))
 for a in (0,1):
  assert own>=pay(a,end(h+(a,))),(h,a)
  comparisons+=1
actual=end(());forced=end((0,0,1))
assert actual==(0,0,0,1,1) and forced==(0,0,1,1,1)
assert pay(0,actual)==F(1,3) and pay(0,forced)==F(1,2)
assert pay(0,actual)==pay(1,forced)
assert sum(pay(a,forced)-pay(a,actual) for a in actual[:2])==F(1,3)
assert len(set(actual))==len(set(forced))==2
out={'status':'PASS_genuine_complete_SPE_refund_obstruction_not_HALF','histories':len(histories),'comparisons':comparisons,'actual':actual,'forced_H':forced,'old_total_refund':'1/3','current_IC_slack':0,'weighted_max_gap_eta':0,'coverage_added':0}
(root/'audit_old_refund_obstruction.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
