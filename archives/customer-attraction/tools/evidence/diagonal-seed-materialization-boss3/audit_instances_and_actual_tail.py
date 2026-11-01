"""Exact unit-type contracts and only the prescribed prefix's last-two subgame.

No six-player root backward induction, strategy search, LP, or original package imports.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json,sys


def audit(path,meta):
    data=json.loads(path.read_text());assert set(data)=={'topics','customers','players'} and data['players']==6
    labels=data['topics'];n=len(labels);assert n==18 and len(set(labels))==n
    types=[];seen=set();multiplicities=[]
    for row in data['customers']:
        assert set(row)=={'topics','multiplicity'};qs=row['topics'];v=row['multiplicity']
        assert isinstance(v,int) and not isinstance(v,bool) and v>0
        assert qs==sorted(set(qs)) and all(isinstance(j,int) and 0<=j<n for j in qs)
        mask=sum(1<<j for j in qs);assert mask not in seen;seen.add(mask);types.append((mask,v));multiplicities.append(v)
        assert sum(6<=j<12 for j in qs)==1
    assert gcd(*multiplicities)==1
    columns=[tuple(int(mask>>i&1) for mask,v in types) for i in range(n)];assert len(set(columns))==n
    total=sum(multiplicities);actual=tuple(meta['actual_path']);comparison=tuple(meta['comparison_T_path'])
    def welfare(profile):return sum(v for mask,v in types if any(mask>>a&1 for a in profile))
    def payoff(profile,i):
        return sum((F(v,sum((mask>>a)&1 for a in profile)) for mask,v in types if (mask>>profile[i])&1),F())
    actualW=welfare(actual);assert actualW==F(meta['actual_W']) and welfare(comparison)==total==F(meta['comparison_union'])
    prefix=actual[:4];table=[];branches=[]
    for a in range(n):
        entries=[]
        for b in range(n):
            profile=prefix+(a,b);entries.append((payoff(profile,4),payoff(profile,5)))
            table.append({'fifth':a,'sixth':b,'fifth_profit':str(entries[-1][0]),'sixth_profit':str(entries[-1][1])})
        best=max(z[1] for z in entries);br=[b for b,z in enumerate(entries) if z[1]==best]
        low=min(entries[b][0] for b in br);high=max(entries[b][0] for b in br)
        branches.append({'fifth':a,'fifth_topic':labels[a],'sixth_best_responses':br,'sixth_best_profit':str(best),'fifth_min_over_true_last_BR':str(low),'fifth_max_over_true_last_BR':str(high)})
    actual_u5=payoff(actual,4);actual_u6=payoff(actual,5);floor=max(F(b['fifth_min_over_true_last_BR']) for b in branches)
    actual_last_is_BR=actual[5] in branches[actual[4]]['sixth_best_responses']
    violations=[b for b in branches if F(b['fifth_min_over_true_last_BR'])>actual_u5]
    tail_possible=actual_last_is_BR and not violations
    return {'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'players':6,'topics':n,'customer_types':len(types),'unit_customer_count':str(total),'multiplicity_gcd':1,'all_18_coverage_columns_distinct':True,'empty_topics':[i for i,c in enumerate(columns) if not any(c)],'each_customer_in_exactly_one_T_topic':True,'OPT6_exact':str(total),'actual_profile':list(actual),'actual_welfare':str(actualW),'actual_coverage_ratio':str(F(actualW,total)),'profile_is_game_SPE':False if not tail_possible else 'not determined by a last-two-node audit','tail_prefix':list(prefix),'actual_u5':str(actual_u5),'actual_u6':str(actual_u6),'actual_last_action_is_best_response':actual_last_is_BR,'last_two_credible_fifth_floor':str(floor),'actual_tail_can_extend_to_a_pure_SPE_of_this_tail':tail_possible,'strict_deviation_rows':violations,'all_18_fifth_branches':branches,'all_324_terminal_payoff_pairs':table,'scope':'One fixed actual-prefix last-two subgame, all 18 actions and every last-player tie kept; no full six-player root SPE enumeration.'}


def main():
    if len(sys.argv)!=2:raise SystemExit('usage: audit_instances_and_actual_tail.py EVIDENCE_DIRECTORY')
    ev=Path(sys.argv[1]);results={}
    for kind in ['Rdiag','Zdiag']:
        meta=json.loads((ev/'replay'/f'seed18_{kind}_meta.json').read_text());out=audit(ev/'original'/f'seed18_{kind}.json',meta);results[kind]=out
    dest=ev/'replay/instance-and-actual-tail-audit.json'
    with dest.open('x') as f:json.dump(results,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({kind:{k:v for k,v in out.items() if k not in ['all_324_terminal_payoff_pairs','all_18_fifth_branches','strict_deviation_rows']}|{'strict_deviation_topics':[r['fifth_topic'] for r in out['strict_deviation_rows']]} for kind,out in results.items()},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
