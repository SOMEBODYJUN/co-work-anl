"""Exact first audit of the legitimate aligned product construction."""
from collections import defaultdict
from fractions import Fraction as F
from common import HERE, BASE, read_sources, digest, product_atoms, eval_interface, rows_json, write_json


def main():
    frozen, root, product, hist = read_sources()
    atoms = product_atoms(product, hist)
    old_margin, new_margin = defaultdict(F), defaultdict(F)
    for atom in atoms:
        old_margin[atom['original_column_index']] += F(atom['mass'])
        new_margin[atom['joint_atom_index']] += F(atom['mass'])
    assert all(old_margin[i] == F(h['weight']) for i, h in hist.items())
    assert all(new_margin[j] == F(r['mass']) for j, r in enumerate(root['support']))
    values = eval_interface(atoms)
    out = {'status': 'PASS' if min(values.values()) >= 0 else 'FIXED ALIGNED PRODUCT FAILS',
           'scope': 'Only this aligned product; no general infeasibility or SPE claim.',
           'point_sha256': frozen['point_sha256'],
           'symmetry': 'Each atom is followed by a common uniform S6 permutation of old and new indices.',
           'zero_root_coupling': 'Uniform independent zero-index permutation conditional on old-hist/new-root pair; t=1 is aligned.',
           'orbit_atom_count': len(atoms), 'literal_atom_count_before_merging': 720*len(atoms),
           'preserved_old_hist_margins': len(hist), 'preserved_root_atom_margins': len(root['support']),
           'interface_rows': rows_json(values), 'negative_row_count': sum(v < 0 for v in values.values()),
           'atoms': atoms}
    write_json(HERE / 'aligned_product_exact.json', out)
    sources = []
    for path in [BASE / 'peer_augmented_lp/augmented_lp_exact.json',
                 BASE / 'cross_root_pricing/projection_inputs_exact.json',
                 BASE / 'cross_root_pricing/joint_completion_exact.json',
                 BASE / 'cross_root_pricing/original_hist_refinement_exact.json']:
        sources.append({'path': str(path.relative_to(BASE)), 'sha256': digest(path)})
    write_json(HERE / 'input_snapshot_exact.json', {'sources': sources, 'projection_inputs': frozen,
               'new_root_certificate': root, 'old_product_refinement': product})
    print(out['status'])
    print('orbit atoms', len(atoms), 'negative rows', out['negative_row_count'])
    for row in out['interface_rows']:
        print(row['row'], row['float'])


if __name__ == '__main__':
    main()
