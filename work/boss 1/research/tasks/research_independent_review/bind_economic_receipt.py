"""Bind individually adjudicated economic checks to one frozen release candidate."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
ROOT = HERE.parents[4]
COMMIT = '1580e869769a9410b88d040acf08bab394c6f9d2'
ACTOR = '/root/research_independent_review'
SELF = 'research/tasks/research_independent_review/'
FORMAL = ['formal/report.md', 'formal/judgments.json', 'formal/scenarios.json', 'formal/calculator.html']


def read(path):
    return json.loads((WORK / path).read_text())


def digest(path):
    return hashlib.sha256((WORK / path).read_bytes()).hexdigest()


def bindings():
    state = read('research_state.json')
    graph = read('research/graph_current.json')
    status = read('research/receipts/graph_status_after_audit.json')
    receipts = read('research/receipts/proposals_applied.json')
    old = read(SELF + 'proposal_receipt.json')
    judgments = read('formal/judgments.json')
    for path in FORMAL:
        stored = subprocess.check_output(['git', 'show', COMMIT + ':work/boss 1/' + path], cwd=ROOT)
        assert hashlib.sha256(stored).hexdigest() == digest(path), path
    assert len(graph['nodes']) == 16 and len(graph['edges']) == 13 and graph['revision'] == 31
    assert not status['unresolved'] and not status['unresolved_edges']
    for typ in ['nodes', 'edges']:
        assert all(row == state[typ][row['id']] for row in graph[typ])
    for e in graph['edges']:
        assert e['mode'] == 'ALL' and len(e['tails']) >= 2 and e['status'] == 'current'
        assert all(e[f] for f in ['conditions', 'counterevidence', 'falsifier', 'lag', 'mechanism'])
        assert all(x in state['sources'] or x in state['nodes'] for x in e['tails'] + e['counterevidence'])
    assert len(judgments['judgments']) == 9
    assert [r['id'] for r in judgments['ranked_paths']] == ['continuity','severe','recovery']
    for row in judgments['judgments']:
        assert row['probability'] is None and all(row[k] for k in ['change_condition','time_window','household_implication'])
        assert all(id in state['sources'] for id in row['evidence_ids'])
        node = state['nodes'][row['id']]
        assert row['verdict'] == node['statement'] and row['graph_revision'] == node['revision']
    assert len(receipts) == 54 and len(old['reviews']) == 18
    for r in old['reviews']:
        id = r['id']
        assert digest('research/proposals/' + id + '.json') == r['file_sha256']
        assert state['proposals'][id]['status'] == 'applied'
        track = [v for v in receipts if v['result']['id'] == id]
        assert [v['command'][0] for v in track] == ['proposal','proposal-review','apply']
        assert track[1]['result']['reviewer'] == ACTOR and track[1]['result']['verdict'] == r['verdict']
    return state


DECISIONS = {
    'sources': (
        '核两期财政原稿、偿付/县和省期限表、两行四份原PDF及六监管XLS的770格、覆盖范围脚注；宏观、历史、指数原值与作者观点分列。QA001与PF029同一事件；截至11月27日已公开信息。',
        'research/data_reconciliation.md research/source_lineage.json research/data/audit_crosscheck_record.json research/tasks/property_fiscal/sources.json research/tasks/property_fiscal/fiscal_releases.csv research/tasks/property_fiscal/supplemental.csv research/tasks/bank_research/sources.json research/tasks/bank_research/statement_extract.csv research/tasks/bank_research/regulatory_series.csv',
        'independent_accounts.json independent_history.json'),
    'frameworks': (
        '独立核七家原文的动作、事前判断及事后反例；复算Setser期末债务率31.846%—32.126%、日美峰后住房/工资/股权及三套历史窗口。Koo资金流量、Sufi全文、Pettis日本反例已落实。',
        'research/framework_cards.md research/tasks/history_framework_review/framework_review.md research/tasks/history_framework_review/history.md research/tasks/history_framework_review/official_inputs.json research/tasks/history_framework_review/results.json',
        'history_audit.py independent_history.json'),
    'models': (
        '逐项核11作业指纹；独立重建训练/校准、事件检出、QR和银行20个条件行。JST原错及修复保留；新HGB校准1/13、Brier0.18540，负斜率非错列，logit3/13不足授中国概率。单版桥接0.64347劣于0.34545。通过限于这些用途裁决。',
        'research/model_results.md research/method_runs.md research/models/model_decisions.md research/historical_model_correction.md research/models/jst_audited_20261127/data_manifest.json compute/ledger.json research/tasks/bank_research/capital_and_liquidity_results.json research/models/equity_real_return_input.json research/models/equity_real_return.json',
        'model_audit.py independent_models.json accounts_audit.py independent_accounts.json history_audit.py independent_history.json'),
    'hyperedges': (
        '逐条核13边的前提、传导、反例、可观测证伪、时滞；18文件各自独立签评、54个实际统一入口操作均匹配。旧版退出必然定价、财政修复唯一和无关外币必要条件均已处理。图的当前状态仅指证据和版本。',
        'research/graph_initial.json research/graph_current.json research/graph_adjudication.md research/receipts/proposals_applied.json research/receipts/graph_status_after_audit.json research/audit_proposal_pack.json',
        'proposal_receipt.json'),
    'judgments': (
        '五个必答题明确有序、九部门裁决与图逐句对应，有反例、时窗和家庭行动。2027四窗按合同拆，从2021至约2030为准备期。拒绝必熊，但不将2016—25人民币实际含息+13.78%当预测。',
        'formal/report.md formal/judgments.json formal/scenarios.json research/challenges.md research/equity_verdict.md research/scenario_design.md',
        'independent_history.json proposal_receipt.json')
}

if __name__ == '__main__':
    state = bindings()
    checks = []
    for id, (reason, own, audit) in DECISIONS.items():
        files = own.split() + [SELF + f for f in ['economics_review.md'] + audit.split()]
        checks.append(dict(id=id, verdict='pass', evidence=reason, artifacts=files))
    paths = sorted({*FORMAL, *[f for chk in checks for f in chk['artifacts']], SELF+'bind_economic_receipt.py'})
    ids = ('MA001 MA002 MA003 MA004 MA007 MA008 MA009 MA011 MT001 EQ001 EQ002 EQ003 QA001 PF009 PF010 PF017 PF018 PF019 PF020 PF023 PF025 PF026 PF027 PF028 PF029 PF030 PF031 PF032 PF033 PF034 PF035 PF036 PF037 BK001 BK002 BK003 BK004 BK005 BK006 BK007 BK008 BK009 BK010 BK011 BK012 BK013 BK014 FW001 FW002 FW003 FW004 FW005 FW006 FW007 FW008 FW009 FW010 HX001 HX002 HX003 HX004 HX006 HX007 HX008 HX009 HX010 HX011 HX012 HX013 HX014 HX016 HX017 HX018 HX019').split()
    records = {id: {k:state['sources'][id][k] for k in ['revision','body_sha256','url','observation_period'] if k in state['sources'][id]} for id in ids}
    doc = {
        'schema': 'independent-economic-scope-review.v1', 'reviewer': ACTOR, 'author': 'boss 1', 'cycle': 1,
        'input_kind': 'real_research', 'as_of': '2026-11-27 America/Los_Angeles',
        'reviewed_at_utc': datetime.now(timezone.utc).isoformat(), 'frozen_commit': COMMIT, 'graph_revision':31,
        'registered_sources':len(state['sources']), 'registered_searches':len(state['searches']),
        'checks':checks, 'file_sha256':{p:digest(p) for p in paths}, 'load_bearing_source_records':records,
        'scope':'此回执只签五项经济内容；未授予发布。', 'other_status':{
            'household_engine':'另一独立家庭审计者对正式内联引擎执行87个请求、179项核对。经济审计者没有自行操作真实浏览器。',
            'offline_ui':'独立正式文件启动失败127，0操作、截图、下载；无法通过。',
            'fresh_restore':'另一独立执行者在新克隆实跑；此回执尚未审核重放结果。'},
        'source_preservation':'4PDF和6XLS为本次本机原件，原SHA、页号/单元格及数字已固化；git未保存被忽略的原文件缓存。新克隆使用持久化CSV/JSON重放。',
        'official_notice_crosscheck':{'source':'QA001','corroborates':'PF029','targets':[],
            'impact_note':'仅验证已有PF029接管事实，公告期限未用于本轮新判断或家庭参数；不会改变已有节点。'}}
    target = HERE/'economic_checks.json'
    target.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    print(target.name, digest(SELF+target.name), 'economics_review.md', digest(SELF+'economics_review.md'))
