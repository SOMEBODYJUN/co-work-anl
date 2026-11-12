from pathlib import Path
import hashlib
import json
import subprocess
import sys

R = Path('/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1')
A = Path('research/workspaces/map-v2/Boss1/session-1a53a6eb65ea')
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


reg = read(R / 'research/registry.json')
obs = {o['object_id']: o for o in reg['objects']}
validation = read(R / A / 'wave12-theta-funding-delivery-review/validation.json')
tasks = list(validation['tasks'])
expected = [
    ('unrelated-machines-3a-3a-ec98dbd143c32cff',
     '990c1ec6633f8bc55654a8653d66b9767d38cfff0109bab78f534f9a2cb81d61',
     '0a0877a37034a6e9d0ea7bd60e56e4ec54150498f1934bf177a7a019af6fa542'),
    ('unrelated-machines-3a-3a-e5622a5b3226206f',
     '61f01a49844cb34448a90baebb297c52cf2b95a80ab1f70f97f1bbb533fade2e',
     'bd5aeb6d89d3430f7507e05fc8b1dc5ef88ddd479d690c74603ca0bd624a6869'),
    ('unrelated-machines-3a-3a-eba225f7871d217b',
     '59a0446fd4d190533c4e5a379f2deca39dd830d8d6f382915ce4e01277c5e0aa',
     '8ef59fe8d33758ba7e7b1a38f222f46520391a935fca60b14d58f70b0fba9201'),
    ('unrelated-machines-3a-3a-f3d11f3d19e62b00',
     'f644d88a1ba4e9f7deb4cb626fd99600c0eb186663efab59ac20a0e38502f8bb',
     'e7d19740b8e9ce408dc9d7c23842d3c0588d363e2e6f34506c68c0ea261c6544'),
    ('unrelated-machines-3a-3a-f4d4b5a27b63ee05',
     '60fc1a19639527d8c874acc627ffea0f79c463700b601bce79b16052c37fe554',
     '901e9c092e85be40924174c961c54dfb817248cec74b644985742662346d6096'),
]
for tid, dp, receipt_sha in expected:
    t = read(R / 'research/operations/map-v2/tasks' / (tid + '.json'))
    d = t['definition']
    rp = f'map/receipts/{tid}.json'
    receipt = read(R / rp)
    assert t['state'] == 'done' and t['receipt'] == receipt
    assert rr.pin(d) == dp and sha(R / rp) == receipt_sha
    assert all(rr.pin(obs[k]) == v for k, v in d['input_pins'].items())
    for item in receipt['assets']:
        assert sha(R / item['path']) == item['sha256']
    tasks.append({'task_id': tid, 'definition_pin': dp, 'receipt_path': rp,
                  'receipt_sha256': receipt_sha, 'receipt_pin': rr.pin(receipt),
                  'input_pins': d['input_pins'], 'core_ids': d['object_ids']})
materials = [
    'wave12-theta-funding-delivery-review/validation.json',
    'wave12-theta-funding-delivery-review/root-mathematical-review.md',
    'wave12-positive-flat-3d/proof-review.md',
    'wave12-positive-flat-3d/refs.json',
    'wave12-positive-flat-3d/root-review.md',
    'wave12-value-mmo-3d/proof-review.md',
    'wave12-value-mmo-3d/refs.json',
    'wave12-value-mmo-3d/root-review.md',
    'wave12-ext-diamondless-3d/root-review.md',
]
record = {
    'review_id': 'boss1-wave12-theta-and-five-um-current-review',
    'reviewer': 'Boss1',
    'task_reviews': tasks,
    'edge_reviews': [],
    'review_materials': [{'path': (A / p).as_posix(), 'sha256': sha(R / A / p)} for p in materials],
    'review_note': 'Boss1 reviewed the full two-core theta/funding delivery and the complete core coverage of five current unrelated-machines packets, with independent workers and Root mathematical reconstruction. All adopted definitions, receipts, assets and endpoints are frozen exactly. Existing logical relations retain their whole/contribution, conditionality and target scope. Concurrent unreviewed changes, including Cheng-Mao and pending RET-source replacements, remain pending.',
    'archive_notes': {
        'archives/customer-attraction': {
            'comparison_scope': 'Four-player pure-theta counterexample versus exact model and mixed-security boundary; OWN/TAME, ALL, ROW, origin-preserving beta-max and old FCLC contracts versus cross-action joint funding. Existing ALL-to-ROW and FCLC-to-OWN proofs compared without duplication.',
            'outcome': 'Two cores isolated after substantive comparison, with one new cites/context relation. Pure theta failure does not negate half or mixed security; per-context IC/refunds do not pay sum of action coefficients or the common remainder 2u-d-H-J. Expanded-family feasibility does not imply old mandatory-NEW feasibility. No identity needs-decision or invented new open node.'
        },
        'archives/unrelated-machines': {
            'comparison_scope': 'EXT-to-positive finite atoms, positive sparse flatness-to-original-T support contribution, fixed-precision Svensson numerical estimation, positive-weight threshold MMO-to-simple-series-parallel transfer, BORDER-to-EXT connected-basis branch versus general C kernel induction, and actual k2 MMO-to-diamondless job-graph hardness; complete single-core coverage for ec98, e562, eba225, f3d11 and f4d4.',
            'outcome': 'EXT-to-POS remains unconditional whole, including rank zero, arbitrary independent Gram basis, ideal/self-adjoint quotient, cyclic positive atoms and original data. POS-to-NF remains delta-zero contribution with original degree-three load localizers and support-count algorithm, not positive-delta extraction. Estimation remains conditional on its exact polynomial threshold backend and does not construct assignments. MMO threshold transfer remains unconditional whole with positive-weight branch handling, explicit width two and safe pseudopolynomial DP; no outerplanar or all-threshold fixed-graph claim. Current canonical Asahiro path is 7bbf1422, not the retired historical path. BORDER-to-EXT retains its extra connected full-rank B condition and contribution scope; the already-proved general EXT kernel induction is not invented as open work. k2 actual simple bipartite degree-three gadgets, tail-load scheduling bijection and ordinary-diamond line-graph exclusion pay the entire target 2/3 gap and fixed c<3/2 hardness.'
        }
    },
    'cross_archive_scope': 'Independent current mathematical reviews in customer-attraction and unrelated-machines; no common model or proof premise is inferred merely from simultaneous integration.',
    'cross_archive_outcome': 'No additional cross-archive relation is asserted; open obligations and unreviewed concurrent changes are preserved.'
}
p = R / A / 'wave12-theta-and-five-um-reviewed.json'
p.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
c = subprocess.run([sys.executable, str(R / A / 'adopt_current_review.py'), str(p)], cwd=R)
raise SystemExit(c.returncode)
