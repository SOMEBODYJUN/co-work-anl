#!/usr/bin/env python3
"""Independent source31-family proof/certificate audit; no optimization.

Minima are rebuilt from literal source and terminal customer shares, not the
Main closed-form generator. Row costs use those minima and explicit index
averages. No Main/builder/old-audit program is imported or executed.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
SRC = WS/'main_all_source31_family'
FAMILY_SHA = '0268bef0a826fc1872f9b7ec7fa5d0433b1730b8670d69098a9d2c8edb5dedfd'
V4_INPUT_SHA = 'b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5'
V4_CERT_SHA = '290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(bit, other_coverers):
    assert bit in (0, 1) and other_coverers >= 0
    return F(1, other_coverers+1) if bit else F(0)


def hidden_cost(p, t, q, tail):
    """31 forced-source payoff + caps - true terminal payoff + terminal query."""
    assert len(tail) >= 1
    return (31*share(t, p+sum(tail)) + sum(tail)
            - share(tail[-1], p+t+sum(tail[:-1]))
            + share(q, p+t+sum(tail[:-1])))


def main():
    fp = SRC/'exact_family.json'
    assert digest(fp) == FAMILY_SHA
    family = json.loads(fp.read_text())
    state_data = json.loads((SRC/'literal_states.json').read_text())
    menu_data = json.loads((SRC/'menu_checks.json').read_text())
    observed_states = {(r['i'],r['p'],r['t'],r['q'],tuple(r['tails'])):r for r in state_data}
    observed_min = {(r['i'],r['p'],r['t'],r['q']):F(r['minimum']) for r in family['all_minima']}
    observed_menu = {(r['i'],r['p'],tuple(r['menu'])):F(r['mean_mean30_residual']) for r in menu_data}
    assert len(observed_states) == len(state_data) == 456
    assert len(observed_min) == 60 and len(observed_menu) == 960
    minima = {}
    positive_hidden_residuals = zero_hidden_residuals = 0
    state_checks = 0
    for i in range(1,6):
        n = 6-i
        for p in range(i):
            assert p+n <= 5
            for t,q in product((0,1),repeat=2):
                values = {tail:hidden_cost(p,t,q,tail) for tail in product((0,1),repeat=n)}
                minimum = min(values.values())
                minima[i,p,t,q] = minimum
                assert minimum == observed_min[i,p,t,q]
                # The analytic target is checked only AFTER literal minimization.
                closed = n*t + F(30*t,p+n+1) + F(q,p+1+n*t)
                assert minimum == closed
                attaining_tail = (t,)*n
                assert values[attaining_tail] == minimum
                for tail,value in values.items():
                    stored = observed_states[i,p,t,q,tail]
                    residual = value-minimum
                    assert value == F(stored['cost'])
                    assert residual == F(stored['residual']) and residual >= 0
                    positive_hidden_residuals += residual > 0
                    zero_hidden_residuals += residual == 0
                    state_checks += 1
    assert state_checks == 456

    def menu_cost(i,p,T,Q,legal,o):
        """Literal averages of exact minima at the one-covered-index endpoint."""
        single = (o,0,0,0,0,0)
        if T != 8 and Q != 8:
            return minima[i,p,legal[T-1],legal[Q-1]]
        if T == 8 and Q != 8:
            return sum((minima[i,p,t,legal[Q-1]] for t in single),F(0))/6
        if T != 8 and Q == 8:
            return sum((minima[i,p,legal[T-1],q] for q in single),F(0))/6
        return sum((minima[i,p,single[k],single[l]]
                    for k in range(6) for l in range(6) if k != l),F(0))/30

    mixed_checks = mean30_checks = 0
    for i in range(1,6):
        n = 6-i
        for p in range(i):
            A = F(n)+F(30,p+n+1)
            B = F(1,p+1)
            C = F(n,(p+1)*(p+n+1))
            assert B-C > 0 and A-C > 0
            for t,q in product((0,1),repeat=2):
                assert minima[i,p,t,q] == A*t+B*q-C*t*q
            for menu in product((0,1),repeat=6):
                d = sum(menu); o = int(d > 0)
                endpoint = (o,0,0,0,0,0)
                for pure in (0,1):
                    literal_T = sum((minima[i,p,t,pure] for t in menu),F(0))/6
                    literal_Q = sum((minima[i,p,pure,q] for q in menu),F(0))/6
                    weak_T = sum((minima[i,p,t,pure] for t in endpoint),F(0))/6
                    weak_Q = sum((minima[i,p,pure,q] for q in endpoint),F(0))/6
                    assert literal_T == B*pure+F(d,6)*(A-C*pure) >= weak_T
                    assert literal_Q == A*pure+F(d,6)*(B-C*pure) >= weak_Q
                    mixed_checks += 2
                literal = sum((minima[i,p,menu[k],menu[l]]
                               for k in range(6) for l in range(6) if k != l),F(0))/30
                weak = sum((minima[i,p,endpoint[k],endpoint[l]]
                            for k in range(6) for l in range(6) if k != l),F(0))/30
                assert literal == F(d,6)*(A+B)-F(d*(d-1),30)*C
                assert weak == F(o,6)*(A+B)
                assert literal >= weak
                assert literal-weak == observed_menu[i,p,menu]
                if d:
                    assert literal-F(1,6)*(A+B) == F(d-1,30)*(5*(A+B)-C*d)
                mean30_checks += 1
    assert mean30_checks == 960 and mixed_checks == 3840

    inp_path = WS/'universal_union_wallet_v4/exact_input.json'
    cert_path = WS/'universal_union_wallet_v4/exact_certificate.json'
    assert digest(inp_path) == V4_INPUT_SHA and digest(cert_path) == V4_CERT_SHA
    old_input = json.loads(inp_path.read_text())
    cert = json.loads(cert_path.read_text())
    atoms = list(product((0,1),repeat=8))
    assert len(old_input['atom_columns']) == 256 and old_input['K_column'] == 256
    for index,bits in enumerate(atoms):
        assert old_input['atom_columns'][index] == {
            'index':index,'a':list(bits[:6]),'x':bits[6],'o':bits[7]}
    rows = family['rows']
    assert len(rows) == 320 and family['optimizer_calls'] == 0
    row_keys = [(r['source'],r['T'],r['Q']) for r in rows]
    assert row_keys == list(product(range(1,6),range(1,9),range(1,9)))
    rebuilt = {}
    coeff_checks = 0
    for row in rows:
        i,T,Q = row['source'],row['T'],row['Q']
        assert row['name'] == 'PORTFOLIO31_i%d_T%d_Q%d'%(i,T,Q)
        assert row['family'] == 'ALL_SOURCE_PORTFOLIO31'
        assert F(row['rhs']) == 0 and F(row['numerical_divisor']) == 31
        assert row['menu_mean_mean_rule'] == ('30 ordered distinct indices' if T == Q == 8 else None)
        assert set(row['a']) == {str(j) for j in range(257)}
        coeff = []
        for index,bits in enumerate(atoms):
            a = bits[:6]; x,o = bits[6:]; p = sum(a[:i-1])
            actual_u = share(a[i-1],sum(a)-a[i-1])
            minimum_cost = menu_cost(i,p,T,Q,a+(x,),o)
            value = 31*actual_u-minimum_cost
            assert value == F(row['a'][str(index)]),(row['name'],index,value)
            coeff.append(value); coeff_checks += 1
        assert F(row['a']['256']) == 6-i
        coeff.append(F(6-i)); coeff_checks += 1
        rebuilt[row['name']] = coeff
    assert coeff_checks == 82240
    known_path = WS/'main_thirty_index_strengthening/SOURCE2_MAXSIZE_31.json'
    known = json.loads(known_path.read_text())
    assert rebuilt['PORTFOLIO31_i2_T6_Q7'] == [F(known['a'][str(j)]) for j in range(257)]

    # Only evaluation of the explicitly supplied v4 vector, not a solver/face audit.
    point = [F(cert['primal'].get(str(j),'0')) for j in range(257)]
    assert all(x >= 0 for x in point)
    assert sum((point[h]*bits[7] for h,bits in enumerate(atoms)),F(0)) == 1
    welfare = sum((point[h] for h,bits in enumerate(atoms) if any(bits[:6])),F(0))
    assert welfare == F(cert['objective'])
    reported = {r['name']:F(r['value']) for r in family['v4_evaluations']}
    assert len(reported) == 320
    evaluations = {}
    for name,coeff in rebuilt.items():
        val = sum((c*x for c,x in zip(coeff,point)),F(0))
        assert val == reported[name]
        evaluations[name] = val
    negative = sorted((value,name) for name,value in evaluations.items() if value < 0)
    assert len(negative) == family['negative_v4_rows'] == 15
    assert negative[0] == (
        F('-104997578333106831070437069794935859/899229760032273191421693253016184735'),
        'PORTFOLIO31_i2_T5_Q6')
    paths = [fp,SRC/'literal_states.json',SRC/'menu_checks.json',SRC/'build_exact.py',SRC/'proof.md',
             inp_path,cert_path,known_path,
             REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
             REPO/'archives/customer-attraction/state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md']
    result = {
        'status':'PASS_INDEPENDENT_SOURCE31_ALL_FIVE_SOURCES_FULL_320x257',
        'family_sha256':FAMILY_SHA,'optimizer_calls':0,
        'Main_or_builder_code_executed_or_imported':False,
        'literal_hidden_states':state_checks,'exact_minima':len(minima),
        'hidden_residuals_positive':positive_hidden_residuals,
        'hidden_residuals_zero':zero_hidden_residuals,
        'literal_mean_mean30_menu_cases':mean30_checks,
        'literal_mixed_menu_cases':mixed_checks,
        'rows':320,'columns_per_row':257,'exact_coefficient_checks':coeff_checks,
        'raw_row_family_counts':{'pure_pure':245,'pure_mean':35,'mean_pure':35,'mean_mean30':5},
        'known_source2_A6_X_duplicate_columns_checked':257,
        'v4_point_rows_evaluated':320,'negative_v4_rows':len(negative),
        'worst_v4':{'name':negative[0][1],'exact_value':str(negative[0][0])},
        'negative_v4_row_values':[{'name':name,'value':str(value)} for value,name in negative],
        'source_scope':'Any genuine source i=1..5 in six-player complete ordered-history pure SPE, its own payoff, true n=6-i successors, actual catalog size maximum K, arbitrary legal T/Q and any six legal query labels; actual rows use actual u_i.',
        'X_maximality_needed_for_this_family':False,
        'OPT_menu_optimality_needed_for_this_family':False,
        'partition_or_label_distinctness_assumed':False,
        'all256_including_o0_and_allzero_retained':True,
        'source_sha256':{str(p.relative_to(REPO)):digest(p) for p in paths},
        'outstanding_errors':[],
        'not_claimed':['whole v4 optimum-face exclusion','full v4 primal/dual re-audit',
                       'next global LP optimum','complete SPE realization',
                       'half theorem or best-known welfare bound'],
    }
    (HERE/'audit_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','literal_hidden_states','exact_minima',
                     'literal_mean_mean30_menu_cases','literal_mixed_menu_cases','rows',
                     'columns_per_row','exact_coefficient_checks','negative_v4_rows',
                     'worst_v4','outstanding_errors')},indent=2))


if __name__ == '__main__':
    main()
