"""Attack the explicit uniform forest last-slot-floor candidate.

Finite output is evidence only. A found violation is expanded to a complete
ordered-history SPE and checked by the existing definition-level verifier.
"""
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def counts(p, total):
    if p == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in counts(p - 1, total - first):
            yield (first,) + tail


def generator(rng, p, m):
    old = [0]
    new = list(range(1, p))
    types = []
    while new:
        parent = rng.choice(old)
        width = rng.randint(1, min(3, len(new)))
        attached = [new.pop(0) for _ in range(width)]
        types.append(CustomerType(frozenset([parent] + attached), rng.randint(1, 12)))
        old.extend(attached)
    for a in range(p):
        value = rng.choice([0, 0, 1, 2, 3, 5, 8, 13])
        if value:
            types.append(CustomerType(frozenset([a]), value))
    return Instance(tuple(f'T{a}' for a in range(p)), tuple(types), m)


def floor(instance):
    values = []
    for prefix in counts(instance.topic_count, instance.players - 1):
        menu = []
        for action in range(instance.topic_count):
            final = prefix[:action] + (prefix[action] + 1,) + prefix[action + 1:]
            menu.append(instance.topic_payoffs(final)[action])
        values.append(max(menu))
    return min(values)


def main():
    rng = random.Random(202610231)
    started = time.monotonic()
    record = []
    for index in range(240):
        p = (4, 5, 6)[index % 3]
        m = (3, 4, 5, 6)[(index // 3) % 4]
        instance = generator(rng, p, m)
        theta = floor(instance)
        solver = ExactSPESolver(instance)
        root = solver.outcomes()
        bad = next((q for q in root if any(q[a] and instance.topic_payoffs(q)[a] < theta
                                          for a in range(p))), None)
        if bad is not None:
            cert = solver.certificate(bad)
            verify_certificate(instance, cert).assert_valid()
            result = {'candidate': 'every remaining SPE player >= global last-slot floor for forest incidence',
                      'status': 'counterexample', 'index': index,
                      'theta': str(theta), 'instance': instance.to_dict(),
                      'root_counts': bad, 'payoffs': [str(x) for x in instance.topic_payoffs(bad)],
                      'full_strategy': cert.to_dict(),
                      'root_outcome_count': len(root), 'seconds': time.monotonic() - started}
            out = Path(__file__).with_name('forest_floor_counterexample.json')
            out.write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps({k: v for k, v in result.items() if k != 'full_strategy'}), flush=True)
            return
        record.append({'p': p, 'm': m, 'theta': str(theta), 'root_outcomes': len(root)})
        if index % 12 == 11:
            print(json.dumps({'checked': index + 1, 'seconds': time.monotonic() - started}), flush=True)
    out = Path(__file__).with_name('forest_floor_probe.json')
    out.write_text(json.dumps({'candidate': 'forest last-slot floor', 'found_counterexample': False,
                               'universal_claim_proved': False, 'cases': record,
                               'seconds': time.monotonic() - started}, indent=2) + '\n')


if __name__ == '__main__':
    main()
