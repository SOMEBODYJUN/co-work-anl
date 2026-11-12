#!/usr/bin/env python3
"""Identity and structure review of a fixed stage-3 package.

This does not execute research producers, LPs, backward induction, SPE search,
full primal/dual replay, or coefficient reconstruction. Existing exact reports
remain the arithmetic certificates. The only new arithmetic is parsing rational
scalars, comparing stored exact objectives, and counting finite stored records.
"""
import argparse, ast, collections, gzip, hashlib, json, pathlib
from fractions import Fraction as F

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--output', required=True)
options = ap.parse_args()
root = pathlib.Path(options.repo).resolve()
task_path = 'research/operations/map-v2/tasks/boss1-six-cycle-3a-d7469a7763ca64c6.json'
task = json.loads((root/task_path).read_text())['definition']
refs = task['context_plan']['reading_refs']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(rel):
    p = root/rel
    raw = p.read_bytes()
    return json.loads(gzip.decompress(raw) if p.suffix == '.gz' else raw)
def canon(q): return hashlib.sha256(json.dumps(q,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
entries=[]
for i,ref in enumerate(refs):
    p = root/ref['path']; raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ref['sha256']
    data = gzip.decompress(raw) if p.suffix == '.gz' else raw
    entry = {'index':i,'path':ref['path'],'sha256':ref['sha256'],'bytes':len(raw),'decoded_bytes':len(data)}
    if str(p).endswith(('.json','.json.gz')):
        q=json.loads(data); counter=collections.Counter(); rational_count=0; stack=[q]
        while stack:
            v=stack.pop(); counter[type(v).__name__]+=1
            if isinstance(v,dict):stack.extend(v.values())
            elif isinstance(v,list):stack.extend(v)
            elif isinstance(v,str):
                parts=v.split('/')
                if len(parts)==2 and parts[0].lstrip('-').isdigit() and parts[1].isdigit():
                    F(v); rational_count+=1
        entry.update(format='json',top_keys=list(q) if isinstance(q,dict) else None,
                     full_tree_type_counts=dict(counter),fraction_strings_parsed=rational_count)
        if isinstance(q,dict):entry['top_sizes']={k:len(v) for k,v in q.items() if isinstance(v,(list,dict))}
    elif p.suffix=='.py':
        tree=ast.parse(data)
        entry.update(format='python',functions=[{'name':n.name,'start':n.lineno,'end':n.end_lineno} for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))])
    else:entry.update(format='text',chars=len(data.decode()))
    entries.append(entry)

D='research/workspaces/six-boss2-20261111-cross/'
M=D+'master_cuts/'
rounds=[
 ('5716',M+'master_5716_exact.json.gz',M+'merged_5716_exact.json',M+'dual_exact.json',M+'certificate_verification.json',5716,4849,333,155),
 *[(str(n),M+f'dynamic_{n}_matrix.json.gz',M+f'dynamic_{n}_exact.json',M+f'dynamic_{n}_dual.json',M+f'dynamic_{n}_verification.json',n,4849,p,d) for n,p,d in [(5727,392,165),(5744,295,159),(5752,306,146),(5775,300,137),(5783,267,160),(5786,300,160),(5799,295,163)]],
 ('11418',M+'complete_zz_5799_v1_matrix.json.gz',M+'complete_zz_5799_v1_exact.json',M+'complete_zz_5799_v1_dual.json',M+'complete_zz_5799_v1_verification.json',11418,7639,806,163),
 ('12666',D+'joint_requery/complete624_actual4_R00_v1_matrix.json.gz',M+'complete624_actual4_R00_opt_v2_exact.json',M+'complete624_actual4_R00_opt_v2_dual.json',M+'complete624_actual4_R00_opt_v2_verification.json',12666,12631,929,516)]
