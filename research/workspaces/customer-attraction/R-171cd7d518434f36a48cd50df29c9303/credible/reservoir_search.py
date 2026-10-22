"""Exact all-SPE outcome oracle on symmetric private themes plus two reservoirs.
This is a finite family probe, not a general efficiency upper bound.
"""
from pathlib import Path
import sys,json,time,argparse,random
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType,Instance,ExactSPESolver,verify_certificate

def make(m,a,b,x):
 k=m-1;R=k;B=k+1;C=k+2;p=k+3;cust=[CustomerType(frozenset((R,B)),x),CustomerType(frozenset((R,C)),x)]
 for j in range(k):
  cust.extend((CustomerType(frozenset((j,)),a),CustomerType(frozenset((j,B,C)),b)))
 return Instance(tuple(f'P{j}' for j in range(k))+('R','B','C'),tuple(cust),m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=5);ap.add_argument('--trials',type=int,default=60);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();rng=random.Random(729148);best=Fraction(0);out=[];start=time.monotonic()
 configs=list((a,1,x) for a in range(1,8) for x in range(1,15));rng.shuffle(configs)
 for a,b,x in configs[:args.trials]:
  ins=make(args.m,a,b,x);sol=ExactSPESolver(ins);w=sol.minimum_welfare();opt=ins.optimal_welfare();ratio=Fraction(opt,w);record={'m':args.m,'a':a,'b':b,'x':x,'W':w,'OPT':opt,'ratio':str(ratio),'worst_outcomes':len(sol.worst_outcomes()),'SPE_outcomes':len(sol.outcomes()),'seconds':time.monotonic()-start}
  if ratio>best:
   best=ratio;record['one_worst']=next(iter(sol.worst_outcomes()));print(json.dumps(record),flush=True)
  out.append(record);args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(out,indent=2)+'\n')
  if ratio>2:
   cert=sol.worst_certificate();verify_certificate(ins,cert).assert_valid();(args.out.parent/(args.out.stem+'_counterexample.json')).write_text(json.dumps({'instance':ins.to_dict(),'certificate':cert.to_dict()},indent=2)+'\n');break
if __name__=='__main__':main()
