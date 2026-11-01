from fractions import Fraction as F
import importlib.util, json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'source/audit_floor_relaxation.py'
frozen=ROOT/'source/floor_relaxation_audit.json'
spec=importlib.util.spec_from_file_location('floor_audit',src)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
result=mod.run()
assert result['terminal']==(0,0,0,1)
assert result['payoffs']==['5/4','5/4','5/4','9/4']
assert result['welfare']==6
assert result['robust_floors']==['1','1','5/4','9/4']
assert result['static_backgrounds_checked']==70
assert result['uniform_query_static_lower']=='8/5'
assert result['one_worst_background']==(0,1,2,3)
assert result['extra_one_aggregate_gap']=='2/5'
assert result['violated_node']==[0,0]
assert result['deviation']==2
assert result['true_last_best_replies']==[1,3,4]
assert result['deviating_player_payoff_under_every_best_reply']=='7/3'
assert result['penultimate_IC_violation']=='13/12'
raw=json.loads(frozen.read_text())
# JSON encodes Fraction fields as strings in the frozen report.
assert raw['status']==result['status']
assert raw['terminal']==list(result['terminal'])
assert raw['payoffs']==[str(x) for x in result['payoffs']]
assert raw['robust_floors']==[str(x) for x in result['robust_floors']]
assert raw['uniform_query_static_lower']==str(result['uniform_query_static_lower'])
assert raw['extra_one_aggregate_gap']==str(result['extra_one_aggregate_gap'])
assert raw['deviating_player_payoff_under_every_best_reply']==str(result['deviating_player_payoff_under_every_best_reply'])
assert raw['penultimate_IC_violation']==str(result['penultimate_IC_violation'])
print(json.dumps({'status':'PASS','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'frozen_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),'static_backgrounds_checked':70,'uniform_query_static_lower':'8/5','penultimate_IC_violation':'13/12'}))
