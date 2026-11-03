"""Structural delivery check only. Never imports/runs original modules or computes payoffs."""
from pathlib import Path
import ast
import hashlib
import itertools
import json
import re
import sys

HERE = Path(__file__).resolve().parent


def main():
    repo = Path(sys.argv[1]).resolve()
    stage = HERE.parents[4]
    # HERE=stage/archives/customer-attraction/tools/evidence/name
    assert (stage / 'archives/customer-attraction').is_dir()
    primary = json.loads((HERE / 'primary-manifest.json').read_text())
    assert len(primary) == 6 and sum(x['size'] for x in primary) == 10086
    reports = {}
    entries = []
    for item in primary:
        p = stage / item['staged_path']
        b = p.read_bytes()
        assert len(b) == item['size']
        assert hashlib.sha256(b).hexdigest() == item['sha256']
        if p.suffix == '.py':
            tree = ast.parse(b, filename=p.name)
            assert not any(isinstance(n, ast.If) and isinstance(n.test, ast.Compare)
                           and isinstance(n.test.left, ast.Name) and n.test.left.id == '__name__'
                           for n in tree.body)
            entries.append(p.name)
        else:
            reports[p.name] = json.loads(b)
    assert len(reports['thirteen_last_menu_exact.json']) == 12
    assert [len(x) for x in reports['thirteen_last_menu_exact.json']['K']] == [6] * 6
    assert len(reports['thirteen_last_menu_exact.json']['actual_profits']) == 13
    assert len(reports['individual_last_root_floor_probe.json']) == 11
    assert len(reports['last_actual_menu_probe.json']) == 10
    deps = json.loads((HERE / 'dependency-manifest.json').read_text())
    assert len(deps) == 1
    dep = deps[0]
    b = (stage / dep['stage_path']).read_bytes()
    assert len(b) == dep['bytes'] == 4080
    assert hashlib.sha256(b).hexdigest() == dep['sha256']
    d = json.loads(b)
    assert d['players'] == 3 and len(d['topics']) == 6
    assert len(d['customer_mask_multiplicities']) == 21
    actions = {tuple(x['history']): x['action'] for x in d['policy']}
    domain = {h for n in range(3) for h in itertools.product(range(6), repeat=n)}
    assert len(d['policy']) == len(actions) == 43 and set(actions) == domain
    assert all(type(a) is int and 0 <= a < 6 for a in actions.values())
    comparisons = json.loads((HERE / 'comparison-manifest.json').read_text())
    for item in comparisons:
        b = (stage / item['snapshot']).read_bytes()
        assert len(b) == item['bytes']
        assert hashlib.sha256(b).hexdigest() == item['sha256']
    receipts = json.loads((HERE / 'receipts.json').read_text())
    assert {x['id'] for x in receipts} == {x['id'] for x in primary}
    assert all(x['disposition'] == 'retained' and x['source_runs_this_batch'] == 0 for x in receipts)
    claim = json.loads((HERE / 'root-claim-receipt.json').read_text())
    assert claim['status'] == 'pushed' and claim['local_sync']['status'] == 'synced'
    assert {x['id'] for x in primary} <= set(claim['ids'])
    formal = stage / receipts[0]['formal'][0]
    assert formal.is_file()
    link_records = []
    for doc in [formal, HERE / 'README.md']:
        for raw in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', doc.read_text()):
            if '://' in raw or raw.startswith('#'):
                continue
            raw = raw.split('#')[0]
            resolved = (doc.parent / raw).resolve()
            if resolved == HERE / 'self-check.json':
                location = 'generated-by-this-check'
            elif resolved.is_file():
                location = 'stage'
            else:
                rel = resolved.relative_to(stage)
                assert (repo / rel).is_file(), (str(doc), raw)
                location = 'existing-repo'
            link_records.append({'document': str(doc.relative_to(stage)), 'target': raw,
                                 'resolved_in': location})
    out = {'status': 'PASS', 'scope': 'structural integrity only; no mathematical evaluation or source execution',
           'primary_count': 6, 'primary_bytes': 10086, 'parsed_original_code_entries': entries,
           'original_report_root_fields': {k: len(v) for k, v in reports.items()},
           'dependency_full_history_actions': 43, 'comparison_snapshots': len(comparisons),
           'relative_links_checked': len(link_records), 'links': link_records,
           'source_entries_run': 0, 'source_imports': 0, 'LP_BI_RNG_IC_math_checker_runs': 0}
    (HERE / 'self-check.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'links'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
