"""Independent synthetic CNY ledger cases, with numpy-financial reference calculations.

Run from any directory with a Python interpreter containing numpy-financial.
The reviewed JavaScript supplies results only; the expected numbers and comparisons are Python-owned.
"""
import collections
import copy
import datetime as dt
import gzip
import hashlib
import io
import json
import math
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
import numpy_financial as nf
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'household_engine'
NODE = os.getenv('AUDIT_NODE') or shutil.which('node') or '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/bin/node'
MODE = {'wageFactor': ('level', '倍'), 'unemploymentMonths': ('event', '月'), 'recoveryMonths': ('level', '月'),
    'reemploymentFactor': ('level', '倍'), 'loanRateDelta': ('annual', '年率差'), 'financialShock': ('shock', '比例'),
    'concentrationHaircut': ('shock', '比例'), 'vacancyAdd': ('level', '比例差'), 'rentFactor': ('level', '倍'),
    'propertyShock': ('shock', '比例'), 'inflationAnnual': ('annual', '年率小数'), 'saleDelay': ('level', '月')}

def household(cash=100000, minimum=0, **extra):
    return dict({'schema': 'household-cny.v1', 'dataKind': 'synthetic_example', 'rangeCase': 'base', 'cash': cash,
        'cashAnnual': 0, 'reserveMonths': 0, 'minimumLiving': minimum, 'cutFraction': 0, 'maxSaleWait': 120,
        'preference': 'cash', 'incomes': [], 'expenses': [], 'financial': [], 'properties': [], 'vehicles': [],
        'loans': [], 'citySources': []}, **extra)

def debt(p, rate, months, **extra):
    return dict({'id': 'L', 'name': 'audit loan', 'kind': 'consumer', 'method': 'annuity', 'principal': p,
        'annualRate': rate, 'months': months, 'payment': None, 'rateType': 'fixed', 'resetFirst': 12, 'resetEvery': 12,
        'canPrepay': True, 'prepayFrom': 1, 'prepayMin': 0, 'prepayFee': 0, 'settlementFee': 0,
        'transferWithLien': False, 'allowRecast': True, 'allowShorten': True, 'collateral': '', 'start': 1,
        'monthlyFee': 0}, **extra)

def income(id, money, **extra):
    return dict({'id': id, 'name': id, 'kind': 'wage', 'monthly': money, 'from': 1, 'to': 120, 'every': 1,
        'annualGrowth': 0, 'stability': 'given', 'stressJob': False, 'jobStart': 1, 'jobMonths': 0, 'jobPayFraction': 0,
        'recoveryMonths': 0, 'returnFraction': 1}, **extra)

def expense(id, money, kind='necessary', **extra):
    return dict({'id': id, 'name': id, 'kind': kind, 'monthly': money, 'from': 1, 'to': 120, 'every': 1,
        'annualGrowth': 0, 'inflationLinked': False}, **extra)

def home(value=1000, sale=1000, **extra):
    return dict({'id': 'P', 'name': 'audit property', 'city': '测试城', 'type': '住宅', 'use': 'idle', 'value': value,
        'saleValue': sale, 'saleLag': 0, 'lock': 1, 'canSell': True, 'rent': 0, 'vacancy': 0, 'leaseLag': 0,
        'discountRent': 0, 'discountLeaseLag': 0, 'carry': 0, 'saleFee': 0, 'closingFee': 0,
        'replacementAllowed': False, 'replacementMonthly': None, 'sourceId': ''}, **extra)

def car(**extra):
    return dict({'id': 'C', 'name': 'audit vehicle', 'value': 2000, 'saleValue': 1740, 'annualDepreciation': 0,
        'saleLag': 1, 'lock': 1, 'canSell': True, 'necessary': True, 'replacementAllowed': False,
        'replacementMonthly': None, 'carry': 35, 'saleFee': 0, 'closingFee': 0}, **extra)

def security(value, **extra):
    return dict({'id': 'F', 'name': 'audit security', 'kind': 'stock', 'value': value, 'annualReturn': 0,
        'concentration': 0, 'fee': 0, 'settle': 0, 'unlock': 1, 'maturity': 0, 'restriction': 'free',
        'purpose': '家庭可用'}, **extra)

def shock(key, value, start=1, duration=120, target='*', **extra):
    mode, unit = MODE[key]
    return dict({'key': key, 'mode': mode, 'unit': unit, 'start': start, 'duration': 1 if mode in ('event',
        'shock') else duration, 'target': target, 'value': value, 'range': [value, value],
        'sourceId': 'independent-audit', 'editable': True, 'assumption': 'stress_test'}, **extra)

def scenario(id='quiet', paths=None, role=None):
    return {'id': id, 'name': id, 'role': role or id, 'paths': paths or []}

def prepay(mode, amount=None, month=2):
    return dict({'kind': 'prepay', 'loan': 'L', 'mode': mode, 'month': month},
        **{'amount': amount} if amount is not None else {})

def sell(id='P', month=1, **extra):
    return dict({'kind': 'list', 'asset': id, 'month': month}, **extra)

def trade(mode='all', **extra):
    return dict({'kind': 'liquidate', 'asset': 'F', 'month': 1, 'mode': mode}, **extra)
requests = []

def add(name, h=None, s=None, actions=(), op='simulate', limit=100):
    requests.append({'id': name, 'op': op, 'household': h, 'scenarios': [scenario()] if s is None else s if isinstance(s,
        list) else [s], 'strategy': {'id': 'independent', 'actions': list(actions)}, 'limit': limit})
add('blank', op='blank')
add('blank_rejected', household(cash=None, minimum=None))
unconfirmed = {'id': 'Q', 'name': 'only principal/rate/term entered', 'kind': 'consumer', 'principal': 10000,
    'annualRate': 0.1, 'months': 12}
add('unknown_loan_permission', household(cash=20000, loans=[unconfirmed]), op='assess')
add('unknown_loan_fees', household(cash=20000, loans=[dict(unconfirmed, canPrepay=True, allowRecast=True,
    allowShorten=True)]), op='assess')
