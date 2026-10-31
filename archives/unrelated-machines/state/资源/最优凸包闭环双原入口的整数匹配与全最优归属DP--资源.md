---
id: unrelated-machines/optimal-hull-closed-cycle-two-original-programs
kind: resource
type_tag: 资源
title: 最优凸包闭环双原入口的整数匹配与全最优归属DP
status: integrated-original-finite-audits
truth_status: existing-family-proof-with-exact-finite-implementation-evidence
source_refs:
  - clean:4b417f3b0c8858c5c2ba
  - clean:7c60cdc8dd34a338c6a6
related_objects:
  - unrelated-machines/optimal-hull-closed-cycle-escape-threshold-20261031
  - unrelated-machines/optimal-hull-long-chain-closed-cycle-finite-review
---

本资源完整吸收两份已认领原程序的数学对象、独有匹配方法与有限域；既有 `UM-OPT-HULL-CLOSED-CYCLE-WEAK-LOCAL-GAP-v1` 的一般结论不另授新定理身份。它们不导入规范构造、槽核心或开链程序，均只有标准库依赖。源码、两最优分量、完整处理时间、冻结结果及本次输入核对在 [证据目录]$../../tools/evidence/um-next-source-programs-primary/README.md$。原大枚举本批新运行 0；复用同 SHA 完整冻结运行，新增数据检查不冒充重跑。

| 主源 | 实际表示与完整入口 | 冻结源码 SHA256 |
|---|---|---|
| `4b417f3b0c8858c5c2ba` | `optimal_hull_closed_cycle_independent.py`；6302B；`audit` 五例和 `tie_audit` 两例 | `ac42e3dce6b3acf0fa6512de939b186e17ea0e1b2e01808f2e9c09cbe761eeaa` |
| `7c60cdc8dd34a338c6a6` | `optimal_hull_closed_cycle_reviewer.py`；6183B；`run` 四例、`matching_opt` 及全部根平局循环 | `aa6ad02c4c40ff976b7978332137793a4ca69906924e5160fc0f14521bb76021` |

## 共同完整输入与结论所依赖的证明

参数是整数 $k\ge3,d\ge1$。置 $a=b=1-1/k,\ \delta=(k-1)/k^2,\ c=1/k^2,\ \beta=1/k,D=d+k-1$。一台 root $r$，$k$ 条长度 $d$ 的 tiny 环与一条长度 $D$ 的 macro 环，只在 $r$ 相交。环 $q$ 有 home $v_{q,1},\ldots,v_{q,h}$、rootjob $g_q$ 及原任务 $e_{q,1},\ldots,e_{q,h}$。每件任务恰两个有限正端点，其余为无穷：

| 原任务 | 端点0及处理时间 | 端点1及处理时间 |
|---|---|---|
| 特殊 $g_0$ | $r,\delta+c/4$ | $v_{0,1},1$ |
| 普通 $g_q,1\le q<k$ | $r,\delta$ | $v_{q,1},1$ |
| macro $g_k$ | $r,b$ | $v_{k,1},1$ |
| 非尾 $e_{q,l}$ | $v_{q,l},a$ | $v_{q,l+1},1$ |
| 特殊尾 $e_{0,d}$ | $v_{0,d},a$ | $r,c/2$ |
| 其余尾 | 最后 home，$a$ | $r,c$ |

计数 $m=(k+1)d+k,n=m+k=(k+1)d+2k$。激活环意为该环所有 bit 取1，否则全0。$S_0$ 激活全部 tiny，$S_1$ 只激活 macro。两调度 root 负载分别 $1-c/2$ 与 $b+5c/4\le1$，home 负载为 $1$ 或 $a$。若最大负载小于1，所有 $g$ 不能到第二端，则 root 已有 $2b+c/4>1$，矛盾。所以真实 OPT=1，$x=\beta S_0+(1-\beta)S_1$ 是完整最优调度凸包点，每条有限边有正质量；不是仅通过 assignment-LP 或边际测试推测配置可行。

ST 槽图按机器处理时间非增、同值按本程序任务顺序排列。任务质量区间 $[u,v]$ 与单位槽 $[s,s+1]$ 仅在 $\max(u,s)<\min(v,s+1)$ 时相连，接触端点不算边。每 home 的 incoming 与 own 质量相加1，恰一个槽；root 总质量 $k+1$，恰 $k+1$ 槽，全图槽数恰 $n$。root 顺序严格分组 $g_k>g_0>普通g>普通tail>特殊tail$。$g_k$ 区间 $[0,\beta]$，$g_0$ 区间 $[\beta,1]$，都只能去槽0。特殊尾最后，区间 $[k+1-\beta,k+1]$，只能去槽 $k$。普通 tiny 的第 $r=1,\ldots,k-1$ 个可注入 root 槽 $r$。

