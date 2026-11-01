"""New 64-by-five exact endpoint reconstruction of the frozen rho table.

This does not import or execute either historical audit. It does not enumerate
the original 2058/3528 coefficient domains, games, or SPEs. The accompanying
proof reduces each 49-point minimum to five explicit endpoints.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import hashlib
import json
import sys
import argparse

HERE = Path(__file__).resolve().parent
PRIMARY = HERE / 'original.json'
AUTHOR = HERE.parent / 'threefold-early-auditor/original/research_1/threefold_penultimate_exact.json'
HASHES = {
    PRIMARY: '6b3ff9871170e1179e8d3df35c5e042788d33791541f82e803804faa88889783',
    AUTHOR: '7adcce9a18beb2654c5fe1a4ef5dc45d8d130e8426f81928243cedd6ea75d35a',
}
LAM = (F(1, 3), F(1, 2), F(1, 2), F(2, 3))
ENDPOINTS = ((0, 0), (1, 0), (1, 6), (6, 0), (6, 6))


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions are required.')
    for path, expected in HASHES.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
    source = json.loads(PRIMARY.read_text())
    author = json.loads(AUTHOR.read_text())
    assert set(source) == {
        'status', 'scope', 'reduced_state_count', 'state_count_with_overlap',
        'minimum_residual', 'rho_table_equal_to_author',
        'minimum_A_residual_by_early_load', 'rho_actual_membership',
    }
    assert source['status'] == 'passed'
    assert source['scope'] == 'conditional HALF-6 and unrestricted residual formula only'
    assert source['rho_table_equal_to_author'] is True
    table = {}
    minimizers = {}
    by_load = {}
    for e in product((0, 1), repeat=4):
        p = sum(e)
        for a, b in product((0, 1), repeat=2):
            c = p + a + b
            eta = sum((w * bit for w, bit in zip(LAM, e)), F(0))
            # Collect all actual-share terms before minimizing comparison counts.
            constant = 2 * int(c > 0)
            if c:
                constant -= (6 * a + 2 * b + eta) / c
            constant += a * sum((LAM[i] / (sum(e[:i]) + 6 - i) for i in range(4)), F(0))
            constant += F(3 * a, 2 * (p + a + 1))

            values = {}
            for d, ell in ENDPOINTS:
                reduced = (-int(d > 0) + F(d, p + 1)
                           + F(ell, 12 * (p + a + 1))
                           - F(d * ell, 6 * (p + 1) * (p + 2)))
                values[(d, ell)] = constant + reduced
            key = ''.join(map(str, (*e, a, b)))
            value = min(values.values())
            table[key] = str(value)
            minimizers[key] = [list(t) for t, val in values.items() if val == value]
            if a:
                by_load[p] = min(by_load.get(p, value), value)
    assert len(table) == 64 and table == source['rho_actual_membership']
    assert table == author['rho_actual_membership']
    grouped = {str(k): str(by_load[k]) for k in range(5)}
    assert grouped == source['minimum_A_residual_by_early_load']
    reduced_count = (2**4 + comb(4, 3) + comb(4, 4)) * 2 * 7**2
    overlap_count = (2**4 + comb(4, 3) + comb(4, 4)) * 2 * comb(9, 3)
    assert reduced_count == source['reduced_state_count'] == 2058
    assert overlap_count == source['state_count_with_overlap'] == 3528
    assert reduced_count == author['complete_restricted_state_count']
    p3 = {key: F(value) for key, value in table.items()
          if key[4] == '0' or sum(map(int, key[:4])) >= 3}
    assert len(p3) == 42 and min(p3.values()) == F(source['minimum_residual']) == 0
    minima_keys = {str(k): [key for key, value in table.items()
                          if key[4] == '1' and sum(map(int, key[:4])) == k
                          and F(value) == by_load[k]] for k in range(5)}
    values = list(map(F, table.values()))
    return {
        'status': 'PASS_CURRENT_FIVE_ENDPOINT_RECONSTRUCTION',
        'scope': '64 ordered actual membership patterns times five analytically sufficient endpoints; report field and input equality checks, not either original program replay.',
        'python_version': sys.version,
        'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_sha256': {str(path.relative_to(HERE.parent)): sha for path, sha in HASHES.items()},
        'actual_patterns': 64, 'endpoint_evaluations': 320,
        'endpoints': ENDPOINTS, 'rho_table_equal_to_primary_and_author': True,
        'rho_actual_membership': table, 'minimizing_endpoints': minimizers,
        'sign_counts': {'negative': sum(x < 0 for x in values),
                        'zero': sum(x == 0 for x in values),
                        'positive': sum(x > 0 for x in values)},
        'p3_actual_patterns': len(p3), 'p3_minimum_rho': str(min(p3.values())),
        'global_minimum_rho': str(min(values)),
        'minimum_A_residual_by_early_load': grouped, 'minimum_A_actual_keys': minima_keys,
        'domain_sizes_by_combinatorial_formula': {'reduced_p3': reduced_count, 'with_h_p3': overlap_count},
        'author_fields_actually_compared': ['rho_actual_membership', 'complete_restricted_state_count'],
        'author_fields_not_asserted': sorted(set(author) - {'rho_actual_membership', 'complete_restricted_state_count'}),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
