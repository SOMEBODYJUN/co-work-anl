"""New exact check of four fixed saved primals; no source import or optimizer.

Upper certificates are the already proved middle/COPY identities. This checks
only the reconstructed positive coordinates against the explicitly listed
finite algebraic row systems, not existence of any complete game strategy.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--evidence-dir', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    specs = [
        ('middle_false', '5c60b4654eaddde9b980', 'probe_middle_rigidity_False.json', 6, 31),
        ('middle_true', 'd8799ea7e2305a682bf4', 'probe_middle_rigidity_True.json', 6, 52),
        ('copy', '056b9f899ae1ff1a9bdc', 'probe_copy_reply_rigidity.json', 7, 100),
        ('three_tail', '8bbd5211a424d9c78a48', 'probe_three_tail_copy_rigidity.json', 9, 165),
    ]
    reports = []
    recovered = {}
    for mode, source_id, name, width, row_count in specs:
        raw = json.loads((args.evidence_dir / 'original' / source_id / name).read_text())
        weights = {}
        recovery = []
        u = None
        for index, bits, value in raw['positive_primal']:
            rational = F(value).limit_denominator(10000)
            assert rational > 0
            recovery.append({'index': index, 'bits': bits, 'saved_float': value,
                             'float_hex': value.hex(), 'reconstructed': str(rational)})
            if index == 1 << width:
                assert bits == 'u' and u is None
                u = rational
            else:
                assert len(bits) == width and all(b in (0, 1) for b in bits)
                assert index == int(''.join(map(str, bits)), 2)
                assert tuple(bits) not in weights
                weights[tuple(bits)] = rational
        assert u is not None
        recovered[mode] = (weights, u)
        rows = []

        def total(function):
            return sum((mass * function(bits) for bits, mass in weights.items()), F())

        def utility(bits, path, position):
            numerator = bits[path[position]]
            return F(numerator, sum(bits[i] for i in path)) if numerator else F()

        def add(name, function, u_coefficient=0, status='known legal contract'):
            residual = total(function) + u_coefficient * u
            assert residual >= 0, (mode, name, residual)
            rows.append({'name': name, 'residual': str(residual), 'contract_status': status})

        original = [0, 2, 3, 4, 5]
        copy4 = [0, 2, 3, 5, 6] if width >= 7 else None
        copy3 = [0, 2, 5, 7, 8] if width == 9 else None
        add('root-real-IC', lambda b: -utility(b, original, 0), 1)
        labels = ['T', 'Q', 'B2', 'B3', 'B4', 'B5', 'C', 'D', 'E'][:width]
        for j in range(width):
            prefix = 'root-size-' if width == 6 else 'size-'
            label = labels[j] if width == 9 else str(j)
            add(prefix + label, lambda b, j=j: -b[j], 5)

        def floors(lab, path, stages):
            for stage in stages:
                for j in range(width):
                    name = (lab + ':floor:' + str(stage) + ':' + labels[j]
                            if width == 9 else 'floor-s' + str(stage) + '-q' + str(j))
                    add(name, lambda b, path=path, stage=stage, j=j:
                        utility(b, path, stage) - F(b[j], sum(b[i] for i in path[:stage]) + 5 - stage))

        def pairs(lab, path, uncertain=False):
            for j, k in combinations_with_replacement(range(width), 2):
                if width == 6:
                    name = 'pair-' + str(j) + '-' + str(k)
                elif width == 7:
                    name = lab + '-pair-' + str(j) + '-' + str(k)
                else:
                    name = lab + ':pair:' + labels[j] + ':' + labels[k]

                def value(b, j=j, k=k, path=path):
                    past = sum(b[i] for i in path[:3])
                    tax_den = (past + 1) * (past + 2)
                    h = utility(b, path, 3) + utility(b, path, 4) + F(b[path[3]], tax_den)
                    return h - F(b[j] + b[k], past + 1) + F(b[j] * b[k], tax_den)

                add(name, value, status=('extra forced-copy PAIR; CAG applicability not closed'
                                         if uncertain else 'known legal contract'))

        if width == 9:
            add('IC-original4-copy5', lambda b: utility(b, original, 3) - utility(b, copy4, 3))
            add('IC-original3-copy5', lambda b: utility(b, original, 2) - utility(b, copy3, 2))
            floors('original', original, range(1, 5))
            floors('copy4', copy4, [4])
            floors('copy3', copy3, [3, 4])
            pairs('original', original)
            pairs('copy3', copy3)
        else:
            floors('original', original, range(1, 5))
            if width == 6:
                if mode == 'middle_true':
                    pairs('original', original)
            else:
                add('penultimate-real-copy-B5', lambda b: utility(b, original, 3) - utility(b, copy4, 3))
                for j in range(width):
                    add('copy-reply-BR-' + str(j), lambda b, j=j:
                        utility(b, copy4, 4) - F(b[j], sum(b[i] for i in copy4[:4]) + 1))
                pairs('actual', original)
                pairs('copy', copy4, uncertain=True)
        assert len(rows) == row_count
        delta = 5 * u - total(lambda b: F(b[0]))
        objective = total(lambda b: F(b[1], 1 + 4 * b[0])) - u
        bound = F(113, 21) if width == 6 else F(16, 3)
        assert delta == 1 and objective == bound
        by_name = {r['name']: F(r['residual']) for r in rows}
        dual = {r['name']: F(r['weight']).limit_denominator(10000) for r in raw['active_rows']}
        assert all(v >= 0 for v in dual.values())
        if width == 6:
            known = {'root-real-IC': F(311, 21), 'root-size-2': F(1, 2),
                     'root-size-3': F(1, 2), 'root-size-4': F(31, 42),
                     'root-size-5': F(37, 42), 'floor-s3-q5': F(5, 21),
                     'floor-s4-q1': F(1)}
        elif width == 7:
            known = {'root-real-IC': F(44, 3), 'size-2': F(1, 2),
                     'size-3': F(1, 2), 'size-4': F(11, 15), 'size-5': F(13, 15),
                     'floor-s4-q1': F(14, 15), 'floor-s4-q6': F(2, 15),
                     'penultimate-real-copy-B5': F(4, 15), 'copy-reply-BR-1': F(1, 15)}
        else:
            known = {'root-real-IC': F(44, 3), 'size-B2': F(1, 2),
                     'size-B3': F(1, 2), 'size-B4': F(11, 15), 'size-B5': F(13, 15),
                     'IC-original4-copy5': F(4, 15), 'original:floor:4:Q': F(14, 15),
                     'original:floor:4:C': F(2, 15), 'copy4:floor:4:Q': F(1, 15)}
        assert dual == known
        assert not any('pair' in n for n in dual)
        assert sum((dual[n] * by_name[n] for n in dual), F()) == 0
        reports.append({'mode': mode, 'source_id': source_id, 'reconstruction': recovery,
                        'rows': rows, 'row_count': len(rows),
                        'minimum_residual': str(min(F(r['residual']) for r in rows)),
                        'delta': str(delta), 'objective': str(objective),
                        'matches_already_proved_upper_bound': True,
                        'recovered_active_multipliers': {n: str(v) for n, v in dual.items()},
                        'active_rows_use_uncertain_PAIR': False,
                        'safe_copy_rows_after_deleting_extra_PAIR': 72 if width == 7 else None})
    tail, tail_u = recovered['three_tail']
    projection = {}
    for bits, mass in tail.items():
        projection[bits[:7]] = projection.get(bits[:7], F()) + mass
    copy, copy_u = recovered['copy']
    assert projection == copy and tail_u == copy_u
    report = {'identity': 'new exact audit of four fixed finite algebraic relaxation primals',
              'original_mains_executed': 0, 'LP_calls': 0, 'random_generation': 0,
              'old_64_or_128_coefficient_audits_replayed': 0,
              'complete_game_SPE_claim': False,
              'three_tail_projection_equals_copy_point': True,
              'projection': [{'bits': list(b), 'mass': str(w)} for b, w in sorted(projection.items())],
              'results': reports}
    with args.output.open('x') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'PASS': True, 'points': len(reports),
                      'rows': sum(r['row_count'] for r in reports),
                      'objectives': {r['mode']: r['objective'] for r in reports},
                      'projection_equal': True,
                      'uncertain_copy_PAIR_not_used_by_upper_certificates': True}, indent=2))


if __name__ == '__main__':
    main()
