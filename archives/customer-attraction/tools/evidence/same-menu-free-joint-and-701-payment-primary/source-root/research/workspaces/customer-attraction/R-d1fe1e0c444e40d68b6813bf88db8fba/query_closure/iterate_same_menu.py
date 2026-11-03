"""Add exact same-menu-reply rows to the fixed 587-row m=6 system."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
from same_menu_reply import system,separate,from_weights,solve_exact_system,verify,TYPES,decode,feasible_reply_witness,verify_feasible_reply_witness
TARGET=Path(__file__).with_suffix('.json')
if '--verify' in sys.argv:
    data=json.loads(TARGET.read_text());types,rows,_=system();assert types==TYPES
    for c in data['cuts']:rows.append((c['name'],from_weights(c['weights'])))
    verify(data['final'],types,rows)
    verify_feasible_reply_witness(decode(data['final'],types),data['final_closure_witness'])
    for c in data['cuts']:
        assert F(c['exact_cut_slack'])<0
    print('EXACT VERIFIED',data['final']['W'],len(rows),'necessary rows only')
else:
    types,rows,_=system();assert types==TYPES
    cuts=[];rounds=[]
    for step in range(25):
        result,n=solve_exact_system(6,types,rows)
        sep,row=separate(n,True)
        rounds.append({'step':step,'W':result['W'],'n_rows':len(rows),'gap_float':sep['gap_float'],'exact_cut_slack':sep['exact_cut_slack']})
        print(step,result['W'],float(F(result['W'])),sep['gap_float'],sep['exact_cut_slack'],len(sep['weights']),flush=True)
        if F(sep['exact_cut_slack'])>=0:break
        name=f'same-menu-reply:{step}'
        cuts.append({'name':name,**sep});rows.append((name,row))
    witness=feasible_reply_witness(n,True) if F(sep['exact_cut_slack'])>=0 else None
    TARGET.write_text(json.dumps({'scope':'exact necessary-row refinement, not an SPE or half proof','cuts':cuts,'rounds':rounds,'final':result,'final_closure_witness':witness},indent=2)+'\n')
