"""NEW stdlib definition check of the complete tables printed in primary MD.

Not the unavailable historical audit_abstract_menu.py, and no LP discovery.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import hashlib,json
E=Path(__file__).resolve().parent
source=E/'original/research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/abstract_menu_counterexample.md'
def key(s):return tuple(sorted(s))
f={key(x):F(2) for x in [(0,0,0),(0,0,1),(0,1,1),(1,1,1)]}
f.update({key(x):F(1) for x in [(0,0,2),(0,1,2),(0,2,2),(1,1,2),(1,2,2)]});f[(2,2,2)]=F(4)
g={key(x):F(1) for x in [(0,0),(0,1),(1,1),(2,2)]};g[(0,2)]=F(-2);g[(1,2)]=F(0)
assert set(f)==set(combinations_with_replacement(range(3),3)) and set(g)==set(combinations_with_replacement(range(3),2))
def u(a,H):return f[key((*H,a))]-g[key(H)]
def utilities(z):return tuple(u(z[i],z[:i]+z[i+1:]) for i in range(3))
actions={():1};actions.update({(a,):b for a,b in enumerate([2,2,1])})
last=[[1,1,2],[1,1,2],[1,0,2]]
actions.update({(a,b):last[a][b] for a,b in product(range(3),repeat=2)})
hs=[h for d in range(3) for h in product(range(3),repeat=d)]
assert set(actions)==set(hs) and len(actions)==13
def follow(h):
    while len(h)<3:h+= (actions[h],)
    return h
rows=[]
for h in hs:
    z=follow(h);own=utilities(z)[len(h)];alts=[]
    for b in range(3):
        zz=follow(h+(b,));value=utilities(zz)[len(h)];assert own>=value
        alts.append({'action':b,'terminal':zz,'utility':value,'margin':own-value})
    rows.append({'history':h,'chosen':actions[h],'terminal':z,'utility':own,'alternatives':alts})
allprofiles=[{'profile':z,'utilities':utilities(z)} for z in product(range(3),repeat=3)]
assert all(x>=0 for rec in allprofiles for x in rec['utilities'])
s=follow(());assert s==(1,2,2);W=sum(utilities(s));assert W==2
menus=[];forced=[]
for i in range(3):
    backgrounds=set();traces=[]
    for a in range(3):
        z=follow(s[:i]+(a,));B=key(z[:i]+z[i+1:]);backgrounds.add(B)
        traces.append({'action':a,'forced_terminal':z,'deleted_background':B})
    menus.append(tuple(sorted(backgrounds)));forced.append(traces)
M=tuple(sorted(set(B for menu in menus for B in menu)))
assert menus==[((0,1),(2,2)),((1,1),(1,2)),((1,2),)]
assert M==((0,1),(1,1),(1,2),(2,2))
Q={(1,1):F(3,4),(2,2):F(1,4)};p={0:F(3,4),2:F(1,4)}
assert sum(Q.values())==sum(p.values())==1
upper=[sum(q*u(a,B) for B,q in Q.items()) for a in range(3)]
lower=[sum(prob*u(a,B) for a,prob in p.items()) for B in M]
assert max(upper)==min(lower)==F(3,4)>W/3
menu_certificates=[]
for i,menu in enumerate(menus):
    q=({(0,1):F(3,4),(2,2):F(1,4)} if i==0 else {menu[0]:F(1)})
    pp=(p if i==0 else {0:F(1)})
    hi=[sum(prob*u(a,B) for B,prob in q.items()) for a in range(3)]
    lo=[sum(prob*u(a,B) for a,prob in pp.items()) for B in menu]
    assert max(hi)==min(lo)
    menu_certificates.append({'menu':menu,'background_distribution':[(B,v) for B,v in q.items()],
       'query_distribution':list(pp.items()),'all_upper_query_values':hi,'all_lower_background_values':lo,'exact_value':max(hi)})
assert sum(x['exact_value'] for x in menu_certificates)==F(11,4)
def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x
out={'status':'pass','new_entry_runs':1,'timing_recorded':False,'original_program_runs':0,'optimizer_calls':0,
 'primary_table_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'method':'manual transcription of complete MD F/G/action tables; exact definition check, no imported verifier/LP',
 'F':[(k,v) for k,v in sorted(f.items())],'G':[(k,v) for k,v in sorted(g.items())],
 'all_27_profiles':allprofiles,'query_matrix_background_order':list(combinations_with_replacement(range(3),2)),
 'query_matrix':[[u(a,B) for B in combinations_with_replacement(range(3),2)] for a in range(3)],
 'node_count':13,'including_self_comparisons':39,'nonself_comparisons':26,'all_node_comparisons':rows,
 'root_path':s,'root_utilities':utilities(s),'W_total_utility':W,'actual_node_forced_branches':forced,
 'actual_node_menus':menus,'union_menu':M,'union_background_distribution':list(Q.items()),
 'union_query_distribution':list(p.items()),'union_all_upper_query_values':upper,'union_all_lower_background_values':lower,
 'exact_union_cap':F(3,4),'W_over_m':W/3,'A_violation':F(1,12),'per_menu_certificates':menu_certificates,
 'sum_menu_values':F(11,4),'B_violation':F(3,4),'CAG_clone_necessary_condition_violation':{
  'a':2,'b':1,'one_other_action':2,'clone_value':u(2,(2,2)),'other_value':u(2,(2,1))},
 'CAG_instance_claimed':False,'half_counterexample_claimed':False}
(E/'textual-abstract-example-exact-check.json').write_text(json.dumps(enc(out),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({k:v for k,v in out.items() if k in ['status','new_entry_runs','original_program_runs','optimizer_calls','node_count','including_self_comparisons','nonself_comparisons','root_path','root_utilities','W_total_utility','exact_union_cap','W_over_m','A_violation','sum_menu_values','B_violation']})))
