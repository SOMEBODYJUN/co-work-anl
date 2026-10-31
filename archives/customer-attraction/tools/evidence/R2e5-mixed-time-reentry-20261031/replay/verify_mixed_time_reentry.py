from pathlib import Path
import hashlib, json
base = Path(__file__).resolve().parent.parent
src, rep = base/'source', base/'replay'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src/'audit_reentry.json') == '710c251f8c8cb5ee26478823319d3aeee88251841ceae2bd2ce9eeac6df6605a'
assert sha(src/'audit_reentry.py') == 'f3c98c975a59e4d731ef279c66d63e8f53cabaea169beafb9b7c349c939ddafe'
a=json.loads((src/'audit_reentry.json').read_text()); b=json.loads((rep/'generated.json').read_text())
assert a == b
assert a['customers'] == [3,4,7]
assert a['SPE_checks'] == [
 {'decision_histories':3,'all_action_comparisons':6,'minimum_slack':'0'},
 {'decision_histories':3,'all_action_comparisons':6,'minimum_slack':'0'},
 {'decision_histories':5,'all_action_comparisons':20,'minimum_slack':'0'}]
assert a['fixed_pure_query_single_reentry_vectors'] == [['2/3','1'],['1','2/3'],['5/3','5/3']]
assert a['sum_component_best_times']=='4/3' and a['product_synchronized_best_time']=='5/3' and a['product_two_reentries']=='4/3'
assert a['endpoint_nesting_checks']==27 and a['product_identity_checks']==16 and a['all_checks_passed'] is True
print('PASS')
