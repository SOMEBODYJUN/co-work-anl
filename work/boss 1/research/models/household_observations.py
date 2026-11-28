"""Reproducible descriptive arithmetic; not fitted causal effects or forecasts."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'household_observations_input.json'
data = json.loads(INPUT.read_text())
h = data['household']
income_prev = h['income'] / (1 + h['income_nominal_growth'])
consumption_prev = h['consumption'] / (1 + h['consumption_nominal_growth'])
annual = data['equity_usd_gross_annual']
wealth = 1.0
for r in annual.values():
    wealth *= 1 + r / 100
out = {
    'schema': 'cncrisis-descriptive-arithmetic.v1',
    'input_kind': 'observed_publication',
    'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'household': {
        'consumption_to_disposable_income_ratio': h['consumption'] / h['income'],
        'previous_year_ratio_reconstructed_from_rounded_growth': consumption_prev / income_prev,
        'income_minus_consumption_yuan_per_person': h['income'] - h['consumption'],
        'meaning': 'NBS household survey same-period mean ratio, not national-accounts savings rate or bank cash change; reconstructed prior year approximate because reported growth rounded',
    },
    'equity': {
        'index': 'MSCI China A Onshore', 'currency': 'USD', 'return': 'gross total return',
        'period': '2016-01-01 to 2025-12-31; ten full calendar years',
        'cumulative_return': wealth - 1, 'annualized_return': wealth ** (1 / len(annual)) - 1,
        'negative_calendar_years': sum(v < 0 for v in annual.values()),
        'meaning': 'Derived from rounded official annual returns; not Oct2026 rolling10y, not CNY, no fees/taxes, no forecast',
    },
}
(HERE / 'household_observations.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(out, ensure_ascii=False, indent=2))
