#!/usr/bin/env python3
"""Exact certificates for complementary-resource constructions; no dependencies."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent

def evaluate(weights,resources):
 n=len(weights);states=list(product((0,1),repeat=n));cost={};phi={}
 for s in states:
  c=[F(0)]*n
  for mask,a,k in resources:
   for flip in (0,1):
    us=[i for i in range(n) if mask[i] and s[i]==((mask[i]-1)^flip)]
    v=a*sum((weights[i] for i in us),F(0))**k
    for i in us:c[i]+=v
  cost[s]=c;phi[s]=sum(c)
 ratios=[];rows=[];checks=0
 r=max(sum(bool(v) for v in mask) for mask,_,_ in resources)
 for s in states:
  ds=[];rs=[]
  for i in range(n):
   alt=list(s);alt[i]^=1;alt=tuple(alt)
   ds.append(cost[alt][i]);old=cost[s][i];new=ds[-1]
   assert phi[alt]-phi[s] <= r*new-old
   checks+=1
   assert new>0,'These certificates should have strictly positive costs.'
   rs.append(old/new)
  best=max(rs);ratios.append(best)
  rows.append({'state':list(s),'costs':list(map(str,cost[s])),'deviation_costs':list(map(str,ds)),'ratios':list(map(str,rs)),'witness':rs.index(best),'best_ratio':str(best)})
 return {'weights':list(map(str,weights)),'resources':[{'mask':list(m),'coefficient':str(a),'degree':k} for m,a,k in resources],'threshold':str(min(ratios)),'threshold_decimal':float(min(ratios)),'support_bound':r,'potential_checks':checks,'rows':rows}

def main():
 triad=evaluate([F(1),F(1,3),F(1,9)],[((0,1,1),F(67),2),((1,1,2),F(19),1),((1,2,1),F(10),2)])
 assert triad['threshold']=='3229/3033'
 # Integer weights and normalized integer coefficients, rounded from screening.
 w4=[F(27),F(9),F(3),F(1)]
 rs4=[((0,1,1,1),F(251,13**4),4),((1,2,1,1),F(365,40),1),((1,1,2,1),F(194,40**4),4),((1,1,1,2),F(191,40**4),4)]
 four=evaluate(w4,rs4)
 assert F(four['threshold'])>F(59,50)
 out={'triad':triad,'four_player_rounded':four}
 # Independently rationalize every floating candidate; failure is recorded.
 if (BASE/'screening.json').exists():
  screened=[]
  for run in json.loads((BASE/'screening.json').read_text()):
   if 'coefficients' not in run:continue
   n=run['n'];q=F(str(run['q'])).limit_denominator(1000);w=[q**i for i in range(n)];rr=[]
   for term in run['coefficients']:
    mask=term['mask'];degree=term['degree'];a=F(str(term['normalized_coefficient'])).limit_denominator(10**9)
    total=sum(w[i] for i,v in enumerate(mask) if v)
    rr.append((tuple(mask),a/total**degree,degree))
   cert=evaluate(w,rr);passes=F(cert['threshold'])>F(str(run['alpha']))
   screened.append({'n':n,'q':str(q),'degree':run['d'],'target':str(run['alpha']),'passes_exact':passes,'certificate':cert})
  out['rationalized_screening']=screened
 (BASE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'triad_threshold':triad['threshold'],'four_player_threshold':four['threshold'],'four_player_decimal':four['threshold_decimal'],'exact_move_checks':triad['potential_checks']+four['potential_checks'],'screened_passes':[(x['n'],x['degree'],x['passes_exact']) for x in out.get('rationalized_screening',[])]},indent=2))
if __name__=='__main__':main()
