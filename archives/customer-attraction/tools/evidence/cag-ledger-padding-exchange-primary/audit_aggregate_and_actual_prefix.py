"""Independent definition-level checks; no imported original solver or audit."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def payoff(types, path, who):
    counts = {}
    for mask, multiplicity in types.items():
        cover = sum(bool(mask & (1 << action)) for action in path)
        if mask & (1 << path[who]):
            counts[cover] = counts.get(cover, 0) + multiplicity
    return sum((F(n, d) for d, n in counts.items()), F(0))


def coverage(types, path):
    union = sum(1 << a for a in set(path))
    return sum(n for mask, n in types.items() if mask & union)


def insertion(types, path, query):
    return sum((F(n, 1 + sum(bool(mask & (1 << a)) for a in path))
                for mask, n in types.items() if mask & (1 << query)), F(0))


def audit(types, q, m, actions):
    histories = [h for k in range(m) for h in product(range(q), repeat=k)]
    assert set(actions) == set(histories)
    assert all(0 <= a < q for a in actions.values())

    def finish(prefix):
        h = tuple(prefix)
        while len(h) < m:
            h += (actions[h],)
        return h

    minimum = None
    min_selected = None
    checks = 0
    for h in histories:
        who = len(h)
        own = payoff(types, finish(h), who)
        min_selected = own if min_selected is None else min(min_selected, own)
        for a in range(q):
            gap = own - payoff(types, finish(h + (a,)), who)
            assert gap >= 0, (h, a, gap)
            minimum = gap if minimum is None else min(minimum, gap)
            checks += 1
    actual = finish(())
    result = dict(histories=len(histories), comparisons_including_self=checks,
                  nonself_comparisons=checks-len(histories), min_gap=minimum,
                  min_selected_payoff=min_selected, actual=actual,
                  payoffs=[payoff(types, actual, i) for i in range(m)],
                  W=coverage(types, actual),
                  OPT=max(coverage(types, p) for p in product(range(q), repeat=m)))
    return finish, result


def aggregate(types, finish, m, e):
    actual = finish(())
    distribution = [(6, 1-e), (2, e)]
    D, G, rows = F(0), F(0), []
    for i in range(m):
        d = sum((pa * payoff(types, finish(actual[:i] + (a,)), i)
                 for a, pa in distribution), F(0))
        g = sum((pa*pt*insertion(types, finish(actual[:i] + (a,)), t)
                 for a, pa in distribution for t, pt in distribution), F(0))
        D += d
        G += g
        rows.append(dict(D=d, G=g, gap=d-g))
    return dict(D=D, G=G, gap=D-G, rows=rows)


def main():
    old = dict(zip([4,27,29,30,31,32,43,45,46,51,53,54,59],
                   [1,4,3,3,2,1,3,3,3,3,3,3,2]))
    last = [[1,2,1,4,3,3,1], [2,0,0,4,3,3,0], [1,0,0,4,3,3,0],
            [1,0,0,4,5,4,4], [1,0,0,5,3,3,3], [1,0,0,4,3,3,3],
            [1,0,0,4,3,3,0]]
    second = [3,3,3,0,0,0,0]
    actions = {(): 0, **{(a,): second[a] for a in range(7)},
               **{(a,b): last[a][b] for a in range(7) for b in range(7)}}
    records = {}
    for K, J in [(1,0), (67,1)]:
        types = {mask: K*n for mask,n in old.items()}
        if J:
            types[64] = J
        finish, result = audit(types, 7, 3, actions)
        result['customers'] = sum(types.values())
        result['K'], result['J'] = K, J
        result['aggregate'] = aggregate(types, finish, 3, F(1,24))
        if J:
            assert result['aggregate']['gap'] == -F(7,384)
            assert result['W'] == 2144 and result['OPT'] == 2278
            masks = [tuple(mask for mask in types if mask & (1<<a)) for a in range(7)]
            assert all(masks) and len(set(masks)) == 7
        else:
            assert result['aggregate']['gap'] == -F(1,48)
            assert result['min_selected_payoff'] == F(29,3)
            assert result['W'] == 32 and result['OPT'] == 34
        records[f'aggregate_K{K}_J{J}'] = result

    cert_path = HERE/'comparison/e83180295536835c44f4/source'
    raw = cert_path.read_bytes()
    source = json.loads(raw)
    actions = {tuple(r['history']): r['action'] for r in source['certificate']['actions']}
    typed = {'A':12,'B':8,'C':4,'D':8,'AE':6,'AF':6,'CE':3,'CF':3,
             'AEF':6,'BEF':2,'CEF':1,'DEF':2}
    types = {sum(1 << (ord(a)-65) for a in label): n for label,n in typed.items()}
    finish, result = audit(types, 6, 4, actions)
    result['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    result['customers'] = sum(types.values())
    result['matrix'] = [[payoff(types, finish(result['actual'][:i] + (a,)), i)
                         for a in range(6)] for i in range(4)]
    assert result['actual'] == (1,0,0,5)
    assert result['matrix'] == [[9]*6,[13,5,11,10,11,11],
                                [13,5,11,10,11,11],[10,5,11,10,11,11]]
    assert result['W'] == 46 and result['OPT'] == 61
    br_rows = []
    f4_values = []
    for a,b in product(range(6), repeat=2):
        p = (0,a,b)
        values = [payoff(types, p+(t,), 3) for t in range(6)]
        br = [t for t in range(6) if values[t] == max(values)]
        f4_values.extend(payoff(types, p+(t,), 0) for t in br)
    assert min(f4_values) == 9
    for a in range(6):
        p = (1,0,a)
        values = [payoff(types, p+(t,), 3) for t in range(6)]
        br = [t for t in range(6) if values[t] == max(values)]
        entrants = [payoff(types, p+(t,), 2) for t in br]
        incumbent = [payoff(types, p+(t,), 1) for t in br]
        br_rows.append(dict(action=a, last_BR=br, next_payoff=entrants,
                            incumbent_payoff=incumbent))
    assert min(br_rows[0]['next_payoff']) == 13
    assert max(max(r['next_payoff']) for r in br_rows[1:]) == 11
    assert min(br_rows[0]['incumbent_payoff']) == 13
    result['f4_lower_from_all_36_prefixes_and_all_last_BR'] = min(f4_values)
    result['BA_two_remaining_BR_rows'] = br_rows
    result['f3'] = 13
    result['ratio_gap'] = F(9)-F(3,4)*13
    records['actual_prefix_61'] = result
    output = dict(status='pass', scope='three explicitly supplied finite certificates; no all-SPE or half search',
                  implementation='independent integer type sums representing distinct unit copies; no original solver imports',
                  records=records,
                  totals=dict(histories=sum(r['histories'] for r in records.values()),
                              comparisons_including_self=sum(r['comparisons_including_self'] for r in records.values()),
                              nonself_comparisons=sum(r['nonself_comparisons'] for r in records.values())))
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
