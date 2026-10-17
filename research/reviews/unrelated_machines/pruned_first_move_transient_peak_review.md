# 剪枝首步分段锐界的独立重构与冻结攻击

## 1. 审查身份、冻结对象和结论

主审为 boss9 内部 `general_builder`；另一内部研究者 `reconfiguration` 独立重构同一计数链与两支锐例，并在读取冻结稿前提出 C=T 零步及 B<C 起点不在图内两项边界异议，修复后完成全文攻击。两人均不登记为独立 Work，不推送、不发公屏。先仅收到精确 Claim，独立重构计数证明和两支锐环，向 boss 回报后才读取冻结全文与规范代码。独立程序不导入规范实现。

实际读取并核对的冻结对象：

- `research/current/unrelated_machines/pruned_first_move_and_transient_peak.md`，SHA256 `ae6be3522e64e4842e67ac8ababb01995a50dd70fc683f8e914353d12f022718`。
- `tests/audits/unrelated_machines/pruned_first_move_transient_peak.py`，SHA256 `8fe6bf4ad206f0af7e03b35fbc3a4994f9851e257dcf82bcf2149a489ef2b651`。

结论：冻结稿两个声明范围的证明通过本次独立重构和攻击，未发现仍成立的实质异议。它们是首步上界与任意固定批量的参数锐初态能垒，不是一般全程重配置上界，也不是 UM-TARGET-v1 算法。新颖性、外审及独立论文价值未认证。

## 2. 在读取全文前完成的独立重构

令 D 为 owner 不同的任务、f 为同 owner 固定负载、A 为源负载、B 为目标负载，故 f_i+A_i≤C，f_i+B_i≤T，源单件≤T。若每条直接目标迁移都超 U=max(2T,C+T/2)，其目的单件 b 都严格大于 T/2，因此每个目的机至多有一件 D 入任务。设所有目的机组成 S，则 |D|=|S|。任何 i∈S 若 D 出任务至多一件，源单件≤T 且 f_i+b≤T 给该步负载≤2T≤U，矛盾。因此 S 内每机至少两个 D 出任务，计数给 |D|≥2|S|，矛盾。

低支锐例独立重构为 m=k+1 环，每机固定 d=C−T 和一件源长 T、后继长 2T−C 的任务；高支为每机两件源长 C/2、后继长 T/2 的任务。≤k 非空改变必留一个收到而未迁出的边界机器；其负载分别至少 2T 或 C+T/2。依次走一圈或两圈直接目标迁移，达到同一峰。两支 OPT 的独立证明分别可用最短时间总和 mT 的平均下界，目标 τ 达到。

因此冻结全文不是先给证明、再由审查者重复赞同的顺序。

## 3. 冻结稿的重点攻击

### C=T、指定目标与孤立图

冻结稿明确把路径目标写成另一指定 τ。在 C=T 时 σ 本身已经最优，不能声称“到最优集合必须峰 U”；这一潜在漏洞已被正文末段明确排除。低支 C=T 中固定任务可为零且只有一个可用端，因此不会产生免费改变 owner 的绕路。任何非平凡变化都涉及环任务，固定批量下界仍成立。

状态图的孤立点声明限制为 C≤B<U：σ 在图内，所有不同且≤k改变的邻点载≥U>B。B<C 时起点不在图内，正文没有误称孤立。B=U 时有给出的单件路径，不属于孤立声明范围。允许倒退、重复任务和任意绕路也绕不开第一个非空批次，所以第一批下界足以推出 minimax 下界。

### 原矩阵中 p>T 的边与 FAIL

NO_T_SCHEDULE 的结论针对完整原 P，而非仅针对剪枝矩阵。这个推论有效：任何 T 可行调度都自动只用 p≤T 的端点，因此全枚举 E_T 的首步已经包含存在性证明所需的某条目标迁移。σmax>T 时，假定 OPT≤T 自动给 τ≠σ；不用免费求 τ。MOVE 是允许成功的广义分支，不能反推出 OPT≤T，正文保持了该单向性。

规范代码确实枚举原矩阵全部不同目的机并保留 p_dest≤T，不固定给定正分数支撑；候选集合为空时返回 NO 也符合证明。其失败证书可以由重新运行同一有限枚举和核对计数定理验证；没有要求某特定 LP 对偶。

### 锐值、路径和模型边界

