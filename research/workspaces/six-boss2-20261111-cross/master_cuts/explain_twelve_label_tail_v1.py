#!/usr/bin/env python3
"""Direct 12-action terminal calculation in the one frozen probe catalog.

No complete-menu recursion, no new input, and no optimizer is invoked.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ip=HERE/'full_history_probe_12label_v1.json'
    assert sha(ip)=='59e86b2961662aba4c9a9c9128fa03f2ee68b0b7c5bd7577896bc897838508f7'
    d=json.loads(ip.read_text());N=int(d['unit_customers']);types=[(r['mask'],int(r['integer_clones'])) for r in d['nonzero_customer_types']]
    def payoff(f,a):
        return sum((F(n,sum(f[j] for j in range(12) if mask&(1<<j)))
                    for mask,n in types if mask&(1<<a)),F())/N
    prefix=[1,1,1,1,0,0,1,0,0,0,0,0]
    last_values=[];current_values=[];terminals=[]
    for a in range(12):
        f=prefix[:];f[a]+=1;terminals.append(f)
        last_values.append(payoff(f,a));current_values.append(payoff(f,6))
    best=max(last_values);best_actions=[a for a,v in enumerate(last_values) if v==best]
    assert best_actions==[7,8,9,10,11]
    target=[1]*6+[0]*6;target_u5=payoff(target,4)
    assert all(current_values[a]==best for a in best_actions) and best>target_u5
    gap=best-target_u5
    frozen=json.loads((HERE/'full_history_probe_12label_v1_result.json').read_text())
    assert F(frozen['first_target_rejection_leaf_to_root']['strict_gap_normalized'])==gap
    out={'scope':'Direct terminal best replies after ordered prefix A1,A2,A3,A4,T1 in the one frozen catalog.',
         'input_sha256':sha(ip),'full_menu_result_sha256':sha(HERE/'full_history_probe_12label_v1_result.json'),
         'script_sha256':sha(Path(__file__)),'command':[sys.executable,'-B',str(Path(__file__).resolve())],
         'all_last_actions':[{'label':d['labels'][a],'terminal_counts':terminals[a],
              'last_player_payoff_normalized':str(v),'gap_to_best':str(best-v),
              'deviating_fifth_player_payoff_normalized':str(current_values[a])}
              for a,v in enumerate(last_values)],
         'exact_best_reply_labels':[d['labels'][a] for a in best_actions],
         'target_u5_normalized':str(target_u5),'deviation_minimum_normalized':str(best),
         'strict_gap_normalized':str(gap),
         'least_gap_excluding_best_replies':str(min(best-v for v in last_values if v<best)),
         'new_catalogs':0,'complete_menu_oracle_calls':0,'optimizer_calls':0}
    p=HERE/'twelve_label_tail_direct_v1.json'
    with p.open('x') as stream:stream.write(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(p),'sha256':sha(p),'best_replies':out['exact_best_reply_labels'],
        'strict_gap':str(gap),'least_excluded_gap':out['least_gap_excluding_best_replies']},ensure_ascii=False))


if __name__=='__main__':main()
