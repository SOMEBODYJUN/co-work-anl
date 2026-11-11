"""Seek a common-denominator joint witness, preserving the exact 5744 point."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import portfolio_master as p
from separate_master import blocks_from_columns

package=json.loads((HERE.parent/'portfolio_selected_5744.json').read_text())
cut=package['cuts'][0]
raw=Path(package['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==package['source_sha256']
columns=json.loads(raw)['columns'];blocks=blocks_from_columns(columns)
original={n:F(w) for n,w in cut['weights'].items()}
attempts=[]
for D in (20,50,100,200,500,1000,2000,5000,10000,20000,50000):
    theta={n:F(round(w*D),D) for n,w in original.items() if round(w*D)}
    theta['sourceT']=F(round(original['sourceT']*D),D)
    theta['sourceC']=1-theta['sourceT']
    row,au,aK,psi=p.make_row(columns,blocks,cut['member'],tuple(cut['orb']),cut['i'],theta)
    slack=sum(F(c['weight'])*v for c,v in zip(columns,row));attempts.append({'D':D,'slack':str(slack),'float':float(slack)})
    if slack<0:
        assert all((w*D).denominator==1 for w in theta.values())
        result={'scope':'Common-denominator version of one joint 17-query row. Same exact old 17 single-Q lifts certify strict projection separation.','source_path':package['source_path'],'source_sha256':package['source_sha256'],'i':cut['i'],'k':cut['k'],'member':cut['member'],'orb':cut['orb'],'query_menu':package['query_menu'],'source_sum_integer':D,'weights_integer':{n:str(w*D) for n,w in theta.items()},'u6_coefficient_integer':str(au*D),'K_coefficient_integer':str(aK*D),'slack_normalized_exact':str(slack),'slack_integer_exact':str(slack*D),'slack_float':float(slack),'sparse_row_normalized':[[i,str(x)] for i,x in enumerate(row) if x],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'attempts':attempts}
        (HERE/'joint_common_denominator_5744.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({key:value for key,value in result.items() if key not in ('sparse_row_normalized','attempts','query_menu')},ensure_ascii=False,indent=2));break
else:
    (HERE/'joint_common_denominator_attempts_5744.json').write_text(json.dumps(attempts,indent=2)+'\n');print('no rounded cut')