for label, values in [('home', home(value=12000, sale=11000)), ('car', car(necessary=False))]:
    group = 'properties' if label == 'home' else 'vehicles'
    for tag, drop in [('permission', ['canSell']), ('fees', ['saleFee', 'closingFee', 'saleLag'])]:
        add('unknown_' + label + '_' + tag, household(cash=20000, **{group: [{k: v for k,
            v in values.items() if k not in drop}]}), op='assess')
add('budget_not_debt', household(cash=180, minimum=0, loans=[debt(20, 0, 1)], expenses=[expense('wish', 220,
    'discretionary')]))
add('annuity_zero', household(loans=[debt(2940, 0, 7)]))
add('annuity_one', household(loans=[debt(2500, 0.096, 1, monthlyFee=17)]))
add('full_prepay_fee', household(cash=2000, loans=[debt(1200, 0, 3, prepayFee=0.01, settlementFee=15)]),
    actions=[prepay('full', month=1)])
add('guarantee_call', household(cash=100, incomes=[income('W', 200)], loans=[debt(500, 0, 1, kind='guarantee', start=3)]))
add('staged_sales', household(cash=0, financial=[security(4000, fee=0.01, settle=1)]), scenario('stages',
    [shock('financialShock', -0.25, 4)]), [trade('stages')])
add('annuity_standard', household(loans=[debt(15437, 0.0547, 19)]))
add('equal_principal', household(loans=[debt(9720, 0.072, 11, method='principal')]))
float_path = scenario('reset', [shock('loanRateDelta', 0.12, 2, 3), shock('loanRateDelta', -0.036, 5, 2)])
add('floating', household(loans=[debt(15600, 0.06, 6, rateType='floating', resetFirst=3, resetEvery=2)]), float_path)
add('fixed_rate_control', household(loans=[debt(15600, 0.06, 6)]), float_path)
for mode in ('recast', 'shorten', 'hold'):
    add('prepay_' + mode, household(loans=[debt(14400, 0.074, 8, prepayFee=0.007)]),
        actions=[] if mode == 'hold' else [prepay(mode, 2130)])
for name, contract, action in [('lock', {'prepayFrom': 3}, prepay('recast', 2130)), ('min', {'prepayMin': 2500},
    prepay('recast', 2130)), ('forbid', {'allowShorten': False}, prepay('shorten', 2130)), ('full_forbid',
    {'canPrepay': False}, prepay('full'))]:
    add('contract_' + name, household(loans=[debt(14400, 0.074, 8, **contract)]), actions=[action])
closing = home(12000, 9000, closingFee=50, saleFee=0.02)
collateral = debt(11000, 0.12, 10, method='bullet', kind='mortgage', collateral='P', prepayFee=0.01, settlementFee=30,
    monthlyFee=9, transferWithLien=True)
close_net = 9000 - 50 - 180 - 11000 - 110 - 110 - 30 - 9
for name, available, transfer in [('under', -close_net - 1, True), ('exact', -close_net, True), ('escrow_under', 11258,
    False), ('escrow_exact', 11259, False)]:
    add('closing_' + name, household(cash=available, properties=[closing], loans=[dict(collateral,
        transferWithLien=transfer)]), actions=[sell()])
for asset, group, record in [('P', 'properties', closing), ('C', 'vehicles', car(necessary=False, saleLag=0))]:
    for missing in ['prepayFee', 'settlementFee']:
        link = dict(collateral, collateral=asset, kind='mortgage' if group == 'properties' else 'car')
        del link[missing]
        add('unknown_lien_' + asset + '_' + missing, household(**{group: [record]}, loans=[link]), actions=[sell(asset)])
add('closing_prohibited', household(properties=[closing], loans=[dict(collateral, canPrepay=False)]), actions=[sell()])
add('closing_delay', household(cash=1000, properties=[home(1100, 1000, use='let', rent=90, carry=12, saleLag=2,
    saleFee=0.01)], loans=[debt(1000, 0, 5, method='principal', kind='mortgage', collateral='P',
    transferWithLien=True)]), actions=[sell()])
add('unsellable', household(cash=65, minimum=40, properties=[home(9000, 8000, canSell=False)]), actions=[sell()])
add('wait_limit', household(cash=65, minimum=40, maxSaleWait=2, properties=[home(9000, 8000, saleLag=1)]),
    scenario('longer', [shock('saleDelay', 3)]), [sell()])
add('occupied_no_alternative', household(properties=[home(use='occupied', replacementAllowed=False)]), actions=[sell()])
add('necessary_car', household(vehicles=[car()]), actions=[sell('C')])
add('replace_car', household(vehicles=[car(replacementAllowed=True, replacementMonthly=28)]), actions=[sell('C')])
add('vacancy', household(properties=[home(use='let', rent=1250, carry=52, vacancy=0.2)]), scenario('vacancy',
    [shock('vacancyAdd', 0.8, 1, 3), shock('rentFactor', 0.9, 1, 4)]))
add('rent_discount', household(properties=[home(rent=1000, carry=20, leaseLag=3, discountRent=0.1, discountLeaseLag=1)]),
    actions=[{'kind': 'rent', 'month': 1, 'asset': 'P', 'discount': True}])
jobs = household(incomes=[income('A', 1500, stressJob=True, jobPayFraction=0.1), income('B', 400), income('working', 90,
    kind='business')])
job_paths = scenario('job', [shock('unemploymentMonths', 2, 2), shock('recoveryMonths', 3, 1, 8),
    shock('reemploymentFactor', 0.7, 1, 8), shock('wageFactor', 0.9, 3, 2, 'B')])
add('employment', jobs, job_paths)
add('total_return', household(cash=85, financial=[security(8100, annualReturn=0.08, concentration=0.4)]),
    scenario('markets', [shock('financialShock', -0.25, 2), shock('concentrationHaircut', 0.1, 3)]))
add('security_settle', household(cash=330, minimum=100, financial=[security(4550, fee=0.02, settle=2)]),
    actions=[trade()])
add('security_late_failure', household(cash=99, minimum=100, financial=[security(4550, fee=0.02, settle=2)]),
    actions=[trade()])
add('restricted_deposit', household(cash=16, minimum=10, financial=[security(1000, kind='deposit', maturity=1,
    restriction='restricted')]), actions=[trade()])
