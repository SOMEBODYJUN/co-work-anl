---
id: "unrelated-machines/hall-original-joint-flow-promise-and-nine-matrices"
kind: "resource"
type_tag: "资源"
title: "Hall共同宏组接收流的原实现与九矩阵证书"
status: "complete-primary-read-and-full-saved-matrix-verification"
truth_status: "implemented-restricted-flow-and-promise-search-with-finite-audits"
summary: "保510行规范接口的严格合同、一次macro/home/sink流、真实前缀、联合瓶颈promise搜索和九个job-major矩阵；纠正旧页把2773成功数归入其他分支的说法。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/hall_group_joint_flow.py#全文"
evidence_manifest: "archives/unrelated-machines/tools/evidence/um-ghmr-flat-moment-and-hall-primary/README.md"
---

主源9fa5bc2e0157bd3693a9全文510行、24011B，SHAebcf08cbc82b841b86ab5c567d1abad79de0cf4b501bcffc24172fba3b94e46e，全部实读。它实现solve、solve_promise、真实矩阵/负载核验和有限枚举；已有[Hall冻结审查](../审查/Hall联合组流冻结审查增量--审查.md)保存一般推导，本页保存实际软件，不重授定理。[全部源、九输入矩阵、九输出及数据自查](../../tools/evidence/um-ghmr-flat-moment-and-hall-primary/README.md)可直接接续。

## 明确域及失败类型

机器为homes H和k台sinks，机器合计至少一台；允许k=0，k代表显式sink数。每home一组不交私有任务，逐job时间w≥0，仅可在该home及共同资格E_h执行，所有这些端时间相同。宏只可在homes。q是严格整数≥2，delta≥0、qδ<2，给定T≥0时要求全部有限宏端>T/2（包括未使用边）、每组

\[
(1/2+1/q)T\le W_h=\sum w_j\le T,\qquad w_j\le\delta T.
\]

None不可用；rational只收精确int/Fraction/string，拒绝bool/float。资格索引检查后去重排序、宏行尺寸和每宏有有限端、至少一机器均显式验证。数学位复杂度按显式二进制有理编码计，不据便捷字符串解析宣称新的紧凑数值输入模型。违反合同抛ValueError/TypeError，与合法合同内的None可靠FAIL不同。

solve在T0时私有w必须全0，有宏则返回None，无宏逐件留home并附完整零负载。delta0非零输入的未知OPT-promise不成立，solve_promise可报ValueError；空任务、无home但有sink、空资格和零宏均保其实际分支。

## 一个流同时决定所有宏和接收机

网络源→每宏容量1；宏→home-in容量1仅保原p≤T端；home-in→home-out容量1；home-out→每E_h中的sink容量1；sink→汇容量min(q,宏数)。BFS按确定节点顺序增广，最多宏数次，不创建q份sink或按二进制q数值循环。

若存在真实T调度，宏>T/2使占用home互异；每占用组实际出口 \(e_h>W_h-T/2\ge T/q\)。同组同体积和共同资格给任意占用子集A

\[
|A|T/q<\sum_{h\in A}e_h\le|N(A)|T.
\]

因此q-copy Hall成立，只在证明中想象复制，原宏匹配与该接收匹配共同给满流。流不满才可在本合同内推普通OPT>T。先独立固定一个宏匹配可能选无接收资格home，不能替代这个共同网络。

取 \(\tau=(q-1+q\delta)/(q+1)\)、\(\rho=q(2+\delta)/(q+1)\)。每占用组按原任务次序迁出前缀直到剩余≤τT，整段送流选的共同sink；未占用组全留home。末件≤δT给每组出口≤(1−τ+δ)T，故

\[
L_h\le(1+\tau)T,\quad L_z\le q(1-\tau+\delta)T,\quad
1+\tau=q(1-\tau+\delta)=\rho<2.
\]

零任务可以先被前缀迁出但身份仍在，不能据零工作把job删除。输出每宏实际端、每私有job实际端和全部机器负载，不只是整数流值。

## 未知OPT接口的瓶颈是联合流瓶颈

