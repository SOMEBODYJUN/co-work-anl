#!/usr/bin/env python3
"""One fixed unit-client check of saved partial rows; not an SPE search."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import lcm
import argparse,json,hashlib

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--profiles',type=Path,required=True);a=ap.parse_args();raw=a.input.read_bytes();doc=json.loads(raw);r=doc['best'][0]
 assert doc['players']==5 and doc['topics']==7 and doc['J']==list(range(5)) and r['step']==0
 masses={int(k):F(v) for k,v in r['masses'].items()};scale=lcm(*(v.denominator for v in masses.values()));weights={mask:int(v*scale) for mask,v in masses.items()};assert scale==5 and weights=={66:1,68:1,121:5}
 clients=[mask for mask,v in weights.items() for _ in range(v)];actions={tuple(row['h']):row['a'] for row in r['actions']};assert len(actions)==len(r['actions'])==2801
 assert set(actions)=={h for d in range(5) for h in product(range(7),repeat=d)} and all(0<=t<7 for t in actions.values())
 @lru_cache(None)
 def finish(h):
  if len(h)==5:return h
  return finish(h+(actions[h],))
 @lru_cache(None)
 def payoff(z):
  result=[F(0)]*5
  for mask in clients:
   hit=[j for j,t in enumerate(z) if mask&(1<<t)]
   for j in hit:result[j]+=F(1,len(hit))
  return result
 def cover(z):return sum(any(mask&(1<<t) for t in z) for mask in clients)
 J=set(doc['J']);kept=omitted=kept_self=omitted_self=kept_strict=omitted_strict_positive=omitted_ties=0;neg=[];minimum=None;root_table=[];lines=[];bylabel=[{'comparisons':0,'negative':0} for _ in range(7)]
 for original in r['actions']:
  h=tuple(original['h']);chosen=actions[h];u=payoff(finish(h))[len(h)];values=[];gaps=[]
  for t in range(7):
   z=finish(h+(t,));v=payoff(z)[len(h)];gap=u-v;values.append(str(v));gaps.append(str(gap));bylabel[t]['comparisons']+=1;bylabel[t]['negative']+=gap<0
   minimum=gap if minimum is None else min(minimum,gap)
   if t in J:
    kept+=1;kept_self+=t==chosen;kept_strict+=gap>0;assert gap>=0
   else:
    omitted+=1;omitted_self+=t==chosen
    if gap<0:neg.append([list(h),t,str(gap/scale)])
    elif gap>0:omitted_strict_positive+=1
    else:omitted_ties+=1
   if not h:root_table.append({'action':t,'leaf':list(z),'root_payoff_integer':str(v),'root_payoff_normalized':str(v/scale),'IC_gap_integer':str(gap),'IC_gap_normalized':str(gap/scale)})
  lines.append(json.dumps({'history':list(h),'action':chosen,'chosen_payoff_integer':str(u),'all_action_payoffs_integer':values,'all_IC_slacks_integer':gaps},separators=(',',':')))
 assert kept==r['audit']['kept_comparisons']==14005 and len(neg)==r['audit']['omitted_negative_count']==2089
 assert neg[:12]==r['audit']['negative_examples']
 actual=finish(());W=cover(actual);target=tuple(doc['J']);target_coverage=cover(target);assert actual==(0,0,3,4,4) and W==5 and target_coverage==len(clients)==7
 assert F(target_coverage,scale)==F(r['value'])==F(7,5)
 assert root_table[6]['IC_gap_integer']=='-1' and payoff(actual)==[F(1)]*5
 a.profiles.write_text('\n'.join(lines)+'\n')
 out={'status':'passed_partial_rows_with_profitable_omissions_not_SPE','scope':'Only frozen step0 exact7-unit clone and full2801-history literal strategy, no original source import/BI/LP/discovery.','input_sha256':hashlib.sha256(raw).hexdigest(),'players':5,'labels':7,'J':doc['J'],'normalized_masses':r['masses'],'integer_scale':scale,'integer_weights':{str(k):v for k,v in weights.items()},'unit_clients':len(clients),'complete_ordered_decision_histories':len(actions),'full_catalog_comparisons_including_self':19607,'full_catalog_self':2801,'full_catalog_proper':16806,'kept_J_comparisons':kept,'kept_J_self':kept_self,'kept_J_proper':kept-kept_self,'kept_J_strict':kept_strict,'kept_J_ties':kept-kept_strict,'omitted_comparisons':omitted,'omitted_self':omitted_self,'omitted_proper':omitted-omitted_self,'omitted_negative':len(neg),'omitted_strict_positive':omitted_strict_positive,'omitted_ties':omitted_ties,'all_negative_count':len(neg),'minimum_full_catalog_IC_slack_integer':str(minimum),'first12_negative_examples_normalized':neg[:12],'counts_by_queried_label':bylabel,'actual':list(actual),'actual_integer_payoffs':list(map(str,payoff(actual))),'actual_W_integer':W,'actual_W_normalized':str(F(W,scale)),'J_coverage_integer':target_coverage,'J_coverage_normalized':str(F(target_coverage,scale)),'OPT_integer':7,'OPT_proof':'J covers all7unit customers, upper bound7; union label6 also coversall.','half_margin_2W_minus_OPT':2*W-target_coverage,'root_all_action_table':root_table,'is_full_pure_SPE':False,'profiles_path':str(a.profiles),'profiles_rows':len(lines),'profiles_sha256':hashlib.sha256(a.profiles.read_bytes()).hexdigest()}
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
