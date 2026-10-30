#!/usr/bin/env python3
"""Run the untouched source once and record its actual function inputs/results."""
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'sources/tests/audits/unrelated_machines/equal_quantum_arbitrary_eligibility_flow.py'
records = []
pending = {}


def encode(v):
    if isinstance(v, (list, tuple)):
        return [encode(x) for x in v]
    if isinstance(v, dict):
        return {k: encode(x) for k, x in v.items()}
    if hasattr(v, 'denominator') and not isinstance(v, int):
        return str(v)
    return v


def profile(frame, event, arg):
    if frame.f_code.co_filename != str(SRC) or frame.f_code.co_name != 'feasible_assignments':
        return
    if event == 'call':
        pending[id(frame)] = {k: encode(frame.f_locals[k]) for k in ('nh', 'E', 'p', 'u', 'T', 'H', 'Z')}
    elif event == 'return':
        rec = pending.pop(id(frame))
        rec['enumerated_feasible_assignments'] = len(arg)
        records.append(rec)


start = time.monotonic()
sys.setprofile(profile)
try:
    runpy.run_path(str(SRC), run_name='__main__')
finally:
    sys.setprofile(None)
(ROOT / 'original-actual-inputs.json').write_text(json.dumps(records, indent=2) + '\n')
(ROOT / 'original-run.json').write_text(json.dumps({
    'source_sha256': hashlib.sha256(SRC.read_bytes()).hexdigest(),
    'entry': 'untouched source via runpy; profile records calls without changing arguments/results',
    'seed': 20261017, 'function_calls': len(records),
    'boundary_calls': 1, 'random_calls': len(records)-1,
    'feasible_calls': sum(bool(x['enumerated_feasible_assignments']) for x in records),
    'feasible_assignment_records': sum(x['enumerated_feasible_assignments'] for x in records),
    'elapsed_seconds': time.monotonic()-start,
    'scope': 'Two direct enumerations of the same scheduling predicate; no max-flow implementation in original.',
}, indent=2) + '\n')
