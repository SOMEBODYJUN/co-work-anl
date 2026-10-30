# 未认领旁读交接：tiny-work、weighted-small 与 weighted-affine

本笔记只保存真实元信息、已完成的相关材料阅读及独立数学推导。**没有新主源全文阅读声明，没有本三源的正式正文或semantic receipt，没有新claim成功。** Boss通知GitHub代理CONNECT 403及network approval cancelled，要求停止新claim/取源/Git；本代理据此停止，不在后台继续。

## 实际生命周期与落点

1. 前一批`um-level-fixed-work-next`的2主源（0d248842c79fa87cc15e、a707d95d1e785d7fcec4）已经完整交付。Boss实际执行外部finalizer，确认4正文/25证据/3记录=32文件、18链接及8份原件hash通过。其交付入口为`cleanup/workspaces/Boss4/um-level-fixed-work-next/delivery.json`。本代理没有执行Git；此轮停止时Boss说正在local-only保全，**不能据本笔记把这32文件称为已pushed/done**。不修改它们或重跑768状态、旧tensor。
2. 下一批原拟ccda5c07c46ee14b1bcb tiny-work主稿与acb99150324dcb0d1a48 weighted-small主稿。Boss远端核对发现ccda已经Boss2领取，原子操作0新claim；它被排除，不写其新主对象、不done。
3. 本代理只读metadata后提出cc3fc3849a2e96e053fb weighted-affine作备用。Boss改拟acb+cc3，后又发现acb已被Boss2先领；该原子claim也失败、0新claim，cc3未确认认领。无权正式落这两源的对象或回执。
4. 本代理对上述ccda/acb/cc3三份**实际原主稿均尚未全文读**，也没有自行Git/show/fetch。缓存是否后来被其他人部分取到不改变这项实际阅读状态。以下推导是从已读索引合同与既有正式成果自行重构，不能冒作新原件实读或冻结审查。

## 元信息

| ID | 路径 | 字节 | 本代理实际状态 |
| --- | --- | ---: | --- |
| ccda5c07c46ee14b1bcb | research/current/unrelated_machines/tiny_work_stability_joint_rounding_and_selection_barrier.md | 12284 | 已读现正式三报告审查及账本相关段；原主稿未全文读；Boss2 owner |
| acb99150324dcb0d1a48 | research/current/unrelated_machines/weighted_small_st_barrier.md | 3593 | 只读metadata、CATALOG/CLAIMS相关段；原主稿及817字节原review未读；Boss2 owner |
| cc3fc3849a2e96e053fb | research/current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md | 8018 | 只读metadata、CATALOG/CLAIMS相关段及相邻正式成果；原主稿/历史证明/原review均未读；未确认认领 |

完整inventory行与比较依赖见同目录`metadata.json`，备用候选原metadata还在`boss4-next-cache/weighted-affine-backup-candidate.json`。这些是本地快照的metadata，不能代替最新远端owner裁决。

## 实际已经读的相关材料

* 全文：`archives/unrelated-machines/state/审查/小任务稳定联合舍入与选择障碍三源审查--审查.md`。它整理c5b/089d/d08三报告：给定CONFIG构造、5000位分母精确CLI、parity ell2/3全原调度枚举。原主稿一般证明在本任务尚未读，不能用这份审查摘要代替完整重构。
* 全文：`archives/unrelated-machines/tools/evidence/quota-selector-audits/source/selector_tiny_root_three_values_audit.py`及同目录`selector_tiny_root_three_values_audit.json`。**未执行**。报告六例的完整assignment数量依次16、64、1024、16384、12288、786432，三值OPT按其显式矩阵核；最后两例q4、mu3、nu2，ell2/3的OPT2、5/3。代码/报告是比较材料，不是本批新增程序完成。
* 全文：现正式`审查/仿射线全局dummy与任意汇点价格覆盖双源审查--审查.md`、`审查/直线集合打包与统一端口停车双源审查--审查.md`。前者global dummy及均匀线束，后者均匀权Hall三半和统一端口matroid；不能替代任意state-dependent权的cc3原证明。
* 前批已真实全文读并可复用：`审查/固定工作局部极小与真实凸包固定槽双源审查--审查.md`及其中最优凸包固定槽族；ST支撑最大件正式定理；有界配置任务数主稿和长审查（当前K5版本14c…，早期8f32…不能称同全文）。此处未重跑。
* 实际索引段：缓存`research/unrelated_machines/CLAIMS.md`的§2378–2385 weighted-small、§3558–3592 tiny-work/selector、§2817–2826 weighted-affine；`research/CATALOG.md`相应§674/677、§762–770、§1313–1319。这些是精确合同定位，不等于主源全文。

在正式tools/evidence中没有定位到c5b/089d/d08三原JSON字节；已向Boss报告需要集中取比较件，**没有声称已读这三原JSON或已重跑其CLI**。名字出现在正式审查中不保证原字节已被本代理取得。

## 独立推导A：weighted-small的工作量合同

下面依已读ledger合同重构；待主原稿与review到位后必须逐项比较定义，尤其beta/gamma范围、零边和Q的精确输入域。

假设每件非Q任务至少有一条small端，所有这些边p_ij≤beta；Q任务全部有限端均时间1。small支持数为d_j，逐机定义s_i为全部small端工作和、u_i为其中d_j≥2任务的工作和。若逐机s_i≤1且u_i≥gamma s_i，gamma∈[0,1]，则对每非Q任务在其全部small端等分质量1/d_j，有

    f_i=sum_j p_ij/d_j <= (s_i-u_i)+u_i/2
        <= (1-gamma/2)s_i <=1-gamma/2.

