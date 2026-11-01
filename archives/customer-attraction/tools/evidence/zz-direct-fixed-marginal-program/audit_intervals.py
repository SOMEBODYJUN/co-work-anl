"""Independent exact interval realization of the fixed-marginal ZZ diagnostic.

Reads all 1905 input columns, never imports the original source or solver.
Checks all group marginals, shared-threshold intersections, literal payoff
integrals, analytic maxima, and the six negatives printed by the original CLI.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def canonical(values):
    # Equivalence partition by first position carrying the same index.
    first = [values.index(v) for v in values]
    ordered = sorted(set(first))
    return tuple(ordered.index(v) for v in first)


def group_key(value):
    f, diagonal, wi, wj = value
    return f, diagonal, tuple(wi), tuple(wj)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--original-report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    assert len(raw) == 816498
    assert hashlib.sha256(raw).hexdigest() == 'cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1'
    data = json.loads(raw)
    cols = data['columns']
    assert len(cols) == 1905
    kinds = Counter(c['kind'] for c in cols)
    assert kinds == {'K':1, 'hist':16, 'joint-reply':582, 'overlap':1306}
    weights = [F(c['weight']) for c in cols]
    assert min(weights) >= 0 and sum(v > 0 for v in weights) == data['positive_columns'] == 175
    words8 = tuple(product((0,1), repeat=3))
    histories = {}
    hist_index = None
    expected_keys = {
        'K': {'kind','weight'},
        'hist': {'kind','actual_bits','d','hist','weight'},
        'joint-reply': {'kind','hist_column_old','group','state','weight'},
        'overlap': {'kind','hist_column','groups','weight'},
    }
    for index, col in enumerate(cols):
        assert set(col) == expected_keys[col['kind']], (index,set(col))
        if col['kind'] == 'hist':
            hist_index = index
            assert cols.index(col) == index  # The original parser relies on this.
            bits = tuple(map(int,col['actual_bits']))
            assert len(bits) == 6 and set(bits) <= {0,1}
            hist = col['hist']
            assert len(hist) == 8 and all(isinstance(n,int) and n >= 0 for n in hist)
            assert sum(hist) == 6 and sum(n*w[0] for n,w in zip(hist,words8)) == col['d']
            histories[index] = {'column':col, 'groups':{}}
        elif col['kind'] == 'joint-reply':
            assert hist_index is not None
            key = group_key(col['group'])
            state = tuple(col['state'])
            assert state in {(0,1),(1,0),(1,1)}
            group = histories[hist_index]['groups'].setdefault(key, {'states':{},'indices':[]})
            assert state not in group['states']
            group['states'][state] = F(col['weight'])
            group['indices'].append(index)
    assert len(histories) == 16
    O = sum(F(item['column']['weight']) for item in histories.values() if item['column']['d'] > 0)
    W = sum(F(item['column']['weight']) for item in histories.values() if '1' in item['column']['actual_bits'])
    assert O == F(data['O']) == 1 and W == F(data['W'])
    assert 1-2*W == F(data['strict_half_gap'])

    # Generate the 15 restricted-growth equality patterns without cl.P4.
    patterns = [(0,)]
    for _ in range(3):
        patterns = [p+(n,) for p in patterns for n in range(max(p)+2)]
    patterns = sorted(patterns)
    assert len(patterns) == 15
    row_keys = [(f,g,p) for f,g,p in product(range(2),range(2),patterns)]
    edges = [(0,i,j) for i in range(6) for j in range(6) if i != j]
    edges += [(1,i,j) for i in range(6) for j in range(6)]
    pairs = [(e,f,(e[0],f[0],canonical((e[1],e[2],f[1],f[2])))) for e in edges for f in edges]
    multiplicities = Counter(row for _,_,row in pairs)
    assert len(edges) == 66 and len(pairs) == 4356 and len(multiplicities) == 42
    totals = {row:F() for row in row_keys}
    details = []
    group_count = zero_histograms = positive_histograms = integral_terms = 0
    overlap_checks = 0
    for index, item in histories.items():
        col = item['column']
        mass = F(col['weight'])
        gs = item['groups']
        words = [w for w,n in zip(words8,col['hist']) for _ in range(n)]
        edge_group = {e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]) for e in edges}
        assert set(gs) == set(edge_group.values())
        ordered = sorted(gs)
        group_index = {key:j for j,key in enumerate(ordered)}
        g_records = []
        breaks = {F(),mass}
        for key in ordered:
            state = gs[key]['states']
            assert set(state) == {(0,1),(1,0),(1,1)}
            state[0,0] = mass-sum(state.values())
            assert min(state.values()) >= 0
            r = state[1,0]+state[1,1]
            z = state[0,1]+state[1,1]
            v = state[1,1]
            o = state[0,1]
            assert 0 <= v <= r <= mass and 0 <= o <= mass-r
            gs[key].update({'r':r,'z':z,'v':v,'o':o})
            breaks.update((r,v,r+o))
            g_records.append({'group':key,'source_columns':gs[key]['indices'],
                              'states':{str(k):str(vv) for k,vv in sorted(state.items())},
                              'R':str(r),'Z':str(z),'RZ':str(v),'Z_minus_R':str(o)})
        group_count += len(gs)
        local = {row:F() for row in row_keys}
        cells = []
        if mass:
            positive_histograms += 1
            points = sorted(breaks)
            pa = sum(map(int,col['actual_bits'][:4]))
            D = (pa+1)*(pa+2)
            mass4 = {key:Counter() for key in ordered}
            rz = {(left,right):F() for left in ordered for right in ordered}
            for low,high in zip(points,points[1:]):
                assert high > low
                middle = (low+high)/2
                length = high-low
                rbit = {key:int(middle < gs[key]['r']) for key in ordered}
                zbit = {key:int(middle < gs[key]['v'] or gs[key]['r'] <= middle < gs[key]['r']+gs[key]['o']) for key in ordered}
                for key in ordered:
                    mass4[key][rbit[key],zbit[key]] += length
                for left,right in rz:
                    if rbit[left] and zbit[right]:
                        rz[left,right] += length
                # Literal unit-customer payoff difference, grouped only to
                # avoid repeating identical Fraction additions in a cell.
                coefficients = Counter()
                for e,f,row in pairs:
                    g_e,g_f = edge_group[e],edge_group[f]
                    coefficients[row,pa+1+rbit[g_e]] += zbit[g_e]-zbit[g_f]
                for (row,denominator),numerator in coefficients.items():
                    local[row] += length*F(numerator,denominator)
                integral_terms += len(pairs)
                cells.append({'left':str(low),'right':str(high),'mass':str(length),
                              'R_groups':[group_index[k] for k in ordered if rbit[k]],
                              'Z_groups':[group_index[k] for k in ordered if zbit[k]]})
            for key in ordered:
                assert all(mass4[key][state] == value for state,value in gs[key]['states'].items())
            for left,right in rz:
                a,b = gs[left],gs[right]
                upper = min(b['v'],a['r']) if a['r'] <= b['r'] else b['v']+min(b['o'],a['r']-b['r'])
                assert rz[left,right] == upper
                overlap_checks += 1
            analytic = {row:F() for row in row_keys}
            for e,f,row in pairs:
                a,b = gs[edge_group[e]],gs[edge_group[f]]
                analytic[row] += (a['z']-b['z'])/(pa+1)+(rz[edge_group[e],edge_group[f]]-a['v'])/D
            assert local == analytic
        else:
            zero_histograms += 1
            assert all(not value for group in gs.values() for value in group['states'].values())
        for row,value in local.items():
            totals[row] += value
        details.append({'hist_column':index,'source_descriptor':col,'group_count':len(gs),
                        'groups':g_records,'interval_cells':cells,
                        'rows':[{'key':str(row),'slack':str(local[row])} for row in row_keys]})
    assert group_count == 194 and positive_histograms == 10 and zero_histograms == 6
    old_overlaps_changed = old_upper_failures = 0
    largest_raise = F()
    for index,col in enumerate(cols):
        if col['kind'] != 'overlap':
            continue
        gs = histories[col['hist_column']]['groups']
        left,right = map(group_key,col['groups'])
        new = min(gs[left]['r'],gs[right]['r'])
        old = F(col['weight'])
        old_upper_failures += old > new
        if old != new:
            old_overlaps_changed += 1
            largest_raise = max(largest_raise,new-old)
    assert old_upper_failures == 0
    negative = [{'row':str(row),'slack':str(value)} for row,value in totals.items() if value < 0]
    original = json.loads(args.original_report.read_text())
    assert original['rows'] == 60 and original['W'] == str(W)
    assert original['negative_rows'] == negative
    assert original['minimum_slack'] == str(min(totals.values()))
    result = {
        'status':'PASS-independent-literal-interval-and-fixed-marginal-check',
        'scope':'All input columns read; direct unit-customer interval integration and simultaneous upper attainment, not old 3889 verification or SPE',
        'input_sha256':hashlib.sha256(raw).hexdigest(), 'input_bytes':len(raw),
        'input_metadata':{k:v for k,v in data.items() if k != 'columns'},
        'input_column_kinds':dict(kinds),'all_columns_nonnegative':True,
        'O_recomputed':str(O),'W_recomputed':str(W),'K_stored':cols[0]['weight'],
        'histograms':16,'positive_histograms':10,'zero_histograms':6,
        'groups':group_count,'explicit_states':582,'implicit_00_states_checked':194,
        'stored_overlap_columns_ignored_by_original':1306,
        'stored_RR_overlaps_changed_by_common_threshold':old_overlaps_changed,
        'largest_RR_overlap_raise':str(largest_raise),
        'edge_counts':{'B_off_diagonal':30,'C_all':36},
        'ordered_edge_pairs_per_histogram':4356,
        'row_slots':60,'nonempty_row_slots':42,'empty_row_slots':18,
        'row_status_counts':dict(Counter('negative' if v < 0 else 'positive' if v > 0 else 'zero' for v in totals.values())),
        'physical_interval_cells':sum(len(d['interval_cells']) for d in details),
        'literal_interval_edge_pair_terms':integral_terms,
        'cross_RZ_maximum_equalities_checked':overlap_checks,
        'row_original_report_comparison':'all six negatives, minimum, row count and W; original stdout does not print the other 54 values',
        'negative_rows':negative,'minimum_slack':str(min(totals.values())),
        'rows':[{'key':str(row),'edge_pair_multiplicity_per_histogram':multiplicities[row],'slack':str(value)} for row,value in totals.items()],
        'histogram_details':details,
        'original_main_invocations_in_this_checker':0,
        'original_functions_imported':False,'LP_calls':0,
    }
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','histograms','positive_histograms','groups','row_status_counts','physical_interval_cells','cross_RZ_maximum_equalities_checked','stored_RR_overlaps_changed_by_common_threshold','minimum_slack')},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
