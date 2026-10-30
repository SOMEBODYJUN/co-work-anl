#!/usr/bin/env python3
"""Producer-independent verifier regressions, including semantic mutants."""
from copy import deepcopy
from fractions import Fraction
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

from facility_spe.cli.verify_phi import DEFAULT_CONTINUATION, _json, verify

ROOT = Path(__file__).resolve().parents[1]


def witness(layout, probabilities, loads, common=None):
    return {"layout": layout, "common": [0, 1] if common is None else common,
            "prob_first": probabilities, "loads": loads}


def fixture():
    """A hand-derived certificate: every customer uses an independent fair coin."""
    instance = {"weights": [1, 1], "locations": [[0, 1], [0, 1]]}
    certificate = {
        "factor": 1,
        "on_path": witness([0, 1], ["1/2", "1/2"], [1, 1]),
        "deviations": [
            {"deviator": 1, "witness": witness([1, 1], ["1/2", "1/2"], [1, 1])},
            {"deviator": 2, "witness": witness([0, 0], ["1/2", "1/2"], [1, 1])},
        ],
        "default_continuation": DEFAULT_CONTINUATION,
    }
    return instance, certificate


class IndependentCertificateTests(unittest.TestCase):
    def rejected(self, instance, certificate):
        with self.assertRaises(ValueError):
            verify(instance, certificate)

    def test_hand_derived_mixed_and_pure_profiles(self):
        instance, certificate = fixture()
        self.assertTrue(verify(instance, certificate))
        certificate["on_path"] = witness([0, 1], [1, 0], [1, 1])
        self.assertTrue(verify(instance, certificate))

    def test_unbalanced_single_mixer_is_an_exact_ne(self):
        # With one co-located customer, both conditional costs are its weight;
        # expected loads need not be equal. Endpoints are also valid.
        for probability in ("0", "1/3", "1"):
            p = Fraction(probability)
            certificate = {"factor": 1,
                           "on_path": witness([0, 0], [probability], [p, 1-p], [0]),
                           "deviations": [], "default_continuation": DEFAULT_CONTINUATION}
            self.assertTrue(verify({"weights": [1], "locations": [[0]]}, certificate))

    def test_probability_mutants_with_correct_total_loads(self):
        instance, baseline = fixture()
        cases = [(["1/4", "3/4"], [1, 1]), ([1, 1], [2, 0]),
                 ([0, 0], [0, 2]), (["-1/2", "3/2"], [1, 1])]
        epsilon = Fraction(1, 10**80)
        cases.append(([Fraction(1, 2)-epsilon, Fraction(1, 2)+epsilon], [1, 1]))
        for probabilities, loads in cases:
            with self.subTest(probabilities=probabilities):
                certificate = deepcopy(baseline)
                certificate["on_path"] = witness([0, 1], probabilities, loads)
                self.rejected(instance, certificate)
        # NE checks must also run at the off-path deviation witnesses.
        certificate = deepcopy(baseline)
        certificate["deviations"][0]["witness"]["prob_first"] = ["1/4", "3/4"]
        self.rejected(instance, certificate)

    def test_forged_loads_and_customer_coverage(self):
        instance, baseline = fixture()
        for field, value in (("loads", [0, 2]), ("loads", [1]),
                             ("common", [1, 0]), ("common", [0, 0]),
                             ("common", [0]), ("prob_first", ["1/2"])):
            with self.subTest(field=field, value=value):
                certificate = deepcopy(baseline)
                certificate["on_path"][field] = value
                self.rejected(instance, certificate)

    def test_exactly_all_unilateral_deviations(self):
        instance, baseline = fixture()
        mutations = []
        certificate = deepcopy(baseline)
        certificate["deviations"].pop()
        mutations.append(certificate)
        certificate = deepcopy(baseline)
        certificate["deviations"].append(deepcopy(certificate["deviations"][0]))
        mutations.append(certificate)
        certificate = deepcopy(baseline)
        certificate["deviations"][0]["deviator"] = 2
        mutations.append(certificate)
        certificate = deepcopy(baseline)
        certificate["deviations"][0]["witness"]["layout"] = [1, 0]  # both move
        mutations.append(certificate)
        certificate = deepcopy(baseline)
        certificate["deviations"][0]["witness"]["layout"] = [0, 1]  # staying put
        mutations.append(certificate)
        for certificate in mutations:
            with self.subTest(certificate=certificate):
                self.rejected(instance, certificate)

    def test_second_facility_inequality_and_zero_payoff(self):
        instance, certificate = fixture()
        instance["weights"] = [2, 1]
        certificate["on_path"] = witness([0, 1], [1, 0], [2, 1])
        certificate["deviations"][0]["witness"] = witness([1, 1], [1, 0], [2, 1])
        certificate["deviations"][1]["witness"] = witness([0, 0], [1, 0], [2, 1])
        self.assertTrue(verify(instance, certificate))
        # This remains an exact NE with correct loads, but facility 2 improves.
        certificate["deviations"][1]["witness"] = witness([0, 0], [0, 1], [1, 2])
        self.rejected(instance, certificate)

        instance = {"weights": [1], "locations": [[], [0]]}
        certificate = {
            "factor": 1, "on_path": witness([0, 1], [], [0, 1], []),
            "deviations": [
                {"deviator": 1, "witness": witness([1, 1], [0], [0, 1], [0])},
                {"deviator": 2, "witness": witness([0, 0], [], [0, 0], [])}],
            "default_continuation": DEFAULT_CONTINUATION}
        self.assertTrue(verify(instance, certificate))
        # Positive gain from zero must fail, even though this mixed NE is valid.
        certificate["deviations"][0]["witness"] = witness([1, 1], ["1/2"], ["1/2", "1/2"], [0])
        self.rejected(instance, certificate)

    def test_factor_bound_and_no_float_or_boolean_coercions(self):
        instance, baseline = fixture()
        for factor in ("1619/1000", "999/1000", 1.0, True, "NaN", "1/0", None):
            with self.subTest(factor=factor):
                certificate = deepcopy(baseline)
                certificate["factor"] = factor
                self.rejected(instance, certificate)
        for field, value in (("prob_first", [0.5, "1/2"]),
                             ("prob_first", [True, False]),
                             ("loads", [1.0, 1]), ("layout", [False, 1]),
                             ("common", [False, 1])):
            certificate = deepcopy(baseline)
            certificate["on_path"][field] = value
            self.rejected(instance, certificate)
        certificate = deepcopy(baseline)
        certificate["deviations"][0]["deviator"] = True
        self.rejected(instance, certificate)
        for value in (True, 1.0, "Infinity", 0, -1):
            bad_instance = deepcopy(instance)
            bad_instance["weights"][0] = value
            self.rejected(bad_instance, baseline)

    def test_catalog_and_incidence_validation(self):
        instance, baseline = fixture()
        for changes in ({"U1": [0, 1]}, {"U1": [0], "U2": [1]},
                        {"U1": [], "U2": []},
                        {"locations": [[False, 1], [0, 1]]}):
            bad_instance = deepcopy(instance)
            bad_instance.update(changes)
            self.rejected(bad_instance, baseline)
        # Set equality permits different catalog ordering; unused sites exist.
        instance["locations"].append([])
        instance["locations"][0] = [0, 0, 1]
        instance.update(U1=[0, 0, 1], U2=[1, 0])
        self.assertTrue(verify(instance, baseline))

    def test_default_rule_is_specified_and_recomputed(self):
        instance, baseline = fixture()
        for rule in (None, "arbitrary text", "all customers at facility 1"):
            certificate = deepcopy(baseline)
            certificate["default_continuation"] = rule
            self.rejected(instance, certificate)
        # More than the on-path/deviation layouts are checked: the generated
        # default profile itself must satisfy direct best-response conditions.
        from unittest.mock import patch
        with patch("facility_spe.cli.verify_phi._default_profile",
                   return_value=([0, 1], [Fraction(1), Fraction(1)])):
            self.rejected(instance, baseline)
        # Menu/cycle claims are expressly outside the attaining certificate.
        baseline.update(response_cycle="not checked", menu_threats="not checked",
                        ordered_pair_count=-1, guarantee="not checked")
        self.assertTrue(verify(instance, baseline))

    def test_empty_instance_and_decimal_json(self):
        instance = {"weights": [], "locations": [[], []]}
        _, certificate = fixture()
        certificate["on_path"] = witness([0, 1], [], [0, 0], [])
        for deviation in certificate["deviations"]:
            deviation["witness"].update(common=[], prob_first=[], loads=[0, 0])
        self.assertTrue(verify(instance, certificate))
        instance, certificate = fixture()
        certificate["on_path"]["prob_first"] = [0.5, 0.5]
        parsed_certificate = _json(io.StringIO(json.dumps(certificate)))
        self.assertTrue(verify(instance, parsed_certificate))
        for raw in ('{"factor":1,"factor":2}', '{"factor":NaN}', '{"factor":Infinity}'):
            with self.assertRaises(ValueError):
                _json(io.StringIO(raw))

    def test_frozen_certificates_and_import_isolation(self):
        for stem in ("tiny", "on_path_chord"):
            with self.subTest(stem=stem):
                instance = _json(io.StringIO((ROOT / f"examples/shared/{stem}.json").read_text()))
                certificate = _json(io.StringIO((ROOT / f"evidence/certificates/shared/{stem if stem != 'tiny' else 'tiny_phi'}.json").read_text()))
                self.assertTrue(verify(instance, certificate))
        # Execute with every producer/local-core import forbidden. This catches
        # a future shortcut back to the producer's validation implementation.
        code = '''
import builtins, json
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name == "facility_spe.shared_phi" or name.startswith("facility_spe.local"):
        raise RuntimeError("verifier imported a producer or shared NE core")
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
from facility_spe.cli.verify_phi import verify
with open("examples/shared/tiny.json") as stream:
    instance = json.load(stream, parse_float=str)
with open("evidence/certificates/shared/tiny_phi.json") as stream:
    certificate = json.load(stream, parse_float=str)
assert verify(instance, certificate)
'''
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
