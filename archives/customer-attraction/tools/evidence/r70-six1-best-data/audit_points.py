"""Independent exact audit of the two saved R70 points and one newly captured strategy.

Only Python standard library. No source solver, strategy helper, BI or optimizer.
JSON decimals are interpreted from their literal text, never Fraction(float).
Integer types are expanded to distinct unit customers before payoff computation.
"""
import argparse
from collections import Counter
from decimal import Decimal
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import gcd, lcm
from pathlib import Path
import gzip
import hashlib
import json
import time


def binding(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, Decimal):
        return str(x)
    raise TypeError(type(x))


def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=encode) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--random', type=Path, required=True)
    ap.add_argument('--lp', type=Path, required=True)
    ap.add_argument('--strategy', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / 'point-audit.json'
    if report_path.exists():
        raise SystemExit('Existing exact event: do not rerun or overwrite')
    start = time.monotonic()
    raw_random = json.loads(args.random.read_text(), parse_float=Decimal)
    raw_lp = json.loads(args.lp.read_text(), parse_float=Decimal)
    random_w = raw_random['weights']
    assert len(random_w) == 128 and all(type(w) is int and w >= 0 for w in random_w)
    literal = [F(w) for w in raw_lp['weights']]
    assert len(literal) == 128 and all(w >= 0 for w in literal)
    denominator = lcm(*(w.denominator for w in literal))
    numerators = [int(w * denominator) for w in literal]
    common = gcd(*numerators)
    lp_w = [x // common for x in numerators]
    scale = F(denominator, common)
    assert all(x * scale == y for x, y in zip(literal, lp_w))
    assert [(m, w) for m, w in enumerate(lp_w) if w] == [(2, 1), (5, 6), (8, 1), (16, 1), (32, 1), (64, 1)]
    assert sum(lp_w) == 11 and raw_lp['actual_count'] == [1, 0, 5, 0, 0, 0, 0]
    strategy_blob = json.loads(args.strategy.read_text())
    assert strategy_blob['n'] == 7 and strategy_blob['players'] == 6
    entries = strategy_blob['entries']
    sigma = {tuple(e['history']): e['action'] for e in entries}
    histories = [h for d in range(6) for h in product(range(7), repeat=d)]
    assert len(entries) == len(sigma) == len(histories) == 19608
    assert set(sigma) == set(histories)
    assert all(type(a) is int and 0 <= a < 7 for a in sigma.values())

    @lru_cache(None)
    def follow(h):
        if len(h) == 6:
            return h
        return follow(h + (sigma[h],))

    terminals = list(combinations_with_replacement(range(7), 6))
    assert len(terminals) == 924
    count_keys = [tuple(z.count(a) for a in range(7)) for z in terminals]
    root = follow(())
    root_counts = tuple(root.count(a) for a in range(7))
    assert list(root_counts) == raw_random['result']['root_min_count'] == raw_lp['actual_count']
    rows = []
    reports = {}
    for name, weights in [('random', random_w), ('lp_integer', lp_w)]:
        customers = [frozenset(a for a in range(7) if mask & (1 << a))
                     for mask, w in enumerate(weights) for _ in range(w)]
        assert all(customers)
        covers = [frozenset(i for i, likes in enumerate(customers) if a in likes) for a in range(7)]
        classes = []
        projection = []
        for cover in covers:
            if cover not in classes:
                classes.append(cover)
            projection.append(classes.index(cover))
        assert len(classes) == 6 and all(classes)
        assert all(not (classes[i] & classes[j]) for i in range(6) for j in range(i))
        table = {}
        terminal_rows = []
        for z, counts in zip(terminals, count_keys):
            loads = [sum(counts[a] for a in likes) for likes in customers]
            # LCM(1,...,6)=60 makes all payments integral. Only used labels have players.
            pay60 = [sum(60 // loads[i] for i in cover if loads[i]) for cover in covers]
            welfare = sum(c > 0 for c in loads)
            table[counts] = (pay60, welfare)
            terminal_rows.append(dict(counts=counts, welfare=welfare, used_topic_pay60={str(a): pay60[a] for a in range(7) if counts[a]}))
        pne = []
        for row in terminal_rows:
            c = tuple(row['counts'])
            profitable = []
            for a in range(7):
                if not c[a]:
                    continue
                current = table[c][0][a]
                for b in range(7):
                    d = list(c)
                    d[a] -= 1
                    d[b] += 1
                    alternative = table[tuple(d)][0][b]
                    if alternative > current:
                        profitable.append([a, b, alternative - current])
            row['static_PNE'] = not profitable
            row['profitable_static_moves_pay60'] = profitable
            if not profitable:
                pne.append(c)
        all_slacks = Counter()
        layer_slacks = [Counter() for _ in range(6)]
        detailed = []
        for h in histories:
            a = sigma[h]
            z = follow(h)
            c = tuple(z.count(b) for b in range(7))
            u = table[c][0][a]
            alternatives = []
            for b in range(7):
                zz = follow(h + (b,))
                cc = tuple(zz.count(t) for t in range(7))
                v = table[cc][0][b]
                slack = u - v
                assert slack >= 0, (name, h, a, b, slack)
                alternatives.append(slack)
                all_slacks[slack] += 1
                layer_slacks[len(h)][slack] += 1
            detailed.append([list(h), a, list(z), u, alternatives])
        W = table[root_counts][1]
        OPT = max(row['welfare'] for row in terminal_rows)
        summary = dict(unit_customers=len(customers), positive_types=[dict(mask=m, likes=[a for a in range(7) if m & (1 << a)], multiplicity=w) for m, w in enumerate(weights) if w],
                       topic_sizes=list(map(len, covers)), projection=projection, disjoint_distinct_nonempty_covers=6,
                       actual=root, actual_count=root_counts, actual_payoffs=[F(table[root_counts][0][a], 60) for a in root],
                       W=W, OPT=OPT, ratio=F(W, OPT), half_slack=2*W-OPT,
                       terminal_multisets=924, static_PNE_count=len(pne), static_PNE_counts=pne,
                       static_PNE_welfare_values=sorted({table[c][1] for c in pne}),
                       strategy_nodes=19608, comparisons=137256, self_comparisons=19608, nonself_comparisons=117648,
                       minimum_slack=F(min(all_slacks), 60), tight_comparisons=all_slacks[0],
                       slack_histogram={str(F(k, 60)): v for k, v in sorted(all_slacks.items())},
                       layers=[dict(depth=d, comparisons=sum(c.values()), tight=c[0], minimum_slack=F(min(c),60)) for d,c in enumerate(layer_slacks)])
        reports[name] = summary
        rows.append(dict(point=name, payment_scale=60, terminal_rows=terminal_rows, ordered_history_rows=detailed,
                         history_row_schema=['history','chosen','true_continuation','chosen_pay60','seven_slacks_pay60']))
    assert reports['random']['W'] == 43 and reports['random']['OPT'] == 58
    assert reports['random']['static_PNE_count'] == 6 and reports['random']['static_PNE_welfare_values'] == [43]
    assert reports['lp_integer']['W'] == 6 and reports['lp_integer']['OPT'] == 11
    binary = json.loads(args.lp.read_text())['weights']
    a = literal[2]
    source_audit = dict(random_fields=list(raw_random), random_result_fields=list(raw_random['result']),
                        lp_fields=list(raw_lp), masks=128, active_masks_start_at_zero=True,
                        ignored_uncovered_mask0=[random_w[0],literal[0]],
                        source_lp_signed_zero_indices=[i for i,w in enumerate(raw_lp['weights']) if isinstance(w,Decimal) and w.is_zero() and w.is_signed()],
                        lp_decimal_common_unit=a, lp_decimal_total_mass=sum(literal), lp_decimal_actual_welfare=6*a,
                        integer_rescaling=scale, lp_integer_weights=lp_w,
                        literal_report_ratio=raw_lp['ratio'], true_normalized_ratio=F(6,11),
                        binary_central_minus_six_singleton=F(binary[5])-6*F(binary[2]),
                        random_literal_ratio_minus_exact=F(raw_random['ratio'])-F(43,58),
                        lp_literal_ratio_minus_exact=F(raw_lp['ratio'])-F(6,11),
                        report_rows_3048_are_not_full_history_comparisons=raw_lp['rows'])
    packed = json.dumps(rows, ensure_ascii=False, separators=(',', ':'), default=encode).encode()
    detail_path = args.output_dir / 'exact-details.json.gz'
    detail_path.write_bytes(gzip.compress(packed, mtime=0))
    write(args.output_dir/'lp-integer-point.json', dict(scope='New exact uniform scaling of literal decimal weights; not original LP JSON or optimizer output',weights=lp_w, multiplier=scale))
    report = dict(status='PASS',scope='Independent unit-customer exact checks for one captured full strategy and two specified points; static PNE enumeration is not a new BI algorithm',
                  original_solver_runs=0, original_helper_calls=0, optimizer_calls=0, random_samples=0,
                  independent_mathematical_entry_runs=1, input_bindings=[binding(p) for p in [args.random,args.lp,args.strategy]],
                  source_fields=source_audit, points=reports, details=binding(detail_path), elapsed_seconds=time.monotonic()-start)
    write(report_path, report)
    print(json.dumps(dict(status='PASS',point_W_OPT={k:[v['W'],v['OPT']] for k,v in reports.items()},comparisons_per_point=137256,terminal_multisets_per_point=924,elapsed_seconds=report['elapsed_seconds'])))


if __name__ == '__main__':
    main()
