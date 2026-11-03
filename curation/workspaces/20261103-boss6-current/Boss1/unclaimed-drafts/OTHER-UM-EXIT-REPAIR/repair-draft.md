# OTHER-UM-EXIT-REPAIR 定向修复草稿

正式输入及 SHA-256 与任务 JSON 一致：

- `archives/unrelated-machines/state/审查/私有组退出池共同宏任务与有界profile联合选择最终审查--审查.md`：`c9ed10ee9e158913d5730f3f389dc4b0b0076d8053d043a24568e9079fcb7fd6`。
- `archives/unrelated-machines/state/审查/Hall联合组流与共享汇点宏分配双源审查--审查.md`：`ac9117aff59705e364108d20e3a1278c650e4adc09bba21c417355b717dce686`。

## 损伤定位与复用

第一输入 §1.3 的“宏任务数可超过 home 数，此时匹配无完美匹配并安全 FAIL”错误。此推论仅适用宏任务只能去 home 的旧接口；允许宏退出后，home 容量只推出至少 `b-h` 件宏任务必须退出，不能推出扩展的 `(b+h)` 阶匹配不存在。

第一输入 §1.1–1.2、第二输入 §8 及冻结规范正文 `archives/unrelated-machines/tools/evidence/um-eligibility-variants-next/comparison-sources/research/current/unrelated_machines/shared_sink_joint_macro_assignment.md` §8 已有正确共同匹配构造。规范实现 `archives/unrelated-machines/tools/evidence/agent_um-20261101/private-group-exit-pool/private_group_exit_pool.py` 已构造 `(b+h)` 方阵；没有 `b>h` 提前拒绝。无需重做或更换算法。

## 拟补正式数学

### 同一匹配中的真实费用

对完美匹配 `M`，记 `C_exit(M)` 为匹配中真实宏任务退出边的真实 sink 成本，`C_cov(M)` 为所有 home 所选真实或空模式的 cover 近似成本之和；dummy→exit 成本为零。最终汇点负载恰为

`C_forced + C_exit(M) + C_cov(M)`。

若 `M*` 来自一个真实 `T` 调度，记其 home 模式精确最小 cover 成本之和为 `C_cov*(M*)`。原调度给出

`C_forced + C_exit(M*) + C_cov*(M*) ≤ T`。

算法最小化的是含真实 exit 成本的同一个匹配目标，因此

`C_forced + C_exit(M) + C_cov(M)`

`≤ C_forced + C_exit(M*) + (1+eta) C_cov*(M*)`

`≤ (1+eta)T`。

局部误差只作用在可选私有撤离成本，不放大真实宏退出成本或强制私有退出成本，也不按 home 数增加误差。不能单独比较 `C_exit(M)` 与 `C_exit(M*)`；正确比较的是完整匹配目标。

### 两宏、一 home、一 sink 的反例

令 `T=1`，私有组为空，有限时间为 `p_(h,b1)=3/4`、`p_(h,b2)=3/4`、`p_(z,b2)=1/4`，而 `b1` 不允许退出。所有有限宏 home 边均严格大于 `T/2`。此时 `b=2>1=h`，却有完美匹配

`b1→home, b2→exit1, dummy→exit2`。

home 模式 cover 成本为零，匹配成本为 `1/4`；恢复负载为 `L_h=3/4`、`L_z=1/4`，真实 `T` 可行。退出位置只区分宏身份，不能把它们解释为各自独立的 sink 容量。

因此不以 `b>h` 单独返回 FAIL；完整扩展匹配不存在，或恢复的真实汇点成本超出 `(1+eta)T` 时，才使用相关拒绝分支。在无可用宏退出边的子情形，`b>h` 确实使该完整匹配不存在，与旧 home-only 接口一致。

### Profile 恢复中的最后一次收费

保留两侧 profile 包络、完整 pool 资格和单件上界。若每台 pool 当前负载均大于 `A=rho(1+eta)T`，则

`sum_(已放 j)c_j ≥ sum_z L_z/(rho a_z) > (1+eta)TS`，

与全部退出 work 预算矛盾。故每次选择的实际负载最小机器在放置前负载至多 `A`。对每台最终收过任务的机器，以其最后一次接收任务计费：放置前至多 `A`，放置该件后至多 `A+beta T`，此后不再增加。因此界同时对全部机器成立。未收过任务的机器负载为零。该表述修正现文“加一件后……之后不再改变”的省略，避免误读为任一放置后均不再接任务。

## 覆盖保全与具体缺口

复用并保留：旧 home-only 命题及其 `b≤h` 必要条件；所有真实 home/exit/dummy 身份与原任务回溯；一次共同匹配；局部保覆盖 FPTAS、零成本分支和 `poly(总位长,1/eta)` 复杂度；强制私有成本只加一次；成功时 `L_h≤T,L_z≤(1+eta)T` 及 `OPT≤T` 必成功的单侧量词；完整 pool、统一上下 profile 包络与单件 `beta T` 上界；虚拟 work 归约和恢复的 `[rho(1+eta)+beta]T` 界；原有限审计证据及其局限。第一输入结论 `rho a_z_j` 的排字应改为 `rho a_z c_j`。

不改变也不宣称填补：任意 unrelated-machines 矩阵到唯一 home/完整 pool/有界 profile 的结构提取；任意资格的共同容量恢复；无 profile 上包络的多 sink 恢复；一般 UM-TARGET。预算内无需新增一般化。

自查针对改写处及承重依赖：反例逐边合法、严格 home 大小条件成立；`b+h` 两侧计数一致；每件宏及私有任务恰执行一次；exit 位置不是物理容量；完整匹配目标包含真实 exit 成本；最小成本比较允许更换退出身份；cover 误差仅对同一预算内的可选成本求和；pool 下包络用于虚拟可行见证，上包络用于恢复收费，完整资格保证每次最小实际负载选择合法；同时界用每机最后一次放置。未重新审查 Hall 流及全部旧证明。
