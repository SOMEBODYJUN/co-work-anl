# 共享外端四环与 small-query 池：canonical 限定全文读后

2026-10-18。已实际通读指定 canonical 全文。**正式认证仅限 §4 的四任务 matching 边界，以及 §5 的新 ID `UM-SHARED-OUTSIDE-SMALL-QUERY-RETURN-POOL-EXACT-RELATION-v1`。** §1–3 的其它主 Claims 只作 context，不在本次独立认证中。

## 实际读取版本

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md`

实际字节数 14,658；实际核对 SHA256：

`6074c7ee16c63404e09ad5fb11ed927c1594f91d58c79abd37469a0c58d92fd4`。

本记录只认证该实际读取 hash 对应的指定章节，不预先覆盖未来改动。旧 Exact-first、作者 Proof 读后和原件均不修改。

## 限定结论

**PASS；两个指定接口在该 canonical 中完整正确落地，无 standing fatal。** §4 明确只是标准匹配边界、不另立 Claim；§5 的新 ID 精确对应已审 small-query/return-pool 的全模式关系。没有将任何一个孤立OPT1模块升级成 source NO、任意外接、变量一致性或 near-2 hardness。

这不是对 §1–3 的局部异权交换/全公式三半模板结论的代审。只因它们与本次对象共页，并不使其依赖、算法、存在量词或外部共同负载自动通过本次认证。

## §4 四任务边界的实际核对

- 完整四job四机矩阵与源 Exact 一致：q_i 仅 H:1/E_i:1，b_1 仅 I:1/E_1:1，b_2 仅 I:(1-epsilon)/E_2:1。E_i 确为共享原机器；四件原 jobs 都必须执行，没有aux、preload或private outside替代。
- 两 aligned assignments 的峰恰1；每 q_1 有限端均time1，给全域OPT下界1，故普通OPT1。
- `C<2-epsilon` 时四台每台至多一job、四jobs强制perfect matching，恰两个aligned。这包含未指定的其它internal subsets，不仅排掉inactive和cross。
- inactive精确峰 `2-epsilon`，两个cross由相应E_i双unit精确峰2。临界等号增加的三份非aligned assignments 是inactive与各一个query加全部returns内部；连同两aligned共有五份。canonical正确保留strict符号，没有改成闭阈值唯一两份。
- `epsilon=delta/3,B=2-delta` 的有限有理strict gap及 O(bitlen(delta)) 编码正确，机器/jobs/finite entries固定。epsilon=0的背景说明仅扣除matching机制，不把正式0<epsilon<1范围改写。
- 两份witness machine-presence相同、每机有一job，并没有闲slot读取合同。新增资格、jobs或外机同一化须重证；canonical没有将该例当成对单纯内部交换的反例，也未新增研究Claim。

## §5 pool 新 ID 的实际核对

| 对象/量词 | canonical 实际核对 |
|---|---|
| 全部输入域 | k>=2、显式正有理a_i总和<=1；2k台互异H/P/E；仅2k件原q/b；q唯一outside E_i；b在任意P或同E_i；其余端infinity，无aux/preload。与源Exact一致。 |
| 全部pattern | S、T任意，包括空集与多query/multireturn；pool返回可任意选P，未把一P一件当硬资格约束。 |
| good pattern | `empty!=T subseteq S` 使pool返回<=k-1，按索引注入不同P，全部原jobs精确覆盖，H总<=1，E每机<=1，b-unit下界给精确OPT1。 |
| bad pattern | T不包含于S给共享E_i双unit；T空给k个unit returns挤k-1池。任意rho的下界2与显式最多一个池双job的上界2结合，精确OPT2。 |
| 任意真实弱sigma | 给定C<2才推出P/E各至多一unit、T非空containment；再结合H<=1，这份原sigma本身峰<=1，无需先重新优化rho。 |
| 最优与任意rho区别 | canonical明写同一good pattern的不恰当pool分配可峰2或更高；并未从pattern OPT1推出每份实际assignment都峰1。 |
| 返回合同强度 | 只保证至少一返回且T subseteq S，不强加S=T、singleton或每个内部query都有return。 |
| 全局孤立值 | S=T全部indices给普通P的unit调度，所以恒OPT1、没有source NO。 |

阈值边界也正确：正式weak合同只用 `1<=B<2`。在 B=2，所有 S/T 都至少有一个峰<=2 witness，坏patterns重新可行；k>=3 时坏的rho仍可峰>2，所以“所有patterns有witness”不同于“所有assignments被接纳”。这些均由canonical的两个方向证明给出，没有闭阈值soundness升级。

singleton aligned/inactive/cross只是完整pattern定理的特例，不遗漏其它模式。k=1始终排除，因其无pool机时T空pattern不再有有限调度。H允许真实多个small queries共居，不沿用§4“每内部机至多一job”的假设。

## 位量词、解码、外接及证据归属

pool 机器/jobs各2k、finite entries `k^2+2k`、dense `4k^2` 全部正确。构造和读取实际目的地只按显式列表及二进制有理输入位长计，不枚举所有patterns，不按分母或delta倒数展开。每件原job输出一个合法原machine identifier；没有未知source或optimum witness输入。

canonical明确：新增q_i外端、E_i与变量环或其它i同机、其它jobs都会改变完整矩阵，不能继续免费沿用T subseteq S。这与源Exact/Proof的scope一致；没有认证外部formula一致性、费用共享、任意clause读取或源hardness。

此前四环的独立小样本负载检查，以及pool在k=2,3,4的4,328份辅助assignments检查，均仅由本reviewer执行。canonical的“root独核全部pattern”可正确指root实际阅读和独立数学核验，不宣称root运行这些有限程序。有限检查不是一般证明，也不构成软件实现认证。本次未新增运行或实现。

## 原件保持

冻结本记录时实际复核以下八份原件/审查，hash未变：

| 文件（位于scratch根） | SHA256 |
|---|---|
| 四环 Exact | `c2f73db04495292714a6a083029b707f3c4c246647e4975f1f58bfdcaf15fe19` |
| 四环 Proof | `43f9bbfc184b7283250b6a5930bab08fabf675c7186babe3fdd7b798ef989fc7` |
| 四环独立记录 | `d77a2e3b911b1f31ebc939fb52c14145d8994d36e82baddf4ecfaff6fb73dce1` |
| 四环作者读后 | `ff7b890d09782e696631a879a54e7f3cba495d4fa75a8bd3a0cdbba40c077bd3` |
| pool Exact | `37304837169ba1e11595c9681528dfe21efe2ccf8a04e6bafc73b7c2b8cf2e4e` |
| pool Proof | `ed5b9c15e075db63c6bfae57511ad025ed254d422b4dd92000ad4a05d1449b99` |
| pool独立记录 | `859691b410ae5ab0033c541508307108e42097400c3c4a42f38c042889f4baf1` |
| pool作者读后 | `49ccdf469a06a0a6b45b3d8fd20090c818d20572b201bd86910acb8fa0d8f20b` |

未改repo、Git、Work或旧源。无standing fatal的限定结论仅属于§4/§5；不认证§1–3、其它Claim、新颖性、外审、实现或主目标closure。
