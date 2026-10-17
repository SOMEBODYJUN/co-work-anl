#!/usr/bin/env python3
"""Self-contained conditional near-flat moment extractor, exact rational HS beam.

No atoms argument in greedy_hs. No prefix-count localizers or entrywise fourth-
moment positivity assumed. Universal near-flat generation is not provided.
Matrix primitives are copied from the earlier prototype; no runtime dependency.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations, product
import hashlib,json,platform,argparse


def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))

def transpose(a): return list(map(list,zip(*a)))

def mm(a,b): return [[dot(row,col) for col in transpose(b)] for row in a]

def mv(a,v): return [dot(row,v) for row in a]

def ident(n): return [[F(i==j) for j in range(n)] for i in range(n)]

def sub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def zero(a): return all(x==0 for row in a for x in row)

def norm(v,g): return dot(v,mv(g,v))

def invert(a):
    n=len(a)
    rows=[row.copy()+ident(n)[k] for k,row in enumerate(a)]
    for k in range(n):
        pivot=next(j for j in range(k,n) if rows[j][k])
        rows[k],rows[pivot]=rows[pivot],rows[k]
        div=rows[k][k];rows[k]=[x/div for x in rows[k]]
        for j in range(n):
            if j!=k and rows[j][k]:
                factor=rows[j][k]
                rows[j]=[x-factor*y for x,y in zip(rows[j],rows[k])]
    return [row[n:] for row in rows]

def psd_exact(matrix):
    """Symmetric rational Schur elimination; zero pivots are handled exactly."""
    a=[list(map(F,row)) for row in matrix]
    n=len(a)
    assert all(len(row)==n for row in a)
    assert a==transpose(a)
    remaining=list(range(n));basis=[];pivots=[]
    while remaining:
        if any(a[i][i]<0 for i in remaining):
            raise ValueError('negative exact Schur diagonal')
        positive=next((i for i in remaining if a[i][i]>0),None)
        if positive is None:
            if any(a[i][j] for i in remaining for j in remaining):
                raise ValueError('zero-diagonal nonzero Schur block')
            break
        pivot=a[positive][positive]
        basis.append(positive);pivots.append(pivot)
        tail=[i for i in remaining if i!=positive]
        for i in tail:
            for j in tail:
                a[i][j]-=a[i][positive]*a[positive][j]/pivot
        remaining=tail
    return {'rank':len(basis),'basis':basis,'positive_pivots':pivots}

def monomials(variables,degree):
    out=[]
    for k in range(degree+1):
        for indices in combinations(range(len(variables)),k):
            if len({variables[e][1] for e in indices})==k:
                out.append(frozenset(indices))
    return out

def build_moments(jobs,atoms,r):
    variables=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
    all_monomials=monomials(variables,2*r)
    def atom_value(s,assignment):
        return all(assignment[variables[e][1]]==variables[e][0] for e in s)
    y={s:sum((w for w,assignment in atoms if atom_value(s,assignment)),F(0)) for s in all_monomials}
    return variables,y

def moment_value(variables,y,s):
    s=frozenset(s)
    if len({variables[e][1] for e in s})!=len(s):return F(0)
    return y[s]

def validate_required(jobs,T,variables,y):
 """Only the stated degree-four contract; no prefix-count or entrywise y>=0 extras."""
 expected=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
 assert variables==expected
 get=lambda s:moment_value(variables,y,s)
 assert get(())==1
 checks=0
 for s in monomials(variables,3):
  for j in range(len(jobs)):
   assert sum((get(s|{e}) for e,(_,v) in enumerate(variables) if v==j),F(0))==get(s)
   checks+=1
 low=monomials(variables,1);high=monomials(variables,2)
 G=[[get(s|t) for t in low] for s in low]
 M2=[[get(s|t) for t in high] for s in high]
 lc=psd_exact(G);hc=psd_exact(M2)
 localizers=[]
 for i in sorted({i for job in jobs for i in job}):
  row=[(e,jobs[j][i]) for e,(v,j) in enumerate(variables) if v==i]
  L=[[T*get(s|t)-sum((p*get(s|t|{e}) for e,p in row),F(0)) for t in low] for s in low]
  checked=psd_exact(L);localizers.append({'machine':i,'rank':checked['rank']})
 return {'low_rank':lc['rank'],'high_rank':hc['rank'],'conservation_checks':checks,'load_localizers':localizers},low,high,G,lc


def tr(a):return sum((a[i][i] for i in range(len(a))),F(0))
def scale(c,a):return [[c*x for x in row] for row in a]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def dumps_f(a):
 if isinstance(a,F):return str(a)
 if isinstance(a,dict):return {str(k):dumps_f(v) for k,v in a.items()}
 if isinstance(a,(list,tuple)):return [dumps_f(v) for v in a]
 return a


def greedy_hs(jobs,T,variables,y,eta,include_certificate=True):
 """Return actual (1+eta)T assignment under the explicit small-defect test.

 Rejecting the defect test says nothing about T infeasibility. Validation uses
 degree-four moments/one-hot relations and exact rational PSD Schur elimination.
 """
 T,eta=F(T),F(eta)
 assert 0<eta<=1 and T>=0
 if not jobs:return {'assignment':[],'loads':{},'trace_defect':F(0),'empty':True}
 checks,low,high,lm,lc=validate_required(jobs,T,variables,y)
 basis=[low[k] for k in lc['basis']];get=lambda s:moment_value(variables,y,s)
 G=[[get(s|t) for t in basis] for s in basis];Gi=invert(G);R=len(G);I=ident(R)
 def adj(M):return mm(mm(Gi,transpose(M)),G)
 def hs2(M):return tr(mm(adj(M),M))
 def op_bound(M,c):
  psd_exact(mm(G,sub(scale(c*c,I),mm(adj(M),M))))
 A=[];D=[];de=[]
 for e in range(len(variables)):
  H=[[get(s|t|{e}) for t in basis] for s in basis]
  a=mm(Gi,H);q=sub(a,mm(a,a))
  assert adj(a)==a
  psd_exact(H);psd_exact(sub(G,H));psd_exact(mm(G,q))
  A.append(a);D.append(q);de.append(tr(q))
 n,d=len(jobs),len(variables);delta=sum(de,F(0))
 for j in range(n):
  assert sum(1 for _,v in variables if v==j)>0
  S=[[sum((A[e][a][b] for e,(_,v) in enumerate(variables) if v==j),F(0)) for b in range(R)] for a in range(R)]
  assert S==I
 machines=sorted({i for job in jobs for i in job})
 for i in machines:
  Q=scale(T,I)
  for e,(v,j) in enumerate(variables):
   if v==i:Q=sub(Q,scale(jobs[j][i],A[e]))
  psd_exact(mm(G,Q))
 threshold=min(F(1,64*n*d*R),eta/F(16))
 if delta>threshold:
  return {'certificate_rejected':True,'reason':'trace defect exceeds sufficient threshold; no infeasibility conclusion',
          'trace_defect':delta,'threshold':threshold,
          'R':R,'n':n,'d':d,'ranks':(checks['low_rank'],checks['high_rank'])}
 eps=n*delta;beta=3*delta
 K=I;chosen=[];beam=[]
 for j in range(n):
  cand=[]
  for e,(_,v) in enumerate(variables):
   if v==j:
    B=mm(A[e],K);cand.append((hs2(B),e,B))
  score,e,K=max(cand,key=lambda z:(z[0],-z[1]));chosen.append(e)
  # Independent exact PSD audit of the analytic near-idempotence estimate.
  Q=sub(mm(K,K),K);op_bound(Q,eps)
  assert score>0 and hs2(K)>=F(1,4)
  beam.append({'job':j,'chosen_edge':e,'scores':[(v,s) for s,v,_ in cand],'K':K,'HS_squared':score})
 h=hs2(K);rho=scale(1/h,mm(K,adj(K)))
 assert tr(rho)==1 and adj(rho)==rho
 psd_exact(mm(G,rho))
 losses=[]
 for e in chosen:
  defect=sub(I,A[e]);L=mm(defect,K)
  op_bound(L,(2*n+1)*delta)
  loss=tr(mm(rho,defect));assert 0<=loss<=beta
  assert loss<=3*de[e]
  losses.append({'edge':e,'loss':loss,'edge_trace_defect':de[e]})
 assignment=[variables[e][0] for e in chosen]
 loads={i:sum((jobs[j][i] for j,v in enumerate(assignment) if v==i),F(0)) for i in machines}
 assert max(loads.values(),default=F(0))<=(1+eta)*T
 result={'assignment':assignment,'loads':loads,'T':T,'eta':eta,'n':n,'d':d,'R':R,
         'ranks':(checks['low_rank'],checks['high_rank']),'trace_defect':delta,'threshold':threshold,
         'epsilon':eps,'beta':beta,'HS_squared':h,'selected_losses':losses,
         'status':'certified actual schedule; no universal small-defect generation claim'}
 if include_certificate:
  result['certificate']={'variables':variables,'basis':[sorted(s) for s in basis],'G':G,'A':A,'D':D,'rho':rho,'beam':beam,
    'moments':[{'monomial':sorted(s),'value':v} for s,v in y.items()]}
 return result


def switch_pair(offset=0,time=F(1)):
 jobs=[{offset:time,offset+1:time}]
 for home,sink in ((offset,offset+2),(offset+1,offset+3)):
  jobs.extend([{home:time/2,sink:time/4} for _ in range(2)])
 a0=(offset,offset+2,offset+2,offset+1,offset+1)
 a1=(offset+1,offset,offset,offset+3,offset+3)
 return jobs,(a0,a1)


def fixture_macro_micro(q,time=F(1),zero_job=False):
 j0,a=switch_pair(0,time);j1,b=switch_pair(4,time);jobs=j0+j1
 atoms=[]
 for x,z in product((0,1),repeat=2):
  weight=q if (x,z)==(1,1) else (1-q)/3
  if weight:atoms.append((weight,a[x]+b[z]))
 if zero_job:
  jobs.append({8:F(0)});atoms=[(w,assignment+(8,)) for w,assignment in atoms]
 return jobs,time,atoms


def fixture_zero(q):
 jobs=[{0:F(0),1:F(0)},{0:F(0),1:F(0)}, {2:F(0),3:F(0)},{2:F(0),3:F(0)}]
 atoms=[]
 for x,z in product((0,1),repeat=2):
  w=q if (x,z)==(1,1) else (1-q)/3
  if w:atoms.append((w,(x,1-x,2+z,3-z)))
 return jobs,F(0),atoms


def run():
 cases=[]
 configs=[('three_point_flat_eta_half',lambda:fixture_macro_micro(F(0)),F(1,2)),
          ('rare_fourth_eta_half',lambda:fixture_macro_micro(F(1,10**12)),F(1,2)),
          ('rare_fourth_eta_tenth_zero_job',lambda:fixture_macro_micro(F(1,10**14),zero_job=True),F(1,10)),
          ('rare_fourth_large_denominators',lambda:fixture_macro_micro(F(1,10**50+151),F(10**40+7,10**40+9)),F(1,10)),
          ('all_zero_T',lambda:fixture_zero(F(1,10**12+39)),F(1,10)),
          ('uniform_nonflat_rejected',lambda:fixture_macro_micro(F(1,4)),F(1,10))]
 for name,build,eta in configs:
  jobs,T,atoms=build();variables,y=build_moments(jobs,atoms,2)
  rs=greedy_hs(jobs,T,variables,y,eta)
  if name=='uniform_nonflat_rejected':assert rs.get('certificate_rejected')
  else:
   assert not rs.get('certificate_rejected')
   if name=='three_point_flat_eta_half':assert rs['trace_defect']==0 and rs['ranks']==(3,3)
   else:assert rs['trace_defect']>0 and rs['ranks']==(3,4)
  cases.append({'name':name,'jobs':jobs,'fixture_distribution':atoms,'result':rs})
 return {'status':'all exact checks passed','python':platform.python_version(),'arithmetic':'Fraction; exact PSD Schur; no eigenvalues/SDP solver',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'self_contained':True,
         'primitive_provenance':'Rational matrix primitives copied from global_assignment_flat_moment_audit.py; runtime has no dependency on that file',
         'cases':cases,'limits':['No general moment/nearflat generator','All fixtures are actual distributions; extractor receives only moments',
                                'Large-defect rejection is not a T infeasibility certificate','Finite examples are not the universal proof']}


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 result=run();args.output.write_text(json.dumps(dumps_f(result),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dumps_f({'status':result['status'],'source_sha256':result['source_sha256'],
  'cases':[{'name':c['name'],**{k:c['result'].get(k) for k in ('n','d','R','ranks','trace_defect','threshold','assignment','loads','certificate_rejected')}} for c in result['cases']]}),ensure_ascii=False,indent=2))
