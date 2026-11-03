"""Replay new cross-copy ICs only on complete ordered pure-SPE witnesses.
Finite semantic regression; the universal proof is joint_copy_ic.md.
"""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import joint_copy_restricted as joint
sys.path.insert(0,str(joint.SOURCE))
from audit_root_copy_rows import check

class NewRows:
    def atom_rows(self,a):return joint.cross_rows(a,exact=True)

def run():
    cases=[]
    for themes in [[set()],[set(),{0},{0,1},{1,2}],[set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]:
        cases.append(check(themes,row_model=NewRows))
    out={'status':'passed','scope':__doc__,'cases':cases,'full_ordered_IC_comparisons':sum(c['full_IC'] for c in cases)}
    (HERE/'audit_joint_copy_ic.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()
