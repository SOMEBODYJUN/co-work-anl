"""Exact two-player kernel of the complete 156-label threshold-realized catalogue.

The kernel is an actual finite unit-customer instance after the reported scale.
It is a candidate catalogue only: the old path is not asserted to be SPE.
No atoms need enumerating: pair coverage moments use at most four named indices.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from math import lcm
from functools import lru_cache
import json,hashlib,time,sys
HERE=Path(__file__).resolve().parent
PAT=tuple(product(range(2),repeat=3))


def main():
 start=time.time();sp=HERE/'combined_branch_master_exact.json';zp=HERE/'pair_master_exact.json';point=json.loads(sp.read_text());zpoint=json.loads(zp.read_text());cols=point['columns'];hs={};hi=None;denoms=[]
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=j;mass=F(c['weight']);denoms.append(mass.denominator)
   hs[hi]={'a':tuple(map(int,c['actual_bits'])),'counts':tuple(c['hist']),'mass':mass,'raw':{},'slabs':{}}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));hs[hi]['raw'].setdefault(g,{})[tuple(c['state'])]=F(c['weight'])
 for h in hs.values():
  h['rad']={g:st[1,0]+st[1,1] for g,st in h['raw'].items()}
  denoms += [v.denominator for v in h['rad'].values()]
 for v in zpoint['variables']:
  h=hs[v['hist_column']];key=(v['left'],v['right']);f,d,wi,wj=v['group'];g=(f,d,tuple(wi),tuple(wj));y=F(v['weight']);denoms.append(y.denominator);ss=h['slabs'].setdefault(key,{'r':{},'z':{}});ss['r'][g]=v['r'];ss['z'][g]=y
 hs={i:h for i,h in hs.items() if h['mass']}
 for h in hs.values():
  h['zm']={g:sum(ss['z'][g] for ss in h['slabs'].values()) for g in h['rad']}
  h['pair']={}
  gs=list(h['rad'])
  for g,k in product(gs,repeat=2):
   h['pair']['R',g,'R',k]=min(h['rad'][g],h['rad'][k])
   h['pair']['R',g,'Z',k]=sum(ss['r'][g]*ss['z'][k] for ss in h['slabs'].values())
   h['pair']['Z',g,'R',k]=sum(ss['z'][g]*ss['r'][k] for ss in h['slabs'].values())
   h['pair']['Z',g,'Z',k]=sum(min(ss['z'][g],ss['z'][k]) for ss in h['slabs'].values())
 actions=[('A',i) for i in range(6)]+[(f,i) for f in ('T','B','C') for i in range(6)]
 actions += [(f,k,i,j) for f in ('R','Z') for k,i,j in product(range(2),range(6),range(6)) if k or i!=j]
 assert len(actions)==156
 def label(a):
  if a[0]=='A':return 'A'+str(a[1]+1)
  if a[0] in ('T','B','C'):return a[0]+str(a[1]+1)
  return a[0]+'_'+str(a[1])+'_'+str(a[2]+1)+'_'+str(a[3]+1)
 def canonical(*aa):
  seen={};out=[]
  def cv(x):
   if x not in seen:seen[x]=len(seen)
   return seen[x]
  for a in aa:
   if a[0]=='A':out.append(a)
   elif a[0] in ('T','B','C'):out.append((a[0],cv(a[1])))
   else:out.append((a[0],a[1],cv(a[2]),cv(a[3])))
  return tuple(out),len(seen)
 def cpair(a,b):
  x,k=canonical(a,b);y,kk=canonical(b,a);assert k==kk
  return min(x,y),k
 @lru_cache(None)
 def assignments(counts,k):
  out=[];n=1
  for j in range(k):n*=6-j
  def go(left,words,weight):
   if len(words)==k:out.append((tuple(words),weight));return
   for j,c in enumerate(left):
    if c:
     z=list(left);z[j]-=1;go(tuple(z),words+[PAT[j]],weight*c)
  go(counts,[],1);assert sum(v for _,v in out)==n
  return tuple(out),n
 def event(a,ws,h):
  if a[0]=='A':return ('old',h['a'][a[1]])
  if a[0] in ('T','B','C'):return ('old',ws[a[1]][('T','B','C').index(a[0])])
  return (a[0],(a[1],int(a[2]==a[3]),ws[a[2]],ws[a[3]]))
 def marginal(e,h):
  if e[0]=='old':return h['mass']*e[1]
  return h['rad'][e[1]] if e[0]=='R' else h['zm'][e[1]]
 def intersection(e,f,h):
  if e[0]=='old':return marginal(f,h)*e[1]
  if f[0]=='old':return marginal(e,h)*f[1]
  return h['pair'][e[0],e[1],f[0],f[1]]
 @lru_cache(None)
 def moment(aa,k):
  answer=F()
  for h in hs.values():
   ass,n=assignments(h['counts'],k);v=F()
   for ws,mult in ass:
    e=event(aa[0],ws,h);mass=marginal(e,h) if len(aa)==1 else intersection(e,event(aa[1],ws,h),h);v+=mult*mass
   pa=sum(h['a'][:4]);div=pa+1 if len(aa)==1 else (pa+1)*(pa+2)
   answer+=v/F(n*div)
  return answer
 @lru_cache(None)
 def welfare(aa,k):
  answer=F()
  for h in hs.values():
   if sum(h['a'][:4]):answer+=h['mass'];continue
   ass,n=assignments(h['counts'],k);v=F()
   for ws,mult in ass:
    e=event(aa[0],ws,h);f=event(aa[1],ws,h);v+=mult*(marginal(e,h)+marginal(f,h)-intersection(e,f,h))
   answer+=v/F(n)
  return answer
 fs=[]
 for a in actions:
  key,k=canonical(a);fs.append(moment(key,k))
 gg=[[F()]*156 for _ in range(156)]
 done=0
 for i,a in enumerate(actions):
  for j in range(i,156):
   key,k=cpair(a,actions[j]);v=moment(key,k);gg[i][j]=gg[j][i]=v
  if i%30==0:print('kernel rows',i,'classes',moment.cache_info().currsize,'seconds',time.time()-start,flush=True)
 # Quotient identical coverages; positive G weights detect equality exactly.
 reps=[];aliases=[]
 for i in range(156):
  old=next((j for j,r in enumerate(reps) if gg[i][i]+gg[r][r]-2*gg[i][r]==0),None)
  if old is None:old=len(reps);reps.append(i)
  aliases.append(old)
 scale=720*lcm(*denoms);Q=60*scale
 assert all((v*Q).denominator==1 for v in fs)
 assert all((v*Q).denominator==1 for row in gg for v in row)
 fints=[int(fs[i]*Q) for i in reps];gints=[[int(gg[i][j]*Q) for j in reps] for i in reps]
 us=[[fints[i]-gints[i][j] for j in range(len(reps))] for i in range(len(reps))]
 actual=[aliases[i] for i in range(6)];u5=us[actual[4]][actual[5]];u6=us[actual[5]][actual[4]]
 targetu=[F()]*6
 for h in hs.values():
  a=h['a'];tot=sum(a)
  if tot:
   for i in range(6):targetu[i]+=h['mass']*F(a[i],tot)
 assert F(u5,Q)==targetu[4] and F(u6,Q)==targetu[5]
 report={'scope':'complete threshold-realized finite catalogue exact r2 kernel after fixed actual A1..A4; not an inherited SPE','source_sha256':hashlib.sha256(sp.read_bytes()).hexdigest(),'pair_source_sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'original_labels':[label(a) for a in actions],'original_descriptors':[list(a) for a in actions],'aliases':aliases,'topics':[label(actions[i]) for i in reps],'players':6,'fixed_prefix':actual[:4],'actual_last_pair':actual[4:],'unit_customer_scale':str(scale),'payoff_denominator_for_normalized_point':str(Q),'F_numerators':list(map(str,fints)),'G_numerators':[[str(v) for v in row] for row in gints],'payoff_numerators':[[str(v) for v in row] for row in us],'actual_payoff_numerators':[str(u5),str(u6)],'source_W':point['W'],'kernel_classes':moment.cache_info().currsize,'seconds':time.time()-start}
 if '--with-welfare' in sys.argv:
  ww=[]
  for i in reps:
   row=[]
   for j in reps:
    key,k=cpair(actions[i],actions[j]);v=welfare(key,k)*scale;assert v.denominator==1;row.append(str(v.numerator))
   ww.append(row)
  assert F(int(ww[actual[4]][actual[5]]),scale)==F(point['W'])
  wr={'scope':'exact full-catalogue r2 final welfare after fixed A1..A4; no inherited SPE','kernel_source':'full156_tail2_kernel_10344.json','kernel_sha256':hashlib.sha256((HERE/'full156_tail2_kernel_10344.json').read_bytes()).hexdigest(),'topics':report['topics'],'aliases':aliases,'unit_customer_scale':str(scale),'actual_pair':actual[4:],'welfare_numerators':ww,'source_W':point['W']}
  (HERE/'full156_tail2_welfare_10344.json').write_text(json.dumps(wr,indent=2)+'\n')
 else:(HERE/'full156_tail2_kernel_10344.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('original_labels','original_descriptors','aliases','topics','F_numerators','G_numerators','payoff_numerators')},indent=2),flush=True)
if __name__=='__main__':main()
