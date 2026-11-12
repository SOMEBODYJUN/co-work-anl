from pathlib import Path
import hashlib, json, shutil, subprocess, sys

B = Path('/workspace/scratch/1a53a6eb65ea')
R = B / 'co-work-anl-boss1'
A = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea'
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data): p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

reviews = []
materials = []
for name, expected in [
    ('residual-static', '544f1a5b27c1695e7b1bd0bb47c4309ed39bb871862bc349c1bc4a3de1fa5c59'),
    ('root-requery-graph', '282bd0c1d1925991e071a0b5b71b2c0c8d542ac7e6a659db990517386a56311d'),
    ('maxroot61', '60c0866331f42834b78452476aca801078f6c9d84df9e580dfd70bc0056ba375'),
]:
    audit = A / ('wave15-' + name + '-delivery-review')
    validation = read(audit / 'validation.json')
    assert validation['status'] == 'NATIVE_FULL_RECEIPT_VALIDATION_PASSED'
    s = validation['tasks'][0]
    assert s['receipt_sha256'] == expected
    task = read(R / 'research/operations/map-v2/tasks' / (s['task_id'] + '.json'))
    assert task['state'] == 'done' and rr.pin(task['definition']) == s['definition_pin']
    assert sha(R / s['receipt_path']) == expected
    assert task['receipt'] == read(R / s['receipt_path'])
    reviews.append(s)
    for filename in ['validation.json', 'root-mathematical-review.md', 'worker-frozen-manifest.json', 'native-binding-events.json', 'final-binding-manifest.json']:
        p = audit / filename
        materials.append({'path': str(p.relative_to(R)), 'sha256': sha(p)})

peer_specs = [
    ('2c3bfa8c793694f1', '9eeed0a4ea7c636789feae17cfb5cbdb1105b93c34de7697e6ac62f060ece935', '937f6870e24c7b66946e15e4a453282bbd0fbfbdd582453c16c5d29911b6de99', '2a9b6a215c591177abcb1a823bbbc2fd604e61a312df8d8ff49a969bd9d685a3'),
    ('a8d6b72548072620', 'c0bd5b4e9097b9ea4b1e179f8bf0e57a23dd07ac8ea59832aeae0b89fcfd065a', '90159dd065f96894e5d6dd71a7a1438356dfe459dd4392c2f20b4b15899326a0', 'c838088fea63157f9c0f497bd1f1ab634148c4f4f1dfe5d5ea6bb331c087cfe7'),
    ('c986a138e6639b6f', '18167d31223a55d5d1cf9f08f87392fe4ef666f0ed9be40f976ba777d63589f7', '22d6559d125aa6cee0a63718b8a32790983a147fa8384382c40beb381b28acfc', '700473878be3919a1fa5fd98d7dea3cfaf9e30d143d4ed41da4c5e6789920af4'),
]
reg = read(R / 'research/registry.json')
objects = {o['object_id']: o for o in reg['objects']}
for suffix, defpin, receipt_sha, receipt_pin in peer_specs:
    tid = 'customer-attraction-3a-3a-' + suffix
    task = read(R / 'research/operations/map-v2/tasks' / (tid + '.json'))
    path = 'map/receipts/' + tid + '.json'
    receipt = read(R / path)
    assert task['state'] == 'done' and task['receipt'] == receipt, tid
    assert rr.pin(task['definition']) == defpin, tid
    assert sha(R / path) == receipt_sha and rr.pin(receipt) == receipt_pin, tid
    assert all(rr.pin(objects[k]) == v for k, v in task['definition']['input_pins'].items()), tid
    for asset in receipt['assets']:
        assert sha(R / asset['path']) == asset['sha256'], asset['path']
    reviews.append({
        'task_id': tid, 'definition_pin': defpin,
        'receipt_path': path, 'receipt_sha256': receipt_sha, 'receipt_pin': receipt_pin,
        'input_pins': task['definition']['input_pins'], 'core_ids': task['definition']['object_ids'],
        'review_method': 'Independent fresh Boss1 mathematical review plus Root substantive source/target and derivation review; mature scientific audits inherited explicitly.'
    })

