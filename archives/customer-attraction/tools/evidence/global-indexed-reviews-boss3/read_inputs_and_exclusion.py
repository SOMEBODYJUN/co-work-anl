"""Complete descriptor/field read plus ONE exact old-coordinate exclusion sum.

No original import/replay, LP, SPE solver, 2396 coefficient rebuild, or1326
coefficient rebuild here. Those two original entries were replayed separately.
"""
import argparse
import collections
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--repository-root',type=Path,required=True);args=ap.parse_args()
inputs=[]


def read(path):
    b=path.read_bytes();inputs.append(dict(path=str(path),size=len(b),sha256=hashlib.sha256(b).hexdigest()))
    return json.loads(b)


old=read(args.repository_root/'archives/customer-attraction/tools/evidence/R486-same-query-clique-20261101/enhanced_2396_exact_obstruction.json')
spec=read(HERE/'related/root_full_hist_completion.json')
exact=read(HERE/'related/root_full_hist_completion_exact.json')
r2396=read(HERE/'original/review_2396.json');rroot=read(HERE/'original/review_root_completion.json')
atoms=old['atom_masses'];assert len(atoms)==38
TY=list(itertools.product((0,1),repeat=3));QU=list(itertools.product((0,1),repeat=4));ds=[]
for a in atoms:
    assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}and F(a['mass'])>0
    for h,t in zip([a['AB_hist'],a['AE_hist'],a['second_hist']],[TY,TY,QU]):
        assert len(h)==len(t)and all(type(n)is int and n>=0 for n in h)and sum(h)==5
    d=sum(n*t[0]for n,t in zip(a['AB_hist'],TY));ds.append(d)
    assert sum(n*t[0]for n,t in zip(a['AE_hist'],TY))==sum(n*t[0]for n,t in zip(a['second_hist'],QU))==d
    assert len(a['menus_lh'])==3
    for ell,h in a['menus_lh']:assert type(ell)is int and type(h)is int and 0<=h<=d and 0<=ell-h<=5-d
assert r2396['source_sha256']==hashlib.sha256((args.repository_root/'archives/customer-attraction/tools/evidence/R486-same-query-clique-20261101/enhanced_2396_exact_obstruction.json').read_bytes()).hexdigest()
assert rroot['source_sha256']==hashlib.sha256((HERE/'related/root_full_hist_completion_exact.json').read_bytes()).hexdigest()
for name,report,field in [('review_2396.py',r2396,'review_script_sha256'),('review_root_completion.py',rroot,'script_sha256')]:
    assert report[field]==hashlib.sha256((HERE/'original'/name).read_bytes()).hexdigest()

assert set(spec)=={'scope','columns','rows','equalities','status','margin','row_names','row_specs','column_specs','point','dual_rows','dual_equalities'}
assert len(spec['row_names'])==len(spec['row_specs'])==spec['rows']==1326
assert len(set(spec['row_names']))==1326
assert len(spec['column_specs'])==len(spec['point'])==spec['columns']==9770
assert len(spec['dual_rows'])==1326 and len(spec['dual_equalities'])==spec['equalities']==38
assert all(type(v)in(int,float)and math.isfinite(v)for v in spec['point']+spec['dual_rows']+spec['dual_equalities'])
menus=set('ABCDEUVWXY')|{'T','L0','L1','L2','AB:X','AB:Y','AE:X','AE:Y','Sbranch:U','Sbranch:V','Sbranch:W'}
for s in spec['row_specs']:
    kind=s[0]
    if kind=='root':assert len(s)==1
    elif kind=='menu':assert len(s)==3 and s[1]in range(4)and s[2].replace('S:','Sbranch:')in menus
    elif kind=='own':assert len(s)==3 and s[1]in range(4)and s[2]in range(5)and(s[1],s[2])!=(3,4)
    elif kind=='reverse':assert len(s)==4 and s[1]in ['actual','second','third']and s[2]in range({'actual':0,'second':2,'third':3}[s[1]],5)and s[3]in range(4)
    elif kind=='profit':assert len(s)==3 and s[1]in [3,4]and len(s[2])==s[1]and s[2]==sorted(s[2])and all(i in range(10)for i in s[2])
    elif kind=='tax':assert len(s)==3 and 0<=s[1]<=s[2]<21
    elif kind=='off':assert len(s)==3 and all(j in range(4)for j in s[1:])
    else:raise AssertionError(kind)


