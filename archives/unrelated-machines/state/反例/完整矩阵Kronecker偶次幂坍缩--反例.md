---
id: "unrelated-machines/actual-kronecker-even-power-collapse"
kind: "counterexample"
type_tag: "反例"
title: "完整矩阵Kronecker偶次幂坍缩"
status: "proved-with-stated-scope"
summary: "八机十任务种子OPT=3/2而完整偶次Kronecker幂OPT=1；未剪枝assignment LP则对任意非负矩阵精确相乘。"
legacy_ids:
  - "UM-ACTUAL-KRONECKER-NO-TO-YES-v1"
  - "UM-UNPRUNED-ASSIGNMENT-LP-KRONECKER-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/private_graft_and_resource_repetition.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/private_graft_and_resource_repetition.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/actual_kronecker_product_review.md"
---

# 完整矩阵Kronecker偶次幂坍缩

完整Kronecker积保留全部任务与机器元组，mixed selector/incidence任务也必须安排。以下8机10任务实例的真实最优值是3/2，全部偶次幂却精确为1；平方的100项全任务调度由统一初态及15件同时改派给出。一般乘法恒等式只针对未按阈值删长边的assignment LP，不能换成剪枝LST或CONFIG。


**证据口径。** 下文关于原作者、原研究者、既有独立重构、读后攻击、内审、代码实现及旧审计数量的叙述，均是所列冻结来源的历史记录。它们不表示本轮重新完成这些活动；本轮实际阅读、核对与新运行单列在文末。外审及新颖性不据这些记录升级。

## 7. 完整处理时间矩阵的平方也能把真实NO变成YES

本节是另一种操作：**所有机器对、所有任务对均保留的实际矩阵 Kronecker 积**，与[共享三维匹配复制](../障碍/私有需求组合与共享三维匹配复制--障碍.md)中的源三元组张量不同，也不是只乘菜单的 state/resource 层。冻结来源记载，原公屏seq260/264的boss7曾报告另一 10 机器、14 任务 parity half-selector 的实际平方使 3/2 降为一；本节未取得其完整冻结证明，不代为升级。冻结来源本节另给更小的 8 机器、10 任务实例及十五件显式交换，补成可直接核查的证书；不认领该反放大现象的首次发现或全球新颖性。

### 7.1 对象与精确身份

**ID/version：UM-ACTUAL-KRONECKER-NO-TO-YES-v1。** 基实例 P 的机器按顺序为

\[
S_{00},S_{01},S_{10},S_{11},R_{00},R_{01},R_{10},R_{11}.
\]

任务按顺序为 A₀、A₁，及按字典序排列的八个 B_gla，g,l,a∈F₂。A_g 仅在 S_g0、S_g1 上耗时一；B_gla 仅在 S_gl 上耗时 1/2、在 R_(a,l+ga) 上耗时一；其余边不可用。加法在 F₂ 中进行。

对任意 t≥1，P^[t] 的机器、任务是原对象的全部 t 元组；当且仅当每个坐标有限时该元组边有限，时间为各坐标时间之积。没有删除 selector×incidence 等 mixed 任务，也没有外加逻辑一致性。精确结论为

\[
\operatorname{OPT}(P)=3/2,
\qquad \operatorname{OPT}(P^{[2k]})=1\quad(k\ge1).
\tag{7}
\]

平方有 64 台机器、100 件不同任务、400 条有限边。下面的统一公式加十五件改派使每台机器恰有负载一。所有 k 的构造按明确输出规模收费，不声称关于二进制 k 的多项式输出。

**基实例。** 每组 selector 激活一个 S_gl；两个不同斜率的已选二点支持恰交一资源。若峰小于 3/2，每个已选根的两枚 incidence 都必须外送，于是交点会收到两枚 unit，矛盾。选两组标签均零，只把交点的一枚 incidence 留 private，即有完整峰 3/2 调度；所有未选 state 的 incidence 留原处，负载一。

### 7.2 平方的全任务公式与有限交换

写第二枚 incidence 为 B_hkc，令 b=l+ga、d=k+hc。先给全部任务如下实际初态：

| 原任务对 | 初始机器对 |
| --- | --- |
| (A_g,A_h) | (S_gh,S_hg) |
| (A_g,B_hkc) | (S_gh,R_cd) |
| (B_gla,A_h) | (R_ab,S_hg) |
| (B_gla,B_hkc)，l=h 且 k=g | (R_ab,R_cd) |
| 其余 (B_gla,B_hkc) | (S_gl,S_hk) |

