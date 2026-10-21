from pathlib import Path
"""Find point-actual-terminal phantom-entry obstruction, discovery only."""
exec(open(str(Path(__file__).with_name('extra_integer_probe.py'))).read().split("out={'scope'")[0])
out={'scope':'finite float discovery only','completed':0,'best':None}
for i in range(150):
 n,k=rng.choice([(5,6),(5,7),(6,5)])
 bg=[0]*k
 if i%3:
  for _ in range(rng.choice([1,2,4,8])):bg[rng.randrange(k)]+=1
 M,sunk,R0,scale=base.representation(n,k,bg)
 w=np.array([rng.randrange(1,20) if rng.random()<rng.choice([.2,.5,1.]) else 0 for mask in range(1,1<<k)])
 actions,G,pair,actual=base.policy_cone(n,k,M,sunk,scale,w,rng)
 h=np.array([actual.count(a) for a in range(k)])@M
 root=M[actual[0]]/np.maximum(sunk+h,1)
 for a in range(k):
  c=M[a]/(1+sunk+h)
  lp=linprog(-c,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[root],b_eq=[1.],bounds=(0,None),method='highs')
  if lp.success:
   ratio=float(c@lp.x)
   if out['best'] is None or ratio>out['best']['ratio']+1e-8:
    out['best']={'ratio':ratio,'n':n,'k':k,'background':bg,'actual':actual,'query':a,'weights':lp.x.tolist(),'actions':{','.join(map(str,h)):int(a) for h,a in actions.items()}}
    print(i,ratio,n,k,bg,flush=True)
   if ratio>1+1e-7:break
 out['completed']=i+1
 if i%10==0 or out['best']['ratio']>1+1e-7:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 if out['best']['ratio']>1+1e-7:break
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
