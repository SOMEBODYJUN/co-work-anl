from pathlib import Path
import hashlib, json
base = Path(__file__).resolve().parent
root = base.parent
src = root / 'source'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
expected = {
 'check_individual_coverage_floor.py':'9888c1b7f22e349680fac7274da3976560861029f05fb9c7114831fe55956ded',
 'individual_coverage_floor_test.json':'d9eb4520ec98feb3b14e86f20175107950f1c8c3d553472110504ca92b4a6336',
 'audit_background_plateau.py':'5e5fce759be6f0cb34e1fdc21b02f78621074060374041bbcb51d98ffe83bcf5',
 'background_plateau_independent_audit.json':'241b437bbae28f8a6c1f7be31f4acbae70d1c74ad31f5622845bc0ee5461bb33',
}
for name,digest in expected.items(): assert sha(src/name)==digest,name
coverage=json.loads((src/'individual_coverage_floor_test.json').read_text())
generated_coverage=json.loads((base/'coverage-floor/individual_coverage_floor_test.generated.json').read_text())
assert coverage==generated_coverage and len(coverage)==5
assert coverage[0]['lp_value']>0 and all(abs(row['lp_value'])<1e-12 for row in coverage[2:])
plateau=json.loads((src/'background_plateau_independent_audit.json').read_text())
generated_plateau=json.loads((base/'plateau/background_plateau_independent_audit.json').read_text())
assert plateau==generated_plateau
assert plateau['status']=='PASS' and plateau['main_states']==210 and plateau['main_histories']==259
assert [x['B'] for x in plateau['audits']]==[3,4,10]
assert [x['plateau_gap'] for x in plateau['audits']]==['1/60','1/84','1/312']
assert all(x['minimum_slack']=='0' and x['histories']==1464 and x['comparisons']==16104 for x in plateau['audits'])
print('PASS')
