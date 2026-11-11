#!/usr/bin/env python3
"""Read-only replay of the coverage-union bridge and root coverage corollary."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

w = Path(__file__).resolve().parent
report = json.loads((w / 'main_optimal_union_prefix.json').read_text())
assert report['proof_sha256'] == hashlib.sha256((w / 'main_optimal_union_prefix.md').read_bytes()).hexdigest()
assert report['parent_type_audit_sha256'] == hashlib.sha256((w / 'main_averaged_menu_prefix.json').read_bytes()).hexdigest()
checks = 0
for den in range(1, 7):
    for mask in range(64):
        d = mask.bit_count()
        o = int(d > 0)
        gain = F(d - o, 6 * den)
        assert F(d, 6 * den) - F(o, 6 * den) == gain >= 0
        checks += 1
assert checks == report['exact_BR_weakening_checks'] == 384
# Coefficients in the root u1 inequality and the five remaining SAFE inequalities.
assert F(5, 31) + F(5, 6) == F(1110, 1116)
assert F(1, 6 * 31) == F(6, 1116)
assert F(-5, 36 * 31) == F(-5, 1116)
assert F(1105) * F(report['half_threshold']) + 6 == 558
assert F(5, 6) == F(930, 1116)
assert F(5, 31) == F(180, 1116)
assert F(180 - 5, 1116) == F(175, 1116)
print(json.dumps({'status': 'PASS_READ_ONLY_UNION_BRIDGE', 'literal_checks': checks,
                  'threshold': report['half_threshold'], 'optimizer_calls': 0}))
