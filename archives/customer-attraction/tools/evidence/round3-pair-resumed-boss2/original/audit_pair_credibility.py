"""Independent definition-level audit of indexed two-player credibility.

No explorer row evaluator is imported. Read exact frozen masses, rebuild the
literal lists of local memberships, and sum the genuine two-player comparison
cost over every ordered branch/query triple. This proves no new SPE theorem:
the symbolic identity in the companion note supplies the universal argument.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').exists())
ACTOR = Path(__file__).resolve().parents[1]


def payoff(q, rival, background):
    return F(q, background + 1 + rival) if q else F(0)


def pair_cost(t, s, background, retained):
    # Shapley harmonic increment for retained=True; entrant profit otherwise.
    if retained:
        return sum((F(1, background + j) for j in range(1, t+s+1)), F(0))
    return F(t+s, background+t+s) if t+s else F(0)


def orbit(i, j, k):
    if i == j == k:
        return 'all_equal'
    if j == k:
        return 'query_equal'
    if i == j:
        return 'first_branch'
    if i == k:
        return 'second_branch'
    return 'all_distinct'


def audit_identity():
    checked = 0
    for p in (0, 1, 2, 7, 1000):
        for a, b, t, s, q in product((0, 1), repeat=5):
            D = (p+1)*(p+2)
            ua, ub = payoff(a, b, p), payoff(b, a, p)
            lhs = ua + ub + F(a, D) - pair_cost(t, s, p, True)
            incentives = (ua-payoff(t, q, p)
                          +payoff(q, t, p)-payoff(s, t, p)
                          +ub-payoff(q, a, p))
            residual = F(a*(1-q), D)
            assert lhs == incentives+residual
            checked += 1
    return checked


def reconstruct(atoms, denominator=None):
    totals = {}
    counts = {}
    for atom in atoms:
        bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
        mass = F(atom['exact_mass']) if denominator is None else F(atom['mass_numerator'], denominator)
        assert mass >= 0
        for family, field, arity, fixed in (
                ('AB', 'AB_hist', 3, 'AB'),
                ('AE', 'AE_hist', 3, 'AE'),
                ('Sbranch', 'second_hist', 4, 'A')):
            data = []
            for ty, multiplicity in zip(product((0, 1), repeat=arity), atom[field]):
                data.extend([ty]*multiplicity)
            for x, y in combinations_with_replacement(range(arity), 2):
                for retained in (False, True):
                    local = {}
                    for i, ty in enumerate(data):
                        p = sum(bits[z] for z in fixed) + sum(ty[:-2])
                        a, b = ty[-2:]
                        H = payoff(a, b, p)+payoff(b, a, p)+F(a, (p+1)*(p+2))
                        for j, k in product(range(len(data)), repeat=2):
                            tag = orbit(i, j, k)
                            local[tag] = local.get(tag, F(0)) + H-pair_cost(data[j][x], data[k][y], p, retained)
                    for tag, value in local.items():
                        key = ('strong:' if retained else '')+f'{family}:pair:{x}{y}:{tag}'
                        totals[key] = totals.get(key, F(0))+mass*value
                        counts[key] = counts.get(key, 0)+1
    assert all(v == len(atoms) for v in counts.values())
    return totals


def selected_old_rows(atom):
    """Rebuild just the fifteen original rows used by the Farkas witness.

    These are written directly from literal payoff/guarantee definitions,
    independently of both original 437-row implementation and reoptimizer.
    """
    b = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    paths = {'actual':'ABCDE', 'second':'AEUVW', 'third':'ABEXY'}
    data = {}
    for family, field, arity in (('AB','AB_hist',3),('AE','AE_hist',3),('Sbranch','second_hist',4)):
        data[family] = [ty for ty,n in zip(product((0,1),repeat=arity),atom[field]) for _ in range(n)]
    def share(path, i):
        n = b[path[i]]
        return F(n, sum(b[t] for t in path)) if n else F(0)
    result = {}
    result['actual:5:K:W'] = share(paths['actual'],4)-F(b['W'],sum(b[t] for t in 'ABCD')+1)
    d = sum(ty[0] for ty in data['AB'])
    p = sum(b[t] for t in 'ABC')
    ell,h = atom['menus_lh'][0]
    result['actual:reply:V'] = F(d*ell-5*h,(p+1)*(p+2))
    for idx,name in ((1,'second'),(2,'third')):
        path = paths[name]
        p = sum(b[t] for t in path[:3])
        ell,h = atom['menus_lh'][idx]
        result[f'{name}:reply:topic-D'] = F(ell-5*b['D'],p+1)+F(d*b['D']-h,(p+1)*(p+2))
    for family, fixed, position, topic in (
            ('AB','AB',0,'V'),('AB','AB',1,'V'),('AB','AB',1,'X'),
            ('AB','AB',1,'Y'),('AE','AE',1,'D'),
            ('Sbranch','A',0,'V'),('Sbranch','A',1,'X')):
        r = F(0)
        for ty in data[family]:
            p = sum(b[t] for t in fixed)+sum(ty[:-2])
            # In Sbranch the third mover is the U coordinate; otherwise X.
            pos = position+1
            n = ty[pos]
            actual = F(n,sum(b[t] for t in fixed)+sum(ty)) if n else F(0)
            remaining = len(ty)-pos
            prefix = sum(b[t] for t in fixed)+sum(ty[:pos])
            r += actual-F(b[topic],prefix+remaining)
        stage = (3 if family=='Sbranch' else 4)+position
        result[f'{family}:{stage}:K:{topic}'] = r
    ry = sum(ty[2] for ty in data['AE'])
    result['AE:actual:1:sum-Y'] = 5*share(paths['actual'],0)-F(ry,5)
    result['AE:second:3:sum-Y'] = 5*share(paths['second'],2)-F(ry,b['A']+b['E']+3)
    rw = sum(ty[3] for ty in data['Sbranch'])
    result['Sbranch:3:sum-W'] = sum((5*(F(ty[1],b['A']+sum(ty)) if ty[1] else F(0))-F(rw,b['A']+ty[0]+3) for ty in data['Sbranch']),F(0))
    result['second:5:sum-SW'] = 5*share(paths['second'],4)-F(rw,sum(b[t] for t in 'AEUV')+1)
    assert len(result)==15
    return result


def audit_farkas(original):
    path = ACTOR/'round3_closure/frozen_pair_reoptimization.json'
    report = json.loads(path.read_text())['retained_overlap_pair_tax']
    multipliers = {name:F(v) for name,v in report['farkas_multipliers'].items()}
    assert all(v>0 for v in multipliers.values())
    residuals = []
    for atom in original['atoms']:
        rr = selected_old_rows(atom)
        pairs = reconstruct([dict(atom,exact_mass='1')])
        for name in multipliers:
            if ':pair:' in name:
                rr[name] = pairs['strong:'+name]
        combined = sum((weight*rr[name] for name,weight in multipliers.items()),F(0))
        residuals.append(-F(int(any(map(int,atom['bits'][:5]))))-combined)
    assert min(residuals)>=0
    assert residuals == [F(x) for x in report['certificate_residuals']]
    return {'scope':'normalized cone on the old 64 atom types only',
            'positive_multipliers':len(multipliers),
            'columns':len(residuals), 'minimum_residual':str(min(residuals)),
            'all_original_and_new_used_rows_rebuilt_without_importing_explorer':True}


def main():
    identity_cases = audit_identity()
    original_path = ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
    augmented_path = ACTOR/'continuation_completion/frozen_support_augmented.json'
    explorer_path = ACTOR/'round3_closure/partition_pair_closure.json'
    original = json.loads(original_path.read_text())['primal']
    augmented = json.loads(augmented_path.read_text())
    explorer = json.loads(explorer_path.read_text())
    reports = {}
    for name, atoms, denominator in (
            ('original_64_atoms', original['atoms'], original['denominator']),
            ('augmented_42_atoms', augmented['atoms'], None)):
        values = reconstruct(atoms, denominator)
        expected = {k:F(v) for k,v in explorer['reports'][name]['all_rows'].items()}
        assert values == expected
        negative = {k:str(v) for k,v in values.items() if v<0}
        reports[name] = {
            'row_count':len(values), 'negative_rows':negative,
            'negative_count':len(negative),
            'negative_loose_count':sum(not k.startswith('strong:') for k in negative),
            'negative_retained_count':sum(k.startswith('strong:') for k in negative)}
    output = {
        'status':'exact independent reconstruction passed',
        'scope':'two frozen marginal witnesses excluded; no general half proof or SPE counterexample',
        'identity_cases':identity_cases,
        'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (original_path, augmented_path, explorer_path)},
        'reports':reports,
        'strong_farkas':audit_farkas(original)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({**output,'reports':{n:{k:v for k,v in r.items() if k!='negative_rows'} for n,r in reports.items()}},indent=2))


if __name__ == '__main__':
    main()
