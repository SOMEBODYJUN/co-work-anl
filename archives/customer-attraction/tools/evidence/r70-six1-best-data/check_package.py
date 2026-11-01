"""Static delivery checks only: no audit import, payoff, BI, coefficient or LP run."""
from pathlib import Path
from fractions import Fraction
import ast
import gzip
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BODY = ROOT / 'archives/customer-attraction/state/计算/六人不交覆盖搜索点的随机记录与锐界实例--计算.md'
IDS = ['15338f897ce896dfb4d3', 'd9f27a00ce820bda3f97']


def read(p):
    return json.loads(p.read_text())


def fingerprint(p):
    b = p.read_bytes()
    return dict(path=str(p.relative_to(ROOT)), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def main():
    manifest = read(HERE / 'source-manifest.json')
    sources = []
    for entry in manifest['sources']:
        p = ROOT / entry['preserved_path']
        b = p.read_bytes()
        assert len(b) == entry['size']
        assert hashlib.sha256(b).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == entry['blob']
        sources.append(entry['id'])
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
    for p in HERE.rglob('*.json'):
        if p.name != 'self-check.json':
            read(p)
    report = read(HERE / 'point-audit.json')
    assert report['status'] == 'PASS'
    assert report['original_solver_runs'] == report['original_helper_calls'] == report['optimizer_calls'] == 0
    assert report['independent_mathematical_entry_runs'] == 1
    event = read(HERE / 'execution.json')
    assert event['exit_code'] == 0 and event['stderr_bytes'] == 0
    assert event['script_sha256'] == fingerprint(HERE / 'audit_points.py')['sha256']
    assert report['details']['sha256'] == fingerprint(HERE / 'exact-details.json.gz')['sha256']
    detail = json.loads(gzip.decompress((HERE / 'exact-details.json.gz').read_bytes()))
    assert len(detail) == 2
    for case in detail:
        summary = report['points'][case['point']]
        assert len(case['terminal_rows']) == summary['terminal_multisets'] == 924
        assert len(case['ordered_history_rows']) == summary['strategy_nodes'] == 19608
        assert case['payment_scale'] == 60
        assert len(summary['slack_histogram']) > 0
        for value in summary['slack_histogram']:
            Fraction(value)
        for row in case['ordered_history_rows']:
            assert len(row) == 5 and len(row[2]) == 6 and len(row[4]) == 7
            assert isinstance(row[3], int) and all(isinstance(x, int) for x in row[4])
        assert sum(summary['slack_histogram'].values()) == 137256
    expected_input = [HERE/'original/random_best.json', HERE/'original/lp_best.json',
                      HERE.parent/'r70-strategy-lp-program/replay/complete-strategy.json']
    for p, b in zip(expected_input, report['input_bindings']):
        f = fingerprint(p)
        assert f['bytes'] == b['bytes'] and f['sha256'] == b['sha256']
    review = read(HERE / 'review-record.json')
    for item in review['bindings']:
        got = fingerprint(ROOT / item['path'])
        assert got == item
    links = []
    for p in [BODY, HERE/'README.md']:
        text = p.read_text()
        assert not any(ord(c) < 32 and c not in '\n\t' for c in text)
        assert text.endswith('\n') and not text.endswith('\n\n')
        assert not any(line.rstrip() != line for line in text.splitlines())
        for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if '://' in href or href.startswith('#'):
                continue
            target = (p.parent / href.split('#', 1)[0]).resolve()
            assert target.exists(), (p, href)
            links.append(dict(source=str(p.relative_to(ROOT)), target=str(target.relative_to(ROOT))))
    fm = BODY.read_text().split('---', 2)[1]
    for field in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
        assert re.search('^' + field + ':', fm, re.M)
    receipts = []
    for sid in IDS:
        p = ROOT/'cleanup/workspaces/Boss7/receipts-round16'/f'{sid}.json'
        rec = read(p)
        assert rec['id'] == sid and rec['disposition'] == 'integrated'
        assert rec['full_file_reviewed'] and rec['related_material_checked'] and rec['unique_content_accounted_for']
        for path in rec['targets']:
            assert (ROOT/path).exists()
        receipts.append(fingerprint(p))
    own = [fingerprint(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name != 'self-check.json']
    result = dict(status='PASS', scope='Static source bytes, schemas, gzip all rows, receipts and links; no mathematical implementation rerun',
                  sources=sources, owned_fingerprints=own, body=fingerprint(BODY), receipts=receipts,
                  shared_and_comparison_bindings=len(review['bindings']), links_checked=len(links), links=links,
                  original_entries=0, independent_mathematical_entries=0, optimizer_calls=0)
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',sources=len(sources),own=len(own),bindings=len(review['bindings']),links=len(links),receipts=len(receipts))))


if __name__ == '__main__':
    main()
