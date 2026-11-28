"""Independent public-statement/fiscal arithmetic, unit checks and compute-ledger integrity."""
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from statistics import mean
import subprocess
import xlrd

HERE=Path(__file__).resolve().parent
W=HERE.parents[2]
ROOT=HERE.parents[4]
BK=W/'research/tasks/bank_research'
PF=W/'research/tasks/property_fiscal'
OUTPUT=W/'compute/outputs'
D=lambda x: Decimal(str(x))


def obj(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def table(p):
    with p.open() as f:
        return list(csv.DictReader(f))


# Bank source currency units, then source-to-RMB-million scale. Where a separately
# billed P&L line uses 100-million yuan, the page locator below notes the conversion.
# ICBC H1 and both Lanzhou runs use amortized-cost-only charges. ICBC Q3 discloses
# combined customer loan impairment and only the net carrying value of loans.
HEAD=['assets','liabilities','book_equity','loan_principal','accrued_interest','ac_allowance','net_loans',
      'loan_charge','net_profit','capital_cet1','rwa']
ROWS={
    'icbc_h1':('BK005',1,[57070593,52714749,4355844,31992126,65947,895553,31162520,123031,176475,3940780,29832780],
               'PDF pages 14–15, 27, 73, 82, 119–123, 142–143, 199; units RMB million.'),
    'icbc_q3':('BK003',1,[57823437,53423272,4400165,32234230,None,None,31424817,150922,288278,3982891,30478278],
               'PDF pp. 5 (1,509.22 亿元), 8–10, 25–26 KM1 including 2027 footnote; RMB million in merged statements.'),
    'lanzhou_h1':('BK006',1000,[533101516,496643028,36458488,266203981,1927649,9068325,259063305,1996881,900714,30638408,350055742],
                  'PDF pp. 9, 11–13, 33–34, 42–46, 126; cited management/summary tables are RMB thousand.'),
    'lanzhou_q3':('BK004',1000,[534817002,497826453,36990549,256730389,2298470,8648952,250379907,2691809,1406671,31168341,353312649],
                  'PDF pp. 3–4, 6–8, 16–18; management table and consolidated statements use RMB thousand.'),
}


def banks():
    answer={}
    received={r['id']:r for r in table(BK/'statement_extract.csv')}
    sources={s['id']:s for s in obj(BK/'sources.json')}
    cases={'opening':(0,1,0),'one_year_charge_no_new_income':(1,1,0),'two_year_charges_no_new_income':(2,1,0),
           'one_year_charge_rwa_plus_5pct':(1,1.05,0),'one_year_charge_rwa_plus_5pct_with_income':(1,1.05,.5)}
    for name,(sid,scale,values,locator) in ROWS.items():
        r={k:(D(v)/scale if v is not None else None) for k,v in zip(HEAD,values)}
        assert all((D(received[name][k]) if received[name][k] else None)==v for k,v in r.items())
        orig=BK/'cache'/f'{name}.pdf'
        verified=None
        if orig.exists():
            assert sha(orig)==sources[sid]['sha256_original']
            txt=subprocess.run(['pdftotext','-layout',str(orig),'-'],check=True,capture_output=True).stdout.decode()
            # 2026 consolidated figures must actually occur in the frozen PDF, using source reporting units.
            for k,v in zip(HEAD,values):
                if v is None:continue
                special={('icbc_q3','loan_charge'):'1,509.22',('icbc_q3','loan_principal'):'322,342.30'}
                token=special.get((name,k), f'{v:,}')
                assert token in txt,(name,k,token)
            verified=True
        assert r['assets']-r['liabilities']==r['book_equity']
        if r['ac_allowance'] is not None:
            assert r['loan_principal']+r['accrued_interest']-r['ac_allowance']==r['net_loans']
        months=6 if name.endswith('h1') else 9
        floor=D('.095') if name.startswith('icbc') else D('.075')
        annual=r['loan_charge']*12/months
        reported={a['scenario']:a for a in obj(next(OUTPUT.glob('china-bank-'+name.replace('_','-')+'-*.json')))['result']['results']}
        bridge={a['case']:a for b in obj(BK/'capital_and_liquidity_results.json')['banks'] if b['bank']==name for a in b['cases']}
        independent={}
        for case,(m,rf,retain) in cases.items():
            equity=r['book_equity']-annual*m+r['net_profit']*D(retain)
            cet1=equity-(r['book_equity']-r['capital_cet1'])
            rwa=r['rwa']*D(rf)
            headroom=cet1-floor*rwa
            rep=reported[case]
            assert abs(equity-D(rep['ending_capital']))<D('1e-6')
            assert abs(D(rep['new_credit_loss_charged_to_capital'])-annual*m)<D('1e-6')
            assert abs(cet1/rwa*100-D(bridge[case]['cet1_ratio_percent']))<D('0.000001')
            assert abs(headroom-D(bridge[case]['cet1_headroom_signed']))<D('.000001')
            independent[case]={'book_equity_100m':float(equity/100),'cet1_100m':float(cet1/100),
                               'cet1_ratio_pct':float(100*cet1/rwa),'signed_headroom_100m':float(headroom/100)}
        answer[name]=dict(original_pdf_sha256=sources[sid]['sha256_original'],verified_pdf_bytes_and_values=verified,
                          source_url=sources[sid]['url'],locator=locator,source_field_names=HEAD,
                          source_line_values=values,reported_units_per_million=scale,annualized_charge_100m=float(annual/100),
                          reference_pct=float(100*floor), book_gap_vs_cet1_100m=float((r['book_equity']-r['capital_cet1'])/100),
                          observations_and_conditional_stresses=independent)
    # Other-public-bank cross-checks: ratio of average amounts is not the average daily ICBC LCR.
    answer['cross_checks']={
        'icbc_extra_50bp_requirement_100m':30478278*.005/100,
        'lanzhou_q3_illustrative_capital_gap_if_book_equity_wrongly_substituted_signed_100m':
            (36990.549-2691.809*4/3-353312.649*1.05*.075)/100,
        'lanzhou_q3_reserve_roll_forward_thousand':9493099+2691809-4441447+878463+27028,
        'lanzhou_q3_gross_observed_ratio_of_hqla_to_net_outflow':94960228/68712744,
        'icbc_q3_ratio_of_two_published_daily_averages_pct':100*12779219/9183235,
        'icbc_q3_published_mean_daily_ratio_pct':138.88,
        'icbc_h1_total_loan_charge_vs_ac_only_millions':[123016,123031],
        'lanzhou_q3_ac_charge_vs_oci_thousand':[2691809,537],
    }
    return answer


def regulatory():
    files={'BK001':'by_type.xls','BK002':'industry.xls','BK010':'1208455.xls','BK011':'1208453.xls',
           'BK012':'1164262.xls','BK013':'1164263.xls'}
    source={r['id']:r for r in obj(BK/'sources.json')}
    series=table(BK/'regulatory_series.csv')
    counts={}
    for sid,fn in files.items():
        disk=BK/'cache'/fn
        if not disk.is_file():continue
        assert sha(disk)==source[sid]['sha256_original']
        book=xlrd.open_workbook(disk);sheet=book.sheet_by_index(0)
        part=[r for r in series if r['source_id']==sid]
        for r in part:
            cell=r['cell'];data=sheet.cell_value(int(cell[1:])-1,ord(cell[0])-ord('A'))
            unit_scale=100 if r['unit']=='百分比' else 1
            assert abs(float(r['value'])-unit_scale*data)<1e-7
        counts[sid]={'numeric_cells_checked':len(part),'sha256':sha(disk)}
        if sid=='BK001':
            counts[sid]['Q3_NPL_rates_pct']={sheet.cell_value(2,c).replace('\n',''):100*sheet.cell_value(30,c) for c in range(2,8)}
        if sid=='BK002':
            counts[sid].update(q3_lcr_pct=sheet.cell_value(24,3)*100,q3_nsfr_pct=sheet.cell_value(25,3)*100,
                               note49='LCR/NSFR restricted by official attachment to commercial banks with assets of at least CNY 200 billion.')
            assert '2000亿元以上' in sheet.cell_value(48,0)
    return counts


def fiscals():
    keys=['land_receipts','land_related_outlay','local_funds_own_income','local_funds_outlay','local_general_own_income','local_general_outlay']
    previous=[24982,33752,30855,72328,104634,191098]
    current=[18526,27919,24566,65517,107635,191434]
    freeze={r['period']:r for r in table(PF/'fiscal_releases.csv')}
    for key,row in [('2025M10',previous),('2026M10',current)]:
        assert [int(freeze[key][v]) for v in keys]==row
    delta={k:b-a for k,a,b in zip(keys,previous,current)}
    figures={(r['indicator'],r['period']):float(r['value']) for r in table(PF/'supplemental.csv')}
    p=[32770,28243,4527,13337,48943]
    assert [figures[k,'2026M10'] for k in ['statutory_bond_principal_due','refinancing_for_matured_principal','other_funds_for_principal','interest_paid','all_refinancing_issues']]==p
    assert p[0]==p[1]+p[2]
    fu=[1043.61,886.60,1113.45];ga=[885.28,846.64,791.99]
    assert [figures['scheduled_principal',str(y)] for y in range(2026,2029)]==fu
    assert [figures['scheduled_principal_plus_interest',str(y)] for y in range(2026,2029)]==ga
    county_before=123059-75198-2350;county_after=63863-2536-2395
    cp=table(PF/'property_releases.csv'); prop={r['period']:r for r in cp}
    housing={k:100*(float(prop['2025'][k])/float(prop['2021'][k])-1) for k in ['sales_value','sales_area','starts_area','developer_funds']}
    cities=table(PF/'cities_price_202610.csv')
    for name in ('new','resale'):
        cut=[r for r in cities if r['market']==name];assert len({r['city'] for r in cut})==70
        housing[name]={'down':sum(float(r['yoy_index'])<100 for r in cut),'unweighted_yoy_pct':mean(float(r['yoy_index']) for r in cut)-100}
    return dict(mof_2025_2026_jan_oct_terms=keys,M10_2025=previous,M10_2026=current,unit='RMB 100m except where specified',
                delta_100m=delta,land_broad_balance_change_100m=delta['land_receipts']-delta['land_related_outlay'],
                distinct_own_source_receipts_change_100m=delta['local_general_own_income']+delta['local_funds_own_income'],
                principal_repayment_breakdown=p,rollover_share_pct=100*p[1]/p[0],interest_plus_other_sources_of_principal=p[2]+p[3],
                fujian_scheduled_principal_2026_27_28=fu,gansu_scheduled_principal_plus_interest_2026_27_28=ga,
                fujian_2027_2026_delta_pct=(fu[1]/fu[0]-1)*100,gansu_2027_2026_delta_pct=(ga[1]/ga[0]-1)*100,
                dingnan_gross_less_two_cost_lines_cny_10000=[county_before,county_after],
                housing=housing)


def ledger():
    ledger=obj(W/'compute/ledger.json')
    plans=['research/models/compute-initial.json','research/models/compute-china-activity.json',
           'research/tasks/bank_research/compute_jobs.json','research/models/compute-audited-history.json']
    jobs={j['id']:j for f in plans for j in obj(W/f)['jobs']}
    records=[]
    for r in ledger['runs']:
        if r.get('status')!='complete':continue
        spec=ROOT/jobs[r['id']]['input'];out=W/'compute'/r['output']
        assert sha(spec)==r['input_sha256'] and sha(out)==r['output_sha256']
        m=obj(spec)
        terms=[r['code_sha256'],r['environment_sha256'],r['method'],sha(spec)]
        if m.get('csv'): terms.append(sha(ROOT/m['csv']))
        expected=hashlib.sha256('|'.join(terms).encode()).hexdigest()
        assert expected==r['fingerprint']
        records.append({'id':r['id'],'method':r['method'],'input':str(spec.relative_to(ROOT)),
                        'input_sha256':sha(spec),'output':str(out.relative_to(W)),'output_sha256':sha(out),
                        'input_kind':obj(out)['result']['input_kind'],'code_sha256':r['code_sha256'],'environment_sha256':r['environment_sha256']})
    return dict(rows=records,runner_only_core_hours=sum(s['estimated_core_hours'] for s in ledger['sessions']))


if __name__=='__main__':
    out={'banks':banks(),'regulatory_originals':regulatory(),'local_government':fiscals(),'ledger':ledger()}
    (HERE/'independent_accounts.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
