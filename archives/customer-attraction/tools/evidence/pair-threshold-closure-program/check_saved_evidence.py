"""Compare saved runs and frozen identity; never rebuild a constraint matrix."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from collections import Counter
import ast
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def main():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    base = json.loads((REPO / manifest['base_frozen_manifest']).read_text())
    records = base['frozen_sources'] + manifest['supplemental_frozen_sources']
    bypath = {}
    for r in records:
        data = (REPO / r['stored_path']).read_bytes()
        assert len(data) == r['size'] and sha256(data).hexdigest() == r['sha256']
        assert r['path'] not in bypath
        bypath[r['path']] = r
    run = json.loads((HERE / 'run-report.json').read_text())
    assert run['original_main_calls'] == 1 and run['linprog_or_solve_float_calls'] == 0
    assert sha256((HERE / 'capture_original.py').read_bytes()).hexdigest() == run['wrapper_sha256']
    assert sha256((HERE / 'all-row-slacks.json').read_bytes()).hexdigest() == run['all_row_slacks_sha256']
    assert sha256((HERE / 'stdout.txt').read_bytes()).hexdigest() == run['stdout_sha256']
    for r in run['imported_runtime_modules']:
        frozen = bypath[r['path']]
        assert (r['size'], r['sha256']) == (frozen['size'], frozen['sha256'])
    rows = json.loads((HERE / 'all-row-slacks.json').read_text())
    assert len(rows) == run['rows'] == 10344
    for i, row in enumerate(rows):
        assert row['index'] == i and F(row['slack']) >= 0
    for section in run['row_sections'].values():
        slacks = [F(x['slack']) for x in rows[section['begin_inclusive']:section['end_exclusive']]]
        assert len(slacks) == section['rows']
        assert str(min(slacks)) == section['minimum']
        assert sum(x == 0 for x in slacks) == section['zero']
        assert sum(x > 0 for x in slacks) == section['positive']
        assert sum(x < 0 for x in slacks) == section['negative'] == 0
    prior_path = REPO / manifest['reused_independent_added_row_report']
    prior = json.loads(prior_path.read_text())
    compared = 0
    for family, start, end in [('Z_to_Z', 5108, 5168), ('PAIR_RZ', 5168, 5228), ('PAIR_ZZ', 5228, 5288)]:
        old = prior['added_row_families'][family]['all_slacks']
        for saved, actual in zip(old, rows[start:end], strict=True):
            name = actual['name']
            tpl = ast.literal_eval(name.split(':', 1)[1]) if family == 'Z_to_Z' else ast.literal_eval(name)[1:]
            assert list(tpl[:2]) == saved['families'] and list(tpl[2]) == saved['equality_pattern']
            assert F(actual['slack']) == F(saved['slack'])
            compared += 1
    assert run['row_sections']['overlap_upper']['rows'] == prior['overlap_upper_bounds']
    assert run['row_sections']['overlap_upper']['zero'] == prior['zero_overlap_upper_slacks']
    # A tiny combinatorial identity only: no client weights or row generation.
    counts = Counter()
    edges = [(f, i, j) for f, i, j in product(range(2), range(6), range(6)) if f or i != j]
    for f, i, j in edges:
        for g, k, l in edges:
            labels = {}
            pattern = tuple(labels.setdefault(v, len(labels)) for v in (i, j, k, l))
            counts[(f, g, pattern)] += 1
    live = {str((f, g)): sum(k[:2] == (f, g) for k in counts) for f, g in product(range(2), repeat=2)}
    assert list(live.values()) == [7, 10, 10, 15] and sum(counts.values()) == 4356
    for start in (5168, 5228):
        for row in rows[start:start + 60]:
            _, f, g, pat = ast.literal_eval(row['name'])
            assert (F(row['slack']) == 0) == ((f, g, pat) not in counts)
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
    obj = REPO / manifest['formal_object']
    checked_links = 0
    for link in re.findall(r'\]\(([^)]+)\)', obj.read_text()):
        if '://' not in link and not link.startswith('#'):
            assert (obj.parent / link.split('#')[0]).resolve().exists(), link
            checked_links += 1
    report = {
        'status': 'PASS_SAVED_EVIDENCE_BINDING_AND_RESULT_COMPARISON',
        'scope': 'Static saved-result inspection and 4356 unweighted index-pair incidence count; no old main, optimization, client matrix or constraint generator run.',
        'frozen_files_checked': len(records), 'imported_modules_checked': len(run['imported_runtime_modules']),
        'all_saved_exact_slacks_checked': len(rows), 'independent_saved_slacks_compared': compared,
        'saved_overlap_count_and_zero_count_match': True, 'four_family_live_pattern_counts': live,
        'index_pairs': sum(counts.values()), 'PAIR_zero_rows_exactly_empty_index_classes': True,
        'formal_local_links_checked': checked_links, 'python_syntax_checked_without_execution': True,
        'run_report_sha256': sha256((HERE / 'run-report.json').read_bytes()).hexdigest(),
        'reused_independent_report_sha256': sha256(prior_path.read_bytes()).hexdigest(),
    }
    (HERE / 'self-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
