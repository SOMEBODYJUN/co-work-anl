"""Main's reviewed ALL edges, scoped to the proof contribution actually used."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;R=B.parents[2]
E=R/'map/edges/customer-attraction-boss2-six-cross-20261111';E.mkdir(parents=True,exist_ok=True)
reg=json.loads((R/'research/registry.json').read_text());objects={o['object_id']:o for o in reg['objects']}
pair='M-e394b173b9b1419588c6c380da4bd326';discount='M-b233ef00a9c34e189817cdfb7a495107';finite='M-ddceaa3d53064498b3e833a32e1f3b6f'
cone='customer-attraction/thirty-four-weight-same-source-two-branch-true-row-cone-and-exact-count-elimination'
strong='M-e960d7f4ebca40a38760eb3ae044cc19'
portfolio='customer-attraction/shared-true-terminal-reply-query-portfolio-and-reweighted-requery'
oldcuts='customer-attraction/same-source-requery-and-capacity-price-three-cut-packs'
oldpoint='M-96807ccbb51d4a04a699093e9211323e'
def ev(ids):
 d={}
 for i in ids:
  q=objects[i]['body'];d[q['path']]=q
 return list(d.values())
base={'kind':'implies','status':'accepted','premises_mode':'all','relation_mode':'unconditional','reviewed_by':'Boss2 Main'}
edges=[dict(base,edge_id='boss2-six-cross-34-and-pair-shared-projection',source_ids=[cone,strong],target_ids=[pair],
 conditions='任意有限单位客户、有限非空共同标签目录和同一份完整有序历史纯SPE。固定同一有序源余k≥3，第二枝强制题恰为第一枝真末题C；所有查询合法，所有权非负，两个源权和1。人数压缩仅在查询不读个别middle身份时使用。',
 roles={cone:'提供两枝source/price/cap/last/safe共34预算以及保共享C的人数域。',strong:'在两个真实末对各自的背景上提供任意合法查询对的零外部预算强PAIR。',pair:'将这些真实行先相加、再联合消去同一组b,c,j,v,s,s′。'},
 explanation='第一枝β1=p+t+s，第二枝β2=p+c+s′，共享第一枝末位与第二枝源会员c。每个PAIR负成本的相反数是三条真实IC与g(D,D)−g(D,R)之和，故对客户总和非负。取34锥非负权和任意PAIR非负权，源权和1，预算恰r+A u_m+D K。联合min只能降低成本右端；中间位只经s,s′时逐客户恰16(k−2)^2候选。λ=0恢复旧锥。不能拆成单独34或单独PAIR已经足够的两条支持边。',
 contribution={'result':'目标正文式(1)—(7)的一般合法共享双分支PAIR投影、旧锥包含关系与准确预算。','remaining':'目标的actual13原子严格性和五个固定5716切面依其明确有理证据及Main独立复核另行成立；本边不以一般行恒等式替代那些数值检查。'},
 scope='一般局部投影贡献；不支持六人half或全图SPE实现。',evidence=ev([cone,strong,pair]),
 review_note='Main全文实读两个原承重正文及新正文，逐项展开三IC的强PAIR恒等式，核同一C、两源总权1、中间(k−3)价格乘数与min方向；严格性和五行另有独立Fraction核验。'),
 dict(base,edge_id='boss2-six-cross-portfolio-to-discounted-closure',source_ids=[portfolio],target_ids=[discount],
 conditions='有限共同标签目录、固定同一有序源及同一完整策略；每个当前强制T的末回复C(T)仍属同目录。种子及常量查询先固定，所有权非负，0≤θ<1。允许查询当前T自身，但不得改变已固定seed查询。',
 roles={portfolio:'提供每个合法T都共用同一源收益、actual末价及K的组合查询真实IC预算。',discount:'用有限目录辅助最大值闭包该预算，再精确求二状态Bellman势。'},
 explanation='原组合行将同一真末回复的查询先加权相加；源权a0按源IC权直接重写，包括a0=0。由B≥ΣH以及V(t)−θV(c)≤H，对每合法T有B≥V(T)−θV(C(T))。在有限目录取加性V最大的T*，C(T*)合法，遂B≥(1−θ)V(T*)≥(1−θ)V(T0)。逐客户收缩Bellman方程的四确定策略只给三个不同起点候选。k2源权等于总查询权时四边平衡，二循环夹在另两候选中，连续θ由有限有理折点求最小。',
 contribution={'result':'一般折扣闭包、三候选精确消元及平衡权连续参数有限化。','remaining':'六条5716分离、固定权18步比较及5727连续θ全区间非分离是目标另附的有理输入/计算结论；不由组合引理的状态标签直接推出。'},
 scope='固定同一源的合法预算闭包；无跨互斥源免费合账，无最优种子必在周期上的假设。',evidence=ev([portfolio,discount]),
 review_note='Main核原portfolio全部真实IC与查询平均规则，独立完成有限最大值证明和Bellman四策略推导，另以独立实现重建6条全4849坐标并证明连续平衡特例。'),
 dict(base,edge_id='boss2-six-cross-three-families-pay-52-added-rows',relation_mode='conditional',source_ids=[oldcuts,pair,discount],target_ids=[finite],
 conditions='继承原5692行4849列及固定16hist域；母图含OPT单换行，比较六元组取最优。三冻结旧包及新包逐SHA绑定，使用同一actual收益/K预算和有名索引归一平均。',
 roles={oldcuts:'提供旧三包27记录合并后24个不同合法向量。',pair:'提供五条actual4及十六条actual2/3/4共享双末对PAIR合法向量。',discount:'提供六条折扣/portfolio行及一条θ0普通portfolio更新。',finite:'将24+11+17共52条与继承5692母图同列合并，分别形成5716、5727、5744系统。'},
 explanation='旧24行只用共同前1905列，新11和17行也在其余2944列取0；全列身份不变。各包按真实源、共同C、末回复及查询预算的正确方向构造，再对30/6有名索引轨道归一平均，不能把orbit数量乘进外部收入。Main逐列独立重建新两轮28行，准确系数和绑定原点负值全相同。三机制共同支持所追加52行的合法性与代入条件，而各有限最优数值另由原始/对偶证书完全证明。',
 contribution={'result':'三轮新增52条必要行的数学合法性、共同预算和正确模型代入。','remaining':'继承5692矩阵与各轮有理原始/对偶最优证书见目标的独立输入和Fraction复核；本边不把“切面有效”当作“最优值已证”，也不支持全类型half。'},
 scope='固定同列有限必要图的新增行来源；各轮确切最优值由目标另载证书承担。',evidence=ev([oldcuts,pair,discount,finite]),
 review_note='Main实读旧三冻结包的正文/原参数，核27记录只有24向量；独立重建5+6及16+1新增行。已独立核5716和5744全原始/对偶，并核5727原始/对偶精确证书。'),
 {'edge_id':'boss2-six-cross-old5692-gap-motivates-dynamic-closure','kind':'motivates','status':'accepted','source_ids':[oldpoint],'target_ids':[finite],'premises_mode':'all','relation_mode':'context',
 'conditions':'仅固定SHA46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e的旧5692必要点和相应母矩阵。',
 'roles':{oldpoint:'提供被后续合法动态切面排除的原始具体点和不变列布局。',finite:'在加行后重新优化并交付新的有理可行完成及匹配对偶。'},
 'explanation':'旧点仍对其5692行系统精确可行；三包24不同新行中12条在它上面严格负。于是必须重优化，不能继续把旧点当完整SPE，也不能由排一个点推出所有同W或全部必要完成都失败。新三轮有限最优值上升但仍小于half，确定的是模型松弛缺少约束。',
 'scope':'研究动机和准确输入接续，不是旧点蕴含新最优值，也不撤销旧对象的原有限可行性。','evidence':ev([oldpoint,finite]),'reviewed_by':'Boss2 Main','review_note':'已核旧输入完整SHA/4849列、24新向量回代及三轮不同新点；该关系只作语境。'}]
for e in edges:(E/(e['edge_id']+'.json')).write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
(B/'formal-edge-files.json').write_text(json.dumps([str((E/(e['edge_id']+'.json')).relative_to(R)) for e in edges],ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(edges),'reviewed edges.')
