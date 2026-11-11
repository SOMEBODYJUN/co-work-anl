# 3A 实读比较：固定正阈值的 DegreeThree 链式降度

任务：unrelated-machines-3a-3a-826effc7485414e4。作者：Boss6 委派 worker。结论：当前核心陈述已完整核清；M-080d9b22ae87408f9a673a898c7a6dc3 的 read-add 已完成，现为 1 core/4 read，以其 finite unit-helper 路径给本 core 交一条完整缩放关系，覆盖为 linked。有限配置桥已经登记，不另称新漏登记。∞ helper 的全正阈值扩展与 InfDegreeTwo 排序、交域 gap 已有自足证明，单独提交仓库外提案，已由 Root 登记并交已发布3B任务boss6-inf-chain-transfer-3b-ea6be0c00b1186cf承接；它们不是数学 open，也不塞进旧对象的整个结论。

## 1. 当前合同与实际输入

开始核到任务 claimed/Boss6，claim request 为 f9d6aced0eae4e8cb894cafcc74b9af4；Root 后续发布 read-add，首轮read-add request为706e57ae1ea44043b5c2bef219bec8f8；M080d的最新已发布read-add request为98644ff1504b43e7aff93ab785de06ad，当前仍claimed/Boss6。worker 仅读取 clone，未执行 Git、work.py、队列写或认证。

| 角色 | 对象 | 版本 | 当前 pin |
| --- | --- | --- | --- |
| core | M-a9534c70ffa74fca9a91cd270468de3f | 3 | 608415f3a648158ae4b612cc7a9f2e21699ee3b73ef786908e0f40654b33fb44 |
| read | M-e52574ff126d4b128f222053c97bf596 | 3 | eff19fc84cf112c156c8fc3228f91b9cc55f928a88b6b3bc21fd9c5a2094130f |
| read | M-b126c4b3ff29400589f7f38abdca4d85 | 3 | 290a361d6679820d0f4564c518bb120fd486835a7bf8cd08e6660438cf690029 |
| read | UM-VW2010-THEOREM12-BACKEND-PRECHECK-v1 | 1 | 16a2920abfebbaed76d2492aee350d1b801fcfe5eb40c65c9a4f33ddddb02584 |
| read | M-080d9b22ae87408f9a673a898c7a6dc3 | 4 | 5041d21ea4cc71de0cf1e759aade84c0cc09a86d8539510dc3683242679ff85c |

上述四份原登记合同均已读取；另实读 M-080d9b22ae87408f9a673a898c7a6dc3 v4 完整合同及 body 全文（pin 5041d21ea4cc71de0cf1e759aade84c0cc09a86d8539510dc3683242679ff85c），Root已完成其read-add；原发布时五端点pin已核对；本次F v4 publication refresh已按Root同ID刷新request 89d6e526e7494500b869128903161801执行最终guard：当前仍claimed/Boss6，五个input pins与当前registry记录逐一匹配，唯F改为v4 pin 5041d21ea4cc71de0cf1e759aade84c0cc09a86d8539510dc3683242679ff85c。以上 pin 按现行 research_runtime.pin 的稳定 JSON 规则独立计算并与 task.input_pins 一致。这里只报告字节核对，不冒充 Root 的 native bind/check 或远端状态查询。

核心 body 是共享文献整理全文，SHA-256 为 a0d8bb0b5261e46ef6843a1e2c9bb812393f22953129ffba03313e0c16b5fb36；必要 primary maxmin.pdf 的 SHA-256 为 7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f。直接从该 PDF 读取印刷页 8、9、13 的文本，并结合仓库原有 maxmin.txt 的指定连续区间核对模型、定理及比较原文，没有声称阅读完整 49 页。

## 2. 核心的整数阈值见证链

固定 t>0。对每件正度 d>3 的旧物品 j，列其正值玩家 i_1,…,i_d，建立 d 份副本 c_1,…,c_d；c_r 对原玩家 i_r 的值等于原值，其余原玩家值零。另增 d−1 位 helper h_k，只对 c_k、c_{k+1} 值 t，未列端值零。

