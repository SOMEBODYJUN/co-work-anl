"""Re-review affected contributions and add narrowly scoped proof-step edges."""
from pathlib import Path
import hashlib
import json
B=Path(__file__).resolve().parent
R=B.parents[2]
E=R/'map/edges/customer-attraction-boss2-six-cross-20261111'
registry=json.loads((R/'research/registry.json').read_text())
objects={o['object_id']:o for o in registry['objects']}
hier='M-b1b4276f0ec747ed8c347bda65c9e0af'
finite='M-ddceaa3d53064498b3e833a32e1f3b6f'
prefix='M-63c882b0c8414805a43d4d8d4e43f4e3'
rz='M-736ccd964c384f16a6816eebcb468f2f'
portfolio='customer-attraction/shared-true-terminal-reply-query-portfolio-and-reweighted-requery'
frechet='customer-attraction/fixed-last-reply-bivariate-marginal-frechet-extension-obstruction'
dp='M-94942bfb644042ea8039e44db39d1504'
assert objects[hier]['version']==2 and objects[finite]['version']==3 and objects[rz]['version']==1
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ev(ids):
    return [objects[i]['body'] for i in ids]
changed=[]
old_ids=[
 'boss2-six-cross-shared-pair-to-query-hierarchy',
 'boss2-six-cross-three-families-pay-52-added-rows',
 'boss2-six-cross-hierarchy-and-shared-tail-pay-39-more-rows',
 'boss2-six-cross-old5692-gap-motivates-dynamic-closure']
for eid in old_ids:
    p=E/(eid+'.json')
    data=json.loads(p.read_text())
    for key in ('endpoint_pins','evidence_pins','review_digest'):
        data.pop(key,None)
    data['evidence']=[{**e,'sha256':sha(R/e['path'])} for e in data['evidence']]
    data['review_note'] += ' 版本3/层级版本2复审：原贡献范围保持，新增624、ZZ完整表示及十二标签真目录证据由独立新边/目标证书承担；本边不自动升级为整个新目标的证明。'
    if eid=='boss2-six-cross-shared-pair-to-query-hierarchy':
        data['roles'][hier]='提供目标中原76/332/616部分的共同隐藏投影与两份旧严格见证；新624部分另由原末节点IC及actual补齐证明承担。'
        data['contribution']['remaining'] += ' 版本2的第三道624严格性使用同一D17域中的另一个padding见证，不由本边的原PAIR恒等式单独推出。'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    changed.append(str(p.relative_to(R)))
base={'kind':'implies','status':'accepted','premises_mode':'all',
      'relation_mode':'unconditional','reviewed_by':'Boss2 Main'}
