"""Attack exact terminal-share candidate; finite tests never give a universal proof."""
import sys,random,json,importlib.util
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=Path.cwd();sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('strategy_lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
lp=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lp;spec.loader.exec_module(lp)
from customer_attraction import Instance,CustomerType,ExactSPESolver
rng=random.Random(131313)
best=Fraction(0)
for m,p,reps in [(3,4,150),(4,5,100),(5,5,50)]:
 for it in range(reps):
  inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),rng.randint(1,15)) for mask in range(1,1<<p) if rng.random()<.5),m)
  sol=ExactSPESolver(inst);paths=list(sol.ordered_outcomes())
  if not paths:continue
  path=max(paths,key=lambda path:inst.player_payoffs(path)[-1]/max(1,inst.welfare(inst.counts(path))))
  cert=sol.certificate(on_path=path);cone=lp.StrategyCone(p,m,dict(cert.actions))
  objective=lp.payoff_row(p,cone.root,path[-1])
  res=linprog(-np.array(objective,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
  if not res.success:raise AssertionError(res.message)
  values=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
  if not cone.verify(values) or lp.dot(cone.welfare,values)!=1:values=cone.recover_vertex(res.x)
  if values is None or not cone.verify(values) or lp.dot(cone.welfare,values)!=1:continue
  share=lp.dot(objective,values)
  if share>best:best=share; print('best',m,p,it,str(share),path,flush=True)
  if (m+1)*share>2:
   clones=lp.integer_clones(values);found=lp.instance_from_clones(p,m,clones)
   assert lp.independently_verify(cone,clones)
   obj={'status':'exact full strategy counterexample to terminal share candidate','m':m,'p':p,'path':path,'payoffs':list(map(str,found.player_payoffs(path))),'W':found.welfare(found.counts(path)),'ratio':str((m+1)*share/2),'instance':found.to_dict(),'actions':[[list(h),a] for h,a in sorted(cone.actions.items())]}
   out=Path(__file__).with_name('terminal_share_counterexample.json');out.write_text(json.dumps(obj,indent=2));print('COUNTEREXAMPLE',out,flush=True);raise SystemExit
 print('completed',m,p,reps,flush=True)
