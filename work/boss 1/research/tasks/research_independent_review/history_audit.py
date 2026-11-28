"""Check the published comparison cases from the original JST data, without importing either author's code."""
import hashlib
import json
import math
from pathlib import Path
import pandas as pd

HERE=Path(__file__).resolve().parent
W=HERE.parents[2]
ROOT=HERE.parents[4]
HIST=W/'research/tasks/history_framework_review'


def path(data, t):
    period=data.loc[t:t+10]
    a,b=period.iloc[0],period.iloc[-1]
    price=b.hpnom/a.hpnom
    cpi=b.cpi/a.cpi
    total=period.iloc[1:].eq_tr
    return {
        'nominal_home':100*(price-1), 'real_home':100*(price/cpi-1),
        'nominal_wages':100*(b.wage/a.wage-1), 'real_gdp_pc':100*(b.rgdpmad/a.rgdpmad-1),
        'real_local_equities':100*(math.prod(1+x for x in total)/cpi-1) if total.notna().all() else None,
        'onsets':[int(y-t) for y,v in period.crisisJST.items() if v==1],
    }


def main():
    f=ROOT/'research/models/jst_example/JSTdatasetR6.dta'
    raw=pd.read_stata(f, convert_categoricals=False)
    frames={iso:q.set_index('year').sort_index() for iso,q in raw.groupby('iso')}
    cases={}
    for iso, start, end in [('JPN',1988,1993),('USA',2003,2008)]:
        y=int(frames[iso].loc[start:end,'hpnom'].idxmax())
        cases[iso]={'peak':y,**path(frames[iso],y)}
    baseline=pd.read_csv(HIST/'named_paths.csv')
    for iso,q in cases.items():
        z=baseline[(baseline.country==iso)&(baseline.years_since_peak==10)].iloc[0]
        for our,their in [('nominal_home','nominal_home_proxy_pct'),('real_home','real_home_proxy_pct'),
                          ('nominal_wages','nominal_wage_index_pct'),('real_gdp_pc','real_gdp_per_person_pct'),
                          ('real_local_equities','equity_total_local_real_pct')]:
            assert abs(q[our]-z[their])<1e-7
    samples={}
    original_scan=pd.read_csv(HIST/'event_scan.csv')
    for hurdle in [5,10,15]:
        episodes=[]
        for iso,q in frames.items():
            last=None
            for t in range(1970,2011):
                if last is not None and t-last<10: continue
                pre=q.loc[t-3:t+3,'hpnom']
                p=q.loc[t-3:t+10,'hpnom']
                y=q.loc[t:t+10,'crisisJST']
                if len(p)!=14 or p.isna().any() or len(y)!=11 or y.isna().any():continue
                if not all(pre[t]>v for j,v in pre.items() if j!=t):continue
                if (1-q.loc[t+1:t+5,'hpnom'].min()/pre[t])*100 < hurdle:continue
                last=t
                episodes.append((iso,t,path(q,t)))
        expected=original_scan[original_scan.drop_filter_pct==hurdle]
        assert {(a,b) for a,b,_ in episodes}==set(zip(expected.country,expected.peak_year))
        eq=[e['real_local_equities'] for _,_,e in episodes if e['real_local_equities'] is not None]
        samples[hurdle]={'windows':len(episodes),'countries':len({a for a,_,_ in episodes}),
            'real_home_negative':sum(int(e['real_home']<0) for _,_,e in episodes),
            'nominal_home_negative':sum(int(e['nominal_home']<0) for _,_,e in episodes),
            'equity_observed':len(eq),'equity_negative':sum(int(a<0) for a in eq),
            'any_onset':sum(bool(e['onsets']) for _,_,e in episodes),
            'year_six':[(a,b) for a,b,e in episodes if 6 in e['onsets']]}
    # Give balance-sheet stocks base-year GDP=100, deliberately avoiding the author's ratio formula.
    setser=[]
    for g in [3,4]:
        beginning_gdp=100; ending_gdp=beginning_gdp+g
        borrowed=ending_gdp*.03
        setser.append({'current_nominal_growth_pct':g,'initial_debt':30,'deficit':borrowed,
            'nominal_ending_debt':30+borrowed,'ending_ratio_pct':100*(30+borrowed)/ending_gdp,
            'stabilizing_total_deficit_pct':100*((.30*ending_gdp)-30)/ending_gdp})
    # Exact values transcribed from the original reports, not from the study's summary CSV.
    r_cny=[-13.43,12.71,-29.35,39.48,31.48,1.38,-20.63,-9.87,14.85,24.39]
    r_usd=[-18.97,20.47,-32.85,37.76,40.29,4.19,-27.09,-11.46,11.91,30.26]
    cpi=114.8925/100.6000*1.008
    nominal=math.prod(1+x/100 for x in r_cny)
    adjusted=nominal/cpi
    out=dict(raw_jst_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),named=cases,ex_post_screen=samples,
        setser=setser,korea_gdp_two_year_factor=(1-.067)*(1+.109),china_2015_static_interest_saving_100m=32000*(.10-.035),
        china_2016_new_property_sales_change_pct=100*(157349/128495-1),china_2016_completed_unsold_change_pct=100*(69539/71853-1),
        equity={'calendar_years':'2016–2025','cny_net_annual_percent':r_cny,'usd_gross_annual_percent':r_usd,
                'msci_cny_source':'https://www.msci.com/documents/10199/255599/msci-china-a-onshore-index-cny-net.pdf',
                'msci_usd_source':'https://www.msci.com/documents/10199/dee20d77-051f-45d9-af6a-80f2b9911147',
                'oecd_price_source':'https://fred.stlouisfed.org/data/CHNCPIALLMINMEI',
                'nbs_2025_dec_source':'https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202601/t20260119_1962330.html',
                'usd_gross_nominal_factor':math.prod(1+x/100 for x in r_usd),'cny_net_nominal_factor':nominal,
                'domestic_price_factor':cpi,'cny_net_real_factor':adjusted,'cny_real_annualized_pct':100*(adjusted**.1-1),
                'limits':'Year-end index versus December monthly average CPI. Published dividend withholding convention does not reproduce all personal costs.'})
    (HERE/'independent_history.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
