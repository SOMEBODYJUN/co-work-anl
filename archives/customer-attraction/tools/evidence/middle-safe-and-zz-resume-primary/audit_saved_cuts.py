"""New exact audit of the two saved source3 cuts, without author row code.

Read only the frozen point and parameter JSON. Reports are new events, not
replacement historical outputs. Invoke with the evidence directory as argv[1].
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


def part(n, d):
    return F(n, d) if n else F()


def primitive(a, member, query, hidden, parameters):
    b = sum(a[:2])
    denominator = b + member + sum(hidden)
    value = part(member, denominator)
    lookup = dict(zip(['Ti', 'Bi', 'Ci', 'Yj', 'R'] +
                      ['A'+str(i+1) for i in range(6)], query))
    for item in parameters:
        pos = item['tail_position'] - 1
        w = F(item['weight'])
        assert 0 <= pos < 3 and 0 <= w <= 32
        if item['kind'] == 'capacity':
            coefficient = F(hidden[pos])
        elif item['kind'] == 'price':
            i = item['query']
            assert 1 <= i <= 6
            coefficient = part(hidden[pos], sum(a[:i-1]) + 7-i)
        else:
            assert item['kind'] == 'safe'
            coefficient = (-part(hidden[pos], denominator) +
                           part(lookup[item['query']],
                                b+member+sum(hidden[:pos])+3-pos))
        value += w * coefficient
    return value


def main(base):
    original = base/'original/research/workspaces/customer-attraction/R-68a6ffab8681474aa2228b770a56e263'
    point = base/'dependencies/research/workspaces/customer-attraction/R-a241704002304c95bca9ef95d516b61f/solo_six/source_requery_exact.json'
    cuts_path = original/'attack/source_middle/cut_source3_B-off.json'
    data, cuts = json.loads(point.read_text()), json.loads(cuts_path.read_text())
    words_order = list(product((0, 1), repeat=3))
    payoffs = [F() for _ in range(6)]
    configurations = defaultdict(F)
    literal_terms = []
    for atom_index, atom in enumerate(data['atoms']):
        index = atom['hist_index']
        h = data['histograms'][index]
        a = tuple(map(int, h['actual_bits']))
        mass = F(atom['weight'])
        assert mass >= 0
        words = [w for w, count in zip(words_order, h['hist'])
                 for _ in range(count)]
        assert len(words) == 6
        groups = {(g[0], g[1], tuple(g[2]), tuple(g[3])): i
                  for i, g in enumerate(data['groups'][index])}
        assert len(groups) == len(data['groups'][index])
        for i in range(6):
            payoffs[i] += mass*part(a[i], sum(a))
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            member = atom['R'][groups[0, 0, words[i], words[j]]]
            query = (*words[i], words[j][1], member, *a)
            configurations[a, member, query] += mass
            literal_terms.append((atom_index, i, j, a, member, query, mass))
    records = {}
    for mode, cut in cuts.items():
        assert cut['source'] == 3 and cut['family'] == 'B-off'
        assert F(cut['lambda_source']) == 1 and cut['parameter_bound'] == 32
        assert len(configurations) == cut['configurations'] == 44
        parameters = cut['parameters']
        cost = 30*payoffs[2]
        for item in parameters:
            if item['kind'] == 'capacity':
                cost += 30*F(data['K'])*F(item['weight'])
            elif item['kind'] == 'price':
                cost += 30*payoffs[item['query']-1]*F(item['weight'])
        rhs = F()
        expanded = []
        for atom, i, j, a, member, query, mass in literal_terms:
            values = [primitive(a, member, query, y, parameters)
                      for y in words_order]
            lowest = min(values)
            rhs += mass*lowest
            expanded.append({'atom': atom, 'i': i, 'j': j,
                             'values': list(map(str, values)),
                             'mass': str(mass), 'minimum': str(lowest)})
        assert cost == F(cut['lhs'])
        assert rhs == F(cut['rhs'])
        assert cost-rhs == F(cut['slack']) < 0
        records[mode] = {'lhs': str(cost), 'rhs': str(rhs),
                         'slack': str(cost-rhs), 'terms': expanded}
    # Full local identity, including zero numerator / zero load boundary.
    identity_checks = 0
    for a in product((0, 1), repeat=6):
        b, ell = sum(a[:2]), sum(a[:5])
        for t, ti, ci, yj in product((0, 1), repeat=4):
            query = (ti, 0, ci, yj, t, *a)
            for p, q, z in words_order:
                d = b+t+p+q+z
                explicit = (part(285*t, d)+5*p+15*part(p, ell+1)+q+
                            part(96*q+120*z, b+4)-part(15*q+30*z, d)+
                            part(15*ci, b+t+p+2)+part(10*(ti+ci+yj), b+t+p+q+1))
                assert 285*primitive(a, t, query, (p,q,z),
                                     cuts['with_middle']['parameters']) == explicit
                identity_checks += 1
    zz_checks = 0
    for a in range(7):
        for re, ze, zf in product((0,1), repeat=3):
            assert F(ze-zf, a+re+1) == (F(ze-zf,a+1) -
                    F(re*ze,(a+1)*(a+2))+F(re*zf,(a+1)*(a+2)))
            zz_checks += 1
    # The historical J=2 example checks equality of implementations; it does
    # not establish a *strict* orbit-constant gap. Keep these claims separate.
    def four_bit_value(bits, edge):
        r0,z0,r1,z1 = bits
        return int(r0 != z0)+int(r1 != z1)+edge*(r0*r1+z0*z1)
    orbit_checks = {str(j): {'all_bits_max': max(four_bit_value(b,j)
                        for b in product((0,1),repeat=4)),
                        'fully_constant_max':max(four_bit_value((v,)*4,j)
                        for v in (0,1))} for j in (1,2)}
    report = {'status':'PASS','event':'new exact data/parameter audit',
              'point_sha256': hashlib.sha256(point.read_bytes()).hexdigest(),
              'cut_sha256': hashlib.sha256(cuts_path.read_bytes()).hexdigest(),
              'point_reported_rows':data['rows'], 'atoms':len(data['atoms']),
              'literal_terms':len(literal_terms),'configurations':len(configurations),
              'integer_formula_checks':identity_checks,'zz_identity_checks':zz_checks,
              'payoffs':list(map(str,payoffs)), 'cuts':records,
              'four_bit_example_check':orbit_checks,
              'scope':'exact saved-cut evaluation and local identities; no LP optimality, SPE realization, or half proof'}
    (base/'saved-cuts-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cuts'},indent=2))


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve())
