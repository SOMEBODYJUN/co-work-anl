"""Independent exact algebra audit; no equilibrium solver and no numerical LP."""
from fractions import Fraction as F
from pathlib import Path
import json


def main():
    checks = 0
    records = []
    for m in range(3, 101):
        for c in range(1,m+1):
            gap = (m-1)*(F(m,c)-1)-(m-c)
            assert gap == F((m-c)*(m-1-c), c)
            assert gap >= 0
            checks += 1
        coeff_from_B = (F(2,2*m-1) + F(m-2,m) + F(m-3,m*m)) / (m*(m-1)-1)
        explicit = F(2*m**3-m*m-5*m+3, m*m*(2*m-1)*(m*m-m-1))
        old = F(2,m*(2*m-1))
        diff = F(m*m-3*m+3,m*m*(2*m-1)*(m*m-m-1))
        assert coeff_from_B == explicit
        assert explicit-old == diff > 0
        if m <= 10:
            records.append({'m':m,'new_root_coefficient':str(explicit),
                            'old_root_coefficient':str(old),'difference':str(diff)})
    assert F(2,5)/5+F(1,3)/5 == F(11,75)
    assert F(2,5)/F(11,75) == F(30,11) < 3
    result = {'status':'exact algebra passed, author audit only',
              'customer_coefficient_checks':checks,'range':[3,100],
              'three_player_root_floor':'11/75',
              'three_player_integer_deficit_multiplier':'30/11',
              'root_coefficients':records}
    print(json.dumps(result,indent=2))
    Path(__file__).with_name('max_theme_branch_capacity_audit.json').write_text(
        json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
