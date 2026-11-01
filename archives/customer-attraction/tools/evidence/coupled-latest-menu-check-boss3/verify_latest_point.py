"""Rebuild a frozen matrix once; verify all saved coordinates and named slacks.

This is an exact replay of the original row builder, with additional interface
checks. It is not an independent row implementation or a complete SPE checker.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import importlib,json,sys,time,hashlib


def main():
    if len(sys.argv)!=4:raise SystemExit('usage: verify_fixed_point.py RUNTIME_ROOT latest NEW_OUTPUT_DIR')
    root=Path(sys.argv[1]).resolve();mode=sys.argv[2];out=Path(sys.argv[3]).resolve();out.mkdir(parents=True,exist_ok=False)
    assert mode=='latest'
    local=root/'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
    module='coupled_latest_master'
    point='coupled_latest_exact.json'
    raw=(local/point).read_bytes();saved=json.loads(raw);sys.path.insert(0,str(local));sys.argv=[str(local/(module+'.py'))]
    start=time.monotonic();mod=importlib.import_module(module);cols,names,m,obj,norm=mod.build();built=time.monotonic()-start
    print(json.dumps({'event':'built','mode':mode,'rows':len(m),'columns':len(cols),'seconds':built}),flush=True)
    values=[F(c['weight']) for c in saved['columns']]
    assert len(cols)==len(values) and len(names)==len(m)==saved['verified_rows']
    assert all(len(r)==len(cols) for r in m) and len(obj)==len(norm)==len(cols)
    # The original writer JSON-serializes nested tuple group labels as arrays.
    # Normalize precisely that serialization representation before identity checks.
    canonical_cols=json.loads(json.dumps(cols))
    descriptor_mismatches=[i for i,(c,s) in enumerate(zip(canonical_cols,saved['columns'])) if c!={k:v for k,v in s.items() if k!='weight'}]
    assert not descriptor_mismatches,descriptor_mismatches[:10]
    assert min(values)>=0 and sum(v>0 for v in values)==saved['positive_columns']
    normal=sum(x*y for x,y in zip(norm,values));W=sum(x*y for x,y in zip(obj,values))
    assert normal==F(saved['O'])==1 and W==F(saved['W'])<F(1,2)
    assert F(saved['strict_half_gap'])==1-2*W
    nonzero=[(i,v) for i,v in enumerate(values) if v]
    slacks=[sum((row[j]*v for j,v in nonzero),F()) for row in m]
    assert min(slacks)>=0 and min(slacks)==F(saved['minimum_slack'])
    allrows=[{'row_index':i,'name':str(n),'slack':str(v)} for i,(n,v) in enumerate(zip(names,slacks))]
    (out/'all-row-slacks.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2)+'\n')
    kinds=Counter(c['kind'] for c in cols);positive=Counter(c['kind'] for c,v in zip(cols,values) if v)
    histogram=[]
    for j,c in enumerate(cols):
        if c['kind']!='hist':continue
        assert len(c['actual_bits'])==6 and set(c['actual_bits'])<=set('01') and len(c['hist'])==8
        assert all(isinstance(v,int) and v>=0 for v in c['hist']) and sum(c['hist'])==6
        assert sum(c['hist'][4:])==c['d']
        h={'column':j,'actual_bits':c['actual_bits'],'d':c['d'],'hist':c['hist'],'mass':str(values[j]),'conditional_masses':{}}
        sources=[4] if mode=='latest' else [2,3,4]
        for source in sources:
            indices=[k for k,z in enumerate(cols) if z.get('hist_column')==j and (z['kind']=='actual-B-branch-state' or z['kind']=='actual-B-family-state' and z['source']==source)]
            assert len(indices)==2**(7-source)
            total=sum((values[k] for k in indices),F());assert total==values[j]
            h['conditional_masses'][str(source)]=str(total)
        histogram.append(h)
    # Evaluate the seven universally valid ordinary prices for each recorded Y-menu.
    # These rows are deliberately NOT counted among the saved matrix's constraints.
    actual=[F() for _ in range(6)]
    for h in histogram:
        a=list(map(int,h['actual_bits']));z=sum(a)
        for i in range(6):actual[i]+=F(h['mass'])*F(a[i],z) if a[i] else F()
    prices=[]
    for source in ([4] if mode=='latest' else [2,3,4]):
        query=[F() for _ in range(6)];mean_size=F()
        for c,v in zip(cols,values):
            if c['kind'] not in ('actual-B-branch-state','actual-B-family-state'):continue
            if c['kind']=='actual-B-family-state' and c['source']!=source:continue
            a=list(map(int,cols[c['hist_column']]['actual_bits']));ell=c['ell'];assert ell in (0,6)
            mean_size+=v*F(ell,6)
            for i in range(6):query[i]+=v*F(ell,6*(sum(a[:i])+6-i))
        prices.append({'source':source,'actual_payoffs':list(map(str,actual)),'Y_query_values':list(map(str,query)),'six_actual_price_slacks':[str(u-q) for u,q in zip(actual,query)],'capacity_slack':str(values[0]-mean_size),'mean_Y_size':str(mean_size)})
    newgroups=defaultdict(list)
    for n,v in zip(names,slacks):
        if str(n).startswith('actualB'):newgroups[str(n).split(':')[0]].append(v)
    summary={'status':'all_saved_matrix_rows_exactly_nonnegative','mode':mode,'source_point_sha256':hashlib.sha256(raw).hexdigest(),'rows':len(m),'columns':len(cols),'column_kinds':dict(kinds),'positive_columns':len(nonzero),'positive_by_kind':dict(positive),'all_saved_column_descriptors_equal_builder_after_JSON_tuple_array_normalization':True,'all_column_and_row_lengths_checked':True,'normalization':str(normal),'W':str(W),'W_float':float(W),'strict_half_gap_one_minus_two_W':str(1-2*W),'K':str(values[0]),'minimum_slack':str(min(slacks)),'zero_slacks':sum(v==0 for v in slacks),'new_row_groups':{k:{'rows':len(v),'minimum_slack':str(min(v)),'zero_slacks':sum(x==0 for x in v)} for k,v in newgroups.items()},'ordinary_Y_menu_prices_not_in_saved_matrix':prices,'build_seconds':built,'total_seconds':time.monotonic()-start,'row_builder_invocations':1,'original_main_or_verify_invocations':0,'linprog_or_SPE_solver_invocations':0,'scope':'Frozen necessary-condition matrix and all saved coordinates only; no exact LP optimum or complete SPE claim.'}
    (out/'histogram-marginals.json').write_text(json.dumps(histogram,ensure_ascii=False,indent=2)+'\n')
    old=json.loads((local.parent/'research_2/coupled_B_master_exact.json').read_text());oldcols=old['columns']
    assert len(oldcols)==len(cols) and all({k:v for k,v in x.items() if k!='weight'}=={k:v for k,v in y.items() if k!='weight'} for x,y in zip(oldcols,saved['columns']))
    summary['comparison_to_5259']={'all_2033_descriptors_same':True,'W_exactly_same':old['W']==saved['W'],'K_same':oldcols[0]['weight']==saved['columns'][0]['weight'],'different_weight_count':sum(F(x['weight'])!=F(y['weight']) for x,y in zip(oldcols,saved['columns'])),'different_weight_by_kind':dict(Counter(x['kind'] for x,y in zip(oldcols,saved['columns']) if F(x['weight'])!=F(y['weight']))),'5259_positive_columns':old['positive_columns'],'5277_positive_columns':saved['positive_columns']}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
