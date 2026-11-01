"""Small API replay only, not the original default six main scans."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('coverage_probe', HERE/'source.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
reports = []
for args in [(3,2,0,2),(3,2,1,2)]:
    module.rng.seed(228419)
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        result = module.scan(*args)
    reports.append(dict(args=args, returned=result, stdout=stream.getvalue()))
print(json.dumps(reports, indent=2))
