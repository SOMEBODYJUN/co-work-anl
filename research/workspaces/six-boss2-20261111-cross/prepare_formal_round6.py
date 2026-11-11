"""Promote verified mathematics, preserving all frozen evidence bytes.

Run once after every explicitly listed Main report is PASS. The existing
hierarchy gets version-2 content; the new shared-RZ lemma gets its allocated ID.
The finite-computation body is prepared separately after the current certificate.
"""
from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parent
R = B.parents[2]
hier = R / 'archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md'
rz = R / 'archives/customer-attraction/state/引理/共享真实末回复边的零容量覆盖信用与收入转移--引理.md'
source = B / 'coverage_bridge/formal_shared_rz_income_bridge_v1.md'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


assert sha(hier) == '9cfcee53e139efeff799ec3bb4decb611d82d0cd10d0c53621e132fb10d3e28a'
assert not rz.exists()
assert sha(source) == '77be2e63597c3840d10cc7d471a0befdbd574cf8995451ca927ec1810ee0477f'
for name in ('main_verify_reverse_terminal_strictness_v1.json',
             'main_verify_complete624_v1.json',
             'main_verify_zero_capacity_v1.json',
             'main_verify_strong_a6_transfer_v1.json'):
    assert json.loads((B/name).read_text())['status'] == 'PASS', name

text = hier.read_text()
old_intro = '本文把原17个单Q与共同332行的严格性，接到新增两个旧查询PAIR的616行；'
assert old_intro in text
text = text.replace(old_intro, '本文把原17个单Q、共同332行、跨查询PAIR的616行和原末节点反查的624行接成同一严格投影层级；', 1)
text = text.replace('**核心命题。** 在同一充分细化的actual第四源、第一类非对角轨道、强制主题为R、固定17菜单的可见域上，有严格包含',
                    '**核心命题（版本2）。** 在同一充分细化的actual第四源、第一类非对角轨道、强制主题为R、固定17菜单的共同17-hist可见域上（或包含它的一般actual关联域上），有严格包含', 1)
text = text.replace(r'\boxed{\mathcal P_{616}\subsetneq\mathcal P_{332}',
                    r'\boxed{\mathcal P_{624}\subsetneq\mathcal P_{616}\subsetneq\mathcal P_{332}', 1)
old = '右边允许17份分别隐藏提升；中间要求17查询共用第一枝C和第二枝J/V；左边在同一隐藏提升上再同时要求两个旧查询的强PAIR。两份不同的actual关联有理点分别证明两个严格包含。它们是必要投影的严格性见证，不是完整SPE，也不否定六人半覆盖命题。'
new = '最右边允许17份分别隐藏提升；332要求17查询共用第一枝C和第二枝J/V；616在同一提升上补两个旧查询的强PAIR；624再补原R/Z末节点对同一宏B/C/J/V的八个零预算查询。三份不同的actual关联有理点分别证明三道严格包含。前两份用原16hist，第三份增加一个确定hist；共同17-hist域在第8节定义。它们都是必要投影见证，不是完整SPE，也不否定六人半覆盖命题。'
assert old in text
text = text.replace(old,new,1)
text = text.replace('本文两道严格性均已获Main独立PASS。', '版本1的两道严格性均已获Main独立PASS；版本2的第三道见第8节。',1)
text = text.replace('本文写入这次审计状态后冻结，后续符号聚合另稿。',
                    '原证据保持冻结；版本2只在本页续接已经独审的新证明，不改原件字节。',1)

