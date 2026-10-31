---
id: customer-attraction/full-terminal-tax-fixed-policy-floating-attack-contract
kind: resource
type_tag: 资源
title: 完整终局税候选的策略锥浮点反例搜索合同
status: complete-source-contract-read; historical-no-witness-run-not-replayed
truth_status: unresolved-general-candidate-and-finite-diagnostic; no-exact-cone-lower-bound
review_level: full-code-read-and-comparison-with-original-independent-reconstruction
scope: 固定有序历史形式策略、同有限目录上的非负兴趣重数锥；原随机范围4/4、5/5、5/4
summary: 原程序以W=1归一，在抽样完整策略的真实IC锥内逐比较并集最小化终局税差；只在严格负浮点候选经有理化、完整证书和真OPT核验后保存反例。历史154策略未得见证不构成精确锥或一般证明。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/load_candidate_attack.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/independent_reconstruction.md
---

对共同目录单位客户游戏、m名玩家的实际终局覆盖负载c，定义
\[
F(c)=\sum_{x:c_x>0}\left(2-\frac1{c_x+1}\right)=W+E(c),\quad
E(c)=\sum_{x:c_x>0}\frac{c_x}{c_x+1}.
\]
原作者重新提出的普遍候选OPTₘ≤F(c)，已被识别为既有full-terminal-tax/OCC-CAP，未成为新定理。对任意有限非零负载W≤F(c)<2W，所以普遍候选若成立会给half；仅核固定终局或若干锥不能完成它。W=0给F=0，不用严格不等式。

对比较m主题元组负载d，定义G_c(T)=Σₓ∈T1/(cₓ+1)，逐客户恒等式给
\[
|\cup T_j|\le\sum_jG_c(T_j)+E(c).
\]
右减左的精确松弛为
\[
\sum_{c_x>0,d_x>0}\frac{d_x-1}{c_x+1}
+\sum_{c_x>0,d_x=0}\frac{c_x}{c_x+1}
+\sum_{c_x=0,d_x>0}(d_x-1)\ge0.
\]
比较重复覆盖与比较并集外的实际客户均要保留。要求m·max G_c(T)≤W是更强的充分桥，既有14客户两人完整SPE以W=9、遗漏主题G=5否定它；这不否定候选F。上述身份及历史反例导航已由[既有独立重构审查](../审查/R105交叉分支与regret修复障碍接续审查--审查.md)保全，本源程序增加的是明确搜索合同和停止点。

## 固定策略锥与真正优化量

先从有限随机游戏用 ExactSPESolver 取至多四个低福利计数终局q，并取一份实现q的完整有序策略cert。`policy_matrix` 对每个有序历史h和非规定动作b，分别沿cert真实补全两分支，形成每个非空兴趣类型L上的收益差Γ(h,b)；只去重完全相同的行，不按计数合并独立历史的选择。固定策略的重数锥是w≥0、Γw≥0。

令c_L=Σₐ∈Lqₐ，e_L=1_{c_L>0}，f_L=2−1/(c_L+1)（c_L=0时f_L=0）。对比较支持P，原代码用浮点HiGHS求
\[
\min_{w\ge0,\ \Gamma w\ge0,\ e\cdot w=1}
\sum_{L\ne\varnothing}(f_L-\mathbf1_{L\cap P\ne\varnothing})w_L.
\]
其中P遍历大小min(m,k)的不同标签子集。客户重数非负、覆盖单调，任何更小支持可扩充且不减少覆盖，故这对m主题最大覆盖比较足够；它不强制实际SPE路径无重复。归一仅覆盖W>0锥切片；代码没有证明这是任意实例的完整归约。无兴趣客户不在锥变量中，对收益和覆盖确实为0。

`linprog` 失败被跳过；返回值只更新该批浮点最小值。目标若小于−10⁻⁸，才逐坐标用分母上限10⁷的Fraction恢复w、精确检查全部Γ行、清分母成整数客户重数、构造新Instance并调用完整策略验证器。CustomerType要求正整数重数，verify_certificate逐有序历史核全部备选、完整性和根终局计数；这些API已在保存实现中定向读核。最终再以该新游戏的精确optimal_welfare检查F<OPT，才输出完整游戏/策略/负载/比较支持反例JSON。代码没有保存非负浮点最优的精确对偶，更没有把所有不可行/非负求解结果变成精确锥证明。

## 有限原运行与本轮执行身份

原main种子105776，参数(k,m,cases)为(4,4,40)、(5,5,40)、(5,4,30)；每个非空兴趣类型以0.24概率保留，重数1至9，每个实际游戏最多取四个SPE终局。原 `independent_reconstruction.md` 和README记录历史154份完整策略抽样没有返回反例。该叙述是历史运行报告；本四源没有附154份输入、逐LP日志或精确对偶，不把它补称可逐项重演的冻结证书。

本轮load_candidate_attack.py全文实读，**新运行0次**。它被原作者识别为已有候选后已停止的有限诊断，不为清洗重复扩大浮点搜索；程序本身、完整历史判断和遗漏的证据边界均已准确保全。只在[背景删除审计](../计算/背景删除节点后悔的定义级精确审计--计算.md)另有一次标准库原入口运行，不能把它计入此攻击程序。

原脚本通过 `__file__.parents[5]` 假定旧仓库层级并导入customer_attraction；直接移动后需要明确依赖路径映射。证据包原文件不改；若未来真运行，应固定所用solver/Instance/verifier字节和SciPy环境、保存输入及每LP状态/精确见证。这里未补造历史环境、exit码、154份客户重数或一般安全/六人结论。