正向解码：一份达到 t 的整数分配令每位 helper 至少取得一份相邻副本。这些物品不能重用，故 d−1 位 helper 占至少 d−1 份，至多一份可正值服务原玩家。将它投影成旧物品 j，原玩家所得价值不变；旧低度物品保留不动。可能有 helper 取得两份，此时可以没有副本服务原玩家，所以精确用语是“至多一份”，不能强称原玩家恰用一份。

反向构造：若旧物品给 i_r，保留 c_r 给它；k<r 时把 c_k 给 h_k，k≥r 时把 c_{k+1} 给 h_k。每位 helper 得到不同副本且效用 t。若旧物品未分配，任取 r 留空；必要时删除零价值使用再构造。低度物品仍给原拥有者。得到同一阈值 t 的整数见证，全部原玩家效用保持。内部副本正度为至多 1 个旧端加 2 个 helper 端，即≤3；端点副本至多2。

严格正阈值是承重条件；t=0 时 helper 不用物品也达标，占用计数不能沿用。有限 helper 版没有任意 OPT 全值等式。例如四玩家各有私有值100物品，再共享一件对四人均值100的物品，原 OPT=100；t=1 后三位 helper 受四份副本限制，输出 OPT=1。

若 S=Σ_{d_j>3}(d_j−1)，则 n′=n+S，m′=m+S；正值边数 E′=E+2S。通常 n,m≥1 时规模 O(nm)，但 n=5,m=1,d=5 时 n′=9,m′=5，不能逐项都声称≤nm。空物品且非空玩家的正阈值直接为 NO。原值逐正边保留，新增 t 按给定二进制长度收费，顶点/边数及稠密矩阵输出均多项式；不按 t 的数值大小枚举。

原 Theorem 2.4 的 MaxMin 后“1”是脚注标，脚注讲 MinMax 的另一个替换，不是 MaxMin1 模型。Root 已发布的最小勘误把这一点及 O(nm) 精确界修正；本轮不再改源或重做源审计。

## 3. 与两个 DegreeTwo 算法的真实比较

### 3.1 历史四近似 M-e52574ff126d4b128f222053c97bf596

实读 primary §3（maxmin.txt 453–595，包括 Figure 3、§3.1–3.2）及完整对象合同。它在每件物品最多两正端的模型上输出实际整数分配≥OPT/4，允许两端异值。模型与核心同为不可分非负加性 MaxMin，但度约束更强。

核心的内部副本恰可有三个正端，不能给此算法当输入。算法将非整数边整理为1/2时保持物品容量，确切依赖每件最多两非零端；若一个三端物品各有1/3，局部全部改成1/2就总占3/2。后续大边树组件内“非叶物品已无第三个外部 taker”的推理也依赖 degree≤2。核心没有消去第三端的映射，所以“先降度到3，再调用四近似”缺少明确且未提供的 degree3→degree2 保证。原输入已经 degree≤2 时降度不改任何物品，至多是恒等适用，不能因此制造核心支撑四近似整条定理的边。

### 3.2 VW2010 实际整数二近似后端

实读其完整 body §1–7 和必要 evidence 的唯一节“二度MaxMin的组合二近似：Theorem 12”。其 forced-largest 把强制物品从两个玩家列表全局删除；剩余物品的两个 occurrence 组成一类匹配，逐玩家降序相邻 occurrence 配成另一类匹配，形成偶交替分量；二染色使同一物品恰给一人，并给每玩家至少 T/2。二进制有理整数化与单侧二分保证总位多项式。

这同样不是三端后端：每件三个正 occurrence 时不再有“同一物品两个 occurrence”的匹配结构。core 的有限 helper 值 t 并不把 helper 正端从支持中删除。因此不能把此整数 OPT/2 后端直接迁到核心输出，也不由此获得一般 MaxMin 的整数二近似。

