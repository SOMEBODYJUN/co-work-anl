"""Independent numerical checks. The upstream CLI receipt is regenerated before comparison."""
import hashlib
import importlib.metadata
import importlib.util
import json
import subprocess
import sys
import warnings
from decimal import Decimal
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "work.py").is_file())
REF = ROOT / "vendor" / "numpy-financial" / "_financial.py"
spec = importlib.util.spec_from_file_location("pinned_financial", REF)
npf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(npf)
local = str(HERE.relative_to(ROOT))
subprocess.run([sys.executable, "work.py", "--workspace", "work/boss 1", "methods", "run", "--name", "loan",
                "--input", local + "/loan_input.json", "--output", local + "/loan_work_reference.json"],
               cwd=ROOT, stdout=subprocess.DEVNULL, check=True)
reference = json.loads((HERE / "loan_work_reference.json").read_text())
contract = json.loads((HERE / "loan_input.json").read_text())
js = r"""
const E=require('./engine.js'),fs=require('fs'),x=JSON.parse(fs.readFileSync(0,'utf8'));
const scenario={id:'neutral',name:'无冲击',paths:[]},baseline=E.baseStrategy();
const h={...E.blank(),minimumLiving:0,cash:400000,loans:[{...E.templates.loans,id:'test',principal:x.principal,annualRate:x.annual_rate,months:x.months}]};
const r=E.simulate(h,scenario,baseline);
console.log(JSON.stringify(r.rows.slice(0,x.months).map(z=>({payment:z.principal+z.interest,interest:z.interest,principal:z.principal,balance:z.debt}))));
"""
def run_js(data):
    result = subprocess.run(["node", "-e", js], cwd=HERE, input=json.dumps(data), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

comparisons = []
for data in [contract, {"principal": 1200, "annual_rate": 0, "months": 12},
             {"principal": 12345, "annual_rate": .0576, "months": 1},
             {"principal": 92761.21, "annual_rate": .0345, "months": 97}]:
    rows = run_js(data)
    principal, annual, periods = data["principal"], data["annual_rate"], data["months"]
    rate = annual / 12
    per = np.arange(1, periods + 1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        payment = float(-npf.pmt(rate, periods, principal))
        interest = -npf.ipmt(rate, per, periods, principal)
        capital = -npf.ppmt(rate, per, periods, principal)
    balance = principal - np.cumsum(capital)
    differences = {
        "payment": max(abs(r["payment"] - payment) for r in rows),
        "interest": max(abs(r["interest"] - i) for r, i in zip(rows, interest)),
        "principal": max(abs(r["principal"] - p) for r, p in zip(rows, capital)),
        "balance": max(abs(r["balance"] - b) for r, b in zip(rows, balance)),
    }
    assert max(differences.values()) < 1e-5
    if data is contract:
        for r, rr in zip(rows, reference["result"]["schedule"]):
            for k in ("payment", "interest", "principal", "balance"):
                assert abs(r[k] - rr[k]) < 1e-5
    comparisons.append({"contract": data, "compared_periods": len(rows),
                        "max_abs_error_cny": {k: float(v) for k, v in differences.items()}})

# Independent Decimal ledger: sale closes in month 3 and clears two liens once.
D = Decimal
opening = D(100)
manual_cash = [
    opening + D(10) - D(".5"),
    opening + 2 * (D(10) - D(".5")),
    opening + 2 * (D(10) - D(".5")) + D(200) - D(8) - D(70) - D(".5")
]
manual_script = r"""
const E=require('./engine.js');
const p={...E.templates.properties,id:'house',canSell:true,lock:1,use:'let',value:100,saleValue:200,rent:10,carry:0,saleLag:2,closingFee:4,saleFee:.02};
const h={...E.blank(),cash:100,minimumLiving:0,properties:[p],loans:[[50,.12],[20,0]].map(([principal,annualRate],i)=>({...E.templates.loans,id:'L'+i,collateral:'house',method:'bullet',months:12,principal,annualRate,canPrepay:true,allowFull:true,prepayMax:"unlimited",prepayPeriodMax:"unlimited",salePayoffRule:"same_terms",salePayoffFeeBase:"balance",prepayFrom:1,prepayFee:0,settlementFee:0,transferWithLien:true}))};
const r=E.simulate(h,{id:'neutral',name:'平',paths:[]},{id:'sale',actions:[{kind:'list',asset:'house',month:1}]});
console.log(JSON.stringify(r.rows.slice(0,3).map(r=>r.cash)));
"""
actual = json.loads(subprocess.run(["node","-e",manual_script],cwd=HERE,capture_output=True,text=True,check=True).stdout)
assert all(abs(float(x)-y)<1e-8 for x,y in zip(manual_cash,actual))
receipt = {"scope": "Contract checks and independently calculated synthetic transactions",
           "python": sys.version.split()[0], "numpy": np.__version__,
           "numpy_financial_distribution": importlib.metadata.version("numpy-financial"),
           "source": str(REF.relative_to(ROOT)), "source_sha256": sha(REF), "engine_sha256": sha(HERE/"engine.js"),
           "work_py_command": "python work.py --workspace 'work/boss 1' methods run --name loan --input INPUT --output RESULTS",
           "work_reference_sha256": sha(HERE/"loan_work_reference.json"),
           "comparisons": comparisons, "decimal_sale_cash": [str(x) for x in manual_cash], "js_sale_cash": actual,
           "verdict": "pass"}
(HERE/"python_reference_checks.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(receipt,ensure_ascii=False))

