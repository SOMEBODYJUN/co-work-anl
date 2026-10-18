# Root 递归 first/pair sparse-support Proof：完整读后攻击

2026-10-18，sol_global_certificate。读序：先仅据 statement 独立完成并冻结 Fisher–Yates 构造 a1e5c37ea049647dfcb59a3f2629cffa36a857e67180066fa913f3a6def8069b；随后 root 才释放另一机制。本文记录实际完整读取其 15 行作者 Proof 后的攻击，不能冒称未读作者证明。

实际全文对象：boss11_uniform_cardinality_pair_sparse_support_proof_v1.md，SHA256 f3d759b4a0e147ab215f2aa1c09f72aca5aeda687426a3adac3ce2643fc28274。本文没有运行软件。

## 1. 正确性与隐式 oracle 攻击

对固定父状态 (d,h)，左右块大小 a,b，合法 u 最多 d+1 个。每个子状态已输出至多 D_a、D_b 个真实定基数集合，故父候选并集可以显式列出，个数至多 (d+1)D_aD_b=O(d^5)。没有搜索未列出的 h-subsets。

给定 u，左右子 law 独立。左/右内部 first/pair 由子假设准确给出；跨块 pair 等于两个 singleton 边际之积 u/a·(h-u)/b。按超几何 u 权混合，正好是均匀父 h-subset 的全部 first/pair。这个论证只证明一个已有显式候选矩阵的可行性，没将目标 b 的 separation 偷换成 quadratic cardinality optimization。

甚至可以直接用已知子权和超几何权形成一个显式父可行权，再做有理消列；父见证本身亦有多项式候选数量，不存在需要展开指数对象的隐藏步骤。

## 2. 递归、总位与基本解攻击

固定二分树每层块大小总和为 d，深度 O(log d)；各块全部基数状态的数量为 O(d log d)，粗界 O(d^2) 也足够。若不缓存而逐父 h 反复递归，运行时间论证会失效，但原 Proof 已明确缓存每个块/大小，排除了此漏洞。

父目标的共同分母可取 q=d(d-1)（d=1 单独处理）。基本解最多 r<=D_d 个正列，取独立 r 行后，0/1 方阵的行列式、Cramer minors 与 q 给每个权 O(D_d log(D_d+1)+log d) bits。不是把所有子分母在整棵递归树无控制连乘。

如果先取普通有理 LP 的多项式位可行解再消列，每次可选 0/1 候选矩阵的基本整数 nullvector，其系数有 O(D_d log(D_d+1)) bits；共同分母每次仅乘一个整数系数，至多 O(d^5) 次，故中间位长仍多项式。输出基本权还有上一段更强的最终界。因此“能求小支持”与“能在总位多项式时间内求”在这里均已支付。

## 3. 边界与七态应用范围

d=1 没有 pair 分母；h=0,d 可唯一集合输出。非平凡父分块 a,b>=1，所以跨块 a,b 分母不为零。候选集合始终恰有 h 个标签，支持压缩不改变每个配置的实际行负载。

七态 K_v 的每类 C 固定，替换 uniform H-subset 只需匹配 singleton/pair；CY_l 也因 C 固定保持。总支持至多 6D_d。该行结论不替换共同 L 的高阶矩或所有全局 q2 证据；原 Proof 明确保留原 uniform law，这一身份正确。

结论：在 statement 的 poly(d) 而非 poly(log d) 复杂度合同下，完整读后未发现 fatal。该机制与我先前 Fisher–Yates 构造不同，但两者均是显式候选列的有理压缩；不作全局新颖性、一般调度算法或主目标完成的判断。
