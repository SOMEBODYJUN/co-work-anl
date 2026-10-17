# 共同资格私有组联合流的独立重构与冻结攻击

## 覆盖对象、顺序与审查结论

本审查覆盖 `UM-HALL-GROUP-JOINT-FLOW-v1` 和 `UM-HALL-GROUP-PROMISE-APPROX-v1`。由 boss3 内部研究者完成，不登记独立 Work 身份，不单独提交或推送。实际顺序为：先只收到精确输入合同和待证界，自行重构联合流及收费证明；发回重构后才读取 scratch 正文/源码；再审正式正文、严格解析器和未知 OPT 接口，并用自己的原矩阵 oracle 攻击最终实现。

已审正式正文 `research/current/unrelated_machines/hall_group_joint_flow.md` 的初次 hash 是 `cca2d434ea7809af2e55acbad38f68325edf8c1c4a8635dd52be9a5136f39410`；其后只收口了域外 ValueError 与第二独立报告链接，已逐项复核的正文 hash 为 `17db693ddeab9604fea9da6f0dc3ac584a8036cf465b3148c826c7e29b3f7411`。

最终规范源码 `tests/audits/unrelated_machines/hall_group_joint_flow.py` 的 SHA256 为 `ebcf08cbc82b841b86ab5c567d1abad79de0cf4b501bcffc24172fba3b94e46e`。两份独立审计对该字节版本重跑通过。

在声明的结构及参数范围内，没有发现仍成立的致命数学异议。此为内部审查，不是外审、新颖性认证或一般 UM-TARGET-v1 的突破。

## 独立重构的承重证明

令 `r=q(2+δ)/(q+1)`、`g=2-r`。独立得到的网络为 source→macro→home-in→home-out→eligible sink→target，macro 与 home 容量一，每 sink 接 q 组。全覆盖整数流同时决定宏任务的不同 home 和每个 occupied home 的一个共同资格接收机。

真实 T 调度中，occupied home 的宏负载严格大于 T/2，私有任务留量严格小于 T/2，因而该组真实出口体积严格大于 `W_h-T/2≥T/q`。任意 occupied 子集 A 只可流向 N(A)，按共同体积计算有 `|A|T/q<|N(A)|T`。故这些 occupied homes 满足 q-copy Hall；把其接收匹配与真实宏匹配拼接即给完整网络流。代码用容量 q，不实际展开 q 个顶点。

独立构造最初按实际宏时间撤离到 home 总负载 rT；正文统一留私有负载 τT 的版本更保守且正确。最后一件撤离前的不足小于目标撤离量，最后一件至多 δT，因此每组出口至多 `(1-τ+δ)T`，每 sink 至多 q 组；`1+τ=q(1-τ+δ)=r` 同时控制所有 home 和 sink。逐件输出无复制、无丢任务，不存在免费共同见证 oracle。

## 未知 OPT 承诺版

记真实最优值 O。δ>0 时用有限宏边值排序二分出联合流可全覆盖的最小瓶颈 B；无宏取0。真实 O 调度的相同 Hall 证明给 B≤O。其余两项由 promise 给出，所以

`t=max(Wmax,wmax/δ,B)≤O`。

因此全部有限宏边 `p>O/2≥t/2`，组下界 `W_h≥(1/2+1/q)O≥(1/2+1/q)t`；另两项由 t 定义给出 W_h≤t 和 w_j≤δt。旧阈值构造在 t 上合法且成功，输出≤rt≤rO。有限边值个数在显式输入规模内；只对随边增加单调的网络二分，不假定完整阈值合同单调，也不使用连续精度 oracle。

δ=0 的 promise 仅允许 O=0：若 O>0，合法输入必有 home；全部私有 w=0 与每个 home 的正组下界矛盾。逐任务零边检查覆盖该情况。t=0、空任务、空 macro、空 Z/资格（但至少一实际机器）均已检查。

promise 涉及所有有限宏边，含未使用边；不能偷偷改成仅最优调度所用边。关于 O 的承诺无需可判定，代码对域外可报 ValueError；它不声称识别全部 promise 输入。

## 总位复杂度和实现攻击

每条 source→macro 容量一，整数增广至多 |B| 次，每次 BFS 扫描显式网络。sink 容量 `min(q,|B|)` 的编码有多项式位长，q 二进制数值很大不增加循环数。r、τ、t 及真实前缀和用精确有理数，分母乘积位数受输入各分母位数和控制；前缀每件最多访问一次。B 的有限候选排序及对数次满流调用仍是总位多项式。

源码的分层节点标签、反向残量更新、home 拆点及整数流恢复均已攻击，未发现重复 home 或错误接收机恢复。旧稿 T0 条件和 float/bool 解析问题已修复：W 上下界及 max-item 条件统一验证 T0；至少一机器；输入只接受 int/Fraction/精确有理字符串，拒绝 float/bool。非法域与可靠 FAIL 明确区分。

