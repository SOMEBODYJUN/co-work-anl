"""Hold supplied 53 weights fixed, weaken PAIR to ordinary two-profit bound.

This is a diagnostic for the supplied combination, not a row-cone lower bound.
The original proof package is only read; all diagnostic output goes to team/.
"""
import importlib.util
from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
PACKAGE = ROOT / 'customer_attraction/proofs/half5_exact_v1'
spec = importlib.util.spec_from_file_location('certificate', PACKAGE/'verify_certificate.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
original = audit.LiteralDomain.pair_feature

def weaker_pair(self,k,p,u,v,pattern):
    seen = getattr(self, '_overlap_ablation_seen', set())
    marker=(k,p,u,v,pattern)
    out=original(self,k,p,u,v,pattern)
    if marker not in seen:
        assert pattern=='query_equal'
        e=self.expanded[k]
        _,G,_=self.features[k,p]['_pair_primitives']
        # Existing PAIR has +g(T,Q). Ordinary profit tax has +2g(T,Q).
        extra=sum((e[:,j,u]*e[:,j,v]*G[:,i]
                   for i,j in product(range(5),repeat=2) if i!=j))
        key=f'pair:{u}{v}:{pattern}'
        self.features[k,p][key]=out+extra
        seen.add(marker)
        self._overlap_ablation_seen=seen
    return self.features[k,p][f'pair:{u}{v}:{pattern}']

audit.LiteralDomain.pair_feature=weaker_pair
sys.argv=['overlap_ablation', str(PACKAGE/'certificate.json'),
          '--manifest',str(PACKAGE/'row_manifest.json'),
          '--output',str(Path(__file__).with_name('overlap_ablation_report.json'))]
try:
    audit.main()
except AssertionError:
    import json
    report=json.loads((Path(__file__).with_name('overlap_ablation_report.json')).read_text())
    assert report['status']=='failed'
    print(json.dumps({'diagnostic':'fixed weights with weaker pair rows',
                      'negative_conditions':len(report['negative_cases']),
                      'minimum_scaled_integer_residual':report['minimum_scaled_integer_residual'],
                      'first_negative':report['negative_cases'][0]},indent=2))
else:
    raise AssertionError('Expected diagnostic weakening to break fixed certificate')
