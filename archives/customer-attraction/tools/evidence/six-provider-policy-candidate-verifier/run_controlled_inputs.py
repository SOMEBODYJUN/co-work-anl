"""Six new controlled m=6 inputs, not replay of a historical search candidate.

The oracle expands actual unit clients and checks all 63 ordered nonterminal
histories for every case. It neither imports the verifier nor uses its 60//load
arithmetic. Each unchanged original CLI is executed once for its stated input.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE/'original/verify_policy_candidate.py'
SHA = '80657032a9aef3f6000634fee03f87b4666e98ef13cba84becc77f88bd2f56cc'
M, K = 6, 2


def clients(weights):
    return [frozenset(j for j in range(K) if b & (1 << j))
            for b, number in weights.items() for _ in range(number)]


def counts(history):
    return tuple(history.count(j) for j in range(K))


def utility(population, terminal_counts, action):
    return sum((F(1, sum(terminal_counts[j] for j in interest))
                for interest in population if action in interest),F())


def all_count_policy(action):
    return {','.join(map(str,q)):action for t in range(M)
            for q in sorted({counts(h) for h in product(range(K),repeat=t)})}


def count_spe_for_three_clients():
    population = clients({1:1,2:2})
    policy = {}
    @lru_cache(None)
    def best(q):
        if sum(q) == M:
            return q
        endpoints = [best(tuple(v+int(j==a) for j,v in enumerate(q))) for a in range(K)]
        action = max(range(K),key=lambda a:utility(population,endpoints[a],a))
        policy[','.join(map(str,q))] = action
        return endpoints[action]
    best((0,0))
    return policy


def fixtures():
    rational_policy = count_spe_for_three_clients()
    ordered_zero = {str(t):[0]*(K**t) for t in range(M)}
    ordered_distinct_history = {'0':[0],'1':[1,0]}
    for t in range(2,M):
        ordered_distinct_history[str(t)] = [j // (K**(t-1)) for j in range(K**t)]
    common = {'k':K,'m':M}
    return [
        ('zero_customers',dict(common,weights={},policy=all_count_policy(0)),{},None),
        ('empty_topic_and_uncovered_clients',dict(common,weights={'0':3,'1':1},ordered_policy=ordered_zero),{0:3,1:1},None),
        ('rational_default',dict(common,weights={'1':'1/3','2':'2/3'},policy=rational_policy),{1:1,2:2},None),
        ('same_policy_denominator_2',dict(common,weights={'1':'1/3','2':'2/3'},policy=rational_policy),{1:1,2:1},2),
        ('bad_policy_ratio_4',dict(common,weights={'1':1,'2':3},policy=all_count_policy(0)),{1:1,2:3},None),
        ('duplicate_topics_order_dependent',dict(common,weights={'3':1},ordered_policy=ordered_distinct_history),{3:1},None),
    ]


def oracle(data, integer_weights):
    population = clients(integer_weights)
    ordered = 'ordered_policy' in data
    def prescribed(history):
        if ordered:
            index = 0
            for a in history:
                index = K*index+a
            return data['ordered_policy'][str(len(history))][index]
        return data['policy'][','.join(map(str,counts(history)))]
    @lru_cache(None)
    def finish(history):
        return history if len(history)==M else finish(history+(prescribed(history),))
    full_checks, representative_checks, negative = [], [], []
    for t in range(M-1,-1,-1):
        grouped = {}
        for index,history in enumerate(product(range(K),repeat=t)):
            a = prescribed(history)
            endpoint = counts(finish(history+(a,)))
            own = utility(population,endpoint,a)
            for b in range(K):
                if b==a:
                    continue
                alt = utility(population,counts(finish(history+(b,))),b)
                slack = own-alt
                scaled = 60*slack
                assert scaled.denominator == 1
                full_checks.append({'history':history,'chosen':a,'alternative':b,
                                    'rational_slack':str(slack),'slack_times_60':int(scaled)})
                if ordered:
                    representative_checks.append(scaled)
                    if slack<0:
                        negative.append([t,index,a,b,int(scaled)])
                else:
                    q = counts(history)
                    value = (a,b,int(scaled))
                    assert q not in grouped or grouped[q]==value
                    grouped[q] = value
        if not ordered:
            for q,(a,b,scaled) in sorted(grouped.items()):
                representative_checks.append(F(scaled))
                if scaled<0:
                    negative.append([list(q),a,b,scaled])
    actual = counts(finish(()))
    covered = lambda selected:sum(any(j in interest for j in selected) for interest in population)
    welfare = covered(finish(()))
    # Independently maximize over all six-action ordered histories, allowing repeats.
    opt = max(covered(h) for h in product(range(K),repeat=M))
    covers = [frozenset(i for i,c in enumerate(population) if j in c) for j in range(K)]
    distinct = len(set(covers))==K
    expected = {'m':M,'topics':K,'distinct_topic_sets':distinct,
                'unit_customers':len(population),'support_types':len(integer_weights),
                'checked_IC':len(representative_checks),'negative_IC_count':len(negative),
                'first_negative_IC':negative[:5],'actual_counts':list(actual),'welfare':welfare,
                'OPT6':opt,'ratio':str(F(opt,welfare)) if welfare else None,
                'strict_original_counterexample':bool(distinct and not negative and opt>2*welfare),
                'integer_weights':{str(b):n for b,n in integer_weights.items()}}
    return expected, full_checks


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
    output = HERE/'controlled-runs'
    output.mkdir(exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    events = []
    with tempfile.TemporaryDirectory(prefix='integer-policy-controls-',dir=HERE) as temporary:
        root = Path(temporary)
        script = root/'verify_policy_candidate.py'
        shutil.copyfile(SOURCE,script)
        for name,data,weights,denominator in fixtures():
            folder = output/name
            folder.mkdir()
            payload = (json.dumps(data,indent=2)+'\n').encode()
            (folder/'candidate.json').write_bytes(payload)
            candidate = root/(name+'.json')
            candidate.write_bytes(payload)
            expected,full_checks = oracle(data,weights)
            argv = [sys.executable,'-I','-B',str(script),str(candidate)]
            if denominator is not None:
                argv += ['--denominator',str(denominator)]
            outfile = root/'explicit-output.json'
            if name=='empty_topic_and_uncovered_clients':
                argv += ['--output',str(outfile)]
            tick = time.monotonic()
            result = subprocess.run(argv,cwd=root,capture_output=True,check=False)
            elapsed = time.monotonic()-tick
            (folder/'stdout.json').write_bytes(result.stdout)
            (folder/'stderr.txt').write_bytes(result.stderr)
            assert result.returncode==0 and not result.stderr
            observed = json.loads(result.stdout)
            assert set(observed)==set(expected)|{'optimal_topics'}
            assert all(observed[k]==v for k,v in expected.items())
            selected = observed['optimal_topics']
            if observed['OPT6']:
                assert selected and len(selected)<=M and len(set(selected))==len(selected)
                assert all(j in range(K) for j in selected)
                assert sum(any(j in c for j in selected) for c in clients(weights))==observed['OPT6']
            else:
                assert selected is None
            if name=='empty_topic_and_uncovered_clients':
                assert outfile.read_bytes()==result.stdout[:-1]
                (folder/'explicit-output.json').write_bytes(outfile.read_bytes())
            assert candidate.read_bytes()==payload
            assert hashlib.sha256(script.read_bytes()).hexdigest()==SHA
            (folder/'independent-oracle.json').write_text(json.dumps(
                {'expected_fields':expected,'full_ordered_history_ICs':full_checks,
                 'all_63_ordered_histories_checked':len(full_checks)==63,
                 'source_compressed_count_or_ordered_field_count':expected['checked_IC']},indent=2)+'\n')
            events.append({'case':name,'argv':argv,'cwd':str(root),'exit_code':result.returncode,
                           'wall_seconds':elapsed,'candidate_sha256':hashlib.sha256(payload).hexdigest(),
                           'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
                           'stdout_bytes':len(result.stdout),'stderr_bytes':0,
                           'original_source_unchanged':True,'candidate_unchanged':True,
                           'all_15_fields_checked_against_unit_client_oracle':True,
                           'summary':observed})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
    report = {'scope':'Six newly constructed m=6 control inputs; original CLI once per stated input. Not a historical search replay or a half theorem.',
              'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
              'python_version':sys.version,'assertions_enabled_in_wrapper':True,
              'source_sha256':SHA,'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'original_entries':len(events),'all_exit_codes_zero':True,
              'source_ICs_checked':sum(e['summary']['checked_IC'] for e in events),
              'independent_ordered_history_ICs':63*len(events),
              'denominator_2_detected_negative_IC':events[3]['summary']['negative_IC_count']>0,
              'ratio_4_bad_policy_rejected_despite_exit_0':events[4]['summary']['ratio']=='4' and events[4]['summary']['negative_IC_count']>0,
              'duplicate_topics_order_dependent_actual_counts':events[5]['summary']['actual_counts'],
              'temporary_directory_removed':not root.exists(),'events':events}
    assert report['denominator_2_detected_negative_IC'] and report['ratio_4_bad_policy_rejected_despite_exit_0']
    (output/'execution.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    run()
