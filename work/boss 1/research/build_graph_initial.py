"""First graph version: conditional mechanisms, with explicit counterevidence; no learned weights."""
import json
from pathlib import Path

W = Path(__file__).resolve().parents[1]
graph = {'nodes': [], 'edges': []}
for topic in ['property_fiscal', 'bank_research']:
    candidate = json.loads((W / f'research/tasks/{topic}/graph_candidates.json').read_text())
    for section in graph:
        graph[section].extend(candidate[section])

def node(id, kind, statement, evidence):
    graph['nodes'].append(dict(id=id, kind=kind, statement=statement, evidence=evidence))

def edge(id, tails, head, conditions, mechanism, counterevidence, falsifier, lag):
    graph['edges'].append(dict(id=id, tails=tails, head=head, mode='ALL', conditions=conditions,
                              mechanism=mechanism, counterevidence=counterevidence, falsifier=falsifier, lag=lag))

node('J-DEMAND', 'judgment', '居民和内需小微的收入、回款与资产负债表约束共同抑制私人支出，信贷需求弱与脆弱借款人的供给约束并存，无法据总量识别各自份额。', ['MA003','MA004','MA008','FW002','FW003'])
node('J-JOBS', 'judgment', '全国就业与实际居民收入总量并未显示同步塌陷，但地产、地方项目和小微相关家庭未来12—24个月的可变薪酬、招聘与回款风险高于总量读数。', ['MA001','MA002','MA003','MA008'])
node('J-MACRO', 'judgment', '未来12—24个月首位路径是渐进滚续与局部承损、地产财政拖累和制造出口增长并存，私人收入与资产修复不均；严重信用收缩次位，有效需求修复是可改变主路径的政策分支。', ['MA001','MA002','MA007','PF018','PF026','PF027','BK001','BK002'])
node('J-DECADE', 'judgment', '从2021年地产高位起计，到约2030年前后的多年调整是应准备的长路径；从2026年再追加整整十年全面停滞或连续股市下跌，缺乏可迁移的历史和会计依据。', ['PF003','PF007','PF009','FW001','FW002','FW003','MA009'])
node('J-EQUITY', 'judgment', '拒绝把地产与收入调整直接推出A股未来十年必熊。市场回报须分别看上市公司利润、估值、股息、币种和买入窗口；近期必要支出不得依赖权益反弹。', ['MA009','MA001','MA007'])
node('A-HOUSEHOLD', 'action', '现在先核到账收入、必要支出、合同本息和资产真实变现时点，按120月逐情景现金失败先筛方案，再比较提前还贷与净资产；触发出售应早于资金耗尽，现金充足家庭保留长期分散投资选择。', ['MA003','MA008','PF010','PF028','FW003'])
node('M-MODEL-USE', 'method', '本轮历史HGB拒用主预警，logit仅比较；中国PMI桥接和DFM未稳定胜过简单基线，拒绝中国危机概率与精确GDP点预测，采用可复算会计和条件敏感性完成裁决。', ['MT001'])

edge('H-DEMAND-REPAIR', ['MA003','MA004','MA008'], 'J-DEMAND',
     ['借款与消费意愿受回款、收入和资产负债表影响，非简单认为降息必然创造净新增贷款。', '调查均值、样本构成与宏观净流量保留边界，不把同一家庭的行为从总量配对出来。'],
     '收入预期与抵押品/净值约束促使部分家庭偿债、增储备，企业需求弱降低投资和外部融资意愿；已有高债与无现金者仍可能被信贷配给。',
     ['MA001','MA002','MA003'],
     '私人非地产投资、家庭实际消费/收入、同框小微回款与借款意愿在多个季度共同恢复，将削弱持续修复主张；仅总社融上升不足以识别私人需求。',
     '实际订单与回款按月，投资与债务存量修复按季度至数年。')
edge('H-FISCAL-INCOME', ['J-FISCAL','MA001','MA008'], 'J-JOBS',
     ['借款主体或雇主实际依赖土地/地方项目，且应收未兑现；非把全国基金支出减额均摊到所有家庭。', '企业无充足现金、其他客户收入或已到账清欠资金抵补。'],
     '财政迟付或项目缩减增加供应商应收与周转占用，先约束招聘和可变工资，再传至家庭支出；账面利润上升可以与现金工资风险并存。',
     ['MA003','PF023','PF026','MA001'],
     '同一批企业应收账龄缩短、拖欠实付、工资与招聘恢复且非靠新增高息短债维持，会切断本链。',
     '结算与工资1—6个月，招聘和投资3—12个月。')
