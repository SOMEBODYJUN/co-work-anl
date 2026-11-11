"""Exact, read-only fixed-point own-X diagnostic; never optimizes X or y.

Input is a future 21021-column exact point JSON with columns[*].weight and the
frozen coordinate descriptors.  Output is restricted to this owned directory.
Neither the old cb45 point nor any solver array is evaluated by the build/check
commands in this package.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def exact(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError('Require exact integer or rational-string weights, not floating values.')
    return F(value)


def evaluate_block(block, values):
    H, x, yq, yr = [values[block[k]] for k in ('H_column', 'X_column', 'yQ_column', 'yR_column')]
    m = {s: sum((F(c) * values[j] for j, c in row), F())
         for s, row in block['mass_by_QR'].items()}
    q, r = m['10'] + m['11'], m['01'] + m['11']
    old = dict(H=H, x=x, H_minus_x=H-x, yQ=yq, yR=yr, x_minus_yQ=x-yq,
               x_minus_yR=x-yr, q_minus_yQ=q-yq, r_minus_yR=r-yr,
               **{f'm{s}': v for s, v in m.items()})
    facets = [yq+yr-x+m['00'], m['10']-yq+yr, m['01']+yq-yr,
              m['00']+m['10']-x+yr, m['00']+m['01']-x+yq, x+m['11']-yq-yr]
    lower = [F(), yq-m['10'], yr-m['01'], yq+yr-x]
    upper = [m['11'], yq, yr, m['00']-x+yq+yr]
    L, U = max(lower), min(upper)
    preconditions = all(v >= 0 for v in old.values()) and sum(m.values(), F()) == H
    feasible = preconditions and L <= U
    assert (preconditions and all(v >= 0 for v in facets)) == feasible
    result = dict(block=block['block'], key=block['key'], H=str(H), x=str(x), yQ=str(yq), yR=str(yr),
                  old_masses={s: str(v) for s, v in m.items()},
                  preconditions_pass=preconditions,
                  failed_preconditions={s: str(v) for s, v in old.items() if v < 0},
                  mass_identity_residual=str(sum(m.values(), F())-H),
                  six_facet_slacks=list(map(str, facets)), beta_lower=list(map(str, lower)),
                  beta_upper=list(map(str, upper)), L=str(L), U=str(U), interval_gap=str(U-L),
                  fixed_values_complete=feasible)
    if feasible:
        beta = L
        psi = {'00': x-yq-yr+beta, '10': yq-beta, '01': yr-beta, '11': beta}
        assert all(0 <= psi[s] <= m[s] for s in m)
        result['beta_witness'] = str(beta)
        result['X1_four_cells'] = {s: str(v) for s, v in psi.items()}
        result['X0_four_cells'] = {s: str(m[s]-psi[s]) for s in m}
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--point', type=Path, required=True)
    p.add_argument('--output', type=Path, default=HERE/'own_diagnostic.json')
    args = p.parse_args()
    target = args.output.resolve()
    if not target.is_relative_to(HERE):
        raise ValueError('Output must remain inside root_x_joint_contract/.')
    mapping = json.loads((HERE/'own_blocks.json').read_text())
    point = json.loads(args.point.read_text())
    cols = point['columns']
    if len(cols) != mapping['coordinate_count']:
        raise ValueError('Require the exact full-X 21021-column coordinate vector.')
    selected = [[j, {k: v for k, v in cols[j].items() if k != 'weight'}]
                for j in mapping['expected_column_indices']]
    if sha256(canonical(selected)).hexdigest() != mapping['expected_descriptor_sha256']:
        raise ValueError('Frozen own-interface descriptor identity mismatch.')
    values = [exact(c['weight']) for c in cols]
    blocks = [evaluate_block(b, values) for b in mapping['blocks']]
    bad = [b['block'] for b in blocks if not b['fixed_values_complete']]
    output = dict(status='FIXED_OWN_X_VALUES_COMPLETE' if not bad else 'FIXED_OWN_X_VALUES_FAIL',
                  point_path=str(args.point.resolve()), point_sha256=sha256(args.point.read_bytes()).hexdigest(),
                  blocks_checked=len(blocks), failed_blocks=bad,
                  scope='Only the supplied exact X and y values. No claim about reselecting y or X; no LP or SPE test.',
                  original_22297_rows_rechecked=False, blocks=blocks)
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: output[k] for k in ('status', 'blocks_checked', 'failed_blocks', 'scope')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
