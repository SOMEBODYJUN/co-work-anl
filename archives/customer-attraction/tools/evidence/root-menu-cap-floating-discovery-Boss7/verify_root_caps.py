#!/usr/bin/env python3
import hashlib, json, math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXPECTED={
 'root_cap_group_factor2.5.json':('25261bdccbe1c27d137b','fa95ba29e2130fa52f1d9fb138064f5c97f90b0d86427555a5456ee762567968',2.5,278,'-0.07754629629629628'),
 'root_cap_group_factor3.json':('3b4b9db523e90c02ffef','89d34bf1f96e51bd7ee571e831a617b59de7128001c7c8e4c39ea0b840cb8028',3.0,190,'0.06250000000000011'),
}
out={}
for fn,(sid,sha,factor,trace_n,best_gap) in EXPECTED.items():
    b=(ROOT/fn).read_bytes(); d=json.loads(b)
    assert hashlib.sha256(b).hexdigest()==sha
    assert d['status']=='floating discovery; no universal assertion'
    assert d['factor']==factor and d['full_histories']==43 and d['true_rows']==215 and d['seed']==3738
    assert len(d['root_backgrounds'])==2 and len(d['trace'])==trace_n
    for row in d['trace']:
        assert len(row['p'])==6
        assert abs(sum(row['p'])-1)<=2e-8
        assert abs(row['gap']-(factor*row['cap']-row['W']))<=2e-8
        assert all(x>=-2e-8 for x in row['p'])
        assert all(x>=-2e-8 for x in row['weights'].values())
        assert abs(sum(row['weights'].values())-1)<=2e-7
    assert abs(d['best']['gap']-float(best_gap))<=2e-12
    out[fn]={'source_id':sid,'sha256':sha,'bytes':len(b),'trace':trace_n,'factor':factor,
             'full_histories':43,'true_rows':215,'best_gap':d['best']['gap'],
             'best_W':d['best']['W'],'best_cap':d['best']['cap'],
             'trace_gap_min':min(x['gap'] for x in d['trace']),'trace_gap_max':max(x['gap'] for x in d['trace']),
             'best_gap_limit_denominator':str(Fraction(d['best']['gap']).limit_denominator(1000000)),
             'best_W_limit_denominator':str(Fraction(d['best']['W']).limit_denominator(1000000)),
             'best_cap_limit_denominator':str(Fraction(d['best']['cap']).limit_denominator(1000000))}
print(json.dumps({'checks':'structural and arithmetic consistency only; no LP optimality proof', 'files':out},ensure_ascii=False,indent=2))
