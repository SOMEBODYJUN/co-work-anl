"""Replay only the read original exact entries helper, never the 420 LP main.
This is a known-source arithmetic audit, not an independent implementation.
"""
import ast,json,sys,math
from pathlib import Path
from fractions import Fraction as F
from itertools import product

source,report,symbolic=map(Path,sys.argv[1:])
tree=ast.parse(source.read_text());nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='entries'];assert len(nodes)==1
namespace={'F':F,'product':product}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),namespace)
rows=json.loads(report.read_text());results=[]
assert len(rows)==420 and {(x['k'],x['l'])for x in rows}=={(k,l)for k in range(1,61)for l in range(2,9)}
for row in rows:
 if not row['success']:continue
 weights=list(map(F,row['multipliers']));assert len(weights)==7
 values=[(key,rhs-sum((a*b for a,b in zip(v,weights)),F(0)))for key,v,rhs in namespace['entries'](row['k'],row['l'])]
 assert len(values)==80
 worst=min(values,key=lambda z:z[1]);accepted=min(weights)>=0 and worst[1]>=0
 assert accepted==row['exact_rationalization']
 results.append(dict(k=row['k'],l=row['l'],source_report_exact=row['exact_rationalization'],all_seven_multipliers_nonnegative=min(weights)>=0,exact_corner_rows=80,minimum_margin=str(worst[1]),worst_membership=list(worst[0]),accepted_exact_certificate=accepted))
s=json.loads(symbolic.read_text());assert len(s['residuals'])==32
failed=[x for x in s['residuals']if not x['positivity']['all_coefficients_nonnegative']]
assert len(failed)==1 and failed[0]['membership']==[1,1,1,0,1]
poly=failed[0]['residual'];num=poly['numerator_l_ascending'];den=poly['denominator_l_ascending']
def shift(v,a):return [sum(F(v[i])*math.comb(i,h)*a**(i-h)for i in range(h,len(v)))for h in range(len(v))]
at3num=shift(num,3);at2den=shift(den,2)
assert at3num==list(map(F,[-376,-974,-688,-189,-18])) and all(x>0 for x in at2den)
at3=at3num[0]/sum(F(v)*3**i for i,v in enumerate(den));assert at3==F(-47,7930)
print(json.dumps(dict(scope='Known original entries helper replay only; no LP, numerical import or original main. Exact reported points and one failed symbolic class, not a bad SPE.',records_total=420,floating_success_records=len(results),floating_unsuccessful_records_without_exact_infeasibility_certificate=len(rows)-len(results),accepted_exact_pairs=sum(x['accepted_exact_certificate']for x in results),rejected_rationalizations=[x for x in results if not x['accepted_exact_certificate']],all_successful_record_checks=results,exact_corner_rows=80*len(results),original_entries_helper_evaluations=len(results),original_main_runs=0,new_LP_calls=0,symbolic_five_multipliers_positive=all(x['positivity']['all_coefficients_nonnegative']for x in s['multipliers'].values()),symbolic_positive_classes=31,symbolic_failed_class=failed[0]['membership'],failed_numerator_shift_l_equals_3_plus_u=list(map(str,at3num)),failed_denominator_shift_l_equals_2_plus_u=list(map(str,at2den)),failed_margin_at_l3=str(at3),failed_margin_strictly_negative_for_all_real_l_ge3=True),ensure_ascii=False,indent=2))
