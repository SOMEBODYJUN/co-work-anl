#!/usr/bin/env python3
"""New curation check of the preserved current article, not recovered author code.

Run from any directory. Uses only stdlib and system Poppler. No compilation or
historical TeX diff is claimed. Rendering was a separate read-only operation.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'archives/weighted-congestion/papers/structural-methods-current'


def digest(data):
    return sha256(data).hexdigest()


manifest = json.loads((HERE / 'source-manifest.json').read_text())
sources = []
for item in manifest['sources']:
    data = (ROOT / item['preserved_path']).read_bytes()
    assert len(data) == item['size']
    assert digest(data) == item['sha256']
    sources.append({'id': item['id'], 'size': len(data), 'sha256': digest(data)})

tex = (PAPER / 'structural_methods_article.tex').read_text()
bib = (PAPER / 'structural_methods_article.bib').read_text()
# Remove unescaped TeX comments before syntax accounting.
active = re.sub(r'(?<!\\)%[^\n]*', '', tex)
labels = re.findall(r'\\label\{([^}]+)\}', active)
refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', active)
cites = [k.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', active)
         for k in group.split(',')]
bibkeys = re.findall(r'@\w+\{([^,]+),', bib)
duplicates = sorted(k for k, n in Counter(labels).items() if n > 1)
undefined_refs = sorted(set(refs) - set(labels))
undefined_cites = sorted(set(cites) - set(bibkeys))
begins = Counter(re.findall(r'\\begin\{([^}]+)\}', active))
ends = Counter(re.findall(r'\\end\{([^}]+)\}', active))
formal = []
for m in re.finditer(r'\\begin\{(lemma|proposition|theorem|corollary)\}(?:\[([^]]*)\])?(.*?)\\end\{\1\}', active, re.S):
    env, title, body = m.groups()
    ids = re.findall(r'\\label\{([^}]+)\}', body)
    formal.append({'environment': env, 'title': title, 'labels': ids,
                   'line': active[:m.start()].count('\n') + 1,
                   'sha256': digest(m.group().encode())})
assert len(formal) == 24
assert begins['proof'] == 24
assert not duplicates and not undefined_refs and not undefined_cites
assert begins == ends
assert all(x['labels'] for x in formal)

pdf = PAPER / 'structural_methods_article.pdf'
info = subprocess.run(['/usr/bin/pdfinfo', str(pdf)], check=True, text=True, capture_output=True).stdout
(HERE / 'pdfinfo.txt').write_text(info)
extracted = subprocess.run(['/usr/bin/pdftotext', '-layout', str(pdf), '-'], check=True,
                           text=True, capture_output=True).stdout
assert extracted == (HERE / 'pdf-text-layout.txt').read_text()
pages = extracted.split('\f')
if not pages[-1].strip():
    pages.pop()
assert len(pages) == 27
assert all(p.strip() for p in pages)

# Literal resource game from current Section 4.4. Actions 0/1 use A/B and
# gate side = action xor (0,1,0). Unit weights, so W=sum of player costs.
def costs(bits):
    n_a = bits.count(0)
    sides = tuple(b ^ phase for b, phase in zip(bits, (0, 1, 0)))
    return tuple(F(n_a if b == 0 else 2) + F(2, 3) * sides.count(sides[i])**2
                 for i, b in enumerate(bits))


expected = [(15, False), (12, True), (24, False), (11, True),
            (12, True), (23, False), (11, True), (12, False)]
table = []
for bits, (w_expected, stable_expected) in zip(product((0, 1), repeat=3), expected):
    old = costs(bits)
    deviations = []
    for i in range(3):
        target = list(bits)
        target[i] ^= 1
        new = costs(tuple(target))[i]
        deviations.append({'player': i, 'old': str(old[i]), 'new': str(new),
                           'old_minus_new': str(old[i] - new)})
    stable = all(F(x['old_minus_new']) <= 0 for x in deviations)
    front = sum(a != b for a, b in zip(bits, bits[1:])) <= 1
    assert sum(old) == w_expected and stable == stable_expected
    table.append({'state': ''.join(map(str, bits)), 'front': front,
                  'costs': list(map(str, old)), 'W': str(sum(old)),
                  'exact_PNE': stable, 'deviations': deviations})
assert min(F(x['W']) for x in table) == 11
assert min(F(x['W']) for x in table if x['exact_PNE']) == 11

# Independent finite dictionary example from Section 2.4.3, actual D/U values.
def ordered(weights):
    load = 0
    out = 0
    for w in weights:
        load += w
        out += w * load**2
    return F(out)


a, b = 3, 1
D = lambda m, n: ordered([a] * m + [b] * n)
U = lambda m, n: ordered([b] * n + [a] * m)
A = min((D(1, n) - D(0, n)) / (a * (a + n*b)**2) for n in range(2))
B = max((U(m, 1) - U(m, 0)) / (b * (m*a + b)**2) for m in range(2))
beta = F(10, 9)
lminus = max(F(0), (1/beta - A)/(1-A))
lplus = min(F(1), (beta-1)/(B-1))
lower = (1 + (B-1)*lminus)/(beta*(A+(1-A)*lminus))
x, y = F(8, 9), F(2, 9)
assert (A, B, lminus, lplus, lower) == (F(7, 8), F(11, 8), F(1, 5), F(8, 27), F(43, 40))
assert A*x+y == 1 and x+y == beta and x+B*y == beta*lower

result = {
    'scope': 'New deterministic curation audit: current assets, TeX syntax, PDF extraction and two finite examples only.',
    'source_hashes': sources,
    'current_tex': {'lines': len(tex.splitlines()), 'formal_count': len(formal),
                    'proof_count': begins['proof'], 'label_count': len(labels),
                    'reference_call_count': len(refs), 'citation_call_count': len(cites),
                    'display_math': {'equation': begins['equation'], 'align': begins['align'],
                                     'bracket_display': len(re.findall(r'(?<!\\)\\\[', active))},
                    'duplicate_labels': duplicates, 'undefined_refs': undefined_refs,
                    'undefined_cites': undefined_cites, 'environment_balance': begins == ends,
                    'bibliography_keys': bibkeys, 'formal_statements': formal},
    'pdf': {'pages': len(pages), 'nonempty_pages': len(pages),
            'page_text_sha256': [digest(p.encode()) for p in pages],
            'extraction_matches_preserved_file': True,
            'visual_check': 'Human/model inspection of all 27 rendered pages in seven contact sheets, plus full extracted-text reading; no clipping or formula spill observed.'},
    'three_player_literal_resource_example': {'states': 8, 'deviations': 24, 'table': table,
                                             'full_OPT': '11', 'minimum_exact_PNE_W': '11'},
    'two_order_literal_example': {'A': str(A), 'B': str(B), 'beta': str(beta),
                                  'lambda_minus': str(lminus), 'lambda_plus': str(lplus),
                                  'scale_interval': [str(lower), str(beta)], 'x': str(x), 'y': str(y)},
    'not_claimed': ['Recompiled PDF', 'Actual diff against unavailable historical TeX',
                    'Private 32-page MOR asset inspected', 'Finite checks prove infinite quantifiers',
                    'External source/policy revalidation or external peer review']
}
(HERE / 'current-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in result['current_tex'].items() if k != 'formal_statements'}, ensure_ascii=False))
print('PASS: 10 source hashes; 27 PDF pages; 24 formal statements/proofs; 8 states/24 deviations; exact finite dictionary example')
