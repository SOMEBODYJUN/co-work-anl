from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib
out=Path(__file__).parent
src=Path('archives/unrelated-machines/tools/evidence/um-joint-projection/exact-witnesses.json')
j=json.loads(src.read_text());results=[];pair_count=0
for name,x in [(f'shift-{z["R"]}-{z["L"]}',z) for z in j['shift_family_cases']]+[('nonuniform',j['nonuniform_decoder_fixture'])]:
 mu={k:list(map(F,v)) for k,v in x['mu'].items()};edges=x['edges'];cs=x['partial_couplings'];left=list(dict.fromkeys(e['u'] for e in edges));right=list(dict.fromkeys(e['v'] for e in edges));S={v:[i for i,p in enumerate(mu[v]) if p] for v in right}
 assert all(sum(v)==1 and min(v)>=0 for v in mu.values())
 assert sum(F(e['weight']) for e in edges)==1
 tau=[]
 for e,c in zip(edges,cs):
  lm=[F(0)]*len(mu[e['u']]);rm=[F(0)]*len(mu[e['v']])
  for a,b,q in c:
   q=F(q);assert q>=0 and e['pi'][a]==b;lm[a]+=q;rm[b]+=q
  assert all(p<=q for p,q in zip(lm,mu[e['u']])) and all(p<=q for p,q in zip(rm,mu[e['v']]))
  tau.append(sum(lm))
 L=max(map(len,S.values()));w=[F(e['weight']) for e in edges];beta=sum(a*b for a,b in zip(w,tau));ref=sum(wi*t/len(S[e['v']]) for wi,t,e in zip(w,tau,edges))
 initial=sum(F(e['weight'])*sum(p for a,p in enumerate(mu[e['u']]) if e['pi'][a] in S[e['v']])/len(S[e['v']]) for e in edges)
 orig=sum(F(e['weight'])*sum(p*mu[e['v']][e['pi'][a]] for a,p in enumerate(mu[e['u']])) for e in edges)
 labels={}
 for u in left:
  scores=[sum(F(e['weight'])/len(S[e['v']]) for e in edges if e['u']==u and e['pi'][a] in S[e['v']]) for a in range(len(mu[u]))];labels[u]=max(range(len(scores)),key=lambda a:scores[a])
 after=sum(F(e['weight'])/len(S[e['v']]) for e in edges if e['pi'][labels[e['u']]] in S[e['v']])
 for v in right:labels[v]=max(S[v],key=lambda b:sum(F(e['weight']) for e in edges if e['v']==v and e['pi'][labels[e['u']]]==b))
 val=sum(F(e['weight']) for e in edges if e['pi'][labels[e['u']]]==labels[e['v']]);d=x['decoder']
 actual={'L':L,'tau_by_edge':list(map(str,tau)),'beta':str(beta),'refined_linear_guarantee':str(ref),'uniform_L_guarantee':str(beta/L),'q1_edge_quadratic_guarantee':str(sum(wi*t*t/L for wi,t in zip(w,tau))),'q1_beta_squared_guarantee':str(beta*beta/L),'original_mu_independent_expectation':str(orig),'right_uniform_initial_expectation':str(initial),'after_left_choice_expectation':str(after),'labels':labels,'satisfied_weight':str(val)}
 assert actual==d,(name,actual,d)
 assert val>=after>=initial>=ref>=beta/L
 if name.startswith('shift'):
  R=x['R'];assert L==x['L'] and beta==F(L,R)
  for pair in x['all_single_label_pairs']:
   a,b=pair['a'],pair['b'];v=sum(F(e['weight']) for e in edges if e['pi'][a]==b);assert v==F(pair['satisfied_weight'])==F(1,R);pair_count+=1
  assert len(x['all_single_label_pairs'])==R*R and F(x['exact_game_value'])==F(1,R)
 results.append({'name':name,**actual})
assert pair_count==1296 and len(results)==37
cart=[]
for t in range(1,5):
 D=2**t;vec=list(product(range(2),repeat=t));resources=list(product(vec,vec));Ss={(g,l):{(a,b) for a,b in resources if all((b[i]+g[i]*a[i])%2==l[i] for i in range(t))} for g in vec for l in vec}
 assert all(len(v)==D for v in Ss.values())
 for g,l,h_l in product(vec,repeat=3):
  h=tuple(1-z for z in g);assert len(Ss[g,l]&Ss[h,h_l])==1
 Bs={g:{(a,b) for a,b in resources if a!=(1,)*t and all(b[i]==(g[(i+1)%t]+g[i]*a[i])%2 for i in range(t))} for g in vec};assert all(len(v)==D-1 for v in Bs.values());assert len(set.union(*Bs.values()))==D*(D-1)
 # Hall is checked exhaustively for the zero f graph, all group subsets including empty.
 adj={g:Ss[g,(0,)*t] for g in vec};k=3**t//D
 for mask in range(1<<D):
  A=[g for i,g in enumerate(vec) if mask>>i&1];N=set().union(*(adj[g] for g in A));assert len(N)>=k*len(A)
 # Full f enumeration through t=3 verifies global resource translation simultaneously.
 f_count=0
 if t<=3:
  for fs in product(list(product(range(2),repeat=2)),repeat=t):
   for g in vec:
    l=tuple(fs[i][g[i]] for i in range(t));image={ (tuple(a[i]^fs[i][0]^fs[i][1] for i in range(t)),tuple(b[i]^fs[i][0] for i in range(t))) for a,b in Ss[g,l]};assert image==adj[g]
   f_count+=1
 cart.append({'t':t,'D':D,'Vfree':str(F(D-1,D)),'k':k,'Vobl':str(F(k,D)),'Rrepair':str(F(k,D-1)),'Hall_subsets':1<<D,'all_f_checked':f_count,'tasks':D**3+D,'machines':2*D**2})
# t1 complete ordinary schedules from the literal model, all jobs finite endpoints.
D=2;t=1;vec=list(product(range(2),repeat=t));jobs=[]
for g in vec:
 jobs.append([( ('M',g,l),F(1)) for l in vec])
 for l in vec:
  for a in vec:
   b=(l[0]^g[0]*a[0],);jobs.append([(('M',g,l),F(1,D)),(('R',a,b),F(1))])
opt=None;cnt=0
for picks in product(*jobs):
 loads={}
 for m,p in picks:loads[m]=loads.get(m,F(0))+p
 peak=max(loads.values());opt=peak if opt is None else min(opt,peak);cnt+=1
assert cnt==1024 and opt==F(3,2)
report={'scope':'Local exact audit, all prescribed decoder fixtures; Cartesian t1..4 construction and all Hall subsets at canonical f, all f translations t1..3; t1 all ordinary schedules. Not all-parameter proof or hardness.','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'decoder_cases':results,'shift_pair_checks':pair_count,'cartesian':cart,'t1_complete_assignments':cnt,'t1_OPT':str(opt)}
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'decoder_cases':len(results),'pairs':pair_count,'cartesian':cart,'t1_complete_assignments':cnt,'t1_OPT':str(opt)},ensure_ascii=False))