此外，该后端对阈值 T 的 success 只保证实际值≥T/2；failure 才认证原 OPT<T。核心保的是指定阈值可行性，不会把这个 success 升成精确 T 可行证。泛指而言，若另有适用于 DegreeThree 的 α-后端，在原 t 可行时产生每位输出玩家值≥t/α>0，则同一 helper 计数能解码原玩家≥t/α；但该后端不是本任务任一现有端点，人数函数也应使用全部 n′。这个条件说明没有为 DegreeTwo 算法补足模型域。

## 4. 与 InfDegreeTwo 配置 gap 的真实比较

### 4.1 区分字面 ∞、算法重估以及玩家侧

primary 159–168 明确 InfDegree 是每物品的∞端数；不是玩家喜欢的∞物品数。§4 开头（595–615）明确先在 {0,1,∞} 值域展示，推广一般有限估值时会把大于 M/λ 的端重估为∞，而重估后仍须符合 InfDegreeOne/Two 要求。

不能笼统声称链归约永不满足 InfDegreeTwo。原值都有限、helper 取∞的原始链中，内部副本确实恰有两个∞ helper 端。但若其原玩家有限大值又被重估为∞，内部副本就可出现第三个∞端。若输入本来有∞旧端也有同样问题。将 helper 改为有限 t 后字面∞度为零，更不能把任意有限值自动看成已经符合论文 {0,1,∞} 大/小值类的算法。若已知每旧物品∞端≤2，则把这些旧端排在链两端可以避免第三∞端；这是后述新引理可付清的兼容性条件。

### 4.2 已登记旧 gap 及 primary 的真实证据范围

M-b126c4b3ff29400589f7f38abdca4d85 是存在家族的 Ω(n^{1/4}) LP gap，n 为全部玩家数，不是 NP-hardness。原 PDF 印刷页13脚注2只有“类似论证”声明；本 worker 没有把脚注当作展开证明。Root 的 pcsp-pending-math-review.json 对该对象已有透明重构；本次逐项复用、核对质量守恒与整数上界，没有运行 gap 程序。

重构取 T 份 H_T，每份含 root a_r、T 位 b_{r,k}、T 件 u 和 T 件 w。a 对全 u 值1；b_k 对其私大 u_k 值∞、对全 w 值1；另有 T−1 件 B_r，在相邻 roots 上值∞。阈值 T 的配置质量：root 的全u配置1/T，其两邻外B singleton总质量1−1/T；b 的私大 singleton 质量1−1/T，全w配置1/T。B_r 按(T−r)/T、r/T分给相邻roots的singleton。每件u、w、B总边际均为1。整数分配有一root无外大物品；若其取得s件u以满足V，则s≥V，对应失去私大的s位b共享T件w，sV≤T，所以V²≤T。

原 n=T²+T，m=2T²+T−1，得到 gap≥√T=Ω(n^{1/4})。物品 w 的总正度T，不能调用任何 DegreeTwo 后端。

### 4.3 已登记有限 LP 桥及需要承接的∞扩展

核心原登记合同只写整数阈值见证；它本身不是“配置 LP 也保持”的证明。本轮补读的现有 M-080d9b22ae87408f9a673a898c7a6dc3 body §4 已经给出有限 unit-helper 的这条完整桥，不是漏登记，不把它称为数学 open 或不可能：对每件旧物品各旧拥有者的配置边际 q_i（Σq_i≤1），补成留空概率 h_i≥q_i、Σh_i=1；按留空位置匹配其余副本给 helper。helper k 的两份 singleton 质量为1−Σ_{i≤k}h_i与Σ_{i≤k}h_i，每份副本的helper边际恰1−h_i，与旧边际相加≤1。反向每helper的配置至少耗一份副本，原玩家在同一旧物品上的总边际≤1，配置逐项投影保持值。∞ helper 版对全部正阈值成立；有限 helper=t 版对0<s≤t成立。这里没有声称 M-LP 变量原样保持。

