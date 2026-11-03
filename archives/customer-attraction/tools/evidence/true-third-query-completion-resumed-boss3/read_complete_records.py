"""Complete B6 structural/source reading; no legacy imports, LP or pricing."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import ast,hashlib,json,math
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
PREFIX='research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/maxroot'
SRC=HERE/'original'/PREFIX
POINT=REPO/'archives/customer-attraction/tools/evidence/five-root-parent-audits-primary/source-root/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/exact_current_source_own_index_v1.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def consume(x,c):
    c[type(x).__name__]=c.get(type(x).__name__,0)+1
    if isinstance(x,dict):
        for k,v in x.items():consume(k,c);consume(v,c)
    elif isinstance(x,list):
        for v in x:consume(v,c)
    elif isinstance(x,float):assert math.isfinite(x)
def atom(a):
    assert len(a['bits'])==10 and set(a['bits'])<=set('01')
    assert len(a['max_bits'])==5 and set(a['max_bits'])<=set('01')
    dd=[]
    for field,k in [('AB_hist',8),('AE_hist',8),('second_hist',16)]:
        h=a[field];assert len(h)==k and all(type(n)==int and n>=0 for n in h) and sum(h)==5
        dd.append(sum(h[k//2:]))
    assert len(set(dd))==1 and len(a['menus_lh'])==3
    for p in a['menus_lh']:assert len(p)==2 and all(type(v)==int and 0<=v<=5 for v in p)
    if 'exact_mass'in a:assert F(a['exact_mass'])>=0
def run():
    m=json.loads((HERE/'source-manifest.json').read_text());out=[];reports={}
    for r in m:
        p=HERE/'original'/r['path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
        z=dict(id=r['id'],name=p.name,bytes=r['size'],sha256=r['sha256'])
        if p.suffix=='.py':ast.parse(p.read_text());z['syntax']='AST parsed, not imported'
        if p.suffix=='.json':
            x=json.loads(p.read_text());cc={};consume(x,cc);z.update(top_fields=list(x),all_nodes_consumed=cc)
            if 'row_names'in x:
                assert len(x['row_names'])==len(set(x['row_names'])) and len(x['atoms'])==len(x['primal_float'])
                for a in x['atoms']:atom(a)
                assert set(x['dual_multipliers_float'])<=set(x['row_names'])
                assert min(x['dual_multipliers_float'].values())>=0
                code=SRC/(p.stem.replace('_discovery','_pricing')+'.py')
                if p.name=='trueH_payment_fullpricing.json':
                    code=REPO/'archives/customer-attraction/tools/evidence/maxroot-related-hinges-resumed-boss3/original'/PREFIX/'price_indexed_hinges.py'
                rep=dict(rows=len(x['row_names']),saved_atoms=len(x['atoms']),positive_float_masses=sum(v>1e-9 for v in x['primal_float']),
                         float_mass_min=min(x['primal_float']),dual_beta_float=x['dual_beta_float'],dual_nonzero=len(x['dual_multipliers_float']),
                         inherited_exact_mass_fields=sum('exact_mass'in a for a in x['atoms']),
                         recorded_code_sha256=x['code_sha256'],current_emitter_path=str(code.relative_to(REPO)),
                         current_emitter_sha256=sha(code),code_sha_matches=x['code_sha256']==sha(code),
                         row_prefix_counts=dict(Counter(':'.join(n.split(':')[:2]) for n in x['row_names'])))
                if 'minimum_slack_float'in x:rep['minimum_slack_float']=x['minimum_slack_float']
                if 'history'in x:
                    rep['history']=x['history'];summary=[]
                    for h in x['history']:
                        s=h['state_reports']
                        if s:assert sorted(v['maximum_state'] for v in s)==list(range(32))
                        summary.append(dict(iteration=h['iteration'],restricted_beta=h['restricted_beta'],new_columns=h['new_columns'],
                                            state_records=len(s),negative_states=sum(v['minimum_scaled_residual']<0 for v in s),
                                            minimum=min((v['minimum_scaled_residual'] for v in s),default=None),
                                            maximum=max((v['minimum_scaled_residual'] for v in s),default=None)))
                    rep['history_summary']=summary
                reports[p.name]=rep
            else:
                assert p.name=='mixed_optimal_query_separation.json' and len(x['reports'])==4
                assert x['source_sha256']==sha(POINT)
                assert x['negative_rows']==[] and x['negative_count']==0 and x['checked_mixed_rows']==240
                for rec in x['reports']:
                    assert len(rec['query_classes'])==23 and len(rec['rows'])==rec['checked_rows']==60
                    vals=[F(v['exact_slack']) for v in rec['rows']]
                    assert min(vals)==F(rec['minimum_exact_slack'])>0
                z['exact_rows_consumed']=240
        out.append(z)
    assert len(m)==11 and sum(r['size'] for r in m)==2259198
    x=json.loads(POINT.read_text());count={};consume(x,count)
    for a in x['atoms']:atom(a);assert F(a['exact_mass'])>0
    assert len(x['atoms'])==63
    result=dict(status='PASS_COMPLETE_B6_FIELDS_AND_INPUT_BINDINGS',sources=out,discovery_reports=reports,
                mixed_input=dict(path=str(POINT.relative_to(REPO)),sha256=sha(POINT),bytes=POINT.stat().st_size,
                                 all_nodes_consumed=count,all_top_fields=list(x),atoms=63,
                                 upstream_source_sha256=x['source_sha256'],source_rows_metadata=x['source_rows'],
                                 boundary='No new audit of the 6750 source rows, actual OPT or full SPE'))
    (HERE/'complete-record-consumption.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'sources':len(m),'input_atoms':63,'history':reports['trueH_payment_fullpricing.json']['history_summary']},indent=2))
if __name__=='__main__':run()
