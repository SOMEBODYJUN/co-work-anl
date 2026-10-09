"""Finite exact enumeration CLI for the sequential customer-attraction model."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from . import ExactSPESolver, Instance, StrategyCertificate, verify_certificate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("instance", type=Path, help="JSON instance with topics, customers, players")
    parser.add_argument("--certificate", action="store_true", help="include a complete worst-outcome pure SPE strategy")
    parser.add_argument("--verify", type=Path, metavar="CERTIFICATE", help="verify a supplied ordered-history strategy instead of solving")
    parser.add_argument("--output", type=Path, help="write JSON exclusively to a new file")
    args = parser.parse_args()
    try:
        instance = Instance.from_dict(json.loads(args.instance.read_text()))
        if args.verify:
            obj = json.loads(args.verify.read_text())
            certificate = StrategyCertificate.from_dict(obj.get("certificate", obj))
            verification = verify_certificate(instance, certificate)
            verification.assert_valid()
            result = {
                "model": "sequential-unit-customer-attraction-v1",
                "equilibrium": "pure SPE with arbitrary ordered-history strategies",
                "valid": True,
                "terminal_counts": list(verification.terminal_counts),
                "terminal_history": list(verification.terminal_history),
                "checked_histories": verification.checked_histories,
                "checked_deviations": verification.checked_deviations,
            }
        else:
            solver = ExactSPESolver(instance)
            outcomes = sorted(solver.outcomes())
            result = {
                "model": "sequential-unit-customer-attraction-v1",
                "equilibrium": "all pure SPE terminal counts with arbitrary history-dependent ties",
                "instance": instance.to_dict(),
                "outcomes": [{"counts": list(counts), "welfare": instance.welfare(counts)}
                             for counts in outcomes],
                "minimum_spe_welfare": solver.minimum_welfare(),
                "maximum_spe_welfare": solver.maximum_welfare(),
                "optimal_welfare": instance.optimal_welfare(),
                "inefficiency_ratio": str(solver.inefficiency_ratio()),
                "stats": asdict(solver.stats),
            }
            if args.certificate:
                certificate = solver.worst_certificate()
                verify_certificate(instance, certificate).assert_valid()
                result["certificate"] = certificate.to_dict()
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            try:
                with args.output.open("x", encoding="utf-8") as handle:
                    handle.write(rendered)
            except FileExistsError as exc:
                raise ValueError(f"Refusing to overwrite existing output: {args.output}") from exc
        else:
            print(rendered, end="")
    except (OSError, ValueError, ZeroDivisionError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
