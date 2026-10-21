"""Independent exact audit of the omitted same-index L2 versus L1 last-node row.

Only the frozen atom table is read.  The tested inequality is necessary for a
real common-catalog realization of its named nodes; no SPE claim is made.
"""
from fractions import Fraction
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'next_credible' / 'enhanced_2396_exact_obstruction.json'

def main():
    atoms = json.loads(SOURCE.read_text())['atom_masses']
    lhs = rhs = Fraction()
    for atom in atoms:
        bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
        # L_i^2 is played after ordered prefix (A,B,E,T_i).
        p = bits['A'] + bits['B'] + bits['E']
        ell2, h2 = atom['menus_lh'][2]
        ell1, h1 = atom['menus_lh'][1]
        mass = Fraction(atom['mass'])
        # Sum over i of 1{L_i^r}/(p+1{T_i}+1).
        lhs += mass * (Fraction(ell2, p+1) - Fraction(h2,(p+1)*(p+2)))
        rhs += mass * (Fraction(ell1, p+1) - Fraction(h1,(p+1)*(p+2)))
    result = {'scope': 'necessary diagonal common-catalog last-player row only',
              'node': '(A,B,E,T_i), prescribed action L_i^2',
              'comparison': 'L_i^1',
              'lhs_sum': str(lhs), 'rhs_sum': str(rhs),
              'slack_sum': str(lhs-rhs),
              'passes_necessary_inequality': lhs >= rhs}
    (HERE/'audit_diagonal_menu.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
