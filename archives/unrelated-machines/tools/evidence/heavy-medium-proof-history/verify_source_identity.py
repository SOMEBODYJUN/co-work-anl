#!/usr/bin/env python3
"""Check archived byte identities only; never execute a mathematical program."""
from pathlib import Path
import hashlib
import json
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    stage = here.parents[4]
    manifest = json.loads((here / 'manifest.json').read_text())
    identities = []
    for group in ('originals', 'comparisons'):
        for row in manifest[group]:
            data = (stage / row['evidence_path']).read_bytes()
            assert len(data) == row['size'], row['id']
            assert sha(data) == row['sha256'], row['id']
            identities.append({'id': row['id'], 'size': len(data), 'sha256': sha(data)})
    final = (here / 'comparisons/unit_presence_two_witness_sharp_gluing.md').read_bytes()
    controls = [{'offset': i, 'byte': v} for i, v in enumerate(final)
                if (v < 32 and v != 10) or v == 127]
    assert not controls
    section = final.split(b'## 8.', 1)[1]
    commands = [b'\\tau', b'\\frac', b'\\varepsilon', b'\\right', b'\\tag']
    assert all(command in section for command in commands)
    prefix = final.split(b'## 8.', 1)[0]
    assert prefix.endswith(b'\n\n')
    restored = prefix[:-2]
    assert restored == (here / 'derived/unit_presence_pre_heavy_foundation.md').read_bytes()
    assert sha(restored) == '1d5d27a9a80c64dbcca319531da735f23b1d65e29d1ef1f16a011a85a4adf4ba'
    result = {
        'kind': 'byte-identity-verification-only',
        'python_version': sys.version,
        'frozen_sources_checked': len(identities),
        'identities': identities,
        'unexpected_ascii_controls_except_LF': controls,
        'final_formula_real_backslash_commands_present': [c.decode() for c in commands],
        'old_foundation_size': len(restored),
        'old_foundation_sha256': sha(restored),
        'old_foundation_exact_prefix_reconstruction': True,
        'old_bad_draft_materialized': False,
        'mathematical_programs_executed_this_batch': 0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
