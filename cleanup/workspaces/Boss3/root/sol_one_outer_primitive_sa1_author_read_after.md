# One-outer primitive-SA1：作者全文实际读后记录

审查者：`sol_general_repair`，2026-10-18。此前 Exact-first 独立重构已冻结为
`sol_one_outer_primitive_sa1_exact_first_reconstruction.md`，SHA256
`419df2115facfc2b8cbd976d7f3a3a94fed2dc707ab915f34be10f5d19c8ca94`，原字节不改。
parent 实际读完该记录后，才释放作者全文。现已实际全文读
`sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md` 的§1–7，预期 SHA256
`da4897a966e8b5e10299622c5f93d67b115f859d1ae8fc77bd29f8f7ce0aa571`。

**指定结论：** 作者所写的给定 rational full primitive-SA1 点到真实全组
\(V\ge\epsilon^2/4\)、完整 ordinary \(C_{\max}\le2-\epsilon^2/4\) 推导无 fatal。
这里审的是该限定结构与作者数学后端，不是作者程序实现、一般 multicore 算法或
degree-four PSD 合同。原 Exact 和独立重构的状态不被本读后记录改写。

## 1. Singleton 与同一条件点逐式核对

作者(4)由 own state 的 value 行乘原 claim 补 \(1-Z\)、box \(A\le1\) 乘 \(Z\)、
一阶 gate \(Z\le A\) 得 \(x_A=x_Z=Y_{AZ}\)，方向正确，需 \(\epsilon>0\)。
作者(5)再用 gate 乘任意原 \(F,1-F\) 与已为零的一阶 slack，确实给所有原条件下
\(Y_{AF}=Y_{ZF}\)。全部次数二，不借 triple，也不把 conditioned 点再条件化。

作者§3只选一次正 outer marginal；每个原 state value、gate、resource 行都乘同一个
outer primitive，故其 \(\mu_{js},t_{jsu}\) 处于同一个条件点。丢去其他外行 helpers
的 claims 用的是二阶非负，不能理解成丢去真实组；它们在§6统一恢复 home。home
singleton 的 pair equality 给 \(f_j\ge b_j\)，因此 weighted fallback benchmark
至少 \(\epsilon^2\)。与独立重构同一步骤，无 scope 差异。

## 2. 作者的均匀赢家后端与独立 CDF 后端分开

作者§4的随机算法按 helper 独立选 state/inactive，再以 \(t/\mu\) 请求资源，最后
在请求者中均匀给一人。给定某 helper 的 state 及自己的请求，其他 helpers 的请求
仍独立于它；请求者数 \(N\) 的期望至多一。整数不等式
\(1/(1+N)\ge1-N/2\) 在 \(N=0,1\) 等号、\(N\ge2\) 右侧非正，故给赢率至少
一半。加权后作者(11)正确。state norm-one 保 \(0\le q_j\le1\)。

作者§5用的是**Bernoulli-count 卷积 DP**：每个资源、每个 helper 的加权 value-request
质量 \(m_{ju}\) 乘其他 helpers 请求数的 \(\mathbb E[1/(1+N_{-j,u})]\)。在任意只固定
若干 helper states 的前缀下，其他 helpers 仍独立，自己的 value/request 与别人的
请求数独立，因此作者(12)的因子分解有效；同 helper 不同资源的请求相关性与按资源
求期望无关。显式 DP 是从 \(P_0(0)=1\) 开始，逐个其他 helper 更新

\[
P_{k+1}(\ell)=(1-r)P_k(\ell)+rP_k(\ell-1),
\qquad
\mathbb E\frac1{1+N}=\sum_\ell\frac{P(\ell)}{1+\ell}.
\]

每个前缀的候选 state/inactive 期望加权平均是当前期望，故选择最高值候选可确定性
保持下界。只考虑正概率候选，零 \(\mu\) 不除；inactive 的请求率和 value-request
质量均为零。全部 states 固定后，在有正请求概率的 chosen-state helpers 中取最大
\(w_jp_{jsu}\) 者，逐资源不小于剩余请求币及均匀赢家的期望；作者(13)方向正确。
若无人正请求则该资源原随机期望也为零，可不分配。

我的独立重构§4使用另一后端：虚拟 claims 的 **maximum weighted score CDF**，用
有限分值层的乘积概率算条件期望，最后给全部 chosen clauses 的最大分值者。
两者各自支持 1/2 常数，但不是同一实现。独立脚本
`sol_one_outer_welfare_backend_independent_audit.py` 及其32个 Fraction 小例只检查
**我的 CDF 后端**，没有运行作者 count-DP，不能转记成作者算法软件审计。本次对
作者 count-DP 是上式及其概率因子分解的数学实读检查。

## 3. count-DP 的总位复杂度

条件请求率是显式有理 \(t/\mu\) 或有限和；正 \(\mu\) 的倒数只增加有理编码长度，
不按数值倒数循环。对给定资源，count-DP 的每项是至多 helper 数个 Bernoulli 参数
的多重线性多项式；取所有参数分母的乘积作公共分母，其位长为参数位长之和。
所以尽管其语义可涉及指数多个 Bernoulli outcomes，卷积 DP 的状态数至多 helper
数、算术操作及中间有理位长均多项式。再乘 \(1/(1+\ell)\) 并求和，新增公共分母
可界为 helper-count 阶乘，位长仍为 \(O(n\log n)\)。各 \(m_{ju}\) 也来自多项式
个显式有理操作。对所有资源、helpers、候选 states 重算 DP 至多多项式次；精确
比较后确定性选候选，不用对数、无理数、随机失败率或隐式状态枚举。

## 4. 阈值、所有组与原任务核对

作者(14)由 \(q_j\le1\)、坏组值小于 \(\tau=\epsilon^2/4\)、weights 和一得
\(W_R\ge\epsilon^2/(4-\epsilon^2)\ge\tau\)，无方向错误。只保留高值 helpers 的
fallback bundles，outer 领取其 own homes；其他本行及所有外行 helpers 均领取
各自 homes。因为 homes 全局 distinct 且与 \(B\) 不交，fallback overlaps 任意也
不会妨碍该回填。没有 home 的辅助 core、多 outer 并行使用 \(B\) 均未被此证明覆盖。

每个真实组采用原 indexed state，原 selector 放其 root；只导出该 selected state
实际领取的正 incidence jobs，其余**全部原 jobs**留原 private，包括 unselected
states 的所有 positive jobs。未选 roots 总一，selected roots 为二减所领值，资源
机至多一枚 unit job；零 incidence 保 private time 零，unused resource 可空，重复
indexed state 不合并。因此输出确为完整普通合法 schedule。没有额外逻辑约束被
塞进实际调度模型，SA 只用于取得所需数值和选择输出。

## 5. 准确通过范围

- 已实际全文核作者§1–7、(4)–(14)、count-DP 因子化/位长、singleton 无三阶、共同
  条件行、全部组及原 jobs 回填；未发现 standing fatal。
- 既有独立 Exact-first 重构和 CDF 后端有限审计保持原身份；未执行作者 count-DP
  程序，也未穷举完整物理矩阵所有 assignments。
- 不替 root 尚待新 Exact 的“LP生成+阈值搜索+完整单outer近似比”自动背书；本次
  只审给定有理可行点的 frozen threshold deduction。一般 `UM-TARGET-v1` 仍 OPEN。
