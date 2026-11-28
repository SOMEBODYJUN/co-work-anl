"""Build the formal bank-stress inputs and independently check the book-to-supervisory bridge.

Run with the repository Python, from any directory. No network, no state mutation.
Amounts are RMB millions. Source line items are in statement_extract.csv.
"""
import csv
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from cncrisis.models import bank_stress

CASES = {
    'opening': (0, 1, 0),
    'one_year_charge_no_new_income': (1, 1, 0),
    'two_year_charges_no_new_income': (2, 1, 0),
    'one_year_charge_rwa_plus_5pct': (1, 1.05, 0),
    'one_year_charge_rwa_plus_5pct_with_income': (1, 1.05, 0.5),
}


def write_json(name, body):
    (HERE / name).write_text(json.dumps(body, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def close(left, right):
    if not math.isclose(left, right, rel_tol=1e-12, abs_tol=0.0011):
        raise ValueError(f'Comparison failed: {left} versus {right}')


def run(row):
    bank_id = row['id']
    def num(name):
        return float(row[name])

    assets, liabilities, opening_equity = (num(k) for k in ('assets','liabilities','book_equity'))
    net_credit = num('net_loans')
    close(assets - liabilities, opening_equity)
    cash = num('cash_equiv')
    ac_reported = row['ac_allowance'] != ''
    if ac_reported:
        gross = num('loan_principal') + num('accrued_interest')
        allowance = num('ac_allowance')
        close(gross - allowance, net_credit)
        key = 'all_customer_loans_including_accrued_interest'
    else:
        # The quarterly report gives neither AC allowance nor interest accrual separately.
        # The opening balance for this portfolio is already net of ECL; zero is the ADDITIONAL
        # undeducted allowance. No one uses it as a report of the institution's total reserve.
        gross, allowance = net_credit, 0.0
        key = 'reported_net_customer_loans_incremental_stress_only'
    bank = {'id':bank_id, 'cash':cash, 'liquid_assets_book':0,
            'other_assets':assets - net_credit - cash,
            'deposits':num('customer_deposits'), 'other_liabilities':liabilities - num('customer_deposits'),
            'capital':opening_equity, 'risk_weighted_assets':num('rwa'), 'minimum_capital_ratio':0,
            'credit':{key:{'gross':gross,'allowance':allowance}}}
    # The baseline holds existing allowances against existing expected loss. Overlay is after them.
    annualized_charge = num('loan_charge') * 12 / num('months')
    reg_open = num('capital_cet1')
    floor = num('min_cet1_with_buffer_2027')
    rwa = num('rwa')
    scenarios=[]
    for name,(multiple,rwa_factor,income_share) in CASES.items():
        loss = allowance + multiple * annualized_charge
        scenarios.append({'id':name, 'loss_rates':{key:loss/gross}, 'deposit_runoff_fraction':0,
                          'liquid_asset_haircut':0, 'cash_retained_earnings':income_share*num('net_profit'),
                          'rwa_multiplier':rwa_factor})
    spec={'input_kind':'observed_chinese_public_bank_financials_with_conditional_shocks',
          'unit':'RMB million','source':row['source_id'],'observed_as_of':row['as_of'],
          'scope':'Consolidated accounting balance sheet. The loan increment is a sensitivity around observed impairment expense. No forward probability. Credit-only runs have no liquidation bucket; funding is tested separately from disclosed LCR.',
          'allowance_basis':row['credit_basis'],
          'existing_allowance_note':'OCI reserve is not deducted from the carrying amount a second time. For net_book_value_incremental_charge_only the reported opening asset is already net; extra undeducted allowance is zero, not total bank reserves.',
          'book_to_regulatory':{'book_equity':opening_equity,'cet1':reg_open,'tier1':num('capital_t1'),
                                'total_regulatory_capital':num('capital_total'),'rwa':rwa,'public_cet1_reference_2027':floor,
                                'model_capital_is_book_equity':True,'model_minimum_0_is_only_nonnegative_book_equity_check':True},
          'banks':[bank],'scenarios':scenarios}
    write_json(bank_id+'_input.json',spec)
    computed=bank_stress(spec)
    bridged=[]
    for raw,scenario in zip(computed['results'],scenarios):
        name=scenario['id']; multiple,rwa_factor,income_share=CASES[name]
        ending_rwa=rwa*rwa_factor
        change=raw['ending_capital']-opening_equity
        expected_increment = multiple*annualized_charge
        close(raw['new_credit_loss_charged_to_capital'], expected_increment)
        close(change, income_share*num('net_profit')-expected_increment)
        close(raw['opening_balance_residual'], 0)
        ending_cet1=reg_open+change
        percent=ending_cet1/ending_rwa*100
        bridged.append({'case':name,'incremental_credit_charge':round(expected_increment,6),
                        'future_retained_cash_income_assumption':round(income_share*num('net_profit'),6),
                        'book_equity_after':round(raw['ending_capital'],6),'cet1_after':round(ending_cet1,6),
                        'rwa_after':round(ending_rwa,6),'cet1_ratio_percent':round(percent,6),
                        'cet1_shortfall_to_public_buffer':round(max(0,ending_rwa*floor-ending_cet1),6),
                        'cet1_headroom_signed':round(ending_cet1-ending_rwa*floor,6),
                        'book_equity_minus_cet1_held_fixed':round(opening_equity-reg_open,6)})
    hqla,outflow=num('hqla'),num('net_30d_outflow')
    # Disclosure conventions matter: for ICBC both amounts and the daily-derived ratio are separately averaged.
    return {'bank':bank_id,'as_of':row['as_of'],'unit':'RMB million unless noted','source_id':row['source_id'],
            'opening_balance_residual':computed['results'][0]['opening_balance_residual'],
            'annualized_reference_flow':round(annualized_charge,6),
            'static_cet1_headroom_to_2027_public_buffer':round(reg_open-rwa*floor,6),
            'static_cet1_headroom_to_bare_5pct_minimum':round(reg_open-rwa*.05,6),
            'static_t1_headroom_to_public_buffer':round(num('capital_t1')-rwa*(floor+.01),6),
            'static_total_headroom_to_public_buffer':round(num('capital_total')-rwa*(floor+.03),6),
            'hqla':hqla,'reported_30d_net_outflow':outflow,'reported_lcr_percent':num('lcr_published'),
            'difference_hqla_minus_net_outflow':round(hqla-outflow,6),
            'conditional_outflow_10pct_hqla_impairment_break_even':round(.9*hqla-outflow,6),
            'cases':bridged}


def main():
    with (HERE/'statement_extract.csv').open() as f:
        rows=list(csv.DictReader(f))
    results=[run(x) for x in rows]
    jobs=[{'id':'china-bank-'+r['id'].replace('_','-'), 'method':'bank-stress',
           'input':str((HERE/(r['id']+'_input.json')).relative_to(ROOT)), 'timeout_seconds':60} for r in rows]
    write_json('compute_jobs.json',{'budget_period':'boss-1-first-research-cycle','allocated_cores':9,'plan_core_hour_budget':6,'jobs':jobs})
    # Ageing proxy on AC loans only, preserving all other existing provisions.
    s2, p2, s3, p3=851133,147630,411632,335960
    stage_cost_if_all=s2*(p3/s3-p2/s2)
    evidence={'icbc_h1_stage_2_to_3_reprice':{'source':'BK005 financial statements note VII.1.3',
                'stage2_effective_provision_pct':100*p2/s2,'stage3_effective_provision_pct':100*p3/s3,
                'incremental_charge_if_all_stage2_resembles_stage3':stage_cost_if_all,
                'half_of_stage2_reprices':stage_cost_if_all/2,
                'interpretation':'Assume the affected stage-2 loans require the observed average stage-3 reserve coverage. This changes the expected loss, not a default transition probability.'},
              'icbc_q3_total_credit_allowance_from_rounded_npl_and_coverage':{
                'interval_million_rmb':[(416776-.5)*(2.1164-.00005),(416776+.5)*(2.1164+.00005)],
                'interpretation':'Rounded published coverage and NPL imply an interval for total loan reserves. It includes OCI loan reserve and does not identify AC separately. Not an input to the net-book Q3 run.'},
              'icbc_extra_2027_cet1_requirement_unchanged_q3_rwa':30478278*.005,
              'lanzhou_q3_allowance_tieout_million':9493.099+2691.809-4441.447+878.463+27.028,
              'lanzhou_q3_disclosed_total_loan_reserves_ac_plus_oci':8648.952+5.321}
    close(evidence['lanzhou_q3_allowance_tieout_million'],8648.952)
    write_json('capital_and_liquidity_results.json',{'unit':'RMB million unless expressly percent','banks':results,'cross_checks':evidence})


if __name__=='__main__':
    main()
