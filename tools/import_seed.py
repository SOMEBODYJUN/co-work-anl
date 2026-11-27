#!/usr/bin/env python3
"""Convert the user's 47 seed rows to provenance-aware ledger records."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse


def convert(root):
    rows = list(csv.DictReader((root / 'inputs/02_macro_evidence.csv').read_text(encoding='utf-8-sig').splitlines()))
    result = []
    for row in rows:
        url = row['来源']
        hostname = urlparse(url).hostname or 'supplied-market-snapshot'
        family = 'NBS' if hostname.endswith('stats.gov.cn') else hostname
        match = re.search(r'/t(\d{4})(\d{2})(\d{2})_', url)
        released = '-'.join(match.groups()) if match else 'not-stated-in-seed'
        value = {'indicator': row['指标'], 'value_as_supplied': row['值'],
                 'unit': row['单位'].strip(), 'observation_period': row['所属期'],
                 'interpretation_as_supplied': row['解读与限制']}
        result.append({'id': row['证据ID'], 'kind': 'observation', 'url': url,
                       'original_source_url': url, 'source_family': family,
                       'published_at': released, 'observation_period': row['所属期'],
                       'event_id': 'seed-publication-' + hashlib.sha256(url.encode()).hexdigest()[:12],
                       'text': json.dumps(value, ensure_ascii=False), 'seed_status': row['状态'],
                       'provenance_scope': 'user-supplied extracted evidence row',
                       'topic': row['主题']})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    records = convert(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'records': records}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'evidence_rows': len(records),
                      'publication_items': len({r['url'] for r in records}),
                      'output': str(args.output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
