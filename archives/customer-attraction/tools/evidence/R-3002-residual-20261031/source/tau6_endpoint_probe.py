"""Test explicit tau=6 endpoint/floor certificate templates.

An infeasible multiplier LP or a Farkas witness is not a game/SPE counterexample.
The row family and complete type domain are fixed here, not inferred from prose.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TAU = F(6)
MODE = 'literal128'

def literal_matrix():
    labels = ['fractional-F:' + str(i+1) for i in range(6)]
    labels += [f'actual-safe:{i+1}:theme-{j+1}' for i in range(6) for j in range(6)]
    labels += ['fractional-endpoint-R', 'averaged-strong-PAIR']
    cols, rows = [], []
    for actual in range(64):
        bits = [(actual >> i) & 1 for i in range(6)]
        count = sum(bits)
        u = [F(b, count) if count else F() for b in bits]
        prior = [sum(bits[:i]) for i in range(6)]
        p = prior[4]
        for o in (0, 1):
            values = [TAU*u[i] - F(o, prior[i]+6-i) for i in range(6)]
            values += [u[i]-F(bits[j], prior[i]+6-i) for i in range(6) for j in range(6)]
            values += [TAU*u[4]+u[5]/2-F(o, p+1)+F(o*bits[4]*int(p == 0), 4)]
            values += [u[4]+u[5]+F(bits[4], (p+1)*(p+2))
                       -o*(F(2, TAU*(p+1))-F(1, TAU*TAU*(p+1)*(p+2)))]
            cols.append((o, actual, F(int(count > 0))-F(o, 2), []))
            rows.append(values)
    return cols, labels, rows


matrix = literal_matrix

def verify(data):
    cols, labels, rows = matrix()
    assert data['row_names'] == labels
    assert len({v['column'] for v in data['support']}) == len(data['support'])
    y = [F()] * len(cols)
    for atom in data['support']:
        j = atom['column']
        assert [cols[j][0], cols[j][1]] == [atom['comparison_bit'], atom['actual_membership']]
        y[j] = F(atom['weight'])
    assert min(y) >= 0 and sum(y) == 1
    expectations = [sum((weight*row[i] for weight, row in zip(y, rows)), F())
                    for i in range(len(labels))]
    target = sum((weight*col[2] for weight, col in zip(y, cols)), F())
    assert min(expectations) >= 0 and target < 0
    return dict(template=MODE,
                tau=str(TAU), columns=len(cols), rows=len(labels),
                support=sum(v > 0 for v in y), minimum_row_average=str(min(expectations)),
                target_average=str(target),
                status='exact Farkas obstruction for listed template; not an SPE counterexample')


def main():
    path = HERE / 'tau6_endpoint_farkas.json'
    if '--verify' in sys.argv:
        print(json.dumps(verify(json.loads(path.read_text())), indent=2))
        return
    import numpy as np
    from scipy.optimize import linprog
    cols, labels, rows = matrix()
    a = np.array(rows, dtype=float).T
    target = np.array([float(c[2]) for c in cols])
    multiplier = linprog(np.zeros(len(labels)), A_ub=a.T, b_ub=target,
                         bounds=(0, None), method='highs')
    print('multiplier LP:', multiplier.message, flush=True)
    result = linprog(target, A_ub=-a, b_ub=np.zeros(len(labels)),
                     A_eq=np.ones((1, len(cols))), b_eq=[1],
                     bounds=(0, None), method='highs')
    assert result.success and result.fun < -1e-8
    support = np.flatnonzero(result.x > 1e-8).tolist()
    active = np.flatnonzero(abs(a @ result.x) < 1e-8).tolist()
    eq = [[rows[j][i] for j in support]
          for i in active]
    eq.append([F(1)] * len(support))
    rhs = [F()] * len(active) + [F(1)]
    system = [row + [value] for row, value in zip(eq, rhs)]
    pivot = 0
    for col in range(len(support)):
        selected = next((i for i in range(pivot, len(system)) if system[i][col]), None)
        assert selected is not None
        system[pivot], system[selected] = system[selected], system[pivot]
        divisor = system[pivot][col]
        system[pivot] = [v/divisor for v in system[pivot]]
        for i in range(len(system)):
            if i != pivot and system[i][col]:
                factor = system[i][col]
                system[i] = [a-factor*b for a, b in zip(system[i], system[pivot])]
        pivot += 1
    assert all(all(v == 0 for v in row) for row in system[pivot:])
    solution = [system[j][-1] for j in range(pivot)]
    data = dict(scope='tau6 literal128: six fractional floors, 36 actual-source safe quotes, endpoint R and averaged strongPAIR; no claimed full-SPE equivalence',
                template=MODE, tau='6', row_names=labels,
                support=[dict(column=j, comparison_bit=cols[j][0], actual_membership=cols[j][1],
                              weight=str(v))
                         for j, v in zip(support, solution)])
    data['verification'] = verify(data)
    path.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data['verification'], indent=2))


if __name__ == '__main__':
    main()
