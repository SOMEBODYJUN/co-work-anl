#!/usr/bin/env python3
"""Generate only the unbound751 catalogue, schemas and twelve static samples."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import sys

sys.dont_write_bytecode=True
from symbolic_coefficients import (catalogue,coefficient,base_atom_coefficient,
    base_K_coefficient,QUERIES,BASE_KERNEL_SHA,C30_SHA)

HERE=Path(__file__).resolve().parent
WS=HERE.parent
ROOT=HERE.parents[3]
BASE=WS/'actual_source2_opt_requery'
P25_RELEASE={
    'proof.md':'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
    'exact_family.json':'8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0'}
def load(path):return json.loads(path.read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()
def save(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
    for name,h in P25_RELEASE.items():assert digest(WS/'main_all_source25_family'/name)==h
    base_catalog=load(BASE/'row_catalogue.json')
    rows=catalogue()
    assert rows[:243]==base_catalog['rows']
    counts=dict(Counter(row['family'] for row in rows))
    save('row_catalogue.json',{
        'status':'SYMBOLIC_UNBOUND','convention':'A_R nu <= b_R(z,K)',
        'genuine_rows':751,'inherited_rows':243,'nested_source25_rows':507,
        'nested_C30_rows':1,'family_counts':counts,'query_descriptors':QUERIES,
        'inherited_catalogue_sha256':digest(BASE/'row_catalogue.json'),
        'inherited_kernel_sha256':BASE_KERNEL_SHA,'rows':rows})
    release=load(BASE/'main_point_release_template.json')
    release['status']='UNBOUND_AWAITING_FUTURE_MAIN_POINT_AND_ONE_PHASE_I_RELEASE'
    release['required_symbolic_catalogue']='actual_source2_nested_requery/row_catalogue.json, 751 genuine raw rows'
    release['point_role']='A separately released future exact point; no v4 or v5 point selected by this package'
    save('main_point_release_template.json',release)
    template=load(BASE/'symbolic_template.json')
    template['status']='SYMBOLIC_UNBOUND'
    template['stage']='TRUE_INTERNAL_P25_AND_C30_AFTER_FORCED_SOURCE2'
    template['dimensions_at_positive_support_s']['genuine_inequalities']=751
    template['dimensions_at_positive_support_s']['raw_inequalities']='751+2*s'
    template['new_rows']={'P25_sources':[3,4,5],'P25_ordered_pairs_per_source':169,
        'P25_total':507,'C30_true_history':['A1','Q'],'C30_total':1}
    template['suggested_positive_divisors_only']={'inherited243':'unchanged',
        'NESTED_SOURCE25':'25','NESTED_C30':'126000'}
    template['numerically_scaled_rows_created']=False
    save('symbolic_template.json',template)
    save('audit_interface.json',{
        'status':'SYMBOLIC_UNBOUND','row_direction':'A nu <= b; slack=b-A nu >=0',
        'kernel':'symbolic_coefficients.py','catalogue':'row_catalogue.json',
        'samples':'literal_samples.json','first243_equal_frozen_catalogue':True,
        'pure_roles':QUERIES[:-1],'mean_descriptor':'Omean',
        'new_source25':{'sources':[3,4,5],'source_count':3,'ordered_pairs':True,
            'rows_per_source':169,'pure_pure':432,'pure_mean':36,'mean_pure':36,
            'mean_mean_inner30':3,'total':507,
            'true_profile':['a1','q','r3','r4','r5','r6'],
            'p':'sum true profile positions before i','n':'6-i',
            'A_coefficient':'chosen_source25_cost - 25*true_branch_v_i',
            'b_atom':'0','b_K':'c=(7-i)/2=(n+1)/2','forced_source2_not_used':True,
            'inner_size_cap_weights':{'middle_each':'1/2','terminal':'1'},
            'pure_cost':'c*t+24*t/(p+n+1)+query/(p+1+n*t)',
            'pureT_meanQ':'(c+24/D)*t+(o/6)*(1/(p+1)-n*t/((p+1)*D))',
            'meanT_pureQ':'query/(p+1)+(o/6)*(c+24/D-n*query/((p+1)*D))',
            'mean_mean30':'(o/6)*(c+24/D+1/(p+1))','D':'p+n+1'},
        'new_C30':{'h_bits':['a1','q','r3','r4','r5','r6','o'],
            'source_table':'main_thirty_index_strengthening/requery30_envelopes.json',
            'source_table_sha256':C30_SHA,'A_coefficient':'-entry.cut',
            'expanded_A':'m30 - 126000*v3 - 65719*v4 - 4962*v6',
            'wallet_history':['A1','Q'],'b_atom':'0','b_K':'0'},
        'averaging':{'outer6':'already included in nu',
            'single_inner6':'separate average of legal menu queries',
            'double_inner30':'distinct indices only; labels may repeat',
            'own_Q':'pure outer role q, never Omean',
            'direct_inner30_rows':4,'projected_C30_rows_with_inner30_payment':1},
        'actual_X_semantics':'Inherited actual MAX/MX/RC keep old P; X is only a legal query in all additions.',
        'future_projection':{'all_old_types':256,'four_tail_states_per_q':16,
            'all_new_states':8192,'W':'sum(lambda_R*A_R)',
            'a_q':'minimum W over all16 four-tail states',
            'm_o0':'a0','m_o1':'min((5*a0+a1)/6,a1)',
            'delta':'max(a1-a0,0)','gamma':'max(a0-a1,0)',
            'mass_multiplier':'a0, unrestricted sign','state_residual':'W-a_q >= 0'},
        'point_bound':False,'matrix_constructed':False,'optimizer_calls':0,
        'not_claimed':['full8192 coefficient verification','fixed-point feasibility',
            'Farkas certificate','complete SPE','half bound']})
    old_samples=load(BASE/'literal_samples.json')['states']
    samples=[]
    for old in old_samples:
        state={k:old[k] for k in ['id','atom','q','tail']}
        atom,q,tail=state['atom'],state['q'],state['tail']
        values=[{'row':row['name'],'A':str(coefficient(row,atom,q,tail)),
            'b_atom':str(base_atom_coefficient(row,atom)),
            'b_K':str(base_K_coefficient(row))} for row in rows]
        assert values[:243]==old['coefficients']
        samples.append({**state,'coefficients':values})
    save('literal_samples.json',{
        'claim':'Twelve point-free boundary states only; not a fixed LP or full8192 matrix',
        'state_count':12,'rows_per_state':751,'states':samples})

    # Bind the mathematical sources and all protected previous artifacts by SHA.
    sources={}
    def add(path,expected=None):
        path=path.resolve();h=digest(path)
        if expected is not None:assert h==expected,str(path)
        sources[str(path.relative_to(ROOT))]=h
    for pkg in ['actual_source2_opt_requery','v4_source2_identity']:
        manifest_path=WS/pkg/'freeze_manifest.json';manifest=load(manifest_path)
        add(manifest_path);add(WS/pkg/'SHA256SUMS')
        for name,h in manifest['file_sha256'].items():add(WS/pkg/name,h)
    for rel,h in load(WS/'v4_source2_identity/source_hashes.json')['file_sha256'].items():add(ROOT/rel,h)
    for pkg in ['main_all_source31_family','main_thirty_index_strengthening']:
        manifest_path=WS/pkg/'manifest.json';manifest=load(manifest_path)
        add(manifest_path)
        for entry in manifest['files']:add(WS/pkg/entry['path'],entry['sha256'])
    # Main explicitly released these exact P25 bytes; a later manifest is optional.
    for name,h in P25_RELEASE.items():add(WS/'main_all_source25_family'/name,h)
    manifest25=WS/'main_all_source25_family/manifest.json'
    if manifest25.exists():
        add(manifest25)
        for entry in load(manifest25)['files']:add(manifest25.parent/entry['path'],entry['sha256'])
    for rel in ['source31_family_audit.md','source31_family_audit/freeze_manifest.json',
                'source31_family_audit/audit_result.json']:
        add(WS/rel)
    save('frozen_sources_before.json',{'claim':'Only frozen mathematical dependencies and earlier artifacts, no point binding',
        'read_only_files':len(sources),'file_sha256':dict(sorted(sources.items()))})
    save('source_bindings.json',{
        'base243_catalogue':{'path':'actual_source2_opt_requery/row_catalogue.json','sha256':digest(BASE/'row_catalogue.json')},
        'base243_kernel':{'path':'actual_source2_opt_requery/symbolic_coefficients.py','sha256':BASE_KERNEL_SHA},
        'P25_proof':{'path':'main_all_source25_family/proof.md','sha256':digest(WS/'main_all_source25_family/proof.md')},
        'P25_frozen_exact_family':{'path':'main_all_source25_family/exact_family.json','sha256':digest(WS/'main_all_source25_family/exact_family.json'),
            'role':'source provenance only; actual-path320 matrix is not inserted into this nested layer'},
        'P25_release':'Main explicitly released the exact proof/family SHA values before this build; no optimizer authorization follows.',
        'P31_weaker_parent_proof':{'path':'main_all_source31_family/proof.md','sha256':digest(WS/'main_all_source31_family/proof.md')},
        'P31_weaker_parent_audit':{'path':'source31_family_audit.md','sha256':digest(WS/'source31_family_audit.md')},
        'C30_proof':{'path':'main_thirty_index_strengthening/proof.md','sha256':digest(WS/'main_thirty_index_strengthening/proof.md')},
        'C30_envelopes':{'path':'main_thirty_index_strengthening/requery30_envelopes.json','sha256':C30_SHA},
        'all_sources':'frozen_sources_before.json','point_input':None,'point_certificate':None})
    print(json.dumps({'status':'SYMBOLIC751_FILES_WRITTEN','genuine_rows':751,
        'inherited243_unchanged':True,'sample_row_evaluations':9012,
        'sample_fraction_entries':27036,'protected_frozen_sources':len(sources),
        'optimizer_calls':0,'point_bound':False,'matrix_constructed':False},indent=2))

if __name__=='__main__':main()
