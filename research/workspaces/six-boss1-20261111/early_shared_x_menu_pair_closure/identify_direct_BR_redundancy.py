#!/usr/bin/env python3
"""Record 42 exact BR+nonnegative identities, without altering the 306 packet.

This is a small explicit implication, not a general cone-independence test.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def main():
    input_paths = [WORK / 'early_shared_x_joint/symbolic_append.json.gz',
                   HERE / 'all_pair_candidates.json.gz', HERE / 'usable_pair_append.json.gz']
    before = {str(p.relative_to(WORK)): sha256(p.read_bytes()).hexdigest() for p in input_paths}
    old, candidates, append = [read(p) for p in input_paths]
    hist = {h['hist_column']: h for h in old['base_contract']['histograms']}
    records = []
    for branch in old['branches']:
        i = branch['source_player']
        z_query = branch['ordered_tail_labels'][-2]
        for raw in candidates['raw_pairs']:
            if raw['source_player'] != i or raw['usable_append_row_id'] is None:
                continue
            if raw['left_query'] == z_query:
                query = raw['right_query']
            elif raw['right_query'] == z_query:
                query = raw['left_query']
            else:
                continue
            comparisons = [v for v in old['raw_inequality_provenance']
                           if v['family'] == 'branch-terminal-BR' and v['branch_source_player'] == i and v['query'] == query]
            assert len(comparisons) == 1
            br = comparisons[0]
            oldrow = {j: F(a) for j, a in old['inequalities'][br['unique_row_id']]['row']}
            row = append['rows'][raw['usable_append_row_id']]
            newrow = {j: F(a) for j, a in row['row']}
            residual = {}
            for offset, col in enumerate(old['new_columns']):
                if col['source_player'] != i:
                    continue
                d = (hist[col['hist_column']]['actual_backgrounds'][i - 1] + col['X_bit']
                     + sum(col['middle_bits'][:-1]) + 1)
                z, t = col['middle_bits'][-1], col['terminal_bit']
                value = F(z * (1 - t), d * (d + 1))
                j = 21021 + offset
                assert newrow.get(j, F()) - oldrow.get(j, F()) == value >= 0
                if value:
                    residual[j] = value
            reconstructed = dict(oldrow)
            for j, value in residual.items():
                reconstructed[j] = reconstructed.get(j, F()) + value
                if not reconstructed[j]:
                    del reconstructed[j]
            assert reconstructed == newrow
            records.append({'source_player': i, 'raw_pair_id': raw['raw_pair_id'],
                            'append306_row_id': raw['usable_append_row_id'],
                            'old_BR_raw_row_id': br['raw_id'], 'old_BR_unique_row_id': br['unique_row_id'],
                            'query': query, 'nonnegative_mu_remainder': sparse(residual),
                            'identity': 'new TP(Z,R) = old branch-terminal-BR(R) + sum_mu z*(1-t)/(dloc*(dloc+1))'})
    assert len(records) == 42
    counts = Counter(v['source_player'] for v in records)
    assert counts == {1: 12, 2: 11, 3: 10, 4: 9}
    omitted = sorted(v['append306_row_id'] for v in records)
    assert len(set(omitted)) == 42
    retained = [v['id'] for v in append['rows'] if v['id'] not in set(omitted)]
    assert len(retained) == 264
    output = {'schema': 'direct-BR-redundancy-in-visible-pairs/v1', 'status': 'PASS_42_EXACT_IMPLICATIONS',
              'input_sha256': before, 'record_count': 42, 'counts_by_source': dict(counts),
              'records': records, 'append306_row_ids_omittable_with_certificate': omitted,
              'append306_row_ids_retained_after_this_one_rule': retained,
              'retained_rows': 264,
              'retained_nonzeros': sum(len(append['rows'][j]['row']) for j in retained),
              'claim': 'Keeping these 264 and the old436 plus mu>=0 implies all306. No independence or further irredundancy of the 264 is claimed.',
              'old436_and_306_packet_bytes_unchanged': True, 'optimizer_calls': 0}
    assert before == {str(p.relative_to(WORK)): sha256(p.read_bytes()).hexdigest() for p in input_paths}
    path = HERE / 'direct_BR_redundancy.json.gz'
    assert not path.exists()
    with path.open('wb') as stream:
        with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as f:
            f.write((json.dumps(output, indent=2, ensure_ascii=False) + '\n').encode())
    print(json.dumps({k: v for k, v in output.items() if k not in ('records', 'append306_row_ids_omittable_with_certificate',
                                                               'append306_row_ids_retained_after_this_one_rule')}, indent=2))


if __name__ == '__main__':
    main()
