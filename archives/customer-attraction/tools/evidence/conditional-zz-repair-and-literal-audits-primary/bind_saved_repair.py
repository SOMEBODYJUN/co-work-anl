"""Bind two saved formats of a mathematical point, without regenerating any row.

No original program, optimizer, game solver, 436-row audit or 108900-pair
loop is called. All 321 rational coordinates, 25 deterministic R modes,
42 saved atoms and 42 saved nonempty ZZ values are compared explicitly.
"""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys
import time

HERE=Path(__file__).resolve().parent
WORKSPACE='research/workspaces/customer-attraction/R-c37d9a1010c64b649a1f8a0368eaf54d/'

def group(g): return (g[0],g[1],tuple(g[2]),tuple(g[3]))
def plain(g): return [g[0],g[1],list(g[2]),list(g[3])]
def hsh(p): return sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def schema(d, keys): return dict(extra=sorted(set(d)-set(keys)), missing=sorted(set(keys)-set(d)))
def leaves(d):
    c=Counter()
    def visit(v):
        c[type(v).__name__]+=1
        if isinstance(v,dict):
            for x in v.values(): visit(x)
        elif isinstance(v,list):
            for x in v: visit(x)
    visit(d);return dict(c)

def main():
    started=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve();ev=repo/'archives/customer-attraction/tools/evidence'
    paths={
      'reference_point':ev/'zz-threshold-exact-point/original/zz_threshold_exact.json',
      'reference_membership':ev/'zz-threshold-exact-point/membership-realization.json',
      'reference_original_execution':ev/'zz-threshold-closure-program/rerun/execution.json',
      'reference_realization_execution':ev/'zz-threshold-exact-point/realization-execution.json',
      'reference_interface':ev/'zz-threshold-closure-program/interface-audit.json',
      'old_point':ev/'combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'}
    manifest=load(HERE/'source-manifest.json');primary={}
    for x in manifest:
        p=HERE/'source-root'/x['path'];assert p.stat().st_size==x['size'] and hsh(p)==x['sha256']
        primary[x['path'][len(WORKSPACE):]]=p
    nr=load(primary['six_query/repair_zz_exact.json']);na=load(primary['six_query/joint_atoms.json'])
    lit=load(primary['six_query/literal_zz_review.json']);aud=load(primary['six_independent/audit_zz_joint.json'])
    ref=load(paths['reference_point']);mem=load(paths['reference_membership']);old=load(paths['old_point'])
    assert hsh(paths['reference_point'])=='72b0d89a7c36f304aead4ae0be9fffa7279316870cd6c3070497f19317367bd0'
    assert nr['source_sha256']==ref['source_sha256']==mem['source_sha256']==hsh(paths['old_point'])
    assert mem['candidate_sha256']==hsh(paths['reference_point'])
    assert mem['prior_ZZ_audit_sha256']==hsh(paths['reference_interface'])
    assert na['repair_sha256']==lit['repair_sha256']==aud['extension_sha256']==hsh(primary['six_query/repair_zz_exact.json'])
    assert lit['source_sha256']==aud['source_sha256']==nr['source_sha256']
    cols=old['columns'];hs={};hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j;hs[j]={'col':c,'groups':{}}
        elif c['kind']=='joint-reply':hs[hi]['groups'].setdefault(group(c['group']),{})[tuple(c['state'])]=j
    reference_modes={};reference_variables={}
    for si,s in enumerate(mem['slabs']):
        vs=[ref['variables'][i] for i in s['variables']]
        rs=frozenset(group(v['group']) for v in vs if v['r'])
        key=(s['hist_column'],F(s['right'])-F(s['left']),rs)
        assert key not in reference_modes;reference_modes[key]=si
        for v in vs: reference_variables[si,group(v['group'])]=v
    mode_map={};modes=[];unmapped=[]
    for mi,m in enumerate(nr['modes']):
        rs=frozenset(map(group,m['r']));assert len(rs)==len(m['r']) and F(m['mass'])>0
        assert rs<=set(hs[m['hist_column']]['groups'])
        key=(m['hist_column'],F(m['mass']),rs);si=reference_modes.get(key)
        mode_map[mi]=si
        if si is None:unmapped.append(mi)
        modes.append(dict(mode=mi,reference_slab=si,hist_column=m['hist_column'],mass=m['mass'],R_one_groups=m['r'],
            reference_interval=None if si is None else [mem['slabs'][si]['left'],mem['slabs'][si]['right']],
            schema=schema(m,['hist_column','mass','r'])))
    variables=[];seen=set();different=[]
    for vi,v in enumerate(nr['variables']):
        mi=v['mode'];g=group(v['group']);assert (mi,g) not in seen;seen.add((mi,g))
        assert F(v['mass'])==F(nr['modes'][mi]['mass']) and 0<=F(v['z_mass'])<=F(v['mass'])
        rv=reference_variables.get((mode_map[mi],g));equal=rv is not None and F(rv['weight'])==F(v['z_mass'])
        if not equal:different.append(vi)
        variables.append(dict(index=vi,mode=mi,reference_slab=mode_map[mi],group=v['group'],mass=v['mass'],z_mass=v['z_mass'],
            reference_record=rv,exact_z_equal=equal,schema=schema(v,['mode','group','mass','z_mass'])))
    expected_keys={(mi,g) for mi,m in enumerate(nr['modes']) for g in hs[m['hist_column']]['groups']}
    missing_variable_keys=expected_keys-seen;extra_variable_keys=seen-expected_keys
    PAT=tuple(product((0,1),repeat=3));EDGES=tuple(e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2])
    atoms=[];atom_sums=defaultdict(F);z_sums=defaultdict(F);actual_atoms=Counter()
    for ai,a in enumerate(na['atoms']):
        mi=a['parent_R_mode'];hi=a['hist_column'];assert hi==nr['modes'][mi]['hist_column']
        weight=F(a['weight']);assert weight>0
        rs=set(map(group,a['R_one_groups']));zs=set(map(group,a['Z_one_groups']))
        assert len(rs)==len(a['R_one_groups']) and len(zs)==len(a['Z_one_groups'])
        assert rs==set(map(group,nr['modes'][mi]['r'])) and zs<=set(hs[hi]['groups'])
        c=hs[hi]['col'];words=[w for w,n in zip(PAT,c['hist']) for _ in range(n)]
        eg=[(f,int(i==j),words[i],words[j]) for f,i,j in EDGES]
        bits=list(map(int,c['actual_bits']))+[w[k] for k in range(3) for w in words]+[int(g in rs) for g in eg]+[int(g in zs) for g in eg]
        assert len(bits)==156
        string=''.join(map(str,bits));actual_atoms[mode_map[mi],hi,weight,string]+=1
        atom_sums[mi]+=weight
        for g in zs:z_sums[mi,g]+=weight
        atoms.append(dict(index=ai,parent_R_mode=mi,reference_slab=mode_map[mi],hist_column=hi,weight=a['weight'],membership_156=string,
            schema=schema(a,['hist_column','parent_R_mode','weight','R_one_groups','Z_one_groups'])))
    for mi,m in enumerate(nr['modes']):assert atom_sums[mi]==F(m['mass'])
    for v in nr['variables']:assert z_sums[v['mode'],group(v['group'])]==F(v['z_mass'])
    reference_atoms=Counter((a['R_slab'],a['hist_column'],F(a['mass']),a['membership_156']) for a in mem['atoms'])
    atom_mismatches=dict(only_primary=[dict(key=[k[0],k[1],str(k[2]),k[3]],multiplicity=v) for k,v in (actual_atoms-reference_atoms).items()],
        only_reference=[dict(key=[k[0],k[1],str(k[2]),k[3]],multiplicity=v) for k,v in (reference_atoms-actual_atoms).items()])
    refzz={(r['family'],r['query_family'],tuple(r['pattern'])):F(r['slack']) for r in mem['ZZ_rows']}
    zz=[];keys=[]
    for r in lit['all_class_slacks']:
        f,g,p=r['class'];key=f,g,tuple(p);keys.append(key)
        zz.append(dict(index_class=r['class'],primary_slack=r['slack'],reference_slack=str(refzz.get(key)),exact_equal=refzz.get(key)==F(r['slack'])))
    assert len(keys)==len(set(keys))
    empty_reference=[dict(index_class=[f,g,list(p)],slack=str(v)) for (f,g,p),v in refzz.items() if (f,g,p) not in keys]
    reference_extras=[k for k,v in refzz.items() if k not in keys and v!=0]
    field_review=dict(repair_top=schema(nr,['scope','source_sha256','status','success','rows','Z_variables','R_modes','fixed_W','minimum_exact_slack','modes','variables']),
      atoms_top=schema(na,['scope','repair_sha256','fixed_W','atom_count','atoms']),
      literal_top=schema(lit,['scope','source_sha256','repair_sha256','fixed_hist_and_R_marginals_exact','mode_count','literal_comparisons','nonempty_index_classes','minimum_ZZ_slack','formerly_negative_class_slack','all_class_slacks']),
      independent_top=schema(aud,['scope','source_sha256','extension_sha256','histograms','positive_R_modes','Z_variables','literal_edge_pairs','joint_state_bounds_checked','RR_intersection_checks','RR_upper_bounds_checked','total_rows_accounted','independently_rebuilt_raw_rows','minimum_rebuilt_slack','ZZ_classes','structurally_nonempty_ZZ_classes','nonzero_ZZ_classes','minimum_ZZ_slack','O','W','strict_half_gap','conditional_joint_realization']))
    all_schema=[*field_review.values(),*[x['schema'] for x in modes+variables+atoms]]
    top_equal=(F(nr['fixed_W'])==F(na['fixed_W'])==F(aud['W'])==F(ref['W'])==F(old['W']) and nr['rows']==ref['rows']==3949 and nr['Z_variables']==ref['variables_count']==321 and nr['R_modes']==len(mem['slabs'])==25)
    all_equal=not unmapped and not different and not missing_variable_keys and not extra_variable_keys and actual_atoms==reference_atoms and all(x['exact_equal'] for x in zz) and not reference_extras and top_equal and all(not s['extra'] and not s['missing'] for s in all_schema)
    data_report=dict(status='ALL_MATHEMATICAL_COORDINATES_AND_SAVED_ATOMS_MATCH' if all_equal else 'DIFFERENCES_RETAINED_REVIEW_REQUIRED',
      source_manifest_sha256=hsh(HERE/'source-manifest.json'),checker_sha256=hsh(Path(__file__)),
      input_fingerprints={k:dict(repo_path=str(p.relative_to(repo)),size=p.stat().st_size,sha256=hsh(p)) for k,p in paths.items()},
      primary_top_fields=dict(repair={k:v for k,v in nr.items() if k not in ['modes','variables']},atoms={k:v for k,v in na.items() if k!='atoms'},literal={k:v for k,v in lit.items() if k!='all_class_slacks'},independent=aud),
      primary_leaf_counts={k:leaves(load(p)) for k,p in primary.items() if p.suffix=='.json'},field_review=field_review,
      format_mapping={'mode':'hist_column, mass, R-one set maps uniquely to reference R slab [left,right]',
       'z_coordinate':'(mode,group,z_mass) -> (hist_column,left,right,group,r,weight); mass=right-left, r determined by R-one set',
       'atom':'group sets expand to all156 labels in old canonical words/order; compare mass and all bits with mature42 atoms',
       'ZZ':'42 saved structurally nonempty values compared to mature60; other18 reference slots must all0',
       'unmapped_report_fields':'scope/status/success/minimum_exact_slack are report metadata, preserved above, not equated to an execution; mature positive_variables/free_vertex_variables not present in C7 format'},
      totals=dict(R_modes=len(modes),Z_coordinates=len(variables),positive_Z_coordinates=sum(F(v['z_mass'])>0 for v in nr['variables']),strict_interior_Z_coordinates=sum(0<F(v['z_mass'])<F(v['mass']) for v in nr['variables']),saved_atoms=len(atoms),saved_atom_bit_entries=156*len(atoms),saved_ZZ_rows=len(zz),reference_only_ZZ_zero_slots=len(empty_reference)),
      unmapped_modes=unmapped,different_coordinates=different,missing_variable_keys=[str(k) for k in missing_variable_keys],extra_variable_keys=[str(k) for k in extra_variable_keys],
      modes=modes,all_coordinates=variables,all_saved_atoms=atoms,atom_mismatches=atom_mismatches,all_saved_ZZ=zz,reference_only_ZZ_slots=empty_reference,
      exact_top_invariants_match=top_equal,all_equal=all_equal,
      execution_scope='one static exact binding; no original import/main, no matrix generation, no old3889/new60/436 audit or edge-pair sweep, no optimization/SPE',
      original_program_calls=0,lp_calls=0,slsqp_calls=0,spe_solver_calls=0,elapsed_seconds=time.perf_counter()-clock)
    args.output.write_text(json.dumps(data_report,ensure_ascii=False,indent=2)+'\n')
    event=dict(argv=sys.argv,started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=data_report['elapsed_seconds'],exit_code=0,comparison_entry_calls=1,checker_sha256=data_report['checker_sha256'],report_sha256=hsh(args.output),original_program_calls=0,lp_calls=0,spe_solver_calls=0,scope=data_report['execution_scope'])
    args.output.with_name('binding-execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:data_report[k] for k in ['status','totals','unmapped_modes','different_coordinates','exact_top_invariants_match','elapsed_seconds']},ensure_ascii=False))
if __name__=='__main__':main()
