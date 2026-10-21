"""Complete exact last-two best-response calculation in the materialized instance.
This does not compute all earlier subgames or certify a root SPE.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,contextlib,io,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('terminal_materialized',HERE/'audit_joint_terminal_materialization.py');m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(m)
labels=m.labels;idx=m.label_to_id
results=[]
for prefix,actual_action,actual_reply in [(['A','B','C'],'D','E'),(['A','E','U'],'V','W'),(['A','B','E'],'X','Y')]:
    matrix=[m.all_utilities(prefix+[a]) for a in labels]
    brs=[[b for b,v in enumerate(row) if v==max(row)] for row in matrix]
    floors=[min(matrix[b][a] for b in brs[a]) for a in range(65)]
    actual=matrix[idx[actual_reply]][idx[actual_action]]
    assert idx[actual_reply] in brs[idx[actual_action]]
    maximum=max(floors);best=[a for a,v in enumerate(floors) if v==maximum]
    results.append({'prefix':prefix,'actual_action':actual_action,'actual_reply':actual_reply,'actual_leader_utility_normalized':str(F(actual,60*m.W)),'can_complete_this_two_player_subgame':actual>=maximum,'maximum_guaranteed_deviation_normalized':str(F(maximum,60*m.W)),'guaranteed_profitable_deviations':[{'action':labels[a],'payoff_normalized':str(F(floors[a],60*m.W)),'all_last_best_replies':[labels[b] for b in brs[a]],'gain_normalized':str(F(floors[a]-actual,60*m.W))} for a in range(65) if floors[a]>actual],'all_floor_payoffs':{labels[a]:str(F(v,60*m.W)) for a,v in enumerate(floors)}})
report={'scope':'Only three actual last-two prefixes in one materialized finite instance; exact comparison against every one of 65 topics and every last best reply','all_three_can_complete':all(r['can_complete_this_two_player_subgame'] for r in results),'results':results}
HERE.joinpath('check_penultimate_completion.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({**report,'results':[{k:v for k,v in r.items() if k!='all_floor_payoffs'} for r in results]},indent=2))
