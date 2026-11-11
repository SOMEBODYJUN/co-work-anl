"""Evaluate the frozen sparse layer at a future exact 21021-column point.

No optimization, no canonicalization, no rewriting of any supplied coordinate.
All 1260 facet values and each beta interval/eight-cell witness are returned.
Only supplied values are tested; a failure says nothing about reselecting y/X.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent


def digest(path): return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()


def exact(value):
    if type(value) is int: return F(value)
    if not isinstance(value,str) or not re.fullmatch(r'-?\d+(?:/[1-9]\d*)?',value):
        raise ValueError('Weights must be exact integers or rational strings; no float, decimal, bool or NaN.')
    return F(value)


def dot(row,values): return sum((F(a)*values[j] for j,a in row),F())


def evaluate_block(block,values,facet_values):
    H,x,qy,ry=[values[block[k]] for k in ('H_column','X_column','yQ_column','yR_column')]
    m={s:dot(row,values) for s,row in block['mass_by_QR'].items()}
    old=dict(H=H,x=x,H_minus_x=H-x,yQ=qy,yR=ry,x_minus_yQ=x-qy,x_minus_yR=x-ry,
             q_minus_yQ=m['10']+m['11']-qy,r_minus_yR=m['01']+m['11']-ry,
             **{f'm{s}':v for s,v in m.items()})
    atom_columns={j for row in block['mass_by_QR'].values() for j,a in row if F(a)>0}
    negative_atom_columns={str(j):str(values[j]) for j in atom_columns if values[j]<0}
    residual=sum(m.values(),F())-H
    preconditions=all(v>=0 for v in old.values()) and not residual and not negative_atom_columns
    lower=[F(),qy-m['10'],ry-m['01'],qy+ry-x]
    upper=[m['11'],qy,ry,m['00']-x+qy+ry]
    L,U=max(lower),min(upper)
    complete=preconditions and L<=U
    assert complete==(preconditions and all(v>=0 for v in facet_values))
    result=dict(block=block['block'],key=block['key'],H=str(H),x=str(x),yQ=str(qy),yR=str(ry),
                old_masses={s:str(v) for s,v in m.items()},preconditions_pass=preconditions,
                failed_preconditions={k:str(v) for k,v in old.items() if v<0},
                negative_atom_columns=negative_atom_columns,mass_identity_residual=str(residual),
                six_facet_slacks=list(map(str,facet_values)),
                negative_facets=[f'O{k+1}' for k,v in enumerate(facet_values) if v<0],
                beta_lower=list(map(str,lower)),beta_upper=list(map(str,upper)),
                L=str(L),U=str(U),interval_gap=str(U-L),beta_interval_nonempty=L<=U,
                active_lower_indices=[i for i,v in enumerate(lower) if v==L],
                active_upper_indices=[i for i,v in enumerate(upper) if v==U],
                fixed_values_complete=complete)
    if complete:
        psi={'00':x-qy-ry+L,'10':qy-L,'01':ry-L,'11':L}
        rest={s:m[s]-psi[s] for s in m}
        assert all(v>=0 for v in psi.values()) and all(v>=0 for v in rest.values())
        assert sum(psi.values(),F())==x and psi['10']+psi['11']==qy and psi['01']+psi['11']==ry
        result.update(beta_witness=str(L),X1_four_cells={s:str(v) for s,v in psi.items()},
                      X0_four_cells={s:str(v) for s,v in rest.items()})
    return result


def evaluate(layer,point):
    columns=point.get('columns')
    if not isinstance(columns,list) or len(columns)!=21021:
        raise ValueError('Require exactly 21021 columns; no old 20585-column point or padded projection.')
    descriptors=[{k:v for k,v in c.items() if k!='weight'} for c in columns]
    if sha256(canonical(descriptors)).hexdigest()!=layer['coordinate_descriptors_sha256']:
        raise ValueError('The complete frozen 21021-column descriptor identity differs.')
    values=[exact(c['weight']) for c in columns]
    row_values=[dot(r['row'],values) for r in layer['rows']]
    blocks=[evaluate_block(b,values,row_values[6*b['block']:6*b['block']+6]) for b in layer['blocks']]
    failures=[b['block'] for b in blocks if not b['fixed_values_complete']]
    negative=[dict(local_row=i,append_index_if_used=r['append_index_if_used'],block=r['block'],
                   key=r['key'],facet=r['facet'],value=str(row_values[i]))
              for i,r in enumerate(layer['rows']) if row_values[i]<0]
    summary=dict(negative_facets=len(negative),negative_facet_counts=dict(Counter(r['facet'] for r in negative)),
                 failed_blocks=len(failures),failed_RZ_blocks=sum(blocks[i]['key'][0]=='own-RZ' for i in failures),
                 failed_B4_blocks=sum(blocks[i]['key'][0]=='B4-H1H2' for i in failures),
                 empty_beta_intervals=sum(not b['beta_interval_nonempty'] for b in blocks),
                 base_precondition_failures=sum(not b['preconditions_pass'] for b in blocks),
                 minimum_facet_value=str(min(row_values)),
                 minimum_interval_gap=str(min(F(b['interval_gap']) for b in blocks)))
    return dict(status='FIXED_OWN_X_VALUES_COMPLETE' if not failures else 'FIXED_OWN_X_VALUES_FAIL',
                coordinate_count=21021,facet_count=1260,blocks_checked=210,summary=summary,
                failed_blocks=failures,facet_values=list(map(str,row_values)),negative_rows=negative,blocks=blocks,
                negative_point_columns=[j for j,v in enumerate(values) if v<0],
                canonicalization_performed=False,LP_calls=0,original_22297_rows_rechecked=False,
                scope='Only this supplied exact (old masses,x,y). No claim about reselecting y or X, global feasibility, optimality or SPE.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--point',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=HERE/'point_evaluation.json')
    args=parser.parse_args()
    target=args.output.resolve()
    if not target.is_relative_to(HERE): raise ValueError('Output must stay inside common_x_own_lift/.')
    freeze=json.loads((HERE/'freeze_manifest.json').read_text())
    for name in ('own_facets.json','evaluate_point.py','verification.json'):
        if digest(HERE/name)!=freeze['files'][name]['sha256']:
            raise ValueError(f'Frozen artifact changed: {name}')
    point=json.loads(args.point.read_text())
    layer=json.loads((HERE/'own_facets.json').read_text())
    result=evaluate(layer,point)
    result.update(point_path=str(args.point.resolve()),point_sha256=digest(args.point),
                  frozen_layer_sha256=digest(HERE/'own_facets.json'),freeze_manifest_sha256=digest(HERE/'freeze_manifest.json'),
                  evaluator_sha256=digest(Path(__file__)))
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','summary','point_sha256','scope')},ensure_ascii=False))


if __name__=='__main__': main()
