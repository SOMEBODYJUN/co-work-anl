#!/usr/bin/env python3
"""Exact audit of one-job external-port downward projections.

An internal machine sees port j only when its global bit equals s_j.  A
port's other endpoint is external; its capacity is EXCLUDED from this
projection.  No result here applies to multi-job encodings or to adding
shared external capacities.  The constructor receives two actual uniform
internal assignments; it does not solve for either of them.

Default stdout is a reproducible JSON audit.  All loads, bounds, and
certificates use fractions.Fraction.  Finite checks are not a general proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
from typing import Iterable


VERSION = "signed-one-job-port-downset-v1.0"
SEED = 1729
CLAIM = "UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1"

# Internal edge: (machine, processing time).
Edge = tuple[int, F]
# Port: (its sole internal machine, processing time, incoming global bit).
Port = tuple[int, F, int]


@dataclass(frozen=True)
class Instance:
    machines: int
    jobs: tuple[tuple[Edge, ...], ...]
    ports: tuple[Port, ...]


@dataclass(frozen=True)
class Witness:
    profile: tuple[int, ...]
    assignment: tuple[int, ...]
    loads: tuple[F, ...]


@dataclass(frozen=True)
class MixedResult:
    witness: Witness
    from_uniform_bit: int
    flipped_port: int


def validate(instance: Instance, bound: F) -> None:
    """Validate an explicit, legal, nonnegative rational gadget input."""
    if instance.machines < 1 or not isinstance(instance.machines, int):
        raise ValueError("at least one internal machine is required")
    if not isinstance(bound, F) or bound < 0:
        raise ValueError("bound must be a nonnegative Fraction")
    for job in instance.jobs:
        if not job:
            raise ValueError("each internal job needs at least one endpoint")
        if len({machine for machine, _ in job}) != len(job):
            raise ValueError("a job cannot repeat an internal machine")
        for machine, p in job:
            if not isinstance(machine, int) or not 0 <= machine < instance.machines:
                raise ValueError("invalid internal endpoint")
            if not isinstance(p, F) or p < 0:
                raise ValueError("processing times must be nonnegative Fractions")
    for machine, p, incoming in instance.ports:
        if not isinstance(machine, int) or not 0 <= machine < instance.machines:
            raise ValueError("invalid port endpoint")
        if not isinstance(p, F) or p < 0 or incoming not in (0, 1):
            raise ValueError("invalid signed port")


def machine_loads(instance: Instance, profile: tuple[int, ...],
                  assignment: tuple[int, ...]) -> tuple[F, ...]:
    """Direct job-to-machine accumulation for one concrete assignment."""
    if len(profile) != len(instance.ports) or any(b not in (0, 1) for b in profile):
        raise ValueError("invalid terminal profile")
    if len(assignment) != len(instance.jobs):
        raise ValueError("one option index per internal job is required")
    loads = [F(0) for _ in range(instance.machines)]
    for job, option in zip(instance.jobs, assignment):
        if not isinstance(option, int) or not 0 <= option < len(job):
            raise ValueError("invalid internal assignment option")
        machine, p = job[option]
        loads[machine] += p
    for bit, (machine, p, incoming) in zip(profile, instance.ports):
        if bit == incoming:
            loads[machine] += p
    return tuple(loads)


def recompute_per_machine(instance: Instance, profile: tuple[int, ...],
                          assignment: tuple[int, ...]) -> tuple[F, ...]:
    """Independent regrouping of actual jobs by each physical machine."""
    result = []
    for machine in range(instance.machines):
        internal = sum((job[option][1]
                        for job, option in zip(instance.jobs, assignment)
                        if job[option][0] == machine), F(0))
        terminal = sum((p for bit, (v, p, incoming) in zip(profile, instance.ports)
                        if v == machine and bit == incoming), F(0))
        result.append(internal + terminal)
    return tuple(result)


def verify_witness(instance: Instance, bound: F, witness: Witness) -> None:
    direct = machine_loads(instance, witness.profile, witness.assignment)
    regrouped = recompute_per_machine(instance, witness.profile, witness.assignment)
    assert direct == regrouped == witness.loads
    assert all(load <= bound for load in direct)


def enumerate_projection(instance: Instance, bound: F) -> dict[tuple[int, ...], Witness]:
    """Audit-only exhaustive search over real internal assignments."""
    validate(instance, bound)
    result = {}
    for profile in product((0, 1), repeat=len(instance.ports)):
        for assignment in product(*(range(len(job)) for job in instance.jobs)):
            loads = machine_loads(instance, profile, assignment)
            if max(loads) <= bound:
                witness = Witness(profile, assignment, loads)
                verify_witness(instance, bound, witness)
                result[profile] = witness
                break
    return result


def zero_refined_bound(instance: Instance) -> dict[str, int]:
    """Count bound conditional on both uniform profiles being feasible."""
    z = sum(p == 0 for _, p, _ in instance.ports)
    a = sum(p > 0 and incoming == 0 for _, p, incoming in instance.ports)
    b = sum(p > 0 and incoming == 1 for _, p, incoming in instance.ports)
    positive = a + b
    return {"positive_incoming_at_zero": a, "positive_incoming_at_one": b,
            "zero_ports": z,
            "sign_specific_bound": (1 << z) * ((1 << a) + (1 << b) - 1),
            "balanced_bound": (1 << z) * ((1 << (positive // 2))
                                            + (1 << ((positive + 1) // 2)) - 1)}


def construct_mixed_from_uniform(instance: Instance, bound: F,
                                 zero: Witness, one: Witness) -> MixedResult | None:
    """Delete one incoming port from an INPUT uniform witness; no solving.

    For k < 2 no mixed Boolean profile exists and None is returned.  For
    k >= 2 the provided internal assignment is kept literally unchanged.
    The caller must supply actual feasible all-zero and all-one witnesses.
    """
    validate(instance, bound)
    k = len(instance.ports)
    if zero.profile != (0,) * k or one.profile != (1,) * k:
        raise ValueError("the two input witnesses must be uniform zero and one")
    verify_witness(instance, bound, zero)
    verify_witness(instance, bound, one)
    if k < 2:
        return None
    # Every port is incoming in exactly one of the supplied uniform states.
    chosen_bit = 0 if any(incoming == 0 for _, _, incoming in instance.ports) else 1
    original = zero if chosen_bit == 0 else one
    index = next(j for j, (_, _, incoming) in enumerate(instance.ports)
                 if incoming == chosen_bit)
    profile_list = list(original.profile)
    profile_list[index] = 1 - profile_list[index]
    profile = tuple(profile_list)
    loads = machine_loads(instance, profile, original.assignment)
    witness = Witness(profile, original.assignment, loads)
    verify_witness(instance, bound, witness)
    assert witness.assignment == original.assignment
    machine, p, _ = instance.ports[index]
    for i, (before, after) in enumerate(zip(original.loads, loads)):
        assert after == before - (p if i == machine else F(0))
    assert profile not in {(0,) * k, (1,) * k}
    return MixedResult(witness, chosen_bit, index)


def check_instance(instance: Instance, bound: F) -> dict:
    profiles = enumerate_projection(instance, bound)
    k = len(instance.ports)
    local_profiles = {tuple(int(bit == incoming)
                            for bit, (_, _, incoming) in zip(profile, instance.ports))
                      for profile in profiles}
    # Check every subset, not just immediate one-bit deletions.
    for local in local_profiles:
        for subset in product(*((0, 1) if bit else (0,) for bit in local)):
            assert subset in local_profiles
    zero_positions = [j for j, (_, p, _) in enumerate(instance.ports) if p == 0]
    # Zero processing time makes each such coordinate independently free.
    for profile in profiles:
        for values in product((0, 1), repeat=len(zero_positions)):
            changed = list(profile)
            for j, bit in zip(zero_positions, values):
                changed[j] = bit
            assert tuple(changed) in profiles
    both = (0,) * k in profiles and (1,) * k in profiles
    refined = zero_refined_bound(instance)
    mixed = None
    if both:
        a0 = sum(incoming == 0 for _, _, incoming in instance.ports)
        assert len(profiles) >= (1 << a0) + (1 << (k - a0)) - 1
        assert len(profiles) >= refined["sign_specific_bound"] >= refined["balanced_bound"]
        if bound == 0:
            assert all(p == 0 for _, p, _ in instance.ports)
            assert len(profiles) == 1 << k
        mixed = construct_mixed_from_uniform(instance, bound,
                                            profiles[(0,) * k], profiles[(1,) * k])
        assert (mixed is not None) == (k >= 2)
        if mixed is not None:
            assert mixed.witness.profile in profiles
    return {"profiles": len(profiles), "both_uniform": both,
            "refined": refined, "mixed_constructed": mixed is not None}


def sharp_instance(a: int, b: int, z: int, bound: F = F(1)) -> Instance:
    """Attain the zero-refined count at every a,b,z >= 0, fixed T>0."""
    if min(a, b, z) < 0 or bound <= 0:
        raise ValueError("nonnegative counts and positive bound are required")
    if a and b:
        # The a ports are incoming at global zero; b at global one.
        ports = ((0, bound / a, 0),) * a + ((1, bound / b, 1),) * b
        ports += ((0, F(0), 0),) * z
        return Instance(2, (((0, bound), (1, bound)),), ports)
    positive = a + b
    ports = (() if positive == 0 else
             ((0, bound / positive, 0 if a else 1),) * positive)
    ports += tuple((0, F(0), j % 2) for j in range(z))
    return Instance(1, (), ports)


def serialize_witness(witness: Witness) -> dict:
    return {"profile": list(witness.profile),
            "internal_option_indices": list(witness.assignment),
            "machine_loads": [str(load) for load in witness.loads]}


def two_internal_endpoints_control(bound: F) -> dict:
    """Equality is possible when both physical endpoints are consumed."""
    if bound < 1:
        raise ValueError("this equality control requires a bound at least one")
    accepted = {}
    for x, y in product((0, 1), repeat=2):
        # Physical job 0 -> u iff x=1, job 1 -> u iff y=0.
        assignments = (0 if x else 1, 0 if not y else 1)
        instance = Instance(2, (((0, F(1)), (1, F(1))),) * 2, ())
        loads = machine_loads(instance, (), assignments)
        assert loads == (F(x + 1 - y), F(1 - x + y))
        assert loads == recompute_per_machine(instance, (), assignments)
        if max(loads) <= bound:
            accepted[(x, y)] = [str(load) for load in loads]
    expected = {(0, 0), (1, 1)} if bound < 2 else set(product((0, 1), repeat=2))
    assert set(accepted) == expected
    return {"bound": str(bound),
            "profiles_and_actual_loads": [{"profile": list(p), "loads": loads}
                                           for p, loads in sorted(accepted.items())],
            "scope_violation": "both endpoints internal; no external occurrence slot"}


def all_random_instances(rng: random.Random) -> Iterable[Instance]:
    values = (F(0), F(1, 2), F(1), F(3, 2))
    for machines in range(1, 4):
        for k in range(0, 7):
            for _ in range(30):
                jobs = []
                for _ in range(rng.randrange(5)):
                    choices = rng.sample(range(machines),
                                         rng.randint(1, min(2, machines)))
                    jobs.append(tuple((machine, rng.choice(values)) for machine in choices))
                ports = tuple((rng.randrange(machines), rng.choice(values), rng.randrange(2))
                              for _ in range(k))
                yield Instance(machines, tuple(jobs), ports)


def audit_example() -> dict:
    """Extend the registered sharp input to complete private-host schedules."""
    path = (Path(__file__).resolve().parents[3] / "examples" /
            "unrelated_machines" / "signed_one_job_port_sharp_profiles.json")
    data = json.loads(path.read_text())
    sharp = data["sharp"]
    jobs = tuple(tuple((i, F(p)) for i, p in job) for job in sharp["internal_jobs"])
    ports = tuple((j["internal_machine"], F(j["internal_time"]), j["incoming_bit"])
                  for j in sharp["ports"])
    bound = F(data["T"])
    instance = Instance(len(sharp["internal_machines"]), jobs, ports)
    profiles = enumerate_projection(instance, bound)
    assert len(profiles) == sharp["predicted_strict_profiles"]
    complete = []
    for profile, witness in sorted(profiles.items()):
        machines = sharp["internal_machines"] + sharp["external_machines"]
        loads = {i: F(0) for i in machines}
        assignment = []
        selected_edges = []
        for job, option in zip(jobs, witness.assignment):
            i, p = job[option]
            selected_edges.append((i, p))
        for bit, j in zip(profile, sharp["ports"]):
            internal = bit == j["incoming_bit"]
            selected_edges.append((j["internal_machine"] if internal else j["external_machine"],
                                   F(j["internal_time"] if internal else j["external_time"])))
        for i, p in selected_edges:
            assignment.append(i)
            loads[i] += p
        assert max(loads.values()) <= bound
        assert all(loads[i] == sum((p for v, p in selected_edges if v == i), F(0))
                   for i in machines)
        complete.append({"profile": list(profile), "assignment": assignment,
                         "all_machine_loads": [str(loads[i]) for i in machines]})
    return {"path": path.relative_to(Path(__file__).resolve().parents[3]).as_posix(),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "complete_private_host_schedules": complete}


def audit() -> dict:
    rng = random.Random(SEED)
    random_count = random_both = mixed_count = 0
    for instance in all_random_instances(rng):
        result = check_instance(instance, F(1))
        random_count += 1
        random_both += result["both_uniform"]
        mixed_count += result["mixed_constructed"]
    sharp = []
    for a, b, z in product(range(4), range(4), range(4)):
        instance = sharp_instance(a, b, z)
        result = check_instance(instance, F(1))
        predicted = (1 << z) * ((1 << a) + (1 << b) - 1)
        assert result["both_uniform"] and result["profiles"] == predicted
        sharp.append({"a": a, "b": b, "z": z, "actual_profiles": result["profiles"],
                      "predicted_profiles": predicted})
    # T=0: all zero-time ports are independent, including arbitrary signs.
    zero_cases = []
    for k in range(7):
        instance = Instance(2, (((0, F(0)), (1, F(0))),),
                            tuple((j % 2, F(0), (j // 2) % 2) for j in range(k)))
        result = check_instance(instance, F(0))
        assert result["both_uniform"] and result["profiles"] == 1 << k
        zero_cases.append({"k": k, "profiles": result["profiles"]})
    zero_positive_control = check_instance(
        Instance(1, (), ((0, F(1), 0), (0, F(0), 1))), F(0))
    assert zero_positive_control["profiles"] == 2
    assert not zero_positive_control["both_uniform"]
    # The empty projection and forced jobs are handled, not inferred feasible.
    infeasible = check_instance(Instance(1, (((0, F(2)),),), ()), F(1))
    assert infeasible["profiles"] == 0 and not infeasible["both_uniform"]
    forced = check_instance(Instance(1, (((0, F(1, 3)),),),
                                     ((0, F(0), 0), (0, F(0), 1))), F(1, 3))
    assert forced["profiles"] == 4 and forced["mixed_constructed"]
    many_endpoints = check_instance(
        Instance(3, (((0, F(1)), (1, F(1)), (2, F(1))),),
                 ((0, F(0), 0), (1, F(0), 1))), F(1))
    assert many_endpoints["profiles"] == 4 and many_endpoints["both_uniform"]
    # Giant denominator: all comparisons and witness loads remain exact.
    denominator = (1 << 521) - 1
    tiny_bound = F(1, denominator)
    giant = sharp_instance(2, 3, 2, tiny_bound)
    giant_result = check_instance(giant, tiny_bound)
    assert giant_result["profiles"] == (1 << 2) * ((1 << 2) + (1 << 3) - 1)
    giant_profiles = enumerate_projection(giant, tiny_bound)
    giant_mixed = construct_mixed_from_uniform(giant, tiny_bound,
                                              giant_profiles[(0,) * 7],
                                              giant_profiles[(1,) * 7])
    assert giant_mixed is not None
    # Outside joint capacity is the missing condition in the downset contract.
    projected = enumerate_projection(Instance(1, (), ((0, F(1), 1), (0, F(1), 0))), F(1))
    assert set(projected) == {(0, 0), (0, 1), (1, 1)}
    outside_restored = {profile for profile in projected
                        if F(1 - profile[0] + profile[1]) <= 1}
    assert outside_restored == {(0, 0), (1, 1)}
    controls = [two_internal_endpoints_control(t)
                for t in (F(1), F(3, 2), F(199, 100), F(2))]
    return {
        "claim": CLAIM, "version": VERSION, "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "fractions.Fraction", "seed": SEED,
        "scope": "finite actual-assignment audit, not a general proof or hardness theorem",
        "port_contract": "one internal endpoint; external capacity excluded",
        "constructor_contract": "two feasible uniform assignments supplied; no internal solving",
        "random_parameters": {"machine_counts": [1, 2, 3], "port_counts": list(range(7)),
                              "trials_per_pair": 30, "internal_job_count_range": [0, 4],
                              "processing_times": ["0", "1/2", "1", "3/2"]},
        "random_instances": random_count, "random_both_uniform": random_both,
        "random_mixed_witnesses": mixed_count,
        "sharp_parameter_ranges": {"a": [0, 3], "b": [0, 3], "z": [0, 3], "T": "1"},
        "sharp_fixtures": sharp,
        "zero_bound_cases": zero_cases,
        "zero_bound_positive_port_negative_control": zero_positive_control,
        "empty_infeasible_projection": infeasible["profiles"],
        "forced_job_zero_ports_profiles": forced["profiles"],
        "three_endpoint_auxiliary_profiles": many_endpoints["profiles"],
        "registered_sharp_example": audit_example(),
        "giant_denominator": {"T": str(tiny_bound), "denominator_bit_length": denominator.bit_length(),
                              "a": 2, "b": 3, "z": 2, "profiles": giant_result["profiles"],
                              "mixed_witness": serialize_witness(giant_mixed.witness),
                              "from_uniform_bit": giant_mixed.from_uniform_bit,
                              "flipped_port": giant_mixed.flipped_port},
        "both_internal_endpoints_negative_controls": controls,
        "outside_joint_capacity_negative_control": {
            "projected_profiles": [list(p) for p in sorted(projected)],
            "with_external_machine_capacity": [list(p) for p in sorted(outside_restored)]},
        "status": "passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
