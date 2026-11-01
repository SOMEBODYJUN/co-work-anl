"""Grouped-type reconstruction of one fixed two-player continuation game.

No original program import or 1024-policy scan. Nine weighted client types
give all 16 terminal payoff vectors; four terminal BR functions determine SPE.
"""
import argparse
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

TYPES = [((1,),1),((0,2),2),((1,2),2),((0,1,2),2),((3,),1),
         ((0,3),2),((1,3),2),((0,1,3),1),((0,2,3),2)]
PREFIX = (0,1,1)
A = 3
REPORT_SHA = '3834ff80162300c16bb14a17c65d3bc95ac07455ce6c58333410b411cf8bbc37'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def grouped_payoff(actions):
    return [sum((F(n,sum(a in themes for a in actions))
                 for themes,n in TYPES if action in themes),F()) for action in actions]


def audit(report_path,capture_path):
    frozen = json.loads(report_path.read_text())
    capture = json.loads(capture_path.read_text())
    assert sha(report_path) == REPORT_SHA and report_path.stat().st_size == 590
    utility = {(c,d):grouped_payoff(PREFIX+(A,c,d)) for c,d in product(range(4),repeat=2)}
    utilities = [{'c':c,'d':d,'payoffs':list(map(str,u))} for (c,d),u in utility.items()]
    assert utilities == capture['utility']
    br = {c:tuple(d for d in range(4) if utility[c,d][5] == max(utility[c,e][5] for e in range(4))) for c in range(4)}
    terminal_functions = list(product(*(br[c] for c in range(4))))
    policies = []
    function_rows = []
    for replies in terminal_functions:
        own = tuple(utility[c,replies[c]][4] for c in range(4))
        sources = [c for c in range(4) if own[c] == max(own)]
        function_rows.append({'replies':list(replies),'source_action_payoffs':list(map(str,own)),
                              'source_best_actions':sources})
        for c in sources:
            d = replies[c]
            policies.append({'c':c,'d':d,'replies':list(replies),
                'old_A_payoff':str(utility[c,d][3]),'source_payoff':str(utility[c,d][4]),
                'terminal_payoff':str(utility[c,d][5])})
    policies.sort(key=lambda x:(x['c'],tuple(x['replies'])))
    feasible = [[x['old_A_payoff'],x['c'],x['d'],x['replies']] for x in policies]
    assert feasible == capture['feasible']
    ell = min(F(x['old_A_payoff']) for x in policies)
    minimizing = [x for x in policies if F(x['old_A_payoff']) == ell]
    swapped = min(utility[3,d][3] for d in br[3])
    per_action_minima = [min(utility[c,d][4] for d in br[c]) for c in range(4)]
    threshold = max(per_action_minima)
    tie_terms = []
    delta_terms = []
    cover_types = {a:tuple(j for j,(t,n) in enumerate(TYPES) if a in t and n>0) for a in range(4)}
    assert len(set(cover_types.values())) == 4
    for themes,n in TYPES:
        p = int(0 in themes)+2*int(1 in themes)
        t = c = int(3 in themes)
        s,z = int(2 in themes),int(0 in themes)
        tie_terms.append(F(n*(s-z),p+t+c+1))
        delta_terms.append(F(n*t*(z-s),(p+c+1)*(p+c+2)))
    tie = sum(tie_terms,F());delta = sum(delta_terms,F())
    assert ell == F(71,30) and swapped == F(13,6) and threshold == F(67,30)
    assert tie == 0 and delta == ell-swapped == F(1,5)
    assert len(policies) == 5 and len(terminal_functions) == 4 and len(minimizing) == 1
    witness = minimizing[0]
    assert [witness['c'],witness['d']] == [3,2] and witness['replies'] == [0,0,0,2]
    last_admissible_candidates = len(terminal_functions)*4
    expected = {'unit_customers':sum(n for _,n in TYPES),'distinct_topics':True,
        'all_two_player_policies':4*4**4,'SPE_tail_policies':len(policies),
        'last_best_reply_sets':{str(c):list(br[c]) for c in range(4)},
        'last_comparisons':last_admissible_candidates*16,
        'source_comparisons':last_admissible_candidates*4,
        'minimum_old_A':str(ell),'minimum_after_commutation':str(swapped),
        'strict_gap':str(ell-swapped),'source_threshold':str(threshold),
        'witness_tail':[witness['c'],witness['d']],
        'same_background_BR_equality':str(tie),'minimum_row_coefficient_sum':str(delta),
        'all_checks_passed':True}
    assert expected == frozen and list(expected) == list(frozen)
    assert capture['BR'] == expected['last_best_reply_sets']
    assert all(capture[k] == v for k,v in {'ell':str(ell),'swapped':str(swapped),
        'source_floor':str(threshold),'tie':str(tie),'delta':str(delta),
        'checked_last':256,'checked_source':64}.items())
    return {'status':'PASS_GROUPED_TYPE_AND_BR_FUNCTION_RECONSTRUCTION',
        'scope':'One specified 15-unit-client background; no original-main run, no 1024-policy scan, no root-game SPE or quotient test.',
        'algorithm':'Nine type-weighted denominator sums for 16 terminal profiles, then all four admissible terminal BR functions and their root maximizers.',
        'types':[{'topics':list(t),'unit_multiplicity':n} for t,n in TYPES],
        'prefix':list(PREFIX),'forced_A':A,'unit_clients':15,'topic_coverage_type_indices':{str(a):list(v) for a,v in cover_types.items()},
        'terminal_profiles':16,'payoff_entries':96,'utility':utilities,
        'all_96_payoffs_equal_original_passive_capture':True,
        'last_best_reply_sets':expected['last_best_reply_sets'],
        'terminal_BR_functions':function_rows,'terminal_admissible_source_candidates':last_admissible_candidates,
        'complete_tail_SPE_policies':policies,'distinct_terminal_pairs':sorted({(x['c'],x['d']) for x in policies}),
        'all_five_full_policies_equal_original_capture':True,
        'source_action_worst_BR_payoffs':list(map(str,per_action_minima)),
        'minimum_old_A':str(ell),'minimum_after_commutation':str(swapped),
        'source_threshold':str(threshold),'strict_gap':str(delta),
        'same_background_BR_terms_by_type':list(map(str,tie_terms)),
        'minimum_row_terms_by_type':list(map(str,delta_terms)),
        'same_background_BR_sum':str(tie),'minimum_row_sum':str(delta),
        'all_15_frozen_report_fields_exactly_reconstructed':True,
        'counter_semantics':'256 and 64 are nominal 16/4 increments for 16 accepted (source action, terminal BR function) candidates; not dynamically measured scalar comparisons.',
        'original_main_invocations':0,'exhaustive_1024_policy_scans':0,'optimizer_invocations':0,'quotient_test_invocations':0,
        'inputs':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in (report_path,capture_path)],
        'not_proved':['the selected prefix lies on any six-player root SPE','a general equal-coverage quotient theorem','a six-player half theorem','a globally payable sum of all minimum continuation values']}


if __name__ == '__main__':
    if sys.flags.optimize:
        raise RuntimeError('Assertions must stay enabled')
    ap = argparse.ArgumentParser()
    ap.add_argument('--report',type=Path,required=True)
    ap.add_argument('--capture',type=Path,required=True)
    a = ap.parse_args()
    print(json.dumps(audit(a.report.resolve(),a.capture.resolve()),ensure_ascii=False,indent=2))
