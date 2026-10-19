# 完整机器任务克隆的多重集、最小周期与指数首次达到：独立后审

对象为 `UM-COMPLETE-CLONE-MULTISET-PERIODICITY-v1`，只审 [正文](../../current/unrelated_machines/private_graft_and_resource_repetition.md)§8.1–8.6（130行），不重审此前§1–7。主研究者为boss24，发布actor为R-40bb9e2c2cb04c489d65ec3d7bf38331。

## 实际发生的审查与最终绑定

`/root/assignment_representation` 最初收到精确候选及主研究者对有限负载集合、半群、分母界的提示，未读另一研究者的完整推导；随后独立重构MC双向实际恢复、阈值达到与半群，并加强为最小最终周期及limsup公式。这不是完全无提示的盲审，也不是把同意票当证据。它在独立重构后实际全文读§8和全部267行规范代码，实际执行代码；最后实际重读修订后的完整§8。

`/root/gap_amplification` 是完整克隆候选的参与构造者，随后实际全文读§8及规范代码并执行；其实际后审不标为盲审。它另行重建原二值CONFIG/多重集差别及任意周期族，核了Sylvester递推。主研究者独立重构有限阈值、整数半群、行容量和Cramer界，编写并实际运行规范审计。没有外部同行评审或全球新颖性认证。

| 最终对象 | SHA-256 |
| --- | --- |
| 正文全文件（审查只覆盖§8） | `6afdec871fa9a209cfb15d169b2846548522d1805ee24f269ec7b97145012d5f` |
| §8从标题至EOF的精确字节 | `963833e8093222662cfc161e81cca83bf3a89cb764ff967e931346183e8446c5` |
| 规范审计代码 | `ff27143a75627f1e6d7bd0f21afccb1ab21aa6119b5a9ed18778c992177bd9de` |
| 冻结运行输出 | `229ffdcf1a54afd756012957457258e70b2f07a0c33ccf4cc11ad9242a72301a` |

独立审者实际运行输出与主研究者冻结输出逐字同hash，均为16138字节。最终读后结论：**无尚成立fatal，无未修复的必要修改**。

## 实质攻击与消除情况

| Proof obligation | 检查与结论 |
| --- | --- |
| 不把complete blowup偷换成置换cover | 每原端确含q²边，所以一个机器副本可接同原类型多件；多重集配置是正确投影。旧cover每原类型至多一条邻接，不能沿用其CONFIG等式。 |
| 零、空任务与不可用端 | 删除的是至少有一个零端的整个类型，全部副本可零负载补回；删空时t₊=0、Λ={0}。其余最小有限处理时间严格正；原输入合同排除无可用端任务。 |
| 聚合计数是否真的恢复全部原任务 | 每类型的slot总数恰q，与q个带标签任务一一匹配；全部克隆资格保证合法。不是仅报告负载估计或存在性oracle。 |
| 最小阈值是否取得 | O_q≤U且每个正配置件数≤K，所有最优值在同一有限有理Λ中；理性LP基本解把任意可行阈值恢复成某个整数q。无极限交换或紧致性漏洞。 |
| 加法闭包是否给最终gcd | 模最小正元的可达余数构成有限子群；选各余数最小代表，直接生成所有足够大gcd倍数，不假设免费计算conductor。 |
| 最小而非某个周期 | 阈值嵌套给d_t\|d*；最优层最终恰d*倍数，任何最终周期h必须保持该集合，迫d*\|h。 |
| limsup与收敛 | 沿q=kd*+1排掉全部非平凡d_t，精确得到首个gcd1层；有限值域保证收敛iff最终恒定iffd*=1。 |
| 分母界是否保证显式多项式 | Cramer/Hadamard只给log d多项式；正文明确不提供MC求解或输出指数多副本的位多项式归约。 |
| 指数首次达到是否只是某个劣证书 | Sylvester族逐行ceil容量给O_q=1 iffR_k\|q，故R_k是所有真实调度的首个达到数；不是仅声称某个基本解用了大分母。矩阵总位长Θ(log R_k)成立。 |
| 任意周期族是否遗漏接收机容量 | 逐行private整数slots充要为mb_i≤q(d+1)，再共同分配所有q件big；m1、q1与余数零分支都覆盖。 |
| 相对主目标的结论范围 | 没有NP-hard源。结果只排指定操作的通用保NO与单调极限断言；不排精选接线、hard-image专属构造、附加一致性或UM-TARGET-v1本身。 |

初读发现两处非fatal措辞：“任一原调度给U上界”不严谨，已改成先选最短端的实际调度；含0的S_t恒非空，已改成“含正整数”。另显式补上删空时Λ={0}。独立审者实际重读这三处及最终§8，确认修复；未借改文改变Claim的数学身份。

## 规范代码的实际审读与运行

代码 [complete_clone_multiset_periodicity.py](../../../tests/audits/unrelated_machines/complete_clone_multiset_periodicity.py) 的两个求解方法不调用彼此：带标签有限枚举使用逐机负载与安全对称剪枝；类型计数DP按全部机器副本更新最小瓶颈。初始最短端总量U是已知合法上界，因此 `new >= best` 剪枝在零值与空任务时也正确。它们都是有限指数oracle，不标为通用多项式后端。

实际运行命令（重跑写clone外scratch，不覆盖冻结输出）：

```sh
python3 tests/audits/unrelated_machines/complete_clone_multiset_periodicity.py > /workspace/scratch/2b358e60fdc5/complete_clone_replay.json
```

Python 3.12.14，Fraction与整数算术，seed24019，全部断言通过。固定输入含空任务、零端、单可用端、单机与大有理分母。

| 有限范围 | 实际检查 |
| --- | --- |
| 86个固定／seed生成矩阵，q1、2 | 172次双oracle比较；不是遍历全部矩阵 |
| 奇偶三任务seed，q1..5 | 两oracle给3,2,3,2,3；全部带标签搜索共2290节点，节点数不是完整分配枚举数 |
| 奇偶seed，q1..24 | 24份完整带标签分配逐机核验，另50个整数容量判据核验 |
| 任意周期族m1..9、q1..40 | 360组全部任务构造与独立最小容量条件核验 |
| Sylvester前5族、q1..100 | 500次Fraction/ceil容量核验；k1、2、3另实际展开首个最优复制数全部带标签任务 |

冻结输出为 [complete_clone_multiset_periodicity.json](../../../evidence/runs/unrelated_machines/complete_clone_multiset_periodicity.json)。没有通用MC solver、conductor/period finder或普通UM近似算法实现。有限检查不代替上表的一般证明；外审、新颖性、独立成文价值均未认证，UM-TARGET-v1及一般反面仍OPEN。
