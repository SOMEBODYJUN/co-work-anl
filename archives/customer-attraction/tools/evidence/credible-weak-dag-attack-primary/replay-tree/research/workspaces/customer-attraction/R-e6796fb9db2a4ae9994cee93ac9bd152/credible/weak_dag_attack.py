"""Full outcome-witness DAG attack on m*u_i >= OPT-W.
Imports the existing unrestricted DAG candidate generator. Every accepted point is
recovered in Fraction and independently audited over the full ordered tree.
No universal assertion is inferred from time-limited numerical searches.
"""
from pathlib import Path
import sys,json,argparse,time
from fractions import Fraction as F
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits'),str(ROOT/'research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search')]
from outcome_dag_milp import build,exact_optimize
from customer_attraction_strategy_lp import coverage_row,payoff_row,serializable
from customer_attraction import Instance,StrategyCertificate,verify_certificate

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--topic',type=int,required=True);ap.add_argument('--portfolio',required=True);ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 q=tuple(map(int,args.root.split(',')));p=len(q);m=sum(q);J=tuple(map(int,args.portfolio.split(',')));a=args.topic
 if not q[a]:raise ValueError('tested payoff must belong to an actual player')
 w=coverage_row(p,[b for b,n in enumerate(q) if n]);o=coverage_row(p,J);u=payoff_row(p,q,a)
 objective=tuple(oo-ww-m*uu for oo,ww,uu in zip(o,w,u))
 cone,meta=build(p,q,objective,args.seconds,objective_floor=0.000001)
 exact=exact_optimize(cone,objective) if cone else None
 if exact and exact['certified']:
  clones=exact['integer_clones']
  from customer_attraction_strategy_lp import instance_from_clones,dot
  inst=instance_from_clones(p,m,clones);cert=StrategyCertificate(cone.actions,cone.root)
  audit=verify_certificate(inst,cert);audit.assert_valid()
  exact['instance']=inst.to_dict();exact['root_history']=audit.terminal_history
  exact['checked_histories']=audit.checked_histories;exact['checked_deviations']=audit.checked_deviations
  exact['weak_gap_integer']=str(inst.optimal_welfare()-inst.welfare(q)-m*inst.topic_payoff(a,q))
 report={'scope':'unrestricted full-history outcome-witness DAG candidate search','universal_bound_proved':False,'root':q,'tested_topic':a,'portfolio':J,'milp':meta,'exact_candidate':exact}
 args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
 report['exact_candidate']=None if exact is None else {k:v for k,v in exact.items() if k not in ('strategy','integer_clones','dual_support','instance')}
 print(json.dumps(serializable(report)),flush=True)
if __name__=='__main__':main()
