---
id: "customer-attraction/r18-gap-cone-lp-review"
kind: "review"
type_tag: "审查"
title: "R-18 缺口锥 LP 与静态机制审查"
status: "source-read-static-audit"
truth_status: "finite-fixed-cone-diagnostic; no-universal-gap-or-half-result"
review_level: "full-3012-byte-read; pycompile-only"
summary: "源脚本在随机产生的完整历史 SPE 策略锥上，以福利归一化和全部历史偏离不等式为约束，浮点 LP 搜索一个固定查询支持/动作的正缺口；有理恢复后只作固定锥候选验证。本批没有运行搜索，不把候选接口当定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_cone_lp.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_cone_lp.py"
  - "clean:7944ebe2f78952461d50:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_cone_lp.py"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R18-literature-gap-agent/original/gap_cone_lp.py"
  - "archives/customer-attraction/tools/evidence/R18-literature-gap-agent/manifest.json"
  - "archives/customer-attraction/tools/evidence/R18-literature-gap-agent/validation/py_compile.stderr"
related_objects:
  - "archives/customer-attraction/state/计算/固定策略锥精确证书与重放--计算.md"
  - "archives/customer-attraction/state/计算/直接覆盖弱匹配LP诊断入口与有限锥边界--计算.md"
  - "archives/customer-attraction/state/计算/静态CCE福利分离的初次策略锥证据--计算.md"
---

# 来源身份和处置

本批只处理冻结源 `7944ebe2f78952461d50`：
`research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_cone_lp.py`。`clean show` 导出的文件为 3012 字节，SHA-256 为
`aaa8553924cedc72a9e7f28f2b40ec7b50eb46211ec52f96370a32842247d3cf`；两个冻结提交的源字节相同。原件和清单保存在本对象的 evidence 目录，`py_compile` 通过。本批没有执行其随机/有限搜索入口，因此没有新增数值结果、反例或无违例证书。

源文件依赖 `tests/audits/customer_attraction_strategy_lp.py` 以及其中导入的 `customer_attraction` 包。仓库中已有该依赖的冻结副本和固定策略锥对象；本页只把它们作为比较和复现边界，不把其他源文件的数值输出倒灌为本源的运行结果。

# 代码对应的数学对象

设有 (p) 个主题、(n) 个提供者，客户类型由非空集合 (S\subseteq[p]) 表示，质量为 (w_S\ge 0)。一个完整纯策略给每个有序历史 (h)（长度小于 (n)）指定动作 (\alpha_h\in[p])。从 (h) 开始沿策略向后递归得到终局动作计数 (t(h))，根计数为 (q=t(\varnothing))。

对客户类型 (S)，若终局使用的主题集合与 (S) 相交，则该客户贡献一单位覆盖福利。根福利行是
\[
\omega_S=\mathbf 1[S\cap\operatorname{supp}(q)\ne\varnothing].
\]
若某一提供者在终局选择动作 (a)，其单位客户收益为
\[
\pi_{a,S}(q)=
\begin{cases}
1/\sum_{b\in S}q_b,&a\in S,\\
0,&a\notin S.
\end{cases}
\]
`payoff_row` 正是这条根终局收益行；它不把根收益误写成客户总值，也不对质量做概率归一化。

固定策略的完整历史 SPE 约束由所有 (h) 和替代动作 (a\ne\alpha_h) 产生：
\[
 g_{h,a,S}=u_S(\alpha_h,t(h))-u_S(a,t(h+(a,))),\qquad
 \sum_S g_{h,a,S}w_S\ge0.
\]
`StrategyCone` 去掉重复零行，组成矩阵 (G)。因此脚本优化的对象是一个**固定动作表的客户质量锥切片**，不是全部策略的并集，也不是直接在客户整数点上搜索。

# LP 目标和候选验证

给定大小为 \(\min(n,p)\) 的主题支持 (J\) 和一个目标动作 (a)，`coverage_row` 产生
\[
 v_{J,S}=\mathbf 1[S\cap J\ne\varnothing].
\]
脚本最大化
\[
 D_{J,a}(w)=\sum_S\bigl(v_{J,S}-\omega_S-n\pi_{a,S}(q)\bigr)w_S
\]
并施加
\[
 Gw\ge0,qquad \langle\omega,w\rangle=1,qquad w\ge0.
\]
代码通过 `linprog(-obj, A_ub=-G, A_eq=omega, b_eq=1)` 求浮点候选；负号只是把最大化改为 SciPy 的最小化。归一化的是根覆盖福利 (W=1)，不是客户总质量或静态均衡福利。一个严格正的 (D_{J,a}) 只表示该**固定策略锥、固定支持、固定动作**存在一个候选质量点，不能直接推出 (\operatorname{OPT}/W)、静态 CCE 下界或六人 half 结论。

