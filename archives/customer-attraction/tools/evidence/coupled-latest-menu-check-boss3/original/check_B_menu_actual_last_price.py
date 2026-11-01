"""Definition-level exact replay of the missing actual-last price on 5277 point."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent
source=HERE/'coupled_latest_exact.json';point=json.loads(source.read_text());cols=point['columns'];u6=F();cost=F()
for c in cols:
 if c['kind']=='hist':
  a=tuple(map(int,c['actual_bits']));s=sum(a)
  if s:u6+=F(c['weight'])*F(a[5],s)
 elif c['kind']=='actual-B-branch-state':
  a=tuple(map(int,cols[c['hist_column']]['actual_bits']));cost+=F(c['weight'])*F(c['ell'],1+sum(a[:5]))
slack=6*u6-cost;old=json.loads((HERE/'B_menu_actual_last_price_check.json').read_text());assert slack==F(old['slack'])<0
print(json.dumps({'scope':'one exact new legal price row on specified necessary point; not SPE/half','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'slack':str(slack),'negative':True},indent=2))
