# PEER-ENT1-3D：十三人具体完整 SPE 到 ENT1/SAIC 的独立复核

审查身份：Boss1，内部词 `PEER-ENT1-3D`。对象是已由 Boss2 done 的任务 `customer-attraction-3a-3a-c986a138e6639b6f`，并非新领包。本记录只供 Root 采用；未修改共享 clone、原任务、原 receipt、原边或全局图，也未重复发布。

**结论：接受当前精确版本的一条 accepted / unconditional / implies / whole_result 边，以及 receipt 对 formal follow-up 的 closed_overlaps 处置；没有发现需要阻断采用的数学错误。** 实际推出的是该指定完整十三人见证违反未缩放 ENT1，且 SAIC 与 ENT1 为同一式。这里没有一般的“有符号 delta 失败推出 ENT1 失败”定理。

## 1. 当前实际输入与字节身份

| 记录 | 当前精确值 |
| --- | --- |
| task definition pin | `18167d31223a55d5d1cf9f08f87392fe4ef666f0ed9be40f976ba777d63589f7` |
| input_pins 字典 pin | `b35db2b36fdcfbc6aa2dba8a5c94ac6d8abf1125149d78b60e49d6d33004cc99` |
| receipt 文件 SHA256 | `22d6559d125aa6cee0a63718b8a32790983a147fa8384382c40beb381b28acfc` |
| receipt 数学记录 pin | `700473878be3919a1fa5fd98d7dea3cfaf9e30d143d4ed41da4c5e6789920af4` |
| edge 文件 SHA256 | `b7eb24be3bec39308944f17b088fa87cc378ca54b7e8fee1bf9f9fce1628606c` |
| edge 数学记录 pin | `bc3c4301c7140db0b3cc96d5d1849cde9cdb8610b64ed524ae6078d8c94184fe` |
| edge review_digest | `92eb653aa1c7032bd196f99f42d59c42242bcb094cd4d70c50312c3398d36998` |

边路径为 `map/edges/customer-attraction-3a-3a-c986a138e6639b6f/thirteen-spe-implies-unscaled-ent1-saic.json`，edge_id 为 `boss2-m7-specific-spe-implies-ent1-saic`。

完整源端点 `M-7e204ccd7c6e4b7c8cbd5ddec64f5716` v3 pin：`008544b2506f11976f6144d22e945849206fed6dc9367c7511f169a03a5c012c`。
完整目标端点 `M-05b51399a0114768921338b101578273` v2 pin：`168d3c72291a54640e4bb0d3779b0fb0efba031884ad88923c1d1957f8f7a1ae`。
formal overlap peer `CA-FRACTIONAL-ACTUAL-LOAD-WEAK-NO-v1` v2 pin：`0ab7439e96f99aa0a69371377fde7fc2cccb843604300f06c0508900e28fe199`。

已经完整读取 actual task（包括嵌套 formal overlap 与 embedded receipt）、独立 receipt、整条 edge、原 proof/support、三个相关对象的完整 registry 合同及所有承重正文。另完整读取 M350 v4 合同作准确 canonical 去重比较。`refs.json` 保存全部完整对象记录、body/evidence refs、实际读路径的原字节 SHA、阅读范围和元数据核对结果。

task input pins 与当前对象 pins、edge endpoint pins、全部 edge evidence 原字节 SHA、evidence_pins、review_digest、receipt assets SHA 均相符；独立 receipt 与任务内 receipt 完全同一。本次只按读取到的纯 JSON 哈希规则核对记录身份，没有调用仓库 native 检查程序。

## 2. 完整策略资格来自什么证据

共同模型是有限不同单位客户、有限非空共同标签目录、单位提供者依次观察全部有序历史各选一次；保重复行动、弱平局、离轨历史及相同计数不同续局。客户兴趣重数表示不同单位客户，不是加权玩家。每个强制行动之后必须沿同一完整策略的真实后继完成。

