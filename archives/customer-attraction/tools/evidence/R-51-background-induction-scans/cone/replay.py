"""Reproduce only the documented small cone smoke, from a fresh seed."""
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('source_background_cone',HERE/'source.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.rng.seed(948153)
assert module.scan(3,2,1,2)
