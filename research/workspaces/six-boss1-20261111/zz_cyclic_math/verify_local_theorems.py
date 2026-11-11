"""Exhaustive exact bit checks and integer local-obstruction certificates."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    odd = [mask for mask in range(64) if mask.bit_count() % 2]
    cases = []
    for bits in product(range(2), repeat=6):
        r = bits[::2]
        z = bits[1::2]
        own = [int(r[i] != z[i]) for i in range(3)]
        cross = [int(r[i] != z[(i + 1) % 3]) for i in range(3)]
        s = sum(r[i] * (z[(i + 1) % 3] - z[i]) for i in range(3))
        assert 2 * s == sum(own) - sum(cross)
        assert (sum(own) + sum(cross)) % 2 == 0
        slacks = []
        for mask in odd:
            upper = (sum(own[i] for i in range(3) if not (mask >> i & 1))
                     - sum(cross[i] for i in range(3) if mask >> (3 + i) & 1)
                     + (mask.bit_count() - 1) // 2)
            slacks.append(upper - s)
            assert upper >= s
        assert s <= 1
        cases.append({'bits_r1z1r2z2r3z3': bits, 'S': s,
                      'odd_slacks': slacks, 'minimum_slack': min(slacks)})
    pair = []
    for r, z, R, Z in product(range(2), repeat=4):
        s = -(r - R) * (z - Z)
        b, c, d = (1-r)*z, r*(1-z), r*z
        B, C, D = (1-R)*Z, R*(1-Z), R*Z
        uppers = [b+c, B+C, b+B, c+C, b+c+d-D, B+C+D-d]
        assert min(uppers) == s
        pair.append({'bits_rzRZ': [r,z,R,Z], 'S': s, 'six_upper_values': uppers})
    # The five literal customers are D1,D2,D3,Q0,Q1.
    realizations = []
    for i, j in combinations(range(3), 2):
        orientations = [0,0,0]
        orientations[i] = 0
        orientations[j] = 1
        data = []
        for k in range(3):
            data.append([(int(e == k), int(e == k)) for e in range(3)])
        for q in range(2):
            zs = [(q + orientations[e]) % 2 for e in range(3)]
            data.append([(1-z,z) for z in zs])
        Lij = sum(F(x[i][1] - x[j][1], 1 + x[i][0]) for x in data)
        Lji = sum(F(x[j][1] - x[i][1], 1 + x[j][0]) for x in data)
        assert Lij == Lji == 0
        for e in range(3):
            assert sorted(data[k][e] for k in (3,4)) == [(0,1),(1,0)]
        realizations.append({'pair': [i+1,j+1], 'customers': data,
                             'Lij': str(Lij), 'Lji': str(Lji)})
    all_joint_Q = []
    for orientations in product(range(2), repeat=3):
        s_Q = 0
        for q in range(2):
            z = [(q + o) % 2 for o in orientations]
            s_Q += sum((1-z[i]) * z[(i+1) % 3] for i in range(3))
        full_cycle = F(-3 + s_Q, 2)
        assert full_cycle <= F(-1, 2)
        all_joint_Q.append({'Q_orientations': orientations,
                            'Q_cycle_sum': s_Q, 'full_IC_cycle': str(full_cycle)})
    out = {
        'scope': 'Exact finite local Boolean and marginal-obstruction checks; not full SPE',
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'three_node_bit_assignments': 64,
        'odd_subsets_per_assignment': 32,
        'odd_subset_pointwise_checks': 64*32,
        'odd_masks_own_then_cross': odd,
        'all_three_node_checks_pass': True,
        'three_node_cases': cases,
        'two_node_cases': pair,
        'two_block_free_only_obstruction': {
            'P': 0,
            'blocks': [
                {'H': 1, 'e_00_01_10_11': [0,0,0,1], 'f_00_01_10_11': [1,0,0,0]},
                {'H': 4, 'e_00_01_10_11': [2,0,0,2], 'f_00_01_10_11': [0,2,2,0]}],
            'free_Lef_upper': '1/2', 'free_Lfe_upper': '0',
            'exact_cycle_upper': '-1/2'},
        'three_node_pair_realizations': realizations,
        'all_eight_three_node_Q_realizations': all_joint_Q,
        'three_node_maximum_cycle_IC': '-1/2',
    }
    dest = HERE/'local-theorem-exact-verification.json'
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in (
        'three_node_cases','two_node_cases','three_node_pair_realizations',
        'all_eight_three_node_Q_realizations')},ensure_ascii=False))


if __name__ == '__main__':
    main()