源、目标的十三人输入是同一 `372216B` 压缩 packet，SHA `bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce`；本次还按原字节核对目标另一 evidence 路径的 packet 与它同 SHA。主题依次 `(A,B,T,D,E,P)`，客户类型为 A2、B2、T1、TD1、TE1、ADE3、BDE1、P25。

成熟完整资格由每个非终端六条观察行动边封闭、计数沿相应边恰加一、根零计数、终端深度13和全节点可达承担。于是每个有序历史唯一落到已核节点；自动机可以把不同历史合并，亦保留相同计数的不同节点。再沿深度逆序求规定行动的真实终局，对每节点六个原行动比较当前角色的真实收益，得到一步偏离条件，有限树原则给完整纯 SPE。这里的 27243 是压缩自动机节点数，不是展开有序历史数；18675 是决策节点数，112050 是含自身的六行动比较数。

本次完整读了成熟 8508B `audit_static_allowance.py`、5457B 原内部独审、1706B 冻结报告及相关现行正文，确认上述证据职责。代码独立展开单位客户并沿真实孩子逆推终局，不拿 desired/expected 字段认证；报告保存 minimum slack 0。当前源码多四个 alpha0 输出字段而旧报告没有，故不声称旧报告是当前源码的一次字节同一重放。这种既有版本差已由正文准确保留，不影响 alpha1 解析结论。

本次只解压读取两 gzip 的结构/元数据/指纹，以及 packet 的完整 instance 和指定真实 actual 链；没有全量重新审计。实际沿 `children[action]` 读出的节点为

`0,27228,27229,27230,27231,27232,27233,27234,27235,27236,27237,27238,27239,11013`。

这给 `P^10,A,A,B` 和末叶 `(2,1,0,0,0,10)`，不是读 expected_path 代替路径绑定。replay gzip 的 source_sha256 绑定同 packet；本次只读其 metadata、18675 条保存记录的长度及第一条完整记录，未重新验证 112050 项。

**成熟大数据继承而非本次重算：**完整全节点 SPE/IC 资格、2002 查询中的368个坏点/两极值均沿既有精确证据使用。原 probe 源码与完整 signed_delta_report（包括12个菜单和总矩阵）已读，但没有 import/main/审计执行、2002重新枚举、LP、求解器或新科学程序调用。

## 3. 单向 whole_result 的完整推导

真实叶的客户负载为：A与ADE合计5名负载2；B与BDE合计3名负载1；P的25名负载10；T、TD、TE合计3名负载0。故 W=33。十个 P 玩家与两个 A 玩家各得5/2，最后 B 得3。A/B/T/P 的并集盖满36客户，允许重复补齐十三槽，故 OPT13=36。

目标使用固定实际全终局负载、未缩放 alpha=1：

\[
g(S)=\sum_{x\in S}\frac1{1+c_x},\quad R_0=\sum_{c_x>0}\frac1{1+c_x},\quad M_1=\max_Sg(S).
\]

逐类型而非跨 alpha 迁移，六个合法查询分别为

\[
g(A)=5/3,\quad g(B)=3/2,\quad g(T)=3,
\quad g(D)=g(E)=1+3/3+1/2=5/2,\quad g(P)=25/11.
\]

因此确实检查了全部六主题最大值 M1=3，且

\[
R_0=5/3+3/2+25/11=359/66,
\qquad 13M_1-W-R_0=39-33-359/66=37/66>0.
\]

这是存在一个完整合法十三人 SPE 使全称 ENT1 失败。M05 是正确的反例存在对象，并非待反驳的 ENT1 全称候选，因此方向是源 `implies` M05；写 `refutes` M05 会反错对象。

SAIC 别名也完整支付：对任意实际终局，未覆盖客户贡献0，已覆盖客户逐个有 c/(1+c)=1−1/(1+c)，故

\[
B=\sum_x\frac{c_x}{1+c_x}=W-R_0,
\quad J_T=g(T),
\quad m\max_TJ_T+B\le2W\iff mM_1\le W+R_0.
\]

