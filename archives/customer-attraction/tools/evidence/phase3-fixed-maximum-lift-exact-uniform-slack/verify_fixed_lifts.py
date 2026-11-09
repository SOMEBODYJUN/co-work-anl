"""Verify the two fixed uniform-slack optima with the Python standard library."""
import argparse
import ast
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


CODE = Path('archives/customer-attraction/tools/evidence/Boss7-resume-rcd-joint/original/lift_maximum_branch.py')
CODE_SHA = '992322af0933458b28d0cbf36e1197247f6b4afeb116e4acabbc95f31f432ce3'
CAP = 'max:cap:second:menu3'
BNS = 'max:BNS:optimal-sum'
INPUTS = (
    ('ap_binary_discovery.json', '244b860746a96682b29d50998d9010877d545b1f122686d7da18eb49fef62f59',
     'maximum_lift_ap_binary_discovery.json', '2e7e3c2c5df5aea48d83513e1c23825e853786650958e7efff49f1e52bceb87b',
     True, 72, 540, F(39573170198126625479863, 114000000000000000000000)),
    ('exact_optimum_primal_joint_terminal.json', 'b5ec102366191aea06e4a7a93073a7913bd625101c743cc5ccc8f9132d744b05',
     'maximum_lift_exact_optimum_primal_joint_terminal_noap.json', 'ffed8a8b1e6395db048119eea4d81fb5e9a67ef9176c6084a49f8e91f7d373ea',
     False, 65, 236, F(12406197488207545300181345254156935793975, 33625231693246534564111099661179845265856)),
)


def frozen(path, expected):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == expected, path
    return raw


def load_rows(root):
    path = root / CODE
    module = ast.parse(frozen(path, CODE_SHA).decode())
    bindings = {'LABELS', 'PATHS', 'START', 'STATES', 'TY3', 'TY4', 'TY5'}
    selected = [node for node in module.body if
                (isinstance(node, ast.FunctionDef) and node.name in {'q', 'rows'}) or
                (isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id in bindings for t in node.targets))]
    assert len(selected) == len(bindings) + 2
    env = {'F': F, 'product': product, 'combinations_with_replacement': combinations_with_replacement}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), 'exec'), env)
    assert env['STATES'] == list(product((0, 1), repeat=5))
    return env['rows'], env['TY4']


def verify(root, certificate_dir, rows, ty4, record):
    filename, input_sha, report_name, report_sha, ap, support_size, row_count, epsilon = record
    cert = json.loads((certificate_dir / filename).read_bytes())
    assert cert['ap'] is ap and F(cert['epsilon']) == epsilon > 0
    assert (cert['expected_support'], cert['row_count']) == (support_size, row_count)
    assert cert['source_sha256'] == input_sha and Path(cert['source_path']).name == filename
    original = json.loads(frozen(root / cert['source_path'], input_sha))
    report = json.loads(frozen(root / CODE.parent / report_name, report_sha))
    assert report['source_sha256'] == input_sha and report['source_exact'] is not ap
    names = report['row_names']
    assert len(names) == len(set(names)) == report['new_rows'] == row_count
    assert report['source_support'] == support_size and report['new_states_per_atom'] == 32
    atoms = original['atoms']
    masses = [F(str(v)) for v in original['primal_float']] if ap else [F(a['exact_mass']) for a in atoms]
    assert len(masses) == len(atoms)
    support = [(atom, mass) for atom, mass in zip(atoms, masses) if mass > F(1, 10**10)]
    assert len(support) == support_size

    dual_sum = F(0)
    for atom, mass in support:
        bits = list(map(int, atom['bits'][:5]))
        root_share = F(bits[0], sum(bits)) if bits[0] else F(0)
        menu = sum(multiplicity * state[3] for multiplicity, state in zip(atom['second_hist'], ty4))
        assert len(atom['AB_hist']) == 8 and len(atom['second_hist']) == 16
        d = sum(atom['AB_hist'][4:])
        assert d == 1
        for m in (0, 1):
            cap = 5 * m - menu
            bns = 400 * root_share - 75 * m - (5 - 4 * m) * d
            assert 71 * cap + 5 * bns == 2000 * root_share - 71 * menu - 25
        dual_sum += mass * (2000 * root_share - 71 * menu - 25)
    assert dual_sum == -76 * epsilon

    sums = [F(0) for _ in support]
    residual = dict.fromkeys(names, epsilon)
    seen = set()
    for term in cert['split']:
        i, bits, weight = term['source_atom'], term['bits'], F(term['mass'])
        assert type(i) is int and 0 <= i < support_size and len(bits) == 5 and set(bits) <= {'0', '1'}
        assert weight > 0 and (i, bits) not in seen
        seen.add((i, bits))
        sums[i] += weight
        col = rows(support[i][0], tuple(map(int, bits)), ap)
        assert list(col) == names
        for name in names:
            residual[name] += weight * col[name]
    assert sums == [mass for _, mass in support] and len(seen) == 83
    assert min(residual.values()) == residual[CAP] == residual[BNS] == 0
    assert F(cert['minimum_other_slack']) == min(v for k, v in residual.items() if k not in {CAP, BNS})
    return {'input': filename, 'source_atoms': support_size, 'rows': row_count,
            'positive_splits': len(seen), 'exact_minimum_uniform_slack': str(epsilon),
            'zero_rows': [name for name, slack in residual.items() if slack == 0]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    args = parser.parse_args()
    rows, ty4 = load_rows(args.repo)
    certificate_dir = Path(__file__).resolve().parent
    print(json.dumps([verify(args.repo, certificate_dir, rows, ty4, x) for x in INPUTS], indent=2))


if __name__ == '__main__':
    main()