因此只激活特殊环的分配 $\sigma$ 可实现：macro 占 root0，普通 tiny 依序占 root1至$k-1$，特殊尾占 root$k$，激活环 incoming 占每 home，其他环 own 占 home。所有平局组内顺序均适用。任一 cover matching 占满所有槽；每个 home 得恰一任务。以 $z_0,z_1,\ldots,z_h$ 记一个环的第二端 bit，计数 $z_{l-1}+1-z_l=1$ 迫全相等，即在**槽匹配输出**中每环全开或全关。

令 $W_0$ 是所有任务端点0的实际总成本，仅作为参照，不声称它槽可行。特殊、普通 tiny、macro 的整环增量依次为
\[
 c_0=d/k-\delta+c/4>0,\qquad c_t=d/k+c-\delta=c_0+3c/4,\qquad c_b=D/k+c-b=c_t+\delta.
\]
至少特殊或 macro 环开启，所有增量正且特殊严格最小，故所有最小成本 cover matching 诱导同一机器分配 $\sigma$。这一步没有证明槽级匹配唯一，也不需要它。坏 root 峰值
\[
 B=b+(k-1)\delta+c/2=2-3/k+3/(2k^2)>1.
\]

现在允许任意合法实际重分配，离开原槽限制。定义 $H=\{j:\tau(j)\ne\sigma(j)\}$，$V(H)$ 为 changed jobs 全部新旧机器端点并集。若 $C_{\max}(\tau)\le B$，home 负载 $z_{l-1}+(1-z_l)a$ 与 $1+a>B$ 迫 $z_0\le\cdots\le z_h$，但可有部分后缀，不能把槽全环约束偷用于实际调度。若没有新的原留 root 的 $g$ 离根：特殊 $g_0$ 仍离根则整环保持；若它返回 root，原尾回 home 至多减 $c/2$，root 净增至少 $\delta-c/4>0$；其他环任一非空后缀将尾送 root 严格增 $c$。所以除 $\sigma$ 自身均超 $B$。任何非平凡弱最大负载改善须新激活一个整环，故 $|H|\ge d+1,|V(H)|\ge d+1$。再激活普通 tiny1 同时达到两界，root 新峰值 $R=B-\delta+c=2-4/k+7/(2k^2)>1$，严格下降。

因 $B\to2$，先固定足够大 $k$，后增 $d$，可排除任意固定预算；固定 $k$ 时 $d+1=(m+1)/(k+1)$，亦排除该初始化下 $o(m)$ 支持的弱最大负载第一步。稀疏对象数 $O(kd+k)$，有限数的分母整除 $4k^2$，位长 $O(\log k)$；按显式输出总长构造为多项式。源码的 $2^n$ 穷举和子集DP是有限审计，不是上述构造复杂度或一般调度算法。

## 整数实现的独有核验义务

`4b417…` 用整数 $4k^2$ 缩放：own 为 $4k(k-1)$，普通 root tiny 为 $4(k-1)$，特殊加1；特殊 tail 为2，其他 tail 为4，第二端 home 为 $4k^2$。任务采用**每环 rootjob 后紧接本环 ownjobs**的交错顺序。`slots` 把 $S_0,S_1$ 的质量存为单位 $1/k$ 的整数1与$k-1$，用严格区间交长建立每件任务邻槽，不靠一般证明指定答案。

`slot_realizes` 对给定完整 owner bits 从每任务出发作 BFS 交替路，边限制在该任务实际目标机器，找到空槽再回溯增广；匹配全部任务才返回真。`audit` 枚举全部 $2^n$ 带标号 owner bits，逐件加负载取真实 OPT，对区别于 bad 且峰值≤B 的全部状态分别最小化 changed jobs 与端点并集。槽输出过滤先检查每非root恰1任务、root恰$k+1$，再真实增广匹配；因槽总数=n，此必要过滤不会漏输出。总处理成本为全机负载之和，保存所有最优 owner bits，断言列表只有 bad。它没有统计槽注入数。

`tie_audit` 对 root 中 $k-1$ 个普通 tiny 与 $k$ 个普通 tail 穷举 $(k-1)!k!$ 次序，分别12和144。每个 tie 图测试所有**整环激活**的 $2^{k+1}$ 状态，检查 bad 可匹配且仍唯一最低成本 owner；没有在每个 tie 图重枚举所有 $2^n$ 任意 bits。默认次序的 `audit` 才覆盖完整实际状态。一般任意tie结论来自前述满槽证明，不能由这段较小tie循环单独推得。

