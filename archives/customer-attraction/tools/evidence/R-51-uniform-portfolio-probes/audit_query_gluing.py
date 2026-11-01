"""Check the canonical certificate realizes all path-query minima at once."""
from pathlib import Path
from fractions import Fraction
import json
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'replay'))
import portfolio_probe as probe
from customer_attraction.certificate import verify_certificate


def check(inst):
    result, solver = probe.check(inst)
    slack, actual, portfolio, welfare, query = result
    cert = solver.certificate(on_path=actual)
    verified = verify_certificate(inst, cert)
    assert verified.valid, verified
    actions = cert.actions

    def terminal(h):
        while len(h) < inst.players:
            h += (actions[h],)
        return h

    actual_payoffs = inst.player_payoffs(actual)
    minima = []
    prefix = [0]*inst.topic_count
    for i, chosen in enumerate(actual):
        for a in range(inst.topic_count):
            child = prefix.copy()
            child[a] += 1
            expected = (actual_payoffs[i] if a == chosen else
                        min(inst.topic_payoff(a, q) for q in solver.outcomes(child)))
            observed = inst.player_payoffs(terminal(actual[:i] + (a,)))[i]
            assert expected == observed, (i, a, expected, observed)
            minima.append((i, a, expected))
        prefix[chosen] += 1
    observed_query = sum((v for i, a, v in minima for b in portfolio if a == b), Fraction())
    assert observed_query == query
    return dict(instance=inst.to_dict(), actual=actual, portfolio=portfolio,
                W=welfare, OPT=inst.optimal_welfare(), query=str(query), slack=str(slack),
                checked_query_pairs=len(minima), certificate_valid=True,
                certificate=cert.to_dict())


if __name__ == '__main__':
    rng = random.Random(734170)
    for sample in range(24):
        customers = []
        for mask in range(1, 1 << 5):
            w = rng.choices([0, 1, 2, 3, 5, 8], [8, 8, 3, 2, 1, 1])[0]
            if w:
                customers.append(probe.CustomerType(frozenset(a for a in range(5)
                    if mask & (1 << a)), w))
        inst = probe.Instance(tuple(map(str, range(5))), tuple(customers), 3)
    records = {'seed734170_sample23': check(inst)}
    for name in ['smoke_input', 'big_family']:
        inst = probe.Instance.from_dict(json.loads((HERE/'replay'/f'{name}.json').read_text()))
        records[name] = check(inst)
    (HERE/'query_gluing.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps({name: {k:v for k,v in data.items() if k not in ['instance','certificate']}
                      for name,data in records.items()}, indent=2))
