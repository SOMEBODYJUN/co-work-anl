# 固定超载见证件数过滤的独立重构与最终全文攻击

日期：2026-10-19。仅覆盖正文§7的 `UM-FIXED-ARITY-WITNESS-FILTER-v1` 和 `UM-FIXED-ARITY-OVERLOAD-HARDNESS-BARRIER-v1`；前文top-2结果保持原身份与审查。

| 实际最终读取对象 | SHA-256 |
|---|---|
| `research/current/unrelated_machines/top_two_pair_witness_boundary.md`，仅§7数学范围 | `7edef8d895a5f5ea7eeb507251268fd303388d26da8429882ee5ac2cb857e119` |
| `tests/audits/unrelated_machines/fixed_arity_overload_witness_audit.py` | `88796d363c8dc33348ed6e156287a1d4daa30398db104c7fe21f20f14e3ab532` |

## 独立顺序与覆盖

`hardness_source`先只获精确阈值合同、初版较弱常数与后来加强的常数递推，独立重构有限big配置LP和不同的定量前缀证明；它没有读作者证明才开始该重构。root传达了可检查的split阈值提示，因此不把后续更强常数论证称为完全盲审。之后该研究者实际通读完整作者证明、最终canonical§7与全部审计代码，并在新结果路径重跑规范程序。root另行重构类型多面体、big/tiny拼接与全部输出语义。

上表记录实际最终读取的字节；章节和式号改为7.x后已经实际全文读取。审查不是以审查者数量或有限计算作证明。

## 关键攻击

1. 原命题只保证`FAIL⇒普通OPT>T`，并非所有OPT>T输入都FAIL；成功只控制B_r，不控制总负载，也不保证OPT≤T。这些方向在正文、算法与账本一致。不声称相对O_r=minB_r的近似。
2. triple流的必要性来自普通T调度每行第s件≤T/s；所有原job各流一单位。输出可同时有T、T/2、T/3三件，故11/6是这个流合同任意输出的锐包络，不是hardness或一般最佳算法界。
3. 行引理的H_t>t来自严格正交长；不能改成≥。当a_r≤1/(D+1)，更短前缀的1/D余量付清新增项；高分支每正权配置截断后至多D件。
4. 高分支类型行l1范数≤D，排序行范数sqrt2、非负行1。H_1>1迫z_1≤1/2；Abel使全部非零z的坐标和严格小于1。有限整数顶点的分母≤D^(r−1)，故精确得到c_r=c_(r−1)^(r−1)。没有把数值接近1当作严格余量。
5. 一般CONFIG没有被当oracle。δ=c_(r−1)/(2r)固定，枚举big子集至多n^K，标准显式有理LP与基本解位长均按输入位长多项式。tiny无本地总工作约束是有意的：控制目标是固定前缀。
6. q=ceil(big质量)≥r时前r槽全由big最大值控制；q<r时只有后缀tiny进入，用c_q≥c_(r−1)而非最弱c_r付费。全部任务只做一次共同槽匹配，Hall来自任务守恒；每机任意r个选中槽可收费给前r槽。
7. 空任务、T=0、原零边、∞、单机单端和大分母均有精确语义。r随输入增长时枚举次数和常数均无统一保证；固定r的障碍不能排除r随固定epsilon增长的归约族。
8. CSP只是所有原同机阈值子集的无丢失表示；不能将任意r-CNF关系免费实现为同一实际矩阵。NO量化所有完整保留端分配、严格>rhoT；rho=2−c_r的等号端点仍可判别。

## 实际核验与未实现范围

运行：`python3 tests/audits/unrelated_machines/fixed_arity_overload_witness_audit.py`。规范[冻结JSON](../../../evidence/runs/unrelated_machines/fixed_arity_overload_witness_audit.json)保存seed20261019、代码hash、14424个两机矩阵及65640个完整实际分配、5440个局部配置law、484份r=4..7的完整big-only证书（q=0/短/长均覆盖）、4092个tuple等价检查和8个非法输入拒绝。程序实现triple整数流及给定一般LP证书的验证/舍入，不实现一般有理LP后端。

`[[1/4,1/4,1/4,1/4,1/4]]`的普通OPT=5/4、O4=1被精确核算；故不能将本算法未经证明改写为相对O_r的近似。有限核验不替代一般行引理、位复杂度或全称可靠性。

**判定：以上最终字节与精确合同无尚成立fatal objection。** 结果是反面归约的限定过滤器，非一般makespan严格次二算法、近二hardness或不存在epsilon证明。外审、全球新颖性与独立论文价值未认证。
