"""Exact fixed replay of the saved separable-omission report point only.
No optimizer, source-program import, policy search, or canonical solver.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import lcm
import json
HERE=Path(__file__).resolve().parent

def main():
 report=json.loads((HERE/'original/f006a01183d092752765/attack_separable_two_report.json').read_text())
 replies=tuple(report['best']['replies']);assert replies[0]==1 and len(replies)==6
 allowed=tuple(mask for mask in range(1,64) if mask&3)+(12,48)
 assert len(allowed)==len(set(allowed))==50
 weights={mask:F(w) for mask,w in report['best']['types']}
 assert len(weights)==len(report['best']['types']) and all(mask in allowed and w>=0 for mask,w in weights.items())
 def utility(a,b,player,weights):
  chosen=(a,b)[player]
  return sum((w/F((mask>>a&1)+(mask>>b&1)) for mask,w in weights.items() if mask>>chosen&1),F(0))
 def coverage(a,b,weights):return sum((w for mask,w in weights.items() if mask>>a&1 or mask>>b&1),F(0))
 def run(weights):
  last=[[utility(a,b,1,weights) for b in range(6)] for a in range(6)]
  root=[utility(a,replies[a],0,weights) for a in range(6)]
  slacks=[]
  for a in range(6):
   slacks += [last[a][replies[a]]-last[a][b] for b in range(6)]
   slacks += [root[0]-root[a]]
  assert len(slacks)==42 and min(slacks)>=0
  W=coverage(0,1,weights);D=sum((w for mask,w in weights.items() if not mask&3),F(0))
  pairs=list(combinations_with_replacement(range(6),2));vals=[coverage(a,b,weights) for a,b in pairs];OPT=max(vals)
  return {'last_player_table':[[str(x) for x in row] for row in last],'root_deviation_values':list(map(str,root)),'W':str(W),'D':str(D),'D_over_W':str(D/W),'SPE_rows_including_self':42,'strict_rows':sum(x>0 for x in slacks),'ties':sum(x==0 for x in slacks),'minimum_slack':str(min(slacks)),'maximum_slack':str(max(slacks)),'comparison_pairs_including_repeat':len(pairs),'OPT_2':str(OPT),'optimal_pairs':[p for p,v in zip(pairs,vals) if v==OPT],'half_margin':str(2*W-OPT)}
 raw=run(weights)
 assert raw['W']==report['exact_W'] and raw['D']==report['exact_D'] and raw['minimum_slack']==report['exact_min_SPE_slack'] and report['exact_SPE_rows']==42 and report['SPE_valid'] is True
 scale=lcm(*(w.denominator for w in weights.values()));integer={mask:int(scale*w) for mask,w in weights.items()};unit=run(integer)
 assert sum(integer.values())==4 and scale==2 and set(integer.values())=={1}
 return {'scope':'one saved complete two-player policy, normalized rational point and its 4-unit-customer integer realization; not a replay of 7776 LPs','allowed_interest_types':allowed,'replies':replies,'normalized_weights':{str(m):str(w) for m,w in weights.items()},'integer_scale':scale,'integer_weights':integer,'normalized':raw,'integer':unit}

if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