四台被选 SS 各有一枚 unit AA，另十二台 SS 各有四枚 1/4；AB、BA 分别双射填满十六台 SR、十六台 RS，各负载一。在 RR 上，固定 a,c 后的映射为 (g,h)↦(h+ag,g+ch)，行列式为 1+ac。除 a=c=1 外均双射；a=c=1 时仅两个对角输出，各有两个原像。因此初态恰 (R₁₀,R₁₀)、(R₁₁,R₁₁) 负载二，(R₁₀,R₁₁)、(R₁₁,R₁₀) 负载零，其余全部一。

使用上面的零起点机器/任务序号，同时替换以下十五枚原任务的目的地；其余保持初态。不声明逐件执行这些交换时的中间容量。

| 任务对 | 旧机器对 | 新机器对 |
| --- | --- | --- |
| (0,7) | (1,7) | (0,2) |
| (2,1) | (4,2) | (0,3) |
| (2,6) | (0,2) | (4,2) |
| (2,7) | (0,2) | (4,2) |
| (2,8) | (0,3) | (4,3) |
| (3,9) | (0,3) | (6,3) |
| (4,7) | (5,7) | (1,7) |
| (5,7) | (7,7) | (1,7) |
| (6,1) | (4,3) | (2,3) |
| (6,8) | (2,3) | (4,3) |
| (7,9) | (2,3) | (7,6) |
| (8,7) | (3,2) | (5,7) |
| (9,1) | (6,3) | (3,2) |
| (9,7) | (3,2) | (6,7) |
| (9,9) | (6,6) | (6,3) |

每个新端均由原定义直接核资格。四台 (0,2)、(0,3)、(2,3)、(3,2) 各移出并移入 1/2；五台 (1,7)、(4,2)、(4,3)、(5,7)、(6,3) 各移出并移入一；两台 RR 对角各移出一，两个 RR 非对角各移入一。因此最终 64 台原机器恰负载一。任意 AA 任务在每个合法目的地都耗时一，给最优值下界一。这是固定有限完整证书证明，不依赖寻找证书时优化器的最优性状态。

将平方调度作 k 份坐标乘积，每个元组机器负载为其 k 个原负载之积，仍一；全部 10^(2k) 件任务各执行一次。全 selector 元组的时间一给相反下界，证明 (7)。

### 7.3 未剪枝 assignment LP 的可乘恒等式

**ID/version：UM-UNPRUNED-ASSIGNMENT-LP-KRONECKER-v1。** 对任意两份 m≥1、n≥0 的合法非负有理 UM 矩阵 P,Q，令 F 为只保任务覆盖与分数负载的 assignment-LP 最优值；**不按候选阈值删去长边**。则

\[
F(P\otimes Q)=F(P)F(Q).
\tag{8}
\]

原初分数分配作乘积即给 ≤。对偶可写成

\[
F(P)=\max_{y_i\ge0,\ \sum_i y_i=1}
\sum_j\min_{i:p_{ij}<\infty}y_i p_{ij}.
\]

取两侧最优 y,z 的乘积，有限资格集是笛卡尔积且因子非负，每个任务对的最小值也相乘；对所有任务对求和即给 ≥。没有使用 0·∞，只在有限边取最小值。每任务至少一条有限边保证 LP 可行，m≥1 使负载阈值非负；空任务或 F=0 同样由该原初/对偶证明覆盖。

本节基实例取 selector 各半分、每 incidence 各半 private/resource，全部行负载一。对偶给每个 S 权 1/6、每个 R 权 1/12；两枚 selector 各贡献 1/6，八枚 incidence 各贡献 1/12，总计一。因此 F(P)=1，平方及所有偶次幂也为一。恒等式是基本 LP 对偶推论；不能换成剪枝 LST 或配置 LP 的可乘性。

### 7.4 范围、实际证据与下一义务

Dependencies 为完整矩阵定义、§7.2 所有原任务的可核证书、非负有限和的乘积分解；(8) 另用有限 LP 强对偶。不使用复杂度假设或 NP 源。反例否定的是“任意真实 3/2-gap seed 经这个完整平方仍保有大于一 gap”的通用合同，不排 reduction-specific hard image、其它乘积、物理一致性或一般 near-two hardness。

