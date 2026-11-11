"""Common-denominator encoding of the same three discovered 616 directions.

Keep a row already having a small common denominator. Otherwise rationally
round its saved weights, rebuild every hidden minimum and all columns, and
retain at least 99 percent of the separately recorded numerical LP margin.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import reduce
from math import lcm
import json,hashlib,copy
import cross_query_pairs_v1 as cone
from separate_master import blocks_from_columns

HERE=Path(__file__).resolve().parent


def main():
    discovery_path=HERE/'cross_pairs_selected_5783_three_v1.json';raw=discovery_path.read_bytes();data=json.loads(raw)
    point_raw=Path(data['source_path']).read_bytes();assert hashlib.sha256(point_raw).hexdigest()==data['source_sha256']
    columns=json.loads(point_raw)['columns'];blocks=blocks_from_columns(columns);out=copy.deepcopy(data)
    out['discovery_sha256']=hashlib.sha256(raw).hexdigest();out['discovery_path']=str(discovery_path)
    scans={(s['i'],s['member'],tuple(s['orb'])):s for s in data['scans']}
    for cut in out['cuts']:
        weights={name:F(value) for name,value in cut['weights'].items()};den=reduce(lcm,(w.denominator for w in weights.values()),1)
        if den<=1000000:
            cut['common_denominator']=den;continue
        gap=scans[cut['i'],cut['member'],tuple(cut['orb'])]['gap_float']
        for grid in (10**6,10**7,10**8,10**9):
            integers={name:round(w*grid) for name,w in weights.items()};source=integers.get('sourceT',0)+integers.get('sourceC',0)
            theta={name:F(value,source) for name,value in integers.items() if value}
            row,au,aK,psi=cone.make_row(columns,blocks,cut['member'],tuple(cut['orb']),cut['i'],theta)
            slack=sum(F(c['weight'])*value for c,value in zip(columns,row))
            if slack>=0 or -float(slack)<0.99*gap:continue
            cut['weights']={name:str(w) for name,w in theta.items()};cut['common_denominator']=source;cut['common_rounding_grid']=grid
            cut['u6_coefficient']=str(au);cut['K_coefficient']=str(aK);cut['exact_slack']=str(slack);cut['slack_float']=float(slack)
            cut['sparse_row']=[[ci,str(value)] for ci,value in enumerate(row) if value]
            cut['row_sha256']=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()
            for visible in cut['visible']:
                p,ell,t,qs,mu=visible['state'];visible['minimum']=str(psi(p,ell,t,tuple(map(F,qs)),tuple(map(F,mu))))
            assert F(data['actual_utilities'][cut['i']])+au*F(data['actual_utilities'][5])+aK*F(data['K'])-sum(F(v['mass'])*F(v['minimum']) for v in cut['visible'])==slack
            break
        else:raise ValueError('Could not preserve discovered margin with compact rational weights')
    target=HERE/'cross_pairs_selected_5783_three_compact_v1.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'cuts':[{'i':c['i'],'orb':c['orb'],'slack':c['slack_float'],'common_denominator':c['common_denominator'],'weight_count':len(c['weights'])} for c in out['cuts']]},ensure_ascii=False))


if __name__=='__main__':main()
