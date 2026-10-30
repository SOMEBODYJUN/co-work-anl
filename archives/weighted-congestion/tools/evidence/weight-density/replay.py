#!/usr/bin/env python3
"""Run the unchanged original density audit and retain its actual game inputs."""
from pathlib import Path
import contextlib
import hashlib
import importlib.util
import io
import json
import sys

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'original/tests/audits/weighted_congestion_density.py'
FROZEN = ROOT / 'original/evidence/runs/2026-10-14/weighted_congestion_density.json'
OUT = ROOT / 'replay'
OUT.mkdir(exist_ok=True)
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('original_density_audit', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
actual_inputs = []
original_audit_game = module.audit_game

def record_input(roots, m, q, strategies, coeff):
    actual_inputs.append({'roots': list(map(str, roots)), 'm': m, 'q': q,
                          'weights': [str(h**m) for h in roots],
                          'strategies': [[sorted(action) for action in player] for player in strategies],
                          'coefficients': [[str(c) for c in poly] for poly in coeff]})
    return original_audit_game(roots, m, q, strategies, coeff)

module.audit_game = record_input
sys.argv = [str(SCRIPT), '--output', str(OUT / 'density.json')]
stdout = io.StringIO()
with contextlib.redirect_stdout(stdout):
    module.main()
(OUT / 'stdout.txt').write_text(stdout.getvalue())
(OUT / 'actual-game-inputs.json').write_text(json.dumps(actual_inputs, indent=2) + '\n')
old = json.loads(FROZEN.read_text())
new = json.loads((OUT / 'density.json').read_text())
different = {key: {'old': old.get(key), 'new': new.get(key)}
             for key in sorted(old.keys() | new.keys()) if old.get(key) != new.get(key)}
result = {'source_sha256': hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
          'frozen_json_sha256': hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
          'actual_game_inputs_saved': len(actual_inputs),
          'differences': different,
          'all_mathematical_and_generation_fields_equal': set(different) <= {'base_commit'},
          'source_change': 'none; audit_game wrapper only records arguments, then calls original function',
          'scope': 'finite exact original tests; arbitrary real proofs are separate',
          'summary': json.loads(stdout.getvalue())}
(OUT / 'comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key:value for key,value in result.items() if key != 'differences'}, ensure_ascii=False, indent=2))
assert len(actual_inputs) == 49 and result['all_mathematical_and_generation_fields_equal']
