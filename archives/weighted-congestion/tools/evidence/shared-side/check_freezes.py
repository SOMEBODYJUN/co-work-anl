#!/usr/bin/env python3
"""Check precise current slices, preserving unmatched historical whole hashes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
source = ROOT / 'original/research/current/weighted_congestion/shared_side_truncated_potential.md'
body = source.read_bytes()
def section(start, end):
    return body[body.index(start.encode()):body.index(end.encode())]
checks = [
    ('unique-light old canonical whole file', body[:body.index('## 八、'.encode())],
     '58b77bb19bee463ad56adf0da8f951fe2b1e92f59bf4f2ac7c146363d22bcfc1'),
    ('multisource old canonical whole file', body[:body.index('## 九、'.encode())],
     '9660ed3b13aa178a49d402bcf457f93d5019539c452afeb0a2ae4844961542fc'),
    ('tradeoff-v1 sections9.1-9.6 including chapter9 heading', section('## 九、', '### 9.7.'),
     '44faec14c309ab19e74f7c22ff06f1cefcb87861c43fa3f47f44d3687ea33624'),
    ('tradeoff-v2 sections9.8-9.12', section('### 9.8.', '### 9.13.'),
     'c5adfcb33930101ea97ff01ed7a235de947bdd405d2c6619d9ca8456c2193387'),
    ('tradeoff-v3 sections9.14-9.17', section('### 9.14.', '### 9.18.'),
     '65636ff885b7e2697ffaff6a3441c8ea580faed65bdc907fa56d138ab888e5fb'),
    ('heterogeneous-v2 chapter11 heading plus11.1-11.4', section('## 十一、', '### 11.5.'),
     'bf4478c57a426b5fd0817a07d06686951596f717cd888620ae663fb0a24afb76'),
]
rows = []
for name, segment, wanted in checks:
    normalized = segment.rstrip(b'\n') + b'\n'
    rows.append({'section': name, 'review_sha256': wanted,
                 'current_slice_with_single_trailing_newline_sha256': hashlib.sha256(normalized).hexdigest(),
                 'matches': hashlib.sha256(normalized).hexdigest() == wanted,
                 'normalization': 'keep literal selected bytes; only replace trailing separator newlines by one newline',
                 'bytes': len(normalized)})
result = {'full_current_sha256': hashlib.sha256(body).hexdigest(), 'checks': rows,
          'unmatched_whole_hashes': 'Historical whole candidates are not present; changed current title/navigation and later edits mean their hashes do not identify current prefixes. No claim of old-candidate byte equivalence.'}
(ROOT / 'replay/freeze-comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
assert all(row['matches'] for row in rows[2:])
