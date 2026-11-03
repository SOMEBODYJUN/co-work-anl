"""Read every frozen policy entry; exact decimal-token audit, no discovery or LP."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
from collections import Counter
import json

ROOT=Path(__file__).resolve().parent
IDS=['8dff4693e3bf97c3ba2f','0905c42c5c46ff627c1d',
     '93c36ec44816004674fa','9425083aae6ad4d30e54']


def audit(sid):
    record=json.loads((ROOT/'original'/(sid+'.json')).read_text(),parse_float=str)
    b=record['best'];n,k=b['n'],b['k']
    weights=[F(x) for x in b['weights']]
    sparse=[(mask,w) for mask,w in enumerate(weights,1) if w]
    bg=b['background']
    sunk={mask:sum(bg[a] for a in range(k) if mask>>a&1) for mask,w in sparse}
    actions={tuple(map(int,h.split(','))) if h else ():a for h,a in b['actions'].items()}
    expected={h for d in range(n) for h in product(range(k),repeat=d)}
    assert set(actions)==expected and all(0<=a<k for a in actions.values())
    def terminal(h):
        while len(h)<n:h+=(actions[h],)
        return h
    def payoff(a,z,insert=False):
        count=Counter(z)
        return sum((w/(sunk[m]+int(insert)+sum(count[c] for c in range(k) if m>>c&1))
                    for m,w in sparse if m>>a&1),F(0))
    diffs=[]
    for h,a in actions.items():
        actual=payoff(a,terminal(h+(a,)))
        for alt in range(k):diffs.append(actual-payoff(alt,terminal(h+(alt,))))
    z=terminal(());assert list(z)==b['actual'];root=payoff(z[0],z)
    out=dict(id=sid,completed=record['completed'],n=n,k=k,
             histories=len(actions),comparisons_including_self=len(diffs),
             min_literal_decimal_ic=str(min(diffs)),min_literal_weight=str(min(weights)),
             root=str(root),reported_ratio=b['ratio'],background=bg,actual=list(z),
             all_fields_consumed=list(b),scope='fixed literal decimal inputs, not a floating tolerance proof or search replay')
    if 'query' in b:
        value=payoff(b['query'],z,True)
        out.update(query=b['query'],insertion=str(value),exact_insertion_ratio=str(value/root))
    if 'p' in b:
        p=[F(x) for x in b['p']];out['literal_query_mass']=str(sum(p))
        def price(t):return sum((p[a]*payoff(a,t,True) for a in range(k)),F(0))
        terms=list(combinations_with_replacement(range(k),n))
        out['query_against_all_integer_backgrounds']=str(min(map(price,terms)))
        out['all_integer_background_multisets']=len(terms)
    if 'menu' in b:
        menu=[[terminal((a,)).count(c) for c in range(k)] for a in range(k)]
        assert menu==b['menu']
        out['all_saved_menu_columns_match']=True
    return out


if __name__=='__main__':
    print(json.dumps([audit(sid) for sid in IDS],ensure_ascii=False,indent=2))
