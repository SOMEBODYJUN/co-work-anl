"""Test one rational independent-across-index lift of the feasible root refinement.
Failure excludes only this lift, not every coupling or a complete SPE.
"""
from pathlib import Path
from fractions import Fraction as F
import json
HERE=Path(__file__).parent
old=json.loads((HERE/'enhanced_2396_exact_obstruction.json').read_text())['atom_masses'];run=json.loads((HERE/'root_menu_completion_exact.json').read_text());rows=run['positive_refinements'];mass=[F(a['mass']) for a in old]
from offdiagonal_probe import types
d=[sum(n*t for n,(t,x,y) in zip(a['AB_hist'],types)) for a in old]
means={}
for a in range(len(old)):
 for t in (0,1):
  den=mass[a]*(d[a] if t else 5-d[a])/5
  means[a,t]=[sum((F(r['mass'])*r['replies'][k] for r in rows if r['atom']==a and r['t']==t),F())/den if den else F() for k in range(4)]
def q(n,d):return n/d if n else F()
slack={f'root:{j}:off-menu:{k}':F() for j in range(4) for k in range(4)}
for r in rows:
 a,t,v,w=r['atom'],r['t'],r['replies'],F(r['mass']);total=t+sum(v)
 for j in range(4):
  den=t+sum(v[:j])+4-j;u=q(F(v[j]),total)
  for k in range(4):
   other=(d[a]-t)*means[a,1][k]+(4-d[a]+t)*means[a,0][k]
   slack[f'root:{j}:off-menu:{k}']+=w*(4*u-other/den)
report={'scope':'one independent conditional root-index lift only; not all couplings','negative':{n:str(v) for n,v in slack.items() if v<0},'slacks':{n:str(v) for n,v in slack.items()}}
(HERE/'independent_root_lift.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({n:float(F(v)) for n,v in report['negative'].items()},indent=2))
