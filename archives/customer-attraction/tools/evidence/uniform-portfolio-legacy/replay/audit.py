from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations_with_replacement, product
from pathlib import Path
import json
import math

from customer_attraction import CustomerType, Instance
from customer_attraction.certificate import StrategyCertificate

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / 'research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/global'


def load(name):
    spec = spec_from_file_location(name, SOURCES / (name + '.py'))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


search = load('uniform_portfolio_search')
cone = load('uniform_portfolio_cone')


def leaf(actions, history, players):
    while len(history) < players:
        history += (actions[history],)
    return history


def payoff(customers, history, topic):
    return sum((Fraction(weight, sum(action in liked for action in history))
                for liked, weight in customers if topic in liked), Fraction(0))


def coverage(customers, history):
    return sum(weight for liked, weight in customers if liked.intersection(history))


def check(instance, cert):
    m, p = instance.players, instance.topic_count
    catalog = range(p)
    actions = cert.actions
    histories = [h for size in range(m) for h in product(catalog, repeat=size)]
    assert set(histories) == set(actions)
    customers = [(entry.topics, entry.multiplicity) for entry in instance.customers]
    for history in histories:
        chosen = actions[history]
        following = leaf(actions, history, m)
        for action in catalog:
            deviating = leaf(actions, history + (action,), m)
            assert payoff(customers, following, chosen) >= payoff(customers, deviating, action)
    actual = leaf(actions, (), m)
    assert tuple(actual.count(a) for a in catalog) == cert.terminal_counts
    welfare = coverage(customers, actual)
    values = [[payoff(customers, leaf(actions, actual[:i] + (a,), m), a)
               for i in range(m)] for a in catalog]
    costs = list(map(sum, values))
    by_query = {}
    for query in product(catalog, repeat=m):
        o = coverage(customers, query)
        by_query[query] = (m * o - (m - 1) * welfare - sum(costs[a] for a in query), o)
    best = max(pair[0] for pair in by_query.values())
    query = next(query for query, pair in by_query.items() if pair[0] == best)
    result = search.attack(instance, cert)
    expected = dict(gap=best, query=query, optimum=by_query[query][1], actual=actual,
                    welfare=welfare, deviation_costs=costs, deviation_values=values)
    assert result == expected
    return dict(players=m, topics=p, histories=len(histories),
                nonself_deviations=len(histories) * (p - 1), ordered_queries=p**m,
                multisets=math.comb(p + m - 1, m), max_gap=str(best),
                argmax_query=query, argmax_coverage=by_query[query][1],
                true_optimum=max(pair[1] for pair in by_query.values()),
                welfare=welfare), by_query


def check_cone(instance, cert):
    p, m = instance.topic_count, instance.players
    masks, membership, rows, actual_cov, query_rows, actual = cone.cone_data(instance, cert)
    assert masks == list(range(1, 2**p))
    actions = cert.actions
    assert actual == leaf(actions, (), m)
    types = [{a for a in range(p) if mask & (1 << a)} for mask in masks]
    assert membership.tolist() == [[int(a in liked) for a in range(p)] for liked in types]
    assert actual_cov.tolist() == [int(bool(liked.intersection(actual))) for liked in types]
    expected = []
    for length in range(m):
        for h in product(range(p), repeat=length):
            t = leaf(actions, h, m)
            chosen = actions[h]
            for action in range(p):
                if action == chosen:
                    continue
                dev = leaf(actions, h + (action,), m)
                expected.append([float(payoff([(liked, 1)], t, chosen))
                                 - float(payoff([(liked, 1)], dev, action))
                                 for liked in types])
    assert Counter(map(tuple, expected)) == Counter(map(tuple, rows.tolist()))
    for a, row in enumerate(query_rows):
        for liked, value in zip(types, row):
            expected_query = sum(payoff([(liked, 1)], leaf(actions, actual[:i] + (a,), m), a)
                                 for i in range(m))
            assert math.isclose(value, float(expected_query), rel_tol=0, abs_tol=1e-14)
    return {'masks': len(masks), 'coefficient_rows': len(rows), 'query_columns': len(query_rows)}


fixtures = {}
excluded = []
for path in sorted((ROOT / 'examples/customer_attraction').glob('*.json')):
    partner = ROOT / 'evidence/certificates/customer_attraction' / path.name
    if not partner.is_file():
        continue
    data = json.loads(partner.read_text())
    if 'actions' not in data:
        excluded.append(path.stem)
        continue
    instance = Instance.from_dict(json.loads(path.read_text()))
    cert = StrategyCertificate.from_dict(data)
    fixtures[path.stem], _ = check(instance, cert)
    fixtures[path.stem]['cone_data_check'] = check_cone(instance, cert)

instance = Instance(('large', 'small'), (CustomerType(frozenset({0}), 6),
                                         CustomerType(frozenset({1}), 1)), 3)
policy = {history: 0 for size in range(3) for history in product(range(2), repeat=size)}
cert = StrategyCertificate(policy, (3, 0))
control, scores = check(instance, cert)
control['cone_data_check'] = check_cone(instance, cert)
control['original_padding_gap'] = str(scores[0, 1, 0][0])
control['alternative_padding_gap'] = str(scores[0, 1, 1][0])
assert scores[0, 1, 0] == (-6, 7) and scores[0, 1, 1] == (-3, 7)
assert control['max_gap'] == '-3'
print(json.dumps(dict(frozen_replay=fixtures, excluded_no_top_level_actions=excluded,
                      padding_control=control), ensure_ascii=False, indent=2))