低支 d≥0，b∈[T/2,T]，最短时间总和恰 mT；高支 a∈(3T/4,T]、b=T/2，最短时间总和也恰 mT。两支均有全部有限边≤T、任务支持≤2，τ 达到 T。第二圈峰 a+T≤2T≤U；固定 k 的 m=k+1 使任何≤k改变不能覆盖全部源机。低支第一圈同样可逐件回算至 U。

T=0 的首步定理可直接由全部源/目标时间为零处理；sharp family 要求 T>0，未借零尺度声称严格能垒。空任务和唯一 owner 不可能满足 τ≠σ 时，存在性前提为空；选择器 DONE/NO 分支分别正确。非负性和源剪枝是计数定理的承重假设，代码都核对。大有理分母不引起按数值枚举。

### 总位复杂度与不允许的推论

实际选择器最多 mn 个候选，每候选只改两个负载并比较 m 台机器；有理和、比较、输出总位长均多项式。锐族大小按显式输出 m=k+1 计；没有把二进制 k 的 O(k) 输出声称成 poly(log k)。审计的指数状态枚举独立于生产选择器。

新首步的当前负载可能超过 2T，所以该定理不能无证明反复调用；正文确实没有这样做。只给 τ 的路径也不能变成求 τ 的算法。冻结稿对这两个常见误用均明确保留开放。

## 4. 独立精确代码与实际核验范围

`tests/audits/unrelated_machines/pruned_first_move_independent.py` SHA256：`c1290ef3d0702868c227b3a94b6aea9c71122b684db7a44a189f49073b7c5c3b`。

该程序完全不导入规范代码，从原矩阵逐件构造每个合法分配并计算真实负载，分别计算：

1. 非空≤k 同步首批的最小新值；
2. 完整单件状态图的 minimax 路径；
3. 完整≤k件状态图的 minimax 路径，允许回搬和非单调绕路；
4. 显式每件恰搬一次的直接目标路径。

实际核验为 k=1,...,4，C/T 取 1、6/5、3/2、7/4、2（交界两支分别测），并加交界两侧的 127 位分母；共26个锐族参数，全部4332个合法分配状态，最大单族1024状态。独立真实 OPT、首批值、两种 minimax 与显式路径均精确相符。

一般首步有限穷举：两机、n=0,...,3、每矩阵元∈{0,1/2,1,∞}，全部3616个合法矩阵，36064对合法有序(σ,τ)，其中2362对目标零负载；另核空输入和3类非法合同。只按 Fraction/整数计算。独立结果文件 SHA256：`65ef5060d3582894bb8961af6a9b0a58e72758208adbb16deddf3226dd32d1f5`。

另有显式导入被测规范选择器的集成审计 `tests/audits/unrelated_machines/pruned_first_move_full_input.py`，其原矩阵 OPT oracle独立全枚举，不能与上述不导入的独立数学审计混同。它穷举两机 n=0,...,2、处理时间∈{0,1/2,1,3/2,2,∞}，共1261个原矩阵（1020个含非剪枝边）、1333个剪枝初调度，得到1117个DONE、162个MOVE、54个NO；所有 NO 的完整原矩阵真实 OPT 均大于 T。代码 SHA256 `e65a83ccd9c4ca238a196f14cd37a7ed8fac9734bc969a0d3efb886ab4e6f3c7`，结果 SHA256 `75fbe282bbc02b2c32aa4b15b82cc22dabf93b376f01e3e33ccabcf3196a9e02`。

规范位置的复现命令（结果写 clone 外，不覆盖冻结证据）：

```text
python3 tests/audits/unrelated_machines/pruned_first_move_transient_peak.py > /workspace/scratch/pruned_first_move_main.json
python3 tests/audits/unrelated_machines/pruned_first_move_independent.py > /workspace/scratch/pruned_first_move_independent.json
python3 tests/audits/unrelated_machines/pruned_first_move_full_input.py tests/audits/unrelated_machines/pruned_first_move_transient_peak.py > /workspace/scratch/pruned_first_move_full_input.json
```

各原始结果的完整 JSON、实际命令、参数与 hash 汇总在 `evidence/runs/unrelated_machines/pruned_first_move_transient_peak_audit.json`。主研究者已重读证明及两个独立重构，并在规范位置亲自复现三份程序；补充探索日志不作为新增一般结论。

上述有限实验只核验所列模型、参数和程序实现，不替代第2节的一般证明，不证明一般全程 5T/2，也不提供未知 τ 的近似算法。
