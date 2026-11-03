"""Consume all B5 fields and records without solver, pricing or SPE replay."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import ast, hashlib, json, math
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
PREFIX='research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/maxroot'
SRC=HERE/'original'/PREFIX
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
    ds=[]
    for field,n in [('AB_hist',8),('AE_hist',8),('second_hist',16)]:
        h=a[field]
        assert len(h)==n and all(type(v)==int and v>=0 for v in h) and sum(h)==5
        ds.append(sum(h[n//2:]))
    assert len(set(ds))==1 and len(a['menus_lh'])==3
    for pair in a['menus_lh']:assert len(pair)==2 and all(type(z)==int and 0<=z<=5 for z in pair)
    if 'exact_mass'in a:assert F(a['exact_mass'])>=0
def endpoints(k):
    L=4*(k-1)
    return sorted({F(0),F(L-1)}|{F(L-1)-F((k-1)*d,5*(p+1))
                  for p in range(6-k) for d in range(6)
                  if F(L-1)-F((k-1)*d,5*(p+1))>=0})
def run():
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    sources=[];reports={}
    for r in manifest:
        p=HERE/'original'/r['path']
        assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
        z=dict(id=r['id'],name=p.name,bytes=r['size'],sha256=r['sha256'])
        if p.suffix=='.py':ast.parse(p.read_text());z['syntax']='AST parsed, not executed'
        if p.suffix=='.json':
            x=json.loads(p.read_text());c={};consume(x,c);z.update(all_nodes_consumed=c,top_fields=list(x))
            if 'row_names'in x:
                assert len(x['row_names'])==len(set(x['row_names']))
                assert len(x['atoms'])==len(x['primal_float'])
                for a in x['atoms']:atom(a)
                assert set(x['dual_multipliers_float'])<=set(x['row_names'])
                assert all(v>=0 for v in x['dual_multipliers_float'].values())
                py=SRC/(p.stem.replace('_discovery','_pricing')+'.py')
                if p.name=='indexed_hinge_fullpricing.json':py=SRC/'price_indexed_hinges.py'
                report=dict(rows=len(x['row_names']),atoms=len(x['atoms']),
                            float_mass_min=min(x['primal_float']),positive_float_masses=sum(v>1e-9 for v in x['primal_float']),
                            inherited_exact_mass_fields=sum('exact_mass'in a for a in x['atoms']),
                            dual_beta_float=x['dual_beta_float'],dual_nonzero=len(x['dual_multipliers_float']),
                            hinge_rows={s:sum((':'+s+':')in n for n in x['row_names'])
                                        for s in ['MaxHinge','OtherMaxHinge','OldHinge','IndexedHinge']},
                            row_prefix_counts=dict(Counter(':'.join(n.split(':')[:2]) for n in x['row_names'])),
                            recorded_code_sha256=x['code_sha256'],current_frozen_code=py.name,
                            current_frozen_code_sha256=sha(py),code_sha_matches=x['code_sha256']==sha(py))
                if 'minimum_slack_float'in x:report['recorded_minimum_slack_float']=x['minimum_slack_float']
                if 'history'in x:
                    report['history']=x['history']
                    for h in x['history']:
                        if h.get('state_reports'):
                            states=h['state_reports'];assert sorted(t['maximum_state'] for t in states)==list(range(32))
                            assert all(t['minimum_scaled_residual']<0 for t in states)
                reports[p.name]=report
            elif p.name=='exact_template_obstruction.json':
                for a in x['atoms']:
                    assert len(a['bits'])==10 and set(a['bits'])<={0,1} and 0<=a['d']<=5 and F(a['mass'])>0
                assert len(x['slacks'])==240 and len(x['old234_slacks'])==234
                assert min(map(F,x['slacks'].values()))==min(map(F,x['old234_slacks'].values()))==0
                z['all_exact_slacks_parsed']=474
            elif p.name=='audit_hinge_algebra.json':
                for rr in x['families']:assert rr['breakpoints']==list(map(str,endpoints(rr['k'])))
        sources.append(z)
    assert len(sources)==23 and sum(r['bytes'] for r in sources)==1341838
    paths=list((REPO/'archives/customer-attraction/tools/evidence/five-root-parent-audits-primary').rglob('audit_actual_union_wallet.json'))
    assert len(paths)==1
    old=json.loads(paths[0].read_text());current=json.loads((SRC/'independent_audit.json').read_text())
    prior={tuple(r['actual'])+(r['query'],):F(r['residue']) for r in old['states']}
    now={tuple(r['bits']):F(r['residual']) for r in current['actual_payment']['residual_table']}
    assert prior==now and len(now)==64
    maxsrc=REPO/'archives/customer-attraction/tools/evidence/maxroot-gamma-shared-menu-primary/source-root/research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only/maxroot_envelope.json'
    assert sha(maxsrc)==current['source_sha256']
    out=dict(status='PASS_FULL_B5_FIELD_AND_RECORD_CONSUMPTION',sources=sources,discovery_reports=reports,
             wallet_all_64_records_match_mature=True,wallet_mature_report=str(paths[0].relative_to(REPO)),
             original_maxroot_source_sha_matches=True,
             boundary='inherited exact_mass is provenance, current report weights are primal_float; no LP, pricing, SPE or old 192/64 replay')
    (HERE/'frozen-record-consumption.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['sources','discovery_reports']},indent=2))
if __name__=='__main__':run()
