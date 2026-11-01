"""Exact, one-pass attack on a specified cross-branch cap2 candidate.

Only existing complete SPE certificates are inputs. No random expansion, LP,
credentials, network or general efficiency theorem is involved. Every accepted
input is checked from its complete ordered strategy before column evaluation.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance


def evaluate(instance, strategy):
    m, k = instance.players, instance.topic_count
    actions = {tuple(row['history']): row['action'] for row in strategy['actions']}
    assert set(actions) == {h for d in range(m) for h in product(range(k), repeat=d)}

    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h + (actions[h],))

    @lru_cache(None)
    def profits(path):
        return instance.player_payoffs(path)

    comparisons = 0
    for h, a in actions.items():
        p = profits(finish(h))[len(h)]
        for alternative in range(k):
            assert p >= profits(finish(h + (alternative,)))[len(h)]
            comparisons += 1
    base = finish(())
    pb = profits(base)
    cb = [sum(a in customer.topics for a in base) for customer in instance.customers]
    branches = [(i, a, finish(base[:i] + (a,))) for i in range(m) for a in range(k)]
    reports = []
    for recipient in range(m):
        rows = []
        total = F(0)
        for sender in range(recipient):
            best = F(0)
            chosen = None
            for cut, forced, leaf in branches:
                if not sender < cut <= recipient:
                    continue
                pw = profits(leaf)[sender]
                positive = F(0)
                for customer, bload in zip(instance.customers, cb):
                    if (base[sender] in customer.topics
                            and base[recipient] in customer.topics
                            and leaf[recipient] not in customer.topics):
                        wload = sum(a in customer.topics for a in leaf)
                        assert bload > 0 and wload > 0
                        positive += F(customer.multiplicity, bload * wload)
                if not pw:
                    assert positive == 0
                    continue
                ratio = positive / pw
                if ratio > best:
                    best = ratio
                    chosen = {'cut_zero_based': cut, 'forced': forced,
                              'leaf': leaf, 'profit_W': str(pw),
                              'q_positive': str(positive), 'lambda': str(pb[sender] / pw)}
            amount = pb[sender] * best
            total += amount
            if chosen:
                rows.append({'sender_zero_based': sender, 'profit_B': str(pb[sender]),
                             'output': str(amount), **chosen})
        if not pb[recipient]:
            assert not total
            ratio = F(0)
        else:
            ratio = total / pb[recipient]
        reports.append({'recipient_zero_based': recipient, 'profit_B': str(pb[recipient]),
                        'total_positive': str(total), 'column_ratio': str(ratio),
                        'rows': rows})
    return {'path': base, 'profits': list(map(str, pb)),
            'verified_histories': len(actions), 'verified_comparisons': comparisons,
            'columns': reports}


def main():
    reports = []
    for source in sorted((ROOT / 'evidence/certificates/customer_attraction').glob('*.json')):
        obj = json.loads(source.read_text())
        if not isinstance(obj, dict):
            continue
        strategy = obj.get('strategy', obj)
        example = ROOT / 'examples/customer_attraction' / source.name
        if not isinstance(strategy, dict) or not {'actions', 'terminal_counts'} <= strategy.keys() or not example.exists():
            continue
        instance = Instance.from_dict(json.loads(example.read_text()))
        result = evaluate(instance, strategy)
        result['source'] = str(source.relative_to(ROOT))
        result['violates_cap2'] = any(F(x['column_ratio']) > 2 for x in result['columns'])
        reports.append(result)
    print(json.dumps({'claim': 'multi-branch amount-normalized prefix positive transfer has column cap2',
                      'scope': 'selected existing complete SPE certificates only',
                      'reports': reports}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
