---
id: customer-attraction-frozen-adjacent-query-bridge-two-old-strategies-and-fixed-PB-audit
kind: program
type_tag: 程序
title: 相邻冻结查询的旧两人策略与PB固定族核验
status: complete-source-and-report-reading-no-original-entry-rerun
truth_status: static-shift-and-last-pair-proved-old-family-checks-finite-general-early-pair-payment-unproved-here
review_level: exact-code-all-fields-and-mature-family-proof-compared-not-new-independent-audit
scope: 任意合法背景完整SPE的冻结查询桥合同；原程序仅两份h1两人策略和一份PB固定参数代数
summary: q_i−q_j为两方向正池差，q_i≤q_j+u_i/2，末位锚只付最后相邻对。旧两人各6含自身IC、PB2475人固定参数安全均不证一般FROZEN-PAIR；程序顶层执行并覆写同名JSON，本轮未导入。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/frozen_pair_bridge_attack.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/audit_frozen_pair_old_families.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/frozen_pair_old_families_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/frozen_pair_bridge_attack.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/audit_frozen_pair_old_families.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/frozen_pair_old_families_audit.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/README.md
---

# 相邻冻结查询的旧两人策略与PB固定族核验

6075B桥稿、4570B标准库源码、2292B完整原报告及3112B入口均完整主读，连9720B全树工作记录为五源闭包，[原件与比较快照](../../tools/evidence/frozen-pair-and-full-tree-credit-five-primary/README.md)保全。本文将一般静态恒等式、未付全称桥和原有限核验分别陈述，不从旧族未击破推正面普遍结论；全树付款尝试与BG-NEW后续反驳另见[接续边界](../资源/全树双重重置与终局代币共同付款的接续边界--资源.md)。

## 精确冻结查询及原候选

有限单位客户、有限非空共同主题目录、单位玩家全部有序历史纯SPE。允许空主题、重复行动、同覆盖标签、零客户及所有离轨平局。固定任意合法过去背景b_x，余r≥2名真实玩家的实际叶\(Z=(S_1,\ldots,S_r)\)，总负载与收益为

\[
 L_x=b_x+\sum_{j=1}^r\mathbf1_{x\in S_j},\qquad
 u_i=\sum_{x\in S_i}1/L_x.
\]

只在S_i内求和，L≥1。定义**冻结其余实际行动**后，移去位置i再插T的静态查询

\[
 q_i(T)=\sum_{x\in T}\frac1{L_x+1-\mathbf1_{x\in S_i}}.
\]

无实际覆盖的查询客户L0且不在S_i，分母1；其余亦正。它不是强制i改T后沿原σ真实重算的收益，早期SPE不直接给q_i(T)≤u_i。此区别与[静态/真实带符号债](../引理/静态插入与真实后继的带符号债务及完整松弛账--引理.md)一致。

原全输入候选是

\[
 \boxed{\max_{T\in\mathcal S}q_i(T)\le u_i+u_{i+1}
 \quad(1\le i<r).}\tag{FROZEN-PAIR?}
\]

它逐个单题、逐个实际相邻位置量化，不是“存在最优元组及匹配使全部冻结费用Q≤W”。后者已被[52客户唯一最优匹配反例](../反例/最优组合冻结匹配的一单位缺口--反例.md)否定，不能直接当本候选反例。也不是保当前槽的FTA额外查询，或只求某一给定最优T的排列。

