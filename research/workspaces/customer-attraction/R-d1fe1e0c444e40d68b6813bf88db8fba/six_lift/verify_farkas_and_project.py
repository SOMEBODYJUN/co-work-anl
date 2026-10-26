"""Independent standard-library exact AB audit and complete visible projection.

Reconstructs only the ten nonzero raw row formulas, uses no discovery module,
NumPy, optimizer, or saved per-type maxima. Every d-compatible 16-bin
histogram is checked. Integer coefficients already include share scaling60.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,time
HERE=Path(__file__).resolve().parent
N=6

def compositions(n,k):
 if k==1:yield (n,);return
 for v in range(n+1):
  for rest in compositions(n-v,k-1):yield (v,)+rest

def share(n,d):return 60*n//d if n else 0

def primitives(p,t,f,b,c):
 z=p+t+f+b+c;D=60//(p+t+f+b+1);A=60//(p+t+f+1);G=60//((p+t+f+1)*(p+t+f+2))
 H=share(b,z)+share(c,z)+b*G
 return (f,b,c,f*c,b*c,share(t,z),share(c,z),D,f*D,b*D,A,f*A,b*A,c*A,G,f*G,b*G,b*c*G,H)

def features(p,d):
 # The two T-groups are histogrammed independently; concatenating these
 # histograms is bijective with the complete d-compatible 16-bin domain.
 pats=list(product((0,1),repeat=3));parts=[]
 for t,count in [(0,N-d),(1,d)]:
  prim=[primitives(p,t,*word) for word in pats];entries=[]
  for hist in compositions(count,8):
   feat=tuple(sum(h*pr[j] for h,pr in zip(hist,prim)) for j in range(19))
   entries.append((hist,feat))
  parts.append(entries)
 for (h0,x),(h1,y) in product(*parts):yield h0+h1,tuple(a+b for a,b in zip(x,y))

def weighted_hidden(f,pf,L):
 nf,nb,nc,nfc,nbc,st,sc,D,fD,bD,A,fA,bA,cA,G,fG,bG,bcG,H=f
 val=-L['source']*st-60*L['cap:3']*nc
 val+=L['fixedpair:actual:1:3']*(-(60//(pf+1))*(nf+nc)+(60//((pf+1)*(pf+2)))*nfc)
 val+=L['fixedpair:actual:2:3']*(-(60//(pf+1))*(nb+nc)+(60//((pf+1)*(pf+2)))*nbc)
 val+=L['floorfamily:3:1:off']*(5*sc-nf*D+fD)
 val+=L['floorfamily:3:2:off']*(5*sc-nb*D+bD)
 val+=L['floorfamily:3:3:all']*(6*sc-nc*D)
 val+=L['pairfamily:1:1:all_distinct']*(20*H-8*(nf*A-fA)+nf*(nf-1)*G-2*(nf-1)*fG)
 val+=L['pairfamily:2:2:all_distinct']*(20*H-8*(nb*A-bA)+nb*(nb-1)*G-2*(nb-1)*bG)
 val+=L['pairfamily:2:3:query_equal']*(5*H-(nb+nc)*A+bA+cA+nbc*G-bcG)
 return val

def constant(bits,L):
 z=sum(bits);u3=share(bits[2],z)
 pf=sum(bits[:4]);de=(pf+1)*(pf+2)
 H=share(bits[4],z)+share(bits[5],z)+(60//de)*bits[4]
 # raw source and fixed-PAIR rows sum over six optimum indices
 return 6*(L['source']*u3+(L['fixedpair:actual:1:3']+L['fixedpair:actual:2:3'])*H)

def run():
 start=time.time();cert=json.loads((HERE/'full_AB_extension.json').read_text());L=cert['integer_row_weights']
 assert len(L)==10 and min(L.values())>0
 kap=360*L['cap:3'];assert kap==cert['K_integer_coefficient']
 maxima={};argmax={};states=0
 for p in range(3):
  for d in range(7):
   cache=list(features(p,d));states+=len(cache)
   for pf in range(p,p+3):
    value,hist=max((weighted_hidden(f,pf,L),hist) for hist,f in cache)
    maxima[p,pf,d]=value;argmax[p,pf,d]=hist
   print('audited p,d',p,d,'full histograms',len(cache),flush=True)
 rows=[];lookup={}
 for bits in product((0,1),repeat=6):
  c=constant(bits,L);p=sum(bits[:2]);pf=sum(bits[:4])
  for d in range(7):
   value=c+maxima[p,pf,d];key=(''.join(map(str,bits)),d);lookup[key]=value
   rows.append({'actual_bits':key[0],'d':d,'coefficient':value})
 # Independently recompute the 33-point upper bound and verify the saved
 # maxima exactly, without trusting them in construction.
 point=json.loads((HERE/'fixed_graph_priced.json').read_text());upper=F(kap)*F(point['K'])
 newmax=[]
 for s in point['support']:
  value=lookup[s['bits'][:6],s['d']];newmax.append(value);upper+=F(s['weight'])*value
 assert newmax==cert['per_fixed_type_integer_maxima']
 assert upper==F(cert['exact_upper_bound'])<0
 result={'exact_verified':True,'independent':True,'uses_optimizer':False,'uses_numpy':False,
 'family':'AB, prefix (A,B), branch (T_i,F_i,B_i,C_i)',
 'histograms_checked_per_background':54264,'background_loads':[0,1,2],
 'distinct_histogram_states_checked':states,'visible_conditional_states':63,
 'exact_fixed_point_upper_bound':str(upper),'K_integer_coefficient':kap,
 'projection':'For every six-player full-history pure SPE, sum_x gamma(actual_6_memberships(x),d(x)) + Kcoef*K >= 0',
 'why_no_offpath_bits':'All ten nonzero rows depend on fixed memberships only through actual A,...,F. Thus the 13-bit coefficient is independent of the seven offpath bits; their minimum is identical.',
 'row_scale':60,'integer_row_weights':L,'coefficients':rows,
 'conditional_histogram_argmax':[{'prefix_load':p,'actual_first4_load':pf,'d':d,'hidden_maximum':maxima[p,pf,d],
  'histogram_t0_then_t1':list(argmax[p,pf,d])} for p,pf,d in sorted(maxima)],
 'elapsed_seconds':time.time()-start,
 'scope':'A valid complete-domain six-player necessary projected row, plus exact separation of the saved 3088-row fixed-query point; not a half theorem or SPE counterexample'}
 (HERE/'AB_projected_row.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('coefficients','conditional_histogram_argmax','integer_row_weights')},indent=2),flush=True)
if __name__=='__main__':run()
