#!/usr/bin/env python3
"""New finite arithmetic expansion of already-proved bank root-column formulas.
No game/strategy construction, controller import, SPE audit, search or optimizer.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
E=Path(__file__).resolve().parent;dest=E/'bank-two-query-exact.json';assert not dest.exists(),'one analytic expansion only'
base=E/'comparison/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md'
base_sha=hashlib.sha256(base.read_bytes()).hexdigest();assert base_sha=='e66e762af835f21575d7799a16937aee608e87706f75bebb3994cec1427562b0'
rows=[]
for m in (4,6):
 topics=list(product(range(m),range(m-1)))
 def kernel(T,A):
  t,b=T;a,j=A;f=1 if a==0 else 0
  economic=(m-1 if t==a else 1 if t==f else 0)
  bank=2 if b==j else 1
  return F(1,1+economic)+F(2,1+bank)
 P=[(1,0),(2,1)];cost=[sum((F(1,2)*kernel(T,A) for T in P),F()) for A in topics]
 u=F(1)+F(1,m-1);alpha=F(1,m)+F(2,3);target=F(4,3)+F(1,2*m)
 cp=sum((F(1,2)*cost[topics.index(A)] for A in P),F());diag=[kernel(A,A) for A in topics]
 assert kernel(P[0],P[1])==kernel(P[1],P[0])==2 and all(a==alpha<u for a in diag)
 assert cp==min(cost)==target and cp-u==F((2*m+1)*(m-3),6*m*(m-1))>0
 attainment=[A for A,v in zip(topics,cost) if v==target]
 assert attainment==[(a,b) for a in (1,2) for b in (0,1)]
 gdiag=u-alpha;goff=u-2;det=gdiag*gdiag-goff*goff
 assert det<0 and -det/(4-2*alpha)==cp-u
 Pfull=list(product(range(1,m),range(m-1)));prob=F(1,(m-1)**2)
 row_costs=[sum((prob*kernel(T,A) for T in Pfull),F()) for A in topics]
 column_caps=[sum((prob*kernel(T,A) for A in Pfull),F()) for T in topics]
 exact_menu=F(2)-F(1,m)-F(1,3*(m-1))
 assert min(row_costs)==max(column_caps)==exact_menu>cp
 rows.append({'players':m,'unit_customers':3*m-2,'topics':topics,'root_u':str(u),'query_support':P,'query_probabilities':['1/2','1/2'],'two_by_two':[[str(kernel(T,A)) for A in P] for T in P],'two_query_rows_all_root_columns':[[str(kernel(T,A)) for A in topics] for T in P],'fixed_p_cost_all_root_columns':list(map(str,cost)),'C_p':str(cp),'min_all_root_columns_fixed_p':str(min(cost)),'fixed_p_strict_gap':str(cp-u),'attaining_root_columns':attainment,'all_singleton_query_values':list(map(str,diag)),'singleton_slack':str(u-alpha),'pair_gap_matrix_diagonal':str(gdiag),'pair_gap_matrix_off_diagonal':str(goff),'pair_gap_matrix_determinant':str(det),'p_is_symmetric_NE':False,'profitable_meta_query':[3,2],'profitable_meta_query_value':str(sum((F(1,2)*kernel((3,2),A) for A in P),F())),'full_menu_matching_laws':{'support':Pfull,'each_probability':str(prob),'row_law_cost_all_columns':list(map(str,row_costs)),'column_law_value_all_queries':list(map(str,column_caps)),'exact_full_menu_minimax':str(exact_menu),'different_from_fixed_p_value':True},'actual_W':2*m,'OPT':3*m-2,'half_slack':m+2})
result={'status':'pass','new_analytic_expansion_calls':1,'case_parameters':[4,6],'original_frozen_program_calls':0,'bank_controller_or_SPE_calls':0,'optimizer_or_Nash_solver_calls':0,'proof_source_canonical_snapshot':str(base.relative_to(E)),'proof_source_sha256':base_sha,'proof_reuse_scope':'parent confirms already-pushed complete bank SPE/root-column formulas; current arithmetic expands exactly those formulas, does not reverify the controller','cases':rows,'general_formulas':{'fixed_two_query_C_and_min_all_columns':'4/3+1/(2m)','fixed_two_query_gap':'(2m+1)(m-3)/(6m(m-1))','fixed_two_query_attainment':'root econ 1 or2 and bank0 or1','singleton_query_value':'1/m+2/3','all_singleton_slack':'1/3+1/(m(m-1))','exact_full_menu_minimax':'2-1/m-1/(3(m-1))','full_menu_minus_fixed_pair':'(4m-3)(m-3)/(6m(m-1))'},'not_claimed':'new game or novelty, all-position U/half counterexample, symmetricNE for the two-query p'}
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'pass','proof_source_sha256':base_sha,'cases':[{'m':a['players'],'C_p':a['C_p'],'min_columns':a['min_all_root_columns_fixed_p'],'u':a['root_u'],'gap':a['fixed_p_strict_gap'],'full_menu':a['full_menu_matching_laws']['exact_full_menu_minimax']} for a in rows]},ensure_ascii=False))
