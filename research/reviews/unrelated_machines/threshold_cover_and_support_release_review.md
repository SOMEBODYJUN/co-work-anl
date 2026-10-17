# 门槛覆盖、前缀整机负载与支撑释放的纠错复核

本复核明确撤回旧版“覆盖候选”段和旧接受结论：它把FPTAS覆盖换成固定前缀，错误声称前缀重量≤需求。公屏seq339给出实质异议，boss6的内部审查先从精确合同独立重构，再冻结修复代码攻击；boss3经seq347另行核认恢复方向。赞同和提交不替代以下推导。旧冻结输出未覆盖改写，旧公式审计也不再用来证明真实恢复。

## 1. 原错误、修复及合同身份

`UM-THRESHOLD-COVER-JOINT-SLOT-v1`的对象、量词、假设和输出界均未改变；改的是原错误算法与证明。

- 原前缀重量通常≥d，未必≤LP权重e。例T1、τ1/2、权(2/5,2/5,1/5)的最小覆盖为3/5，前缀却为4/5。
- 错误可无界放大：每个整数r≥1取5r组、一个共同sink，s=1/(10r)。各组强制宏1/2+s，私有固定顺序为1/5后跟3r+1件s；W=1/2+s、d=s。每组token成本s，总LP成本1/2；旧前缀却把每组1/5送出，sink负载r。每组送两件s给出真实OPT1，低于1则每组须送至少三件s，sink≥3/2，故OPT确1。
- 正确恢复直接送出**同一个**FPTAS覆盖X。共同资格使它可送流选sink，真实成本=e；home留量W−e≤τT。联合整数流与有序槽于是同时给home≤(1+τ)T、sink≤(1+η)(2−τ+δ)T。
- 原UB在存在大单件时忽略小件覆盖，不保证UB≤2e*；d10、权(6,4,100)给100对10。修复同时比较最小大单件与仅小于d项目的首次越阈值前缀。小件够则前缀<2d≤2e*；否则最小大单件本为最优。
- Z=ηUB/(2n)，缩放成本ceil(w/Z)，截断到floor(UB/Z)+n。每层保最大原精确覆盖与原任务见证，最优覆盖不被截掉；e≤e*+nZ≤(1+η)e*。0/1转移只读上一层，零需求直接空集。固定η为总位多项式，η作输入时显式依赖1/η。

未知OPT的one-sided搜索在此修复后有效。真实OPT调度使每个t≥OPT的测试接受；任何拒绝low都小于K*=QOPT。以整数high=QU和low=−1哨兵二分，high−low=1时high≤K*；不需要e(t)或所有低端接受点单调。高端U为合法调度总工作量，QU为整数；T0先按零端处理。成功保证与OPT≤T必接受证明分开；给定证书被程序拒绝不构成OPT拒绝。

## 2. 两路真实核验和软件范围

可复现命令均在仓库根运行，重跑stdout写scratch或新文件，不覆盖冻结JSON：

- `python3 tests/audits/unrelated_machines/threshold_cover_recovery.py`：21846个子集oracle比较，4个非法输入；大分母、空/零组、无sink、实际分数联合流、原任务恢复和错误前缀族。
- `python3 tests/audits/unrelated_machines/threshold_cover_recovery_independent.py`：seed61749381；38412个整数缩放覆盖、2400个非均匀有理覆盖（含大分母）、2399个合法共同见证，其中1477个分数见证、447个无sink；20个前缀错误族；2036个满足上侧全接受的非单调谓词。1个随机点因预算不满足在测试前丢弃，不记作合法样本或失败。独立按原处理时间逐任务、逐机器回算，并核较强局部槽收费界。

目标实现仅覆盖T>0时给定精确LP见证后的验证、FPTAS和实际舍入；通用LP求解器、零阈值外层与未知OPT端到端软件未实现。数学算法和这些软件范围分开。两个独立程序共享已审的Flow类，但覆盖oracle、样本制造与原负载回算独立于被测恢复核心；不把两次调用同一核心当双重证明。

冻结结果：`evidence/runs/unrelated_machines/threshold_cover_recovery_audit.json`、`threshold_cover_recovery_independent_audit.json`。原公式审计仍保留其真实有限范围。

## 3. C2前缀见证的第二处实质修复

旧`UM-C2-PREFIX-CONDITIONING-DEGREE-v1`见证有两件互补的3/2任务，完整B负载恒为3/2。旧程序只检查指定literal的0/1，不能支持所声称的整机负载差异。原存在性陈述可由替代见证保留：四件零时间A/B前缀，任务5在A/B均1并由第五bit控制，任务6零时间固定A，任务7仅C耗时2。两parity来源各16个真OPT2调度，实际≤4阶one-hot矩相同，前缀下完整B负载确为0与1。

