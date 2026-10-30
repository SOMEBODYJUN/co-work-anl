"""Definition-level Fraction audit of the written naive rent-reserve failure."""
from fractions import Fraction as F
from itertools import product


def harmonic(c):
    return sum((F(1, j) for j in range(1, c+1)), F(0))


def main():
    m = 9
    # Catalogue A=0={x,z}, B=1={x}; full strategy always chooses A.
    customers = [frozenset([0, 1]), frozenset([0])]
    def utility(path, action):
        return sum((F(1, sum(a in typ for a in path)) for typ in customers if action in typ), F(0))
    checks = 0
    for k in range(m):
        for h in product(range(2), repeat=k):
            actual = h+(0,)*(m-k)
            actual_u = utility(actual, 0)
            for alternative in range(2):
                branch = h+(alternative,)+(0,)*(m-k-1)
                assert actual_u >= utility(branch, alternative)
                checks += 1
    assert len({x for typ in customers for x in typ}) == 2
    values = []
    for h in range(m-2):
        # Direct total old-prefix utility, Ω universal to both customers.
        before = 2*F(h, h+1)
        after = F(h, h+3)+F(h, h+2)
        error = before-after
        assert error == 2*F(h, (h+1)*(h+3))+F(h, (h+1)*(h+2))
        values.append(error)
    total = sum(values, F(0))
    assert total == F(1879, 840) and total-2 == F(199, 840)
    for c in range(1, 101):
        direct = sum((2*F(h, (h+1)*(h+3))+F(h, (h+1)*(h+2)) for h in range(c)), F(0))
        closed = 3*harmonic(c)+F(5, c+1)+F(3, c+2)-F(13, 2)
        assert direct == closed
    print({'exact': True, 'full_history_comparisons': checks,
           'prefix_errors': len(values), 'sum': str(total), 'root_W': 2,
           'naive_budget_excess': str(total-2), 'closed_form_cases_checked': 100})


if __name__ == '__main__':
    main()
