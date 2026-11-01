# 真正聚合安全值桥：独立攻击 checkpoint

2026-10-21。研究对象严格为 CAG-MODEL（单位客户、共同有限目录、任意完整历史纯 SPE）。主目标 Q-CAG-HALF 及辅助桥

\[
\mathrm{BR}:\qquad W\ge m v_m,
\quad v_m=\max_p\min_{B\in\mathcal S^{m-1}}\sum_a p_a f_B(a)
\]

均未解决。本目录只是个人探索资产；浮点优化器输出和零反例实验不构成排除定理。

## 当前结论身份

1. **Elementary reduction SC-RED-FULL-INTEREST（解析观察，尚无独立审查）**。若某兴趣类型喜欢全部目录主题，重数为 c，则删除该类型不改变任意固定完整形式策略的 SPE 性，且
   \[
   W'=W-c,\qquad v'_m=v_m-c/m,\qquad W'-mv'_m=W-mv_m.
   \]
   证明：全部终局每一位玩家均从该类型得 c/m，故任意真实偏离收益差为零；任意查询、任意静态竞争背景亦都得 c/m。因此寻找 BR 的严格反例时可无损将全兴趣类型质量置零。零福利退化不能是严格反例。此为基础消元，并不支付任何早期玩家的安全值。
2. **Elementary cap SC-CAP-IID（标准基本观察，不作新颖性主张）**。任意查询 p，以 m−1 个独立 p 主题作为静态对手。令 m 个独立 p 主题为 Z，由对称性
   \[
   \min_B\sum_a p_af_B(a)\le \frac1m\mathbb E W(Z)\le\operatorname{OPT}_m/m.
   \]
   对 p 取最大即 \(mv_m\le\operatorname{OPT}_m\le|N_{\rm coverable}|\)。所以终局覆盖全部可覆盖客户时 BR 自动成立，严格反例必须遗漏正客户质量。这个必要条件不能转成半覆盖证明。

## 已完成实验（全部仅 numerical discovery）

* `search.py`：完整可实现 SPE 终局集合递推（按计数缓存集合，而非固定平局策略），每个输入另解真正静态安全值 LP。7 主题、5 人、seed182，20000 次随机/局部客户质量候选，重数为非负整数；搜索拒绝覆盖全部客户的候选，全兴趣类型固定0。最高浮点 \(5v_5/W=1.0000000000000002\)，没有超过容差的候选。时间约264秒。最优点存 `best-k7-m5-s182.json`。这不证明一般桥，且很多等号面来自互不交的大主题/小主题结构，局部搜索易停在等号面。
* `cone_search.py`：从 seed 的逆向归纳得到随机完整 count-Markov 策略，保留各节点全部真实一次偏离行 Γ；固定查询 p 后，在 \(w\ge0,\Gamma w\ge0\) 上用 LP 最大化 \(m\min_B\beta_B(p)w-W\)，并与给定 w 的最优安全查询交替。7 主题、5 人、seed184，300 棵策略，每树最多5轮；强制全兴趣类型质量0、根遗漏至少1%总质量。最大浮点规范化差 \(1.11\cdot10^{-16}\)，未见正候选，时间约128秒。`cone-best-k7-m5-s184.json` 是发现状态，不是全锥对偶证书。
* seed183 的200树初始run也无正候选，但该进程启动时补集seed的Python异或索引括号尚未修正；其seed只是另一随机合法整数客户种子，不能按预期的横截补集种子解释。正式代码已经修正，seed184 run使用修正代码。

## 正在完成的有限 MILP run

`security_milp.py` 基于仓库 `tests/audits/cone_attack_joint_milp.py` 的全有序历史动作/传播/节点激励建模；归一化实际根 W=1，使用由根安全偏离严格得到的 M=m；另给每个静态竞争多重集加入 \(t\le\sum_a p_af_B(a)\)，目标最大化 t，固定安全查询p。全兴趣类型质量0由 SC-RED-FULL-INTEREST 支持。浮点 MIP 上下界均不是证明。

* 3人6主题、实际路径012、均匀查询，55秒时限：可行目标1/3，未发现严格BR候选；浮点剩余上界约0.36363636，故没有数值排除。580变量、4459约束，输出 `milp-m3k6-distinct-uniform.json`。
* 3人6主题、路径012、查询(10,10,10,10,21,21)/82，55秒；以及路径001、均匀查询，55秒，正在完成。完整结果在相应 `milp-*.json`，结束后补充本页。

## 恢复与下一步

代码都限定本目录写文件，不读凭据、不git提交。运行命令例如：

```sh
OPENBLAS_NUM_THREADS=1 python3 research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/bridge_attack/security_milp.py --k 6 --path 0,1,2 --seconds 55 --tag m3k6-distinct-uniform
```

需要新机制而非继续增加零反例次数。一个尚未测试的新菜单：混合全部在轨节点(i,a)的真实首次偏离终局去掉i后的竞争背景，是否存在一个共同分布将全部纯查询封顶在W/m。已有单个节点菜单失败不能直接否定该更大菜单；它若失败仍只否定菜单支持约束，不否定 BR。
