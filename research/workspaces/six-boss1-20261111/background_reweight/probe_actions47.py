"""One exact check of genuinely new rows on the cloud 47-atom lower point.

The older 65-atom certificate is a different measure. No optimizer is run.
The repeated-Z test uses the already frozen rational 19-parameter row only.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
from hidden_z_probe import ROWS, hidden_z_value


def main():
    point_path = HERE/'actions_full/exact_lower_certificate.json'
    point = json.loads(point_path.read_text())
    assert len(point['atoms']) == 47
    mass_z = sum(F(a['mass'])*a['witness']['background'] for a in point['atoms'])
    K = F(point['capacity_mass'])
    rows = {'MAX:Z': K-mass_z}
    for tag, seat in ROWS:
        rows[f'{tag}:{seat}:K:Z'] = sum(F(a['mass'])*hidden_z_value(a['witness'], tag, seat) for a in point['atoms'])
    # Independent Bellman implementation: no numerical discovery import.
    check_path = HERE/'repeated_z_price/verify_one.py'
    spec = importlib.util.spec_from_file_location('fixed_ZZ_independent', check_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    prior_path = HERE/'repeated_z_price/single_case_result.json'
    prior = json.loads(prior_path.read_text())
    weights = list(map(F, prior['parameters']))
    masses = defaultdict(F)
    utility = [F(0)]*5
    for atom in point['atoms']:
        w = atom['witness']
        b, bits, d, mass = w['background'], tuple(map(int, w['bits'])), w['d'], F(atom['mass'])
        masses[b, bits, d] += mass
        for i in range(5):
            utility[i] += mass*module.frac(bits[i], b+sum(bits[:5]))
    wallet = [utility[0], 3*utility[4], utility[4], 3*K, K]+[F(0)]*14
    value = sum(w*v for w, v in zip(weights, wallet))
    checks = 0
    table = []
    for key, mass in sorted(masses.items()):
        psi, minimum, count = module.check_bellman(key, weights)
        value -= mass*psi[3*key[0]]
        checks += count
        table.append({'background': key[0], 'bits': ''.join(map(str, key[1])), 'd': key[2], 'mass': str(mass),
                      'psi': list(map(str, psi)), 'initial_value': str(psi[3*key[0]]), 'min_bellman_slack': str(minimum)})
    out = {'status': 'EXACT-CLOUD-47-ATOM-NEW-ROW-CHECK', 'point_sha256': hashlib.sha256(point_path.read_bytes()).hexdigest(),
           'atoms': len(point['atoms']), 'background_mass': str(mass_z), 'capacity_mass': str(K),
           'row_values': {n: str(v) for n, v in rows.items()}, 'row_values_float': {n: float(v) for n, v in rows.items()},
           'negative_rows': [n for n, v in rows.items() if v < 0],
           'repeated_Z_fixed_row_source_sha256': hashlib.sha256(prior_path.read_bytes()).hexdigest(),
           'repeated_Z_fixed_row_slack': str(value), 'repeated_Z_fixed_row_slack_float': float(value),
           'repeated_Z_fixed_row_negative': value < 0, 'repeated_Z_parameters': prior['positive_parameters'],
           'repeated_Z_scope': 'Frozen one row from the 65-atom study; not a new full 19-parameter optimization on 47 atoms.',
           'literal_middle_word_bellman_checks': checks, 'repeated_Z_type_table': table,
           'not_an_SPE_counterexample': True}
    (HERE/'actions47_new_row_audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('row_values', 'repeated_Z_type_table')}, indent=2))


if __name__ == '__main__':
    main()
