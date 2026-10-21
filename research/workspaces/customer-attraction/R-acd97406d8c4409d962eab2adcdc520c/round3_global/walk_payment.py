from probe_payment import *
import argparse

def improve(cone,support):
 rows=payment_rows(cone,support);n=(1<<cone.topics)-1
 avg=tuple(sum((rows[i][k][j] for i in range(cone.players) for k in range(len(support))),Fraction(0))/len(support) for j in range(n))
 obj=tuple(w+p-o for w,p,o in zip(cone.welfare,avg,slp.coverage_row(cone.topics,support)))
 res=linprog(np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
 if not res.success:return None
 vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
 if not cone.verify(vals) or slp.dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(res.x)
 if vals is None:return None
 clones=slp.integer_clones(vals)
 return slp.dot(obj,vals),clones

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--steps',type=int,default=100);ap.add_argument('--seed',type=int,default=633);ns=ap.parse_args()
 p=ns.topics;m=ns.players;rng=random.Random(ns.seed);start=time.time();supports=list(combinations(range(p),m));queue=[]
 for r in slp.structural_seeds(p,m):queue.append((r,None))
 seen=set();best=Fraction(100);ci=0
 while ci<ns.steps:
  if not queue:
   r=tuple(rng.randint(0,5) if rng.random()<.15 else 0 for mask in range(1,1<<p));target=None
  else:r,target=queue.pop(rng.randrange(len(queue)))
  if not any(r):continue
  inst=slp.instance_from_clones(p,m,r);solver=ExactSPESolver(inst)
  if target not in solver.outcomes():target=rng.choice(tuple(solver.worst_outcomes()))
  for rep in range(2):
   cone=slp.cone_from_solver(solver,target,rng,True)
   key=tuple(sorted(cone.actions.items()))
   if key in seen:continue
   seen.add(key);ci+=1
   results=[]
   for support in supports:
    rs=improve(cone,support)
    if rs is not None:results.append((rs[0],rs[1],support))
   if not results:continue
   results.sort(key=lambda v:v[0]);q,r2,support=results[0]
   if q<best:
    best=q
    frozen={'q':str(q),'instance':slp.instance_from_clones(p,m,r2).to_dict(),'root':cone.root,'portfolio':support,'actions':[{'h':h,'a':a} for h,a in cone.actions.items()]}
    (OUT/'best_uniform_walk.json').write_text(json.dumps(frozen,indent=2));print('BEST',ci,str(q),round(time.time()-start,2),flush=True)
   queue.extend((rr,cone.root) for qq,rr,ss in results[:3])
   if q<0:print('FOUND',flush=True);return
   print('STEP',ci,'q',str(q),'queue',len(queue),'sec',round(time.time()-start,2),flush=True)
   if ci>=ns.steps:break
if __name__=='__main__':main()
