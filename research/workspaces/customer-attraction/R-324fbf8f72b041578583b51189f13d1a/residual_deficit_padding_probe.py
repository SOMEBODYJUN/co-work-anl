"""Exact finite padding diagnosis; no symbolic SPE assertion."""
from pathlib import Path
from fractions import Fraction
import json,argparse,time
from customer_attraction import Instance,CustomerType,ExactSPESolver

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--leaves',type=int,default=6);ap.add_argument('--output',required=True);a=ap.parse_args();k=a.leaves;m=k+3
 root=Path(__file__).resolve().parents[4];d=json.loads((root/'examples/customer_attraction/aggregate_theta_failure.json').read_text());types=[CustomerType(frozenset(t['topics']),10*t['multiplicity'])for t in d['customers']]+[CustomerType(frozenset({6+j}),101)for j in range(k)];inst=Instance(tuple(list(d['topics'])+['L'+str(j) for j in range(k)]),tuple(types),m);s=ExactSPESolver(inst);start=time.monotonic();out=s.outcomes();w=s.minimum_welfare();print('SOLVED',time.monotonic()-start,'outcomes',len(out),'W',w,'stats',s.stats,flush=True)
 bestlast=None;bestpair=None;n=0;kappa=Fraction(m+1,2*(m-1))
 for q in s.worst_outcomes():
  vals=inst.topic_payoffs(q)
  for h in s.ordered_outcomes(q):
   n+=1;last=(m-1)*vals[h[-1]];pair=min(last,(m-kappa)*vals[h[-2]])
   if bestlast is None or last<bestlast[0]:bestlast=(last,h)
   if bestpair is None or pair<bestpair[0]:bestpair=(pair,h)
 report={'scope':'exact finite complete-history SPE outcome enumeration','instance':inst.to_dict(),'welfare':w,'opt':inst.optimal_welfare(),'outcome_count':len(out),'worst_count_vectors':[list(q)for q in sorted(s.worst_outcomes())],'worst_paths':n,'last_min_cost':str(bestlast[0]),'last_min_path':bestlast[1],'pair_min_cost':str(bestpair[0]),'pair_min_path':bestpair[1],'runtime':time.monotonic()-start}
 Path(a.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({key:val for key,val in report.items()if key not in ['instance','worst_count_vectors']},indent=2),flush=True)
if __name__=='__main__':main()