solve_promise先作精确零边分支。正值时要求delta>0，在全部有限宏时间排序表中二分最小B，使**同一macro/home/receiver联合网络**满流；无宏B0。不是只找宏到home匹配的最小瓶颈。令

\[
t=\max\{\max_hW_h,\max_jw_j/\delta,B\}.
\]

若在真实O=OPT处满足完整promise，真实O调度的Hall证明给B≤O，其他两项≤O，所以t≤O；原全部宏边>O/2≥t/2，组下界也自动在t成立，solve(t)给真实峰≤ρt≤ρO。只对随宏边增加单调的网络做二分，不假设整个带组界的阈值合同单调，也不使用OPT精度oracle。域外可报ValueError，不免费识别该含OPT承诺。q增长时改善\((2-q\delta)/(q+1)\)可趋0，非一般统一epsilon。

## 原矩阵oracle和有限main的实际归属

full_matrix按job-major保存宏在前、再按home/组原次序的全部私有job，机器homes在前、sinks随后。matrix_optimum从这些原端做带精确当前上界剪枝的指数搜索；exact_feasible另作原任务阈值递归，不调用Hall oracle。matrix_check从完整实际输出还原σ和每台原负载。它们是有限审计，不是生产接口运行所需的最优值oracle。

基础域h1..3、k0..2、0..min(2,h)宏，所有共同资格与非空宏支持图、两half组、宏3/4、q2/delta1/2：共4448，真实T1可行2278，输出2773，可靠拒绝1675。**这四个counts只在基础循环增加**；2773包含495个T1不可行但舍入成功的基础输入，命名fixture及其他域没有混入。原代码逐例断言所有2278真可行都输出。旧页“输出还包括命名fixture/其他分支”的解释与实际循环不符，只保未应用修订建议，不覆盖共享页。

非均匀组(0,1/3,1/3,1/6)、q3/delta1/3、强制宏2/3的228例单列。宏变化域h2、k0..2、0..2宏，所有行取None,3/5,1,5/4但不全None，两种组参数，共10122，T1可行2071、输出2650。三个域合计14798，关于其真实OPT满足完整promise的检查及附带例计3991；这不是3991个全新去重矩阵。另2079个公式点包含qδ2仅作代数端点，不传给要求严格qδ<2的solve；9类非法输入拒绝单列。

## 九份完整输入输出及本批核对

| 名称 | 真实输出/边界 |
|---|---|
| joint_reselection | 宏共同重选home1,2，原峰OPT1；输出负载1,3/2,3/2,1/2,1/2 |
| zero_target | 全零私有任务完整保留 |
| zero_target_positive_macro | T0但正宏，合法合同内None，真实OPT1 |
| zero_macro | 无宏、组留home |
| pruned_only_macro_edge | 唯一宏端2>T1，None，真实OPT2 |
| large_denominator | 分母\(2^{521}-1\)的完整实际原任务与前缀 |
| huge_q_empty_jobs | q=\(2^{200}\)，无home/无job、一台sink；只是巨大q空任务边界 |
| near_factor_two | q3、qδ严格小于2的有理近端点，仍真实输出 |
| unknown_opt_bottleneck | 联合瓶颈t=OPT11/10；输出home1,2负载37/20、rho27/16 |

50558…和40c223…分别保九个完整job-major原矩阵及实际输出/σ/精确OPT。新独立数据核验不导入原程序，逐份重新列所有原端，枚举共2152个合法完整assignment求九个OPT；7份成功输出的46枚原job全部核资格、实际时间和所有机器负载。它不是新一次Hall主审计或无界检查。旧同SHA的6b44…主报告已充分，本批Hall原main新run0。

CLI不加参数只stdout；--export-dir会创建不存在的新目录并以排他写方式输出九命名证书，不覆盖旧文件。旧主稿/审查的最后变化仅有O(n log(m+1))输出位长及域外分支说明，最终当前正文和代码SHA均保其真实范围。唯一home、组同资格/同体积、组负载下界及全部宏大边均不可删；现行旧双源页提到W_h≥T的反例是q2特例，不可替代一般\((1/2+1/q)T\)合同。外审、新颖性与一般UM仍未认证/开放。
