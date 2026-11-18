"""Standalone exact replay of the 71/15 six-player proof certificate.

No discovery LP or original probe is imported. The mathematical validity of
F, H, R is proved in the accompanying theorem, not inferred from this script.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json


def audit():
    cert = json.loads(Path(__file__).with_name('certificate.json').read_text())
    tau = Q(cert['tau'])
    assert tau == Q(71, 15)
    den = cert['common_denominator']
    weights = {k: Q(v, den) for k, v in cert['integer_multipliers'].items()}
    assert weights and all(v > 0 for v in weights.values())
    residuals = []
    for word in product((0, 1), repeat=6):
        total = sum(word)
        pay = [Q(v, total) if total else Q(0) for v in word]
        for o in (0, 1):
            values = {}
            for i in range(6):
                past = sum(word[:i])
                values['F'+str(i+1)] = tau*pay[i]-Q(o, past+6-i)
                for j in range(6):
                    values[f'H{i+1}_{j+1}'] = pay[i]-Q(word[j], past+6-i)
            p, a = sum(word[:4]), word[4]
            values['R1/2'] = tau*pay[4]+pay[5]/2-Q(o, p+1)+Q(o*a*(p == 0), 4)
            assert not (set(weights)-set(values))
            remainder = Q(2*(total > 0)-o)-sum(weights[k]*values[k] for k in weights)
            assert remainder >= 0, (word, o, remainder)
            residuals.append({'e': list(word), 'o': o, 'remainder': str(remainder)})
    return {'claim_scope': 'complete 128-type rational certificate; not unrestricted six-player half',
            'tau': str(tau), 'type_count':len(residuals),
            'minimum_remainder':str(min(Q(x['remainder']) for x in residuals)),
            'zero_types':sum(Q(x['remainder']) == 0 for x in residuals),
            'minimum_positive_remainder':str(min(Q(x['remainder']) for x in residuals if Q(x['remainder']) > 0)),
            'weights':{k:str(v) for k,v in weights.items()}, 'residuals':residuals}


if __name__ == '__main__':
    result = audit()
    out = Path(__file__).with_name('exact-replay.json')
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'residuals','weights'}},ensure_ascii=False))