先对Q求容量1匹配。失败则每个实际调度至少在一机放两个Q，故OPT≥2；这里只是下界，不提供该分支的最优调度。若匹配成功，固定每机至多一件unit，只对small任务作一次全局ST匹配，tiny实负载≤f_i+beta，加回unit得C≤2−gamma/2+beta。所有任务使用同一个全局列身份，不独立拼逐机结果。

只有beta<gamma/2时该绝对上界严格小于2。Q非空时另有OPT≥1，成功分支可作相对解释；Q空则没有这个归一化下界。不得把此fixed-scale输出界改写成所有符合small条件的相对统一次二近似。

### Q空的明确相对反例（由既有固定槽族推导）

取m台相同机器，一个每端1/m的大任务，以及m²−1件每端1/[m(m+1)]的小任务，所有端均可用。每行全部small端工作为

    s_i=1/m+(m²−1)/[m(m+1)]=1,

每任务small支持m≥2，故gamma=1。给任何固定beta>0，m足够大时全部有限端≤1/m≤beta，所以Q空。等分支撑x_ij=1/m使每机总任务质量m、槽数m；全部m²任务的每个覆盖槽匹配都用完所有槽，每机恰m件。大任务所在机负载(2−2/(m+1))/m，原OPT=1/m（一个最优分量把大任务单独放、其余机器各m+1件tiny）。因此相对比率趋2，虽然absolute bound成立。此证明直接用现正式固定槽计数，不是新运行。

### 逐机密度不能免费改成全局平均

一个core强制一件unit且有10件只该core可用、每件1/10的small，总负载必2。另加10台机器分成5对，每对有10件两端均1/10的small；所有行small工作均1，后10行全部柔性。全局u/s=10/11、beta1/10，但第一行u=0不满足逐机条件。若误用全局gamma=10/11，会预测C≤2−5/11+1/10=181/110<2，与强制core负载2矛盾。其余pairs任意分配可使峰≤2，故真实OPT2。尚未建立程序输入/执行，这里是显式数学边界，不冒充原稿已有例。

## 独立推导B：完整sum关系的任意权半保留机制

以下依已读ledger模型自行重构，尚未与cc3全文/两路历史证明逐字比较，不记为该来源已完成。模型假设很强，只有它们全部成立才适用：素数R≥2、k≥2、R个groups j∈F_R，每组**完整**允许状态A_j={a∈F_R^k:sum_i a_i=j}，每变量有tagged R²点资源，选态a的线为(i,z,a_i z+j)。每state任意非负有理权w_{j,a}(i,z)，总和1，可为0。

选c,v满足sum c=0、sum v=1，并对每j取a^(j)=c+jv。它们全在对应A_j。对变量i，选态线满足

    y=c_i z+j(1+v_i z).

v_i=0时各j线平行不交；v_i≠0时唯一碰撞为z_i=−1/v_i，所有j在同一资源点相交，除此以外全不相交。先删各选态的所有碰撞点，令其丢权为ell_j。

均匀取(c,v)。固定j且条件于选态a∈A_j，有c=a−jv，条件下v仍均匀于sum v=1；因k≥2，每个v_i单独均匀于F_R。每z≠0成为碰撞的概率1/R，z0永不碰撞，所以

    E[ell_j | a] <= (1/R) sum_(i,z) w_{j,a}(i,z)=1/R.

从而E sum_j ell_j≤1，至少存在同一(c,v)使总丢权≤1。至多一组丢权>1/2；若无则全部保留≥1/2，若有唯一j*，把所有公共碰撞点给j*（其它组原已删除），其保留升至1，别组仍≥1/2。得到各组同时保留权≥1/2的真实互不交资源子集，非分别平均见证。

若标准normalized incidence编译确实按每state权1、selector private时间1、incidence private时间w/资源端时间1，则selected private负载=1+未外送权≤3/2，资源机≤1，未选state全部incidences留private负载1。它保留全部原jobs，不是假只排selected部分。应在主原稿到位后核完整机器/端点定义和OPT=2−V桥是否已由源证明。

显式位复杂度候选：共有R^k个states、各有kR个资源权的全表输入；枚举R^{2(k−1)}组(c,v)至多states数平方，逐个查总丢权，可确定性找≤1见证。不能只按succinct logR,k宣称多项式。此复杂度目前仅按上述完整全表模型推出，待原文核精确表示。

源CSP本身任意assignment恰满足一个sum=j关系，故value恰1/R。该低源值与partial≥1/2、实际≤3/2并存，只反驳包含这整个完整关系族且**仅改state权**的一概低partial soundness；不能否定避开本族的hard image、预处理或新gadget。

k1时sum v1使v唯一、条件均匀性失效：可将各唯一状态的权都放在公共碰撞点，min保留0、标准UM峰2。即便k≥2，若把完整A_j改成任意singleton关系，也能令两group仅有的状态都集中同一个交点，发生同样失败。因此完整关系和k≥2不是修辞条件。尚未取原稿，例的精确输入需与其边界核对，不能提前登记为来源中的反例。

## 后续仅在重新授权且实际认领后进行

先核最新owner，不重复ccda/acb的Boss2领取。对cc3若未来另获正式claim，再集中取主稿、2102字节review和5历史证明/审查，全文比较实际时间顺序及SHA。原meta候选文件列全7源50123字节；没有把它们标完成。本笔记结束时停止新claim、取源、Git和后台工作。
