"""Inspect frozen quotient reports and saved per-case diagnostics without rerunning tests.

This does not import the quotient compiler, run BI, draw random numbers, or
independently verify any policy.  The case domains come from the read source;
the SPE/signal outcomes are explicitly inherited from saved prior diagnostics.
"""
from pathlib import Path
from itertools import product
from hashlib import sha256
import argparse
import json


def load(path, expected=None):
    data = path.read_bytes()
    if expected:
        assert sha256(data).hexdigest() == expected, path
    return json.loads(data)


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    p = argparse.ArgumentParser()
    p.add_argument('--repository', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    args = p.parse_args()
    base = args.repository / 'archives/customer-attraction/tools/evidence/action-quotient-parent-replay'
    primary = base / 'related/duplicate_action_quotient_test_report.json'
    author = load(primary, 'e9290b6074fb49286de774237f2ead2d4130adfe3bb784f587c572f87700b407')
    parent = load(base/'original/action_quotient_replay.json', '55f8b8ff482456604a8b32c650c62309d892197290e2da58070d370b36cd96b2')
    counts = load(base/'replay/count-semantics.json', '1cd43d61563d15e31d1b266feff708fc2abd403a85e3f42153a0d7a30fb05b6a')
    event = load(base/'replay/execution-event.json')
    replay = base/'replay/author-stdout.json'
    assert replay.read_bytes() == primary.read_bytes()
    expected = {'exhaustive_games':64,'exhaustive_full_policies':5184,'exhaustive_full_SPE':856,
                'random_three_player_games':200,'duplicate_signal_dependent_cases':43,
                'six_player_original_IC_comparisons':137256,'six_player_quotient_IC_comparisons':55986,
                'compiled_exact_IC_comparisons':67626,'all_checks_passed':True}
    assert author == expected and {k:parent[k] for k in author} == author
    assert set(parent)-set(author)=={'review','compiler_sha256','test_sha256'}
    for key, name in [('compiler_sha256','duplicate_action_quotient.py'),('test_sha256','test_duplicate_action_quotient.py')]:
        assert sha256((base/'related'/name).read_bytes()).hexdigest() == parent[key] == event[key]
    assert event['exit_code']==0 and event['assertions_enabled'] and event['pythonoptimize_environment_removed']
    assert event['stdout_sha256']==sha256(primary.read_bytes()).hexdigest() and event['stdout_bytes']==339
    table = counts['two_player_SPE_by_private_masses']
    assert len(table)==16 and {(x['private_a'],x['private_b']) for x in table}==set(product(range(4),repeat=2))
    lookup={(x['private_a'],x['private_b']):x['spe_per_shared_c'] for x in table}
    games=[{'game':j,'a':a,'b':b,'c':c,'weights':{'3':a,'4':b,'7':c},'full_policies':81,
            'SPE_count_from_prior_diagnostic':lookup[a,b], 'quotient_classes':1 if a==b==0 else 2}
           for j,(a,b,c) in enumerate(product(range(4),repeat=3))]
    assert len(games)==64 and sum(x['full_policies'] for x in games)==5184
    assert sum(x['SPE_count_from_prior_diagnostic'] for x in games)==856
    compiled_two=sum(x['SPE_count_from_prior_diagnostic']*(x['quotient_classes']+x['quotient_classes']**2) for x in games)
    assert compiled_two==3840
    details=counts['random_signal_details']
    assert len(details)==200 and [x['game'] for x in details]==list(range(200))
    for row in details:
        assert set(row)=={'game','quotient_topics','label_signal_actions','coverage_signal_actions'}
        assert row['quotient_topics']==3
        assert set(row['coverage_signal_actions'])<=set(row['label_signal_actions'])<=set(range(4))
        assert row['label_signal_actions']==sorted(set(row['label_signal_actions']))
        assert row['coverage_signal_actions']==sorted(set(row['coverage_signal_actions']))
    signal=[x['game'] for x in details if x['label_signal_actions']]
    coverage=[x['game'] for x in details if x['coverage_signal_actions']]
    alias_only=[x['game'] for x in details if x['label_signal_actions'] and not x['coverage_signal_actions']]
    none=[x['game'] for x in details if not x['label_signal_actions']]
    assert (len(signal),len(coverage),len(alias_only),len(none))==(43,16,27,157)
    compiled_three=sum(sum(x['quotient_topics']**i for i in (1,2,3)) for x in details)
    original_six=sum(7**i for i in range(1,7)); compiled_six=sum(6**i for i in range(1,7))
    assert (compiled_three,original_six,compiled_six,compiled_two+compiled_three+compiled_six)==(7800,137256,55986,67626)
    domain={'scope':'Complete generated two-player input domain and saved 200-case diagnostics; policy outcomes reused from earlier evidence, no tests or RNG rerun.',
            'two_player_games':games,'two_player_SPE_count_grid_a_rows_b_columns':[[lookup[a,b] for b in range(4)] for a in range(4)],
            'random_seed_in_read_author_source':566240,'random_type_mask_map':{'1':3,'2':4,'3':7,'4':8,'5':11,'6':12,'7':15},
            'random_weights_and_full_policies_stored_in_report':False,'random_saved_diagnostics':details,
            'coverage_signal_game_ids':coverage,'alias_only_signal_game_ids':alias_only,'no_signal_game_ids':none,
            'six_player_case':{'weights':{'1':6,'2':1,'4':1,'8':1,'16':1,'96':1},'full_policy':'action 0 at every original history',
                               'projection':[0,1,2,3,4,5,5],'unit_customers':11,'actual_payoffs':[1,1,1,1,1,1],'W':6,'OPT6':11}}
    report={'status':'PASS-report-interpretation','primary_bytes':339,'all_nine_fields':author,
            'parent_first_nine_fields_equal':True,'replayed_author_stdout_byte_identical':True,
            'shared_execution_event':str((base/'replay/execution-event.json').relative_to(args.repository)),
            'shared_execution_event_sha256':sha256((base/'replay/execution-event.json').read_bytes()).hexdigest(),
            'count_semantics_sha256':sha256((base/'replay/count-semantics.json').read_bytes()).hexdigest(),
            'all_16_saved_private_mass_rows_read':True,'all_64_input_cases_accounted_for':True,'all_200_saved_case_diagnostics_read':True,
            'signal_cases':{'label_difference':43,'coverage_class_difference':16,'alias_only_difference':27,'no_detected_difference':157},
            'compiled_IC_decomposition':[compiled_two,compiled_three,compiled_six],
            'six_original_history_nodes':sum(7**i for i in range(6)), 'six_quotient_history_nodes':sum(6**i for i in range(6)),
            'six_quotient_lifts_including_terminals':sum(6**i for i in range(7)),
            'new_original_test_runs':0,'new_compiler_imports':0,'new_backward_induction_runs':0,'new_random_draws':0,
            'scope':'Current source/record interpretation and arithmetic only, reusing the existing unchanged author-suite execution and prior diagnostic outcomes; not another policy verification or general quotient proof.'}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'case-domain.json').write_text(json.dumps(domain,indent=2)+'\n')
    (args.out/'report-interpretation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','signal_cases','compiled_IC_decomposition','new_original_test_runs']},indent=2))


if __name__=='__main__':main()
