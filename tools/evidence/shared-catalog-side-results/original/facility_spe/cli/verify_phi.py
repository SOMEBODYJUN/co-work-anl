#!/usr/bin/env python3
"""Independently check a shared-catalog certificate and its full continuation.

Only the standard library is used: no producer, menu, load, or NE helper is
imported. Customer costs are recomputed from the incidence input, conditional
on each customer's own action. The certificate's explanatory menu/cycle fields
are not assertions checked by this module.
"""
import argparse
from fractions import Fraction
import json


DEFAULT_CONTINUATION = "guarded_repair of all common customers at facility 1"


def _rational(value, field):
    """Accept exact values only, including JSON decimals read as strings."""
    if type(value) not in (int, str, Fraction):
        raise ValueError(f"{field} must be an integer or exact rational string/value")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{field} is not a finite exact rational") from error


def _array(value, field):
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def _indices(value, bound, field, *, unique=True):
    items = _array(value, field)
    if any(type(i) is not int or not 0 <= i < bound for i in items):
        raise ValueError(f"{field} contains an invalid index")
    if unique and len(set(items)) != len(items):
        raise ValueError(f"{field} contains a duplicated index")
    return items


def _input(instance):
    if not isinstance(instance, dict):
        raise ValueError("The input must be an object")
    weights = [_rational(w, "weight") for w in
               _array(instance.get("weights"), "weights")]
    if any(w <= 0 for w in weights):
        raise ValueError("All customer weights must be positive")
    locations = _array(instance.get("locations"), "locations")
    sites = [set(_indices(site, len(weights), "location", unique=False)) for site in locations]
    if not sites:
        raise ValueError("The shared catalog must be nonempty")
    if "U1" in instance or "U2" in instance:
        first = _indices(instance.get("U1"), len(sites), "U1", unique=False)
        second = _indices(instance.get("U2"), len(sites), "U2", unique=False)
        if not first or set(first) != set(second):
            raise ValueError("U1 and U2 must be the same nonempty shared catalog")
        catalog = list(dict.fromkeys(first))
    else:
        catalog = list(range(len(sites)))
    return weights, sites, catalog


def _layout(value, catalog):
    pair = _array(value, "layout")
    if len(pair) != 2 or any(type(s) is not int or s not in catalog for s in pair):
        raise ValueError("layout must contain two legal tagged facility sites")
    return tuple(pair)


def _customer_check(weights, sites, pair, common, probabilities):
    """Compute independent conditional costs, without a shared NE formula."""
    first, second = pair
    if common != sorted(sites[first] & sites[second]):
        raise ValueError("Witness has an incorrect ordered common-customer list")
    if len(probabilities) != len(common) or any(p < 0 or p > 1 for p in probabilities):
        raise ValueError("Invalid customer probability vector")
    private_first = sum((weights[i] for i in sites[first] - sites[second]), Fraction())
    private_second = sum((weights[i] for i in sites[second] - sites[first]), Fraction())
    x = private_first + sum((weights[i] * p for i, p in zip(common, probabilities)), Fraction())
    y = private_second + sum((weights[i] * (1 - p) for i, p in zip(common, probabilities)), Fraction())
    for customer, probability in zip(common, probabilities):
        # Condition on this customer's actual action. Only OTHER customers'
        # independent probabilities belong in the expected background load.
        cost_first = private_first + weights[customer] + sum(
            (weights[other] * p for other, p in zip(common, probabilities)
             if other != customer), Fraction())
        cost_second = private_second + weights[customer] + sum(
            (weights[other] * (1 - p) for other, p in zip(common, probabilities)
             if other != customer), Fraction())
        if ((probability > 0 and cost_first > cost_second)
                or (probability < 1 and cost_second > cost_first)):
            raise ValueError(f"Customer {customer} is not an exact independent mixed best response")
    return x, y


