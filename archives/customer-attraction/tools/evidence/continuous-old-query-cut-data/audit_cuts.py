"""Read all 64 frozen cuts and independently evaluate their exact projections.

No discovery LP and no import of any old generator.  This evaluates the stated
cut family only, not all 5108/10344 constraints or complete-history strategies.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
EV = HERE.parent
CUTS = HERE/'original/continuous_old_query_cuts.json'
OLD = EV/'continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json'
MASTER = EV/'full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'
PAIR = EV/'full156-pair-master-point/original/pair_master_exact.json'
PAT = tuple(product((0, 1), repeat=3))
EXPECTED = {
    CUTS: 'e9ce9c66ea5598038ad7f5aa19cfab44d5156c8e35b3081665481153a968c4fa',
    OLD: '0c06316a0ad5b4079c54d36cf59255c36943af957644b0ffab1b34a249ee6f7c',
    MASTER: 'd1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8',
    PAIR: '090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2',
}


def key(g):
    f, diag, wi, wj = g
    return f, diag, tuple(wi), tuple(wj)


def read_point(point):
    hs, hi = {}, None
    for i, c in enumerate(point['columns']):
        w = F(c['weight'])
        assert w >= 0
        if c['kind'] == 'hist':
            hi = i
            hs[hi] = {'a': tuple(map(int, c['actual_bits'])), 'mass': w,
                      'hist': c['hist'], 'marginals': {}}
        elif c['kind'] == 'joint-reply':
            g = key(c['group'])
            m = hs[hi]['marginals'].setdefault(g, [F(), F()])
            for member in range(2):
                m[member] += w*c['state'][member]
    assert len(hs) == 16
    return hs


@lru_cache(None)
def psi(i, p, ell, t, q, am, al, mu):
    n = 5-i
    candidates = []
    # All intermediate prices equal am: a count s represents all their bits.
    for s, g in product(range(n), range(2)):
        z = p+t+s+g
        candidates.append((F(t, z) if t else F())
                          - (mu*F(g, z) if g else F())
                          + (am*s+al*g)/F(ell+1)
                          + mu*F(q, p+t+s+1))
    return min(candidates)


def evaluate(hs, cut):
    i, member, family, diagonal, qi, ams, als, mus = cut
    am, al, mu = map(F, (ams, als, mus))
    count = 6 if diagonal else 30
    value = F()
    for h in hs.values():
        a, mass = h['a'], h['mass']
        whole, p, ell = sum(a), sum(a[:i]), sum(a[:5])
        own = F(a[i], whole) if a[i] else F()
        last = F(a[5], whole) if a[5] else F()
        value += count*mass*(own+((4-i)*am+al)*last)
        for g, marginal in h['marginals'].items():
            f, diag, wi, wj = g
            if (f, diag) != (family, diagonal):
                continue
            ni, nj = h['hist'][PAT.index(wi)], h['hist'][PAT.index(wj)]
            mult = ni if diag else ni*nj-(ni if wi == wj else 0)
            q = (wi+wj)[qi]
            t_mass = marginal[member]
            assert 0 <= t_mass <= mass
            value -= mult*((mass-t_mass)*psi(i,p,ell,0,q,am,al,mu)
                           + t_mass*psi(i,p,ell,1,q,am,al,mu))
    return value


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    loaded = {}
    for path, sha in EXPECTED.items():
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha
        loaded[path] = json.loads(raw)
    source = loaded[CUTS]
    assert set(source) == {'scope', 'input', 'parameter_bounds', 'LPs', 'selected'}
    assert source['parameter_bounds'] == [0,1000] and source['LPs'] == 180
    records = source['selected']
    assert len(records) == 64
    cuts = [r['cut'] for r in records]
    assert len({tuple(c) for c in cuts}) == 64
    for r in records:
        assert set(r) == {'cut', 'slack'} and len(r['cut']) == 8
        i,m,f,d,q,am,al,mu = r['cut']
        assert i in range(5) and m in range(2) and (f,d) in ((0,0),(1,0),(1,1)) and q in range(6)
        assert all(isinstance(v,str) for v in (am,al,mu))
        assert all(0 <= F(v) <= 1000 for v in (am,al,mu))
        assert F(r['slack']) < 0
    old_hs, master_hs = read_point(loaded[OLD]), read_point(loaded[MASTER])
    pair_hs = read_point(loaded[MASTER])
    new_z = {}
    for c in loaded[PAIR]['variables']:
        k = c['hist_column'], key(c['group'])
        new_z[k] = new_z.get(k,F())+F(c['weight'])
    for hi, h in pair_hs.items():
        for g, values in h['marginals'].items():
            values[1] = new_z.get((hi,g),F())
    results = []
    for j, r in enumerate(records):
        old = evaluate(old_hs,r['cut'])
        master = evaluate(master_hs,r['cut'])
        pair = evaluate(pair_hs,r['cut'])
        assert old == F(r['slack']) < 0
        assert master >= 0 and pair >= 0
        results.append({'position':j,'cut':r['cut'],'old_4971_slack':str(old),
                        'combined_5108_slack':str(master),'changed_Z_pair_slack':str(pair)})
    summary = {}
    for name in ('old_4971_slack','combined_5108_slack','changed_Z_pair_slack'):
        vals = [F(r[name]) for r in results]
        summary[name] = {'rows':64,'negative':sum(v<0 for v in vals),
                         'zero':sum(v==0 for v in vals),'positive':sum(v>0 for v in vals),
                         'minimum':str(min(vals)), 'maximum':str(max(vals))}
    later = HERE/'related/continuous_refinement_cuts.json'
    comparison = None
    if later.exists():
        ld = json.loads(later.read_text())
        later_cuts = {tuple(c) for c in ld['cuts']}
        old_cuts = {tuple(c) for c in cuts}
        comparison = {'later_bytes':later.stat().st_size,
                      'later_sha256':hashlib.sha256(later.read_bytes()).hexdigest(),
                      'later_count':len(ld['cuts']), 'exact_tuple_intersection':len(later_cuts&old_cuts),
                      'later_only_cuts':sorted(later_cuts-old_cuts),
                      'later_in_old_first_32':sum(tuple(c) in later_cuts for c in cuts[:32])}
    return {'status':'PASS_ALL_64_CUTS_EXACT_THREE_STAGE_EVALUATION',
            'scope':'Independent by-count mathematical projection and exact integration at three finite points; not discovery optimality or all old rows at changed Z.',
            'python_version':sys.version,
            'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'source_sha256':{str(p.relative_to(EV)):s for p,s in EXPECTED.items()},
            'metadata':{k:v for k,v in source.items() if k!='selected'},
            'coordinate_counts':{name:dict(Counter(str(c[j]) for c in cuts))
                                 for j,name in enumerate(('source_index','member','family','diagonal','query_bit','alpha_middle','alpha_last','mu'))},
            'old_slacks_exactly_match_all_saved_values':True,
            'old_record_order_is_exact_nondecreasing':all(F(records[j]['slack'])<=F(records[j+1]['slack']) for j in range(63)),
            'stage_summaries':summary, 'all_64_rows':results, 'later_list_comparison':comparison,
            'not_certified':['all other rows at changed Z','completeness of continuous cut family',
                             'exact LP or graph optimum','complete-history SPE','universal half theorem']}


if __name__ == '__main__':
    result = run()
    (HERE/'three-stage-cut-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
