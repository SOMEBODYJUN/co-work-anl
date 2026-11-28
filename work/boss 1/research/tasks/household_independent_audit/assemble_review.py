"""Assemble the independent evidence matrix after fresh numerical, sample, packaging and browser runs."""
import datetime as dt
import gzip
import hashlib
import json
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'household_engine'

def load(n):
    return json.loads((HERE / n).read_text())

def sha(b):
    return hashlib.sha256(b).hexdigest()

def dump(x):
    return json.dumps(x, ensure_ascii=False, indent=2) + '\n'
report = load('numeric_report.json')
demo = load('demo_crosscheck.json')
package = load('packaging_report.json')
ui = load('offline_attempt.json')
old = load('pre_repair_findings.json')
checks = report['checks']
clusters = {'起始金额与显式区间': ['empty household', 'empty original', 'editable recorded', 'unknown center', 'explicit upper',
    'invalid assumption'], '等额本息、零利率与一期': ['annuity_zero', 'annuity_one', 'annuity_standard'],
    '等额本金、浮息重定价与定息对照': ['equal principal', 'floating only', 'floating contract', 'fixed_rate_control'],
    '部分预付降供缩期与现金来源': ['prepay_', 'recast reduces', 'shorten saves', 'fully prepaid', 'salary-funded',
    'small enumerated universe'], '合同限制、费用与未知许可': ['contract_', 'unknown_loan', 'unknown_home', 'unknown_car',
    'unknown_security', 'unknown_lien', 'contract can prohibit'], '负资产、解押先行、出售交割与关联贷款只扣一次': ['closing_', 'sale delayed',
    'rent and carry', 'sale normal', 'closing month', 'closing proceeds', 'multiple sales', 'two-property',
    'same property cannot'], '无法出售、必要车与替代出行、住房处理': ['unsellable', 'wait_limit', 'occupied_no_alternative',
    'necessary_car', 'replacement mobility'], '空置、成交净额、待收款与受限金融资产': ['full vacancy', 'vacancy carry',
    'discounted lease', 'trade financial', 'four staged sales', 'pending financial', 'restricted deposit',
    'free deposit', 'pledged security'], '证券杠杆同步还贷、延迟结算与禁止解押': ['contract-authorized margin', 'security liquidation',
    'delayed margin'], '失业、复工、投资总回报与通胀购买力': ['independent wage', 'investment total', 'one-off loss',
    'real wealth deflation'], '失败截断、欠款保留、消费预算分类与失败后不得比较终值': ['guarantee call', 'failed cash', 'failed month',
    'failure source', 'unfunded optional', 'failed rich', 'no feasible', 'all failed or'],
    '最低生活与储备约束': ['mandatory minimum', 'reserve breach', 'discretionary loan'], '跨策略同外生输入与无未来信息': ['no knowledge',
    'order before', 'threshold lists', 'future loss', 'identical exogenous'],
    '小组合全量，大组合分层、经济轨迹与逐月实跑': ['small universe', 'small complete', 'rich stratified', 'rich reported', 'rich exported',
    'rich at least', 'all simulated monthly', 'shortlist unique', 'baseline has', 'raw Cartesian'],
    '排序按目标、同可行集后悔比较': ['best feasible', 'regret equals', 'winner target', 'independent Pareto'],
    '逆向压力、租售盈亏与预付款上限': ['reverse wage', 'reverse retains', 'reverse price', 'reverse rent', 'reverse joint',
    'reverse months', 'reverse prepayment', 'reverse sale', 'gross breakeven'], '多进程复现及单文件内置代码重放': ['identical fresh',
    'formal calculator bytes', 'same exposed browser-global', 'same engine from']}
items = []
for name, prefixes in clusters.items():
    matched = [c for c in checks if any((c['check'].startswith(p) for p in prefixes))]
    items.append({'criterion': name, 'verdict': 'pass' if matched and all((x['pass'] for x in matched)) else 'fail',
        'tested': len(matched), 'failedChecks': [x['check'] for x in matched if not x['pass']],
        'evidence': 'numeric_report.json', 'checkPrefixes': prefixes})
actual = {f: sha((AUTHOR / f).read_bytes()) for f in report['reviewedArtifacts']}
version_ok = report['reviewedArtifacts'] == actual and actual['calculator.html'] == package['sha256'] == ui['htmlSha256'] and (actual['engine.js'] == demo['engineSHA256']) and (actual['synthetic_household.json'] == demo['inputHouseholdSha256']) and (actual['scenarios.json'] == demo['inputScenarioSha256'])
input_ok = report['inputSHA256'] == sha((HERE / 'independent_input.json').read_bytes()) and report['uncompressedOutputSHA256'] == sha(gzip.decompress((HERE / 'observed_engine_output.json.gz').read_bytes())) and (report['scriptSHA256'] == sha((HERE / 'independent_numeric.py').read_bytes())) and (report['adapterSHA256'] == sha((HERE / 'node_bridge.cjs').read_bytes()))
default_limit = int(re.search('\\blimit\\s*=\\s*(\\d+)', (AUTHOR / 'ui.js').read_text()).group(1))
example = demo['run'].get(str(default_limit), {})
default_coverage = example.get('differentMonthlyTracesInCommon', 0)
items += [{'criterion': '默认合成演示跨全部情景实际不同的可行月度轨迹', 'verdict': 'pass' if 100 <= default_coverage <= 500 else 'fail',
    'engineDefaultDisplayLimit': default_limit, 'actual': example, 'evidence': 'demo_crosscheck.json'},
    {'criterion': '版本、脚本、原始输入和输出哈希一致', 'verdict': 'pass' if version_ok and input_ok else 'fail',
    'artifactsMatch': version_ok, 'inputOutputCodeMatch': input_ok,
    'evidence': 'numeric_report.json, packaging_report.json, offline_attempt.json'}, {'criterion': '单文件源码、内联参数和静态网络依赖',
    'verdict': 'pass' if all((x is True or x == [] for x in package['checked'].values())) else 'fail',
    'evidence': 'packaging_report.json'}]
for text in ['真实 file:// 离线打开及真实浏览器请求与 console 监听', '显式示例、收入/区间与房产、车辆、贷款增删后重算', '界面情景/目标/假设类型可编辑且切换结果生效',
    'JSON 往返、全策略与各月 CSV 下载内容', '实际月表与图表数据切换、桌面和 390/320px 手机截图目检']:
    items.append({'criterion': text,
        'verdict': 'blocked' if ui['verdict'] == 'blocked' else 'pending_visual_review' if ui['verdict'] == 'automated_interactions_pass' else 'fail', 'evidence': 'offline_attempt.json', 'completedBrowserActions': len(ui['actions'])})
engine = all((i['verdict'] == 'pass' for i in items[:-5])) and report['failed'] == 0
res = {'reviewer': '/root/household_independent_audit', 'implementationAuthor': '/root/household_engine',
    'projectActor': 'boss 1', 'completedAt': dt.datetime.now(dt.timezone.utc).isoformat(),
    'numericEngineVerdict': 'pass' if engine else 'fail', 'offlineUIVerdict': ui['verdict'],
    'realDataScope': 'Independent engineering checks use invented CNY values. They do not calibrate scenarios or model the user’s household.', 'binding': {'engine': actual['engine.js'], 'packagedHTML': actual['calculator.html'], 'independentInput': report['inputSHA256'], 'uncompressedResults': report['uncompressedOutputSHA256']}, 'items': items}
(HERE / 'audit_matrix.json').write_text(dump(res))
print(dump({k: v for k, v in res.items() if k != 'items'}))
