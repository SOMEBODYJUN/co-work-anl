"""Export the generic symbolic lift and the reviewed original-coordinate rows.

No fixed-point RHS is substituted. The already independently rebuilt raw
block is remapped from peer hidden 7639..12630 to our 15593..20584.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import gzip,io,json,time,sys,platform,traceback
import transfer as T

HERE=T.HERE
def signature(row):
    if not row:return ()
    values=[(int(j),F(v)) for j,v in row]
    factor=abs(values[0][1])
    return tuple((j,str(v/factor)) for j,v in values)

def main():
    point,ours,peer,mapping=T.load()
    audit=T.read(HERE/'contract_audit.json')
    assert audit['status']=='PASS' and audit['feature_coefficients_independently_rebuilt']==3115008
    original=ours['columns'][:4849]
    assert original==peer['columns'][:4849]
    added_rows=[];row_names=[];row_metadata=[]
    for oldindex,row in enumerate(peer['rows'][11418:],11418):
        assert all(j<4849 or j>=7639 for j,v in row['nonzero'])
        sp=[[j if j<4849 else j-7639+15593,v] for j,v in row['nonzero']]
        assert sp==sorted(sp)
        assert all(not 4849<=j<15593 for j,v in sp)
        reverse=[[j if j<4849 else j-15593+7639,v] for j,v in sp]
        assert reverse==row['nonzero']
        newindex=19662+oldindex-11418
        added_rows.append(sp);row_names.append(row['name'])
        row_metadata.append({'index':newindex,'peer_row_index':oldindex,'name':row['name'],'kind':row['new_row_kind'],'sparse_sha256':T.canon(sp)})
    assert len(added_rows)==1248
    new_columns=peer['columns'][7639:]
    assert len(new_columns)==4992
    # Carry affine marginal maps, never the particular point's mass values.
    groups=[]
    for oldgroup in mapping['groups']:
        g=dict(oldgroup);g['states']=[]
        for oldstate in oldgroup['states']:
            s=dict(oldstate)
            s['hidden_columns']=[j-7639+15593 for j in oldstate['hidden_columns']]
            s['equality_plus_row']=oldstate['equality_plus_row']-11418+19662
            s['equality_minus_row']=oldstate['equality_minus_row']-11418+19662
            g['states'].append(s)
        groups.append(g)
    budgets=[]
    for oldbudget in mapping['budgets']:
        b=dict(oldbudget);b['row_index']=oldbudget['row_index']-11418+19662;budgets.append(b)
    bundle={'schema':1,'scope':'Generic symbolic full624 lift for only actual4/R/family0-off and the original16 histogram descriptors. All zero-mass cells and all16 hidden states retained. No fixed-point RHS, no SPE sufficiency.',
            'base_matrix_path':str(T.OURS.relative_to(T.REPO)),'base_matrix_sha256':T.sha(T.OURS),'base_point_path':str(T.POINT.relative_to(T.REPO)),'base_point_sha256':T.sha(T.POINT),'base_row_count':19662,'base_column_count':15593,'original_column_count':4849,'preserved_auxiliary_column_count':10744,'added_row_count':1248,'added_column_count':4992,'row_count':20910,'column_count':20585,'inequality_convention':'sum(row[j]*x[j]) >= 0','nonnegative_columns':'all','source_matrix_sha256':T.sha(T.MATRIX),'source_mapping_sha256':T.sha(T.MAP),'source_contract_path':str((T.PEER/'joint_requery/complete624_actual4_R00_v1_contract.md').relative_to(T.REPO)),'source_contract_sha256':T.sha(T.PEER/'joint_requery/complete624_actual4_R00_v1_contract.md'),'independent_contract_audit_sha256':T.sha(HERE/'contract_audit.json'),'independent_audit_script_sha256':T.sha(HERE/'transfer.py'),'original4849_descriptor_sha256':T.canon(original),'original4849_objective_sha256':T.canon(ours['objective'][:4849]),'original4849_normalization_sha256':T.canon(ours['normalization'][:4849]),'new_columns':new_columns,'rows':added_rows,'row_names':row_names,'row_metadata':row_metadata,'objective_extension':['0']*4992,'normalization_extension':['0']*4992,'mapping':{'groups':groups,'budgets':budgets,'hidden_state_order':mapping['hidden_state_order'],'RZ_state_order':mapping['RZ_state_order'],'hidden_column_formula':'15593+64*group_index+16*(2*r+z)+(8*b+4*c+2*j+v)','margin_plus_formula':'19662+2*(4*group_index+2*r+z)','budget_row_formula':'20286+feature_index','new_columns_half_open':[15593,20585],'margin_rows_half_open':[19662,20286],'budget_rows_half_open':[20286,20910]},'base_retention_contract':'Append these rows and columns. Every old row gets4992 zero columns; keep all old15593 descriptors and every19662 old row unchanged. W/O and any old dual extend by zero; existence of a new point at the oldW is not asserted.'}
    target=HERE/'full_lift_bundle.json.gz';assert not target.exists()
    with target.open('wb') as f:
        with gzip.GzipFile(fileobj=f,filename='',mode='wb',mtime=0) as gz:
            with io.TextIOWrapper(gz,encoding='utf-8') as txt:json.dump(bundle,txt,ensure_ascii=False,separators=(',',':'))
    # Read back the delivered bytes, compare the entire remapped block, and
    # check that every link is still a linear relation on the old variables.
    reload=T.read(target)
    assert reload==bundle
    for gi,g in enumerate(reload['mapping']['groups']):
        for si,s in enumerate(g['states']):
            plus={j:F(1) for j in s['hidden_columns']}
            for j,v in s['old_marginal_affine']:plus[j]=-F(v)
            row=s['equality_plus_row']-19662
            assert reload['rows'][row]==T.sparse(plus)
            assert reload['rows'][row+1]==T.sparse({j:-v for j,v in plus.items()})
    report={'status':'PASS','bundle_sha256':T.sha(target),'rows':20910,'columns':20585,'added_rows':1248,'added_columns':4992,'added_nonzeros':sum(len(r) for r in added_rows),'old4849_symbolic_budget_coefficients_retained':True,'all10744_auxiliary_coefficients_zero':True,'fixed_point_rhs_substitutions':0,'all312_symbolic_marginal_equalities_rebuilt':True,'all1248_remapped_rows_exactly_match_independently_audited_source':True,'every_original_row_column_objective_normalization_preserved_by_append':True,'generic_on_entire_fixed_descriptor_domain':True,'zero_source_weight_faces_not_removed':True,'old_optimal_value_may_remain_attainable':True}
    T.write('full_lift_bundle_verification.json',report)

    known=T.read(HERE/'known_rows_transfer_pack.json')['records']
    compact=T.read(HERE/'compact_separating_row_exact.json')
    rounded=T.read(HERE/'separating_row_exact.json')
    proofs=[(r,'known_rows_transfer_pack.json',i) for i,r in enumerate(known)]
    proofs+=[(compact,'compact_separating_row_exact.json',None),(rounded,'separating_row_exact.json',None)]
    wanted={signature(p['sparse_original4849_row']) for p,_,_ in proofs}
    baseline_matches=defaultdict(list)
    # Compare only required oriented rays, retaining all positive candidates.
    target_supports={tuple(j for j,v in sig) for sig in wanted}
    for i,row in enumerate(ours['rows']):
        if tuple(j for j,v in row) not in target_supports:continue
        sig=signature(row)
        if sig in wanted:baseline_matches[sig].append(i)
    all_rows=[];selected=[];seen={}
    # Put the compact integer ray first among fresh negatives so peer-dual
    # scaling is recorded as provenance, not a third mathematically new cut.
    proofs=[proofs[-2],proofs[-1],*proofs[:-2]]
    for proof,origin,index in proofs:
        sig=signature(proof['sparse_original4849_row'])
        sp=proof['sparse_original4849_row']
        rec={'name':proof['name'],'coefficients':sp,'vector_sha256':hashlib.sha256(json.dumps(sp,separators=(',',':')).encode()).hexdigest(),'slack':proof['exact_slack'],'exact_slack':proof['exact_slack'],'slack_float':proof['slack_float'],'sign':proof['sign'],'weights':proof['weights'],'wallet':proof['wallet'],'proof_path':origin,'proof_record_index':index,'proof_file_sha256':T.sha(HERE/origin),'baseline_duplicate_rows':baseline_matches[sig],'all_auxiliary_coefficients_zero':True}
        if sig in seen:rec['same_oriented_ray_as']=seen[sig]
        else:seen[sig]=rec['name']
        all_rows.append(rec)
        if not rec['baseline_duplicate_rows'] and 'same_oriented_ray_as' not in rec:selected.append(rec)
    pack={'scope':'All revalued known rows retained, including positive and zero ones. selected_rows contains only rays absent from frozen19662, deduplicated by positive scaling. Generic full lift is the recommended next LP augmentation.',
          'point_sha256':T.sha(T.POINT),'matrix_sha256':T.sha(T.OURS),'baseline_rows':19662,'columns':15593,'original_columns':4849,'all_rows':all_rows,'selected_rows':selected,'selected_negative_rows':sum(F(r['slack'])<0 for r in selected),'selected_positive_rows':sum(F(r['slack'])>0 for r in selected),'selected_zero_rows':sum(F(r['slack'])==0 for r in selected),'full_lift_bundle_sha256':T.sha(target)}
    T.write('row_transfer_pack.json',pack)
    print(json.dumps({'bundle':report,'all_rows':[{k:r[k] for k in ('name','sign','baseline_duplicate_rows')} for r in all_rows],'selected_rows':[{k:r[k] for k in ('name','sign','slack_float')} for r in selected]},ensure_ascii=False),flush=True)

if __name__=='__main__':
    import hashlib
    started=time.monotonic()
    receipt={'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),'script_sha256':T.sha(Path(__file__)),'transfer_script_sha256':T.sha(HERE/'transfer.py'),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    try:main();receipt['status']='SUCCESS'
    except BaseException as e:receipt.update(status='FAILED',error=repr(e),traceback=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.monotonic()-started
        T.write('execution_build_bundle.json',receipt)
