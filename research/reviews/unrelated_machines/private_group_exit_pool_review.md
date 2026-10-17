# 宏任务退出与完整接收池的独立重构及冻结攻击

## 冻结对象与实际顺序

被审基线为main `00f181f0b3767047edd014d8bd60061e56f2f178` 加本阶段改动。被审正文 `research/current/unrelated_machines/shared_sink_joint_macro_assignment.md` 的SHA256为 `8aec1196d16fccdd5dd661d1ebfebd1f1c211d256da021aa02f433304424ef2c`；新范围仅§8–10及其所依赖的§2–5。旧 `UM-SHARED-SINK-JOINT-MACRO-v1` 的身份和旧审查未被替换。

内部子研究者 `pool_statement_review` 先只收到两个精确输入/输出合同，在没有读正文或实现时给出独立重构：按全局绝对sink预算向下舍入的私有任务DP，加允许macro退出的共同匹配；完整pool用`S=Σ1/a_z`归一化，再按实际当前负载恢复。收到其独立推导后，才让其读上述冻结正文；它追溯cover证明与位复杂度，未读取规范实现。独立floor重构是**未实现的替代推导**，不把它算成生产实现。

另一内部子研究者 `pool_claim_attack` 在首次工具调用已打开旧正文与新实现，然后完成独立推导及实现攻击；因此不称其为完全盲审。它后来核对同一冻结正文逐行适用条件。boss复核双方重构、实际代码和两份可复现精确核验。子研究者不登记独立Work，不自行提交或对外发言；审查不是票决。

## 身份、费用和所有机器同时的负载

1. §8匹配左右各`b+h`点：b个真实macro、h个dummy；h个home、b个exit。若k个macro留home，则b−k个macro占exit、h−k个dummy占空home、余k个dummy占余exit。每个home的私有组选择一次，每个macro的真实exit成本也只计一次；强制私有exit成本在匹配外加一次。
2. cover近似只放大相应可选私有撤离成本，macro退出和强制成本不放大。任意原T调度给一个全局匹配见证，最小成本匹配因而不超过同一个`(1+η)T`预算，不按home数量付误差。
3. pool下包络给任何真实T调度`Σc_j≤TΣ1/a_z`，因此虚拟single-sink的T见证真实存在。此步骤不假定免费取得原调度；仅用于one-sided正确性证明。
4. 恢复使用上包络：若所有pool当前负载均大于`ρ(1+η)T`，已分配work便严格大于全部退出work预算。故最小**实际**负载的接收机不超过该阈值，增加一件至多βT。对每台机器以其最后一次接收任务收费，得到同时成立的负载界。无需错误地最小化`load/a_z`。
5. 完整资格是每次选任意最小负载sink仍合法的承重条件；任意eligibility不能沿用这个恢复器。ρ损失来自实际profile的上包络，不是cover误差。

## 边界与位复杂度攻击

核对了T0、正T但OPT0、c0、β0、无home、macro数超过home数、仅一个可用端点、空组、极大有理分母及任意输入数量的pool。零work由正rate与上包络强制全部pool时间0；T0时正宏home不可用，零pool出口必须保持，要求home承受正负载的模式被拒绝。OPT0由逐任务零边分配准确保持。

一个实际编码异议已经修复：仅以二进制整数H加少量private给出紧凑输入时，当前API的H长数组和匹配图不保证poly(log H)。正文§5明确机器逐台显式编码，H只是编号简写；这是本阶段真实复杂度合同，不声称更紧凑表示也成立。

`S=Σ1/a_z`和`c_j/S`只有多项式位长；模式数≤h(b+1)，每个cover至多`O(q_h^4/η)`状态更新，匹配为`O((b+h)^3)`整数步骤，最后恢复`O(n|Z|)`。所有成本/覆盖量为实际有理子集和，清分母的乘积位长是多项式数量的多项式位长之和。ρ、a_z、T的数值大小不控制循环次数。此处是整个算法界，有限枚举oracle不属于生产运行时间。

## 可复现代码与有限证据

规范代码SHA256：`64879bbb4daacb4ce603606a7c40850277405f4033fce81222f1e6053113cf14`。其复用旧`shared_sink_joint_assignment.py`的cover与Hungarian原语；未声称重写或独立验证新的同名原语。

在仓库根运行（输出到scratch，不覆盖冻结记录）：

```sh
python3 tests/audits/unrelated_machines/private_group_exit_pool_audit.py
python3 tests/audits/unrelated_machines/private_group_exit_pool_independent.py
```

规范审计906个实际实例，706个T可行实例均成功；检查174639份原调度，含321个零目标和6项非法合同。六组固定输入/实际输出包含非rank-one、无home、T0、空任务和大小尺度变换；源码、Python版本、seed、精度与范围见`private_group_exit_pool_audit.json`及实际input/certificate。

独立代码采用原任务完整分配求OPT、枚举macro目的地与cover子集，并用不同的顺序阈值恢复pool；不调用规范Hungarian或cover-FPTAS求其第二构造。ρ=1与ρ=9/8两批各700例，分别枚举99518与123701份原分配，551与571个T可行例无误拒，成功输出逐件真实负载核对；501个零最优实例保持0。它们不是一般证明，也不构成参数空间穷尽。冻结报告明确记录两条实现来源hash和局限。

## 结论与未审范围

声明范围内没有仍成立的fatal objection，两个新命题可登记为限域完整证明、内部独立已审与有限实现已核。cover FPTAS、dummy完美匹配和有界任务list scheduling均为标准机制；新增记录的是允许宏任务共同退出、给定profile时无界pool数量的实际接口组合，不认证基本算法新颖性、全球优先权、外审或独立论文价值。

没有证明一般矩阵能变成唯一home/完整pool/有界profile且保留统一余量；没有一般资格的共同容量恢复器。`UM-TARGET-v1`仍OPEN。成功推送、代码通过及两位审查无异议均不把该限域结论升级为主目标算法。