def histogram_key(ai,hist):
    assert type(ai)is int and 0<=ai<38
    d=0;total=0;bins=collections.Counter()
    for t,v,n in hist:
        assert type(t)is int and t in(0,1)and len(v)==4 and all(type(a)is int and a in(0,1)for a in v)and type(n)is int and n>0
        total+=n;d+=t*n;bins[(t,tuple(v))]+=n
    assert total==5 and d==ds[ai]
    return(ai,tuple(sorted((t,v,n)for(t,v),n in bins.items())))


column_keys=[histogram_key(ai,hist)for ai,hist in spec['column_specs']]
float_positive={k for k,v in zip(column_keys,spec['point'])if v>0}
exact_keys=[];groups=[F(0)]*38
assert len(exact['positive_histograms'])==exact['positive_columns']==53
assert exact['rows']==1326 and exact['equalities']==38 and exact['all_constraints_verified_exactly']is True
for r in exact['positive_histograms']:
    assert set(r)=={'atom','histogram','mass'}and F(r['mass'])>0
    key=histogram_key(r['atom'],r['histogram']);exact_keys.append(key);groups[r['atom']]+=F(r['mass'])
assert len(set(exact_keys))==53 and set(exact_keys)==float_positive and all(k in set(column_keys)for k in exact_keys)
assert all(g==F(a['mass'])for g,a in zip(groups,atoms))
assert exact['minimum_slack']==rroot['minimum_slack']and exact['minimum_slack_float']==rroot['minimum_slack_float']

# One specified later necessary row; no index search or alternative cut search.
summands=[];A=F(0)
for i,a in enumerate(atoms):
    b=list(map(int,a['bits']));p=b[0]+b[1]+b[4]
    ell1,h1=a['menus_lh'][1];ell2,h2=a['menus_lh'][2]
    c=F(ell2-ell1,p+1)-F(h2-h1,(p+1)*(p+2));value=F(a['mass'])*c;A+=value
    summands.append(dict(atom=i,past_ABE_load=p,coefficient=str(c),mass=a['mass'],weighted=str(value)))
expected=F(-33962942532321286037391724417608677893,2370629578513027021549656484975223155224)
assert A==expected<0
out=dict(kind='full input descriptor reconciliation plus one later old-coordinate necessary-row evaluation',inputs=inputs,old38=dict(positive_atoms=38,all_domains_checked=True,source_hash_matches_original_review=True),root_specs=dict(all_fields_read=True,columns=9770,unique_histogram_columns=len(set(column_keys)),rows=1326,equalities=38,row_kind_counts=dict(collections.Counter(s[0]for s in spec['row_specs'])),profit_counts=dict(collections.Counter(str(s[1])for s in spec['row_specs']if s[0]=='profit')),float_positive_columns=len(float_positive),float_negative_columns=sum(v<0 for v in spec['point']),float_primal_and_duals_not_recertified=True),exact53=dict(all53_positive_inputs_valid=True,all_in_original_finite_columns=True,exact_and_float_positive_descriptor_sets_equal=True,all38_marginal_masses_equal_old=True,strict_new_minimum=exact['minimum_slack'],old2396_inherited_by_projection_not_recomputed_per_histogram=True),later_L2_vs_L1=dict(formula='sum_alpha mass_alpha*((ell2-ell1)/(p+1)-(h2-h1)/((p+1)*(p+2))), p=A+B+E',value=str(A),all38_summands=summands,negative=True,projection_preserves_value=True,why='coefficient depends only on retained old atom; each root refinement group sums exactly to old mass',scope='excludes every complete SPE extension keeping these38 old atoms/masses, not arbitrary reoptimized points or half'),extra_coefficient_replays_or_LP_solver_calls=0)
(HERE/'input-and-exclusion-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status='passed',old_atoms=38,root_histograms=53,new_rows=1326,finite_columns=9770,exact_float_support_descriptors_match=True,later_necessary_row=str(A),LP_calls=0)))
