"""Reviewed proof-step ALL edges for the new strict hierarchy and closure bridges."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2]
E=R/'map/edges/customer-attraction-boss2-six-cross-20261111'
reg=json.loads((R/'research/registry.json').read_text())
objects={o['object_id']:o for o in reg['objects']}
pair='M-e394b173b9b1419588c6c380da4bd326';discount='M-b233ef00a9c34e189817cdfb7a495107'
hier='M-b1b4276f0ec747ed8c347bda65c9e0af';prefix='M-63c882b0c8414805a43d4d8d4e43f4e3'
price='M-043045ec129b4a5f82a3368b324accf9';finite='M-ddceaa3d53064498b3e833a32e1f3b6f'
def evidence(ids):return [objects[i]['body'] for i in ids]
base={'kind':'implies','status':'accepted','premises_mode':'all','relation_mode':'unconditional','reviewed_by':'Boss2 Main'}
edges=[
 dict(base,edge_id='boss2-six-cross-shared-pair-to-query-hierarchy',source_ids=[pair],target_ids=[hier],
      conditions='完整有序历史纯SPE、有限共同标签目录。同一源两枝共享C；17查询为固定合法主题或对合法纯主题的归一平均。新增same/off耦合对全部客户共同固定；严格见证限actual4/R/第一非对角轨道和同一细化可见域。',
      roles={pair:'提供34预算、两枝全部合法强PAIR及先合账再对共同隐藏回复取min的合同。',hier:'将查询由各自隐藏提升合为同一提升，再加两个旧查询的PAIR；用两份独立准确证据严格区分三种投影。'},
      explanation='无Q的60真行保一次，每个合法Q加16真行，得到332。旧查询对按固定纯索引分布平均强PAIR，加入每枝142行得616。删除284行给P616⊆P332，将共同提升限制到任一查询给P332⊆交P76。额外剩余交矩只细化可见域，旧提升按n_v/n_y分裂保全部预算。跨查询PAIR与两个自身PAIR的差为E[(x-y)^2]/[2(β+1)(β+2)]；k3第一枝β=p+t可见，故差完全穿过联合min。',
      contribution={'result':'76/332/616三个投影族的合法定义、两道非严格包含、正确共同可见域及对称差逐客户恒等式。','remaining':'两道严格包含另由目标所附5744的17份旧提升/500权负行、5775的79原子332提升/12权负行及Main独立Fraction报告证明；本边不以非负增量自行断言不可由其它旧权推出。'},
      scope='一般行合同和投影关系的证明贡献；不表示所有输入严格，也不产生完整SPE。',
      evidence=evidence([pair,hier]),
      review_note='Main实读原PAIR正文与新层级全文，独立构造332全部特征、字面same/off查询耦合、8×4849系数、79原子质量与332预算，并核192×16隐藏恒等式。此前17份76提升与500整数权也已独立通过。'),
 dict(base,edge_id='boss2-six-cross-pair-and-discount-pay-shared-terminal',source_ids=[pair,discount],target_ids=[prefix],
      conditions='同一完整策略、同一合法有序源余k≥3；初段第二枝真末V属于共同目录。固定菜单在尾合同对全部合法F量化之前选定；alpha/beta独立非负，0≤delta<1。',
      roles={pair:'给初段T→B/C、回同源C→J/V的共享隐藏合同及其实际源/末价/K费用。',discount:'给同一固定尾权对所有合法F都成立的折扣加性合同。',prefix:'在初段真实V上使用尾合同，支付两合同全部预算后共同消去相同v。'},
      explanation='初段Balpha≥ΣEalpha在真实两枝会员上成立；尾合同Bbeta≥ΣPsi_beta(1_F)对每个合法F成立，故取F为初段真实V后可相加。真实局部赋值包含在16(k−2)^2域内，按同一个v取min只能降低成本。预算为(aT+aC+a_beta)r+(Aalpha+Abeta)u_m+(Dalpha+Dbeta)K；初段中间k−3，尾段k−2。逐客户min(E+Psi(v))≥min(E)+min(Psi)，但不能由此推出全部参数锥的严格包含。',
      contribution={'result':'目标一般共享末端组合定理、完整预算、beta0嵌入与固定参数联合投影不弱于分别投影。','remaining':'16条5752负行、12条非零尾权的固定同权严格增益由目标另附准确输入/系数及Main独立Bellman、逐索引和全列核验承担；有限目标严格改善见计算对象的删行见证。'},
      scope='两个承重合同共同支付同一个证明步骤；缺任一合同都不足以推出组合行。',
      evidence=evidence([pair,discount,prefix]),
      review_note='Main全文核两个来源与目标，四确定策略独立求Bellman并重建16×4849系数；核三项源权之和、middle人数和共享v，不将同参数或delta0比较扩张成全锥结论。'),
 dict(base,edge_id='boss2-six-cross-balanced-discount-to-positive-price',source_ids=[discount],target_ids=[price],
      conditions='同一有序源余k≥2，固定静态查询及显式当前自查询，源权a=M；非负价格/容量，0≤theta<1。所有静态Q在主题F的全称量词之前固定。',
      roles={discount:'提供同一Bellman势和对全部合法种子成立的折扣合同。',price:'利用平衡权两行之差给严格正客户价格及任意尾长上下界，转成全目录统一价格上限。'},
      explanation='平衡时H(1,c,s)−H(0,c,s)=(a−q)/(p+s+1)+(mu_*+q)/(p+s+2)，与c和各价格成本无关，且随s递减。对s取min夹住e1c−e0c，再对同一Bellman固定点的c取min夹住V1−V0。乘1−theta得w界；a>0时下界正，a0时w0。由已证全目录合同B≥ΣPsi(1_F)，写Psi=b+w1_F即得统一上限B−Σb。每次用于其它分枝都连同B、常量一并按权支付。',
      whole_result='一般k平衡末回复闭包的全目录非负价格、a>0时严格正价、精确上下界及合法跨枝使用预算；目标不含未经证实的数值切点宣称。',
      scope='一般局部正价定理；只在k2得到上下界相等，不声称k>2参数独立或全域half。',
      evidence=evidence([discount,price]),
      review_note='Main亲自推导同c/s差及两次min夹界，包括p=s=c0的零分子边界；coverage_bridge独立审查PASS。未借任何有限网格建立一般定理。'),
 dict(base,edge_id='boss2-six-cross-hierarchy-and-shared-tail-pay-39-more-rows',source_ids=[hier,prefix],target_ids=[finite],
      conditions='保持5744原矩阵16hist、4849列、W/O和共同K；比较六元组为OPT6。8条5744共同查询、7条5752共同查询、16条5752初段/尾和8条5775跨查询分别绑定准确源SHA，并由独立全列审计准入。',
      roles={hier:'给共同17查询/616交叉PAIR的合法零预算特征与精确共同投影，支付8+7+8条新增向量。',prefix:'给独立初段/尾合同共享真实V的合法投影，支付16条新增向量。',finite:'在不改旧列/目标/原行的条件下串行并39行，分别形成5752、5775、5783系统并另核原始/对偶。'},
      explanation='各行对固定真实源、静态合法查询和完整R/Z四态同一客户会员求值，依30/6有名边归一平均。所有收入预算随参数归一同步，未以轨道大小额外付款。Main逐列重建8+7+16+8行，并在每次扩展后核旧矩阵前缀完全相同。这两条已证机制给新39行的数学来源；具体精确最优值由目标原始/对偶证书证明，删12条正尾后的可行点给其有限目标贡献。',
      contribution={'result':'5744之后39条新增必要行的合法性、共同预算及模型代入。','remaining':'继承矩阵、三轮准确最优数值、5752对偶支撑修复和12条正尾有限消融由目标独立有理证书及Main逐行逐列回代承担；本边不把单点负值升级为全域覆盖定理。'},
      scope='本次固定支持有限系统的新行来源；一般题仍须全客户型共同付款或完整SPE实现。',
      evidence=evidence([hier,prefix,finite]),
      review_note='Main亲自核共同隐藏域/查询交矩/Bellman预算；5752、5775、5783全原始与对偶准确取等。另独立验证5763删行点及5775对偶，有限消融范围明确。')]
new_files=[]
for e in edges:
    path=E/(e['edge_id']+'.json')
    assert not path.exists(),'Do not overwrite an already reviewed new edge'
    path.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
    new_files.append(str(path.relative_to(R)))

# Only the two old incident edges change their target body/version pin.
# Their original 52-row logical contribution and motivation scope stay intact.
updated=[]
for name in ('boss2-six-cross-three-families-pay-52-added-rows','boss2-six-cross-old5692-gap-motivates-dynamic-closure'):
    path=E/(name+'.json');e=json.loads(path.read_text())
    assert e['target_ids']==[finite]
    e['evidence']=[objects[finite]['body'] if r['path']==objects[finite]['body']['path'] else r for r in e['evidence']]
    e['review_note']+=' 版本2复审：目标新增5752/5775/5783独立续节，原三轮52行贡献或原5692动机保持不变；本旧边不替代新39行来源边及新数值证书。'
    for key in ('endpoint_pins','evidence_pins','review_digest'):e.pop(key,None)
    path.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
    updated.append(str(path.relative_to(R)))
out={'new_edge_files':new_files,'updated_incident_edge_files':updated,'all_reviewed_files':new_files+updated}
(B/'formal-round4-edge-files.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
