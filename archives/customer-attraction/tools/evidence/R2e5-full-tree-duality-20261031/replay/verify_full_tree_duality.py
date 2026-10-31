from pathlib import Path
import hashlib, json

base = Path(__file__).resolve().parent.parent
src = base / 'source'
rep = base / 'replay'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected = {
    'audit_omitted_deletion.py': '7a32c282f80320f22d9323276a3b664103ce89e5e2af284891a41e991a71846f',
    'global_customer_gluing_verification.json': 'f3694c27451d1fe2f796cc438181d5e616f335aa5d73bca86a8cb3cdeab18491',
    'omitted_deletion_independent_audit.json': '26ea8648c6b8ab6c8a41d95b9d257f639a9b541b512cb8ad41e93874421ca4c5',
    'verify_global_customer_gluing.py': 'd7ddc1bcb63060ee588429d103ff512aac72186a0d49cc9c661c8085ef31f717',
}
for name, digest in expected.items():
    assert sha(src / name) == digest, (name, sha(src / name))

# Global gluing verification is deterministic and byte-identical.
global_src = json.loads((src / 'global_customer_gluing_verification.json').read_text())
global_out = json.loads((rep / 'global_gluing.stdout.txt').read_text())
assert global_src == global_out
assert global_src['m'] == 2 and global_src['k'] == 4 and global_src['p'] == 9
assert global_src['terminal_counts'] == 45
assert global_src['payoff_vertices'] == 81
assert global_src['pairs_with_explicit_common_nonnegative_realization'] == 990
assert global_src['sharp_dilution_comparisons'] == 729
assert global_src['complete_ordered_histories'] == 10
assert global_src['SPE_graph_comparisons'] == 90
assert global_src['hypermetric_value'] == '-8'

# Omitted-deletion audit differs only in the path string when run in a new layout.
om_src = json.loads((src / 'omitted_deletion_independent_audit.json').read_text())
om_out = json.loads((rep / 'omitted_deletion_independent_audit.generated.json').read_text())
assert om_src['exact'] is True and om_out['exact'] is True
assert om_src['scope'] == om_out['scope']
assert om_src['target'] == om_out['target'] == [2, 1, 0, 0, 2]
assert om_src['original']['target_realizable'] is True
assert om_src['deleted']['target_realizable'] is False
assert om_src['original']['customer_count'] == 36
assert om_src['deleted']['customer_count'] == 35
assert om_src['original']['root_outcomes'] == om_out['original']['root_outcomes']
assert om_src['deleted']['root_outcomes'] == om_out['deleted']['root_outcomes']
assert om_src['deleted']['exclusion_tree'] == om_out['deleted']['exclusion_tree']
assert om_src['source'].endswith('/omitted_deletion/reduced.json')
assert om_out['source'].endswith('/omitted_deletion/reduced.json')
assert sha(rep / 'reduced.json') == '6323f6d761c537aaeee50b17a6ae3ffa8f53d36b2c7879de40856fedd4162fe5'
assert (rep / 'audit_omitted_deletion.stderr.txt').read_bytes() == b''
assert (rep / 'global_gluing.stderr.txt').read_bytes() == b''
print('PASS')
