"""Build explicitly retrospective Chinese panels from preserved public data.

GDP is single-quarter real YoY. Two archived official vintages are retained,
including their overlap; no cumulative nominal GDP transformation is used.
The replay input is the extracted numeric table, not a copyrighted full page.
"""
from pathlib import Path
import hashlib
import io
import json
import re
import pandas as pd

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
DATA = W / 'research/data'

def extract(key, vintage, source, filename):
    path = DATA / filename
    if not path.exists():
        raw = (W / 'cache' / key / 'raw.bin').read_bytes()
        table = pd.read_html(io.StringIO(raw.decode('utf-8')))[1]
        rows = []
        for _, row in table.iterrows():
            if re.fullmatch(r'20\d\d', str(row.iloc[0])):
                for q in range(1, 5):
                    if pd.notna(row.iloc[q]):
                        rows.append({'quarter':f'{row.iloc[0]}Q{q}', 'real_gdp_yoy':float(row.iloc[q]),
                                     'vintage':vintage, 'source_url':source, 'source_table':'Table 2',
                                     'raw_sha256':hashlib.sha256(raw).hexdigest()})
        pd.DataFrame(rows).to_csv(path,index=False)
    return pd.read_csv(path)

def main():
    old = extract('d6e8c24d7b930ad4a46c','2022-01-18',
        'https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1901345.html','gdp_quarterly_2022vintage.csv')
    new = extract('dba214a76634608df8aa','2026-10-20',
        'https://www.stats.gov.cn/sj/zxfb/202610/t20261020_1965658.html','gdp_quarterly_2026vintage.csv')
    overlap = old.merge(new,on='quarter',suffixes=('_old','_new'))
    overlap['revision_pp'] = overlap.real_gdp_yoy_new-overlap.real_gdp_yoy_old
    overlap.to_csv(DATA/'gdp_vintage_overlap.csv',index=False)
    gdp = pd.concat([old[old.quarter<'2021Q1'],new]).set_index('quarter').sort_index()
    pmi = pd.read_csv(DATA/'macro_china_pmi.csv')
    pmi.index = pd.PeriodIndex([f'{int(y):04d}-{int(m):02d}' for y,m in
        pmi['月份'].str.extract(r'(\d{4})年(\d{2})月').itertuples(index=False,name=None)],freq='M')
    pmi=pmi.sort_index()
    for suffix,start in [('long','2016-01'),('same_vintage','2021-01')]:
        idx=pd.period_range(start,'2026-09',freq='M')
        x=pmi.reindex(idx)
        if x[['制造业-指数','非制造业-指数']].isna().any().any():
            raise ValueError('Missing monthly PMI: do not fill with invented values')
        qs=pd.period_range(pd.Period(start,'M').asfreq('Q'),'2026Q3',freq='Q')
        y=gdp.loc[[str(q) for q in qs],'real_gdp_yoy'].tolist()
        panel={'input_kind':'observed_china_retrospective_panel',
            'information_mode':'retrospective_revised_spliced' if suffix=='long' else 'retrospective_single_GDP_vintage',
            'monthly_periods':[str(t) for t in idx],
            'monthly':{'manufacturing_pmi':x['制造业-指数'].astype(float).tolist(),
                       'nonmanufacturing_pmi':x['非制造业-指数'].astype(float).tolist()},
            'quarterly_periods':[str(q) for q in qs], 'quarterly_gdp':y,
            'target_definition':'NBS single-quarter real GDP year-on-year percentage change',
            'units':{'manufacturing_pmi':'diffusion index','nonmanufacturing_pmi':'business activity diffusion index','gdp':'percent YoY'},
            'vintage_limit':'No original-release monthly vintage history; not pseudo-real-time forecasting validation'}
        (HERE/f'panel_{suffix}.json').write_text(json.dumps(panel,ensure_ascii=False,indent=2)+'\n')
    files=['macro_china_pmi.csv','gdp_quarterly_2022vintage.csv','gdp_quarterly_2026vintage.csv','gdp_vintage_overlap.csv']
    manifest={'input_kind':'observed_publication_tables','files':{f:hashlib.sha256((DATA/f).read_bytes()).hexdigest() for f in files},
        'target_rows':len(gdp),'monthly_rows':129,'overlap_revisions':overlap[['quarter','revision_pp']].to_dict('records'),
        'monthly_vintage':'2026-11-27 client date retrieval; first releases not available',
        'GDP_splice':'2016-2020 old release, 2021-2026 newer release; sensitivity uses2021 onward only',
        'availability_error_caught':'AKShare industrial 发布时间 is observation-month start, not actual release date; excluded from forecast availability claims'}
    (HERE/'data_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
