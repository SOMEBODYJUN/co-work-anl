"""Independent Fraction reconstruction of omitted terminal menu comparisons.

Uses only the frozen JSON schema and explicit five indexed terminal prefixes;
does not import either five-player row generator or any solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
STATES = tuple(product((0,1),repeat=4))


def one_atom(atom):
    a = int(atom["bits"][0])
    indexed = [state for state,n in zip(STATES,atom["second_hist"]) for _ in range(n)]
    assert len(indexed) == 5
    # At last-player prefix (A,T_r,H_r,I_r), a candidate action with
    # membership z earns z/(a+t_r+h_r+i_r+z). We write zero without
    # evaluating any fraction, so the unused-action z=0 case is exact too.
    def terminal_payoff(r,z):
        return F(z,a+sum(indexed[r][:3])+z) if z else F(0)
    offdiag = sum((terminal_payoff(r,indexed[r][3])-terminal_payoff(r,indexed[s][2])
                   for r in range(5) for s in range(5) if r != s),F(0))
    diagonal = sum((terminal_payoff(r,indexed[r][3])-terminal_payoff(r,indexed[r][2])
                    for r in range(5)),F(0))
    allpairs = sum((terminal_payoff(r,indexed[r][3])-terminal_payoff(r,indexed[s][2])
                    for r in range(5) for s in range(5)),F(0))
    total_I = sum(state[2] for state in indexed)
    compressed = sum((F(n*(4*j+i-total_I),a+t+h+i+1)
                      for (t,h,i,j),n in zip(STATES,atom["second_hist"])),F(0))
    assert compressed == offdiag
    assert offdiag+diagonal == allpairs
    return offdiag,diagonal,allpairs


def main():
    primal = json.loads((ROOT/"evidence/certificates/customer_attraction/five_player_indexed_bound.json").read_text())["primal"]
    result = [F(0),F(0),F(0)]
    for atom in primal["atoms"]:
        mass = F(atom["mass_numerator"],primal["denominator"])
        for k,coefficient in enumerate(one_atom(atom)):
            result[k] += mass*coefficient
    offdiag,diagonal,allpairs = result
    assert offdiag < 0
    assert diagonal >= 0 and allpairs >= 0
    record = {"scope":"Universal valid new necessary row; excludes only this stored relaxed point, not an SPE counterexample",
              "atoms":len(primal["atoms"]),"terminal_comparisons_in_new_row":20,
              "offdiagonal_sum":str(offdiag),"offdiagonal_mean":str(offdiag/20),
              "diagonal_sum":str(diagonal),"all_25_sum":str(allpairs),
              "decomposition_verified_every_atom":True}
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record,indent=2))


if __name__ == "__main__":
    main()
