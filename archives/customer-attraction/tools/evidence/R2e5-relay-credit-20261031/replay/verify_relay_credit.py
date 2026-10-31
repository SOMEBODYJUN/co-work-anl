from pathlib import Path
import hashlib, json

base=Path(__file__).resolve().parent.parent
src=base/'source'; rep=base/'replay'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
expected={
 'audit_full_depth_ledger.py':'dc30ee4ee359393b83f58cd702cc9f74521c6027d0a4464ed59c2f86e4fa877b',
 'full_depth_ledger_audit.json':'7abe44353c7fe29cd963ad5016da7bd209950a43a6320085c271e36ef43c615f',
 'workspace.json':'c8c53ec643368ed68a036f7a35c978fc3c17a0e17b1b32884e6f5d4c12733205',
}
for n,d in expected.items(): assert sha(src/n)==d
frozen=json.loads((src/'full_depth_ledger_audit.json').read_text())
generated=json.loads((rep/'generated.json').read_text())
assert frozen==generated
assert frozen['status']=='all_exact_checks_passed'
assert frozen['sharp_family_complete_SPE']['all_ordered_histories']==10213
assert frozen['sharp_family_complete_SPE']['all_action_comparisons']==60276
assert frozen['all_optimal_permutations']=={'m_min':2,'m_max':7,'count':5912}
assert frozen['variable_m_formulas']['m_max']==80
assert frozen['arbitrary_strategy_algebra']=={'instances':60,'edges':5678,'zero_client_instances':6,'empty_theme_in_every_instance':True,'SPE_claim':False}
ws=json.loads((src/'workspace.json').read_text())
assert set(ws)=={'schema','save','actor','instance'}
assert ws['save']=='customer-attraction'
print('PASS')
