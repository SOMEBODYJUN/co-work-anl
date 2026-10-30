"""Replay original constructors and three frozen five-site audit cases.

This driver is new. Its constructor modules and five-site audit module are
unchanged frozen sources. The four-site part checks construction identities,
not equilibria or a universal hardness assertion.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from functools import reduce
from math import gcd
import importlib.util
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / "original"
RUN = ROOT / "run"
RUN.mkdir(exist_ok=True)
sys.path.insert(0, str(ORIGINAL))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


five = module("frozen_five", ORIGINAL / "facility_spe/shared/five_site_hardness.py")
four = module("frozen_four", ORIGINAL / "facility_spe/shared/four_site_fptas_hardness.py")
audit = module("frozen_audit", ROOT / "related/tests/audits/five_site_hardness.py")


def write(name, value):
    (RUN / name).write_text(json.dumps(five.serial(value), indent=2) + "\n")


five_rows = []
for stem, full in [("five_site_a3_2_no", True),
                   ("five_site_a3_2_yes", True),
                   ("five_site_a809_500_yes", False)]:
    fixture = json.loads((ORIGINAL / "examples/shared" / (stem + ".json")).read_text())
    frozen = json.loads((ORIGINAL / "examples/shared" / (stem + "_metadata.json")).read_text())
    src = frozen["source"]
    factor = frozen["parameters"]["a"]
    argv = [sys.executable, str(ORIGINAL / "facility_spe/shared/five_site_hardness.py"),
            "--factor", factor, "--numbers", ",".join(map(str, src["numbers"])),
            "--target", str(src["target"]), "--output", str(RUN / (stem + "_cli.json")),
            "--metadata", str(RUN / (stem + "_cli_metadata.json"))]
    proc = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    generated = json.loads((RUN / (stem + "_cli.json")).read_text())
    generated_meta = json.loads((RUN / (stem + "_cli_metadata.json")).read_text())
    assert generated == fixture
    assert generated_meta["parameters"] == frozen["parameters"]
    assert reduce(gcd, generated["weights"]) == 1
    result, instance, pars, cert = audit.audit_case(
        src["numbers"], src["target"], F(factor), full)
    assert five.serial(result) == frozen["result"]
    assert instance == fixture
    assert five.serial(pars) == frozen["parameters"]
    if cert:
        assert audit.verify_complete_certificate(instance, cert)
        write(stem + "_complete_certificate.json", cert)
    write(stem + "_audit_result.json", result)
    five_rows.append(dict(stem=stem, source=src, factor=factor,
                          full_diagonal_enumeration=full,
                          constructor_argv=argv, cwd=str(ROOT), returncode=proc.returncode,
                          stdout=proc.stdout, stderr=proc.stderr,
                          instance_equal=True, parameters_equal=True, result_equal=True,
                          integer_scale=generated_meta["integer_scale"],
                          certificate_layouts=25 if cert else 0,
                          result=result))

four_rows = []
for values in ([1], [1, 1], [1, 2, 3], [2, 3, 5], [1, 2, 4, 8],
               [1, 10**60 + 1]):
    pars = four.parameters(values)
    inst = four.reduction(values)
    n, scale = pars["n"], pars["scale"]
    normalized = [F(w, scale) for w in inst["weights"]]
    expected = [pars["M"]] + pars["variables"] + [
        pars["q"], n - pars["q"], F(n),
        pars["R"] - pars["M"] - pars["q"], F(n, 5)]
    assert normalized == expected
    assert len(normalized) == n + 6
    assert all(type(w) is int and w > 0 for w in inst["weights"])
    assert sum(pars["variables"]) == n
    assert sum(abs(w - 1) for w in pars["variables"]) <= F(1, 8*n)
    reach = [sum(normalized[i] for i in s) for s in inst["locations"]]
    assert reach == [F(9*n, 2), F(9*n, 2), pars["R"], pars["d"]]
    assert 2*pars["R"] - pars["q"] == pars["alpha"] * pars["V"]
    assert pars["R"] == pars["alpha"]*(pars["V"] + pars["tau"])/2
    assert inst["U1"] == inst["U2"] == list(range(4))
    # This explicitly searches these small source lists only; reduction() does not.
    partition_yes = any(2*sum(x for x, b in zip(values, bits) if b) == sum(values)
                        for bits in product((0, 1), repeat=len(values)))
    row = dict(values=values, parameters=pars, instance=inst,
               normalized_weights=normalized, normalized_reach=reach,
               source_partition_yes=partition_yes,
               max_integer_bits=max(w.bit_length() for w in inst["weights"]),
               construction_identities_passed=True, equilibrium_solver_run=False)
    four_rows.append(row)

rejections = []
for args in [([], 0, "3/2"), ([True], 0, "3/2"), ([0], 0, "3/2"),
             ([2], True, "3/2"), ([2], -1, "3/2"), ([2], 3, "3/2"),
             ([2], 1, "1"), ([2], 1, "2")]:
    try:
        five.reduction(*args)
    except ValueError as exc:
        rejections.append(dict(api="five.reduction", args=args, error=str(exc)))
    else:
        raise AssertionError(("accepted invalid five-site input", args))
for values in [[], [0], [-1], [True], [F(1)], "1,2"]:
    try:
        four.parameters(values)
    except ValueError as exc:
        rejections.append(dict(api="four.parameters", args=values, error=str(exc)))
    else:
        raise AssertionError(("accepted invalid four-site input", values))

# Exact observation about conversion, not a recommendation to pass binary floats.
float_parameters = five.constants(1.5)
assert float_parameters == five.constants(F(3, 2))
out = dict(python=sys.version, platform=platform.platform(), argv=sys.argv,
           cwd=str(Path.cwd()), five_site_cases=five_rows, four_site_cases=four_rows,
           invalid_api_inputs_rejected=rejections,
           factor_conversion_observation="constants(1.5) equals constants(Fraction(3,2)); no float-type rejection",
           five_case_scope="three exact frozen fixtures; original audit_case; not a universal proof",
           four_case_scope="six original constructor calls and exact formula checks; no equilibrium optimization",
           all_assertions_passed=True, repository_checks_run=False)
write("summary.json", out)
print(json.dumps(five.serial(out), indent=2))
