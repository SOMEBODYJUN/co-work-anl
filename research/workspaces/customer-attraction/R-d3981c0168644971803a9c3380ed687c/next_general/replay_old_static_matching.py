"""Replay an existing independent audit; this is not a new implementation."""
from pathlib import Path
import json
import runpy

HERE = Path(__file__).resolve().parent
WORKSPACES = HERE.parent.parent
SOURCE = (WORKSPACES / "R-a0bb57fa24044a8794bc7991918a19c6"
          / "direct_global/static_matching_independent_audit.py")
OUTPUT = HERE / "old_static_matching_replay.json"

namespace = runpy.run_path(str(SOURCE))
namespace["main"].__globals__["OUTPUT"] = OUTPUT
namespace["main"]()
result = json.loads(OUTPUT.read_text())
result["this_round_provenance"] = (
    "Root replay of the existing author's independent audit, using that exact "
    "implementation; no new independent reconstruction or mathematical result."
)
OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
