"""Compare all metadata and exact weights of the two saved 4849-column points."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json
HERE=Path(__file__).resolve().parent
def main():
    old=json.loads((HERE/'original/research_2/maxroot_identity_exact.json').read_text())
    new=json.loads((HERE/'original/research_2/all_menu_prices_exact.json').read_text())
    assert len(old['columns'])==len(new['columns'])==4849
    metadata=lambda c:{k:v for k,v in c.items() if k!='weight'}
    assert all(metadata(a)==metadata(b) for a,b in zip(old['columns'],new['columns']))
    changes=[{'column':i,'kind':a['kind'],'old_weight':a['weight'],'new_weight':b['weight']} for i,(a,b) in enumerate(zip(old['columns'],new['columns'])) if F(a['weight'])!=F(b['weight'])]
    counts=Counter(c['kind'] for c in changes)
    assert len(changes)==214 and counts=={'joint-reply':70,'overlap':52,'actual-B-family-state':52,'maximum-root-family-state':40}
    assert old['W']==new['W']
    assert all(a['weight']==b['weight'] for a,b in zip(old['columns'],new['columns']) if a['kind'] in ('K','hist'))
    oa=json.loads((HERE/'replay/maxroot-structure-and-prices-audit.json').read_text())
    na=json.loads((HERE/'replay/structure-and-prices-audit.json').read_text())
    negative=[c for c in oa['new_menu_price_rows'] if F(c['slack'])<0]
    assert len(negative)==1 and negative[0]['family']=='actual-B-2' and negative[0]['row']=='actual-menu-price:6'
    matches=[c for c in na['new_menu_price_rows'] if c['family']==negative[0]['family'] and c['row']==negative[0]['row']]
    assert len(matches)==1 and F(matches[0]['slack'])==0
    assert all(F(c['slack'])>=0 for c in na['new_menu_price_rows'])
    out={'metadata_identical_all_4849':True,'changed_weight_count':len(changes),'changed_weights_by_kind':dict(counts),'changed_columns':changes,'W_identical':True,'K_and_all_hist_weights_identical':True,'old_root_new_price_violations':negative,'same_price_on_completed_point':matches[0],'old_root_new_price_negative_count':1,'new_point_new_price_negative_count':0,'old_author_reported_rows':old['verified_rows'],'new_original_builder_verified_rows':new['verified_rows'],'old_positive_columns':old['positive_columns'],'new_positive_columns':new['positive_columns'],'changed_top_level_noncolumn_fields':{k:{'old':old[k],'new':new[k]} for k in old if k!='columns' and old[k]!=new[k]},'limits':'No rerun of the previous 5664-row entrypoint; its old author report remains distinct from the new 5692-row replay; all 28 new rows evaluated exactly on both points.'}
    (HERE/'replay/point-comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='changed_columns'},ensure_ascii=False))
if __name__=='__main__':main()
