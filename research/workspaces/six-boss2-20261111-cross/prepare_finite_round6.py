"""Version-3 continuation of the same finite-computation identity."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

B=Path(__file__).resolve().parent
R=B.parents[2]
body=R/'archives/customer-attraction/subarchives/six-providers/state/计算/同源跨枝增强必要图的精确最优值与半界缺口--计算.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(body)=='09279a4d27440954584adaa3b323723a0e07f4419c58b4c0b85646665e58f4bb'
reports={}
for n in ('main_verify_dynamic_5786.json','main_verify_dynamic_5799.json',
          'main_verify_complete_zz_5799_v1.json','main_verify_complete624_opt_v2.json',
          'main_verify_624_projection_v1.json','main_verify_full_history_probe_v1.json'):
    d=json.loads((B/n).read_text())
    assert d['status']=='PASS',n
    reports[n]=d
oldW=F(reports['main_verify_complete_zz_5799_v1.json']['W'])
newW=F(reports['main_verify_complete624_opt_v2.json']['W'])
assert 0<oldW<newW<F(1,2)
d=json.loads((B/'master_cuts/complete624_actual4_R00_opt_v2_dual.json').read_text())
parts={'old5799':0,'zz':0,'margin':0,'raw624':0}
for term in d['row_multipliers']:
    if F(term['weight'])<=0:continue
    i=term['row_index']
    parts['old5799' if i<5799 else 'zz' if i<11418 else 'margin' if i<12042 else 'raw624']+=1
assert parts=={'old5799':152,'zz':42,'margin':306,'raw624':16}

s=body.read_text()
s=s.replace('scope: 固定16hist、4849列的明示必要LP；不是完整SPE或全输入半覆盖结论',
            'scope: 固定16hist及明示辅助提升的十个必要LP，另含一个指定十二标签真目录的全SPE排除；不是全输入半覆盖结论',1)
s=s.replace('# 固定16hist必要图的六轮精确最优值','# 固定16hist必要图的十个精确最优值与一个真目录排除',1)
s=s.replace('本对象版本2补入5752、5775和5783三轮精确证书及正尾行的有限消融；前版到5744的全部结论保留。',
            '本对象版本3在原六轮及正尾消融结论上续接5786、5799、完整39类ZZ和完整单结构624提升，并记录由同一边缘构造的指定十二标签真博弈之完整SPE排除。原证据字节不改，全部历史成立结论保留。',1)
row='| 5783 | 1 | 0.4926332627883867 | 8条616特征的跨旧查询PAIR |'
assert row in s
s=s.replace(row,row+'\n'+
'''| 5786 | 1 | 0.49265432731768616 | 3条已知616特征再配权 |
| 5799 | 1 | 0.49265432731768616 | 1条跨分枝容量行和12条ZZ端点上界 |
| 11418 | 1 | 0.49265432731768616 | 完整39类ZZ自由min，7639列 |
| 12666 | 1 | 0.49265618211149476 | actual第四源/R/第一非对角结构的完整624共同提升，12631列 |

前八系统的列域均为原4849列；后两系统保留其前缀并新增必要辅助量。表中每一数均有匹配准确原始/对偶；各个完整局部投影的闭包范围并不等于全目录、全有序历史。
''',1)
s=s.replace('本稿止于5783；更后续分离必须重新绑定此点SHA',
            '本节冻结的第六轮结论止于5783；后续分离必须重新绑定所使用点SHA',1)

addition=r'''
## 续接：5786与5799，排除一份旧点不等于提高最优值

Main独立核准三条616再配权行后，5786×4849的准确最优值为

\[
v=\frac{121493068957403865211086566942389521730338522914685389129175912565358962386745}
{246609158228421583872999564263448718798282013890815209401160684000599193827791}.
\]

全部5786行、4849对偶列非负，原始300正列、160正对偶。三新行中两条正对偶承重，故5783只加这两条的5785子系统也有同值最优；不称第三行全域冗余。

再并入跨分支CAP-H0及12条ZZ Fréchet必要行，得到5799×4849。旧5786保存点确被这些行排除，但新295正列原始点达到同一v，163正对偶准确匹配，13新行权全0。新点的16hist与K和旧点完全相同，仅174个其它语义坐标改变；这说明当前最优面仍有不同隐藏完成。

CAP-H0使用同一目录最大主题根分支的首个真实后继作为actual第二源的强制动作，重新按该源真实后继投影。它不是把旧后继冻结不动。ZZ行在旧真实Z节点查另一合法Z，使用真实IC的正交叠上界。Main已分别从真实4后继位、66个字面节点和完整描述符重建这13行；不得仅凭邻接边的accepted状态使用。

完整原始推导、绑定输入、负值和正对偶支撑分别在工作区 master_cuts/formal_5786_gap.md、formal_5799_gap.md，独审为 main_verify_cross_pairs_5783_three.json、main_verify_neighbor_5786.json 及两份全原/对偶报告。每条旧点负值只属于其绑定SHA。

## 完整39类ZZ自由min的精确闭合

固定hist的actual前四负载P，旧66个真实边节点的四态边缘写为
\(q_e=|R_e|,\ v_e=|Z_e|,\ t_e=|R_e\cap Z_e|\)。
真实Z末节点互查给

\[
L_{ef}=\frac{v_e-v_f}{P+1}
+\frac{J(R_e,Z_f)-t_e}{(P+1)(P+2)}\ge0.
\]

把正交叠放宽为 \(J(R_e,Z_f)\le\min(q_e,v_f)\)，再按固定字面四索引相等模式、稳定子等度关联聚合，共42类；删3个真正字面自查零类，余39类。不同字面节点即使落在同一词组，也不能被当成自查；不同R来源族即使索引相同，也不是同一节点。

每个使用到的hist/有序组对引入非负z，并要求
\(z\le q_g,\ z\le v_k\)。
共有2790个z、5580个上界和39预算。由于所有预算对z的系数非负，存在一份z满足这些预算，当且仅当把所有z同时置为各自的min后预算都成立。这证明该明确自由上界机制的完整有限表示；z不是实际交集，不证明这些min可由同一客户联合实现。

在全部5799旧行基础上，得到11418×7639矩阵。准确原始806正列（312原坐标、494辅助）达到v，旧163正对偶零扩后仍完全有效，故最优值准确不变。新点的39个canonical min预算全非负、最小0。对这39类继续改各hist的端点选择或非负合权不能分离该点；更强共同运输和新真实查询没有被此结论排除。

Main独立重建68640个字面边对项、10724条等度关联、全部5580上界和39预算；随后核全部11418原始行、7639对偶列及原4849投影，均PASS。准确半界缺口仍为

\[
1-2v=
\frac{3623020313613853450826430378669675337604968061444431142808858869881269054301}
{246609158228421583872999564263448718798282013890815209401160684000599193827791}>0.
\]

## 完整单结构624提升：小但严格的有限最优值改善

完整624的数学定义、所有非负权含零源权的有限消元等价，以及一般actual关联域上的严格层级，见引理 M-b1b4276f0ec747ed8c347bda65c9e0af。这里保原16hist；第17个padding型只用于那份局部严格性证明，没有加入本矩阵。

唯一结构是actual第四源、强制旧R、第一类非对角轨道。78个词对组×4个旧RZ态×16个共同宏隐藏态，新增4992变量；312质量等式以正反两行写成624行，再加全部624原始预算。保完整ZZ基底后为12666×12631，2704303非零系数。所有零质量hist/RZ型和四条恒零middle预算也保留。

Main逐系数独审先核3115008个特征值、质量映射及预算，随后另以标准库Fraction核完整准确原始/对偶。精确最优值为

\[
v_{624}=
\frac{13693318164200062394544139323881241367110722785072814019991361521168964799531933891388293129846749081130815}
{27794877363583108099358388689114427166754304884304339872804344677151233213541847015562845931339866326138413}.
\]

它比v严格增加约0.0000018547938085719664，仍低于half：

\[
1-2v_{624}=
\frac{408241035182983310270110041351944432532859314158711832821621634813303614477979232786259671646368163876783}
{27794877363583108099358388689114427166754304884304339872804344677151233213541847015562845931339866326138413}>0.
\]

准确原始点929个正列：319原语义列、534个ZZ辅助、76个宏隐藏质量。对偶516正项：152条旧5799行、42条ZZ上界、306条宏质量联系和16条raw624预算。原始最小余量与对偶最小剩余都为0，互补取等。16条raw预算中含原Z真实末节点查询宏V，方向仍用原背景；正权本身不代替严格包含或必需性证明。

该新点本身提供本结构所有624原始行的一份共同隐藏提升，所以本结构任意非负投影权（包括零源权）都不能分离该点。这不闭合其它源、其它R/Z结构、已见真实分支的新查询或跨多个旧组的共同会员。39个ZZ canonical min预算在新点上全部严格正。

### 精确恢复曾拒绝一份伪最优候选

第一份原始有理点满足全矩阵，但其候选449支撑对偶有4个严格负列余项，含正质量hist列250；强制正质量互补方程在所选支撑上不相容。未截断小负值，也未称该点最优。原点、候选基与失败诊断均保留在 solve_v1 名下。

更严格的独立数值候选另存 opt_v2，随后恢复上述同值有理原/对偶。第一份点比准确最优高约 \(4.28372902183459\times10^{-13}\)，说明浮点接近不能替代准确证书。本节只以Main全行全列PASS为最优性依据。

### 不可变证据身份

| 证据 | SHA-256 |
|---|---|
| 完整ZZ矩阵 | 8b076497ef826b60c797edcb8dc719f2f7ad678a01a34ecf66d2e757af525a20 |
| 完整ZZ准确点 | e5cd48369fc08f652490b09ecddc80dbacc09dd45d06e5fe97dc64de3f247075 |
| 完整ZZ对偶 | efb9fefe2bcacef00cee500a44d27e85f8606b4fe1d793187bc9bffeb8a809ca |
| 624矩阵 | 556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a |
| 624准确最优点 | 02bcb92f33f7e7e4fac00a4c64fd39b0a4f0c68a736559c300bbfba255168817 |
| 624准确对偶 | f97619798dd8abd6800210264abb6a48c13f9d61ef57de54a412b8a205a4798e |
| 624原4849列投影 | 75cf981c8e9a6554b796735b3e96c7e1145f420addec0ba045b25a293139803c |

624矩阵和映射位于RUN的 joint_requery/complete624_actual4_R00_v1_*；最优点、对偶和投影位于 master_cuts/complete624_actual4_R00_opt_v2_*。独立报告为 main_verify_complete624_v1.json、main_verify_complete624_opt_v2.json 和 main_verify_624_projection_v1.json。有限LP结论止于这些准确SHA；后续任何分离均需重新绑定新投影。

'''
s+='\n'+addition

# The complete exact game proof is a finite boundary consequence, not a new
# universal mechanism. Keep all mathematical details in the formal body.
probe=B/'master_cuts/formal_twelve_label_probe_v1.md'
assert sha(probe)=='d691a1a81992337dfca30df5d69213e94e3f42e4812d3c578ef80e6d2744b2a4'
dptext=probe.read_text()
dptext=dptext.replace('# 固定十二标签目录的完整 SPE 菜单与第五人严格拒绝',
'''# 指定十二标签真目录：完整SPE排除所保留的付款缺口

以下计算来自同一RUN，所有未加目录前缀的输入、菜单和见证文件位于 master_cuts/；Main审计在RUN根目录。采用既有全SPE终局集合递推定理 M-94942bfb644042ea8039e44db39d1504 的集合部分，使用任意精度整数新实现，不套用旧七标签/小人数实现的int64域。
''',1)
s+='\n'+dptext
body.write_text(s)
out={'body_path':str(body.relative_to(R)),'body_sha256':sha(body),
     'W_old':str(oldW),'W_624':str(newW),'strict_increase':str(newW-oldW),
     'dual_partition':parts,'version':3}
(B/'formal-finite-round6.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
