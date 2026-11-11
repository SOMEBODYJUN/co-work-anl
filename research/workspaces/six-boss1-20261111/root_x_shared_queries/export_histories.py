"""Export exact ordered-history and wallet provenance for every query token."""
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent


def label(token):
    f, k, ids = token
    if f == 'A':
        return f'A{k+1}'
    if f in ('T', 'B', 'C'):
        return f'{f}_{ids[0]+1}'
    if f in ('R', 'Z'):
        return f'{f}_({k},{ids[0]+1},{ids[1]+1})'
    if f == 'H':
        return f'H{k+1}'
    if f == 'Y':
        return f'Y_({ids[0]+1},{k+1})'
    return 'X'


def provenance(token):
    f, k, ids = token
    record = dict(token=token, label=label(token))
    if f == 'X':
        return dict(record, selection='One fixed argmax of sum_X 1/(P+1) over the original legal label catalog.',
                    selection_prefix=['A1', 'A2', 'A3', 'A4'], no_comparison_index=True)
    if f == 'T':
        return dict(record, origin='fixed legal comparison label; forced root action is not presumed optimal')
    if f == 'A':
        prefix, player = [f'A{i+1}' for i in range(k)], k+1
    elif f in ('B', 'C'):
        prefix = ['A1', 'A2', 'A3', f'T_{ids[0]+1}']
        if f == 'C':
            prefix += [f'B_{ids[0]+1}']
        player = 5 if f == 'B' else 6
    elif f == 'R':
        prefix = ['A1', 'A2', 'A3', f'T_{ids[0]+1}', f'{("B", "C")[k]}_{ids[1]+1}']
        player = 6
    elif f == 'Z':
        prefix = ['A1', 'A2', 'A3', 'A4', label(('R', k, ids))]
        player = 6
    elif f == 'H':
        prefix = ['A1', 'A2', 'A3', 'A6'] + (['H1'] if k else [])
        player = 5+k
    else:
        prefix = [f'T_{ids[0]+1}']+[f'Y_({ids[0]+1},{i+1})' for i in range(k)]
        player = k+2
    return dict(record, source_player=player, ordered_prefix=prefix,
                origin='action prescribed by the same complete pure strategy at this exact prefix')


def main():
    with gzip.open(HERE/'query_orbits_exact.json.gz', 'rt') as f:
        inv = json.load(f)
    with gzip.open(HERE/'direct_interface_exact.json.gz', 'rt') as f:
        direct = json.load(f)
    queries = [provenance(q) for k in ('old_catalog', 'X_catalog', 'root_catalog') for q in inv[k]]
    rows = []
    for row in direct['rows']:
        name = row['name']
        if name[0] == 'RX':
            k = name[1]
            record = dict(name=name, source_player=k+1,
                          ordered_prefix=['T_i']+[f'Y_i{j}' for j in range(1, k)],
                          query='X', budget=f'only the true income of Y_i{k}',
                          following_players=5-k, lemma='true IC plus SAFE denominator bound')
        elif name[0] in ('RPQ', 'RXX'):
            q = 'X' if name[0] == 'RXX' else ('T_i' if name[1] == 0 else f'Y_i{name[1]}')
            record = dict(name=name, source_player=5,
                          ordered_prefix=['T_i', 'Y_i1', 'Y_i2', 'Y_i3'],
                          pair_query=['X', q], budget='root true fifth income + root true sixth income + J_p(Y_i4,Y_i4)',
                          helper='R=sigma6(T_i,Y_i1,Y_i2,Y_i3,X), shared by all three true ICs',
                          lemma='strong PAIR; remainder J_p(Y_i4,Y_i4)-J_p(Y_i4,R)')
        else:
            record = dict(name=name, ordered_prefix=['A1', 'A2', 'A3', 'A4'],
                          budget={'XM':'C=B_P(X)', 'XC':'actual fifth income a', 'RC-SAME':'a+C'}[name[0]],
                          lemma={'XM':'fixed X maximizes B_P', 'XC':'same-X cap a>=U_P(Q,X)',
                                 'RC-SAME':'same-X RC a+C>=Phi_P(Q,R)'}[name[0]])
        record['root_index_average'] = 'uniform over the six named roots; X itself is not renamed'
        rows.append(record)
    out = dict(query_count=189, query_provenance=queries, direct_row_provenance=rows,
               root_PAIR_provenance=dict(row_count=41, source_prefix=['T_i','Y_i1','Y_i2','Y_i3'],
                                         queries='(X,Q) for every one of the 189 legal expressions',
                                         wallet='true root last-two incomes + self-tax of Y_i4'),
               actual_RC_provenance=dict(unordered_rows=185, ordered_orbits=360,
                                         source_prefix=['A1','A2','A3','A4'],
                                         queries='every unordered pair containing at least one of 30 named Y tails',
                                         wallet='a+C'),
               known_alias='R_(0,i,i)=C_i is omitted as a separate R expression; empty labels, repeated roles, weak ties and other possible aliases remain.')
    (HERE/'source_histories.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(query_count=189,direct_row_sources=len(rows),root_PAIR=41,actual_RC=185)))


if __name__ == '__main__':
    main()
