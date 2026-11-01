"""Exact coverage identity for the captured trial, without any SPE computation."""
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
d = json.loads((HERE/'replay/capture.json').read_text())
w, r = d['weights'], d['result']
assert len(w) == 128 and w[0] == 0
assert all(type(x) is int and x >= 0 for x in w)
counts = r['root_min_count']
assert len(counts) == 7 and sum(counts) == 6
actual = [a for a, count in enumerate(counts) if count]


def coverage(support):
    return sum(value for mask, value in enumerate(w)
               if any(mask & (1 << a) for a in support))


comparisons = [{'support': list(s), 'coverage': coverage(s)}
               for s in combinations(range(7), 6)]
W = coverage(actual)
OPT = max(x['coverage'] for x in comparisons)
assert W == r['min_welfare'] == 95
assert OPT == r['optimum'] == 98 == sum(w)
assert all(coverage([a]) > 0 for a in range(7))
report = {'status': 'PASS', 'unit_clients': sum(w), 'topic_count': 7, 'players': 6,
          'positive_types': [{'mask': m, 'multiplicity': x} for m, x in enumerate(w) if x],
          'returned_count': counts, 'coverage_of_returned_count': W,
          'exact_static_optimum': OPT, 'all_seven_maximal_size_supports': comparisons,
          'source_ratio_is_floating': r['ratio'],
          'ratio_of_these_two_coverages': '95/98',
          'original_or_canonical_spe_calls': 0, 'lp_calls': 0,
          'scope': 'static coverage of the returned count, not SPE feasibility or minimum SPE welfare'}
(HERE/'replay/static-coverage-audit.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: report[k] for k in ['status', 'unit_clients',
                                      'coverage_of_returned_count', 'exact_static_optimum', 'scope']}))
