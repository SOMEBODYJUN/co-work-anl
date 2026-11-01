"""Reproducible form of the separately logged inline primitive-order check.
No root pricing entry or optimizer is called.
"""
from pathlib import Path
import json,sys
S=Path(__file__).resolve().parent
C=S.parent/'global_prices_runtime/research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible'
sys.path.insert(0,str(C));p=C/'root_menu_completion.py';src=p.read_text()
assert src.count('# Maximize a common margin')==1
env={'__file__':str(p)}
exec(compile(src.split('# Maximize a common margin')[0],'<original root primitives only>','exec'),env)
raw=json.loads((C/'root_full_hist_completion.json').read_text())
assert env['names']==raw['row_names'][:-16]
assert json.loads(json.dumps(env['spec']))==raw['row_specs'][:-16]
assert len(raw['dual_rows'])==len(env['A'])+16
assert len(raw['dual_equalities'])==len(env['old'])==38
print(json.dumps({'primitive_rows':len(env['A']),'primitive_variables':len(env['variables']),'per_index_groups':len(env['E']),'row_order_equal':True,'LP_calls':0}))