add('free_deposit', household(cash=35, minimum=10, financial=[security(1000, kind='deposit', maturity=3,
    annualReturn=0.12)]))
add('pledged', household(cash=200, financial=[security(900, restriction='pledged')], loans=[debt(800, 0, 10,
    method='bullet', collateral='F')]), actions=[trade()])
for label, sec, contract, start_cash in [('immediate', security(3000, restriction='pledged'), debt(1000, 0, 12,
    kind='margin', method='bullet', collateral='F', transferWithLien=True), 0), ('delayed', security(3000,
    restriction='pledged', fee=0.02, settle=2), debt(1000, 0.12, 12, kind='margin', method='bullet', collateral='F',
    transferWithLien=True, prepayFee=0.01, settlementFee=7), 100), ('forbid_early', security(3000,
    restriction='pledged'), debt(1000, 0, 12, kind='margin', method='bullet', collateral='F', transferWithLien=True,
    canPrepay=False), 0), ('no_lien_transfer', security(3000, restriction='pledged'), debt(1000, 0, 12, kind='margin',
    method='bullet', collateral='F', transferWithLien=False), 0), ('short_equity', security(700, restriction='pledged'),
    debt(1000, 0, 12, kind='margin', method='bullet', collateral='F', transferWithLien=True), 0)]:
    add('margin_' + label, household(cash=start_cash, minimum=10, loans=[contract], financial=[sec]), actions=[trade()])
for name, omit in [('eligibility', ['restriction', 'unlock']), ('cost_settlement', ['fee', 'settle'])]:
    z = {k: v for k, v in security(1000).items() if k not in omit}
    add('unknown_security_' + name, household(cash=10000, financial=[z]), op='assess')
from_salary = household(cash=0, minimum=100, incomes=[income('salary', 1000)], loans=[debt(5000, 0, 10, prepayMin=100)])
add('salary_funded_candidates', from_salary, op='assess')
add('salary_funded_control', from_salary, actions=[prepay('recast', 200, 1)])
add('monthly_inflation', household(cash=585, minimum=1, incomes=[income('I', 100)], financial=[security(200)]),
    scenario('inflation', [shock('inflationAnnual', 0.12)]))
add('failure', household(cash=140, minimum=50, loans=[debt(200, 0.12, 3, method='bullet')]))
all_failed = household(cash=10, minimum=70, financial=[security(3000, restriction='restricted')])
add('no_feasible', all_failed, op='assess')
add('mixed', household(cash=0, minimum=1, financial=[security(200)]), op='assess')
add('minimum_floor', household(cash=50, minimum=120, expenses=[expense('living', 60), expense('med', 13, 'medical')],
    incomes=[income('I', 98)]))
add('reserve_short', household(cash=71, minimum=17, reserveMonths=5, incomes=[income('I', 17)]), op='assess')
add('reserve_blocks_prepay', household(cash=350, minimum=120, reserveMonths=2, incomes=[income('I', 217)],
    loans=[debt(600, 0, 6)]), actions=[prepay('recast', 200, month=1)])
clock = household(cash=1100, minimum=100, incomes=[income('I', 35)], properties=[home(2200, 2100, saleLag=2)],
    financial=[security(500)])
trigger = [sell(trigger='reserve', buffer=3)]
for id, s in [('plain', scenario()), ('future', scenario('future', [shock('propertyShock', -0.6, 15), shock('wageFactor',
    0.5, 15, 20, 'I')]))]:
    add('trigger_' + id, clock, s, trigger)
    add('hold_' + id, clock, s)
range_home = household(cash={'low': 50, 'base': 100, 'high': 250}, incomes=[income('I', 300)])
range_path = scenario('range', [shock('wageFactor', {'low': 0.55, 'base': 0.8, 'high': 1.1}, 1, 1, range=[0.55, 1.1],
    assumption='historical')])
for setting in ['low', 'base', 'high']:
    add('range_' + setting, dict(range_home, rangeCase=setting), range_path)
add('range_missing', dict(range_home, cash={'low': 10, 'high': 55}))
add('range_missing_high', dict(range_home, cash={'low': 10, 'high': 55}, rangeCase='high'))
add('bad_assumption', range_home, scenario('bad', [shock('wageFactor', 1, assumption='industry_average')]))
add('duplicate_action', household(properties=[home()]), actions=[sell(), sell(month=2)])
add('two_sales', household(cash=10000, properties=[home(id='A', value=1500, sale=1300), home(id='B', value=2600,
    sale=2300)]), actions=[sell('B', 1), sell('A', 3)])
add('simple_enumeration', household(cash=500, properties=[home()]), op='assess')
rich = household(cash=25000, minimum=600, reserveMonths=2, cutFraction=0.4, incomes=[income('W', 4400, stressJob=True),
    income('R', 1700, kind='business')], expenses=[expense('X', 600), expense('D', 500, 'discretionary')],
    financial=[security(12500, annualReturn=0.06, settle=1, fee=0.005)], properties=[home(98000, 93000, use='idle',
    rent=680, carry=70, leaseLag=3, discountRent=0.12, discountLeaseLag=1, saleLag=3, saleFee=0.021)],
    vehicles=[car(necessary=False)], loans=[debt(18800, 0.078, 26, prepayFee=0.006, prepayMin=300)])
rich_paths = [scenario(), scenario('squeeze', [shock('wageFactor', 0.82, 3, 22, 'W'), shock('unemploymentMonths', 4, 7),
    shock('recoveryMonths', 3), shock('financialShock', -0.23, 3), shock('propertyShock', -0.12, 2)]),
    scenario('recovery', [shock('wageFactor', 1.12, 1, 18, 'W'), shock('propertyShock', 0.06, 3)], 'recovery')]
add('rich_enumeration', rich, rich_paths, op='assess', limit=350)
add('reverse_unknown_price', household(cash=1000, properties=[home(sale=None)]), actions=[sell()], op='reverse')
add('reverse_unknown_delay', household(cash=1000, properties=[home(saleLag=None)]), actions=[sell()], op='reverse')
add('reverse_price', household(cash=0, minimum=10, properties=[home(1500, 1500)]), actions=[sell()], op='reverse')
add('reverse_joint', household(cash=0, minimum=150, incomes=[income('W', 100)], properties=[home(use='let', rent=100)]),
    op='reverse')
