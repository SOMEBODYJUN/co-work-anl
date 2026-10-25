"""Exact algebra QA of the finite five-player terminal-menu envelope.

Not a finite game search or a verifier for HALF(5). The analytic proof is in
terminal_menu_envelope.md. This script checks every local integer type and
feasible pair of comparison/reply histogram margins, with exact fractions.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def main():
    breaks = {F(0), F(1)}
    for p in range(4):
        for d_bit in range(2):
            for d in range(6):
                breaks.add(F(d * (p+d_bit+1), 5*(p+1)*(p+2)))
    assert min(breaks) == 0 and max(breaks) == 1
    checked = 0
    minimum = None
    for alpha in sorted(breaks):
        for p in range(4):
            for d_bit in range(2):
                for e_bit in range(2):
                    total = p+d_bit+e_bit
                    a = F(d_bit,total) if total else F()
                    b = F(e_bit,total) if total else F()
                    L = (p+1)*(p+2)
                    for d in range(6):
                        for ell in range(6):
                            for cross in range(max(0,d+ell-5),min(d,ell)+1):
                                S = 5*a-F(d,p+1)+F(cross,L)
                                Z = 5*b-F(ell,p+d_bit+1)
                                V = F(d*ell-5*cross,L)
                                Q = S+alpha*Z+V/5
                                direct = 5*a+5*alpha*b-F(d,p+1)+ell*(F(d,5*L)-alpha/F(p+d_bit+1))
                                G = 5*a+5*alpha*b-F(d,p+1)+max(F(),F(d,L)-5*alpha/F(p+d_bit+1))
                                assert Q == direct
                                assert G >= Q
                                margin = G-Q
                                minimum = margin if minimum is None else min(minimum,margin)
                                checked += 1
    result = {
        'scope': __doc__,
        'alpha_breakpoints': list(map(str,sorted(breaks))),
        'exact_cases_checked': checked,
        'minimum_upper_envelope_margin': str(minimum),
        'all_identities_and_upper_bounds': True,
        'proves_half5': False,
    }
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
