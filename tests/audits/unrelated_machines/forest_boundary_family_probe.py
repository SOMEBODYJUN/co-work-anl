#!/usr/bin/env python3
"""森林边界接口在经典间隙和私有汇点族上的精确运行。"""
from pathlib import Path
import importlib.util, hashlib, json, platform
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[3]
def module(name, rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
base=module('classical','tests/audits/unrelated_machines/rounding_and_gap.py')
up=module('upward','tests/audits/unrelated_machines/forest_boundary_upward.py')

def run():
    classical=[]
    for k in [2,3,4]:
        p,_,t=base.gap_instance(k)
        jobs=[{i:p[i][j] for i in range(len(p)) if p[i][j] is not None} for j in range(len(p[0]))]
        theta=F(2*k-1,k)
        for T in sorted({t,theta}):
            out=up.boundary_oracle(len(p),jobs,0,T,F(1,10))
            if out is None:
                assert T<theta
                classical.append({'k':k,'T':str(T),'reject':True});continue
            b,a,_=out;load=up.load_vector(len(p),jobs,a)
            if T==theta:assert b<=T and max(load)<=F(11,10)*theta
            if F(11,10)*T<theta:assert b>T
            classical.append({'k':k,'machines':len(p),'jobs':len(jobs),'T':str(T),'root_b':str(b),'max_load':str(max(load)),'root_b_at_most_T':b<=T})
    private=[]
    for k in [2,3,5,10]:
        r=k*k
        # Restrict B to H0 as an explicit repair problem. All original small
        # edges remain; the r home-sink components have parallel task bundles.
        jobs=[{0:F(1)}]+[{i:F(1,k),r+i:F(1,k)} for i in range(r) for _ in range(k)]
        out=up.boundary_oracle(2*r,jobs,0,F(1),F(1,10));assert out is not None
        b,a,_=out;load=up.load_vector(2*r,jobs,a)
        assert b==1 and max(load)==1
        assert sum(a[1+t]==r for t in range(k))==k
        private.append({'k':k,'r':r,'machines':2*r,'jobs':len(jobs),'root_b':str(b),'max_load':str(max(load)),'all_B_home_small_moved':k})
    return {'purpose':'finite exact family runs; not a generic scheduler or proof','python':platform.python_version(),'arithmetic':'Fraction/integer','eta':'1/10','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'upward_sha256':hashlib.sha256((ROOT/'tests/audits/unrelated_machines/forest_boundary_upward.py').read_bytes()).hexdigest(),'classical_baseline_sha256':hashlib.sha256((ROOT/'tests/audits/unrelated_machines/rounding_and_gap.py').read_bytes()).hexdigest(),'classical':classical,'private_sink_B_fixed':private,'limits':'Only listed parameters; B restriction in private-sink experiments is explicit and justified by symmetry of that family only.'}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