静态安全值\(v_s(b')\)使用s−1槽不观察query实现的对手。固定i后的实际r−i主题是其一个合法静态竞争元组，故

\[
 v_{r-i+1}(b+S_{<i})\le\max_Tq_i(T).
\]

因此候选若普遍成立，就给每对实际首两人和至少相应静态安全值。背景嵌入又给各实际前缀的该值≥原根v_m(0)，末位自身亦≥v_m(0)。把实际位置两两分组，条件推出\(W\ge\lceil m/2\rceil v_m(0)\)，再用[静态锐计数界](../定理/静态混合安全值的锐目录计数界--定理.md)得\(W\ge\lceil m/2\rceil OPT_m/(2m-1)\)。这是**以未证候选为前提**的弱常数归约，不是half证明或本批新一般界。

## 角色转移恒等式、末位锚和未付premium

对任意两个真实位置i,j，逐客户比较移去S_i还是S_j：

\[
 q_i(T)-q_j(T)=D^+_{ij}(T)-D^-_{ij}(T),
\]
\[
 D^+_{ij}=\sum_{x\in T\cap(S_i\setminus S_j)}\frac1{L_x(L_x+1)},
 \quad D^-_{ij}=\sum_{x\in T\cap(S_j\setminus S_i)}\frac1{L_x(L_x+1)}.
\]

两池非负；D+中的客户L≥1，所以

\[
 D^+_{ij}\le\frac12\sum_{x\in S_i}1/L_x=u_i/2,
 \quad q_i(T)\le q_j(T)+u_i/2.\tag{SHIFT}
\]

这对任意合法终局成立，不用早期IC；源root随后提示可直接取j=r，无须逐相邻累加。只有真正末位处q_r(T)就是该真实节点的改题收益，故

\[
 \boxed{q_i(T)\le q_r(T)+u_i/2\le u_r+u_i/2.}\tag{LAST-ANCHOR}
\]

于是最后相邻对i=r−1确实满足FROZEN-PAIR，r=2时所有相邻位置因而都已处理。更早i+1还不是末位，\(q_{i+1}(T)-u_{i+1}\)可能是正的冻结静态Nash溢价。其准确未付账为

\[
 u_i+u_{i+1}-q_i(T)
 =\underbrace{u_i-D^+_{i,i+1}}_{\ge u_i/2}
 +\underbrace{u_{i+1}-q_{i+1}(T)}_{\text{可为负}}
 +D^-_{i,i+1}.\tag{UNPAID}
\]

完整后继IC尚未被这里用于共同控制中间负项。把q_(i+1)≤u_(i+1)当SPE性质等于偷换静态Nash；把同u_i重复支付SHIFT和premium亦不合法。LAST-ANCHOR允许以一份末位钱包控制这些查询的某个最大值，不允许每个早期相邻对各重新领取u_r。已有[静态正遗憾复制族](../反例/完整SPE静态正遗憾的四客户副本放大--反例.md)说明SPE可有正premium；该族的事实本身也不反本相邻对具体阈值。

## 原程序的两份完整两人策略

源码无外部数据输入，直接取客户0/1在A、客户2在B，故|A|2、|B|1，h=1。完整动作字典只有根和两个一历史：根A；首B后末位A；首A后分别末位A或B。`finish`在改变后的真实前缀按同一字典补齐，`utility`从单位客户最终覆盖人数求Fraction。

每份逐全部三个历史、两个行动比较，含自身共6项，合12。再从实际叶算两人收益及移去root后的A/B静态查询，断言最大query≤两人和。原报告两条各八字段，其全部数学值为：

| 首A后末位 | 完整动作(empty,A,B) | 实际叶 | 利润 | 冻结root查询(A,B) | IC含自身 | 首对−最大query |
|---|---|---|---|---|---:|---:|
| A | (A,A,A) | AA | (1,1) | (1,1) | 6 | 1 |
| B | (A,B,A) | AB | (2,1) | (2,1/2) | 6 | 1 |

两条`old_family`均为`terminal_reply_transport: |A|=2h, |B|=h, h=1`，其余七字段由表列出，其中`last_after_A`分别0/1，未省略一份策略。对任意整数h≥1，全客户复制h倍即得旧|A|2h/|B|h同族，所有收益与余量乘h；源码只实测h1，任意h结论来自这个解析齐次性。[既有末回复运输](../定理/末回复规范化的条件性对偶提升--定理.md)已给这两份全历史证明和终局AA/AB覆盖差，不能称此次新发现。

## PB固定背景族：参数、实际路径及全部代数字段

脚本硬编码

\[
 (k,d,q,t,r,Q,H,M)=(3,20,12,10,2475,2063,100000,10^9),
\]
\[
 f(c)=\frac{q-1}{M+c}+\frac1{M+c+1},\quad
 g(c)=\frac{Hq}{HM+c},\quad u=dkf(k).
\]

完整PB输入/合法背景/Fill-Copy-Punish-Greedy及singleton子树的SPE证明复用[成熟PB反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)。它有48,495,120个不同单位客户、r2475的完整后续子SPE，背景可由原目录动作合法实现且已覆盖全部客户。程序没有展开客户表、目录或巨大树，也没有再次认证其SPE。

在旧实际后续，前三人选同一三个real块，随后r−3=2472位Greedy每段先填Q−k=2060个其它real块，再把412个加至二，1648个停一，无未用real块。删除实际第一或第二人时，query可遇到最小real other-count1、dummy other-count r−3，故首位置的精确最大query为

\[
 q_{root}^{max}=d\max_{1\le\ell\le k}
 [\ell f(2)+(k-\ell)g(r-2)]
 =d[f(2)+(k-1)g(r-2)].
\]

这个max只有固定三个ℓ代数值，不是新参数或游戏搜索。原代码还核\(g(1)>f(1)\)，故任意实际位置的regular查询≤\(U_q=d[f(1)+(k-1)g(1)]\)，singleton≤1/(M+1)<U_q。旧Fill/Copy条件

\[
 kf(k)>f(t)+(k-1)g(1),\quad f(1)\le kf(k)
\]

给\(U_q<2u-df(t)<2u\)。实际Greedy利润至少\(d[f(2)+(k-1)g(r)]>u\)，后一严格性由旧条件\(g(r)>2f(1)-f(2)\)支付。因此所列实际后续任一相邻对≥2u，全部冻结查询≤U_q<2u；此旧族不击破本桥。代码核的是这些已给公式的标量正性，不重证Punish/Greedy在全部离轨历史的真实性。

原PB报告共14字段：`old_family`为`round5/menu/pair_attack.md fixed published constants`，`scope`明确只核旧PB实际路径代数、没有新SPE认证，`parameters`为上述八个数；其余11字段完整原分数为：

| PB原字段 | 完整原值 |
|---|---|
| `unused_real_blocks` | `0` |
| `single_greedy_real_blocks_per_segment` | `1648` |
| `double_greedy_real_blocks_per_segment` | `412` |
| `first_three_payoff_u` | `180000000705/250000001750000003` |
| `root_frozen_query_max` | `36000000155296760144865550/50000000251236500306182500007419` |
| `first_pair_margin` | `9000000032120949952120597358621380/12500000112809125327782125308037250007419` |
| `all_position_frozen_query_upper` | `3272727281363647277090930/4545454559090954554545590909091` |
| `all_position_pair_lower` | `360000001410/250000001750000003` |
| `all_position_margin_lower` | `818181821613649996477361570181973850545520/1136363647727284130681931875000397754546022727273` |
| `strict_root_IC_margin_per_segment` | `17241792075873809327687186758861/1724137979310362532759105210349467793121068965540` |
| `greedy_profit_lower_minus_u` | `854060004787825005724855/500000004512375013111375012321750000297` |

`first_pair_margin`是2u减首query最大值；`all_position_margin_lower`是2u−U_q；`strict_root_IC_margin_per_segment`是上列Fill/Copy不等式余量，不是新全树最小slack；`greedy_profit_lower_minus_u`是所列Greedy保底差。所有正性是精确有理意义，不能把极小正差舍入为0。原报告顶层另有完整`candidate_status="OPEN; these old-family checks do not prove FROZEN-PAIR"`，以及上述两人数组与PB对象，共三顶层字段。

PB原先反的是首对≥2v_(r+1)(b)，不是本弱首对≥v_r(b)或FROZEN-PAIR。它的背景合法不保证是根SPE实际前缀；[最后D-singleton偏离障碍](../障碍/PB大背景的最后单例偏离--障碍.md)已排除原参数/目录精确实现该背景后接2475 regular的直接在轨迁移。这个后继障碍没有推翻PB子SPE及上述背景内代数，不能因“actual path”一词把本报告写成根实际全路径认证。

## 运行、证据与停止范围

原4570B代码只导入Fraction、Path、json，无模型/solver/随机/优化器依赖，**没有main guard**。顶层立即调用两份`two_player`和`pb_old_family`，正常assert后将完整JSON加换行写到脚本相邻`frozen_pair_old_families_audit.json`，再打印同一完整JSON。普通import也会执行并覆盖邻接报告，故本轮未导入或调用它。

原JSON无源hash、argv、环境或进程事件；全文读代码和报告可以恢复合同，不能据此伪造当年运行时间或成功进程。检索当前仓库/runtime没有找到这份同SHA原入口成功事件，本轮没有为补日志重跑。原入口/源函数/两人IC回放/PB公式函数/BI/LP/随机/大树调用均0。随附`check_saved.py`只核五源与21比较指纹、语法及已存报告字段/分数身份，没有重新求解两人策略或计算新PB域。

SHIFT、末位锚和UNPAID是可复用的精确数学；末位锚还说明两人输入阴性本来就不能诊断更早的未知premium。两个旧族通过不能证明一般桥，也不能宣称一般桥已假。弱半安全floor和首对安全付款的真正断口见[全树接续页](../资源/全树双重重置与终局代币共同付款的接续边界--资源.md)，其BG-NEW则已有后续明确反例，状态不能合并为一项OPEN。当前六人half依然不由这些局部付款闭合，五人另证也不回授这个全背景候选为真。
