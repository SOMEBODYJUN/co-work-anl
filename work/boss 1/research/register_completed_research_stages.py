"""Register only completed research batches 03–12; not UI/audit/release acceptance."""
from pathlib import Path
import subprocess,json
W=Path(__file__).resolve().parents[1]
ROOT=W.parents[1]
base=[str(ROOT/'.venv-methods/bin/python'),str(ROOT/'work.py'),'--workspace',str(W)]
searches=[str(p.relative_to(W)) for p in sorted((W/'research/searches').glob('*.json'))]
batches=[
('s03_acquisition',['research/acquisition.md','research/source_lineage.json','research/data_dictionary.md']+searches,'156条记录按112原发定位组/104事件组归并，45批实际检索；不是独立样本数。真实原表、反证与访问失败保留。'),
('s04_vintages',['research/data_reconciliation.md','research/data_dictionary.md','research/models/activity/data_manifest.json','research/models/jst_audited_20261127/data_manifest.json','research/models/equity_real_return_input.json'],'统计期/发布期/旧新GDP版本、毛净土地/本金本息/CET1、币种股息与未知标签逐项对齐。'),
('s05_methods',['research/method_runs.md','research/historical_model_correction.md','research/models/model_decisions.md','research/models/compute-initial.json','research/models/compute-china-activity.json','research/models/compute-audited-history.json','compute/ledger.json','research/receipts/methods_doctor.json'],'已实跑11作业；保留被拒模型、纠错新输入与原始失败结果；本地CPU和预算已记。'),
('s06_viewpoints',['research/framework_cards.md','research/tasks/history_framework_review/framework_review.md','research/tasks/history_framework_review/review_receipt.json','research/tasks/property_fiscal/mechanisms_and_reading.md'],'七组原文核读与独立反证，采用问题/制度/动作，纠正日本历史、债务算术及需求供给口径；不作作者评分。'),
('s07_property',['research/tasks/property_fiscal/analysis_property.md','research/tasks/property_fiscal/property_releases.csv','research/tasks/property_fiscal/cities_price_202610.csv','research/tasks/property_fiscal/recompute.py','research/tasks/property_fiscal/results.json'],'实算开发链收缩、70城分化、二手与开发融资区别、新旧项目规则及交付反证。'),
('s08_fiscal',['research/tasks/property_fiscal/analysis_fiscal.md','research/tasks/property_fiscal/fiscal_releases.csv','research/tasks/property_fiscal/supplemental.csv','research/tasks/property_fiscal/results.json'],'土地毛净资源、预算/实付、法定债滚续与两省到期、平台退出和地方成本反例完成。'),
('s09_households',['research/analysis_households.md','research/models/household_observations.py','research/models/household_observations_input.json','research/models/household_observations.json'],'居民实际收入与消费、小微调查范围、利润回款、就业和家庭收入关联完成；用户个人金额不臆填。'),
('s10_banks',['research/tasks/bank_research/banks.md','research/tasks/bank_research/mechanisms.md','research/tasks/bank_research/statement_extract.csv','research/tasks/bank_research/regulatory_series.csv','research/tasks/bank_research/capital_and_liquidity_results.json','research/tasks/bank_research/bank_accounts.py','research/tasks/bank_research/compute_jobs.json'],'四份真实银行输入及披露CET1核算、条件额外损失/RWA敏感性、流动性/偿付区别、实际接管和承接完成。'),
('s11_external',['research/analysis_external.md','research/models/activity/data_manifest.json'],'外需和制造缓冲、价格成本及政策净到账范围已核；保留外部共振与私人自主恢复两条竞争解释。'),
('s12_history',['research/tasks/history_framework_review/history.md','research/tasks/history_framework_review/official_inputs.json','research/tasks/history_framework_review/recompute.py','research/tasks/history_framework_review/results.json','research/tasks/history_framework_review/named_paths.csv','research/tasks/history_framework_review/event_scan.csv','research/historical_model_correction.md'],'日本美国逐年十年、18国规则筛选敏感性、韩国短外债、中国置换棚改实际历史完成；旧预警原结果与最新纠错另列。')]
for sid,files,note in batches:
 for f in files:
  if not (W/f).is_file():raise FileNotFoundError(f)
 p=subprocess.run(base+['stage','--id',sid,'--files']+files+['--note',note],cwd=ROOT,capture_output=True,text=True)
 if p.returncode:print(p.stdout,p.stderr);raise SystemExit(p.returncode)
 q=subprocess.run(base+['checkpoint','--message',f'{sid}: {note}','--paths',str((W/'research_state.json').relative_to(ROOT)),str(Path(__file__).relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 if q.returncode:print(q.stdout,q.stderr);raise SystemExit(q.returncode)
 z=json.loads(q.stdout)
 nxt=subprocess.run(base+['session','next','--actor','boss 1'],cwd=ROOT,capture_output=True,text=True)
 data=json.loads(nxt.stdout)
 print(json.dumps({'stage':sid,'files':len(files),'commit':z['commit'],'next':data['next_action'],'complete':data['complete']},ensure_ascii=False),flush=True)
