"""Audit stored Fraction equalities only; never reconstruct payoffs, IC, a game, or an optimum."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys

def main():
 source=Path(sys.argv[1]);dest=Path(sys.argv[2]);raw=source.read_bytes();obj=json.loads(raw)
 counts={'budget_equalities':0,'output_products':0,'column_totals':0,'column_ratios':0,'report_flags':0}
 cases=[];max_ratio=F(-1);max_locations=[];positive_columns=zero_columns=stored_rows=lambda_gt_one=0
 for ri,report in enumerate(obj['reports']):
  profits=list(map(F,report['profits']));m=len(report['path'])
  assert len(profits)==m and len(report['columns'])==m
  ratios=[]
  for ci,column in enumerate(report['columns']):
   assert column['recipient_zero_based']==ci and F(column['profit_B'])==profits[ci]
   total=F(0);senders=set()
   for row in column['rows']:
    sender=row['sender_zero_based'];assert sender not in senders and 0<=sender<ci;senders.add(sender)
    parent=F(row['profit_B']);child=F(row['profit_W']);q=F(row['q_positive']);lam=F(row['lambda']);out=F(row['output'])
    assert parent==profits[sender] and lam>=0 and child>0 and q>=0
    assert lam*child==parent;counts['budget_equalities']+=1
    assert lam*q==out;counts['output_products']+=1
    total+=out;stored_rows+=1
    if lam>1:lambda_gt_one+=1
   assert total==F(column['total_positive']);counts['column_totals']+=1
   expected=total/profits[ci] if profits[ci] else F(0)
   if not profits[ci]:assert total==0
   ratio=F(column['column_ratio']);assert ratio==expected;counts['column_ratios']+=1;ratios.append(ratio)
   if total:positive_columns+=1
   else:zero_columns+=1
   loc={'report_index':ri,'source':report['source'],'recipient_zero_based':ci}
   if ratio>max_ratio:max_ratio=ratio;max_locations=[loc]
   elif ratio==max_ratio:max_locations.append(loc)
  assert report['violates_cap2']==any(x>2 for x in ratios);counts['report_flags']+=1
  cases.append({'report_index':ri,'source':report['source'],'path':report['path'],'profits':report['profits'],
    'reported_histories':report['verified_histories'],'reported_comparisons_including_self':report['verified_comparisons'],
    'column_ratios':[str(x) for x in ratios],'stored_sender_rows':sum(len(x['rows']) for x in report['columns']),
    'violates_cap2_flag':report['violates_cap2']})
 result={'status':'PASS','scope':'stored report lambda*child=parent, lambda*q=output, column sums/ratios and flags only; no source game/IC/maximality recomputation',
  'input_bytes':len(raw),'input_sha256':hashlib.sha256(raw).hexdigest(),'reports':len(cases),'columns':positive_columns+zero_columns,
  'positive_columns':positive_columns,'zero_columns':zero_columns,'stored_sender_rows':stored_rows,'lambda_gt_one_stored_rows':lambda_gt_one,
  'sum_reported_histories_not_replayed':sum(x['verified_histories'] for x in obj['reports']),
  'sum_reported_comparisons_not_replayed':sum(x['verified_comparisons'] for x in obj['reports']),
  'max_reported_column_ratio':str(max_ratio),'max_ratio_locations':max_locations,'all_report_flags_false':all(not x['violates_cap2'] for x in obj['reports']),
  'arithmetic_checks':counts,'case_readout':cases,'original_checker_entry_runs':0,'original_checker_imports':0,'SPE_or_IC_replays':0,'solver_or_LP_runs':0}
 s=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
 with dest.open('x') as f:f.write(s)
 sys.stdout.write(s)

if __name__=='__main__':main()
