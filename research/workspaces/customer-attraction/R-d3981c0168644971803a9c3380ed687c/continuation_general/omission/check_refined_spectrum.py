import sys,random,json,itertools
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[6]))
from customer_attraction.model import CustomerType,Instance
from customer_attraction.exact import ExactSPESolver
rng=random.Random(761198)
bestgap=F(0);checked=0
for t in range(1200):
 k=rng.choice([4,5,6]);m=rng.choice([3,4,5])
 types=[]
 for mask in range(1,1<<k):
  sz=mask.bit_count()
  if rng.random()<(.7 if sz==1 else .25 if sz==2 else .04):types.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),rng.randint(1,15)))
 if not types:continue
 inst=Instance(tuple(map(str,range(k))),tuple(types),m);sol=ExactSPESolver(inst)
 sets=[frozenset(j for j,a in enumerate(types) if i in a.topics) for i in range(k)]
 maxima=[a for a in range(k) if not any(sets[a]<sets[b] for b in range(k)) and sets[a] not in sets[:a]]
 private={a:sets[a]-frozenset().union(*(sets[b] for b in maxima if b!=a)) for a in maxima}
 for q in sol.outcomes():
  C=frozenset(j for j,a in enumerate(types) if any(q[i] for i in a.topics))
  Q={a:private[a]-C for a in maxima};aa={a:sum(types[j].multiplicity for j in Q[a]) for a in maxima}
  oldslots=sorted((F(aa[a],l)+F(sum(types[j].multiplicity for j in sets[a]-Q[a]),m) for a in maxima for l in range(1,m+1)),reverse=True)
  for hist in itertools.islice(sol.ordered_outcomes(q),15):
   b=[0]*len(types);newsum=F(0);oldsum=F(0);rows=[]
   for i,act in enumerate(hist):
    r=m-i
    e={a:sum((F(types[j].multiplicity,b[j]+r) for j in sets[a]-Q[a]),F(0)) for a in maxima}
    lam=sorted((F(aa[a],l)+e[a] for a in maxima for l in range(1,r+1)),reverse=True)[r-1]
    direct=max(sum((F(types[j].multiplicity,b[j]+r) for j in sets[a]),F(0)) for a in maxima)
    old=max(oldslots[r-1],direct)
    assert inst.player_payoffs(hist)[i]>=lam>=old
    newsum+=lam;oldsum+=old;rows.append([r,str(lam),str(oldslots[r-1]),str(direct)])
    for j in sets[act]:b[j]+=1
   checked+=1
   if newsum-oldsum>bestgap:
    bestgap=newsum-oldsum
    out={'instance':inst.to_dict(),'path':hist,'welfare':inst.welfare(q),'new':str(newsum),'old_combined':str(oldsum),'gap':str(bestgap),'rows':rows}
    Path(__file__).with_name('refined_spectrum_strict_example.json').write_text(json.dumps(out,indent=2))
    print('gap',str(bestgap),'new',str(newsum),'old',str(oldsum),'w',inst.welfare(q),flush=True)
Path(__file__).with_name('refined_spectrum_regression.json').write_text(json.dumps({'seed':761198,'attempted_inputs':1200,'checked_paths':checked,'best_strict_gap':str(bestgap),'assertions':'actual u_i >= new lambda_i >= max(old private lambda, direct denominator floor)'},indent=2)+'\n')
print('checked',checked,'bestgap',bestgap)
