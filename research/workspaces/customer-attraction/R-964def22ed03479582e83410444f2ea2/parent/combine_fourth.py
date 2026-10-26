"""Add the new indexed fourth-source inequality to the frozen 701-row system."""
from pathlib import Path
from fractions import Fraction as F
import json,sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba'
sys.path.insert(0,str(OLD/'parent'))
import joint_system as js

def run():
    types,rows=js.build()
    original=json.loads((OLD/'parent/joint_system.json').read_text())
    for i,c in enumerate(original['menu_cuts']):
        rows.append(('same-menu-joint:'+str(i),js.from_weights(c['weights'])))
    for cut in original['pair_cuts']:
        rows.append(js.row(types,{k:v for k,v in cut.items() if k!='separation_slack'}))
    js.verify_primal(original['certificate'],types,rows)
    assert len(rows)==701
    data=json.loads((HERE/'fourth_indexed_projection.json').read_text())
    lookup={(tuple(map(int,z['actual_bits'])),z['d']):F(z['coefficient']) for z in data['coefficients']}
    norm=F(data['scale']*data['integer_weights'][0])
    rows.append(('complete-indexed-actual-fourth',[lookup[t]/norm for t in types]+[F()]))
    result,n=js.solve_primal(types,rows)
    result['base_rows']=701
    result['added_component']='fourth_indexed_projection.json'
    (HERE/'combined_702.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='support'},indent=2),flush=True)
    print('float W/O',float(F(result['W'])),flush=True)

if __name__=='__main__':run()
