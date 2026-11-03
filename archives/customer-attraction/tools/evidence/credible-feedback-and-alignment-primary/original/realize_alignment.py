from pathlib import Path
import sys,json,itertools,math
from fractions import Fraction as F
from collections import defaultdict
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists());sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def main():
 primal=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];sol=json.loads((HERE/'best_alignment_proposal.json').read_text());masses=defaultdict(F)
 atoms=primal['atoms'];ts=[F(sol['x'][5*k]).limit_denominator(10**6) for k in range(len(atoms))]
 coeff=[F(a['mass_numerator'],int(primal['denominator']))/F(sum(map(int,a['bits'][:4]))+1) for a in atoms]
 exact_E=sum(F(a['mass_numerator'],int(primal['denominator']))*F(int(a['bits'][4]),sum(map(int,a['bits'][:5]))) for a in atoms if a['bits'][4]=='1')
 residual=sum(g*t for g,t in zip(coeff,ts))-exact_E
 pivot=next(k for k,t in enumerate(ts) if F(1,10)<t<F(9,10));ts[pivot]-=residual/coeff[pivot]
 assert sum(g*t for g,t in zip(coeff,ts))==exact_E
 for k,a in enumerate(atoms):
  d=sum(a['AB_hist'][4:]);t=ts[k];assert 0<=t<=1
  mass=F(a['mass_numerator'],int(primal['denominator']));base=sum(int(b)<<i for i,b in enumerate(a['bits']))
  for member,prob in [(0,1-t),(1,t)]:
   if not prob:continue
   choices=list(itertools.combinations(range(1,5),d-member))
   assert choices
   for choice in choices:
    mask=base+sum(1<<(10+j) for j in choice)+(member<<10)
    masses[mask]+=mass*prob/len(choices)
 den=math.lcm(*(v.denominator for v in masses.values()));counts={mask:int(mass*den) for mask,mass in masses.items()};gg=math.gcd(*counts.values());counts={m:n//gg for m,n in counts.items()}
 inst=Instance(tuple('ABCDEUVWXY')+tuple('T'+str(j) for j in range(5)),tuple(CustomerType(frozenset(j for j in range(15) if m>>j&1),n) for m,n in sorted(counts.items())),5)
 (HERE/'aligned_catalog_instance.json').write_text(json.dumps(inst.to_dict(),indent=2)+'\n');solver=ExactSPESolver(inst);target=(1,)*5+(0,)*10;report=[]
 for depth in range(4,-1,-1):
  prefix=tuple(int(j<depth) for j in range(15));out=solver.outcomes(prefix);actual=inst.topic_payoff(depth,target);thr=solver.threshold(prefix)
  record={'prefix':inst.topics[:depth],'desired_tail_feasible':target in out,'threshold':str(thr),'on_path_payoff':str(actual),'margin':str(actual-thr),'number_outcomes':len(out),'forcing_deviations':[]}
  if target not in out:
   for j in range(15):
    child=tuple(v+int(ell==j) for ell,v in enumerate(prefix));R=solver.outcomes(child);m=min(inst.topic_payoff(j,q) for q in R)
    if m>actual:record['forcing_deviations'].append({'topic':inst.topics[j],'gain':str(m-actual),'minimum_reply_counts':min(q for q in R if inst.topic_payoff(j,q)==m)})
  report.append(record);print(json.dumps(record),flush=True)
  if target not in out:break
 (HERE/'aligned_catalog_prefix_audit.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