对旧 InfDegreeTwo 家族取 T≥4，只需降低 T² 件总度T的 w。使用∞ helper，原 w 端值仍有限1，内部副本∞度≤2。新增 S=T²(T−1) 位 helper/物品，n′=T³+T，m′=T³+T²+T−1。整数 OPT 全阈值保持，配置 LP 阈值T可 lift，因此 DegreeThree∩InfDegreeTwo 有 gap≥√T=Ω((n′)^{1/6}) 的显式家族。∞度在此家族的玩家侧也≤2，但 root 总正度为T加外邻接数，b总正度T+1；没有两侧总度3。

有限 helper=t 的 LP 桥是已有 M080d 的缩放/局部应用，不能重复登记。可独立登记的增量仅为同一个∞ helper输出对全部正阈值同时保持及InfDegreeTwo端点排序，后接此具体交域家族。该家族还可精确计值：q=floor√T时，每block root取q件u，失u的q位b各取q件w，q²≤T，故OPT=q；s>T时每位root配置都须含外B，而T位root只对应T−1件B，故配置LP最高阈值=T。∞桥输出的精确gap为T/q=Θ((n′)^{1/6})，只是该族的增长阶，不是全类tight gap。它不能写成旧M-b126的原Ω(n^{1/4})整条结果由核心推出；旧gap也不能反向证明核心对所有输入的降度定理。自足∞扩展与推论置于仓库外proposal/chain-config-infdegree-two-lemma.md，Root已登记并发布3B承接任务boss6-inf-chain-transfer-3b-ea6be0c00b1186cf；不造self-edge或将新目标塞回旧对象。

## 5. 既有 SC 单位路径到核心的完整缩放关系

source 为 M-080d9b22ae87408f9a673a898c7a6dc3 v4，target 为 M-a9534c70ffa74fca9a91cd270468de3f v3。源body的唯一节“4. SC unit-helper 路径”已对任意非空有限SC agents和非负二进制有理值给出逐物品的实际分配双向变换；所保目标阈值正向≤1，反向任意正值。这个限制是目标阈值，不是每个估值≤1，更不需要先知道旧OPT≤1才能做一次阈值变换。

数学上对核心任意给定有限实t>0，直接把每条新helper的值设为t，并使用源的逐物品copy/左右matching公式。该证明只用正阈值、单归属及copy原值对应，不用数值离散化，故源虽在有限二进制有理输入上表述，其显式matching公式在任意有限实t处可直接逐项验证。算法编码的多项式声明另限显式二进制有理原值和有理t：此时可先用v_ij/t归一化有限原值，在目标阈值1应用源的unit-helper证明，再把全体值乘回t。单位helper变为t，原玩家的专属copy恢复原值。有限有理除乘与精确比较按输入和t的总位长多项式。若按文献记号还把原∞端纳入核心域，先用v̂_ij=min(v_ij,t)（∞截t）。任一bundle达t当且仅当封顶后达t：若含至少一个≥t端，单件封顶t已够；否则完全不变。因此先在有限v̂/t上使用源，最后把原玩家copy的估值恢复v_ij。正向实际owner拿自己的copy，所以其原效用准确保持；反向任意新阈值t见证经同一封顶仍达t，源计数投影可行，且原copy到原物品的值一一对应，恢复估值不降阈值。这个小步只付本次t，不宣称原∞的全值与有限封顶OPT相同。特别是即使旧OPT>1（归一化单位），只要给定旧分配已达阈值1，逐物品保留旧owner自己的copy仍保持每个旧玩家的全部价值，新helper各值1，因此新分配达到1；此边直接用这一构造，不从旧OPT≤1的精确最优值结论跳步。