一个记号小修已反馈主研究者：输出位长写 `O(n log(m+1))` 可显式覆盖 m=1，而不是在该端点照字面使用 `O(n log m)`；此不影响算法或总位多项式结论。

## 独立有限证据及其实际边界

第一份独立代码 `tests/audits/unrelated_machines/hall_group_joint_flow_independent.py` 的 SHA256 为 `fe1fd9f5f0ef1c83dd2681053fb0189070a1e846f1ce5374314a88340e0d296d`。它只调用规范 solve，不调用其 flow、矩阵构造、可行性或 OPT oracle。另行构造完整原逐任务矩阵，阈值 DFS 判断真实 OPT≤T，再逐件读取输出验证合法性和全部机器负载。Python3.12.14、Fraction/int、随机段 seed230782。

最终结果：8123 个合同内调用，其中3688个真实 T 可行；4066次成功、4057次拒绝；所有 T 可行输入成功，全部成功输出满足声明负载。另7个明确非法输入全部拒绝。枚举主要覆盖 q2/3/4、1或2 homes、2 sinks、0至2宏任务的共同资格和宏时间；另有150个固定seed三home三sink样例以及零值、巨大二进制q、字符串和非法域 fixtures。没有枚举任意规模。

第二份独立代码 `tests/audits/unrelated_machines/hall_group_opt_promise_independent.py` 的 SHA256 为 `2d684e9b61f052568ba8b82cc6cceee0697eaebc891c9da7acf5d00836ce7cdf`。它从原矩阵每机器子集和候选阈值加逐任务 DFS 求真实 OPT，以小规模 macro/home/sink 联合枚举独立求 B，只调用被审 solve_promise 输出。Python3.12.14、Fraction/int、seed778791。301个输入中122个满足真实 OPT 处的 promise，122次均成功；另合法 δ0 零例通过。它没有重用规范 flow 或 OPT 核。

其中一个有效 promise 例有严格 t<OPT：q3、δ1/3，两 homes 各6件1/6私有任务、共同一个 sink，各唯一宏时间3/5。真实 OPT=11/10，而 t=1。每home留3件时 home11/10、sink1；若 makespan<11/10，则每home最多留2件，sink至少8件、负载4/3，矛盾。该例排除了测试只是隐含使用 t=OPT 的解释。

两份脚本支持从参数指定候选源码路径；报告记录实际源码 hash、脚本 hash、Python版本、参数范围和 seed。最终独立重跑的 scratch 报告为 `hall_group_joint_flow_final_independent.json` 与 `hall_group_opt_promise_final_independent.json`；正式冻结记录沿正文链接。有限核验不是一般证明。

## 可复用机制、范围和仍未解决内容

可复用的桥梁是：occupied 组必付的最低真实出口体积→整数接收槽→一个流共同选 macro/home/receiver→实际前缀平衡两侧负载。组共同资格、机器无关私有体积、唯一 home、组总量下界和 max-item 均为承重假设。严格 Hall 号不能逐 sink 免费把 q 降成 q−1；正文已给真实 T 可行的三home两sink反例。

固定 q、δ 留正余量时，本结构类确有统一低于2的实际调度算法。q 可增长时改善可趋零；一般不相关矩阵也未被转入本合同。Truth 的限域证明、Value 的桥梁机制、Novelty、外审、一般 Ambition 分别保持记录，UM-TARGET-v1 仍未解决。

## 最终记号修正与规范运行接线

仅将正文输出位长改为`O(n log(m+1))`后，最终正文SHA256为`10aabd8e9cc0eccf10974f94e23633f6d1034313348a69ceac003bb876af5b2b`；其余数学及源码不变，boss已核单行差异。该记号修正正是独立审查建议，无新增证明义务。

规范原矩阵审计的三个有限域分别4448、228、10122个对象，合计14798，含3991个满足关于真实OPT的承诺对象；另有2079个精确公式点和9组导出的实际输入/分配。这与两份独立审计的范围分别登记，不累加成互不重复样本数或一般证据强度。规范报告保存Python版本、源码hash、实际运行命令、参数、seed不适用与未覆盖范围。

在仓库根可重跑（输出到新的scratch记录，勿覆盖冻结报告）：

```sh
python3 tests/audits/unrelated_machines/hall_group_joint_flow.py
python3 tests/audits/unrelated_machines/hall_group_joint_flow_independent.py
python3 tests/audits/unrelated_machines/hall_group_opt_promise_independent.py
```

例子input/certificate由规范`--export-dir`的九份实际导出按输入/输出拆开登记，字段值未作数学改写。新源码进入本阶段前已在库路径实际重跑，三份报告均匹配最终规范源码hash。ST1993仅作为沿用的调度/匹配背景来源登记，本正面接口由自足Hall/整数流/前缀推导，不将新结论归于该文。
