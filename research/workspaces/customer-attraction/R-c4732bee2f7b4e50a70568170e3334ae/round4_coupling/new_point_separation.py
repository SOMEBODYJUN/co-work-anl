"""Reproduce exact final-menu separation of round4's unrestricted-type point."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
from joint_transport import ACTOR, frozen_report

source = ACTOR / 'round4_pricing/exact_primal_overlap1.json'
document = json.loads(source.read_text())
report = frozen_report(document['atoms'], [F(z['exact_mass']) for z in document['atoms']])
report['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
report['scope'] = 'Exact necessary joint cross-menu cuts on the new 60-atom full-universe '
report['scope'] += '557-row point, not a full SPE'
Path(__file__).with_name('new_point_joint_transport.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'source_sha256': report['source_sha256'],
                  'rows': report['row_count'],
                  'negative_rows': len(report['negative_rows']),
                  'literal_matching_checks': report['literal_matching_checks']}, indent=2))