def _default_profile(weights, sites, pair):
    """Recompute the supported all-first pure repair, including its tie rule.

    Start all common customers at facility 1. While its load is strictly
    larger, move the largest-weight customer still there whose weight is
    strictly smaller than the load gap (ties: smallest customer index).
    Stop at the first load reversal or when no customer strictly improves.
    The caller directly checks the resulting pure NE, on every default layout.
    """
    first, second = pair
    common = sorted(sites[first] & sites[second])
    x = sum((weights[i] for i in sites[first]), Fraction())
    y = sum((weights[i] for i in sites[second] - sites[first]), Fraction())
    probabilities = [Fraction(1) for _ in common]
    while x > y:
        candidates = [j for j, i in enumerate(common)
                      if probabilities[j] == 1 and weights[i] < x - y]
        if not candidates:
            break
        j = max(candidates, key=lambda j: (weights[common[j]], -common[j]))
        probabilities[j] = Fraction(0)
        x -= weights[common[j]]
        y += weights[common[j]]
    return common, probabilities


def verify(instance, certificate):
    """Return True only for an attaining certificate with a complete exact NE rule.

    Verify the on-path profile, exactly one witness for every actual unilateral
    deviation, and the recomputed supported default rule on ALL remaining
    tagged layouts. No menu-minimality, cycle, instance-optimality, universal
    existence, or running-time assertion follows from this instance check.
    """
    weights, sites, catalog = _input(instance)
    if not isinstance(certificate, dict):
        raise ValueError("The certificate must be an object")
    factor = _rational(certificate.get("factor"), "factor")
    if factor < 1 or factor * factor - factor - 1 > 0:
        raise ValueError("Claimed approximation factor is outside [1, phi]")
    if certificate.get("default_continuation") != DEFAULT_CONTINUATION:
        raise ValueError("Unsupported or missing default_continuation rule")

    def check(record):
        if not isinstance(record, dict):
            raise ValueError("Each witness must be an object")
        pair = _layout(record.get("layout"), catalog)
        common = _indices(record.get("common"), len(weights), "common")
        probabilities = [_rational(p, "prob_first") for p in
                         _array(record.get("prob_first"), "prob_first")]
        claimed = [_rational(load, "loads") for load in
                   _array(record.get("loads"), "loads")]
        if len(claimed) != 2:
            raise ValueError("loads must contain exactly two entries")
        loads = _customer_check(weights, sites, pair, common, probabilities)
        if tuple(claimed) != loads:
            raise ValueError("Witness has incorrect facility loads")
        return pair, loads

    (s, t), on_loads = check(certificate.get("on_path"))
    expected = {(1, r, t) for r in catalog if r != s}
    expected |= {(2, s, r) for r in catalog if r != t}
    observed = set()
    covered = {(s, t)}
    for deviation in _array(certificate.get("deviations"), "deviations"):
        if not isinstance(deviation, dict):
            raise ValueError("Each deviation must be an object")
        who = deviation.get("deviator")
        if type(who) is not int or who not in (1, 2):
            raise ValueError("Invalid deviating facility label")
        pair, loads = check(deviation.get("witness"))
        key = (who, *pair)
        if key not in expected or key in observed:
            raise ValueError("Unexpected or duplicated unilateral deviation")
        if loads[who - 1] > factor * on_loads[who - 1]:
            raise ValueError("A facility deviation violates the factor")
        observed.add(key)
        covered.add(pair)
    if observed != expected:
        raise ValueError("Missing unilateral deviations")
    for first in catalog:
        for second in catalog:
            pair = (first, second)
            if pair not in covered:
                common, probabilities = _default_profile(weights, sites, pair)
                _customer_check(weights, sites, pair, common, probabilities)
                covered.add(pair)
    if len(covered) != len(catalog) ** 2:
        raise ValueError("Incomplete tagged-layout continuation")
    return True


def _json(stream):
    """Preserve decimal tokens exactly; reject duplicate keys and NaN/Infinity."""
    def object_from_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicated JSON object key: {key}")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f"Non-rational JSON constant: {value}")

    return json.load(stream, parse_float=str, parse_constant=invalid_constant,
                     object_pairs_hook=object_from_pairs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="exact-rational incidence JSON")
    parser.add_argument("certificate", help="output of facility_spe.shared_phi")
    args = parser.parse_args()
    try:
        with open(args.input, encoding="utf-8") as stream:
            instance = _json(stream)
        with open(args.certificate, encoding="utf-8") as stream:
            certificate = _json(stream)
        verify(instance, certificate)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Invalid certificate or input: {error}\n")
    print("Valid attaining phi certificate: exact customer NE on every tagged layout "
          "and every unilateral facility deviation checked; explanatory menu/cycle metadata unchecked")


if __name__ == "__main__":
    main()
