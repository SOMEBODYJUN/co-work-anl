"""Fingerprint the displayed synthetic household under the packaged scenario assumptions; never real household data."""
import gzip
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
import independent_numeric as a
raw_house = (a.AUTHOR / 'synthetic_household.json').read_bytes()
raw_sc = (a.AUTHOR / 'scenarios.json').read_bytes()
h = json.loads(raw_house)
ps = json.loads(raw_sc)
if isinstance(ps, dict):
    ps = ps['scenarios']
out = {}
for budget in (400, 500):
    request = {'id': 'demo', 'op': 'assess', 'household': h, 'scenarios': ps, 'limit': budget}
    res = a.run_engine([request], a.HERE.parents[2] / 'formal' / 'calculator.html')['demo']
    raw = a.canonical(res)
    raw_path = a.HERE / f'demo_{budget}_output.json.gz'
    raw_path.write_bytes(gzip.compress(raw, mtime=0))
    all_ = res['all']
    common = [r for r in all_ if r['feasible']]
    sig = lambda r: tuple((o['hash'] for o in r['scenarios'].values()))
    out[str(budget)] = {'differentRules': len(all_), 'commonFeasibleRules': len(common),
        'differentMonthlyTracesInCommon': len(set(map(sig, common))), 'allDifferentMonthlyTraces': len(set(map(sig,
        all_))), 'raw': res['coverage']['rawCombinations'], 'allScenarios': len(ps),
        'allPathReplays': len(all_) * len(ps),
        'observedMonths': sum((s['rows'] for r in all_ for s in r['scenarios'].values())),
        'shortlist': res['shortlist'], 'fullReplayedResultSHA256': a.sha(raw), 'rawCompressedFile': raw_path.name}
summary = {'scope': 'synthetic sample, distinct economics by cent-level monthly cash, debts, financial/property/vehicle value, rent, receivables, net worth, unpaid, extra principal, sale and optional expenses over every scenario', 'inputHouseholdSha256': a.sha(raw_house), 'inputScenarioSha256': a.sha(raw_sc), 'engineSHA256': a.sha((a.AUTHOR / 'engine.js').read_bytes()), 'run': out}
(a.HERE / 'demo_crosscheck.json').write_text(a.dump(summary))
print(a.dump(summary))