# Root executes only after receiving and reading the final worker reports.
worker_hashes = {
    'wave15-peer-two-3d-worker': {
        'proof-review.md': '2d6db1cf861fcccbeed777b179cbbd67c2ab9274f404cd60f3b789386499d819',
        'refs.json': '98bde257b45ada5200df5bae535232464c5bcc46fe26e9076bd3cbde233bcbf2',
        'review-summary.json': '355980e1ae27cc2a0e8795197d2efb33a73cf877b5143728b934f749c93caddd',
    },
    'wave15-peer-ent1-3d-worker': {
        'proof-review.md': 'e4ee43d9600445666c78824ea7196f379ecfab0dc968a8dfe045e9394b32452c',
        'refs.json': 'f14e7399d44eb5b5c3a70479385c3b2ef8f89c465493372940d0786d21e0d939',
        'review-summary.json': 'b384333e3a8413584c1aa26a8219260155c145e4e61c3de9a97cd876c83f1189',
    },
}
for folder, files in worker_hashes.items():
    for filename, expected in files.items():
        assert sha(B / folder / filename) == expected, (folder, filename)
peer_audit = A / 'wave15-peer-three-integration-review'
assert not peer_audit.exists()
peer_audit.mkdir()
for folder in ['wave15-peer-two-3d-worker', 'wave15-peer-ent1-3d-worker']:
    source = B / folder
    dest = peer_audit / folder
    dest.mkdir()
    for filename in ['proof-review.md', 'refs.json', 'review-summary.json']:
        assert (source / filename).is_file(), source / filename
    for p in sorted(source.rglob('*')):
        if not p.is_file(): continue
        target = dest / p.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        assert sha(p) == sha(target)
        materials.append({'path': str(target.relative_to(R)), 'sha256': sha(target)})
shutil.copyfile(B / 'wave15-peer-three-root-review.md', peer_audit / 'root-mathematical-review.md')
shutil.copyfile(Path(__file__), peer_audit / 'adopt-six-reviewed.py')
for filename in ['root-mathematical-review.md', 'adopt-six-reviewed.py']:
    p = peer_audit / filename
    materials.append({'path': str(p.relative_to(R)), 'sha256': sha(p)})

