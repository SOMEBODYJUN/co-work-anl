"""Read frozen arrays and independently audit coverage arithmetic only.

No original imports, equilibrium solver, history policy, LP or SPE check.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import hashlib,json
B=Path(__file__).resolve().parent
R=B/'original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample'
report=json.loads((R/'population_gadget_probe.json').read_text())
old=json.loads((R/'population_gadget_seed.json').read_text())['exact_candidate']['integer_clones']
interior=json.loads((R/'population_interior_seed.json').read_text())['exact_candidate']['integer_clones']
new=json.loads((R/'restricted_m5p7_population.json').read_text())['exact_candidate']['integer_clones']
for c in (old,new,interior):assert len(c)==127 and all(type(v)is int and v>=0 for v in c)
assert all(a==b+100*c for a,b,c in zip(interior,old,new))
assert [(i,v)for i,v in enumerate(old,1)if v]==[(1,12),(2,12),(3,4),(4,4),(5,8),(6,8),(8,9),(16,9),(32,9),(64,9)]
assert [(i,v)for i,v in enumerate(new,1)if v]==[(7,5),(16,1),(32,1),(72,1)]
def covered(c,support):
 selected=sum(1<<t for t in support)
 return sum(v for i,v in enumerate(c,1)if i&selected)
def optimum(c):
 return max(covered(c,s)for k in range(6)for s in combinations(range(7),k))
def inspect(c,q):
 assert len(q)==7 and all(type(x)is int and x>=0 for x in q)and sum(q)==5
 w=covered(c,[t for t,n in enumerate(q)if n]);o=optimum(c)
 return dict(customers=sum(c),nonzero_types=sum(v>0 for v in c),reported_root=q,root_coverage=w,optimum=o,OPT_over_root_coverage=str(Fraction(o,w)))
rows=[]
for row in report['rows']:
 t=row['private_multiplicity'];c=[0]*127
 for i,v in {1:12,2:12,3:4,4:4,5:8,6:8,8:t,16:t,32:t,64:t}.items():c[i-1]=v
 x=inspect(c,row['worst_root']);assert x['root_coverage']==row['worst_welfare'];assert x['optimum']==row['optimum'];assert x['OPT_over_root_coverage']==row['ratio']
 assert x['optimum']==max(48+2*t,44+3*t,24+4*t)
 rows.append({'private_multiplicity':t,**x})
mixed=[]
for row in report['finite_vertex_degeneracy_probe']:
 f=row['new_to_old_scale'];c=[a+f*b for a,b in zip(old,new)];x=inspect(c,[2,2,1,0,0,0,0])
 assert x['root_coverage']==48+5*f and x['optimum']==71+8*f and x['OPT_over_root_coverage']==row['ratio']
 mixed.append({'factor':f,**x,'equilibrium_reachability_and_counts':'retained as historical report; not checked here'})
inputs=[R/'population_gadget_probe.json',R/'population_gadget_seed.json',R/'population_interior_seed.json',R/'restricted_m5p7_population.json']
out={'scope':'independent exact integer coverage and vector-identity audit only; no equilibrium or history verification','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs},'vector_length':127,'old_seed':{'nonzero':[[i,v]for i,v in enumerate(old,1)if v],'total':sum(old)},'new_vertex':{'nonzero':[[i,v]for i,v in enumerate(new,1)if v],'total':sum(new)},'interior_seed':{'nonzero':[[i,v]for i,v in enumerate(interior,1)if v],'total':sum(interior),'equals_old_plus_100_new_all_127_coordinates':True},'original_twelve_rows':rows,'original_six_mixed_rows':mixed,'original_probe_runs':0,'canonical_solver_calls':0,'policy_IC_checks':0,'this_static_arithmetic_checker_runs':1,'status':'all array identities, displayed-root coverage, exact coverage optima and ratios matched'}
P=B/'static-clone-coverage-check.json'
with P.open('x') as stream:json.dump(out,stream,ensure_ascii=False,indent=2);stream.write('\n')
print(json.dumps({k:v for k,v in out.items()if k not in ['original_twelve_rows','original_six_mixed_rows','source_sha256']},ensure_ascii=False))