浮点向量先按分母 (10^7) 限制转成 `Fraction`；若不能同时满足 (Gw\ge0) 和 (\langle\omega,w\rangle=1)，`recover_vertex` 只用浮点活动行加福利行做有理线性消元。恢复成功后再用最小公倍数清分母、除以客户重数的最大公因子，并由 `independently_verify` 逐个有序历史、逐个替代动作比较实际分摊收益。这个检查可以确认该恢复点在该动作表上是完整历史纯 SPE，但源代码没有生成 LP 对偶证书，也没有证明正目标在所有可行质量上的最优性。

候选输出还重建一个 `Instance`，报告 `welfare`、`optimal_welfare`、目标动作收益和完整动作表。因而它能把一个通过恢复的点变成可重放的有限实例；它没有把浮点 LP 失败、未恢复点或未达到正值的尝试写成反例。

实现中有两个必须保留的边界：

* `support` 只枚举恰好 (\min(n,p)) 个主题的组合，不枚举空支持、较小支持或所有主题子集；
* `for a,q in enumerate(target): if not q: continue` 把 0 号主题当作假值跳过，因此目标动作 (a=0) 从未进入 `optimize`。这是脚本的搜索范围限制，不能解释为数学上排除了主题 0。

# 主入口的有限量词

随机种子固定为 `6198922`。主循环只使用四组参数：

| 提供者 (n) | 主题 (p) | 轮数上限 | 每轮动作表来源 |
|---:|---:|---:|---|
| 3 | 4 | 100 | `ExactSPESolver` 生成的随机客户输入与最差终局 |
| 3 | 6 | 100 | 同上 |
| 4 | 5 | 60 | 同上 |
| 5 | 7 | 15 | 同上 |

每轮先从 `structural_seeds` 或固定取值集合 `[0,0,0,1,2,3,5,8]` 随机生成非空客户类型重数，再由 `ExactSPESolver` 取 `worst_outcomes()`，随机抽取至多两个终局，并用随机平局选择器生成一份完整动作表。随后枚举大小为 (\min(n,p)) 的 (J)，只对目标终局中非零的动作索引调用 LP。找到严格正的、成功有理恢复且通过完整历史检查的候选后，程序立即写 `gap_cone_counterexample.json` 并退出；如果整个有限队列没有候选，才在末尾写 `gap_cone_summary.json`。

所以“没有写出候选”只表示这四组参数、这些随机种子、有限最差终局和有限支持枚举没有触发正值；它不是对全部客户质量、全部完整纯 SPE 或全部支持的穷尽否定。反过来，写出的候选只覆盖一棵动作表和一个根福利归一化锥切片。

# 和已有策略锥/静态机制对象的关系

本源与[固定策略锥、可信续局和联合表示的精确证书与重放](../计算/固定策略锥精确证书与重放--计算.md)共享“完整有序历史 + 真实偏离行 + 非负质量 + 福利归一化”的底层形式；区别是本源只把 LP 结果用于一个支持/动作缺口候选，没有保存原/对偶坐标证书，也没有对固定策略样本做穷尽的 exact dual 统计。

它也和[直接覆盖弱匹配 LP 诊断入口与有限锥边界](../计算/直接覆盖弱匹配LP诊断入口与有限锥边界--计算.md)同属有限锥诊断，但后者额外引入匹配/平均桥约束并允许随机 (k,m)；本源没有 `match`、`strong_average` 或 `average` 目标，不能把两种脚本的负值/正值互换为同一个桥的证据。

与[静态 CCE 福利分离的初次策略锥证据](../计算/静态CCE福利分离的初次策略锥证据--计算.md)相比，本源的 (D_{J,a}) 是单个固定动作收益行和支持覆盖行的组合，未构造对所有静态偏离的乘子 (\lambda)，也未量化所有终局静态 CCE。它因此不能给静态 CCE 的普遍下界或福利替换结论。

# 缺口、可复用接口与接续

可复用的接口是：在一个已固定且可逐历史核验的纯策略上，用 (G w\ge0) 把客户质量筛到 SPE 锥，再把覆盖行、根福利行和单动作收益行组成显式线性目标。若未来要把它变成数学证据，应在小 (n,p) 上将 (G,omega,v_J,pi_a) 全部保留为有理矩阵，给出 LP 原/对偶证书，并明确 (D_{J,a}) 与要证明的福利或半覆盖量之间的代数关系。

当前未解决的关键点包括：全部完整策略而非随机最差终局的量词、所有支持大小、主题 0 的跳过、浮点恢复失败的处理、LP 对偶最优性，以及 `optimal_welfare` 与目标缺口之间没有写出可推出 half 的不等式。脚本没有证明或反驳 Q-CAG-HALF-6，也没有证明静态 CCE、弱匹配或一般安全预算桥。所有这些边界随本源保留，避免把“固定策略锥中的有限搜索入口”升级为全称定理。
