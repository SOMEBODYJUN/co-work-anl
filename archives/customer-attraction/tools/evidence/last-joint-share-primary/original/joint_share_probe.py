#!/usr/bin/env python3
"""Use the established full-history joint MILP to propose payoff-cap attacks.

Only the objective is changed in memory. MILP bounds and statuses are recorded
as floating exploration, never as a proof. An extracted tree is independently
optimized and checked with exact strategy-cone constraints.
"""
import argparse,json,sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).parent))
from last_share_probe import *
import cone_attack_joint_milp as joint

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=5);ap.add_argument('--path',action='append',default=[]);ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 out={'scope':'floating full-history joint MILP candidate search, exact extracted-cone witnesses only','records':[]}
 original=joint.coverage_row
 for path in [tuple(map(int,s.split(','))) for s in a.path or ['0,0,1','0,1,0','0,1,1','0,1,2']]:
  p,m=a.topics,len(path);q=tuple(path.count(b) for b in range(p));sentinel=object();obj=payoff_row(p,q,path[-1])
  joint.coverage_row=lambda pp,s:obj if s is sentinel else original(pp,s)
  cone,meta=joint.joint_candidate(p,path,sentinel,a.seconds)
  record={'path':path,'milp':meta}
  if cone is not None:record['exact_cone_optimization']=optimize(cone,path[-1])
  out['records'].append(record);a.output.write_text(json.dumps(serializable(out),indent=2)+'\n')
  print(json.dumps(serializable({'path':path,'milp':meta,'exact_best_share':record.get('exact_cone_optimization',{}).get('value')})),flush=True)
 joint.coverage_row=original
if __name__=='__main__':main()