edges=[
 dict(base,edge_id='boss2-six-cross-shared-tail-to-rz-income-credit',
      source_ids=[prefix],target_ids=[rz],
      conditions='同一完整六人纯SPE及actual第四源；静态Bj一致换合法Cj，原R^C与Z^C必须来自同一真实边。初段共享c、尾部共享v；两套参数先固定，尾合同对全部合法F成立后用于真实v。',
      roles={prefix:'给两套整数初段/尾合同及完整999u4+139u6、10000u4+1358u6付款，K系数0。',rz:'将两合同放在同一R^C/Z^C边，增加原Z末位IC，再证明四态差界、保持v映射和覆盖税。'},
      explanation='取冻结第2/13参数乘999/10000，仅将第2静态Bj换Cj；初段隐藏b不换。两个合同在合法种子R^C和Z^C上分别成立，按49和10合账得到148951u4+20391u6。共同模型末位IC给17965倍(n/6−z)/(P+r+1)零预算。目标直接证明四态min及21669/D收入信用，随后按同一actual客户量减21669u6；不得将−1278u6解释为负IC权。',
      contribution={'result':'六人固定实例的两笔有效初段/尾预算、合法种子/查询代入以及共享末端的必要条件。','remaining':'一般四态两差界引理、49:10完整2560型有理差界、保持v隐藏映射、覆盖税与U/C付款障碍均由目标直接证明及Main独立表核承担；本边不支持半覆盖已闭。'},
      scope='已证共享尾合同在同一真实边上的准确应用；一般代数新结论保留在目标正文。',
      evidence=ev([prefix,rz]),
      review_note='Main已全文实读来源、目标769行建议稿与最终正文；独立从原alpha/beta重建3840/720个L、2560四态、2880保持v映射及两版224覆盖型，核预算和负基线。'),
 dict(base,edge_id='boss2-six-cross-portfolio-and-frechet-pay-cap-zz',
      source_ids=[portfolio,frechet],target_ids=[finite],
      conditions='原16hist/4849语义前缀不变，H0是同一最大主题根枝的真实合法首后继；R_e/Z_e按共同目录真实有序节点定义。字面边先按相等模式计数，再稳定子等度平均；所有辅助非负。',
      roles={portfolio:'支付actual第二源强制合法H0、查询A6的显式零末价容量行。',frechet:'提供真实Z_e查询Z_f的准确IC及固定own四态下的min交叠上界。',finite:'对12选定端点行、完整39非自查类及2790上界辅助做独立准确表示和有限优化。'},
      explanation='CAP用真实四后继、源权1、中间容量3/64、末容量1/16与末查询1/16，预算u2+13K/64。ZZ用L_ef=(v_e−v_f)/(P+1)+(J(R_e,Z_f)−t_e)/((P+1)(P+2))，以J≤min(q_e,v_f)得到必要预算。组对上界变量z同时受q/v约束，所有39预算对z正，故可一齐置min；该有限等价不构造真实交集。Main从字面节点/后继位重建所有系数。',
      contribution={'result':'5799中CAP与ZZ行的真实合法来源，及11418完整自由min机制的必要性。','remaining':'2790映射与39预算的完整表示、5799/11418准确同值和806正列完成，由目标独立精确证书承担；这些上界不宣称全共同运输或SPE充分性。'},
      scope='指定固定支持必要系统的新增机制；旧负值的点绑定与新最优面的变更分别记录。',
      evidence=ev([portfolio,frechet,finite]),
      review_note='Main实读原始portfolio/Fréchet正文及其条件，未用其旧点不可扩张结论替代新点计算。另独核13×4849系数、68640字面pair项、10724等度检查和全原/对偶。'),
 dict(base,edge_id='boss2-six-cross-complete624-projection-pays-lift',
      source_ids=[hier],target_ids=[finite],
      conditions='只取actual第四源、强制旧R、第一非对角轨道、原16hist与同一17菜单。每个旧RZ四态对应16宏隐藏态；所有零质量结构型及零源权面保留，轨道重数只乘一次。',
      roles={hier:'提供全部624原始预算的合法性、原R/Z背景、共享宏身份和全非负权有限提升等价。',finite:'按78组×4四态×16隐藏态表示，保11418母块后认证12666×12631有限原/对偶。'},
      explanation='312边缘等式以624正反行加入，另加624预算，新增4992非负列。存在共同宏提升等价于指定结构全部非负624投影行。老目标/归一新列补0，全部原行/列按前缀保持；Main独立核3115008特征值和完整有限原/对偶。',
      contribution={'result':'完整624有限提升的数学必要性、共同隐藏语义、正确预算和局部全权闭包解释。','remaining':'精确最优v624、原始929正列、516正对偶及对首轮伪最优候选的拒绝由目标另附有理证书承担。原17-hist严格性见证不加入本16-hist矩阵。'},
      scope='仅所列单结构624局部闭包，不覆盖其它源、跨旧组或全部共同目录。',
      evidence=ev([hier,finite]),
      review_note='Main已独立全12666原始行、12631对偶列及互补取等PASS，并核原4849投影和39ZZmin。新数值收益不用于替代层级的独立严格见证。'),
 dict(base,edge_id='boss2-six-cross-full-spe-menu-pays-fixed-catalog-exclusion',
      source_ids=[dp],target_ids=[finite],
      conditions='唯一冻结12标签48兴趣类型整数输入，六T分割总客户集；原六人完整有序历史模型及任意弱平局。新实现采用任意精度整数和60倍收益，不使用旧七标签实现的int64/有限哨兵。',
      roles={dp:'提供全部可实现终局集合及逐子博弈最低可信收益门槛的必要/充分逆推定理。',finite:'对指定输入重算全18564状态、完整根菜单并保存完整策略DAG，给A5最早严格拒绝。'},
      explanation='仅取源算法E(c)的键集合S(c)，门槛τ(c)=max_b min_(g∈S(c+e_b))P_b(g)。终局f可沿a实现恰须f在该孩子菜单且P_a(f)≥τ。各有序孩子独立接其可信子SPE，缓存的是集合，目标依赖DAG不强加全局计数政策。六T分割给OPT=N；该输入根菜单仅六T各一次，且h=(A1..A4,T1)的全部末位回复为T2..T6。',
      contribution={'result':'全菜单递推为何覆盖全部完整历史SPE，以及目标依赖全孩子DAG为何是可信策略证书。','remaining':'该唯一输入的整数数值、全菜单相等、所有行动IC和严格G−u5分数由目标冻结输出及Main独立重算承担。只排除此目录，未排除附加标签。'},
      scope='固定真目录全部SPE的精确有限结论；不从300税实验或计数策略扫描推断一般half。',
      evidence=ev([dp,finite]),
      review_note='Main全文核源定理的必要/充分性与大整数实现限制，另独立生成所有计数态、12376终局、33486菜单从属对、123950候选比较及74256DAG行动IC，未导入发现器。')
]
for edge in edges:
    p=E/(edge['edge_id']+'.json')
    assert not p.exists()
    p.write_text(json.dumps(edge,ensure_ascii=False,indent=2)+'\n')
    changed.append(str(p.relative_to(R)))
manifest={'changed_edge_files':changed,'new_edge_files':changed[len(old_ids):],
          'scope':'Four old proof contributions preserved and re-reviewed; four new narrowly scoped ALL edges.'}
(B/'edges-round6-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