本例 B=1819/66，同一失败量37/66。这个普遍恒等式只依单位客户和实际负载定义，不要求额外未证付款前提，所以当前 unconditional 准确。源使用其完整指定 witness；虽然只用源结论的一部分统计，得到的目标整条反例/别名陈述已经完整成立，无须降成 contribution。目标主正文保存的另一 m4/p5/350 可行点及旧 LP 行为属于背景资料，既非 M05 本条陈述，也未被此边冒称推出。

## 4. 必须保留的条件、量词及禁止外推

1. 这条边是指定十三人、36不同单位客户、六标签、完整纯 SPE 的同一实际叶推论。没有“每个 delta 粗预算反例均导致 ENT1 失败”的一般关系，也没有把不同输入的付款助手同一化。
2. ENT1 的失败是一个合法最大单查询的失败；本例只有 T 达到最大值3，不是全部六 query 都坏。重复 T 十三次只覆盖3客户，不能当最优覆盖元组。
3. alpha=1 是本边目标。alpha=12/13 的实际缩放桥和 alpha≥12/13 区间虽有成熟相关结果，各保各的目标；本边没有凭名称替换 alpha、另选背景或真实查询终局。
4. SAIC 与 ENT1 逐式同一，不产生第二独立付款。静态代数 OPT≤mM1+B 仍真；其充分预算失败不反 half。本例 2W−OPT=30，十三人也不属于恰六人限制域。
5. `P*` 允许删冗余而保最多m槽；`K0` 是覆盖最优的固定m槽费用。私有客户迫选A/B/T/P，所以本例 P*=557/66，九个额外槽可用最便宜B补齐，K0=724/33。W+R0分别多出30与33/2，不能从本边否这两个存在候选。H4还涉及真实后继和共同最优排列，亦未被此单 query 失败否定。
6. 源 M7 反的是“所有共同 mu”及“所有最优计数诱导 mu”均可付粗 delta 预算。其同一 SPE 已有好最优 query；一般每份 SPE 存在一个共同最优 query 并同时支付独立余项仍开放。
7. 源真实 delta 来自中继菜单/真实末回复，跟目标静态 g 及 H4 债不同。反向只知 ENT1 失败和静态 g 不自动提供12菜单、总矩阵、2002统计及全部信用；本包没有反向 whole-result 或 equivalent_to。
8. 信用归一不能省掉：2399/429 是累计 G，实际扣2399/5577；1373/507扣后为12704/5577，再减18/13才是4982/5577。累计 overlap441/2须再除13，实际扣441/26，最终超额−179225/11154。因此同点没有反保全部信用预算；不能把 adjusted_total_delta 改名为另一 coarse envelope。

## 5. formal follow-up overlap 的闭合核对

task 的 `definition.context_plan.overlap_comparisons` 明列 `(M7, CA-FRACTIONAL-ACTUAL-LOAD-WEAK-NO-v1)`，状态 follow-up/3B。不能因其嵌套而漏审。本次完整读 peer v2 合同及同页四主题全人数构造、全有序历史证明、查询代数和独立十三人段，确认 receipt 的 `closed_overlaps` 有实质依据。

peer 给每个 m≥2 的 A/B/Q/D 四标签、兴趣重数 A:(m−1)、Q:1、AD:1、BQD:m(m−1)。全部B前缀非末位取B、末位取A；其它有序历史由两个单位奖金资源 Q/D 的完整逆归纳 beta 续局。这是构造完整策略，不把任意 SPE 限为计数策略。非全B上已有A时，非A行动的大块收益 C(a)=m(m−1)/(m−a)≥m，改A至多m/2；没有A而已出现Q/D时，首次改A与改D给同一 beta 子状态/真实后继及相等收益。改B少奖金；Q/D之间由 beta 最优。全B上遵从收益m，改A至多m，改Q/D共同块m−1加至多1；末位A/Q/D并列m，B得m−1。确已穷尽所有有序历史与原目录行动，短视贪心不能取代 beta。

