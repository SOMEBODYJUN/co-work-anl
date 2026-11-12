#!/usr/bin/env python3
"""Render the exact JSON audit into readable tables; no new inference."""
from pathlib import Path
from fractions import Fraction as F
import json

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'exact_envelopes.json').read_text())
lines=['# 全部条件最小值的分段表','',
       '每行简写 m=A+Bδ；全部16成本与完整弱态在 exact_envelopes.json。',
       '尾位次固定为 r3 r4 r5 r6。','']
for case in data['cases']:
    lines+=['## '+case['id'],'','| 条件 | 开区间δ | A | B | 全部达到尾 |',
            '|---|---|---:|---:|---|']
    for cid,env in case['envelopes'].items():
        for c in env['open_cells']:
            lines.append('| '+cid+' | ('+c['left']+', '+c['right']+') | '+c['minimum_affine'][0]+
                         ' | '+c['minimum_affine'][1]+' | '+', '.join(c['active_tails'])+' |')
    lines+=['','### 全部端点弱态','','| 条件 | δ | 精确最小值 | 全部达到尾 |',
            '|---|---:|---:|---|']
    for cid,env in case['envelopes'].items():
        for c in env['points']:
            lines.append('| '+cid+' | '+c['delta']+' | '+c['minimum']+' | '+', '.join(c['active_tails'])+' |')
    lines+=['']
(HERE/'conditional_piecewise_table.md').write_text('\n'.join(lines)+'\n')

witnesses=[]
for case in data['cases']:
    if case['mode']=='pure':
        x=F(0) if F(case['s'])==9 else F(1,144)
        p=0 if F(case['s']) else 1
        cid=f'p{p}_t1_o0'
    else:
        x=F(0);p=1;cid='p1_d1_t1'
    q0=F(case['q0']);s=F(case['s'])
    t4=F(5977,6912)-x;t5=F(43,48)+x
    S=1+3*q0/2+t4+t5+q0*t4/12+q0*t5/3
    anchor=S+F(24,p+5)-s/5
    values={r:F(line[0])+F(line[1])*x for r,line in case['states'][cid].items()}
    minimum=min(values.values());active=[r for r,v in values.items() if v==minimum]
    assert minimum<anchor
    witnesses.append({'case':case['id'],'context':cid,'delta':str(x),'old_linear_anchor':str(anchor),
                      'true_minimum':str(minimum),'difference':str(minimum-anchor),'all_active_tails':active,
                      'meaning':'old specified affine anchor fails; not a full SPE counterexample'})
(HERE/'old_anchor_counterexamples.json').write_text(json.dumps({'witnesses':witnesses},ensure_ascii=False,indent=2)+'\n')
print('PASS: readable tables and six exact old-anchor witnesses')
