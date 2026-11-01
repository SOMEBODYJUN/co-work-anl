"""Deterministic replay of the frozen run() and greedy minimize() functions."""
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
spec = importlib.util.spec_from_file_location('frozen_welfare_probe',
                                             source.with_name('probe_monotone_welfare.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
raw = module.run()
minimized = module.minimize()
normalized = json.loads(json.dumps(minimized))
saved = json.loads(source.read_text())
assert normalized == saved
print(json.dumps({
    'status': 'PASS',
    'run_default_result': raw,
    'minimize_current_result': minimized,
    'minimize_matches_frozen_json_values': normalized == saved,
    'historical_generation_command_known': False,
    'global_or_coordinate_minimum_certified': False,
}, indent=2))
