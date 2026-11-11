"""Read-only exact append API; this module neither optimizes nor loads a point.

The caller owns its base matrix.  iter_rows() yields homogeneous sparse rows
in a deterministic append layout, preserving all old indices 0..21020.
There is no call which edits or replaces frozen23676 input files.
"""
from fractions import Fraction
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def read(name):
    with gzip.open(HERE / name, 'rt') as stream:
        return json.load(stream)


def layout(scope='extended'):
    if scope not in ('direct', 'extended'):
        raise ValueError('scope must be direct or extended')
    if scope == 'extended':
        return json.loads((HERE / 'append_index_map.json').read_text())['blocks']
    return [dict(namespace=name, offset=offset, count=count) for name, offset, count in (
        ('old', 0, 21021), ('mu', 21021, 1216), ('inherited_root_aux', 22237, 2700),
        ('inherited_root_lower', 24937, 9572), ('eta', 34509, 1216))]


def iter_rows(scope='extended', include_root=True):
    """Yield {origin,name,sense,terms,rhs}; sense is >= or =, rhs is always 0.

    Term coefficients are canonical rational strings.  All columns after the
    old 21021 are nonnegative variable domains, not extra inequality rows.
    If the caller already has the matching 438-principal root system, use
    include_root=False and preserve the namespace mapping returned by layout.
    """
    offsets = {d['namespace']: d['offset'] for d in layout(scope)}

    def emit(row, mapping, origin, sense):
        terms = []
        for source, target in mapping.items():
            terms.extend((offsets[target]+i, c) for i, c in row.get(source, []))
        terms.sort()
        assert len({i for i, _ in terms}) == len(terms)
        return dict(origin=origin, name=row['name'], sense=sense, terms=terms, rhs='0')

    if include_root:
        with gzip.open(BASE / 'root_sorting_20910/symbolic_matrix_exact.json.gz', 'rt') as stream:
            root = json.load(stream)
        mapping = dict(old='old', mu='mu', aux='inherited_root_aux', lower='inherited_root_lower')
        for row in root['rows']:
            yield emit(row, mapping, 'inherited_root_438', '>=')
        for row in root['equalities']:
            yield emit(row, mapping, 'inherited_root_mu_mass', '=')
    filename = 'direct_interface_exact.json.gz' if scope == 'direct' else 'extended_interface_exact.json.gz'
    data = read(filename)
    mapping = {name: name for name in ('old', 'mu', 'eta', 'z', 'cost') if name in offsets}
    families = ['rows', 'eta_upper_rows'] if scope == 'direct' else [
        'principal_rows', 'eta_upper_rows', 'z_upper_rows', 'sorting_piece_rows']
    for family in families:
        for row in data[family]:
            yield emit(row, mapping, family, '>=')
    for row in data['eta_equalities']:
        yield emit(row, mapping, 'shared_eta_mass', '=')


def evaluate_exact(terms, values):
    """Evaluate a supplied exact vector. No input vector is read or inferred."""
    return sum((Fraction(c)*Fraction(values[i]) for i, c in terms), Fraction())


def audit_layout():
    """Validate index relocation only; this is not an SPE or LP feasibility test."""
    result = {}
    for scope in ('direct', 'extended'):
        columns = layout(scope)
        dimension = sum(d['count'] for d in columns)
        rows, equalities, coefficients = 0, 0, 0
        for row in iter_rows(scope):
            assert all(0 <= i < dimension for i, _ in row['terms'])
            assert all(str(Fraction(v)) == v and Fraction(v) for _, v in row['terms'])
            rows += row['sense'] == '>='
            equalities += row['sense'] == '='
            coefficients += len(row['terms'])
        assert equalities == 76
        result[scope] = dict(columns=dimension, appended_inequalities=rows,
                             appended_equalities=equalities, appended_nonzeros_including_equalities=coefficients,
                             combined_inequalities_if_base23676=23676+rows)
    assert result['direct']['appended_inequalities'] == 38034
    assert result['extended']['appended_inequalities'] == 75708
    return result


if __name__ == '__main__':
    receipt = dict(status='EXACT_APPEND_NAMESPACE_AUDIT_PASS', scopes=audit_layout(),
                   point_vectors_evaluated=0, optimizer_calls=0, frozen_parent_matrix_written=False)
    (HERE / 'append_api_verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, sort_keys=True))
