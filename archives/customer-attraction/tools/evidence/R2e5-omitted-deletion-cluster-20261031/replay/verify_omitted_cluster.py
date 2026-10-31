from pathlib import Path
import hashlib, json

base = Path(__file__).resolve().parent.parent
src = base / 'source'
rep = base / 'replay'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected = {
    'breakpoints.json': 'b99e316ef1debb7e8e296343d258fd4b849563b03ab5330b532b7ad1808c5c11',
    'discovery.json': 'eec5d795a8d391a60a71657dc3038e10e35de8a5cc057c187cc856349cf3767d',
    'minimal.json': '4c259f62e2c2211d4348149b02c571f94fc20c4f8fa66e974083576f059e2e6e',
    'minimize.py': 'a3d910eb2740d7df1472f951f4b4af97cc43d9c0f9af7c99db9a25eb12f32af0',
    'parameter_scan.json': '0e04fea2d88ffc956ec7533557dc5ad014834e254dfec5aae2d15477985e1902',
}
for name, digest in expected.items():
    assert sha(src / name) == digest, (name, sha(src / name))

discovery = json.loads((src / 'discovery.json').read_text())
minimal = json.loads((src / 'minimal.json').read_text())
replayed = json.loads((rep / 'minimal.replayed.json').read_text())
assert discovery['target'] == [2, 0, 1, 0, 0, 2]
assert discovery['discovery_trial'] == {'players': 5, 'topics': 6, 'trial': 135}
assert sum(x['multiplicity'] for x in discovery['instance']['customers']) == 82
assert minimal == replayed
assert minimal['target'] == discovery['target']
assert minimal['reductions'] == 36
assert sum(x['multiplicity'] for x in minimal['instance']['customers']) == 38

scan = json.loads((src / 'parameter_scan.json').read_text())
breakpoints = json.loads((src / 'breakpoints.json').read_text())
reference = json.loads((rep / 'reference-parameter-partition.json').read_text())
assert breakpoints == reference['cuts']
projection = [
    {'t': x['t'], 'target_realizable': x['target_in_root'],
     'root_threshold': x['threshold'], 'outcomes': x['root_outcomes']}
    for x in reference['representatives']
]
assert scan == projection
assert len(scan) == 129 and len(breakpoints) == 65
assert sum(not x['target_realizable'] for x in scan) == 96
assert sum(x['target_realizable'] for x in scan) == 33
assert scan[0]['root_threshold'] == '33/4'
assert scan[96]['t'] == '3/4' and scan[96]['target_realizable']
assert scan[96]['root_threshold'] == '7'
assert scan[96]['outcomes'] == [[2, 0, 1, 1, 1], [2, 1, 0, 0, 2], [2, 1, 1, 0, 1]]
assert scan[97]['t'] == '91/120'
assert all(x['root_threshold'] == '33/4' for x in scan[:96])
assert all(x['root_threshold'] == '7' for x in scan[96:])
print('PASS')
