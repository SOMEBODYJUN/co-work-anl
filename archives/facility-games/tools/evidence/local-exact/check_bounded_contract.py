"""Narrow exact source-documented regressions; run once under -O.
This is not the unrecovered historical 300/100-case suite and not an optimizer proof.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,importlib.util,json,sys
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('bounded_original',BASE/'original/facility_spe/exact/bounded_overlap.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def single_local(weights):
 return m.local(list(map(F,weights)),[set(range(len(weights)))],0,0)
one=single_local([1]);need(min(z['lo'] for z in one['pieces'])==0,'one-client minimum');need(max(z['hi'] for z in one['pieces'])==1,'one-client maximum');need(any(z['lo']==0 and z['hi']==1 for z in one['pieces']),'one-mixer continuum')
four=single_local([1,1,1,1]);spectrum=sorted({z['lo'] for z in four['pieces']}|{z['hi'] for z in four['pieces']});need(spectrum==[F(7,4),F(2),F(9,4)],'four-unit full local load set')
instance=json.loads((BASE/'author-example-input.json').read_text());certificate=json.loads((BASE/'replay/bounded-author-example.stdout.txt').read_text())
# This checker must not call either enumerator or optimizer, even under -O.
def forbidden(*args,**kwargs):raise RuntimeError('witness checker called support enumerator/optimizer')
m.local=forbidden;m.solve=forbidden;m.verify(instance,certificate)
bad=[]
negative={'finite_factor_exists':False}
missing=copy.deepcopy(certificate);missing['deviations'].pop()
prob=copy.deepcopy(certificate);prob['on_path']['prob_first'][0]='2'
wrongload=copy.deepcopy(certificate);wrongload['on_path']['loads'][0]='5'
for name,value in [('negative-report',negative),('missing-deviation',missing),('probability-out-of-range',prob),('inconsistent-load',wrongload)]:
 try:m.verify(instance,value)
 except ValueError as exc:bad.append({'case':name,'exception_type':'ValueError','message':str(exc)})
 else:raise RuntimeError('accepted '+name)
print(json.dumps({'python_optimize':sys.flags.optimize,'one_client_load_interval':['0','1'],'four_unit_load_spectrum':list(map(str,spectrum)),'attainment_certificate_verified_with_enumerator_and_optimizer_disabled':True,'invalid_certificates_rejected':bad,'historical_300_100_suite_recovered_or_executed':False},indent=2))
