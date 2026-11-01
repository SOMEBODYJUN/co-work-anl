"""Exact feasible witness for 1326 root-completion necessary conditions only."""
from pathlib import Path
from fractions import Fraction as F
import json
HERE=Path(__file__).parent
ns={'__file__':str(HERE/'recover_root_completion.py')};src=(HERE/'recover_root_completion.py').read_text();exec(compile(src.split('x=[F(float(t))')[0],'<exact primitive root coefficients>','exec'),ns)
coefficient=ns['coefficient'];old=ns['old'];masses=ns['mass']
run=json.loads((HERE/'root_full_hist_completion.json').read_text());cols=run['column_specs'];spec=run['row_specs'];names=run['row_names'];x=[F(float(t)).limit_denominator(10**9) for t in run['point']]
for a in range(len(old)):
 inds=[i for i,(aa,h) in enumerate(cols) if a==aa];gap=masses[a]-sum(x[i] for i in inds);j=max(inds,key=lambda i:x[i]);x[j]+=gap;assert x[j]>=0
assert min(x)>=0
S=[i for i,z in enumerate(x) if z]
def off(h,j,k):
 count=sum(n*v[k] for t,v,n in h);z=F()
 for t,v,n in h:
  total=t+sum(v);den=t+sum(v[:j])+4-j;u=F(v[j],total) if v[j] else F();z+=n*(4*u-F(count-v[k],den))/5
 return z
slacks={}
for name,sp in zip(names,spec):
 def colcoef(a,h):
  if sp[0]=='off':return off(h,sp[1],sp[2])
  return sum((F(n,5)*coefficient(sp,(a,t,v)) for t,v,n in h),F())
 slacks[name]=sum((x[i]*colcoef(*cols[i]) for i in S),F())
assert min(slacks.values())>0
report={'scope':'exact feasible full five-index root histogram refinement for 1326 necessary inequalities; not a complete SPE','positive_columns':len(S),'rows':len(names),'equalities':len(old),'all_constraints_verified_exactly':True,'minimum_slack':str(min(slacks.values())),'minimum_slack_float':float(min(slacks.values())),'positive_histograms':[{'atom':cols[i][0],'histogram':cols[i][1],'mass':str(x[i])} for i in S]}
(HERE/'root_full_hist_completion_exact.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='positive_histograms'},indent=2))
