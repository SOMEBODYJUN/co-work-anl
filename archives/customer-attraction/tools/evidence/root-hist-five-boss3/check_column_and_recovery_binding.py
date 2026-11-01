"""New saved-input binding only: deterministic columns and rational mass repair.

No source import/exec, no LP, no 1326-row coefficient evaluation, no SPE solver.
The already archived independent row review is deliberately not repeated.
"""
import argparse
import ast
import collections
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--runtime-root',required=True,type=Path)
ap.add_argument('--out',required=True,type=Path)
args=ap.parse_args()
prefix=Path('research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible')
inputs=[]
def read(name):
    p=args.runtime_root/prefix/name;b=p.read_bytes()
    inputs.append({'runtime_relative_path':str(prefix/name),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    return json.loads(b)

old=read('enhanced_2396_exact_obstruction.json')['atom_masses']
run=read('root_full_hist_completion.json')
exact=read('root_full_hist_completion_exact.json')
couple=read('couple_root_refinement.json')
types=list(itertools.product((0,1),repeat=3))
d=[sum(n*t[0]for n,t in zip(a['AB_hist'],types))for a in old]
assert len(old)==38 and d==[1]*38
cols=[];seen=set();corners_added=0;couple_added=0;overlap=[]
def add(a,h):
    key=(a,tuple((t,tuple(v),n)for t,v,n in h if n))
    if key in seen:return False
    seen.add(key);cols.append([a,h]);return True
for a in range(len(old)):
    for v0,v1 in itertools.product(itertools.product((0,1),repeat=4),repeat=2):
        h=[]
        if d[a]<5:h.append([0,list(v0),int(5-d[a])])
        if d[a]>0:h.append([1,list(v1),int(d[a])])
        corners_added+=add(a,h)
assert couple['columns']==len(couple['column_specs'])==96
for ci,(a,h)in enumerate(couple['column_specs']):
    if add(a,h):couple_added+=1
    else:overlap.append(ci)
assert corners_added==9728 and couple_added==42 and len(overlap)==54
assert len(cols)==run['columns']==9770 and cols==run['column_specs']
assert len(set((a,tuple((t,tuple(v),n)for t,v,n in h))for a,h in cols))==len(cols)
assert len(run['point'])==9770 and len(run['row_names'])==len(run['row_specs'])==run['rows']==1326
assert len(run['dual_rows'])==1326 and len(run['dual_equalities'])==run['equalities']==38
assert len(set(run['row_names']))==1326

x=[F(float(t)).limit_denominator(10**9)for t in run['point']]
before_positive=sum(bool(z)for z in x);repairs=[]
for a in range(len(old)):
    inds=[i for i,(aa,h)in enumerate(cols)if a==aa]
    before=sum((x[i]for i in inds),F());mass=F(old[a]['mass'])
    gap=mass-before;j=max(inds,key=lambda i:x[i]);oldj=x[j]
    x[j]+=gap;assert x[j]>=0
    assert sum((x[i]for i in inds),F())==mass
    repairs.append({'atom':a,'column_count':len(inds),'maximum_column_index':j,'target_mass':str(mass),'rounded_sum_before':str(before),'gap_added':str(gap),'selected_before':str(oldj),'selected_after':str(x[j])})
assert min(x)>=0
positive=[{'atom':cols[i][0],'histogram':cols[i][1],'mass':str(z)}for i,z in enumerate(x)if z]
assert len(positive)==exact['positive_columns']==53 and positive==exact['positive_histograms']

# Count and order the ENHANCED descriptors without importing its NumPy/LP path.
labels='ABCDEUVWXY';paths={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}
titles=['L'+str(i)for i in range(3)]+[tag+str(j)for tag,m in [('AB',2),('AE',2),('S',3)]for j in range(1,m+1)]
groups=list(paths)+['AB','AE','S']
new_specs=[]
for title in titles:
    for k in range(4):new_specs.append(['old-index',title,k])
for group in groups:
    for k in range(4):
        for mi in range(21):new_specs.append(['old-tax',group,k,mi])
    for k,l in itertools.combinations_with_replacement(range(4),2):new_specs.append(['old-tax-root',group,k,l])
for k in range(4):
    for mi in range(21):new_specs.append(['root-tax',k,mi])
for k,l in itertools.combinations_with_replacement(range(4),2):new_specs.append(['root-tax-root',k,l])
assert len(new_specs)==698
source=args.runtime_root/prefix/'root_full_hist_enhanced.py'
b=source.read_bytes();inputs.append({'runtime_relative_path':str(prefix/source.name),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
tree=ast.parse(b);addfn=next(z for z in tree.body if isinstance(z,ast.FunctionDef)and z.name=='add')
assert len(addfn.body)==3 and all(isinstance(z,ast.Expr)and isinstance(z.value,ast.Call)and isinstance(z.value.func,ast.Attribute)and z.value.func.attr=='append'for z in addfn.body)
families=dict(collections.Counter(z[0]for z in new_specs))
out={'kind':'new deterministic column/recovery/append-contract binding; no old row recertification','inputs':inputs,'columns':{'all_d':[1]*38,'corner_columns':9728,'previous_coupling_columns':96,'previous_coupling_overlap_corner_indices':overlap,'new_coupling_columns':42,'ordered_full_descriptors_match':True,'total':9770},'recovery':{'algorithm':'Fraction(float).limit_denominator(10**9), then one largest rounded coordinate per old atom receives exact mass residual','before_positive':before_positive,'after_positive':53,'all38_exact_masses_preserved':True,'all_repaired_coordinates_nonnegative':True,'nonzero_repairs':sum(F(z['gap_added'])!=0 for z in repairs),'repairs':repairs,'positive_histograms_in_original_order':positive,'entire_saved_positive_histogram_list_exactly_equal':True,'row_slacks_reused_from_archived_review_not_recomputed':True},'enhanced_contract':{'old_titles':titles,'old_tail_groups':groups,'new_row_kind_counts':families,'new_spec_order':new_specs,'new_rows':698,'base_rows':1326,'total_appended_rows':2024,'source_add_is_three_unconditional_appends':True,'nonzero_or_independent_rank_not_asserted':True,'no_saved_enhanced_result_in_primary':True},'original_import_exec_LP_BI_review_runs_this_batch':0,'new_supplemental_binding_execution':1}
args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'passed','column_order_match':9770,'coupling_overlap':54,'new_coupling_columns':42,'exact_recovery_records_equal':53,'mass_repairs':len(repairs),'enhanced_appended_rows':698,'enhanced_total_rows':2024,'old_row_coefficients_or_LP_recomputed':False}))