独立审查未调用新规范audit。`c2_prefix_full_load_independent.py`检查13个实际端literal的全部1093个≤4阶子集（706相容、387互斥零项）、全部64个实际调度、M2的86维精确PSD/秩16、三台14维localizer的PSD/秩6,6,0和2142条one-hot乘子恒等式。前缀概率均1/16，完整条件负载为(1,0,2)与(0,1,2)。规范`c2_prefix_conditioning_degree.py`另按原矩阵回算，显式保留旧见证抵消的负控。

这只证明**指定来源分布**的条件负载不能由四阶表唯一识别；允许重求或重新耦合的算法不被排除。替换见证没有改存在性Claim的量词或定义域，但旧见证特有的Objects/代码/地图描述必须同步，不能假装原证明正确。

## 原支撑族修正

原 `lst_support_release_and_threshold_group.py` 的枚举输出实际为

`OPT=51/100 + 49m/(100(m+1)) = 1−49/(100(m+1))<1`，

而不是 `OPT=1`。因此旧族仍可反驳“锁定正支撑后残余小任务必可填入”的合同，但不能作为真实 `OPT=T=1` 的近二族。

独立重构的新 `UM-LST-SUPPORT-RELEASE-OPTIMAL-v1` 采用每块 `m` 核心机、一备用机、`m` 私有任务和一个单位锚任务；私有任务在其核心和备用机耗时 `1−1/m`，锚任务在全部本块机器耗时 `1`。LST 点把私有任务放核心、锚均匀分到核心，核心分数负载为1。真实最优值恰为1（锚任务下界及锚放备用机见证）。无零质量边激活时锚必落核心并与相应私有任务叠加，负载为 `2−1/m`；每块激活一条零边即可达到1。`r` 个独立块因此在至多 `k` 条零边预算下有精确前沿 `2−1/m`（`k<r`）和1（`k≥r`）。这只限制固定支撑加有限释放合同，不是一般算法困难性。

## 4. 同行撤回记录与本次修复关系

同行在4300c26正确登记seq339：固定前缀可能迁出4/5，而同组覆盖只收3/5；旧式(85)及旧搜索恢复都未被证明，Claim当时必须保持candidate。该撤回与本次第1节修复没有冲突：我们公开保留原fatal，换为同一覆盖实际输出并补齐UB/DP证明，再冻结独立攻击后才恢复声明范围状态。未把旧review或公式测试追认为正确。

## 5. 其他清点修复与限制

rank-jump抽象块例的第三端不能把任务和补成I/1：ΣA=diag(2/5,1)、Σc=8/5。现仅作为逐端投影条件不足的toy，明确不满足完整任务守恒；没有构造完整C2伪矩反例，不动真实有限支持闭合引理。

异质宏审计的宏数边界旧fixture用一件时间1的tiny，违反小边假设。替换为第一home五件强制1/5 tiny、一件单位宏可去两home；唯一OPT1把宏放第二home，第一home tiny总量1>统一半容量。这里是精确容量矛盾，没有调用LP求解器。`heterogeneous_macro_boundary_repair_audit.json`只核此修复，不声称重跑旧全部随机范围。

**判定：** 对本次冻结修复及限定范围，未发现仍成立的fatal objection。UM-TARGET-v1仍OPEN，一般结构生成与可求共同容量仍未闭合；外审/新颖性未认证。

## 6. 本次冻结哈希

独立脚本入库仅调整路径/输出，重新运行后冻结。审查自身不循环列hash。

| 文件 | SHA256 |
| --- | --- |
| `research/questions/unrelated_machines/barrier_escape_obligations.md` | `9c0007adaa87e158d9e0b22a09c66f244d95eecc15142b02cd69b87526df00e0` |
| `research/current/unrelated_machines/c2_prefix_conditioning_degree_boundary.md` | `1f7e495f1cdcb4747149ad5b28ffcc8372f5306b34320c09c5d6c5b61d44ff43` |
| `tests/audits/unrelated_machines/threshold_cover_recovery.py` | `a709d0903feaf19ba4412186a3242660fd03ea36603911cec7ec7cf7533427f4` |
| `tests/audits/unrelated_machines/threshold_cover_recovery_independent.py` | `432c22c5a235d2a8c5dde993f6a0f5c03f926de0771d2422c53ccabbc38a7a60` |
| `tests/audits/unrelated_machines/weighted_group_joint_slot.py` | `4cab1691aaef9c1265fd517d1cf5dbd2cb2f7e5b0757a0d88fcc2e9ae3905a4e` |
| `tests/audits/unrelated_machines/c2_prefix_conditioning_degree.py` | `e9ce6730e65c8924d619f42919b2d494a63096794573ebf1113eb32d64db1960` |
| `tests/audits/unrelated_machines/c2_prefix_full_load_independent.py` | `5777042a4192d908d251bc80b6967d41273701705a7ac59de18da72c1512c183` |
| `tests/audits/unrelated_machines/heterogeneous_macro_uniform_residual.py` | `34026b4a0e648258a20e72b4fa29d8fcccb10b24f5e1e66d75c2d8458915e8fc` |
