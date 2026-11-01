"""Replay only check() on the frozen point; no randomized run/minimize call."""
from pathlib import Path
import importlib.util
import json
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'original'
sys.path.insert(0, str(ROOT))
source = ROOT / ('research/workspaces/customer-attraction/'
                 'R-51ca8c2b36184c41818099bc490374ca/independent/'
                 'background_welfare_nonmonotone.json')
probe = source.with_name('probe_monotone_welfare.py')
spec = importlib.util.spec_from_file_location('frozen_welfare_probe', probe)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
saved = json.loads(source.read_text())
rows = [(sum(1 << a for a in customer['topics']), customer['multiplicity'])
        for customer in saved['instance']['customers']]
ok, instance, original, added_instance, added = module.check(
    rows, saved['base'], saved['add'], saved['r'])
solver = module.ExactSPESolver(instance)
added_solver = module.ExactSPESolver(added_instance)
background_after = tuple(n + int(a == saved['add']) for a, n in enumerate(saved['base']))
report = {
    'status': 'PASS' if ok else 'FAIL',
    'entry': 'frozen probe_monotone_welfare.check on saved rows/base/add/r',
    'random_run_called': False,
    'minimize_called': False,
    'instance': instance.to_dict(),
    'base': saved['base'],
    'add': saved['add'],
    'r': saved['r'],
    'added_instance_players': added_instance.players,
    'original': [original[0], list(original[1])],
    'added': [added[0], list(added[1])],
    'original_all_outcomes': sorted(map(list, solver.outcomes(saved['base']))),
    'added_all_outcomes': sorted(map(list, added_solver.outcomes(background_after))),
}
assert report['original'] == saved['original']
assert report['added'] == saved['added']
assert report['status'] == 'PASS'
print(json.dumps(report, indent=2))
