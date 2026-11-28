"""Create reviewable proposals grounded in new historical evidence and actual audits."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parent; W=R.parent
s=json.loads((W/'research_state.json').read_text()); out=R/'proposals'; out.mkdir(exist_ok=True)
nodes={
'J-PROPERTY':('strengthen','中国新房开发与项目融资更可能在2027年继续收缩或低位运行，二手住房通过分城降价与换手出清；交付与核心城市可先改善。开发规模稳定在可持续低位也可结束持续恶化，不要求重回2021高点。',['HX008','HX009','HX010','HX016'],'2016库存、棚改与2023交付反例表明销售、库存、施工和交付可以不同步；保留本期负向主判断，补足出清结束条件。'),
'J-FISCAL':('strengthen','高土地依赖且转移、营运现金和可执行融资不足的市县先调整项目与回款；全国一般预算支出存在实际缓冲。置换可降票息及推迟本金，却不自动形成同额净新增需求，中央融资能力和当地实际到账分别判断。',['HX006','HX007','HX019'],'2015实际置换节息支持工具有效，但Setser债务率算例错误，不能以低利率自动推断稳定债务或家庭现金已改善。'),
'J-DEMAND':('strengthen','居民和内需小微的收入、回款及资产负债表约束共同抑制私人支出；部分主体融资需求弱、部分脆弱借款人受供给限制。全国银行贷款存款净流量不能识别同一借款人的主动偿债，也不等于全体私人部门资金流量表净借贷。',['HX014','HX002'],'Sufi完整原文区分住房套现、消费和建筑错配；Koo净借贷口径不能被贷款总量替代，日本十年工资反例取消房价到普遍工资的机械映射。'),
'J-BANKS':('strengthen','中国银行业首位路径仍是盈利承压、局部损失消化和资本补充；众邦已被接管，截至2026年11月27日公开证据不足以判全国系统危机已发生。升级须见跨地区重大银行困境与大规模应急干预或异常重大损失，亦核跨行外流、融资冻结和支付/授信失灵；不要求财报先完整确认。',['HX001','HX003','HX004','HX011','HX012'],'历史确认损失滞后及短期融资骤停均真实存在；日本五年截尾不能当恢复，不能把无排队挤兑当无危机。'),
'M-MODEL-USE':('replace','旧JST实验保留，纠错35未知标签和3全特征缺失后新作业仍拒绝校准HGB主预警，logit只作历史比较。raw与校准结果分别披露，负校准斜率经独立重估确认；已见测试不得称新验证。中国桥接和DFM未稳定胜基线，拒绝中国危机概率与精确GDP预测，以可复算会计和条件敏感性完成裁决。',['MT001'],'实际审计定位标签与校准问题，新输入1703行和独立重估一致，模型表现不佳不取消经济裁决责任。'),
'J-JOBS':('strengthen','全国就业与实际居民收入未显示同步塌陷；地产、地方项目及小微相关家庭未来12—24个月的可变薪酬、招聘和回款风险高于总量读数。风险只在相关雇主缺口传至实际工资与经营收入时计入，不把房价或土地毛款下降直接分摊给每户。',['HX002','HX006','HX014'],'日本房价代理下降时名义工资仍可上升，2015置换可实际减息；本轮传导必须追雇主实付而非宏观比例移植。'),
'J-MACRO':('strengthen','未来12—24个月首位是渐进滚续与局部承损、地产财政拖累和制造出口增长并存，收入与资产修复不均；外需和弱地方金融共振的严重信用收缩列次位。净财政支出真正到账并带动私人收入、回款和投资，或没有新增财政转移而私人现金、工资与投资自主持续改善，均可将有效修复升为主路径。',['HX006','HX007','HX009','HX014'],'2015—16说明有效需求和融资工具可改变方向，但非识别因果乘数；接受缓冲反证仍按当前资金和投资事实排序。'),
'J-DECADE':('strengthen','从2021年开发链高位起，到约2030年前后的多年地产与债务修复是应准备的主时间尺度，终点取决于收入、损失确认与结构替代。日本、美国及统一历史筛选支持长期实际住房拖累可能，不支持从2026固定再加十年全面停滞或2027第六年必爆。',['HX001','HX002','HX003','HX012','HX013','HX017','HX018'],'明确日本土地代理/美国住宅/中国开发量不同；17段事后筛选仅1段第六年危机且共振非独立；拒绝Pettis从无危机及现价美元份额降逾半旁证。'),
'J-EQUITY':('strengthen','拒绝从地产和收入调整直接推出A股未来十年必熊或每年下跌。日本与美国峰后十年实际含息回报不同，MSCI年历美元毛回报又是另一窗口；应分别核上市利润、估值、股息、币种及费用。近期必要支出不得依赖权益反弹，长期实际亏损仍须承受能力测试。',['HX002','HX013','EQ001','EQ002','EQ003'],'统一历史筛选的住房与股票不同步及端点币种复算，强化资产不能机械等号；历史正回报不保证未来。'),
'J-2027':('strengthen','2027是专门置换安排转换、平台名录退出、大行资本加码和部分首套贴息新增受理的复核窗口；合同期限与已执行滚续支持地区分化，不能据全国单一到期墙或日本第六年来定位系统危机。关键是同一债务人的可用现金、分币种剩余期限、承诺融资及真正到账是否覆盖支付。',['HX001','HX002','HX004','HX006','HX015'],'历史融资危机须期限币种匹配，SAFE两个边际比例不可相乘；本期省级到期反例及已执行置换降低机械年份解释。'),
'A-HOUSEHOLD':('strengthen','现在核对到账收入、必要支出、合同本息和资产变现时点，逐月120期先筛现金可执行方案，再比省息及净值。提前还款许可、费用和改供/缩期方式必须明确确认，未知不能视为允许或零费；可选预算不足和未付合同债务分列，出售启动早于资金耗尽。',['HX002','HX014'],'独立家庭审计发现未知合同默认允许/零费问题，必须改变动作准入；历史工资资产不同步强化家庭自己的现金日历。')}
edits={
'H-PF-EXIT':{'conditions':['若退出削弱原有保证或市场支持预期，且无新资本、补贴或可执行融资替代，才可能传至借贷条件。'],'mechanism':'2027年6月底名录安排是合同与支持预期的核验窗口；只有退出实际削弱保证或融资支持，才可能影响弱主体下一次融资价格和期限。未取得同主体同贷款退出前后报价，不能把名录变化本身当已识别的融资冲击。','counterevidence':['PF026','PF027','PF032','PF033','HX004'],'falsifier':'退出前后同一主体已获长期可执行融资、支持安排和经营现金足额，或报价期限并未恶化；均否定该主体由退出触发的融资收紧解释。'},
'H-FISCAL-INCOME':{'conditions':['同一雇主或经营客户实际依赖地方项目，存在应收延付且缺其他现金抵补；不将全国土地毛款减额均摊。','置换节息、清欠到账、工资发放和新增消费各记一次，债务换券本身不计为家庭收入。'],'mechanism':'实际财政迟付或项目缩减占用供应商周转，先影响可变工资和招聘，再传至家庭支出；2015置换可真实减息，但只有支付进入企业并转成工资或采购才构成下一步需求。','counterevidence':['MA003','PF023','PF026','MA001','HX006','HX007'],'falsifier':'同组供应商应收账龄缩短、实际清欠、工资招聘恢复且非靠高息短债；或成本节约和转移已完全补缺，切断本链。'},
'H-MACRO-SPLIT':{'mechanism':'旧开发链通过投资、地方实际支付和私人修复拖累内需；制造服务与出口增长提供缓冲，滚续保支付连续但不能制造旧项目收益。2015—16的置换和购买力支持说明可改变节奏，财政主导修复须见净资源实际到人到项目；外需、生产率或可持续私人现金、工资与投资自主改善也能独立形成有效恢复。','counterevidence':['PF026','PF029','MA003','BK004','HX006','HX009','HX014']},
'H-2027-CAPITAL':{'mechanism':'2027年工行附加资本要求增加50基点，按同日RWA静态增加资本需求1523.91亿元。真实可计入留存和实缴资本可补缓冲，RWA变化也会改变约束；监管要求增量不等于当天现金流出，规则日期本身不推出资不抵债。','counterevidence':['BK003','BK009','BK014'],'conditions':['以2026年9月披露RWA作静态参照，新增资本按实际入账认定；不将资本要求增量当现金提款。']},
'H-DECADE-REPAIR':{'conditions':['存量房地产过剩、地方收入结构和私人收入分配需要多年调整，开发规模可在较低可持续水平稳定。','若政策以展期与渐进承损为主且收入修复慢，长期拖累延续；历史样本事后选取且共振，不可作中国概率。'],'mechanism':'滚续可避免集中清算却不增加旧项目现金收益，损失经利润财政和收入分担。日本1991—2001与美国2007—2017实际住房都未回所选峰但工资股权路径不同，持续期由收入、损失确认和资源转移决定；中国2021起点是开发链规模而非同类房价。','counterevidence':['PF026','PF037','MA001','MA003','MA006','HX009','HX002'],'lag':'2021起至约2030前后的跨周期窗口；不保证2030结束，更不从2026固定追加整整十年。'},
'H-EQUITY-SEPARATION':{'mechanism':'上市利润、估值和股息共同决定回报，国内地产不是全部上市利润。日本与美国所选住房峰后十年本币实际含息股权分别约-32.5%与+72.0%，显示机制可分离，不将任一端点移为中国参数。','conditions':['明确指数、币种、股息税费、名义实际和持有窗口；年历连乘与滚动十年另列。','历史峰后样本事后筛选；负总回报与每年下跌是不同命题。'],'counterevidence':['MA009','PF009','HX002','HX013','EQ001','EQ002','EQ003']},
'H-HOUSEHOLD-ACTION':{'conditions':['真实合同、可动用现金和处置限制明确；提前还款、改供/缩期权限和费用只有明确确认才进入可行策略，未知不能默认允许或零。','策略只读当期可见信息；出售有等待、抵押解除与到账顺序，未及时到账记录缺口；初始金额为空。'],'mechanism':'现金不足可能先表现为未完成可选支出，再成为合同本息未付，两者单列；正净值不能支付当月账单。先保生活与合同付款，再以同一台账比较提前还款省息、流动缓冲、出售和长期净值。','falsifier':'所有压力路径都满足储备及合同支付则无需强制削债或出售；无可行策略须报告补资缺口。规则数量和分币级独特轨迹数量分别报告，不以重复动作凑可行策略。','counterevidence':['PF026','MA003','HX002','HX014']}}
order=['J-PROPERTY','J-FISCAL','J-DEMAND','J-BANKS','M-MODEL-USE','H-FISCAL-INCOME','J-JOBS','H-MACRO-SPLIT','J-MACRO','H-DECADE-REPAIR','J-DECADE','H-EQUITY-SEPARATION','J-EQUITY','H-2027-CAPITAL','J-2027','H-HOUSEHOLD-ACTION','A-HOUSEHOLD']
order.insert(order.index('J-2027'),'H-PF-EXIT')
pack=[]
for i,target in enumerate(order,1):
    bucket='nodes' if target in nodes else 'edges'; cur=s[bucket][target]
    pid = 'AUDIT-18' if target=='H-PF-EXIT' else f'AUDIT-{i if i < 15 else i-1:02d}'
    p={'id':pid,'author':'boss 1','target':target,'base_revision':cur['revision'],'old_statement':cur.get('statement',cur.get('mechanism'))}
    if bucket=='nodes':
        action,statement,ev,reason=nodes[target]; p.update(action=action,new_statement=statement,new_evidence=ev,reason=reason)
    else:
        rep={k:copy.deepcopy(v) for k,v in cur.items() if k not in ('revision','status','last_proposal')}; rep.update(edits[target])
        ev=[x for x in rep.get('counterevidence',[]) if x.startswith('HX')]
        p.update(action='strengthen',replacement=rep,new_evidence=ev,reason='新历史来源及独立实际复核检验本机制的边界、反证与到账顺序；保留条件机制，不声称估计因果效应。')
    p['new_method']='历史统一筛选、同币种/同主体现金和资本核对；数值及原文独立审计，保留失败记录并按具体机制改正。'
    p['review_artifacts']=['research/historical_model_correction.md','research/tasks/history_framework_review/history.md','research/tasks/history_framework_review/framework_review.md','research/tasks/research_independent_review/independent_models.json']
    (out/f'{p["id"]}.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n'); pack.append(p)
(R/'audit_proposal_pack.json').write_text(json.dumps({'author':'boss 1','base_evidence_revision':s['revision'],'apply_order':order,'proposals':pack},ensure_ascii=False,indent=2)+'\n')
print({'proposals':len(pack),'source_revision':s['revision'],'statuses':{t:s['nodes' if t in nodes else 'edges'][t]['status'] for t in order}})