edge('H-MACRO-SPLIT', ['J-PROPERTY','J-FISCAL','J-DEMAND','MA001','MA007'], 'J-MACRO',
     ['出口与制造的实际增长部分延续，但对旧地产和地方就业的接替受地区、技能与收入分配约束。', '债务滚续、资本补充和项目交付继续执行，没有发生跨区域支付失灵。'],
     '旧开发链损失通过投资减少、财政收缩和私人修复压低内需；新制造与服务增加值支撑总量，渐进处置延长损失承担时间并保支付连续。',
     ['PF026','PF029','MA003','BK004'],
     '若大规模净新增可用财政资金实际转至居民/供应商并持续拉动私人回款与投资，转向有效恢复；若外需骤降与多地银行融资/资本缺口共振，转向严重下行。',
     '3—6个月看到账与订单，2027年看持续性，资产负债表修复跨3—5年。')
edge('H-2027-CAPITAL', ['BK-ICBC-FLOOR','J-BANKS'], 'J-2027',
     ['以2026年9月披露RWA作静态参照，新增资本按实际入账时点认定。'],
     '2027年初大行附加资本要求上升占用缓冲；能否提前留存或实缴决定信贷扩张约束，不能从规则日期推断全国资不抵债。',
     ['BK003','BK009','BK014'],
     '实际合格资本到位或RWA管理使各项要求持续满足，则该日期不产生现金或授信断点。',
     '2027-01-01规则生效，实际注资与季度资本披露按月季核验。')
edge('H-DECADE-REPAIR', ['J-PROPERTY','J-FISCAL','J-DEMAND','FW001','FW002'], 'J-DECADE',
     ['房地产存量过hang、地方收入结构与私人收入分配需要多年调整。', '政策以展期、项目保交付和渐进承损为主，尚未全面转为及时可用的居民收入与损失重组。'],
     '滚续避免集中清算但不创造原项目现金收益，损失会经利润、财政和收入逐年分担；结构替代与收入修复速度决定持续期，日历年本身不决定终点。',
     ['PF026','PF037','MA001','MA003','MA006'],
     '家庭收入份额和私人投资持续恢复、地产库存与债务负担可比下降、地方税基替代土地并正常付款，能把长期拖累缩短；不能以单日股价否证或证实。',
     '地产2021高位到约2030的跨周期窗口，非从2026固定再数十年。')
edge('H-EQUITY-SEPARATION', ['J-DECADE','MA009','MA001'], 'J-EQUITY',
     ['用含股息总回报、明确币种和持有窗口，上市企业与全国地产口径不同。'],
     '利润、估值和股息共同决定股市回报，国内地产现金流不是全部上市利润；期初估值和政策反应可使弱宏观中的某些年份上涨。',
     ['MA009','PF009'],
     '特定市场在固定币种/费用/窗口下的长期总回报可为负，但须由其盈利与估值路径证实，不能仅用宏观危机命名推出。',
     '市场可提前定价；年度和十年复利分别检验。')
edge('H-HOUSEHOLD-ACTION', ['J-JOBS','J-PROPERTY','J-DEMAND','J-EQUITY'], 'A-HOUSEHOLD',
     ['用户真实合同、可动用现金及资产处置限制明确；默认金额为空。', '策略不可预知未来，只按预先动作或当期可见现金触发，未及时变现即记录失败。'],
     '高净值但月度现金不足仍会失约，先保生活与合同付款可避免被迫低价出售；提前还贷省息与减少流动缓冲必须在同一台账比较。',
     ['PF026','MA003'],
     '若用户所有压力路径现金持续满足储备且无近期支出，必要削债/出售结论可被否定；无一方案可行则明确补资缺口而非判安全。',
     '现在核账，30—90天执行流动性安排，逐月120期与政策/收入变化时复算。')

for n in graph['nodes']:
    if n['id'] == 'J-2027':
        n['statement'] = '2027是专门置换安排转换、平台退出名录、大行资本加码和部分首套贴息新增受理的复核窗口；已查期限与滚续支持地区分化，尚不足以判断全国同年集中爆发。'
        n['evidence'] += ['BK003','BK007']
for e in graph['edges']:
    if e['id'] == 'HBK-LOSS-CAPITAL':
        e['mechanism'] = e['mechanism'].replace('本金缺口', 'CET1相对缓冲线的缺口')
    e.setdefault('research_status', 'conditional_mechanism_not_estimated_causal_effect')

(W / 'research/graph_initial.json').write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n')
print(len(graph['nodes']), 'nodes;', len(graph['edges']), 'conditional ALL edges')
