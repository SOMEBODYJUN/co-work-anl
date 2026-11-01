"""Independent unit-customer/state-closure check; no original or numerical imports."""
from pathlib import Path
from itertools import combinations
from collections import Counter, deque
from fractions import Fraction
import gzip
import hashlib
import json
import time
import sys

base = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve()
if target.exists():
    raise FileExistsError(target)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step(counts, flags, action):
    group = action // 6
    flags = list(flags)
    flags[group] = (action % 6) // 3 if sum(counts[6*group:6*group+6]) < 2 else 0
    counts = list(counts)
    counts[action] += 1
    return tuple(counts), tuple(flags)


all_reports = []
pay_caches = {}
clock = time.perf_counter()
for name in ['old-open', 'open-default', 'finish-scale2']:
    directory = base / name
    main = json.loads((directory / 'main-capture.json').read_text())
    report = json.loads((directory / 'report.json').read_text())
    source = json.loads(gzip.decompress((directory / 'original-state-and-pay-capture.json.gz').read_bytes()))
    assert main['k'] == 12 and main['n'] == 6 and main['L'] == 60
    scale = main['parameters']['scale2']
    units = []
    for group in range(2):
        X = range(6*group, 6*group+3)
        Y = range(6*group+3, 6*group+6)
        multiplicity = scale if group == 1 else 1
        for x in X:
            for y in Y:
                units.extend([(x,y)] * multiplicity)
        for I in combinations(X,2):
            for J in combinations(Y,2):
                units.extend([I+J] * (3*multiplicity))
    assert len(units) == 36*(1+scale)
    captured_types = Counter()
    for mask, weight in zip(main['types'], main['w']):
        assert weight > 0
        captured_types[tuple(a for a in range(12) if mask >> a & 1)] += weight
    assert Counter(units) == captured_types
    assert len(units) * 60 < 2**63
    cache = pay_caches.setdefault(scale,{})
    observed_pay = {tuple(row[0]): tuple(row[1]) for row in source['pay']}
    assert len(observed_pay) == len(source['pay'])
    for counts, expected in observed_pay.items():
        assert len(counts) == 12 and sum(counts) == 6 and min(counts) >= 0
        if counts not in cache:
            values = [0]*12
            for interests in units:
                load = sum(counts[a] for a in interests)
                if load:
                    assert 60 % load == 0
                    share = 60//load
                    for a in interests:
                        values[a] += share
            cache[counts] = tuple(values)
        assert cache[counts] == expected
    rows = {(tuple(r[0]),tuple(r[1])):r for r in source['states']}
    assert len(rows) == len(source['states']) == report['states']
    root = ((0,)*12,(0,0))
    queue = deque([root])
    reached = {root}
    inequalities = nonself = positive = tied = 0
    least = None
    levels = Counter()
    for key,row in rows.items():
        counts,flags = key
        assert len(counts) == 12 and len(flags) == 2 and min(counts) >= 0
        assert sum(counts) <= 6 and set(flags) <= {0,1}
        levels[sum(counts)] += 1
        end = tuple(row[2])
        assert len(end) == 12 and sum(end) == 6
        if sum(counts) == 6:
            assert end == counts and row[3] is None
            continue
        action = row[3]
        assert 0 <= action < 12
        values = []
        for other in range(12):
            child = step(counts,flags,other)
            assert child in rows
            terminal = tuple(rows[child][2])
            assert terminal[other] > 0
            values.append(cache[terminal][other])
        assert row[4] == max(values) == values[action]
        assert row[5] == [a for a,value in enumerate(values) if value == max(values)]
        assert end == tuple(rows[step(counts,flags,action)][2])
        for other,value in enumerate(values):
            delta = values[action] - value
            assert delta >= 0
            inequalities += 1
            if other != action:
                nonself += 1
                positive += delta > 0
                tied += delta == 0
                least = delta if least is None else min(least,delta)
    while queue:
        counts,flags = queue.popleft()
        if sum(counts) < 6:
            for action in range(12):
                child = step(counts,flags,action)
                if child not in reached:
                    reached.add(child)
                    queue.append(child)
    assert reached == set(rows)
    key = root
    path = []
    while sum(key[0]) < 6:
        action = rows[key][3]
        path.append(action)
        key = step(*key,action)
    assert path == report['path']
    profits = [str(Fraction(cache[key[0]][a],60)) for a in path]
    assert profits == report['payoffs']
    W = sum(any(key[0][a] for a in interests) for interests in units)
    assert str(W) == report['W']
    assert sum(cache[key[0]][a] * key[0][a] for a in range(12)) == W*60
    # Six X labels cover every customer, giving the exact maximum by total mass.
    cover = {0,1,2,6,7,8}
    assert all(any(a in cover for a in interests) for interests in units)
    examples = []
    for history in [(0,3),(3,0)]:
        state = root
        for action in history:
            state = step(*state,action)
        examples.append({'history':history,'counts':state[0],'flags':state[1],'action':rows[state][3]})
    all_reports.append({
        'case':name,'parameters':main['parameters'],'unit_customers':len(units),
        'state_count':len(rows),'states_by_depth':dict(sorted(levels.items())),
        'terminal_pay_vectors_checked':len(observed_pay),'including_self_IC':inequalities,
        'nonself_IC':nonself,'positive_nonself':positive,'tied_nonself':tied,
        'minimum_nonself_scaled_slack':least,'negative_IC':0,
        'all_states_reachable':True,'all_12_children_present':True,
        'path':path,'payoffs':profits,'W':W,'OPT_6':len(units),
        'half_slack':2*W-len(units),'reversed_local_history_examples':examples,
        'capture_sha256':sha(directory/'original-state-and-pay-capture.json.gz'),
        'original_report_sha256':sha(directory/'report.json'),
    })
answer = {'status':'PASS','independent_unit_state_audit_runs':1,'original_or_LP_DP_calls':0,
          'new_SPE_searches':0,'seconds':time.perf_counter()-clock,
          'scope':'three already captured complete deterministic state graphs; quotient transition proof covers every ordered history',
          'ordered_histories_not_individually_expanded':True,'cases':all_reports}
target.write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':answer['status'],'seconds':answer['seconds'],
                 'cases':[{k:r[k] for k in ['case','state_count','including_self_IC','W','OPT_6','half_slack']}
                          for r in all_reports]},ensure_ascii=False))
