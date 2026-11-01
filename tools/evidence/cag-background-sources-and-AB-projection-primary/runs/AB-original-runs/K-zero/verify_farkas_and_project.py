"""Independent standard-library exact AB audit and complete visible projection.

Reconstructs a guarded set of fifteen supported raw row formulas, uses no discovery module,
NumPy, optimizer, or saved per-type maxima. Every d-compatible 16-bin
histogram is checked. Integer coefficients already include share scaling60.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,json,time
HERE=Path(__file__).resolve().parent
N=6

def compositions(n,k):
 if k==1:yield (n,);return
 for v in range(n+1):
  for rest in compositions(n-v,k-1):yield (v,)+rest

def share(n,d):return 60*n//d if n else 0

def primitives(p,t,f,b,c):
 z=p+t+f+b+c;D=60//(p+t+f+b+1);A=60//(p+t+f+1);G=60//((p+t+f+1)*(p+t+f+2))
 H=share(b,z)+share(c,z)+b*G;D1=60//(p+t+3)
 return (f,b,c,f*c,b*c,share(t,z),share(c,z),D,f*D,b*D,A,f*A,b*A,c*A,G,f*G,b*G,b*c*G,H,share(f,z),D1,c*D1)

def features(p,d):
 # The two T-groups are histogrammed independently; concatenating these
 # histograms is bijective with the complete d-compatible 16-bin domain.
 pats=list(product((0,1),repeat=3));parts=[]
 for t,count in [(0,N-d),(1,d)]:
  prim=[primitives(p,t,*word) for word in pats];entries=[]
  for hist in compositions(count,8):
   feat=tuple(sum(h*pr[j] for h,pr in zip(hist,prim)) for j in range(22))
   entries.append((hist,feat))
  parts.append(entries)
 for (h0,x),(h1,y) in product(*parts):yield h0+h1,tuple(a+b for a,b in zip(x,y))

SUPPORTED={'source','cap:3','fixedpair:actual:1:3','fixedpair:actual:2:3',
 'fixedfloor:actual:1:3','fixedfloor:actual:5:1','fixedfloor:actual:5:2','fixedfloor:actual:5:3',
 'floorfamily:1:3:off','floorfamily:3:1:off','floorfamily:3:2:off','floorfamily:3:3:all',
 'pairfamily:1:1:all_distinct','pairfamily:2:2:all_distinct','pairfamily:2:3:query_equal'}

def weighted_hidden(f,actual,L):
 a,pf,ell=actual;w=lambda name:L.get(name,0)
 nf,nb,nc,nfc,nbc,st,sc,D,fD,bD,A,fA,bA,cA,G,fG,bG,bcG,H,sf,D1,cD1=f
 val=-w('source')*st-60*w('cap:3')*nc
 val-=w('fixedfloor:actual:1:3')*(60//(a+5))*nc
 for q,nq in [(1,nf),(2,nb),(3,nc)]:val-=w(f'fixedfloor:actual:5:{q}')*(60//(ell+1))*nq
 val+=w('fixedpair:actual:1:3')*(-(60//(pf+1))*(nf+nc)+(60//((pf+1)*(pf+2)))*nfc)
 val+=w('fixedpair:actual:2:3')*(-(60//(pf+1))*(nb+nc)+(60//((pf+1)*(pf+2)))*nbc)
 val+=w('floorfamily:1:3:off')*(5*sf-nc*D1+cD1)
 val+=w('floorfamily:3:1:off')*(5*sc-nf*D+fD)
 val+=w('floorfamily:3:2:off')*(5*sc-nb*D+bD)
 val+=w('floorfamily:3:3:all')*(6*sc-nc*D)
 val+=w('pairfamily:1:1:all_distinct')*(20*H-8*(nf*A-fA)+nf*(nf-1)*G-2*(nf-1)*fG)
 val+=w('pairfamily:2:2:all_distinct')*(20*H-8*(nb*A-bA)+nb*(nb-1)*G-2*(nb-1)*bG)
 val+=w('pairfamily:2:3:query_equal')*(5*H-(nb+nc)*A+bA+cA+nbc*G-bcG)
 return val

def constant(bits,L):
 w=lambda name:L.get(name,0);z=sum(bits);u2=share(bits[1],z);u3=share(bits[2],z);u6=share(bits[5],z)
 pf=sum(bits[:4]);de=(pf+1)*(pf+2)
 H=share(bits[4],z)+share(bits[5],z)+(60//de)*bits[4]
 return 6*(w('source')*u3+w('fixedfloor:actual:1:3')*u2
   +sum(w(f'fixedfloor:actual:5:{q}') for q in (1,2,3))*u6
   +(w('fixedpair:actual:1:3')+w('fixedpair:actual:2:3'))*H)

def run(certificate='full_AB_extension.json',input_file='fixed_graph_priced.json',output='AB_projected_row.json'):
 start=time.time();cert=json.loads((HERE/certificate).read_text());L=cert['integer_row_weights']
 assert set(L)<=SUPPORTED and min(L.values())>0
 kap=360*L.get('cap:3',0);assert kap==cert['K_integer_coefficient']
 has_fixed_floor=any(name.startswith('fixedfloor:') for name in L)
 visible_key=lambda bits:(bits[0],sum(bits[:4]),sum(bits[:5])) if has_fixed_floor else (0,sum(bits[:4]),0)
 maxima={};argmax={};states=0
 for p in range(3):
  for d in range(7):
   cache=list(features(p,d));states+=len(cache)
   visible=sorted({visible_key(bits) for bits in product((0,1),repeat=6) if sum(bits[:2])==p})
   for actual in visible:
    value,hist=max((weighted_hidden(f,actual,L),hist) for hist,f in cache)
    maxima[p,*actual,d]=value;argmax[p,*actual,d]=hist
   print('audited p,d',p,d,'full histograms',len(cache),flush=True)
 rows=[];lookup={}
 for bits in product((0,1),repeat=6):
  c=constant(bits,L);p=sum(bits[:2]);pf=sum(bits[:4])
  for d in range(7):
   value=c+maxima[p,*visible_key(bits),d];key=(''.join(map(str,bits)),d);lookup[key]=value
   rows.append({'actual_bits':key[0],'d':d,'coefficient':value})
 # Independently recompute the 33-point upper bound and verify the saved
 # maxima exactly, without trusting them in construction.
 point=json.loads((HERE/input_file).read_text());upper=F(kap)*F(point['K'])
 newmax=[]
 for s in point['support']:
  value=lookup[s.get('actual_bits',s.get('bits'))[:6],s['d']];newmax.append(value);upper+=F(s['weight'])*value
 assert newmax==cert['per_fixed_type_integer_maxima']
 assert upper==F(cert['exact_upper_bound'])<0
 result={'exact_verified':True,'independent':True,'uses_optimizer':False,'uses_numpy':False,
 'family':'AB, prefix (A,B), branch (T_i,F_i,B_i,C_i)',
 'histograms_checked_per_background':54264,'background_loads':[0,1,2],
 'distinct_histogram_states_checked':states,'visible_conditional_states':len(maxima),
 'exact_fixed_point_upper_bound':str(upper),'K_integer_coefficient':kap,
 'projection':'For every six-player full-history pure SPE, sum_x gamma(actual_6_memberships(x),d(x)) + Kcoef*K >= 0',
 'source_certificate':certificate,'source_point':input_file,
 'why_no_offpath_bits':'All supported nonzero rows depend on fixed memberships only through actual A,...,F. Thus the 13-bit coefficient is independent of the seven offpath bits; their minimum is identical.',
 'row_scale':60,'integer_row_weights':L,'coefficients':rows,
 'conditional_histogram_argmax':[{'conditional_key':list(key),'hidden_maximum':maxima[key],'histogram_t0_then_t1':list(argmax[key])} for key in sorted(maxima)],
 'elapsed_seconds':time.time()-start,
 'scope':'A valid complete-domain six-player necessary projected row, plus exact separation of the supplied exact point; not a half theorem or SPE counterexample'}
 (HERE/output).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('coefficients','conditional_histogram_argmax','integer_row_weights')},indent=2),flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--certificate',default='full_AB_extension.json')
 parser.add_argument('--input',default='fixed_graph_priced.json')
 parser.add_argument('--output',default='AB_projected_row.json')
 args=parser.parse_args();run(args.certificate,args.input,args.output)
