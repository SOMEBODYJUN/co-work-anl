"""Independent unit-customer Fraction certificate, with no BI or LP calls."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path


def counts_of(actions, k):
    return tuple(actions.count(a) for a in range(k))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    raw = args.source.read_bytes()
    assert len(raw) == 1179
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == '19ad9937d6c7149dfef7ccfc4e33f914f6360c8f90619f2a0db9652befb15913'
    d = json.loads(raw)
    lexical = json.loads(raw, parse_float=str)
    assert list(d) == ['iteration', 'n', 'k', 'ratio_W_over_nv', 'v_screen',
                      'target', 'weights', 'query_screen']
    n, k = d['n'], d['k']
    assert (n,k,d['iteration']) == (5,7,238)
    weights = d['weights']
    assert len(weights) == (1 << k)-1
    assert all(type(w) is int and 0 <= w <= 5 for w in weights)
    types = []
    customers = []
    for mask, multiplicity in enumerate(weights,1):
        if multiplicity:
            likes = frozenset(a for a in range(k) if mask >> a & 1)
            types.append({'mask': mask, 'array_index': mask-1,
                          'topics': sorted(likes), 'multiplicity': multiplicity})
            customers.extend([likes]*multiplicity)
    assert len(customers) == 34 and len(types) == 11
    themes = [frozenset(i for i, likes in enumerate(customers) if a in likes)
              for a in range(k)]
    assert len(set(themes)) == k and all(themes)
    chosen = 5
    assert d['target'] == [0,0,0,0,0,n,0]
    assert d['query_screen'] == [0.,0.,0.,0.,0.,1.,0.]
    v = Fraction(len(themes[chosen]), n)
    backgrounds = []
    for actions in combinations_with_replacement(range(k), n-1):
        loads = [sum(a in likes for a in actions) for likes in customers]
        queries = [sum((Fraction(1,1+loads[i]) for i in themes[a]),Fraction(0))
                   for a in range(k)]
        assert queries[chosen] >= v
        assert all(queries[chosen] > queries[a] for a in range(k) if a != chosen)
        backgrounds.append({'counts': list(counts_of(actions,k)),
                            'query_payoffs': list(map(str, queries)),
                            'chosen_minus_others': [str(queries[chosen]-queries[a]) for a in range(k)]})
    assert len(backgrounds) == 210
    pure_bg = next(b for b in backgrounds if b['counts'] == [0,0,0,0,0,n-1,0])
    assert max(map(Fraction,pure_bg['query_payoffs'])) == v
    lower_by_action = []
    for a in range(k):
        private_chosen = len(themes[chosen]-themes[a])
        private_alternative = len(themes[a]-themes[chosen])
        bound = Fraction(private_chosen,n)-private_alternative
        exact_min = min(Fraction(b['chosen_minus_others'][a]) for b in backgrounds)
        assert exact_min >= bound
        if a != chosen:
            assert bound > 0
        lower_by_action.append({'alternative': a, 'chosen_private': private_chosen,
                                'alternative_private': private_alternative,
                                'uniform_gap_lower_bound': str(bound),
                                'exact_minimum_gap_over_210_backgrounds': str(exact_min)})
    terminal_rows = []
    for actions in combinations_with_replacement(range(k),n):
        covered = set().union(*(themes[a] for a in actions))
        terminal_rows.append({'counts': list(counts_of(actions,k)),
                              'coverage': len(covered)})
    assert len(terminal_rows) == 462
    optimum = max(t['coverage'] for t in terminal_rows)
    assert optimum == 34
    welfare = len(themes[chosen])
    ratio = Fraction(welfare,n*v)
    assert welfare == 29 and ratio == 1
    minimum_gap = min(Fraction(row['exact_minimum_gap_over_210_backgrounds'])
                      for row in lower_by_action if row['alternative'] != chosen)
    assert minimum_gap == Fraction(3,5)
    report = {
        'status': 'PASS_EXACT_PURE_SADDLE_AND_UNIQUE_COMPLETE_SPE',
        'primary': {'bytes':len(raw),'sha256':digest,'all_fields':d},
        'encoding': {'mask_first':1,'mask_last':127,'index': 'mask-1',
                     'positive_types':types,'zero_weights': weights.count(0),
                     'unit_customers':len(customers),'theme_sizes':list(map(len,themes)),
                     'all_seven_coverages_nonempty_and_pairwise_distinct':True},
        'exact_point': {'players':n,'topics':k,'terminal_counts':d['target'],
                        'ordered_actual_path':[chosen]*n,'W':welfare,'OPT_5':optimum,
                        'each_player_payoff':str(v),'v_5':str(v),'W_over_5v':'1',
                        'W_minus_5v':'0','twoW_minus_OPT':2*welfare-optimum,
                        'W_over_OPT':str(Fraction(welfare,optimum)),
                        'customers_uncovered_on_actual':len(customers)-welfare},
        'static_saddle': {
            'primal_query_distribution': ['0','0','0','0','0','1','0'],
            'dual_background_point_mass_counts':pure_bg['counts'],
            'all_seven_payoffs_against_dual':pure_bg['query_payoffs'],
            'query_minimum_over_all_210_backgrounds':str(min(Fraction(b['query_payoffs'][chosen]) for b in backgrounds)),
            'all_210_backgrounds_checked_with_all_repetitions':True,
            'ordered_backgrounds_covered_by_counts': k**(n-1),
            'no_optimization_or_reconstruction_of_float_multipliers':True},
        'unique_strategy': {
            'rule':'sigma(h)=5 for every ordered history of length<5',
            'uniform_private_set_bounds':lower_by_action,
            'minimum_exact_nonself_gap':'3/5',
            'proof':'Every 4-competitor background strictly prefers T5. Backward induction makes every continuation T5, at every ordered history; all earlier movers then have the same strict best response. This proves uniqueness, not just a prescribed on-path outcome.',
            'number_of_decision_histories_covered_by_proof':sum(k**j for j in range(n)),
            'number_of_nonself_history_comparisons_covered_by_proof':(k-1)*sum(k**j for j in range(n)),
            'ordered_tree_separately_enumerated':False,
            'exact_BI_solver_called':False},
        'coverage': {'terminal_count_vectors_checked':len(terminal_rows),
                     'ordered_terminal_histories_covered_by_counts':k**n,
                     'coverage_histogram':dict(sorted(Counter(t['coverage'] for t in terminal_rows).items())),
                     'number_of_optimal_count_vectors':sum(t['coverage']==optimum for t in terminal_rows),
                     'explicit_optimal_five_actions':[0,1,4,5,5],
                     'explicit_optimal_coverage':len(set().union(*(themes[a] for a in [0,1,4,5,5])))},
        'serialized_decimal_errors_not_binary_error_claim': {
            'v_screen_literal':lexical['v_screen'],
            'v_screen_minus_exact':str(Fraction(lexical['v_screen'])-v),
            'ratio_literal':lexical['ratio_W_over_nv'],
            'ratio_minus_exact':str(Fraction(lexical['ratio_W_over_nv'])-ratio)},
        'scope': {'independent_script_executions':1,'original_imports':0,'original_helpers':0,
                  'original_main':0,'RNG':0,'BI':0,'LP':0,
                  'new_scalar_fraction_background_payoffs':len(backgrounds)*k,
                  'new_terminal_coverage_evaluations':len(terminal_rows),
                  'method':'Expand 34 unit customers; evaluate every unordered background and terminal multiset directly; elementary saddle and strict-dominance proof.'}
    }
    assert report['coverage']['explicit_optimal_coverage'] == optimum
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,obj in [('point-audit.json',report),('background-payoffs.json',backgrounds),
                     ('terminal-coverages.json',terminal_rows)]:
        (args.output_dir/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'v':str(v),'W':welfare,'OPT':optimum,
                      'backgrounds':len(backgrounds),'terminals':len(terminal_rows),
                      'min_strict_gap':str(minimum_gap),'LP':0,'BI':0}))


if __name__ == '__main__':
    main()
