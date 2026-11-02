"""Verify only the saved rational matrix-game witnesses, without LP or SPE calls."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import time


def check(source: Path) -> dict:
    raw = source.read_bytes()
    records = json.loads(raw)
    reviewed = []
    cells = 0
    for item in records:
        matrix = [[F(x) for x in row] for row in item['matrix']]
        query = list(map(F, item['query']))
        deletion = list(map(F, item['deletion']))
        counts = item['counts']
        support = [i for i, c in enumerate(counts) if c]
        assert item['support'] == support
        assert all(isinstance(c, int) and c >= 0 for c in counts)
        assert sum(counts) == item['m']
        assert len(matrix) == len(counts) == len(query)
        assert all(len(row) == len(support) == len(deletion) for row in matrix)
        assert Counter(item['path']) == Counter({i: c for i, c in enumerate(counts) if c})
        assert all(x >= 0 for x in query + deletion)
        assert sum(query, F()) == sum(deletion, F()) == 1
        assert all(x >= 0 for row in matrix for x in row)
        rows = [sum((x * y for x, y in zip(row, deletion)), F()) for row in matrix]
        cols = [sum((query[i] * matrix[i][j] for i in range(len(matrix))), F())
                for j in range(len(support))]
        lower, upper = min(cols), max(rows)
        assert str(lower) == item['lower'] and str(upper) == item['upper']
        assert lower == upper
        threshold = F(2 * item['W'], 2 * item['m'] - 1)
        assert str(threshold) == item['threshold']
        assert item['strict_failure'] is (lower > threshold)
        assert item['verified'] is True
        cells += sum(map(len, matrix))
        reviewed.append({
            'example': item['example'], 'rows': len(matrix), 'columns': len(support),
            'value': str(lower), 'threshold': str(threshold),
            'threshold_minus_value': str(threshold - lower),
            'row_prices_under_saved_deletion': list(map(str, rows)),
            'column_payoffs_under_saved_query': list(map(str, cols)),
            'nonnegative_row_slacks': [str(upper - x) for x in rows],
            'nonnegative_column_slacks': [str(x - lower) for x in cols],
            'query': item['query'], 'deletion': item['deletion'],
            'strict_failure': lower > threshold,
            'historical_verified_field_not_reverified': item['verified'],
        })
    return {
        'scope': 'Saved rational matrices and saved rational probability witnesses only; no source-customer reconstruction, no SPE or LP calls.',
        'input_sha256': hashlib.sha256(raw).hexdigest(),
        'records': len(records), 'matrix_entries_read': cells,
        'all_matching_saddle_values_exact': True,
        'strict_failures': sum(x['strict_failure'] for x in reviewed),
        'current_original_probe_runs': 0, 'current_SPE_checks': 0,
        'current_LP_runs': 0, 'current_DAG_IC_checks': 0,
        'cases': reviewed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    report = check(args.input)
    report['python'] = platform.python_version()
    report['elapsed_seconds'] = time.perf_counter() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('records', 'matrix_entries_read',
        'all_matching_saddle_values_exact', 'strict_failures', 'elapsed_seconds')}, indent=2))


if __name__ == '__main__':
    main()
