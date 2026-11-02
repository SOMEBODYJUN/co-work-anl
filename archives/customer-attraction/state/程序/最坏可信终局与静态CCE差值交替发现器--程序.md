---
id: customer-attraction/worst-credible-terminal-static-cce-gap-search-program
kind: program
type_tag: 程序
title: 最坏可信终局与静态CCE差值交替发现器
status: complete-source-contract-with-small-deterministic-interface-check
truth_status: floating-discovery-program; no-new-general-bridge-or-counterexample
review_level: full-4806-byte-source-read; independent-ordered-history-Fraction-check-and-individual-CCE-LP-comparison-on-five-small-inputs
scope: 正整数k个共同目录标签、m名单位提供者；非空兴趣型非负质量；全部有序历史纯策略；同人数全部静态CCE
summary: 完整解释search_cce的计数可实现终局递推、全部有序策略重构、静态CCE计数LP及固定策略固定乘子客户交替；target是排序代表，改变客户后不重算最坏SPE；保全部CLI、覆写、容差、依赖和失败边界。
source_ids: [60bd06f1f9dcdc4e5347]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/search_cce.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/search_cce.py
---

# 程序身份与目标

本对象保全原4806B `search_cce.py` 的全部实现合同。[原字节、来源与当前小型复算](../../tools/evidence/security-cce-search-program-primary/README.md)独立保存；两个冻结提交同一SHA-256，不算两份独立实现。模块只依赖标准库、NumPy和SciPy/HiGHS，不读取相邻JSON，不导入规范CAG模型或SPE求解器。`if __name__ == "__main__"`保护搜索；导入会加载数值库和定义函数，不会运行随机trial或写文件。

