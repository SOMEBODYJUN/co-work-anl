"""Exact forty-pair certificate: optimal two-tail potential is not submodular.

No strategy or equilibrium assertion is made.  All four ordered prefix types
have depth 1, 2, or 3 and are legal in the original five-provider game.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json

def main():
    # Distinct unit clients: L={0,...,5}, R={6,...,11}, Z={12,...,20}.
    themes = (set(range(6)), set(range(6,12)), set(range(12)), set(range(12,21)))
    labels = ('A','B','C','D')
    H = [F()]
    for n in range(1,6):
        H.append(H[-1]+F(1,n))
    def potential(profile):
        return sum((H[sum(x in themes[a] for a in profile)] for x in range(21)),F())
    prefixes = {'q':(3,), 'q+A':(3,0), 'q+B':(3,1), 'q+A+B':(3,0,1)}
    reports = {}
    for name, q in prefixes.items():
        values = [(pair,potential(q+pair)) for pair in combinations_with_replacement(range(4),2)]
        maximum = max(v for pair,v in values)
        reports[name] = {
            'ordered_prefix': [labels[a] for a in q], 'prefix_depth': len(q),
            'M2': str(maximum),
            'maximizing_pairs': [[labels[a] for a in pair] for pair,v in values if v==maximum],
            'all_pair_potentials': [{'pair':[labels[a] for a in pair],'potential':str(v)} for pair,v in values],
        }
    gap = F(reports['q+A']['M2'])+F(reports['q+B']['M2'])-F(reports['q']['M2'])-F(reports['q+A+B']['M2'])
    assert gap == -F(1,2)
    out = {'claim':'The legal two-tail potential envelope M2 need not be submodular.',
           'scope':__doc__, 'unit_clients':21,
           'themes':{label:sorted(t) for label,t in zip(labels,themes)},
           'pair_evaluations':40,'submodularity_gap':str(gap),'prefixes':reports}
    Path(__file__).with_name('m2_non_submodular_exact.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'M2':{k:v['M2'] for k,v in reports.items()},'submodularity_gap':str(gap),'pair_evaluations':40},indent=2))

if __name__=='__main__':main()