局部应用必须说明，不能从“源变换所有物品”静默删helper。源证明对每个物品分别选择hole并匹配其自己d−1位helper，其copy和helper不与别的物品共享。故可仅对d>3物品逐项应用上述构造；对d≤3物品保留原物品及其原owner。正向原玩家获得每件旧物品的原值，新增helper每位达t；反向对每条保留的高次链用至少d−1个副本的占用计数合并，对低度原物品直接保留，不删任何仍存在的helper需求。不同物品的投影不冲突，原玩家总值保持。

若S=Σ_{d_j>3}(d_j−1)，这个局部源应用输出恰n+S位玩家、m+S件物品，内部copy≤3正端，满足核心对任意有限实t>0的全部固定t整数阈值与双向见证合同，并有§2的精确计数；n,m≥1时规模O(mn)，空物品的正阈值输入单列NO；二进制多项式界专指显式有理输入和有理t，不宣称任意实数有有限字符串编码。helper可从原文∞记号截到t的精确理由是同一固定t处非空singleton已经满足需求，既不删除正端也不冒称degree2。CONFIG保持是源已有的额外性质，此边的whole目标只支付核心原整数合同。

## 6. canonical 与交付边界

对 canonical 清单按本核心及实际候选端点检索，未发现 incident core 边。实际完整读到的 um-0195479a-vw-maxmin-to-degree-two-menu 把 VW 二正端后端迁入显式二度菜单。它不含本 core；其菜单端点也不是本包负责对象。故只把它作为现有接口范围的检索比较，不复制、不改 SHA，不计作本核心覆盖边，不列为本任务的新 asset 或 reused_read_only_evidence。其菜单值桥必要正文未在本次重读，不能冒称全链复核。

M-90610eea6c6447188c03208eaa549254（InfDegreeOne gap）、M-de7aec4bd7c24b0f9dc342c483c4a75e（严格2硬度）、一般 MaxMin 半整数声明只作登记候选定位，不是本包新增端点，没有迁移这些结果。§3.1 原文顺带含 Theorem3.1、§4原文含 Lemma4.1，不把读到这些文本冒作它们主任务的交付。

本任务提交一核心的准确coverage；read对象没有被重复记为核心。新增关系在M080d正式read-add后已列入asset，由Root最终native bind/check；内容是§5完整缩放所得core whole_result，不是LP加分性质替代整数目标。review与reading-ledger为本次说明资产，收据不把自身列asset。新∞扩展已经登记，已发布3B任务承接后续构图；这里没有待补的数学实验。worker未做native bind/check、队列done、推送或科学程序重放。


## 7. F v4 的有限 publication refresh

本次只完整读取 M-080d9b22ae87408f9a673a898c7a6dc3 v4 record，并检查一项已发布 evidence delta。F 的 model、statement、quantifiers、assumptions 及 body（8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66）完全保持；version升4，当前registration pin为5041d21ea4cc71de0cf1e759aade84c0cc09a86d8539510dc3683242679ff85c，objections仅追加本次澄清的追溯说明。

改动的“归一化菜单福利与配置证书双源审查”由旧SHA a5d9a684e8d8413457f5cf999e28b8a6aa93b140256be3031d6f3e2e02742195更新到63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255。本轮实读该页§一1（当前29–39行），确认P_gate正向全任务调度现已显写：root pin留root；选中组connector放gate、selector放相应private；未选组connector留root、selector去gate；剩余所有incidence（含未选states和零jobs）留各自private。没有重新审查福利13/8或其它菜单定理。

本边使用的是未改body的唯一节“4. SC unit-helper 路径”，本轮重读当前58–65行；其copy、hole、实际正阈值正反向及helper占用计数没有变化。P_gate的root/gate/private全任务澄清不进入本边的fixed-threshold unit-helper推导，故保原accepted whole数学、core v3、实际3B承接任务和全部范围边界。仅刷新F版本/输入pin、该证据版本和本review/ledger的字节引用；最终native重新绑定/检查由Root执行。

本次publication refresh的最终guard只读取本task和当前五个record计算pin，并核staging证据/资产SHA；未执行native bind/check、Git、队列写或数学程序。Root随后对原文件重新绑定和检查。
