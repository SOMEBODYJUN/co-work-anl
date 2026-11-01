"""Run the unchanged wrapper with its unchanged R18 dependency layout."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
args = sys.argv[1:]
if '--out' not in args:
    raise SystemExit('supply --out and a new output file path')
i = args.index('--out')+1
args[i] = str(Path(args[i]).resolve())
if Path(args[i]).exists():
    raise SystemExit('preserve existing output; choose a new --out')
with tempfile.TemporaryDirectory(prefix='milp-layout-', dir=HERE) as directory:
    root = Path(directory)
    script = root/'research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/portfolio_full_tree.py'
    base = root/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/full_tree_milp.py'
    script.parent.mkdir(parents=True)
    base.parent.mkdir(parents=True)
    shutil.copyfile(HERE/'original/portfolio_full_tree.py', script)
    shutil.copyfile(HERE/'replay/full_tree_milp.py', base)
    raise SystemExit(subprocess.call([sys.executable,str(script),*args]))
