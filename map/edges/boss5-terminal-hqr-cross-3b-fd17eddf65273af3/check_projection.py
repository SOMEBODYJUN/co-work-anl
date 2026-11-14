"""Check the frozen terminal/HQR comparison without running any original CLI."""

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "archives/customer-attraction/tools/evidence"
WORKSPACE = ROOT / "research/workspaces/map-v2/Boss5/terminal-hqr-follow-up"
sys.path.insert(0, str(WORKSPACE))
import check_terminal_hqr_followup as saved


P13_DIRECTORY = EVIDENCE / (
    "actual13-and-joint-lift-audits-primary/original/research/workspaces/"
    "customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate"
)
AUDIT_DIRECTORY = EVIDENCE / (
    "round5-load-audits-resumed-boss2/final-717-original-run/tree/research/workspaces/"
    "customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_parent"
)
TERMINAL_FIELDS = ("bits", "AB_hist", "AE_hist", "second_hist", "menus_lh")
MAX_FIELDS = (*TERMINAL_FIELDS, "max_bits")
TARGET = "crossfinal:AB:Sbranch:1O"
P13_WEIGHTS = (8251, 4703, 5446, 165, 307, 92, 66, 2, 925, 15, 7, 17, 4)
FROZEN = json.loads((WORKSPACE / "terminal-hqr-follow-up-exact.json").read_text())


def load_functions(name, path):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def project(atoms, fields):
    grouped = defaultdict(F)
    for atom in atoms:
        key = json.dumps([atom[field] for field in fields], separators=(",", ":"))
        mass = F(atom["exact_mass"])
        assert mass > 0
        grouped[key] += mass
    return grouped


def terminal_atom(key, mass):
    return dict(zip(TERMINAL_FIELDS, json.loads(key)), exact_mass=str(mass))


def sorted_single_o(bits, families):
    ab, target = families["AB"], families["second"]
    inverses = [F(1, bits[0] + bits[1] + t + r + 1) for t, r, _ in ab]
    target_size = sum(row[1] for row in target)
    outside = sum(inverse * (4 * row[-1] - target_size)
                  for row, inverse in zip(ab, inverses))
    return outside + sum(
        sum(inverse * member for inverse, member in zip(
            sorted(v for row, v in zip(ab, inverses) if row[0] == t),
            sorted(row[1] for row in target if row[0] == t),
        )) for t in (0, 1)
    )


def check_lift_rows(lift, p13):
    row_totals = defaultdict(F)
    root_ic = F(0)
    weighted_max = F(0)
    for atom in lift["actual_HQR_lift"]:
        ctx = p13.context(atom)
        assert len(atom["max_bits"]) == 5 and set(atom["max_bits"]) <= {"0", "1"}
        state = tuple(map(int, atom["actual_HQR_bits"]))
        assert state in p13.STATES
        blocks = p13.raw_blocks(ctx, state)
        mass = F(atom["exact_mass"])
        for block in blocks:
            for row, value in block.items():
                row_totals[f"actual-extension:{row}"] += mass * value
        weights = dict(zip((row for block in blocks for row in block), P13_WEIGHTS))
        weighted_max += mass * max(p13.conditioned(ctx, hidden, weights) for hidden in p13.STATES)
        bits = tuple(map(int, atom["bits"]))
        max_bits = tuple(map(int, atom["max_bits"]))
        root_ic += mass * (F(bits[0], sum(bits[:5]) or 1) - F(max_bits[0], sum(max_bits) or 1))
    assert len(row_totals) == 13
    assert all(value == F(lift["row_slacks"][row]) >= 0 for row, value in row_totals.items())
    assert root_ic == F(lift["row_slacks"]["max:root:IC"]) >= 0
    assert weighted_max == F(FROZEN["7497_point"]["actual_P13"]) >= sum(
        weight * value for weight, value in zip(P13_WEIGHTS, row_totals.values())
    ) >= 0
    return {
        "root_ic": str(root_ic),
        "p13_shared_row_slacks": {row: str(value) for row, value in row_totals.items()},
    }


