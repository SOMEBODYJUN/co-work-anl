"""Exact fixed-point comparisons between terminal rows and true third-node cuts."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
sys.path.insert(0, str(ROOT / "map/edges/customer-attraction-3a-3a-319e676fff137944"))
from check_crossed_terminal_rows import POINTS, read_frozen, decode, cross_row

F_TABLE = (
    (0, 960, 1220, 1480, 1740, 2000),
    (0, F(1665, 4), F(2745, 4), F(3785, 4), F(4825, 4), F(5865, 4)),
    (0, 320, 524, 728, 932, 1136),
)
LIFT_PATH = "five-full-actual-extension-primary/original/certificate/exact_full_actual_extension_known_v1.json"
LIFT_SHA = "8b28de8d89c76684bc95c3eb3f890e6f4ee4492cb152102281d125912e2a30e2"


def projected_atom(atom):
    return decode({key: value for key, value in atom.items() if key != "max_bits"})


def actual_p7(bits, d, max_bit_upper):
    a, b, c, _, _, _, _, w, _, _ = bits
    p = a+b
    actual_share = F(c, sum(bits[:5]) or 1)
    return 17040*actual_share + 1085*max_bit_upper - F(13395*w, p+3) - F_TABLE[p][d]


def actual_p13(bits, families, d, max_bit_upper, z4):
    a, b, c, _, _, _, _, _, x, y = bits
    p = a+b
    actual_share = F(c, sum(bits[:5]) or 1)
    ab_last, ae_last = (sum(row[2] for row in families[family]) for family in ("AB", "AE"))
    s1, s2, s3 = (sum(row[pos] for row in families["second"]) for pos in (1, 2, 3))
    candidates = []
    for h, q, r in product((0, 1), repeat=3):
        h_share, q_share, r_share = (F(bit, p+h+q+r or 1) for bit in (h, q, r))
        B2 = q_share + r_share + F(q, (p+h+1)*(p+h+2))

        def tax(alpha, beta, n, m):
            return (n*m*B2 - F(m*alpha+n*beta-2*alpha*beta, p+h+1)
                    - F(2*alpha*beta, p+h+2))

        candidates.append(
            8251*(actual_share-h_share)
            + F(4703*(h-q)+5446*(h-r), p+3)
            + 165*(5*r_share-F(d, p+h+q+1))
            + 307*(max_bit_upper-h)
            + 92*tax(x, y, 1, 1)
            + 66*tax(y, z4, 1, 1)
            + 2*tax(ab_last, d, 5, 5)
            + F(925*(5*h-ae_last), p+3)
            + 15*tax(s1, x, 5, 1)
            + 7*tax(s1, s2, 5, 5)
            + 17*tax(s1, s3, 5, 5)
            + 4*tax(s2, d, 5, 5)
        )
    return max(candidates)


def main():
    reports = {}
    for n, (point_path, point_sha, _, _, atom_count) in POINTS.items():
        point = read_frozen(point_path, point_sha)
        assert len(point["atoms"]) == atom_count
        p7 = F(0)
        p13 = F(0)
        for atom in point["atoms"]:
            bits, families, d, mass = decode(atom)
            root_safe_upper = 5*F(bits[0], sum(bits[:5]) or 1)
            p7 += mass*actual_p7(bits, d, root_safe_upper)
            p13 += mass*actual_p13(bits, families, d, root_safe_upper, 0)
        assert p7 < 0 and p13 < 0
        reports[n] = {"primal_sha256": point_sha, "atoms": atom_count,
                      "actual_P7_W_repeat_upper": str(p7), "actual_P13_upper": str(p13)}

    lift = read_frozen(LIFT_PATH, LIFT_SHA)
    assert len(lift["atoms"]) == lift["positive_projected_atoms"] == 64
    p7, p13, root_safe, terminal, w, o = [F(0) for _ in range(6)]
    for atom in lift["atoms"]:
        bits, families, d, mass = projected_atom(atom)
        z0, _, _, _, z4 = map(int, atom["max_bits"])
        p7 += mass*actual_p7(bits, d, z0)
        p13 += mass*actual_p13(bits, families, d, z0, z4)
        root_safe += mass*(5*F(bits[0], sum(bits[:5]) or 1)-z0)
        terminal += mass*cross_row(bits, families, "AB", "second", ((1, "O"),))
        w += mass*bool(any(bits[:5]))
        o += mass*bool(d)
    assert w == F(lift["welfare"]) == 1 and o == F(lift["comparison_cover"]) > 2
    assert p7 == F(lift["row_slacks"]["PFixed:actual:W"]) > 0
    assert p13 >= 0 and root_safe >= 0 and terminal < 0
    print(json.dumps({
        "terminal_points": reports,
        "7497_point": {
            "primal_sha256": LIFT_SHA,
            "projected_atoms": len(lift["atoms"]),
            "comparison_cover": str(o),
            "actual_P7_W_repeat": str(p7),
            "actual_P13": str(p13),
            "root_5u_minus_K": str(root_safe),
            "crossfinal:AB:Sbranch:1O": str(terminal),
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