add('reverse_wage', household(cash=0, minimum=75, incomes=[income('I', 100)]), op='reverse')
add('reverse_prepay', household(cash=5000, minimum=50, incomes=[income('I', 500)], loans=[debt(1200, 0, 12)]),
    op='reverse')
add('reverse_delay', household(cash=200, minimum=100, properties=[home(value=12000, sale=12000)]), actions=[sell()],
    op='reverse')
add('reverse_rent', household(cash=20000, properties=[home(value=12000, sale=13000, rent=25, carry=3)]), op='reverse')

def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def run_engine(rows, product=None):
    proc = subprocess.run([NODE, str(HERE / 'node_bridge.cjs'), str(product or AUTHOR / 'engine.js')],
        input=canonical(rows), capture_output=True, check=True)
    return json.loads(proc.stdout)
checks = []

def eq(label, actual, expected, tol=1e-06):

    def close(a, b):
        if isinstance(b, (int, float)) and (not isinstance(b, bool)):
            return isinstance(a, (float, int)) and (not isinstance(a, bool)) and (abs(a - b) <= max(tol, abs(b) * 1e-10))
        if isinstance(b, list):
            return isinstance(a, list) and len(a) == len(b) and all((close(x, y) for x, y in zip(a, b)))
        if isinstance(b, dict):
            return isinstance(a, dict) and b.keys() == a.keys() and all((close(a[k], v) for k, v in b.items()))
        return a == b
    ok = close(actual, expected)

    def sample(x):
        if isinstance(x, list) and len(x) > 15:
            return {'count': len(x), 'first': x[:4], 'last': x[-3:], 'sha256': sha(canonical(x))}
        return x
    checks.append({'check': label, 'pass': ok, 'observed': sample(actual), 'expected': sample(expected),
        'absoluteTolerance': tol})
    return ok

