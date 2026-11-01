"""One-shot exact static audit of the two n4/k6 saved reports.
Does not import/run Search, SPE DP, cone reconstruction, LP, or random search.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import Counter
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
if (ROOT/'original').exists(): ROOT=ROOT/'original'
SPECS={'transitive_n4_g3.json':'0c8b436ec4ef7e09d2cf9b9634d802b58bbc831bd63540554a7b2a85eb523d19','transitive_cones_n4_g3.json':'bde55b6c43cbcb95ce296b927b7ba876bbb07d7c171196c3085fbb7a0f6b782e'}
D={}
for name,sha in SPECS.items():
 p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
 D[name]=json.loads(p.read_text())
a=D['transitive_n4_g3.json'];b=D['transitive_cones_n4_g3.json']
classes=[(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3)]
assert a['classes']==b['classes']==list(map(list,classes))
assert set(a)=={'status','trials','elapsed','seed','classes','best','bank'}
assert set(b)=={'status','classes','results'} and len(a['bank'])==30 and len(b['results'])==10
masks=[tuple(i for i in range(6) if mask>>i&1) for mask in range(1,64)]
def label(T):return tuple(sorted((sum(i<3 for i in T),sum(i>=3 for i in T))))
sizes=[sum(label(T)==c for T in masks) for c in classes]
def counts(d):
 for labels in combinations_with_replacement(range(6),d):yield tuple(labels.count(i) for i in range(6))
backgrounds=list(counts(3))
def orbit(h):return tuple(sorted((tuple(sorted(h[:3],reverse=True)),tuple(sorted(h[3:],reverse=True)))))
orbits=sorted({orbit(h) for h in backgrounds})
coef={}
for key in orbits:
 h=key[0]+key[1]
 coef[key]=[sum(len(T)*(12//(1+sum(h[i] for i in T))) for T in masks if label(T)==c) for c in classes]
record_keys={'n','k','weights','min_welfare','value_numerator','value_denominator','gap_numerator','relative_gap','worst_counts','minimizing_backgrounds','query','orbit_weights'}
records=[('best',a['best'])]+[(f'bank/{j}',r) for j,r in enumerate(a['bank'])]+[(f'initial/{j}',r['initial']) for j,r in enumerate(b['results'])]
out=[]
for name,r in records:
 assert set(r)==record_keys and r['n']==4 and r['k']==6 and r['value_denominator']==72
 x=r['orbit_weights'];w=r['weights'];assert len(x)==8 and len(w)==63
 assert all(type(v) is int and v>=0 for v in x+w)
 assert w==[x[classes.index(label(T))] if label(T) in classes else 0 for T in masks]
 assert r['query']==[1/6]*6
 vals=[sum(wj*len(T)*(12//(1+sum(h[i] for i in T))) for T,wj in zip(masks,w)) for h in backgrounds]
 v=min(vals);mins=[list(h) for h,z in zip(backgrounds,vals) if z==v]
 assert r['value_numerator']==v and r['minimizing_backgrounds']==mins
 wc=r['worst_counts'];assert len({tuple(q) for q in wc})==len(wc)
 assert all(len(q)==6 and all(type(t) is int and t>=0 for t in q) and sum(q)==4 for q in wc)
 W=[sum(wj for T,wj in zip(masks,w) if any(q[i] for i in T)) for q in wc]
 assert all(z==r['min_welfare']==sum(w) for z in W)
 gap=72*r['min_welfare']-4*v;assert r['gap_numerator']==gap
 assert abs(r['relative_gap']-float(F(gap,4*v)))<1e-15
 out.append({'record':name,'orbit_weights':x,'customers':sum(w),'value_numerator':v,'value_denominator':72,'gap_numerator':gap,'minimum_background_orbits':[orbits.index(key) for key in orbits if sum(c*t for c,t in zip(coef[key],x))==v],'worst_counts_count':len(wc),'listed_worst_coverage_all_customers':True,'SPE_or_completeness_checked':False})
assert a['best']==a['bank'][0]
assert len({tuple(r['weights']) for r in a['bank']})==30
matches=[]
for j,r in enumerate(b['results']):
 assert set(r)=={'seed','n','k','status','states','rows','root','initial','orbit_weights','value','gap','min_margin'}
 assert r['seed']==j and r['n']==4 and r['k']==6 and r['states']==84
 assert r['rows']==(385 if j==0 else 367)
 assert r['root'] in r['initial']['worst_counts']
 assert r['status']=='Optimization terminated successfully. (HiGHS Status 7: Optimal)' and r['min_margin']==0.0
 assert all(abs(t)<=1e-15 for t in r['orbit_weights'][:-1]) and abs(r['orbit_weights'][-1]-1/6)<1e-15
 assert abs(r['value']-float(F(35,144)))<1e-15 and abs(r['gap']-float(F(1,36)))<1e-15
 matches.append({'cone_seed':j,'complete_matching_bank_indices':[i for i,s in enumerate(a['bank']) if s==r['initial']]})
# Independent rational reconstruction of the common dense point, not exact
# equality of the finite binary floats or a check of the missing policy cone.
wr=[F(1,6) if len(T)==5 else F(0) for T in masks]
rv=[sum(w*F(len(T),6*(1+sum(h[i] for i in T))) for T,w in zip(masks,wr)) for h in backgrounds]
assert min(rv)==F(35,144) and sum(wr)==1
report={'status':'PASS_EXACT_STATIC_RECORD_CHECK','scope':'all fields schema; exact input expansion, complete static background values/minimizer arrays, listed terminal coverage and arithmetic; rational common output reconstruction only; no SPE, cone IC, LP optimality or generation history check','source_sha256':SPECS,'classes':classes,'class_sizes':sizes,'background_count':len(backgrounds),'background_orbits':[{'index':i,'representative':key[0]+key[1],'size':sum(orbit(h)==key for h in backgrounds),'C_scaled_uniform_sum':coef[key]} for i,key in enumerate(orbits)],'all_41_record_checks':out,'cone_seed_bank_identity':matches,'common_rational_reconstruction':{'per_missing_label_type':'1/6','W':'1','v4':'35/144','W_minus_4v4':'1/36','relative_gap':'1/35','minimizing_background_count':sum(z==min(rv) for z in rv)},'original_program_entries_executed':0,'DP_LP_IC_random_search_runs':0,'python':sys.version.split()[0]}
print(json.dumps(report,ensure_ascii=False,indent=2))