数学基准为[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、m名单位提供者按全部有序历史各选一个主题，客户的一单位价值在最终覆盖者间均分。全部重复、离轨历史和弱最优平局保留。软件用k个可区分标签，允许不同标签同覆盖及空主题；数学目录若要求不同覆盖集合，须对最后的候选另核，不能由参数k直接认证。

每个非空兴趣型T⊆{0,…,k−1}有非负质量r_T。整数质量代表互异单位客户的重数；非负有理数共同清分母可还原单位客户。浮点质量没有自动完成此还原。完全不喜欢任何主题的客户对所有量贡献零，故mask0省略；全兴趣mask `2**k−1` **保留**，与另一份明确删除全兴趣型的[完整策略锥CCE程序](完整策略锥与静态粗相关对偶的交替接口--程序.md)不同。

程序寻找某个客户向量r和完整纯SPE σ，使

\[
 C_m(r)-W_\sigma(r)>0,\qquad
 C_m(r)=\min_{\mu\in\mathrm{static\ CCE}_m}\mathbb E_\mu W.
\tag{GAP}
\]

同实例静态CCE允许任意相关、任意玩家不对称的有序终局分布，要求每位i对每个**事前固定**标签a满足E[u_i(z)−u_i(a,z_−i)]≥0；静态偏离冻结其他终局行动。顺序偏离则沿σ的真实离轨子树。正gap攻击同人数**强静态CCE福利替换桥**，不是直接攻击OPT_m/2，也不是把C_m/m当作真正静态安全值v_m。

# data：类型、计数与收益张量

`masks`为1至2^k−1升序。`profiles`按`combinations_with_replacement(range(k),m)`的确定顺序枚举排序行动串，共N=binom(k+m−1,m)个；对应计数q及反向索引ix。设I_(aT)=1_(a∈T)，d_T(q)=Σ_aq_a I_(aT)。三个张量为

\[
 u_{qaT}=\frac{I_{aT}}{\max(d_T(q),1)},\quad
 w_{qT}=\mathbf1_{d_T(q)>0},
\]

\[
 g_{qaT}=w_{qT}
 -\sum_{b:q_b>0}q_b\frac{I_{aT}}
 {\max(d_T(q)-I_{bT}+I_{aT},1)}.
\tag{1}
\]

若q_a>0，则(u_q a·r)是一个最终选择a者的真实收益。q_a=0时该数组项只是方便的代数存储，不能当成“往现有终局再插入一位a”的收益；后面的可信递推只在当前行动a确实属于该孩子终局时使用它。所有实际非零分子处负载至少1，`maximum(...,1)`只是避免0/0，没有为未覆盖客户创造收益。

式(1)对每个原选择b的位置分别先删b再换a，乘q_b合并这些玩家；所以(g_qa·r)=G_a(q)=W(q)−Σ_i u_i(a,z_−i)。它计算**固定人数**的静态替代，不增加第m+1位。w_q·r为覆盖福利。

# solve_spe：全部可实现计数与一棵完整树

给定原r，内部`outcomes(q)`用本次调用独有的缓存递推；|q|=m返回对应终局索引。非终局时，对每个a取孩子R(q+e_a)，令

\[
 M(q)=\max_a\min_{j\in R(q+e_a)} U_a(j),\qquad
 R(q)=\bigcup_a\{j\in R(q+e_a):U_a(j)\ge M(q)\}.
\tag{2}
\]

源码把最后比较放宽为≥M−10⁻⁹。精确版本的必要性是每个孩子真实SPE收益不低于该孩子的最小可实现值；充分性是实际孩子实现目标j，其它孩子各取最小收益SPE，所有有序子树可以独立拼合。[可信续局菜单](../算法/可信续局菜单与完整策略重构--算法.md)有完整证明，并区分“可实现全部终局”与“枚举全部完整策略”。本程序只保留各终局索引一次，不枚举全部策略。

根target在R(0)中按`(welfare,index)`最小，精确理想情形是最坏SPE终局；10⁻⁹容差和浮点r使实际返回值须作独立精确认证。`expand(h,q,desired)`保留真实有序历史h：按标签次序选第一个可以实现desired、当前收益达到同一floor的行动a，写入σ[h]。实际孩子继续desired；其它孩子b选`(U_b,index)`最小的可信终局，再分别展开。故同计数只缓存**可实现集合**，没有把不同有序历史的动作强绑成同一个函数。

展开同时为每个有序节点和每个b加入

\[
 \Gamma_{h,b,T}=u_{\mathrm{desired},a,T}-u_{\mathrm{childdesired}(b),b,T}.
\tag{3}
\]

这恰是沿同一σ实际偏离后继的收益差。先递归孩子、再追加该边，故行序为深度优先后序。自身动作也加入零行；不去重。总动作数H=Σ_(t=0)^(m−1)k^t，Γ有kH行。默认k4/m3时H21、Γ84；有序终局64却只需20个静态计数列。这些计数单位不可混用。

精确非负r满足Γr≥0当且仅当这份**固定完整策略**是SPE，理由见[完整策略重数锥](../定理/固定完整策略的客户重数锥--定理.md)。σ的真实根路径可能不是排序行动串；输出`target=profiles[target]`只给该路径的排序代表。例如计数相同的2333与3332不是同一个有序路径。复用时须从σ的空历史`""`开始执行，不能把target直接当作逐人行动顺序。

# cce：允许所有不对称CCE的静态最低值

原函数对计数列分布ℓ求

\[
 \min_{\ell\ge0}\sum_q\ell_q W_q,
 \quad\sum_q\ell_q=1,\quad
 \sum_q\ell_qG_a(q)\ge0\quad(\forall a).
\tag{4}
\]

任意CCE相加个体约束就给聚合行。反之，对满足(4)的计数分布，在每个计数内部均匀重排玩家身份，每位的每个固定偏离损失恰为聚合值的1/m，所以得到真正CCE。匿名对称化不改变福利，因此(4)精确求的是**所有**静态CCE最低福利，不是把输入分布限制iid后得到的另一个值。详见[占用表示](../候选/较弱CCE福利桥的占用LP表示与边界--候选.md)。

实现用`linprog(wc@r,A_ub=−(g@r).T,...)`。返回依次是最低值、y=−`ineqlin.marginals`及最优计数分布ℓ。对偶是

\[
 C_m(r)=\max_{y\ge0}\min_q D_y(q;r),\qquad
 D_y(q;r)=(w_q-\sum_a y_ag_{qa})\cdot r.
\tag{5}
\]

因为CCE的E G_a≥0，E D_y≤E W，逐列D_y≥L才给所有CCE的福利下界L。源码没有限制Σy=1；也没有独立有理化、核非负/逐列/原始残差，只`assert lp.success`。此assert不是有限有理证书，`python -O`还会移除它。保存的`dual_y`因而只是数值建议。

# main：固定σ与固定乘子的两块交替

CLI为`--k 4 --m 3 --trials 1000 --seed 1 --out PATH`，仅out必填。NumPy `default_rng(seed)`的同一随机流贯穿trial。每个非空mask先独立抽0,…,7整数，再独立以1/2概率保留；全零trial跳过，其余除以总质量，得到Σr=1。该归一化按**总客户质量**，不是按W_σ=1。

每个非零trial只调用一次`solve_spe`，固定target、Γ和σ。其后最多12步，每步：

1. 对当前r重新求(4)，得到val=C_m(r)及新y；计算gap=val−w_target·r。
2. gap超过跨全部trial的best至少10⁻⁹时，先打印一次进度、再覆写out。gap>10⁻⁷立即从main返回。
3. 固定此y，解下面客户LP；失败或新旧r欧氏距离<10⁻⁸则结束当前trial，否则换r继续。

\[
 \max_{r,t}t\quad\text{s.t.}\quad
 r\ge0,\ \mathbf1^Tr=1,\ \Gamma r\ge0,
\]
\[
 \big(w_q-\sum_a y_ag_{qa}-w_{target}\big)\cdot r\ge t
 \quad\text{对每个计数列q},\qquad t\in\mathbb R.
\tag{6}
\]

linprog目标系数末项−1，Γ块使用−Γ，逐列块使用负系数和t的+1，方向与(6)一致。理想精确情形下，新r在同一固定策略锥；固定乘子的t只给新gap的一个下界，下一步重新求(4)才有该r的CCE最低值。两块分别线性，但y与r乘积使联合问题不是一个LP；12步交替不认证全局最优，也不穷尽某个固定锥。

**客户改变后不重算最坏SPE。** 因Γ保持这份σ的真实IC，σ在新r上仍可作为分离见证，但未必仍是新输入最低福利的SPE。输出后续的`w`或target不可继续称“该实例最坏SPE”而省略这项区别。第12步若没有提前结束，源码仍解一次(6)并更新r，却已无第13次CCE评估；该最后新点不会自动出现在保存文件中。

这里没有将(6)的t保存到输出，也没有以其正负直接判定候选；停止阈值看的是每步**重新求得**的val−W。负面停止或未命中只涉及随机种子、选中σ和有限交替，不能证明强桥，已有[八/十三客户完整反例](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)已反驳全人数强桥。

# 输出、覆写与失败边界

进度stdout每次更新best打印一行JSON，字段为trial、step、gap、w、cce。out则以`write_text`覆盖旧文件，只含k、m、gap、全masks、全r、排序target、dual_y及完整sigma。sigma键以逗号分隔历史标签，空根键为`""`；完整动作表有H项。

文件**不含**trial、step、seed、trials、argv、软件版本、运行时长/退出码、val、W、t、最优原始分布ℓ、Γ、精确残差或OPT。val与W可从原数据重新计算，但不能把后补计算冒作旧保存字段；stdout若未另存也无法由out恢复完整时间序列。四份`cce_best*`是各自浮点快照，不是一个文件保存了全部搜索历史。相邻七份发现/整数/精确数据由[独立快照对象](../计算/静态CCE分离搜索快照与四十二客户证书--计算.md)逐源处置。

程序不会为out创建父目录；无权限或父目录不存在时写文件会失败。trials=0/负数或所有trial全零时不会新建输出，也不删除原有out，调用者不能把已有文件当本次结果。没有规范终结报告或返回候选布尔值；正常耗尽与找到候选都可能exit0。best初值−10¹⁰，首次有限gap通常即写出，**保存文件不意味着gap正**。CLI不校验k,m为正；本数学合同限k,m≥1，零/负维度和极大参数不作有效输入承诺。

data需要约N·k·(2^k−1)规模的u和g内存；完整sigma大小H随深度增长，缓存不能免除输出全树。没有超时、内存界或多项式算法承诺。后续精确认证应保原始输入、完整σ、全部有序真实IC、非负有理y及全部静态列下界，清分母回单位客户；若要认证CCE**锐值**，还需匹配的有理CCE原始分布和逐玩家固定偏离验证。

# 本轮五个小型接口复算与既有成熟证据

[当前小检查](../../tools/evidence/security-cce-search-program-primary/check_small_contract.py)从原码只调用data、solve_spe和cce；从整数客户自行实现Fraction逐玩家收益、**全部有序历史**的集合递推、真实后继、Γ全部系数及原行序；另用全部有序终局和m·k个**个体**固定偏离行构造另一LP，与原计数聚合LP比较。它不导入规范模型、SPE求解器、既有审计或相邻候选。当前真实输出见[完整报告](../../tools/evidence/security-cce-search-program-primary/small-contract-check.json)，环境和stdio绑定见[执行记录](../../tools/evidence/security-cce-search-program-primary/small-check-execution.json)。

| 固定输入 | k/m | 有序历史 / 含self比较 | 计数 / 有序终局 | 指定SPE W | 原计数LP与个体LP共同值 |
|---|---:|---:|---:|---:|---:|
| 三个不交单位单例 | 3/3 | 13 / 39 | 10 / 27 | 3 | 21/10 |
| 零客户 | 2/3 | 7 / 14 | 4 / 8 | 0 | 0 |
| 一人，两个不交主题分别1、2客户 | 2/1 | 1 / 2 | 2 / 2 | 2 | 2 |
| 空主题及两个同覆盖标签 | 3/3 | 13 / 39 | 10 / 27 | 1 | 1 |
| 单主题三客户 | 1/2 | 2 / 2 | 1 / 1 | 3 | 3 |

五例Γ系数逐项和顺序均匹配，全部精确SPE最小slack为0；原LP与独立个体LP在10⁻¹⁰阈值内一致，非负对偶、概率归一化、聚合原始残差及最小对偶列也核对。**LP对比仍是浮点数值检查**；三单例21/10的精确解析证明已有[安全下界与严格间隙引理](../引理/静态粗相关均衡的安全下界与三单例严格间隙--引理.md)。本批未重新证明或另授一个新定理。

运行总量准确为五次原solve_spe、五次原cce LP、五次独立个体LP；原main、随机搜索、客户交替LP、八/十三/四十二客户原验证器本批均0次。成熟的八客户锐值544/87、四十二客户W32/CCE下界33及两份八客户策略变体，直接复用[原核验合同与已存完整重放](../资源/八客户与四十二客户静态CCE分离的原核验合同--资源.md)，没有机械再跑；四十二客户33未认证为CCE最低锐值。后续安全值搜索即使复用data/solve_spe，目标和静态查询量词仍不同，不能借本cce函数授其maximin证书。

# 比较、关系与接续

全仓按原程序名、源ID、精确函数签名及CCE关键词检索，全文比较了共同模型、可信菜单、固定策略锥、静态占用候选、现有八/十三客户反例及安全值边界、初次五主题分离、原始对偶基准、完整策略锥交替程序、安全工作区入口和八/四十二客户原核验合同。没有发现另一份已发表同4806B原程序正文；相关程序提供数学接口而非本源已done的替代。两条策略锥实现的区别包括：本源先求最坏可实现终局、总客户质量归一化、全兴趣保留、每trial只固定一棵极小续局策略；另一实现以固定完整证书输入、W归一化并删除全兴趣。

关系判断为：共同模型提供定义域；可信终局递推实现可实现集合、极小后继构造实现一份完整树；真实节点IC定义其固定重数锥；CCE对称化给计数LP等价；固定乘子列和客户锥联合定义探索目标；旧JSON是该发现链的数值资源，后续Fraction原核验器才承担具体单位客户分离证明。程序与有限输出的关系是实现/发现证据，不是新的普遍推导或独立外审。正式超图留第三阶段，本对象未生成图。

接续应分别读取程序、快照和精确证书，给新候选补齐源/输入/动作/环境与有理认证；未命中不得推出桥成立。强CCE失败不一并否定较弱系数桥、跨人数平均桥或真正安全聚合，三人实例也不替代恰六人全称half目标。本批不认证实例规模最小性、全球新颖性或外部同行审查。