冻结审查记载，原独立研究者先按精确对象另构造平方调度，随后读作者完整证明、证书与结构交换，见[实际矩阵平方审查](https://github.com/SOMEBODYJUN/co-work-anl/blob/68fad804ec5946cb296f77dc5b336308a66abf12/research/reviews/unrelated_machines/actual_kronecker_product_review.md)。原矩阵、两份不同分配、规范 Fraction 检查和冻结结果在审查中逐项列出。独立于搜索代码不自动等于独立数学审查；两种角色分别记录。限定范围证明完成；外审、全球新颖性及独立论文价值未认证，UM-TARGET-v1 仍 OPEN。真正的近二反面仍须保住源相关整数一致性，而非只保分数 LP 值。

## 本次核对、关系与接续

本次已读actual_kronecker_product_review，明确旧checker负索引别名、额外row漏检和primal未核均曾修复，随后v3再拒绝重复同端稀疏序列化；这些属于旧程序历史，不能回填为旧版已经正确。

本次另写并实际运行[独立结构见证核验](../../../../tools/evidence/private-tree/structural_witness_check.py)，按正文原资格重建64机100任务400有限端，逐个核全部15件旧/新端及最终100项调度，全部64行精确负载1；[新输出](../../../../tools/evidence/private-tree/structural_witness_check.json)保存全部100项分配。这不是优化器，也未声称运行通用证书输入验证器。基实例下界及所有偶次幂仍由正文一般论证承担。

[源三元组的pool/张量障碍](../障碍/私有需求组合与共享三维匹配复制--障碍.md)与此仅有失败机制的比较关系，不是同一操作或证明依赖。另[有界接线](../定理/有界重数克隆接线与共同循环坍缩--定理.md)的见证也真实坍缩，但改变资格图而非时间乘积。奇次幂、源专用hard image和附加一致性不在本结果否定范围。

## 完整矩阵审查的修复顺序与实际覆盖

专门审查源为source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/actual_kronecker_product_review.md，源ID c1ddd58e8cbc645b74b7。它只审原§7.1–7.4，原§1–6前缀保持不变，不能由本审查倒推此前源pool或graft证明又被重审。

原审者先按精确矩阵对象重建8机10任务种子及平方，找到另一份100项完整调度；随后才读作者证明、原证书和checker。统一初态与15件同时交换形成后又实际读后核对。两份不同分配的存在是两个具体证书，不代表其搜索过程构成一般算法；审查代码与独立重建数学也分别登记。旧公屏还曾报告另一10机14任务实例，本审查没有取得并认证那份旧证书，不认领反放大现象的首次发现。

| checker阶段 | 原审查确认的缺陷或修复 | 证据限度 |
|---|---|---|
| 初版 | 负编号可能借Python负索引别名，字典schema可能忽略额外row；只核dual却标成primal_dual | 前两项旧版接受是读代码所得语义判断。旧版实际变异在修复后中止，没有旧版已实测接受的运行证据。 |
| 修复后v2 | 增补索引/schema及实际primal核对；独立错误变异、既有output拒覆盖通过 | 只能说明修复后拒绝，不能回填为旧版本早已拒绝。v2仍允许同端重复序列化。 |
| 最终v3 | 总row数100，每row四个唯一且严格为int的端ID，另核范围；五类实际sparse变异拒绝 | 针对固定矩阵证书schema，不是一般任意UM矩阵输入验证器。 |

最终规范代码SHA256为8e95e8c4b00654b2e85efbd37e294837796755ce189e7e933e5200752abebbb3。原规范运行重建全部100×64矩阵的400条有限端，核两份证书、初态与15交换、种子全部1024份原分配，以及完整四次幂10000件任务、4096台机器负载全1；另把半半原初与显式对偶各自回算为1。原冻结结果和v2/v3变异分别位于同commit的evidence/runs/unrelated_machines/actual_kronecker_product_audit.json、actual_kronecker_checker_mutations_v2.json及actual_kronecker_checker_sparse_guard_v3.json。

原审查全文件绑定SHA256为6e0f4996e94e5873425d2f29d95be494a60cc5eaf1b62f6e46541df5d5c479da，实际覆盖仅其§7。作者Exact、两种证明、独立重构、逐阶段读后与checker异议原稿的完整hash对照在该冻结review中保留。本文的新结构核验仅承担上文明确的平方与共同循环有限范围，没有冒作重新执行旧种子穷举、四次幂或全部变异。
