"""Build a self-contained asset from the reviewed engine, UI and scenario inputs."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--scenarios", type=Path, default=ROOT / "scenarios.json")
parser.add_argument("--output", type=Path, default=ROOT / "calculator.html")
args = parser.parse_args()
text = (ROOT / "ui.html").read_text(encoding="utf-8")
for marker, path, data in [
    ("SCENARIOS", args.scenarios, True),
    ("EXAMPLE", ROOT / "synthetic_household.json", True),
    ("ENGINE", ROOT / "engine.js", False),
    ("UI", ROOT / "ui.js", False),
]:
    contents = path.read_text(encoding="utf-8")
    if data:
        value = json.loads(contents)
        if marker == "SCENARIOS" and isinstance(value, dict):
            value = value["scenarios"]
        contents = json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", r"\u003c")
    elif "</script" in contents.lower():
        raise ValueError("Unexpected closing script tag in " + path.name)
    assert text.count("@@" + marker + "@@") == 1
    text = text.replace("@@" + marker + "@@", contents)
args.output.write_text(text, encoding="utf-8")
print(args.output)
