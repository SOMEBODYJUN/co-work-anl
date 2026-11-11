"""Independent standard-library audit of the shared old-C / root-tail measure.

No discovery, common-interface module, coefficient generator, NumPy, SciPy or
SymPy is imported. The terminal checks explicitly expand all 720 simultaneous
index permutations and every one of the 216 literal terminal comparisons.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import lcm
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(a, b):
    return F(a, b) if a else F(0)


def decode(word, length):
    return tuple(map(int, f'{word:0{length}b}'))


def interface_orbits(actual, old, new):
    p = sum(map(int, actual[:3]))
    ans = defaultdict(F)
    for i in range(6):
        t,b,c = decode(old[i],3)
        for j in range(6):
            s = old[j] >> 2
            e = decode(new[j],5)
            rel = 'same' if i == j else 'off'
            n = 6 if i == j else 30
            for l in range(5):
                ans['C-to-Y',l,rel] += F(c-e[l],n*(p+t+b+1))
            ans['Y5-to-C',rel] += (q(e[4],s+sum(e))-F(c,s+sum(e[:4])+1))/n
    return dict(ans)


def terminal_literal_coefficients(atom):
    """All rational coefficients after uniform S6, counted with integers."""
    old = [decode(w,3) for w in atom['old_words']]
    new = [decode(w,5) for w in atom['new_words']]
    p = sum(map(int,atom['actual'][:3]))
    counts = [[0]*7 for _ in range(216)]
    permutations_seen = 0
    for perm in permutations(range(6)):
        ow = [old[k] for k in perm]
        nw = [new[k] for k in perm]
        for i in range(6):
            t,b,c = ow[i]
            den = p+t+b+1
            for j in range(6):
                e = nw[j]
                base = (6*i+j)*5
                for role in range(5):
                    counts[base+role][den] += c-e[role]
                last = 180+6*j+i
                s = ow[j][0]
                if e[4]:
                    counts[last][s+sum(e)] += 1
                counts[last][s+sum(e[:4])+1] -= c
        permutations_seen += 1
    assert permutations_seen == 720
    result = [sum(F(row[d],720*d) for d in range(1,7)) for row in counts]
    orbits = interface_orbits(atom['actual'],atom['old_words'],atom['new_words'])
    for i in range(6):
        for j in range(6):
            rel = 'same' if i == j else 'off'
            for role in range(5):
                assert result[(6*i+j)*5+role] == orbits['C-to-Y',role,rel]
            assert result[180+6*j+i] == orbits['Y5-to-C',rel]
    return result


def root_literal_costs(actual, old, new, table):
    """Every root and every ordered distinct-root pair is evaluated literally."""
    a = tuple(map(int,actual))
    roots = [(w>>2,decode(v,5)) for w,v in zip(old,new)]
    d = sum(t for t,e in roots)
    ans = defaultdict(F)
    root = F(0)
    for j,(t,e) in enumerate(roots):
        z = sum(e)
        root += q(t,t+z)/6
        ans['gamma',] += (-2*q(z,t+z)+table[t,new[j],d-t])/6
        for k in range(5):
            v = q(e[k],t+z)
            den = t+sum(e[:k])+5-k
            ans['price',k] += F(e[k],6*(sum(a[:5])+1))
            ans['capacity',k] += F(e[k],6)
            for i in range(6):
                ans['floor-actual',k,i] += (F(a[i],den)-v)/6
            ans['floor-other-opt',k] += (F(d-t,den)-5*v)/6
            ans['floor-root',k] += (F(t,den)-v)/6
            for l in range(5):
                if l != k:
                    ans['floor-own-tail',k,l] += (F(e[l],den)-v)/6
                for i,(s,f) in enumerate(roots):
                    if i != j:
                        ans['cross-floor',k,l] += (F(f[l],den)-v)/6
            for i in range(5):
                ans['actual-floor',i,k] += F(e[k],6*(sum(a[:i])+6-i))
        p = t+sum(e[:3])
        tax = q(e[3]+e[4],t+z)+F(e[3],(p+1)*(p+2))
        ap = sum(a[:4])
        own = (t,)+e
        for qindex in range(6):
            for rindex in range(qindex,6):
                ans['actual-pair',qindex,rindex] += (
                    F(own[qindex]+own[rindex],ap+1)
                    -F(own[qindex]*own[rindex],(ap+1)*(ap+2)))/6
                for i,(s,f) in enumerate(roots):
                    if i != j:
                        donor = (s,)+f
                        ans['cross-pair',qindex,rindex] += (-tax
                            +F(donor[qindex]+donor[rindex],p+1)
                            -F(donor[qindex]*donor[rindex],(p+1)*(p+2)))/30
    assert len(ans) == 163
    return root,dict(ans)


def verify_fixed_marginal_bounds(snapshot, hist):
    bound = json.loads((HERE/'fixed_root_marginal_obstruction_exact.json').read_text())
    assert bound['point_sha256'] == PIN
    assert bound['old_root_certificate_sha256'] == sha(BASE/'cross_root_pricing/joint_completion_exact.json')
    roots = snapshot['new_root_certificate']['support']
    columns = []
    for index,h in hist.items():
        if not F(h['weight']):
            continue
        old = sorted([w for w,n in enumerate(h['hist']) for _ in range(n)],key=lambda w:(-int(w>=4),w))
        assert sum(w>=4 for w in old) == 1
        for j,r in enumerate(roots):
            if h['actual_bits'] != r['actual']:
                continue
            seen = set()
            for p in sorted(set(permutations(r['zero_words']))):
                new = [r['one_word'],*p]
                key = tuple(sorted(zip(old,new)))
                if key in seen:
                    continue
                seen.add(key)
                columns.append((index,j,interface_orbits(h['actual_bits'],old,new)))
    assert len(columns) == bound['incidence_orbits'] == 32
    for b in bound['bounds']:
        row = tuple(b['row'])
        dual = {tuple(v['margin']):F(v['value']) for v in b['dual_potentials']}
        gaps = []
        for i,j,coeff in columns:
            gap = -coeff[row]-dual['old-hist',i]-dual['root-atom',j]
            assert gap >= 0
            gaps.append(gap)
        assert list(map(str,gaps)) == b['all_32_column_dual_gaps']
        assert all(v == 0 for v in gaps) == b['is_exact_invariant']
        upper = -sum(F(h['weight'])*dual.get(('old-hist',i),F(0)) for i,h in hist.items())
        upper -= sum(F(r['mass'])*dual['root-atom',j] for j,r in enumerate(roots))
        assert upper == F(b['upper_bound']) < 0
    return len(bound['bounds'])


def main():
    started = time.monotonic()
    certpath = HERE/'joint_completion_exact.json'
    cert = json.loads(certpath.read_text())
    snapshotpath = HERE/'input_snapshot_exact.json'
    assert cert['point_sha256'] == PIN == sha(BASE/'peer_augmented_lp/augmented_lp_exact.json')
    assert cert['input_snapshot_sha256'] == sha(snapshotpath)
    snapshot = json.loads(snapshotpath.read_text())
    for source in snapshot['sources']:
        assert sha(BASE/source['path']) == source['sha256']
    raw = json.loads((BASE/'peer_augmented_lp/augmented_lp_exact.json').read_text())
    hist = {i:{'original_column_index':i,**h} for i,h in enumerate(raw['columns']) if h['kind']=='hist'}
    frozen = snapshot['projection_inputs']
    for source in frozen['sources']:
        assert sha(BASE/source['path']) == source['sha256']
    assert list(hist.values()) == frozen['original_hist_records']
    table = {}
    for t in (0,1):
        path = BASE/f'background_five_bridge/fixed53_b{t}_profit.json'
        rows = json.loads(path.read_text())['min_by_actual_and_d']
        for row in rows:
            table[t,int(row['actual'],2),row['d']] = F(row['min_rho'])
    assert table == {(r['t'],r['word'],r['comparison_count']):F(r['value']) for r in frozen['remainder_table']}
    cap = next(F(v['weight']) for v in raw['columns'] if v['kind']=='K')
    pay = [sum(F(h['weight'])*q(int(h['actual_bits'][i]),sum(map(int,h['actual_bits'])))
               for h in hist.values()) for i in range(6)]
    assert sum(pay) == F(raw['W']) == F(frozen['W'])
    assert cap == F(frozen['K']) and pay == list(map(F,frozen['u']))
    oldmarg = defaultdict(F)
    rootmarg = defaultdict(F)
    budgetcost = defaultdict(F)
    literal = [F(0)]*216
    sourcecost = F(0)
    candidate_roots = snapshot['new_root_certificate']['support']
    denom = 1
    for atom in cert['atoms']:
        m = F(atom['mass'])
        assert m > 0
        i,j = atom['original_column_index'],atom['joint_atom_index']
        h = hist[i]
        r = candidate_roots[j]
        assert atom['actual'] == h['actual_bits'] == r['actual']
        ow,nw = atom['old_words'],atom['new_words']
        assert len(ow) == len(nw) == 6
        assert [ow.count(w) for w in range(8)] == h['hist']
        assert 4 <= ow[0] < 8 and all(0 <= w < 4 for w in ow[1:])
        assert sum(w>>2 for w in ow) == h['d'] == r['d'] == 1
        assert nw[0] == r['one_word'] and sorted(nw[1:]) == r['zero_words']
        oldmarg[i] += m
        rootmarg[j] += m
        coefficients = terminal_literal_coefficients(atom)
        literal = [a+m*b for a,b in zip(literal,coefficients)]
        rc,bc = root_literal_costs(atom['actual'],ow,nw,table)
        sourcecost += m*rc
        for name,value in bc.items():
            budgetcost[name] += m*value
        denom = lcm(denom,(m/720).denominator)
    assert len(cert['atoms']) == cert['support_atoms'] == 17
    assert all(oldmarg[i] == F(h['weight']) for i,h in hist.items())
    assert all(rootmarg[x['original_root_state']] == F(x['mass']) for x in cert['new_root_state_margins'])
    assert sum(oldmarg.values()) == F(cert['total_mass']) == 1
    assert denom == int(cert['unit_customer_scale'])
    assert all((F(a['mass'])*denom/720).denominator == 1 for a in cert['atoms'])
    assert min(literal) >= 0
    saved = {tuple(r['row']):r for r in cert['budget_slacks']}
    budgets = {}
    for name,cost in budgetcost.items():
        typ = name[0]
        if typ == 'gamma':
            budget = -F(226487,10**21)*cap-F(5,6)*F(raw['O'])
        elif typ == 'price':
            budget = pay[5]
        elif typ == 'capacity':
            budget = cap
        elif typ == 'actual-floor':
            budget = pay[name[1]]
        elif typ == 'actual-pair':
            budget = pay[4]+pay[5]+sum(F(h['weight'])*F(int(h['actual_bits'][4]),
                (sum(map(int,h['actual_bits'][:4]))+1)*(sum(map(int,h['actual_bits'][:4]))+2)) for h in hist.values())
        else:
            budget = F(0)
        slack = budget-cost
        assert slack >= 0 and slack == F(saved[name]['slack']) and budget == F(saved[name]['budget'])
        budgets[name] = slack
    assert len(budgets) == 163
    sourcegap = pay[0]-sourcecost
    assert sourcegap > 0 and sourcegap == F(cert['root_slack']) == F(saved['root-source',]['slack'])
    assert sourcecost == F(cert['root_cost']) and pay[0] == F(cert['root_budget'])
    assert pay[0] == F(saved['root-source',]['budget'])
    queryreport = []
    for i in range(6):
        for j in range(6):
            rel = 'same' if i == j else 'off'
            for l in range(5):
                v = literal[(6*i+j)*5+l]
                assert v == F(saved['C-to-Y',l,rel]['slack'])
                assert F(saved['C-to-Y',l,rel]['budget']) == 0
                queryreport.append({'row':['C-to-Y',i,j,l], 'value':str(v)})
            v = literal[180+6*j+i]
            assert v == F(saved['Y5-to-C',rel]['slack'])
            assert F(saved['Y5-to-C',rel]['budget']) == 0
            queryreport.append({'row':['Y5-to-C',j,i], 'value':str(v)})
    assert len(queryreport) == 216 and len(saved) == len(cert['budget_slacks']) == 176
    restricted_bounds = verify_fixed_marginal_bounds(snapshot,hist)
    report = {'status':'INDEPENDENT STANDARD-LIBRARY COMMON-CUSTOMER AUDIT PASSED',
              'scope':'Finite old-C/new-root-tail projection only; no complete SPE or general half conclusion.',
              'point_sha256':PIN,'certificate_sha256':sha(certpath),
              'verifier_sha256':sha(Path(__file__)),
              'positive_orbit_atoms':len(cert['atoms']), 'simultaneous_permutations_per_atom':720,
              'literal_atoms_before_merging':720*len(cert['atoms']),
              'literal_query_coefficient_checks':216*len(cert['atoms']),
              'raw_permuted_query_evaluations':720*216*len(cert['atoms']),
              'old_hist_margins_checked':len(hist), 'old_budget_rows_checked':len(budgets),
              'terminal_queries_checked':len(queryreport),
              'terminal_queries_strict':sum(v > 0 for v in literal),
              'terminal_queries_zero':sum(v == 0 for v in literal),
              'terminal_queries_negative':sum(v < 0 for v in literal),
              'root_slack':str(sourcegap),'root_slack_float':float(sourcegap),
              'unit_customer_scale':str(denom),
              'fixed_old_root_margin_bounds_checked':restricted_bounds,
              'elapsed_seconds':time.monotonic()-started,
              'literal_terminal_values':queryreport}
    (HERE/'independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='literal_terminal_values'},indent=2))


if __name__ == '__main__':
    main()
