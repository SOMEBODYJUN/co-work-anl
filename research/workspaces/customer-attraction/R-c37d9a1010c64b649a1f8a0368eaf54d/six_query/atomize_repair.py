"""Materialize a small joint (R,Z) support preserving all affine moments.

This is a finite common membership distribution for the necessary graph, not
an SPE strategy or a sufficiency assertion.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
def key(g):return g[0],g[1],tuple(g[2]),tuple(g[3])

def main():
    path=HERE/'repair_zz_exact.json';saved=json.loads(path.read_text());vs={}
    for v in saved['variables']:vs.setdefault(v['mode'],{})[key(v['group'])]=F(v['z_mass'])
    atoms=[]
    for mi,mode in enumerate(saved['modes']):
        mass=F(mode['mass']);z=vs[mi];cuts=sorted({F(),mass,*z.values()})
        for lo,up in zip(cuts,cuts[1:]):
            if lo==up:continue
            atoms.append({'hist_column':mode['hist_column'],'parent_R_mode':mi,'weight':str(up-lo),'R_one_groups':mode['r'],
                          'Z_one_groups':[g for g,q in z.items() if q>=up]})
    # Independently recover every conditional Z mass and mode mass.
    for mi,mode in enumerate(saved['modes']):
        aa=[a for a in atoms if a['parent_R_mode']==mi]
        assert sum((F(a['weight']) for a in aa),F())==F(mode['mass'])
        for g,z in vs[mi].items():
            assert sum((F(a['weight']) for a in aa if g in set(map(key,a['Z_one_groups']))),F())==z
    report={'scope':__doc__,'repair_sha256':sha256(path.read_bytes()).hexdigest(),'fixed_W':saved['fixed_W'],'atom_count':len(atoms),'atoms':atoms}
    (HERE/'joint_atoms.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='atoms'},indent=2))

if __name__=='__main__':main()
