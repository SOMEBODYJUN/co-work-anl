"""Run unchanged discovery bytes with an explicitly reconstructed dependency.

The missing original import prevents an original-environment replay. This run
only demonstrates that the frozen algorithm works with the documented matrices.
The generated certificate must be checked independently with verify.py.
"""
import contextlib
import io
import json
from pathlib import Path
import platform
import sys

import numpy
import scipy

import reconstruct_generator_dependency as dependency


def main():
    root = Path(__file__).resolve().parent
    replay = root / "replay"
    replay.mkdir(exist_ok=True)
    source = root / "original/history/source/notes/customer_attraction/security_gluing_2026-10-10/iid_conditional_dual_generator.py"
    # Compile the exact source bytes; the virtual __file__ only routes its output.
    namespace = {"__name__": "frozen_discovery_reconstruction", "__file__": str(replay / source.name)}
    sys.modules["symmetric_ne_bridge_attack"] = dependency
    exec(compile(source.read_bytes(), namespace["__file__"], "exec"), namespace)
    transcript = io.StringIO()
    with contextlib.redirect_stdout(transcript):
        namespace["extract"](3, 6, dependency.policy36, [dependency.F(1, 6)] * 6,
                             "36_uniform_iid_ne_dual")
    (replay / "generator-stdout.json").write_text(transcript.getvalue())
    generated = json.loads((replay / "36_uniform_iid_ne_dual.json").read_text())
    report = {
        "mode": "unchanged-source-with-new-definition-level-dependency",
        "original_dependency_present_in_frozen_inventory": False,
        "versions": {"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__},
        "sparse_spe_rows": len(generated["sparse_spe"]),
        "sparse_ne_rows": len(generated["sparse_ne"]),
        "self_reported_fraction_valid": generated["fraction_valid"],
        "self_reported_minimum_multiplier": generated["minimum_multiplier"],
        "self_reported_minimum_residual": generated["minimum_residual"],
        "independent_verification_required": True,
    }
    (replay / "generator-reconstruction.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