## Fraction reviewer 的独有全最优归属 DP

`7c60…` 用 Fraction 直接生成 times 与端点0质量 $x_j$，任务编号为**所有 rootjobs 在前，再各环 ownjobs**，区别于整数脚本。按该编号构图后，`matching_opt` 将任务按邻槽数量排序，缓存状态 `(q,used_slot_mask)`：在尚未用的每个邻槽尝试，返回最小剩余处理成本，以及该最小值下全部机器归属后缀的 `frozenset`。遇到同成本分支取归属向量集合并，最后逆排序复原原任务编号。此法直接在真实槽图上求所有最优 owner，不使用“整环全开”的化简，也不会把槽层的多个注入错误算成多个 owner。记录的 `matching_DP_states` 是缓存状态总数，不是机器数、匹配数或路径搜索状态数。

`run` 独立穷举全部合法bits求 OPT、全部 other-B-feasible、最少改件/参与机，并显式把普通 tiny1 全激活检验同一个严格改善见证同时达两界。其默认 `do_matching=True` 另跑上述DP并要求所有最优 owner 集合为 bad。主入口四例缺少整数程序的 `(4,2)`；两者不可套同一总数。reviewer 的每个 tie 图均重跑完整 matching DP，不局限整环状态，因而其 tie范围比整数脚本直接验证的范围更大。

## 真实冻结结果及两个层次的数量

旧聚合 `optimal_hull_closed_cycle_audit.json` SHA `5cd6127e5038ea25f2b19c2cb0b2b5d281dde127a91fad5e5ab2d5c3a77ec4eb` 的 `sha256` 字段精确绑定两主源。复用其中完整 `independent_integer_owner_enumeration` 与 `independent_subset_DP`，保原 Python3.12.14 历史身份；本次没有给旧事件补造新 exit code 或时间。

| $k,d$ | $m,n$ | 完整 owner 数 | 非bad且≤B | 槽可行 owner 数（整数） | 最小支持 jobs/machines | B | reviewer 最小成本 / DP states |
|---|---|---:|---:|---:|---|---|---|
| 3,1 | 7,10 | 1024 | 42 | 6 | 2/2 | 7/6 | 11/2 / 98 |
| 3,2 | 11,14 | 16384 | 84 | 6 | 3/3 | 7/6 | 17/2 / 269 |
| 4,1 | 9,13 | 8192 | 195 | 8 | 2/2 | 43/32 | 243/32 / 171 |
| 4,2 | 14,18 | 262144 | 466 | 8 | 3/3 | 43/32 | 未在reviewer主入口运行 |
| 5,1 | 11,16 | 65536 | 883 | 10 | 2/2 | 73/50 | 483/50 / 271 |

整数总353280，reviewer总91136；各自所有最小成本 owner 数均1。两路各自 tie12+144=156，不相加成312个不同输入，也不扩到任意k,d。

`k3d1` 原输入为7机器、10件、20有限边，certificate 完整给两分量、x、坏注入、锐重分配及5个状态的4次单任务迁移。本次独立数据检查对原输入、两份 certificate、32组显式构造输入和源 SHA 实核，输出完整各源码编号顺序、每件两个端点、所有状态、x、负载、槽邻边、root区间和逆尾路径；没有重新计算旧全枚举计数。

## 与逃逸程序、开链及审查先验的关系

两主源均不实现 bottleneck Dijkstra 或最小路径峰值oracle。聚合中 `normative`、`independent_minimax_path` 来自其他比较源，不借其计数给本次两个入口增加运行。既有闭环单任务结论是到最优调度**集合**的最小峰值 $B+c$：任何第一步为 inactive尾回 root（峰值B+c）、进入home（至少1+a>B+c），或特殊根回root（B+δ+c/4>B+c）；逆尾依次激活其余tiny到S0达上界。其c=1/k²趋0，故不排除微小暂时增载修复。开链有空sink、最少参与机d+2并有Cmax不增单任务路径，不能把闭环d+1及无法中性起步移给开链。

原 reviewer 的 statement-first 身份来自已冻结审查叙述：先精确声明/旧§10比较、独立重构槽和全部owner，之后才读冻结§11；原盲审的未扰动公式 $2-3/k+2/k^2$ 后被当前 $B$ 替代。本次是已读证明和代码后的清洗自查，不追加“盲审”认证。外审、全球新颖性及一般UM算法/硬度均未完成。
