"""One explicit-unit-customer audit of the frozen k17 terminal table; no SPE DP."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import time

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
assert not args.output.exists()
clock=time.monotonic()
raw=args.source.read_bytes();source=json.loads(raw)
keys=['scope','k','pools','players','formal_path_welfare','formal_optimum','formal_half_violation','prefix',
      'last_action_values','all_last_best_replies','last_best_reply_payoff','deviator_payoff','proposed_payoff']
assert set(source)==set(keys) and len(source)==13
assert source['k']==source['pools']==17 and source['players']==20
k=q=17
catalog=['A','B','P']+[a+str(j) for j in range(q) for a in ['T','D','E']]
customers=[]
def add(likes,n):
    customers.extend(frozenset(likes) for _ in range(n))
add(['A'],4);add(['B'],4);add(['P'],5*k)
punishers=[a+str(j) for j in range(q) for a in ['D','E']]
add(['A']+punishers,6);add(['B']+punishers,2)
for j in range(q):
    add(['T'+str(j)],2)
    add(['T'+str(j),'D'+str(j)],2)
    add(['T'+str(j),'E'+str(j)],2)
assert len(catalog)==54 and len(customers)==203
topics={a:{i for i,b in enumerate(customers) if a in b} for a in catalog}
def payoff(actions,position):
    return sum((F(1,sum(i in topics[b] for b in actions)) for i in topics[actions[position]]),F())
def cover(actions):
    return len(set().union(*(topics[a] for a in actions)))
actual=['P']*k+['A','A','B']
prefix=['P']*k+['A']
assert len(actual)==20 and len(prefix)==18
rows=[]
for a in catalog:
    actions=prefix+['D0',a]
    rows.append(dict(last_action=a,last_payoff=str(payoff(actions,19)),deviator_payoff=str(payoff(actions,18))))
computed={r['last_action']:r['last_payoff'] for r in rows}
assert computed==source['last_action_values']
best=max(F(v) for v in computed.values())
replies=[a for a in catalog if F(computed[a])==best]
assert replies==source['all_last_best_replies'] and best==F(source['last_best_reply_payoff'])==6
deviator=[dict(last_action=r['last_action'],payoff=r['deviator_payoff']) for r in rows if r['last_action'] in replies]
assert len(deviator)==16 and all(F(r['payoff'])==7 for r in deviator)
proposed=payoff(actual,18)
assert proposed==source['proposed_payoff']==5 and source['deviator_payoff']==7
optimal_actions=['P','A','B']+['T'+str(j) for j in range(q)]
assert len(optimal_actions)==20 and cover(optimal_actions)==len(customers)==source['formal_optimum']==203
assert cover(actual)==source['formal_path_welfare']==101
assert source['formal_half_violation']==203-2*101==1
report=dict(status='PASS_EXACT_DIRECT_TERMINAL_TABLE',source_sha256=hashlib.sha256(raw).hexdigest(),source_bytes=len(raw),source_fields=keys,
            python=platform.python_version(),original_program_entries=0,DP_calls=0,LP_calls=0,independent_audit_entries=1,
            scope='A new explicit-unit-customer Fraction reconstruction of k17/q17 only; not a recovered historical producer or full-SPE audit.',
            k=k,pools=q,players=20,topics=catalog,unit_customers=len(customers),
            customers=[dict(id=i,likes=sorted(b)) for i,b in enumerate(customers)],
            proposed_path=actual,proposed_player_payoffs=[str(payoff(actual,i)) for i in range(20)],
            formal_path_welfare=101,formal_OPT=203,OPT_certificate=dict(actions=optimal_actions,covered=203,total_customers=203),
            formal_half_deficit=1,formal_ratio_OPT_over_W='203/101',
            prefix=prefix,forced_current_action='D0',last_reply_rows=rows,all_last_best_replies=replies,
            best_reply_payoff='6',deviator_payoffs_for_every_best_reply=deviator,proposed_current_payoff=str(proposed),strict_deviation_gain='2',
            compared_last_action_entries=54,compared_best_reply_entries=16,
            elapsed_seconds=time.monotonic()-clock,
            limits=['General k>=1,q>=2 result is proved analytically in the formal object, not extrapolated from this finite run.',
                    'No full game tree, all SPE outcomes, actual SPE optimum/minimum or historical argv is computed.',
                    'Only the specific path P^k AAB is refuted; this does not rule out all profiles with equal counts or all possible counterexamples.'])
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','unit_customers','players','compared_last_action_entries','compared_best_reply_entries','strict_deviation_gain','elapsed_seconds']}))