matrices=[]; previous=None; values=[]; previous_point=None
for name,mp,pp,dp,vp,nr,nc,np,nd in rounds:
    matrix,point,dual,report=map(load,(mp,pp,dp,vp))
    assert len(matrix['rows'])==matrix['row_count']==nr
    assert len(matrix['columns'])==matrix['column_count']==nc
    assert len(matrix['objective'])==len(matrix['normalization'])==nc
    assert [{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]==matrix['columns']
    nonzeros=0
    for i,row in enumerate(matrix['rows']):
        assert row['index']==i
        cols=[j for j,v in row['nonzero']]
        assert cols==sorted(cols) and len(set(cols))==len(cols)
        assert all(type(j) is int and 0<=j<nc for j in cols)
        nonzeros+=len(cols)
    assert dual['matrix_sha256']==sha(root/mp) and dual['point_sha256']==sha(root/pp)
    assert len(dual['residuals'])==nc and min(map(F,dual['residuals']))>=0
    assert all(F(t['weight'])>0 for t in dual['row_multipliers'])
    assert len(dual['row_multipliers'])==nd
    assert sum(F(c['weight'])>0 for c in point['columns'])==np
    assert min(F(c['weight']) for c in point['columns'])>=0
    assert report['status'].lower() in ('pass','passed')
    for key,rel in [('matrix_sha256',mp),('point_sha256',pp),('dual_sha256',dp)]:assert report[key]==sha(root/rel)
    value=F(point['W']); values.append(value)
    assert value==F(dual['dual_value'])==F(dual['normalization_multiplier'])==F(report.get('exact_optimum',report.get('W')))
    assert F(report['minimum_primal_slack'])==F(report['minimum_dual_residual'])==0
    assert 0<value<F(1,2)
    hist=[c for c in matrix['columns'][:4849] if c['kind']=='hist']
    assert len(hist)==16 and all(c['d']==1 for c in hist)
    if previous is not None:
        oldn=previous['column_count'];oldr=previous['row_count']
        assert matrix['columns'][:oldn]==previous['columns']
        assert matrix['rows'][:oldr]==previous['rows']
        assert matrix['objective']==previous['objective']+['0']*(nc-oldn)
        assert matrix['normalization']==previous['normalization']+['0']*(nc-oldn)
    if name=='5799':
        changed=collections.Counter(c['kind'] for c,d in zip(point['columns'],previous_point['columns']) if F(c['weight'])!=F(d['weight']))
        assert sum(changed.values())==174 and not changed['hist'] and not changed['K']
    else: changed=None
    matrices.append({'name':name,'rows':nr,'columns':nc,'nonzeros':nonzeros,'positive_primal_columns':np,'positive_dual_multipliers':nd,'matrix_sha256':sha(root/mp),'point_sha256':sha(root/pp),'dual_sha256':sha(root/dp),'report_path':vp,'report_sha256':sha(root/vp),'W':str(value),'strict_half_gap':str(1-2*value),'delta_from_previous':str(value-values[-2]) if len(values)>1 else None,'all_16_hist_have_d_one':True,'exact_prefix_preserved':True,'changed_5786_to_5799':dict(changed) if changed else None})
    previous,previous_point=matrix,point
assert values[6]==values[7]==values[8] and values[9]>values[8]
assert all(v>=w for v,w in zip(values[1:],values))
for pref,full in [('complete_zz_5799_v1',M+'complete_zz_5799_v1_exact.json'),('complete624_actual4_R00_opt_v2',M+'complete624_actual4_R00_opt_v2_exact.json')]:
    p=load(full);projection=load(M+pref+'_original4849_exact.json')
    assert projection['columns']==p['columns'][:4849]

inp=load(M+'full_history_probe_12label_v1.json'); result=load(M+'full_history_probe_12label_v1_result.json')
menus=load(M+'full_history_probe_12label_v1_menus.json.gz'); witness=load(M+'full_history_probe_12label_v1_witnesses.json.gz')
assert len(inp['labels'])==12 and len(inp['nonzero_customer_types'])==48
assert result['menus_sha256']==sha(root/(M+'full_history_probe_12label_v1_menus.json.gz'))
assert result['witnesses_sha256']==sha(root/(M+'full_history_probe_12label_v1_witnesses.json.gz'))
assert all(q['input_sha256']==sha(root/(M+'full_history_probe_12label_v1.json')) for q in (result,menus,witness))
leaves=menus['leaf_terminal_counts'];states=menus['states']
assert len(leaves)==len(set(map(tuple,leaves)))==12376
assert len(states)==len({tuple(s['past_counts']) for s in states})==18564
byid={s['state_id']:s for s in states}; assert len(byid)==18564
pairs=0
for s in states:
    c=s['past_counts']; ids=s['menu_terminal_ids'];pairs+=len(ids)
    assert len(c)==12 and 0<=sum(c)<=6 and all(type(z)is int and z>=0 for z in c)
    assert len(ids)==len(set(ids)) and all(0<=j<len(leaves) for j in ids)
    assert all(all(fa>=ca for fa,ca in zip(leaves[j],c)) for j in ids)
    if sum(c)<6:
        assert len(s['child_state_ids'])==len(s['child_minimizing_terminal_ids'])==len(s['child_minimum_payoffs_scaled60'])==12
        for act,childid in enumerate(s['child_state_ids']):
            nxt=c[:];nxt[act]+=1; assert byid[childid]['past_counts']==nxt
            assert s['child_minimizing_terminal_ids'][act] in byid[childid]['menu_terminal_ids']
    else:assert ids==[leaves.index(c)]
assert pairs==result['all_retained_state_terminal_pairs']==33486
rootstate=next(s for s in states if sum(s['past_counts'])==0)
assert [leaves[j] for j in rootstate['menu_terminal_ids']]==[[0]*6+[1]*6]
assert result['target_in_root_menu'] is False and result['minimum_root_W_over_OPT6']=='1'
wr=witness['worst']; nodes=wr['nodes']; keys={(n['state_id'],n['target_terminal_id']) for n in nodes}
assert len(keys)==len(nodes)==wr['node_count']==18564
outgoing=0
for n in nodes:
    state=byid[n['state_id']];target=n['target_terminal_id'];assert target in state['menu_terminal_ids']
    if sum(state['past_counts'])==6:assert state['past_counts']==leaves[target]
    else:
        a=n['chosen_action'];targets=n['child_target_terminal_ids'];assert len(targets)==12 and targets[a]==target
        for childid,ct in zip(state['child_state_ids'],targets):assert (childid,ct) in keys
        outgoing+=12
assert outgoing==74256
spe_report=load(D+'main_verify_full_history_probe_v1.json');assert spe_report['status']=='PASS'
assert spe_report['input_sha256']==sha(root/(M+'full_history_probe_12label_v1.json'))
assert spe_report['menus_sha256']==result['menus_sha256'] and spe_report['witnesses_sha256']==result['witnesses_sha256']
assert spe_report['result_sha256']==sha(root/(M+'full_history_probe_12label_v1_result.json'))

canonical_dir='map/edges/customer-attraction-boss2-six-cross-20261111/'
canonical_names=['three-families-pay-52-added-rows','hierarchy-and-shared-tail-pay-39-more-rows','complete624-projection-pays-lift','full-spe-menu-pays-fixed-catalog-exclusion','portfolio-and-frechet-pay-cap-zz']
registry=load('research/registry.json'); permitted=set(task['object_ids']+task['read_object_ids']);edges=[]
for suffix in canonical_names:
    rel=canonical_dir+'boss2-six-cross-'+suffix+'.json'; edge=load(rel)
    assert rel in registry['edge_files'] and set(edge['source_ids']+edge['target_ids'])<=permitted
    assert edge['status']=='accepted' and edge['premises_mode']=='all' and 'contribution' in edge
    edges.append({'path':rel,'sha256':sha(root/rel),'edge_id':edge['edge_id'],'actual_result':edge['contribution']['result'],'remaining_for_aggregate_target':edge['contribution']['remaining']})
report={'task_id':task['task_id'],'scope':'Current-file SHA, complete JSON/gzip parse and scalar traversal, Python AST parsing, ten saved certificate structural identities/prefixes and stored scalar equalities, stored menu/DAG structure only. No mathematical full LP/DP replay.','script_sha256':sha(pathlib.Path(__file__)),'all_declared_ref_sha_match':True,'ref_count':len(entries),'total_bytes':sum(e['bytes'] for e in entries),'total_decoded_bytes':sum(e['decoded_bytes'] for e in entries),'refs':entries,'ten_saved_LP_certificates':matrices,'fixed_catalog_structural_counts':{'states':len(states),'terminals':len(leaves),'retained_state_terminal_pairs':pairs,'witness_nodes':len(nodes),'witness_child_links':outgoing,'root_menu':[[0]*6+[1]*6],'independent_full_SPE_report_path':D+'main_verify_full_history_probe_v1.json','independent_full_SPE_report_sha256':sha(root/(D+'main_verify_full_history_probe_v1.json'))},'canonical_reuse':edges,'new_research_executions':{'LP':0,'SPE_or_BI':0,'coefficient_reconstruction':0,'full_primal_dual_replay':0,'discoverers':0},'status':'PASS'}
out=pathlib.Path(options.output); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','refs':len(entries),'LP_certificates':len(matrices),'SPE_states_structurally_read':len(states),'canonical_reuse':len(edges),'output':str(out),'sha256':sha(out)},ensure_ascii=False))
