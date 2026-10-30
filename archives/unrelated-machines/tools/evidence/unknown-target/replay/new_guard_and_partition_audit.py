#!/usr/bin/env python3
"""New explicit tests; not the historical missing scratch harness."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util, json, sys, contextlib, io
base=Path(__file__).resolve().parents[1]
src=base/'original/tests/audits/unrelated_machines/unknown_target_common_size_exact_repair.py'
spec=importlib.util.spec_from_file_location('tiny_guard',src);mod=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(mod)
n=1200; f=[F(0)]*n; elig=[[i,i+1] for i in range(n-1)]+[[0]]
witness=list(range(1,n))+[0]
assert all(witness[j] in elig[j] for j in range(n))
assert len(set(witness))==n
try:
    mod.feasible(f,F(1),elig,F(1))
    recursion='returned normally'
except RecursionError:
    recursion='RecursionError'
assert recursion=='RecursionError'
partition=[]
for weights in [[1,1],[1,2,3],[1,1,1,3],[2,2,2,2,2]]:
    B=sum(weights)//2; T=2*B
    assert sum(weights)==2*B and max(weights)<=B
    initial=[3*B,B]; maxima=[B,B]
    assert all(initial[i]<=T+maxima[i] for i in range(2))
    opt=min(max(B+sum(w for w,b in zip(weights,bits) if b==0),B+sum(w for w,b in zip(weights,bits) if b==1)) for bits in product((0,1),repeat=len(weights)))
    balanced=any(sum(w for w,b in zip(weights,bits) if b)==B for bits in product((0,1),repeat=len(weights)))
    assert (opt<=T)==balanced
    partition.append(dict(weights=weights,B=B,T=T,initial=initial,actual_maxima=maxima,opt=opt,balanced=balanced))
result=dict(new_audit=True,historical_harness_replayed=False,recursion_limit=sys.getrecursionlimit(),chain_jobs=n,chain_witness_valid=True,legacy_predicate_outcome=recursion,partition_actual_anchor_cases=partition)
out=base/'replay/new_guard_and_partition_audit.json';out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
