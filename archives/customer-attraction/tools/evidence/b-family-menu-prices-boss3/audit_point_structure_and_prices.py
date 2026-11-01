"""Independent standard-library audit of every saved column and 28 new price rows.

This does not reconstruct the inherited 5664 rows. Their separate check uses
the original matrix builder and is reported as a same-implementation replay.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
BASE='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1'
SCHEMAS={
'K':('kind','weight'),
'hist':('kind','actual_bits','d','hist','weight'),
'joint-reply':('kind','hist_column_old','group','state','weight'),
'overlap':('kind','hist_column','groups','weight'),
'actual-B-family-state':('kind','source','hist_column','hidden','ell','weight'),
'maximum-root-family-state':('kind','hist_column','M','hidden','ell','weight')}
def metadata(c):return {k:v for k,v in c.items() if k!='weight'}
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: audit_point_structure_and_prices.py /absolute/prepared-runtime')
    runtime=Path(sys.argv[1])
    point=HERE/'original/research_2/all_menu_prices_exact.json'
    report=json.loads(point.read_text());cols=report['columns']
    assert set(report)=={'scope','base_rows','first_raw_rows','additional_index_class_rows','O','W','strict_half_gap','verified_rows','minimum_slack','positive_columns','columns'}
    assert len(cols)==4849 and (report['base_rows'],report['first_raw_rows'],report['additional_index_class_rows'])==(702,37,100)
    weights=[F(c['weight']) for c in cols]
    assert min(weights)>=0 and sum(v>0 for v in weights)==report['positive_columns']==261
    for c in cols:assert tuple(c)==SCHEMAS[c['kind']]
    kinds=Counter(c['kind'] for c in cols)
    assert kinds==Counter({'K':1,'hist':16,'joint-reply':582,'overlap':1306,'actual-B-family-state':896,'maximum-root-family-state':2048})
    oldfile=runtime/BASE/'research_5/combined_branch_master_exact.json'
    old=json.loads(oldfile.read_text())['columns']
    assert len(old)==1905
    assert all(metadata(x)==metadata(y) for x,y in zip(cols[:1905],old))
    hist={i:c for i,c in enumerate(cols) if c['kind']=='hist'}
    PAT=list(product(range(2),repeat=3))
    for i,c in hist.items():
        assert len(c['actual_bits'])==6 and set(c['actual_bits'])<=set('01')
        assert len(c['hist'])==8 and all(isinstance(x,int) and x>=0 for x in c['hist']) and sum(c['hist'])==6
        assert c['d']==sum(n*w[0] for n,w in zip(c['hist'],PAT))
    O=sum(weights[i]*int(c['d']>0) for i,c in hist.items())
    W=sum(weights[i]*int('1' in c['actual_bits']) for i,c in hist.items())
    assert O==F(report['O'])==1 and W==F(report['W'])
    assert O-2*W==F(report['strict_half_gap'])>0
    K=weights[0];assert cols[0]['kind']=='K'
    expected=[]
    for source in (2,3,4):
        for hj in hist:
            for hidden in product(range(2),repeat=6-source):
                for ell in (0,6):expected.append({'kind':'actual-B-family-state','source':source,'hist_column':hj,'hidden':list(hidden),'ell':ell})
    for hj in hist:
        for m in (0,1):
            for hidden in product(range(2),repeat=5):
                for ell in (0,6):expected.append({'kind':'maximum-root-family-state','hist_column':hj,'M':m,'hidden':list(hidden),'ell':ell})
    assert len(expected)==2944
    assert [metadata(c) for c in cols[1905:]]==expected
    families=defaultdict(list)
    for j,c in enumerate(cols):
        if c['kind']=='actual-B-family-state':families['actual-B-'+str(c['source'])].append(j)
        elif c['kind']=='maximum-root-family-state':families['maximum-M-root'].append(j)
    marginals=[];prices=[]
    for name,js in families.items():
        for hj in hist:
            actual=sum((weights[j] for j in js if cols[j]['hist_column']==hj),F())
            assert actual==weights[hj]
            marginals.append({'family':name,'hist_column':hj,'sum':str(actual),'hist_mass':str(weights[hj]),'difference':'0'})
        for pos in range(6):
            val=F()
            for j in js:
                c=cols[j];a=tuple(map(int,hist[c['hist_column']]['actual_bits']))
                u=F(a[pos],sum(a)) if a[pos] else F()
                val+=weights[j]*(u-F(c['ell'],6*(6-pos+sum(a[:pos]))))
            assert val>=0,(name,pos,val)
            prices.append({'family':name,'row':'actual-menu-price:'+str(pos+1),'slack':str(val)})
        cap=K-sum((weights[j]*F(cols[j]['ell'],6) for j in js),F())
        assert cap>=0
        prices.append({'family':name,'row':'menu-CAP','slack':str(cap)})
    rootmass=sum((weights[j]*cols[j]['M'] for j in families['maximum-M-root']),F())
    assert rootmass==K
    assert len(marginals)==64 and len(prices)==28
    themecaps=[]
    for pos in range(6):
        size=sum((weights[hj]*int(c['actual_bits'][pos]) for hj,c in hist.items()),F())
        assert K>=size
        themecaps.append({'actual_position':pos+1,'size':str(size),'K_minus_size':str(K-size)})
    summary={'status':'all saved columns parsed; full metadata matched; exact independent 28-row checks passed',
      'input_sha256':hashlib.sha256(point.read_bytes()).hexdigest(),
      'all_top_level_fields_consumed':True,'all_column_metadata_fields_consumed':True,
      'column_count':len(cols),'kind_counts':dict(kinds),
      'positive_kind_counts':dict(Counter(c['kind'] for c,v in zip(cols,weights) if v>0)),
      'hist_support_count':len(hist),'positive_hist_support_count':sum(weights[h]>0 for h in hist),
      'old1905_metadata_matched':True,'new2944_metadata_matched':True,
      'minimum_weight':str(min(weights)),'positive_columns':sum(v>0 for v in weights),
      'O':str(O),'W':str(W),'strict_half_gap_O_minus_2W':str(O-2*W),
      'K':str(K),'maximum_root_M_mass':str(rootmass),
      'hist_masses':[dict(column=i,weight=str(weights[i]),actual_bits=c['actual_bits'],d=c['d'],hist=c['hist']) for i,c in hist.items()],
      'conditional_marginals':marginals,'new_menu_price_rows':prices,'actual_theme_capacity_checks':themecaps,
      'header_only_until_separate_original_matrix_check':{k:report[k] for k in ('verified_rows','minimum_slack')},
      'limits':'Independent metadata, masses, marginals, K identity, O/W and specified 28 rows only; inherited 5664 rows require separate original-builder replay; no full SPE or universal half result'}
    target=HERE/'replay/structure-and-prices-audit.json';target.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('hist_masses','conditional_marginals','new_menu_price_rows','actual_theme_capacity_checks')},ensure_ascii=False))
if __name__=='__main__':main()
