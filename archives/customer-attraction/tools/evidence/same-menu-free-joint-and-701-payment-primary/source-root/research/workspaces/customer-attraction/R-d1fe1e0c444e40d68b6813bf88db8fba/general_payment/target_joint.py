"""One directed free-joint separation at the parent's exact feasible point."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
import free_joint as gen

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'parent/joint_system.json'

def compact(cut,types,n):
    for den in (100,1000,10000,100000,1000000):
        c=gen.rawcut(cut)
        c['weights']={k:str(F(round(F(v)*den),den)) for k,v in c['weights'].items() if round(F(v)*den)}
        _,row=gen.make_row(types,6,c);slack=sum(x*y for x,y in zip(row,n))
        if slack<0:
            c['at_input_slack']=str(slack);c['rounding_grid']=den
            return c
    raise AssertionError('no compact cut retained strict negativity')

if __name__=='__main__':
    raw=SOURCE.read_bytes();point=json.loads(raw)['certificate']
    types=[(a,d) for a in product((0,1),repeat=6) for d in range(7)]
    n=gen.decode(point,types);cuts=[];diagnostics=[]
    for k in (3,4,5,6):
        new,diag=gen.separate(types,6,n,k)
        cuts += [compact(c,types,n) for c in new];diagnostics+=diag
        print('TARGET',k,'exact new compact cuts',len(new),flush=True)
    report={'scope':'single directed separation of a necessary-row feasible point, not SPE nor half proof','input_file':str(SOURCE.relative_to(gen.ROOT)),'input_sha256':hashlib.sha256(raw).hexdigest(),'input':point,'cuts':cuts,'diagnostics':diagnostics}
    HERE.joinpath('target_joint.json').write_text(json.dumps(report,indent=2)+'\n')
    print('EXACT NEGATIVE CUTS',len(cuts),'at W/O',point['W'],flush=True)