record = {
    'review_id': 'boss1-wave15-residual-maxroot-and-three-peer-current-review',
    'reviewer': 'Boss1', 'task_reviews': reviews, 'edge_reviews': [], 'review_materials': materials,
    'source_reviews': [{
        'object_id': 'CA-FRACTIONAL-ACTUAL-LOAD-WEAK-NO-v1',
        'object_pin': '0ab7439e96f99aa0a69371377fde7fc2cccb843604300f06c0508900e28fe199',
        'materials': [{
            'path': 'archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md',
            'sha256': '32a7f769383211709c67373e85118ceb541b5e4d58d2bb3d826272ac3e332b1f',
        }],
        'review_scope': 'Full beta construction, every ordered-history IC case and all-m scaled weak-bridge versus positive exact-tax balance, used to discharge the c986 formal named overlap. This is not a substitute primary3A receipt.'
    }],
    'review_note': 'Boss1 adopts exactly six current task receipts and ten relations after substantive source/target and derivation review: three own deliveries (six edges) and three concurrent Boss2 deliveries (four edges). Whole fixed-background saddle specializations, row-source contributions, context checks, one fixed-cone welfare contribution, and the complete ENT1 counterexample transfer retain distinct scopes. Original workers preserve their full declared reading and lossless data views; independent 3D and Root reviews preserve the inherited scope of mature scientific certificates. No source/truth-status changes or scientific replay occurred. Unreviewed concurrent changes remain pending.',
    'archive_notes': {
        'archives/customer-attraction': {
            'comparison_scope': 'Pure saddle specialization versus three legal residual backgrounds; static PNE/CCE replay contracts; two-tail tax versus five true maxroot requery graphs; seven-source CART and retained three/four-tail bounds versus the fixed 61-atom 4007-row library; fixed common-Q policy cones versus static sharp security and fixed-query duality; three tail theorems versus the two-path induction array; and the same complete thirteen-player witness versus unscaled ENT1/SAIC, including the declared four-theme weak-payment overlap.',
            'outcome': 'The pure saddle row gives exact v=(63/10,32/3,53/6), residual P=r v and unique complete constant-action SPE through strict true IC at every ordered history, rather than inferring strategy uniqueness from one outcome count. Static PNE/CCE entries supply two context checks only: an existing W15 SPE is not a min-SPE=15 proof; the static CCE checker does not certify all sequential SPE welfare3. Two-tail tax and six-index pair averaging pay only the PAIRO families of five requery graphs; their other rows and integer full-cube certificates remain separate. The 61-atom packet receives 1904 AP rows from seven true sources and 875 repeated-tuple rows from THREE plus complete original1499/750 Retained FOUR, with the same maximum-root branch, ordered tail and rho_min. Validity of these rows does not prove fixed-primal feasibility or inverse SPE realization. The 21 common-Q cones instantiate fixed-p dual certificates by n-weighted averaging and remain checks/context. Their sole b352 six-player cone combines by ALL with the same-instance static price11 to give W>=6OPT/11 on integer and denominator-cleared rational points. The two-path array receives 1416 true tail rows with T3 d=0 and five copies of the same T4 remainder; 90 true-node safe rows and rootE complete its necessary projection, but the exact LP optimum still needs mature primal/dual certificates and does not contradict five-player half. Finally, the same complete thirteen-player witness gives g=(5/3,3/2,3,5/2,5/2,25/11), R0=359/66 and ENT1 excess37/66; B=W-R0 identifies SAIC without identifying it with the abstract delta budget. The four-theme all-m weak-payment family has positive exact-tax and half balances, so its formal overlap is correctly closed as a distinct claim. Read-only M05 target coverage is not manually promoted to replace its own primary3A receipt. Seven logical and three context relations are adopted; no arbitrary-directory half theorem or missing inverse realization is claimed.'
        },
        'archives/customer-attraction/subarchives/six-providers': {
            'comparison_scope': 'The one specified six-player eight-label complete-policy cone b352, the same-instance static mixed-security sharp bound, and the exact-six full-history half question.',
            'outcome': 'ALL of the certified whole fixed cone W>=6v6 and static OPT6<=11v6 yields the completed local contribution W>=6OPT6/11, hence half, on its integer and cleared rational client domain. Other complete six-player policies and all other directory sizes remain open. The 20 five-player cones, the five-player row libraries and the thirteen-player auxiliary-budget counterexample are not promoted into this target.'
        }
    },
    'cross_archive_scope': 'All six reviewed packets concern the common-catalog customer-attraction model, including its exact-six subarchive. The independent static games and legal nonempty residual histories retain their explicit quantifiers.',
    'cross_archive_outcome': 'No new cross-archive model migration is inferred from shared notation or directory proximity. Only exact reviewed receipts and endpoints are discharged; other concurrent changes and primary3A coverage obligations are preserved.'
}
p = A / 'wave15-residual-maxroot-and-three-peer-reviewed.json'
assert not p.exists()
save(p, record)
q = subprocess.run([sys.executable, str(A / 'adopt_current_review.py'), str(p)], cwd=R, capture_output=True, text=True)
(B / 'wave15-six-current-review-adoption.txt').write_text(q.stdout + '\n' + q.stderr)
print(q.stdout)
if q.returncode: print(q.stderr)
raise SystemExit(q.returncode)
