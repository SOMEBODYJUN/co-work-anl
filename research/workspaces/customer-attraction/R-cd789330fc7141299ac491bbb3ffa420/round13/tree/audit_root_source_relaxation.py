"""Exact feasibility of a necessary-row relaxation point; never a true SPE claim."""
from pathlib import Path
from fractions import Fraction as F
from types import SimpleNamespace
import importlib.util,sys,json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd();sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from terminal_share_symbolic import build
spec=importlib.util.spec_from_file_location('strategy_lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py');lp=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lp;spec.loader.exec_module(lp)
from customer_attraction import Instance,CustomerType,ExactSPESolver
out=[]
for m in [3,5]:
 p,masks,actual,branch,au,bu,rows,names,welfare=build(m)
 res=linprog(-np.array(au[-1],float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=np.array([welfare],float),b_eq=[1],bounds=(0,None),method='highs')
 dummy=SimpleNamespace(welfare=welfare,rows=rows)
 values=lp.StrategyCone.recover_vertex(dummy,res.x)
 assert values is not None and all(v>=0 for v in values)
 slacks=[lp.dot(row,values) for row in rows]
 assert min(slacks)>=0 and lp.dot(welfare,values)==1
 last=lp.dot(au[-1],values);assert (m+1)*last>2
 clones=lp.integer_clones(values);inst=lp.instance_from_clones(p,m,clones)
 sol=ExactSPESolver(inst);checks=[]
 for label,path in [('actual',actual),('root_source',branch)]:
  prefix=path[:-2];M=sol.threshold(inst.counts(prefix));u=inst.player_payoffs(path)[-2]
  checks.append({'which':label,'prefix':prefix,'tail_current_payoff':str(u),'exact_tail_threshold_M':str(M),'passes_threshold':u>=M})
 out.append({'m':m,'p':p,'status':'exact necessary-row relaxation feasible; NOT SPE certificate','actual_path':actual,'source_path':branch,'actual_payoffs_normalized':[str(lp.dot(a,values)) for a in au],'source_payoffs_normalized':[str(lp.dot(a,values)) for a in bu],'last_share':str(last),'candidate_violation':str((m+1)*last-2),'all_relaxation_slacks_nonnegative':True,'minimum_slack':str(min(slacks)),'positive_normalized_types':[[mask,str(v)] for mask,v in zip(masks,values) if v],'integer_instance':inst.to_dict(),'two_player_tail_checks':checks})
print(json.dumps(out,indent=2))
HERE.joinpath('root_source_relaxation_exact.json').write_text(json.dumps(out,indent=2)+'\n')
