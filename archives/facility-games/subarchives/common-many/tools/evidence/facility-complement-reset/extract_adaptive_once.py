#!/usr/bin/env python3
"""Execute the preserved adaptive main once, retaining its returned fixture rows."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import runpy

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--script', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
assert not args.output.exists()
namespace = runpy.run_path(str(args.script.resolve()), run_name='__main__')
# The original __main__ already called audit() and audit(True); do not call again.
base, augmented = namespace['base'], namespace['extra']
def maximum(data):
    return str(max(Fraction(r['deviator'], r['a']) for r in data['all_labeled_deviations']))
result = {'original_script_sha256': hashlib.sha256(args.script.read_bytes()).hexdigest(),
          'execution': 'Original __main__ executed once by runpy; no repeated audit() call.',
          'base': base, 'augmented': augmented,
          'maximum_selected_gain_base': maximum(base),
          'maximum_selected_gain_augmented': maximum(augmented)}
args.output.write_text(json.dumps(result, indent=2) + '\n')
