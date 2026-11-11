"""Re-run the independent old literal-payoff verifier on the new joint atoms."""
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
cmd=[sys.executable,str(WORK/'common_network_19662/verify_common.py'),
     '--point',str(WORK/'union_augmented_lp/augmented_lp_exact.json'),
     '--witness',str(HERE/'common_atoms_with_D.json'),
     '--output',str(HERE/'old_network_verification.json')]
subprocess.run(cmd,check=True)