def verify(out):

    def at(k, m, f):
        return out[k]['rows'][m - 1][f]

    def col(k, f, n=None):
        return [r[f] for r in out[k]['rows'][:n]]

    def arr(k, fields, m=1):
        return [at(k, m, f) for f in fields]

    def sm(k, f):
        return out[k]['summary'][f]

    def completion(k):
        return sm(k, 'completed')

    def clean(k):
        return sm(k, 'feasible')

    def audit_amort(k, p, rate, n, fee=0):
        payments = []
        interests = []
        principal = []
        balances = []
        running = p
        for i in range(1, n + 1):
            interest = 0.0 if rate == 0 else float(-nf.ipmt(rate / 12, i, n, p))
            pp = p / n if rate == 0 else float(-nf.ppmt(rate / 12, i, n, p))
            running -= pp
            payments.append(pp + interest + fee)
            interests.append(interest)
            principal.append(pp)
            balances.append(max(0, running))
        for name, y in [('interest', interests), ('principal', principal), ('regularDue', payments), ('debt', balances)]:
            eq(k + ' ' + name, col(k, name, n), y)
        eq(k + ' final paid', arr(k, ['debt', 'regularDue'], n + 1), [0, 0])
        eq(k + ' 120 months', len(out[k]['rows']), 120)
    eq('empty household cash / required floor', [out['blank']['cash'], out['blank']['minimumLiving'],
        out['blank']['incomes'], out['blank']['dataKind']], [None, None, [], 'household'])
    eq('empty original amounts cannot run', 'error' in out['blank_rejected'], True)
    audit_amort('annuity_zero', 2940, 0, 7)
    audit_amort('annuity_one', 2500, 0.096, 1, 17)
    audit_amort('annuity_standard', 15437, 0.0547, 19)
    audit_amort('fixed_rate_control', 15600, 0.06, 6)
    eq('fully prepaid remaining principal plus variable and fixed fee checked once', arr('full_prepay_fee', ['principal',
        'prepaid', 'prepayFees', 'debt', 'cash']), [400, 800, 23, 0, 777])
    eq('fully prepaid loan has no later installments', col('full_prepay_fee', 'regularDue', 4), [400, 0, 0, 0])
    eq('guarantee call creates a due debt without cash drawdown proceeds', [col('guarantee_call', 'principal', 4),
        col('guarantee_call', 'cash', 4)], [[0, 0, 500, 0], [300, 500, 200, 400]])
    eq('four staged sales each sell one quarter of initial shares at prevailing prices', [(x['month'],
        x['amount']) for x in out['staged_sales']['events'] if x['type'] == 'trade'], [(1, 990), (4, 742.5), (7, 742.5),
        (10, 742.5)])
    eq('four staged sales do not settle early or sell a second time', [(x['month'],
        x['amount']) for x in out['staged_sales']['events'] if x['type'] == 'settle'], [(2, 990), (5, 742.5), (8,
        742.5), (11, 742.5)])
    eq('four staged sales total cash net of fees', sm('staged_sales', 'terminalNominal'), 3217.5)
    n = 11
    p = 9720
    r = 0.072 / 12
    eq('equal principal constant installment', col('equal_principal', 'principal', n), [p / n] * n)
    eq('equal principal interest by opening balance', col('equal_principal', 'interest', n),
        [(p - p / n * j) * r for j in range(n)])
    eq('equal principal last balance', at('equal_principal', n, 'debt'), 0)
    balance = 15600
    annual = [0.06, 0.06, 0.18, 0.18, 0.024, 0.024]
    f_due = []
    f_pr = []
    f_int = []
    f_bal = []
    for i, a in enumerate(annual):
        re = a / 12
        if i in (0, 2, 4):
            pay = -float(nf.pmt(re, 6 - i, balance))
        interest = balance * re
        pr = pay - interest
        balance -= pr
        f_due.append(pay)
        f_pr.append(pr)
        f_int.append(interest)
        f_bal.append(max(0, balance))
    for f, values in [('regularDue', f_due), ('principal', f_pr), ('interest', f_int), ('debt', f_bal)]:
        eq('floating only at resets ' + f, col('floating', f, 6), values)
    eq('floating contract annual path', [x['annualRate'] for x in out['floating']['byLoan']['L']], annual)
    rate = 0.074 / 12
    n = 8
    p = 14400
    prepaid = 2130
    pre_fee = 14.91
    origpay = -float(nf.pmt(rate, n, p))
    for mode in ('hold', 'recast', 'shorten'):
        k = 'prepay_' + mode
        bal = p
        pay = origpay
        ints = []
        debts = []
        dues = []
        cash = 100000
        cashpath = []
        expected_last = 8
        for m in range(1, 9):
            interest = bal * rate
            principal = min(bal, max(0, pay - interest))
            bal -= principal
            cash -= interest + principal
            if m == 2 and mode != 'hold':
                bal -= prepaid
                cash -= prepaid + pre_fee
                if mode == 'recast':
                    pay = -float(nf.pmt(rate, n - m, bal))
                else:
                    expected_last = m + math.ceil(float(nf.nper(rate, -origpay, bal)) - 1e-10)
            ints.append(interest)
            debts.append(max(0, bal))
            dues.append(principal + interest)
            cashpath.append(cash)
        for f, v in [('principal_balance', debts), ('interest', ints), ('regularDue', dues), ('cash', cashpath)]:
            eq(k + ' ' + f, col(k, 'debt' if f == 'principal_balance' else f, 8), v)
        eq(k + ' final loan installment month', max((x['month'] for x in out[k]['byLoan']['L'] if 'principal' in x)),
            expected_last)
    eq('recast reduces next payment; shorten keeps scheduled amount', [at('prepay_recast', 3, 'regularDue') < origpay,
        at('prepay_shorten', 3, 'regularDue')], [True, origpay])
    eq('shorten saves more interest', sm('prepay_shorten', 'interestTotal') < sm('prepay_recast',
        'interestTotal') < sm('prepay_hold', 'interestTotal'), True)
    for suffix in ('lock', 'min', 'forbid', 'full_forbid'):
        k = 'contract_' + suffix
        eq(k + ' blocked/paid/ongoing', [len(sm(k, 'blocked')), sm(k, 'prepaid'), completion(k), clean(k)], [1, 0, True,
            False])
        eq(k + ' unchanged schedule', col(k, 'debt', 8), col('prepay_hold', 'debt', 8))
    for k in ('under', 'escrow_under'):
        k = 'closing_' + k
        eq(k + ' no sale/no secured discharge', [at(k, 1, 'saleGross'), at(k, 1, 'closingPrincipal'), at(k, 1,
            'property'), at(k, 1, 'debt'), sm(k, 'blocked')[0]['need']], [0, 0, 12000, 11000, 1])
    for k, starting in [('exact', -close_net), ('escrow_exact', 11259)]:
        k = 'closing_' + k
        eq(k + ' cash after separate fees and secured debt', arr(k, ['cash', 'saleGross', 'saleFees', 'closingPrincipal',
            'closingInterest', 'releaseFees', 'loanFees', 'debt', 'property', 'regularDue']), [starting + close_net,
            9000, 230, 11000, 110, 140, 9, 0, 0, 0])
        eq(k + ' settlement once', sum((x['closingPrincipal'] + x['principal'] for x in out[k]['rows'])), 11000)
    for asset in ('P', 'C'):
        for field in ('prepayFee', 'settlementFee'):
            k = 'unknown_lien_' + asset + '_' + field
            eq(k + ' cannot indirectly close an unconfirmed loan at zero cost', [at(k, 1, 'saleGross'), at(k, 1,
                'closingPrincipal'), len(sm(k, 'blocked')), completion(k)], [0, 0, 1, True])
    eq('contract can prohibit mortgage discharge', [at('closing_prohibited', 1, 'saleGross'),
        len(sm('closing_prohibited', 'blocked'))], [0, 1])
    eq('sale delayed by two full monthly intervals', col('closing_delay', 'saleGross', 4), [0, 0, 1000, 0])
    eq('rent and carry disappear at closing', [[at('closing_delay', m, f) for m in range(1, 5)] for f in ['rent',
        'carry']], [[90, 90, 0, 0], [12, 12, 0, 0]])
    eq('sale normal + closing principal reconcile', [(at('closing_delay', m, 'principal'), at('closing_delay', m,
        'closingPrincipal'), at('closing_delay', m, 'debt')) for m in range(1, 5)], [(200, 0, 800), (200, 0, 600), (0,
        600, 0), (0, 0, 0)])
    eq('closing month cash including fees', col('closing_delay', 'cash', 4), [878, 756, 1146, 1146])
    eq('closing proceeds net', sm('closing_delay', 'saleNet'), 390)
    for k in ('unsellable', 'wait_limit'):
        eq(k + ' fallback and failure', [sm(k, 'firstFailure'), sm(k, 'worstGap'), sm(k, 'terminalReal'), sm(k,
            'saleNet'), len(sm(k, 'blocked'))], [2, 15, None, 0, 1])
    for k in ('occupied_no_alternative', 'necessary_car'):
        eq(k + ' law or replacement constraint', [at(k, 1, 'saleGross'), len(sm(k, 'blocked')), clean(k)], [0, 1, False])
    eq('replacement mobility starts on closing', [(at('replace_car', m, 'saleGross'), at('replace_car', m, 'carry'),
        at('replace_car', m, 'replacement')) for m in (1, 2, 3)], [(0, 35, 0), (1740, 0, 28), (0, 0, 28)])
    eq('full vacancy still incurs carrying cost', col('vacancy', 'rent', 5), [0, 0, 0, 900, 1000])
    eq('vacancy carry', col('vacancy', 'carry', 5), [52] * 5)
    eq('discounted lease pays only once lease begins', col('rent_discount', 'rent', 4), [0, 900, 900, 900])
    a = [1500, 150, 150, 450, 750, 1050, 1050]
    b = [400, 400, 360, 360, 400, 400, 400]
    eq('independent wage loss, unaffected business and gradual recovery', col('employment', 'income', 7),
        [i + j + 90 for i, j in zip(a, b)])
    eq('investment total return includes distributions, no second dividend cash', col('total_return', 'cash', 13),
        [85] * 13)
    eq('one-off loss and concentration, compounded annual return', col('total_return', 'financial', 13),
        [8100 * 1.08 ** (m / 12) * (0.75 if m >= 2 else 1) * (0.96 if m >= 3 else 1) for m in range(1, 14)])
    eq('trade financial position at order; proceeds only at T+2', [[at('security_settle', m, f) for m in (1, 2,
        3)] for f in ['cash', 'financial', 'receivables', 'securityReceipts', 'securityTradeFees']], [[230, 130, 4489],
        [0, 0, 0], [4459, 4459, 0], [0, 0, 4459], [91, 0, 0]])
    eq('pending financial proceeds cannot pay current obligation', [sm('security_late_failure', 'firstFailure'),
        at('security_late_failure', 1, 'receivables'), sm('security_late_failure', 'worstGap'),
        sm('security_late_failure', 'terminalNominal')], [1, 4459, 1, None])
    eq('restricted deposit never becomes usable', [sm('restricted_deposit', 'firstFailure'), sm('restricted_deposit',
        'worstGap'), at('restricted_deposit', 2, 'financial'), sm('restricted_deposit', 'securityNet')], [2, 4, 1000, 0])
    eq('free deposit maturity and cumulative accrued interest', col('free_deposit', 'securityReceipts', 4), [0, 0,
        1000 * 1.12 ** 0.25, 0])
    eq('pledged security held before release', [at('pledged', 1, 'financial'), at('pledged', 1, 'securityReceipts'),
        len(sm('pledged', 'blocked'))], [900, 0, 1])
    eq('contract-authorized margin liquidation retires loan and covers monthly needs', arr('margin_immediate', ['cash',
        'debt', 'financial', 'unpaid']) + [sm('margin_immediate', 'terminalNominal'), sm('margin_immediate',
        'firstFailure')], [1990, 0, 0, 0, 800, None])
    for label in ['forbid_early', 'no_lien_transfer', 'short_equity']:
        k = 'margin_' + label
        eq('security liquidation with unresolved debt ' + label, [sm(k, 'firstFailure'), sm(k, 'worstGap'), at(k, 1,
            'debt'), len(sm(k, 'blocked'))], [1, 10, 1000, 1])
    for m, expected in [(1, [80, 1000, 0]), (2, [60, 1000, 0]), (3, [1963, 0, 0])]:
        vals = arr('margin_delayed', ['cash', 'debt', 'unpaid'], m) if len(out['margin_delayed']['rows']) >= m else None
        eq('delayed margin cash, principal and spending m' + str(m), vals, expected)
    eq('delayed margin proceeds paid once after 2 months; transaction and release fees plus all 3 months of interest',
        sm('margin_delayed', 'terminalNominal'), 793)
    eq('salary-funded feasible control after necessities and first due installment', arr('salary_funded_control',
        ['income', 'cash', 'principal', 'prepaid']), [1000, 200, 500, 200])
    sal = out['salary_funded_candidates']['all']
    eq('small enumerated universe includes an executable partial repayment from already contracted income',
        any((r['feasible'] and any((a['kind'] == 'prepay' and a['mode'] in ('shorten',
        'recast') for a in r['actions'])) for r in sal)), True)
    for m in (1, 12, 36, 120):
        c = 585 + 100 * m - sum((1.12 ** (i / 12) for i in range(1, m + 1)))
        eq('real wealth deflation m' + str(m), arr('monthly_inflation', ['cpi', 'netWorth', 'realNetWorth'], m),
            [1.12 ** (m / 12), c + 200, (c + 200) / 1.12 ** (m / 12)])
    eq('failed cash stops; unpaid non-principal and principal survive as liabilities', [sm('failure', 'firstFailure'),
        sm('failure', 'supportMonths'), sm('failure', 'worstGap'), at('failure', 3, 'arrears'), at('failure', 3,
        'debt'), len(out['failure']['rows']), sm('failure', 'terminalNominal'), sm('failure', 'terminalReal'),
        sm('failure', 'points')['120']], [3, 2, 216, 2, 200, 3, None, None, None])
    eq('failed month book balance remains available only as diagnostic', arr('failure', ['cash', 'netWorth',
        'realNetWorth', 'bookNetWorth'], 3), [0, None, None, -202])
    eq('failure source for each unpaid yuan', arr('failure', ['unpaid', 'missedDebtService', 'unfundedEssential',
        'unfundedDiscretionary', 'arrears'], 3), [216, 202, 14, 0, 2])
    eq('unfunded optional spending is a failed budget, not a new lender balance', arr('budget_not_debt', ['unpaid',
        'debt', 'arrears', 'missedDebtService', 'unfundedDiscretionary', 'bookNetWorth']), [60, 0, 0, 0, 60, 0])
    for name, kind in [('unknown_loan_permission', 'prepay'), ('unknown_loan_fees', 'prepay'),
        ('unknown_home_permission', 'list'), ('unknown_home_fees', 'list'), ('unknown_car_permission', 'list'),
        ('unknown_car_fees', 'list'), ('unknown_security_eligibility', 'liquidate'),
        ('unknown_security_cost_settlement', 'liquidate')]:
        test = out[name]
        baseline_ok = 'all' in test and test['all'][0]['scenarios']['quiet']['completed']
        opted = [r['id'] for r in test.get('all', []) if r['feasible'] and any((a['kind'] == kind for a in r['actions']))]
        eq(name + ' baseline possible; no unconfirmed economic action marked feasible', [baseline_ok, len(opted)], [True,
            0])
    t = out['no_feasible']
    eq('no feasible household, only first unfunded obligations, no wealth prize', [t['coverage']['evaluated'],
        t['commonCount'], t['winners']['leastGap'], t['all'][0]['funding'], t['shortlist'], t['all'][0]['worstWealth'],
        t['all'][0]['regret'], t['winners']['wealth']], [1, 0, 'S000', 60, [], None, None, None])
    eq('no feasible default role output', [t['winners'][k] for k in ('robust', 'cash', 'debt', 'regret')], [None] * 4)
    t = out['mixed']
    good = [r['id'] for r in t['all'] if r['feasible']]
    bad = [r for r in t['all'] if not r['feasible']]
    eq('failed rich book balance never ranks with fulfilling strategies',
        all((all((t['ranks'][k].index(i) < t['ranks'][k].index(j['id']) for i in good for j in bad)) for k in t['ranks'])) and all((r['regret'] is None and r['worstWealth'] is None and (not r['pareto']) for r in bad)) and bool(good) and bool(bad), True)
    eq('mandatory minimum applies independently of declared regular costs', [at('minimum_floor', 1, 'essential'),
        at('minimum_floor', 1, 'cash'), sm('minimum_floor', 'firstFailure'), sm('minimum_floor', 'worstGap')], [133, 15,
        2, 20])
    eq('reserve breach without a payment failure', [out['reserve_short']['commonCount'],
        out['reserve_short']['all'][0]['funding'], out['reserve_short']['all'][0]['scenarios']['quiet']['completed']],
        [0, 14, True])
    eq('discretionary loan prepayment cannot spend reserve', [sm('reserve_blocks_prepay', 'prepaid'),
        len(sm('reserve_blocks_prepay', 'blocked')), sm('reserve_blocks_prepay', 'blocked')[0]['need']], [0, 1, 93])
    prefix = 14
    for variant in ('hold', 'trigger'):
        p, f = (out[variant + '_plain'], out[variant + '_future'])
        eq('no knowledge of later path / ' + variant, p['rows'][:prefix] == f['rows'][:prefix], True)
        eq('order before month 15 follows same observed funds / ' + variant,
            [e for e in p['events'] if e['month'] <= prefix], [e for e in f['events'] if e['month'] <= prefix])
    eq('threshold lists in month 14 before the month-15 price shock',
        [e['month'] for e in out['trigger_future']['events'] if e['type'] == 'list'], [14])
    eq('future loss priced at actual settlement not anticipated', [at('trigger_future', 16, 'saleGross'),
        at('trigger_plain', 16, 'saleGross')], [840, 2100])
    for variant in ('plain', 'future'):
        a, b = (out['hold_' + variant], out['trigger_' + variant])
        n = min(len(a['rows']), len(b['rows']))
        eq('identical exogenous income under rival actions / ' + variant, [x['income'] for x in a['rows'][:n]],
            [x['income'] for x in b['rows'][:n]])
    for choosing, expected in [('low', [50, 165]), ('base', [100, 240]), ('high', [250, 330])]:
        eq('editable recorded household + scenario uncertainty ' + choosing, arr('range_' + choosing, ['openingCash',
            'income']), expected)
    eq('unknown center requires explicit choice', 'error' in out['range_missing'], True)
    eq('explicit upper endpoint with no center', at('range_missing_high', 1, 'openingCash'), 55)
    eq('invalid assumption type rejected', 'error' in out['bad_assumption'], True)
    eq('same property cannot be disposed twice', 'error' in out['duplicate_action'], True)
    eq('multiple sales sequence follows specified asset and month',
        [e['asset'] for e in out['two_sales']['events'] if e['type'] == 'close'], ['B', 'A'])
    eq('two-property proceeds only enter once', sm('two_sales', 'saleNet'), 3600)
    t = out['simple_enumeration']
    eq('small universe complete count', [t['coverage']['rawCombinations'], t['coverage']['evaluated'], len(t['all']),
        len(set((x['scenarios']['quiet']['hash'] for x in t['all'])))], ['4', 4, 4, 4])
    eq('small complete action months', sorted((r['actions'][0]['month'] for r in t['all'] if r['actions'])), [1, 6, 12])
    t = out['rich_enumeration']
    common = [x for x in t['all'] if x['feasible']]
    universe = math.prod((x['choices'] for x in t['coverage']['dimensions']))
    unique = lambda x: tuple((o['hash'] for o in x['scenarios'].values()))
    fingerprints = set(map(unique, common))
    short = set(t['shortlist'])
    eq('rich stratified actual count', [len(t['all']), t['coverage']['evaluated'], t['coverage']['rawCombinations'],
        len({canonical(x['actions']) for x in t['all']})], [350, 350, str(universe), 350])
    eq('rich at least 100 actually distinct feasible monthly cash and portfolio histories',
        100 <= len(fingerprints) <= 500, True)
    eq('all simulated monthly records or explicit failure cutoff',
        all((o['valid'] for x in t['all'] for o in x['scenarios'].values())), True)
    eq('shortlist unique real outcome and within 10-20', 10 <= len(short) <= 20 and len(set(map(unique,
        [r for r in common if r['id'] in short]))) == len(short), True)
    allgroups = set(map(unique, t['all']))
    reported = t['coverage']
    eq('rich reported distinct actual paths agrees with independent ledger fingerprints',
        [reported.get('distinctMonthlyTrajectories'), reported.get('distinctFeasibleMonthlyTrajectories')],
        [len(allgroups), len(fingerprints)])
    pairs = {(r.get('trajectory'), unique(r)) for r in t['all']}
    eq('rich exported economic groups are a one-to-one match to independent cent-level monthly ledgers',
        len(pairs) == len({k for k, v in pairs}) == len({v for k, v in pairs}) and all((k is not None for k,
        v in pairs)), True)

    def peak(r):
        return max((float('inf') if t['peakDsrInfinite'] else t['peakDsr'] for t in r['scenarios'].values()))
    triples = {r['id']: (r['minCash'], r['worstWealth'], peak(r)) for r in common}
    eps = 1e-07

    def dominates(t, u):
        return t[0] >= u[0] - eps and t[1] >= u[1] - eps and (t[2] <= u[2] + eps) and (t[0] > u[0] + eps or t[1] > u[1] + eps or t[2] < u[2] - eps)
    marked = sorted((r['id'] for r in common if r['pareto']))
    independent = sorted((i for i, t3 in triples.items() if not any((dominates(other, t3) for j,
        other in triples.items() if i != j))))
    eq('independent Pareto non-dominance across minimum cash, real wealth and peak DS ratio', marked, independent)
    eq('baseline has no actions', t['all'][0]['actions'], [])
    eq('raw Cartesian product exceeds actual bounded sample', universe > 350, True)
    best = {p['id']: max((r['scenarios'][p['id']]['terminalReal'] for r in common)) for p in rich_paths}
    for k in best:
        eq('best feasible actual wealth in ' + k, t['best'][k], best[k])
    eq('regret equals max gap against same feasible set, currency only',
        all((abs(r['regret'] - max((best[k] - r['scenarios'][k]['terminalReal'] for k in best))) < 1e-06 for r in common)), True)
    eq('all failed or implementation-blocked excluded from usable wealth',
        all((r['worstWealth'] is None and r['regret'] is None and (not r['pareto']) for r in t['all'] if not r['feasible'])), True)
    for objective in ['cash', 'wealth', 'regret']:
        k = {'cash': 'minCash', 'wealth': 'worstWealth', 'regret': 'regret'}[objective]
        win = next((r for r in common if r['id'] == t['winners'][objective]))
        best_value = (min if objective == 'regret' else max)((r[k] for r in common))
        eq('winner target ' + objective, win[k], best_value)
    for name, direction in [('reverse_unknown_price', 'price'), ('reverse_unknown_delay', 'delay')]:
        test = out[name]
        eq('reverse retains unknown assumption ' + direction, [len(test['base']['blocked']),
            test['grid'][direction]['firstBlocked'], test['base']['saleNet']], [1, 0, 0])
    eq('reverse price threshold on actual sale; first gap is at month 119',
        out['reverse_price']['grid']['price']['boundary'], {'value': 21, 'failureMonth': 119, 'gap': 5,
        'previousSafe': 20})
    eq('reverse rent threshold with other wage intact', out['reverse_joint']['grid']['rent']['boundary'], {'value': 51,
        'failureMonth': 1, 'gap': 1, 'previousSafe': 50})
    eq('reverse joint wage and rent threshold', out['reverse_joint']['grid']['joint']['boundary'], {'value': 26,
        'failureMonth': 1, 'gap': 2, 'previousSafe': 25})
    eq('reverse wage, only 26% fails at 75 yuan obligations and 100 wage',
        out['reverse_wage']['grid']['wage']['boundary'], {'value': 26, 'failureMonth': 1, 'gap': 1, 'previousSafe': 25})
    eq('reverse months without pay first failure month 1', out['reverse_wage']['grid']['job']['boundary'], {'value': 1,
        'failureMonth': 1, 'gap': 75, 'previousSafe': 0})
    eq('reverse prepayment cap after first principal installment',
        out['reverse_prepay']['affordablePrepay']['largestTested'], 1100)
    eq('reverse sale delay first loses liquidity at three months', out['reverse_delay']['grid']['delay']['boundary'],
        {'value': 3, 'failureMonth': 3, 'gap': 100, 'previousSafe': 2})
    be = out['reverse_rent']['breakEven']
    eq('gross breakeven rent from 120-month residual wealth with carrying costs', [be['grossMonthlyThreshold'],
        be['netMonthlyThreshold'], be['saleNet']], [1000 / 120 + 3, 1000 / 120, 13000], 0.005)
    return {'testedPolicies': len(t['all']), 'rawActionCombinations': universe, 'commonFeasiblePolicyRules': len(common),
        'distinctCentLevelMonthlyOutcomesAmongCommon': len(fingerprints),
        'distinctAllRealizedLedgers': len(set(map(unique, t['all']))),
        'fullPathLedgerInspections': sum((len(x['scenarios']) for x in t['all'])),
        'inspectedRealizedMonths': sum((o['rows'] for x in t['all'] for o in x['scenarios'].values())),
        'shortlist': t['shortlist']}

