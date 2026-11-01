import json
from fractions import Fraction
from pathlib import Path
p=Path(__file__).resolve(); E=p.parent; root=p.parents[7]
float_obj=json.loads((E/'original/crosscap_n4_k6.json').read_text())
exact=json.loads((root/'archives/customer-attraction/subarchives/six-providers/tools/evidence/full-terminal-crosscap-primary/original/research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/dual/crosscap_failure_exact.json').read_text())
act_float={tuple(a['history']):a['action'] for a in float_obj['actions']}
act_exact={tuple(a['history']):a['action'] for a in exact['actions']}
weights_exact={}
for item in exact['instance']['customers']:
    mask=sum(1<<a for a in item['topics'])
    weights_exact[str(mask)]=weights_exact.get(str(mask),0)+item['multiplicity']
weights_float={k:round(float(v)*245) for k,v in float_obj['weights'].items()}
result={
  'actions_equal': act_float==act_exact,
  'action_count_float': len(act_float),
  'action_count_exact': len(act_exact),
  'weights_after_rounding_to_245': weights_float,
  'weights_exact_multiplicity': weights_exact,
  'weights_equal_after_rounding': weights_float==weights_exact,
  'float_W_fraction': str(Fraction(float_obj['W']).limit_denominator(10000)),
  'float_gap_fraction': str(Fraction(float_obj['gap']).limit_denominator(10000)),
  'status': 'comparison-only;does-not-certify-floating-source'
}
(E/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