def check_terminal_bounds(terminal, p13):
    reports = {}
    for n, point in terminal.items():
        p7_upper = p13_upper = w = o = F(0)
        assert len(point["atoms"]) == FROZEN["terminal_points"][n]["atoms"]
        assert len(point["slacks"]) == int(n)
        assert all(F(value) >= 0 for value in point["slacks"].values())
        for atom in point["atoms"]:
            bits, _, d, mass = saved.decode(atom)
            root_upper = 5 * F(bits[0], sum(bits[:5]) or 1)
            p7_upper += mass * saved.actual_p7(bits, d, root_upper)
            ctx = p13.context(dict(atom, max_bits="00000"))
            blocks = p13.raw_blocks(ctx, (0, 0, 0))
            weights = dict(zip((row for block in blocks for row in block), P13_WEIGHTS))
            p13_upper += mass * (max(p13.conditioned(ctx, hidden, weights) for hidden in p13.STATES)
                                 + 307 * root_upper)
            w += mass * any(bits[:5])
            o += mass * (d > 0)
        assert w == F(point["welfare"]) == 1 and o == F(point["comparison_cover"]) > 2
        expected = FROZEN["terminal_points"][n]
        assert p7_upper == F(expected["actual_P7_W_repeat_upper"]) < 0
        assert p13_upper == F(expected["actual_P13_upper"]) < 0
        reports[n] = {"actual_P7_W_repeat_upper": str(p7_upper), "actual_P13_upper": str(p13_upper)}
    return reports


def check_terminal_projection(lift, terminal, audit):
    atoms = lift["atoms"]
    assert len(atoms) == len(project(atoms, MAX_FIELDS)) == 64
    assert project(lift["actual_HQR_lift"], MAX_FIELDS) == project(atoms, MAX_FIELDS)
    projected = project(atoms, TERMINAL_FIELDS)
    assert len(projected) == 52
    old_names = list(terminal["717"]["slacks"])
    assert old_names == list(lift["row_slacks"])[:717]
    assert all(TARGET in terminal[n]["slacks"] for n in ("727", "728", "737"))
    assert TARGET not in lift["row_slacks"]
    evaluate = audit.prior.old_evaluator()
    totals = defaultdict(F)
    terminal_row = w = o = F(0)
    for key, mass in projected.items():
        atom = terminal_atom(key, mass)
        bits, families, d, _ = saved.decode(atom)
        hs = [atom[field] for field in ("AB_hist", "AE_hist", "second_hist")]
        rows = evaluate(bits, hs, atom["menus_lh"], True)
        rows.update(audit.prior.literal_added(atom))
        rows.update(audit.literal_cross(atom))
        assert set(rows) == set(old_names)
        for row, value in rows.items():
            totals[row] += mass * value
        literal = saved.cross_row(bits, families, "AB", "second", ((1, "O"),))
        assert literal == sorted_single_o(bits, families)
        terminal_row += mass * literal
        w += mass * any(bits[:5])
        o += mass * (d > 0)
    assert all(totals[row] == F(lift["row_slacks"][row]) >= 0 for row in old_names)
    assert terminal_row == F(FROZEN["7497_point"][TARGET]) < 0
    assert w == F(lift["welfare"]) == 1 and o == F(lift["comparison_cover"]) > 2
    return {
        "projected_atoms_without_max_bits": len(projected),
        "reconstructed_717_coefficients": len(totals) * len(projected),
        "matching_717_row_slacks": len(totals),
        "zero_717_row_slacks": sum(not value for value in totals.values()),
        "welfare": str(w),
        "comparison_cover": str(o),
        TARGET: str(terminal_row),
    }


def main():
    terminal = {n: saved.read_frozen(path, fingerprint)
                for n, (path, fingerprint, *_) in saved.POINTS.items()}
    lift = saved.read_frozen(saved.LIFT_PATH, saved.LIFT_SHA)
    assert len(lift["actual_HQR_lift"]) == 85
    assert sum(F(value) < 0 for value in lift["row_slacks"].values()) == 0
    p13_path = P13_DIRECTORY / "actual13_projection.py"
    p13 = load_functions("actual13_functions", p13_path)
    audit_path = AUDIT_DIRECTORY / "audit_cross_primal.py"
    audit = load_functions("literal_717_audit_functions", audit_path)
    output = {
        "fixed_7497_sha256": saved.LIFT_SHA,
        "helper_sha256": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in (p13_path, audit_path, Path(audit.prior.__file__),
                         audit.prior.ROOT / "tests/audits/customer_attraction_five_indexed.py")
        },
        "terminal_bounds": check_terminal_bounds(terminal, p13),
        "projection": check_terminal_projection(lift, terminal, audit),
        "actual_HQR_support": check_lift_rows(lift, p13),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