def main():
    name = 'independent_input.json'
    (HERE / name).write_text(dump(requests))
    hashes = {f: sha((AUTHOR / f).read_bytes()) for f in ['engine.js', 'ui.js', 'ui.html', 'synthetic_household.json',
        'scenarios.json', 'calculator.html']}
    out = run_engine(requests)
    ob = canonical(out)
    (HERE / 'observed_engine_output.json.gz').write_bytes(gzip.compress(ob, mtime=0))
    stats = verify(out)
    second = run_engine([r for r in requests if r['id'] in ('rich_enumeration', 'failure', 'closing_exact',
        'trigger_future')])
    eq('identical fresh Node process, fixed input output hashes', {k: sha(canonical(v)) for k, v in second.items()},
        {k: sha(canonical(out[k])) for k in second})
    inline_requests = [r for r in requests if r['id'] in ('blank', 'annuity_standard', 'prepay_shorten', 'employment',
        'failure', 'unknown_loan_permission', 'closing_exact', 'security_late_failure', 'range_high',
        'simple_enumeration', 'reverse_wage')]
    formal = HERE.parents[2] / 'formal' / 'calculator.html'
    eq('formal calculator bytes equal frozen author artifact', sha(formal.read_bytes()), hashes['calculator.html'])
    actual_file = run_engine(inline_requests, formal)
    eq('same exposed browser-global ledger embedded in deliverable and source module', {k: sha(canonical(v)) for k,
        v in actual_file.items()}, {k: sha(canonical(out[k])) for k in actual_file})
    new_hash = sha((AUTHOR / 'engine.js').read_bytes())
    eq('same engine from initial replay to final fresh-process replay', new_hash, hashes['engine.js'])
    checks.extend([])
    bad = [c for c in checks if not c['pass']]
    report = {'reviewer': '/root/household_independent_audit', 'author': '/root/household_engine',
        'auditKind': 'engineering_only_independently_created_synthetic_cases',
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'python': platform.python_version(),
        'numpyFinancial': nf.__version__, 'node': subprocess.run([NODE, '--version'], capture_output=True, text=True,
        check=True).stdout.strip(), 'reviewedArtifacts': hashes, 'inputSHA256': sha((HERE / name).read_bytes()),
        'uncompressedOutputSHA256': sha(ob), 'scriptSHA256': sha(Path(__file__).read_bytes()),
        'adapterSHA256': sha((HERE / 'node_bridge.cjs').read_bytes()), 'requests': len(requests),
        'checksRun': len(checks), 'passed': len(checks) - len(bad), 'failed': len(bad), 'coverage': stats,
        'checks': checks}
    (HERE / 'numeric_report.json').write_text(dump(report))
    print(dump({k: v for k, v in report.items() if k not in ('checks', 'reviewedArtifacts')}))
    print(dump(bad))
    return 1 if bad else 0
if __name__ == '__main__':
    sys.exit(main())