appendix = r'''
## 8. 原真实末节点反查同一宏：624严格小于616

原R、原Z可以查询新宏B/C/J/V，但其背景必须保持原有序历史。第一类非对角边满足

\[
R_{ij}=\sigma_6(A_1,A_2,A_3,T_i,B_j),\qquad
Z_{ij}=\sigma_6(A_1,A_2,A_3,A_4,R_{ij}).
\]

写 \(\beta_R=p+t_i+b_j,\ \beta_Z=p+a_4+r\)。对新宏任一合法主题E，其会员为e，真实末位最优性给八条零预算行：

\[
\sum_x\left[\frac e{\beta_R+1}-\frac r{\beta_R+r}\right]\le0,\qquad
\sum_x\left[\frac e{\beta_Z+1}-\frac z{\beta_Z+z}\right]\le0. \tag{9}
\]

终局0/0份额记0。这里未把被强制的B_j当最佳回复，也没有借用新宏背景。所有成本先在同一个宏隐藏四位上合账。令624要求616的同一提升再满足(9)，即有 \(\mathcal P_{624}\subseteq\mathcal P_{616}\)。

### 8.1 第三份严格见证的共同17-hist域

原16hist之外，加一个确定型

\[
a(H_*)=(0,0,0,1,0,1),\quad
(T_i,B_i,C_i)(H_*)=(1,1,1)\quad(i=1,\ldots,6).
\]

共同域 \(\mathcal D_{17}\) 允许这17种hist的非负质量及合法R/Z四态，仍由同一actual六位计算 \(u_4,u_6\)。原5744和5775见证以新hist质量0嵌入，原两道严格性不变。新见证用新hist正质量，因此不能据它声称624相对616已在原16-hist限制域严格。

5799点本来已违反完整616，不能仅凭624的新正权证明严格性。先恢复一份完整616提升，在自由源付款 \(u_4+\delta\)、原 \(u_6,K\) 下可行，其中

\[
\delta=
\frac{2465201632061400404249536195487906900932734809402071846465468132650811843841}
{1025894098230233788911678187335946670200853177785791271108828445442492646323610560}>0.
\]

给H*取R=Z=1、宏四位全1、质量 \(6\delta\)。其单位actual收益 \(u_4=u_6=1/2\)，两个源成本各1/3，四末价各1/2，容量各1。其余last/safe/PAIR成本非正，八条(9)全0。新actual预算变为 \(u'_4=u_4+3\delta,\ u'_6=u_6+3\delta,\ K'=K+6\delta\)，准确支付旧提升与新增原子；没有把自由来源虚记为实际收益。

所得57个可见型、77个正隐藏原子满足全部616预算、全部质量等式以及17菜单actual末价和容量，精确最小余量0。

### 8.2 新624方向的严格负值

以下16个整数权共用同一宏：

| 特征 | 整数权 |
|---|---:|
| sourceT，sourceC | 6406414，3593586 |
| price B，C，J，V | 1018800，942217，817252，1084048 |
| cap V | 331490 |
| last2 B | 1335914 |
| last1 T_i，C_i，B_j | 797069，797069，786840 |
| last2 B_j | 4976 |
| PAIR₂(T_i,B)，PAIR₂(余T均值,B) | 19906，79624 |
| PAIR₁(T_i,B_j) | 1098148 |
| 原Z查询宏V | 54741 |

预算恰为 \(10^7u_4+3862317u_6+331490K\)，最后一项为(9)的Z→V、预算0。源归一后，该共同min行在H*上单位余量精确为1/6；因此补齐后的余量为5799原负值加 \(\delta\)，精确等于

\[
-\frac{148845568998121138356228513900153618711355035474766353741403675003844902443555714733}
{115156612526343742805335876528460013730045769206455070181965993000919799549825285360000000}<0.
\]

新点属于616而不属于624，完成第三道严格包含。此点不声称保全5799主图所有早期IC，更没有完整SPE实现。三个严格见证互不相同，各自支付一道严格性。

证书 actual_padding_616_vs_624_strictness_5799_v1.json 的SHA为
a06786cd8a5176754544d614034eeec78efc6a733f8ad0552f5ce760b48a14ce。
16权包 reverse_terminal_5799_one_v1.json 的SHA为
3b39262c153be351853f2625809da5679e634648d895c233b554868f1bd0077c。
Main独立报告 main_verify_reverse_terminal_strictness_v1.json 核两套4849系数、全部616预算、质量、actual链接和严格负分数，结果PASS。完整逐特征补齐证明见 formal_reverse_terminal_strictness_v1.md。

## 9. 全部非负权与一份共同有限提升等价

对任一指定76、332、616、624原始行族，固定可见非负质量m，隐藏提升域
\(\mathcal X(m)=\{X\ge0:\sum_hX_{v,h}=m_v\}\)
是非空紧凸集，包括零质量型。令成本向量为C(X)、预算为B，则

\[
\exists X\in\mathcal X(m),\ C(X)\le B
\quad\Longleftrightarrow\quad
\forall\lambda\ge0:\quad
\lambda\cdot B\ge\sum_vm_v\min_h\sum_\alpha\lambda_\alpha F_\alpha(v,h).
\tag{10}
\]

正向是预算合账与逐型min。反向，紧集 \(C(\mathcal X(m))\) 加非负正交锥是闭凸上集。若B不在其中，严格分离法向必须非负，否则上集沿该正坐标无界使线性泛函无下界。逐质量单纯形求分离下界恰得(10)右端，从而矛盾。源总权为0的权也必须保留，不能只检查源归一为1的参数。

细hist/词对/RZ域与其充分统计量粗域可条件分配。若粗型v含细组g、其轨道权为 \(\omega_g\)，细质量m_g、粗质量 \(n_v=\sum_g\omega_gm_g\)，对粗提升 \(\xi_{v,h}\) 置
\(X_{g,h}=m_g\xi_{v,h}/n_v\)（n_v>0），零粗质量时全置0。按同一权合并即逆转，所有预算不变。该等价只是指定局部行族的投影，不是共同目录或完整SPE实现定理。

## 10. 原16-hist的完整624有限表示

本节表示与第8节扩域见证分开。原16hist的第一类非对角轨道有78个非空词对组，每组4个旧RZ状态各接16个宏隐藏态，共4992新非负变量。312个质量等式以正反两行编码为624行，再加全部624预算，总共1248行。当前质量为0的hist和RZ状态均保留。

在完整11418×7639 ZZ基底上，矩阵为12666×12631，老行、老列、W和归一化前缀不改，新列目标/归一化为0。条件质量只按字面重数/30乘一次。表示证明见 complete624_actual4_R00_v1_contract.md 与同前缀 mapping.json。

矩阵 complete624_actual4_R00_v1_matrix.json.gz 的SHA为
556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a，
映射SHA为24a601ebc1e2f7dc5e175bca453a5ab05433e046dfc7c2a782e830849817d109。
Main独立核3,115,008个特征系数、312质量联系、624预算和1920个字面查询，全部PASS。

此表示只闭合 actual第四源/R/第一非对角结构的完整624局部投影；其他来源、主题、不同旧组的共同会员仍在范围外。有限精确原始/对偶另由计算对象 M-ddceaa3d53064498b3e833a32e1f3b6f 承担，不能代替本页严格性证明。

'''
anchor = '## 文件定位与证据等级'
assert anchor in text
text = text.replace(anchor, appendix + anchor, 1)
hier.write_text(text)

body = source.read_text()
body = body.replace('status: "proved-with-exact-scope"\n',
                    'status: "proved-with-exact-scope"\ntruth_status: "proved"\n',1)
body = body.replace('本页是上述稳定身份的正式正文建议稿，仅在研究工作区准备。其独有数学包括：',
                    '本页由Boss2 Main全文审阅并核准后回流。其数学内容包括：',1)
rz.write_text(body)
manifest = {
    'ids':{'hierarchy':'M-b1b4276f0ec747ed8c347bda65c9e0af',
           'finite':'M-ddceaa3d53064498b3e833a32e1f3b6f',
           'shared_rz':'M-736ccd964c384f16a6816eebcb468f2f'},
    'bodies':{'hierarchy':str(hier.relative_to(R)), 'shared_rz':str(rz.relative_to(R)),
              'finite':'archives/customer-attraction/subarchives/six-providers/state/计算/同源跨枝增强必要图的精确最优值与半界缺口--计算.md'},
    'initial_sha256':{'hierarchy':sha(hier),'shared_rz':sha(rz)},
    'scope':'Hierarchy version 2 and new shared-RZ income lemma; finite version 3 prepared separately.',
}
(B/'formal-round6-identities.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
