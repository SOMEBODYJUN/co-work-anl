#!/usr/bin/env python3
"""Reuse existing complete-tree bounded MILP with changed exact cap objective.

Only the candidate-generation objective is changed. Any output is separately
reoptimized over its rational complete-policy cone, then replayed exactly.
"""
from pathlib import Path
import sys,inspect,json
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
import cone_attack_joint_milp as original
import terminal_cap_iteration as cap
from customer_attraction_strategy_lp import serializable,independently_verify
source=inspect.getsource(original.joint_candidate)
old='objective[:n]=-np.array(coverage_row(p,portfolio),dtype=float)'
new='objective[:n]=-m*np.array(payoff_row(p,rootq,path[-1]),dtype=float)'
assert old in source
source=source.replace(old,new)
namespace=dict(original.__dict__)
exec(compile(source,'complete_tree_cap_objective','exec'),namespace)
reports=[]
for path in [(0,0,1,1,2),(0,1,1,2,3),(0,1,2,3,3)]:
 cone,metadata=namespace['joint_candidate'](4,path,(),20)
 result=None
 if cone is not None:
  result=cap.optimize(cone,path[-1])
  if result is not None:assert independently_verify(cone,result[1])
 report={'path':path,'metadata':metadata,'exact_cap':str(result[0]) if result else None,'clones':result[1] if result else None,'actions':[{'history':h,'action':a} for h,a in sorted(cone.actions.items())] if cone else None}
 reports.append(report)
 print(json.dumps({k:v for k,v in report.items() if k!='actions'}),flush=True)
 Path(__file__).with_name('terminal_cap_joint.json').write_text(json.dumps(serializable({'scope':'three selected fixed complete-tree paths; numerical candidate MILP, exact recovered cone cap','reports':reports}),indent=2)+'\n')