actual 为 B^(m−1)A、每人m、W=m²、OPT=m²+1。令 alpha=(m−1)/m、Delta=m²−m+1，最大查询是

\[
M=1+\frac{m^2(m-1)}\Delta,
\quad (m-\tfrac12)M-W=\frac{m^2(m-4)+3m-1}{2\Delta}>0\quad(m\ge4).
\]

但这个四主题族有

\[
W+G-mM=\frac{m(m-1)}\Delta+\frac{m^2}{2m-1}>0,
\quad v_m\le m,\quad2W-OPT=m^2-1>0.
\]

故它否定的是实际缩放的弱桥，精确税在该族反而通过；它没有给六标签旧自动机的真实 delta 菜单/信用，也不能由弱桥失败推出未缩放 ENT1。反向固定十三人 witness 不推出四标签∀m族。同页另一个十三人段是不同输入，不是四主题主 Claim 的 m=13 代入。这个具名对象对已经比较清楚，没有尚缺的具体迁移问题非得另开3B；一般共同最优 query 的数学 open 仍保留。接受此次 closed_overlaps，但不把它理解成关闭一般研究义务。

## 6. canonical 与本地 integration 状态

按当前 registry.edge_files 对2315份 canonical JSON 只做 edge_id/端点字段筛查，并保存每个实际读路径原SHA；这不声称逐条语义审阅2315条边。M7/M05端点只有本次指定边命中。四主题peer另有已存反弱桥及PCAP贡献关系；完整读了这两条相关边，未复制它们。

完整读已存 `ca-r36-root-stationary-witness-to-unscaled-insertion`：SHA `6d86d996fd580245bda754ecafa9223b175d0ae5fbe6ed3ffc6fa516c6dfd690`。它从根平稳核见证到 M350 v4，目标为所有 alpha≥12/13 的实际精确税失败。其同witness与alpha1算术是成熟数学；源身份和完整目标范围不同，不等同本次 M7→M05 的delta见证到 ENT1/SAIC 关系。本次没有再建根核→M350边，也不宣称新发现37/66。

本地 integration 已列该任务相同 receipt pin 和该边相同数学记录 pin，canonical清单亦已含该边。`pending_changes` 尚列 M7、M05 和 edge_id，符合 Root assemble 后等待定向3D采用的状态。本次无远端/Git/native读取，**不能据此判定原Boss是否已经把这一当前精确版本推送集成**；Root掌握发布事实，若已发布仅采用本审查记录，不重复集成/发布。

Root应关注的一项覆盖展示细节：当前 M7 coverage 为 linked；read-add目标 M05 虽列该边，coverage仍为 needs-decision，理由是尚无核心比较批。这与边完整支持目标并不矛盾；M05是本任务只读端点，本次没有擅自代交它的独立核心覆盖。3D说明应据实际任务范围写，不能把有一条入边自动宣称目标全部比较任务都已done。

## 7. 交付范围与未付工作

本次无修正文案、无新边、无需要发布的 follow-up，无数学阻碍。建议 Root 可原样采用该当前边、M7 receipt 和 formal overlap 闭合；保所有量词/条件/开放选择义务。

`refs.json` 提供37份定向读路径及2315份canonical字段筛查指纹、task definition/input/receipt pins、完整端点记录/pins和全部edge绑定。`review-summary.json` 提供机器可读接受结论、未付范围及Root注意事项。科学/审计程序执行数为0，仓库native/Git/网络调用数为0；全部写入只在本worker目录。

最终指纹补充：Root在审查期间新增6条canonical边；本次补读其端点字段后，最终2315条名单与选定registry一致，无删除、无已存边字节变化，M7/M05仅命中指定边。task definition、receipt、边字节、两端点和formal peer pin再次保持不变；相关元数据后续版本与最终本地integration选段已存refs，未因此重跑数学。
