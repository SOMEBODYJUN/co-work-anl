#!/usr/bin/env python3
"""One untouched original run; save all actual explicit states and clarify R_B/R_all."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import runpy
import sys

root=Path(__file__).resolve().parent
src=root/'sources/tests/audits/unrelated_machines/fixed_work_and_medium_config_barriers.py'
cases=[];pending={}
def profile(frame,event,arg):
    if frame.f_code.co_filename!=str(src) or frame.f_code.co_name!='private_leaf_states':return
    if event=='call':pending[id(frame)]=(frame.f_locals['h'],frame.f_locals['q'])
    elif event=='return':
        h,q=pending.pop(id(frame));t,states=arg;A=F(2)-F(1,h)
        out=[];wrong_work=0
        for C,W,b,bits,loads in states:
            rb=sum(bits[b*q:(b+1)*q]);ra=sum(bits)
            assert C==max(F(1),A-t*rb)
            assert W==h+(1-t)*ra
            wrong_work+=int(W!=h+(1-t)*rb)
            out.append({'macro_core':b,'tiny_to_leaf_bits':bits,'R_B':rb,'R_all':ra,
                'loads':list(map(str,loads)),'peak':str(C),'work':str(W)})
        quad=[sum(x*x for x in row[4]) for row in states]
        hinge=[sum(max(F(0),x-1) for x in row[4]) for row in states]
        quad_min=min(quad);hinge_min=min(hinge)
        hinge_peaks=sorted({states[i][0] for i,x in enumerate(hinge) if x==hinge_min})
        assert hinge_min==0 and hinge_peaks==[F(1)]
        cases.append({'h':h,'q':q,'t':str(t),'states':out,
            'wrong_if_work_uses_R_B_count':wrong_work,
            'quadratic_global_min':str(quad_min),
            'quadratic_minimizer_peaks':list(map(str,sorted({states[i][0] for i,x in enumerate(quad) if x==quad_min}))),
            'quadratic_strict_q_condition':F(q)>(1-F(1,h))*5,
            'hinge_global_min':str(hinge_min),'hinge_minimizer_peaks':list(map(str,hinge_peaks))})
sys.setprofile(profile)
try:runpy.run_path(str(src),run_name='__main__')
finally:sys.setprofile(None)
(root/'fixed-work-actual-states.json').write_text(json.dumps(cases,indent=2)+'\n')
summary={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
    'python':sys.version,'platform':platform.platform(),'original_entry_executions':1,
    'function_calls':len(cases),'actual_state_count':sum(len(x['states']) for x in cases),
    'work_formula_counterexamples_if_R_B_used':sum(x['wrong_if_work_uses_R_B_count'] for x in cases),
    'cases':[{k:v for k,v in c.items() if k!='states'} for c in cases],
    'all_passed':True,'scope':'Original explicit finite matrices once; profile also checks two-count identities and fixed hinge Delta0 escape. Medium original only checks arithmetic for three alpha, not an expanded k4 matrix or CONFIG.'}
(root/'fixed-work-run.json').write_text(json.dumps(summary,indent=2)+'\n')
