"""Verify the saved discovery boundary after explicit rational reconstruction.

No random search, optimizer, canonical game implementation, or author audit is
imported. This is a new check of one saved numerical point, not its run history.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json


def main():
    root = Path(__file__).resolve().parent
    original = json.loads((root / 'original/occupied_saddle_face_probe.json').read_text())
    z = original['best']
    assert original['cases'] == 80 and original['candidate'] is None
    assert z['m'] == 4 and z['k'] == 5
    p = (F(0), F(0), F(0), F(1, 3), F(2, 3))
    weights = tuple(F(1) if mask == 8 else F(5) if mask == 19 else F(0)
                    for mask in range(1, 32))
    for observed, exact in zip(z['p'], p):
        assert abs(observed - float(exact)) < 1e-12
    for observed, exact in zip(z['weights'], weights):
        assert abs(observed - float(exact)) < 1e-12
    assert sum(p) == 1 and sum(weights) == 6
    assert z['counts'] == [0, 0, 0, 1, 3] and z['d'] == 3
    masks = tuple(range(1, 32))
    rows = []
    for history in combinations_with_replacement(range(5), 4):
        counts = tuple(history.count(a) for a in range(5))
        load = tuple(sum(counts[a] for a in range(5) if mask & (1 << a))
                     for mask in masks)
        query = tuple(sum((weight / (1 + c) for mask, weight, c
                           in zip(masks, weights, load) if mask & (1 << a)), F(0))
                      for a in range(5))
        value = sum((mass * gain for mass, gain in zip(p, query)), F(0))
        assert value >= 1
        rows.append((counts, query, value, load))
    assert len(rows) == z['full_backgrounds'] == 70
    assert len(z['Q']) == 70 and z['Q'][-1] == 1
    assert all(x == 0 for x in z['Q'][:-1])
    dual = rows[-1][1]
    assert dual == (F(1), F(1), F(0), F(1), F(1))
    assert max(dual) == 1
    selected = next(row for row in rows if row[0] == tuple(z['counts']))
    occupied = sum((weight / c for mask, weight, c in zip(masks, weights, selected[3])
                    if mask & (1 << z['d'])), F(0))
    assert selected[2] == occupied == 1
    active = [list(row[0]) for row in rows if row[2] == 1]
    assert len(active) == 25
    return {
        'status': 'PASS_EXACT_RATIONAL_RECONSTRUCTION_OF_ONE_SAVED_BOUNDARY',
        'scope': 'one explicit reconstructed point; no discovery or LP rerun, no SPE test',
        'source_float_reconstruction_tolerance': '1e-12',
        'static_competitors': 4,
        'topic_labels': 5,
        'unit_clients_after_rational_reconstruction': 6,
        'nonzero_interest_masks': {'8': '1', '19': '5'},
        'p': list(map(str, p)),
        'dual_pure_background': list(rows[-1][0]),
        'dual_pure_query_values': list(map(str, dual)),
        'backgrounds_checked': len(rows),
        'safe_value': '1',
        'selected_counts': z['counts'],
        'selected_occupant': z['d'],
        'occupied_payoff': str(occupied),
        'net_static_debt': '0',
        'original_active_backgrounds_field': z['active_backgrounds'],
        'original_field_semantics': 'seed matrix before reweighting',
        'reconstructed_active_background_count': len(active),
        'reconstructed_active_backgrounds': active,
        'duplicate_coverage_labels': [0, 1, 4],
        'empty_topic_label': 2,
        'sequential_SPE_claim': False,
    }


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
