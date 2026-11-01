#!/usr/bin/env python3
"""One independent Fraction audit of displayed data and an integer lift. No source import, AST extraction, NumPy/SciPy, MILP, BI or SPE solver."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import argparse,hashlib,json


def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def fp(path):
 b=path.read_bytes();return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args()
 args.output_dir.mkdir(parents=True,exist_ok=False)
 raw=json.loads(args.input.read_text(),parse_float=str)
 p=raw['parameters']['topics'];m=raw['parameters']['players'];assert (p,m)==(6,3)
 masks=list(range(1,1<<p));mass_cap=p*m
 # Independent definition: all multisets of m-1 different-from-query labels.
 menus=[(a,B) for a in range(p) for B in combinations_with_replacement(tuple(b for b in range(p) if b!=a),m-1)]
 selected={a:tuple(raw['witness'][str(a)]) for a in range(p)}
 selected_indices=[j for j,(a,B) in enumerate(menus) if selected[a]==B]
 assert len(selected_indices)==p
 z=[F(int(j in selected_indices)) for j in range(len(menus))]
 literal=[F(raw['weights'].get(str(mask),'0')) for mask in masks]
 lift=[F(3) if mask in [10,20,33] else F(0) for mask in masks]
 def column(player_action,profile,mask):
  interested=[bool(mask&(1<<action)) for action in profile]
  return F(1,sum(interested)) if mask&(1<<player_action) else F(0)
 def payoff_row(a,profile):return {j:column(a,profile,mask) for j,mask in enumerate(masks) if mask&(1<<a)}
 rows=[]
 def add(kind,meta,w,zpart,lower=None,upper=None):rows.append({'kind':kind,'meta':meta,'w':w,'z':zpart,'lower':lower,'upper':upper})
 for a in range(p):add('choose_one',{'a':a},{},{j:F(1) for j,(aa,B) in enumerate(menus) if aa==a},F(1),F(1))
 for j,(a,B) in enumerate(menus):
  profile=(a,)+B
  add('query_upper',{'menu':j,'a':a,'B':list(B)},payoff_row(a,profile),{j:F(mass_cap)},upper=F(1+mass_cap))
  for b in sorted(set(B)):
   add('follower_lower',{'menu':j,'a':a,'B':list(B),'b':b},payoff_row(b,profile),{j:F(-mass_cap)},lower=F(1-mass_cap))
 add('mass_cap',{},dict.fromkeys(range(len(masks)),F(1)),{},upper=F(mass_cap))
 assert len(rows)==247
 def evaluate(weights):
  values=[];violations=[]
  for i,row in enumerate(rows):
   value=sum((weights[j]*v for j,v in row['w'].items()),F(0))+sum((z[j]*v for j,v in row['z'].items()),F(0))
   slacks=[]
   if row['lower'] is not None:slacks.append(value-row['lower'])
   if row['upper'] is not None:slacks.append(row['upper']-value)
   smallest=min(slacks)
   values.append({'row':i,'value':str(value),'minimum_bound_slack':str(smallest)})
   if smallest<0:violations.append({'row':i,'kind':row['kind'],'meta':row['meta'],'minimum_bound_slack':str(smallest)})
  bounds=[v for x in weights for v in [x,mass_cap-x]]+[v for x in z for v in [x,1-x]]
  objective=sum((weights[j] for j,mask in enumerate(masks) if mask&((1<<m)-1)),F(0))
  return {'objective':str(objective),'mass':str(sum(weights,F(0))),'minimum_variable_bound_slack':str(min(bounds)),
          'row_count':len(values),'negative_rows':violations,'minimum_row_slack':str(min(F(v['minimum_bound_slack']) for v in values)),
          'row_values':values}
 literal_result=evaluate(literal);lift_result=evaluate(lift)
 assert lift_result['negative_rows']==[] and lift_result['objective']=='9' and lift_result['mass']=='9'
 assert len(literal_result['negative_rows'])==4
 # Distinct unit customers, not weighted atoms; direct selected-menu role payoffs.
 clients=[]
 for mask in [10,20,33]:
  for clone in range(3):clients.append((mask,clone))
 def unit_payoffs(profile):
  out=[F(0) for _ in profile]
  for mask,clone in clients:
   positions=[i for i,a in enumerate(profile) if mask&(1<<a)]
   for i in positions:out[i]+=F(1,len(positions))
  return out
 menu_checks=[]
 for a,B in selected.items():
  assert len(B)==m-1 and a not in B
  profile=(a,)+B;pay=unit_payoffs(profile);assert pay==[F(1)]*3
  other=next(b for b in range(p) if not ((1<<b)&next(mask for mask in [10,20,33] if mask&(1<<a))))
  deviated=profile[:-1]+(other,);devpay=unit_payoffs(deviated)[-1];assert devpay==3
  menu_checks.append({'a':a,'B':list(B),'profile':list(profile),'unit_role_payoffs':list(map(str,pay)),
                      'last_role_deviation':other,'deviated_profile':list(deviated),'deviation_payoff':str(devpay),'strict_gain':str(devpay-pay[-1])})
 coverage=[]
 for size in range(m+1):
  for support in combinations(range(p),size):
   value=sum(any(mask&(1<<a) for a in support) for mask,_ in clients)
   coverage.append({'support':list(support),'covered':value})
 assert len(coverage)==42 and max(x['covered'] for x in coverage)==9
 point={'weights':{str(mask):'3' for mask in [10,20,33]},'selected_binary_indices':selected_indices,'selected_menus':raw['witness'],
        'integer_unit_customers':[{'id':i,'topics':[a for a in range(p) if mask&(1<<a)]} for i,(mask,_) in enumerate(clients)]}
 matrix=[]
 for i,row in enumerate(rows):matrix.append({'row':i,'kind':row['kind'],'meta':row['meta'],'weight_coefficients':[[masks[j],str(v)] for j,v in row['w'].items()],
       'binary_coefficients':[[j,str(v)] for j,v in row['z'].items()],'lower':None if row['lower'] is None else str(row['lower']),'upper':None if row['upper'] is None else str(row['upper'])})
 save(args.output_dir/'coefficient-rows.json',{'construction':'Independent definition-level rational reconstruction, not extracted from original source or solver matrix.','shape':[len(rows),len(masks)+len(menus)],'weight_masks':masks,'menus':[{'index':j,'a':a,'B':list(B)} for j,(a,B) in enumerate(menus)],'rows':matrix})
 save(args.output_dir/'point-and-menus.json',{'point':point,'menus':menu_checks,'support_coverage':coverage})
 report={'status':'PASS','input':fp(args.input),'scope':'One new independent standard-library definition-level audit of a repaired integer point and the displayed decimal zero-filled candidate. No original/AST/helper/optimizer/BI/SPE calls.',
 'original_imports':0,'original_MILP_runs':0,'solver_calls':0,'canonical_SPE_calls':0,
 'parameters':{'topics':p,'players':m,'threshold':'1','mass_cap':mass_cap},
 'matrix':{'rows':len(rows),'columns':len(masks)+len(menus),'continuous_weights':len(masks),'binary_menu_variables':len(menus),
           'row_family_counts':{kind:sum(x['kind']==kind for x in rows) for kind in ['choose_one','query_upper','follower_lower','mass_cap']},
           'nonzero_coefficients':sum(len(x['w'])+len(x['z']) for x in rows)},
 'displayed_candidate':{'interpretation':'JSON decimal tokens as exact rationals, omitted weights set to zero, displayed selected binaries one and all others zero. This is not the unrecorded full HiGHS vector.',
                        'reported_value_token':raw['value'],'reported_dual_bound_token':raw['dual_bound'],
                        'reported_value_minus_displayed_objective':str(F(raw['value'])-F(literal_result['objective'])),**literal_result},
 'integer_repair':{'different_from_displayed_float_candidate':True,'point':point,**lift_result},
 'coverage':{'unit_customers':len(clients),'supports_enumerated':len(coverage),'OPT_3':9,'first_three_topic_coverage':9,'optimal_supports':[x['support'] for x in coverage if x['covered']==9]},
 'objective_upper_bound':'For each topic a, the exactly selected menu has u_a <= 1. Every interested customer has denominator at most m = 3, so topic_mass(a)/3 <= u_a <= 1. The fixed first-three-topic union is at most the sum of those three topic masses, hence objective <= 9. The independently verified integer point attains 9. The separate total mass cap is p*m = 18 and has slack 9 at this point; it is not the bound proving objective 9. This proves optimality only for the normalized noncredible-menu MILP, not a SPE statement.',
 'protected_floor_warning':{'query_payoff':'1','follower_payoffs':['1','1'],'query_strictly_below_normalized_floor':False,'OPT_over_2m':'3/2','followers_meet_OPT_over_2m':False},
 'credibility_warning':'In each selected menu the last follower can choose a different disjoint block and gain from 1 to 3; no selected menu is a true two-player continuation SPE.',
 'field_limits':'Original record lacks full x, residuals, exact certificate, MIP-gap/node log and library versions. Floating Optimal/value/dual_bound are preserved, not promoted to exact feasibility of the original full incumbent.'}
 save(args.output_dir/'exact-audit.json',report)
 print(json.dumps({'status':'PASS','matrix':report['matrix'],'selected_binary_indices':selected_indices,'displayed_negative_rows':literal_result['negative_rows'],'displayed_value_difference':report['displayed_candidate']['reported_value_minus_displayed_objective'],'exact_capped_optimum':9,'SPE_claim':False},ensure_ascii=False))


if __name__=='__main__':main()
