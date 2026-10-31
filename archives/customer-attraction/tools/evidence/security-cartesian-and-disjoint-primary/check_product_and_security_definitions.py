"""New stdlib exact definition check from the complete primary Markdown.

Not any missing author audit/policy JSON. The Cartesian policy is constructed
here from the proved menu completion. Four tiny rational LPs are solved by
explicit pure/two-point vertex enumeration, with finite scalar dual checks.
No numerical solver, canonical game implementation, or EF/ER code is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations,combinations_with_replacement
from functools import lru_cache
import json,hashlib
E=Path(__file__).resolve().parent;output=E/'new-product-and-security-check.json'
if output.exists():raise SystemExit('Definition entry already completed; do not rerun')
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [enc(y) for y in x]
 return x
def utilities(units,z):
 pay=[F(0)]*len(z);covered=0
 for likes in units:
  players=[i for i,a in enumerate(z) if a in likes]
  if players:
   covered+=1;v=F(1,len(players))
   for i in players:pay[i]+=v
 return tuple(pay),covered

masses=[0,0,5,9,5,4,7,9,6,3,8,9,1,6,0]
base=[frozenset(a for a in range(4) if mask>>a&1) for mask,n in enumerate(masses,1) for _ in range(n)]
assert len(base)==72
pay={z:utilities(base,z)[0] for z in product(range(4),repeat=3)}
L={(a,b):tuple(c for c in range(4) if pay[a,b,c][2]==max(pay[a,b,t][2] for t in range(4))) for a,b in product(range(4),repeat=2)}
phi={a:max(min(pay[a,b,c][1] for c in L[a,b]) for b in range(4)) for a in range(4)}
g={};g_details={}
for a in range(4):
 opts=[(b,c,pay[a,b,c][0],pay[a,b,c][1]) for b in range(4) for c in L[a,b]]
 vertices=[]
 for b,c,u,v in opts:
  if v>=phi[a]:vertices.append((u,((b,c,F(1)),)))
 for z,w in combinations(opts,2):
  b,c,u,v=z;bb,cc,uu,vv=w
  if (v-phi[a])*(vv-phi[a])<0:
   alpha=(phi[a]-vv)/(v-vv)
   vertices.append((alpha*u+(1-alpha)*uu,((b,c,alpha),(bb,cc,1-alpha))))
 best=min(vertices,key=lambda x:(x[0],len(x[1]),x[1]));g[a]=best[0]
 lambdas={F(0)}
 for z,w in combinations(opts,2):
  if z[3]!=w[3]:
   lam=(z[2]-w[2])/(z[3]-w[3])
   if lam>=0:lambdas.add(lam)
 duals=[(min(u-lam*(v-phi[a]) for b,c,u,v in opts),lam) for lam in lambdas]
 value,lam=max(duals,key=lambda x:(x[0],-x[1]));assert value==g[a]
 g_details[a]={'options':[{'b':b,'c':c,'u1':u,'u2':v} for b,c,u,v in opts],
  'primal_vertices_checked':len(vertices),'chosen_mixture':best[1],'g':g[a],
  'dual_lambda':lam,'dual_lower_slacks':[u-lam*(v-phi[a])-g[a] for b,c,u,v in opts]}
G1=max(min(pay[a,b,c][0] for b in range(4) for c in L[a,b] if pay[a,b,c][1]>=phi[a]) for a in range(4))
reported_mix={2:[(2,3,F(17,18)),(3,0,F(1,18))],3:[(2,3,F(17,24)),(3,2,F(7,24))]}
mix_checks=[]
for a,mu in reported_mix.items():
 assert all(c in L[a,b] for b,c,q in mu) and sum(q for b,c,q in mu)==1
 u=sum((q*pay[a,b,c][0] for b,c,q in mu),F(0));v=sum((q*pay[a,b,c][1] for b,c,q in mu),F(0))
 mix_checks.append({'a':a,'mixture':mu,'u1':u,'u2':v,'feasible':v>=phi[a],'optimal':u==g[a]})
 assert v>=phi[a] and u==g[a]
labels=list(product(range(4),repeat=2));index={z:i for i,z in enumerate(labels)}
menus={};minimums={}
for A in labels:
 menu=[];floor=sum(phi[a] for a in A)
 for B in labels:
  for C in product(*(L[a,b] for a,b in zip(A,B))):
   u=tuple(sum(pay[a,b,c][i] for a,b,c in zip(A,B,C)) for i in range(3))
   if u[1]>=floor:menu.append((u[0],B,C,u))
 assert menu
 menus[A]=menu;minimums[A]=min(menu,key=lambda z:(z[0],z[1],z[2]))
G2=max(z[0] for z in minimums.values())
actualA=(2,3);actualB=(3,2);actualC=(3,3)
chosen=next(z for z in menus[actualA] if z[1]==actualB and z[2]==actualC)
assert chosen[0]>=G2
actions={():index[actualA]}
for A in labels:
 row=chosen if A==actualA else minimums[A];Bstar,Cstar=row[1:3]
 actions[index[A],]=index[Bstar]
 for B in labels:
  C=Cstar if B==Bstar else tuple(min(L[a,b],key=lambda c:(pay[a,b,c][1],c)) for a,b in zip(A,B))
  actions[index[A],index[B]]=index[C]
jointunits=[]
for coord in range(2):
 for likes in base:jointunits.append(frozenset(i for i,z in enumerate(labels) if z[coord] in likes))
assert len(jointunits)==144
@lru_cache(None)
def jointpay(z):return utilities(jointunits,z)
def follow(h):
 while len(h)<3:h+=(actions[h],)
 return h
rows=[];comparisons=0
for h in [(),*((a,) for a in range(16)),*((a,b) for a,b in product(range(16),repeat=2))]:
 z=follow(h);u=jointpay(z)[0][len(h)];alts=[]
 for a in range(16):
  zz=follow(h+(a,));v=jointpay(zz)[0][len(h)];assert u>=v
  alts.append({'action':a,'terminal':zz,'payoff':v,'slack':u-v});comparisons+=1
 rows.append({'history':h,'chosen':actions[h],'terminal':z,'chosen_payoff':u,'alternatives':alts})
z=follow(());actualpay,W=jointpay(z)
alljoint=[(jointpay(zz)[1],zz) for zz in product(range(16),repeat=3)];OPT,opt_witness=max(alljoint)
cap_values=[pay[a,2,3][0] for a in range(4)];base_security_upper=max(cap_values)
cartesian={'unit_customers_base':72,'unit_customers_joint':144,'phi':[phi[a] for a in range(4)],
 'L':[{ 'a':a,'b':b,'last_best_replies':L[a,b]} for a,b in L],
 'base_payoffs':[{'triple':z,'utilities':u} for z,u in pay.items()],
 'g_details':g_details,'g':max(g.values()),'G1':G1,'G2':G2,'reported_mixture_checks':mix_checks,
 'all16_root_menu_minima':[{'A':A,'U1_min':t[0],'B':t[1],'C':t[2],'utilities':t[3]} for A,t in minimums.items()],
 'policy_origin':'Own construction using printed exact-menu sufficiency, notmissingoriginalJSONpolicy',
 'joint_labels':labels,'all273_policy_entries':[{'history':h,'action':a} for h,a in actions.items()],
 'all273_nodes_and4368_comparisons':rows,'nodes':len(rows),'including_self_comparisons':comparisons,
 'nonself_comparisons':comparisons-len(rows),'actual_joint_labels':z,'actual_component_actions':[labels[a] for a in z],
 'actual_utilities':actualpay,'W':W,'OPT':OPT,'OPT_witness':opt_witness,'half_slack':2*W-OPT,
 'base_static_upper_background':[2,3],'base_static_upper_all_query_values':cap_values,
 'base_v3_upper':base_security_upper,'joint_strong_aggregate_slack_lower':W-6*base_security_upper}
assert cartesian['phi']==[F(161,6),F(55,2),F(55,3),F(161,6)]
assert (G1,max(g.values()),G2)==(F(161,6),F(55,3),F(271,6))
assert actualpay==(F(146,3),F(146,3),F(110,3)) and W==134 and OPT==144 and comparisons==4368
assert W-6*base_security_upper>=0

# 36-unit-client gadget, exact original three-player rule, static screens.
gadget=[frozenset([a,b]) for a in range(3) for b in range(3,6)]
for X in combinations(range(3),2):
 for Y in combinations(range(3,6),2):gadget.extend([frozenset(X+Y)]*3)
assert len(gadget)==36
def oldaction(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 group=range(3) if h[1]<3 else range(3,6)
 return next(a for a in group if a not in h)
def oldfollow(h):
 while len(h)<3:h+=(oldaction(h),)
 return h
oldrows=[]
for h in [(),*((a,) for a in range(6)),*((a,b) for a,b in product(range(6),repeat=2))]:
 zz=oldfollow(h);u=utilities(gadget,zz)[0][len(h)];vals=[]
 for a in range(6):
  v=utilities(gadget,oldfollow(h+(a,)))[0][len(h)];assert u>=v;vals.append(v)
 oldrows.append({'history':h,'action':oldaction(h),'value':u,'all6_values':vals})
oldz=oldfollow(());up,oldW=utilities(gadget,oldz)
@lru_cache(None)
def query(a,bg):return sum((F(1,1+sum(b in likes for b in bg)) for likes in gadget if a in likes),F(0))
deletions=[oldz[:i]+oldz[i+1:] for i in range(3)]
deletion_values=[query(5,bg) for bg in deletions]
fractional=[sum((1/(1+F(2,3)*sum(a in likes for a in oldz)) for likes in gadget if q in likes),F(0)) for q in range(6)]
Q2=[p for grp in [range(3),range(3,6)] for p in combinations(grp,2)];Q3=[(0,1,2),(3,4,5)]
Q2values=[sum((query(a,bg) for bg in Q2),F(0))/6 for a in range(6)]
Q3values=[sum((query(a,bg) for bg in Q3),F(0))/2 for a in range(6)]
uniform2=[{'background':bg,'uniform_query_value':sum((query(a,bg) for a in range(6)),F(0))/6} for bg in combinations_with_replacement(range(6),2)]
assert oldz==(0,3,4) and up==(10,12,12) and oldW==34
assert deletion_values==[12]*3 and fractional==[F(43,5),F(373,35),F(373,35),F(65,7),F(65,7),F(397,35)]
assert Q2values==[10]*6 and Q3values==[F(15,2)]*6 and min(x['uniform_query_value'] for x in uniform2)==10
replications=[]
for K in range(1,6):
 vals=[F(0)]*(6*K);count=0;weight=F(1,K*6*2**(K-1))
 for J in range(K):
  other=[i for i in range(K) if i!=J]
  for pair in Q2:
   for choices in product(range(2),repeat=K-1):
    local={J:pair,**{i:Q3[c] for i,c in zip(other,choices)}}
    assert sum(len(x) for x in local.values())==3*K-1
    for i in range(K):
     for a in range(6):vals[6*i+a]+=weight*query(a,local[i])
    count+=1
 cap=F(15,2)+F(5,2*K);assert vals==[cap]*(6*K)
 replications.append({'K':K,'opponent_slots':3*K-1,'support_size':count,'cap':cap,'all_pure_query_values':vals,'conditional_W34percopy_slack_lower':34*K-3*K*cap})
lower_records=[]
for bg in combinations_with_replacement(range(12),5):
 locals=[tuple(a%6 for a in bg if a//6==i) for i in range(2)]
 value=sum((query(a,local) for local in locals for a in range(6)),F(0))/12
 lower_records.append({'background':bg,'uniform_query_value':value})
minimum=min(x['uniform_query_value'] for x in lower_records)
assert len(lower_records)==4368 and minimum==F(35,4)
gadget_result={'unit_customers':36,'original_rule_nodes':oldrows,'nodes':43,'including_self_comparisons':258,
 'nonself_comparisons':215,'actual':oldz,'utilities':up,'W':oldW,'deletion_backgrounds':deletions,'query5_values':deletion_values,
 'fractional_mean_load_query_values':fractional,'fractional_violation':max(fractional)-F(oldW,3),
 'Q2_query_values':Q2values,'Q3_query_values':Q3values,'uniform_query_all21backgrounds':uniform2,'v3_exact':10,
 'disjoint_static_K1_to5':replications,'two_copy_uniform_lower_all4368':lower_records,'two_copy_v6_exact':minimum,
 'sixplayer_fullSPE':'No reconstruction/newverification ofmissingdisjointauthorpolicy; static4368checks only'}
result={'status':'pass','new_definition_entry_runs':1,'original_entries':0,'external_solver_calls':0,
 'tiny_exact_LP_values_by_explicit_vertex_and_dual_enumeration':4,'timing_recorded':False,
 'cartesian':cartesian,'gadget_deletion_and_disjoint':gadget_result,
 'not_replayed':['missingauthor273nodeJSON','missingoriginaldisjointsixplayerpolicy','rootallSPEscan','finitePAIRfloatbatches','EF andERchecks'],
 'source_md_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (E/'original').rglob('*.md')},
 'scope':'Finite exact examples/menus; allKreplicationlimit andstaticdistribution proved analytically; nogeneralhalf/aggregate/PAIR theorem.'}
output.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':'pass','nodes':273,'IC_including_self':4368,'IC_nonself':4095,'G1':G1,'G2':G2,'g':max(g.values()),'phi':list(phi.values()),'g_by_first_action':g,'g_dual_lambda':{a:x['dual_lambda'] for a,x in g_details.items()},'actual_utilities':actualpay,'W':W,'OPT':OPT,'base_v3_upper':base_security_upper,'two_copy_v6':minimum,'old36IC':258,'fractional_violation':gadget_result['fractional_violation'],'new_entries':1,'original_entries':0,'external_solver_calls':0}),ensure_ascii=False))
