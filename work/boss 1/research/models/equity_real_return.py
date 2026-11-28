"""Reproduce the declared 2016–2025 CNY total-return window; not a forecast."""
from pathlib import Path
import json, math
R=Path(__file__).resolve().parent
x=json.loads((R/'equity_real_return_input.json').read_text())
nominal=math.prod(1+y/100 for y in x['annual_net_total_return_percent'])
prices=x['cpi_2024_12']/x['cpi_2015_12']*(1+x['cpi_2025_12_yoy_percent']/100)
result={'window':'2015 year end to 2025 year end','currency':'CNY','nominal_net_total_return_percent':100*(nominal-1),'cpi_factor':prices,'real_net_total_return_percent':100*(nominal/prices-1),'real_annualized_percent':100*((nominal/prices)**.1-1),'negative_calendar_years':sum(y<0 for y in x['annual_net_total_return_percent']),'interpretation':'Index NET dividend-withholding convention, not all household fees/taxes; December monthly-average CPI approximates year-end purchasing power. Rounded published annual returns and 2025 CPI limit precision. Historical observation does not predict a future ten-year window.'}
(R/'equity_real_return.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
