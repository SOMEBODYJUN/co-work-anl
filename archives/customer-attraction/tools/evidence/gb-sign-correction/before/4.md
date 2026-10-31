---
id: "customer-attraction/common-static-q-certificate-generator"
kind: "computation"
type_tag: "计算"
title: "共同静态 Q 线性证书生成器的范围与审计边界"
status: "algorithm-only-no-certified-output"
truth_status: "algorithm-read-no-output-certified"
review_level: "full-source-read-and-dependency-scope-audit"
scope: "固定完整策略锥；共同背景分布 Q；逐查询主题的锥证书；不覆盖任意策略或六人半覆盖全称命题"
summary: "该脚本把一个固定策略锥上的‘同一个静态背景混合 Q 同时支付所有查询主题’写成浮点 LP，并将结果近似恢复为有理数；源文件没有随附 common_Q 输出，因而本轮只确认算法和证据边界，没有声称任何证书成功。"
source_sha256: "c32d5a8ca340ddfdc6f3646f59b45261f779f87166b9e515d8e81d86d9321452"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/security-gluing-boss5/original/common_q_generator.py"
  - "archives/customer-attraction/tools/evidence/security-gluing-boss5/manifest.json"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/security_gluing_2026-10-10/common_q_generator.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/security_gluing_2026-10-10/common_q_generator.py"
related_objects:
  - "../定理/完整策略锥的静态安全值对偶--定理.md"
  - "../障碍/固定安全预算锥的五个失败实例--障碍.md"
  - "../../tools/evidence/iid-conditional-cone/original/evidence/certificates/customer_attraction/iid_security_conditional_36.json"
---

# 对象与原始代码

源文件 `common_q_generator.py` 的 SHA-256 为
`c32d5a8ca340ddfdc6f3646f59b45261f779f87166b9e515d8e81d86d9321452`，库存中的源版本来自两个相同路径的冻结提交。正文和证据目录中目前没有与它配套的
`common_Q_<name>_<i>.json` 运行输出；旧源所引用的 `attack` 模块也不在该源目录中。因此这里清洗的是算法语义，不把历史源代码误写成已执行的数值证书。

脚本从外部模块导入 `cone` 对象、`F`/`np`/`linprog`、`load`、`OUT` 和序列化函数。它预期的字段是：

* `cone.m`：查询主题数；
* `cone.k`：客户兴趣类型（非空主题掩码）数；
* `cone.Bs`：允许作为静态竞争背景的有序元组列表，数量记为 `nb`；
* `cone.Frows[j][a][k]`：背景 `B_j` 下查询主题 `a` 对客户类型 `k` 的单位客户收益系数；
* `cone.rows`：固定完整有序策略的 SPE 激励行，数量记为 `nr`，每行按客户类型给系数；
* `cone.u`：待证明支付上界的目标向量列表，每个目标 `target[k]` 是某个目标玩家（或外部加载器定义的目标）的每类客户收益系数。

最后一个字段的玩家标签和 `attack` 中的构造没有在本源文件内定义，不能仅凭本文件把 `enumerate(cone.u)` 的索引称为第几位玩家。

# 线性证书的准确含义

对固定目标向量 `u`，脚本为每个查询主题 `a` 引入一组独立的非负乘子
`lambda[a,r] >= 0`，但令所有查询共用同一个背景分布
`Q in Delta({B_j})`。它试图满足每个客户类型的恒等式

\[
u_k-\sum_jQ_jF_{j,a,k}
 =\sum_{r=1}^{nr}\lambda_{a,r}\,G_{r,k}+r_{a,k},
\qquad r_{a,k}\ge0 .
\]

其中 `G_r` 是 `cone.rows` 中的真实 SPE 激励行。因而只要客户重数向量
`w >= 0` 满足固定策略的全部激励约束 `G_r dot w >= 0`，内积后便得到

\[
u(w)\;\ge\;\sum_jQ_j f_{B_j}(a;w)
\quad\text{对每个查询 }a.
\]

同一个 `Q` 同时控制所有纯查询，故对查询混合 `p` 仍有

\[
\max_p\min_B\;\mathbb E_{a\sim p}f_B(a;w)
\;\le\;\max_a\mathbb E_{B\sim Q}f_B(a;w)\;\le\;u(w).
\]

这是一种固定策略锥上的静态安全值上界证书。若 `cone.u` 包含每个在轨玩家的系数向量，则每个目标分别给出 `u_i >= v_n`；若加载器还提供了福利/聚合目标，则相应的证书只对那个外部定义的目标成立。源文件自身不构造 `cone.u`，因此不扩大该语义。

# 程序如何求解

`common(cone,target)` 构造变量顺序为

\[
(Q_1,\ldots,Q_{nb},\lambda_{0,1},\ldots,\lambda_{m-1,nr}).
\]

不等式矩阵有 `m*k` 行：第 `(a,k)` 行对 `Q_j` 放入 `Frows[j][a][k]`，对第 `a` 个乘子块放入 `cone.rows[r][k]`，右端为 `target[k]`。另有一条等式
`sum_j Q_j = 1`，全部变量设为非负；目标函数只最小化乘子总和，不最小化或最大化 `Q` 的质量。该目标只是求一个稀疏或易求解的可行点，不改变证书逻辑。

`run_common()` 只尝试三个外部命名的固定案例：

* `aggregate_theta_failure`；
* `root_tax_failure`；
* `global_decorrelation_failure`。

每个案例对 `cone.u` 中的目标逐一求解，并预期把结果写成
`OUT/common_Q_<name>_<i>.json`。失败时只写 `{success:false,status:...}`；成功时保存浮点目标值、背景支持、每个查询的非零 λ、逐类型 residual 和 `exact` 标志。

# 有理恢复与严格边界

求解器使用 SciPy 浮点 `linprog`。返回向量的每个分量再通过
`Fraction(float(x)).limit_denominator(10**8)` 转成有理数，然后以恢复后的有理向量重新计算 residual。只有同时满足 `sum(Q)==1`、所有恢复分量非负以及所有逐类型 residual 非负时，输出才标记 `exact=true`。这是一个有用的后验筛选，但不是浮点求解器本身的证明：

1. 分母上限 (10^8) 可能错过存在的有理证书；
2. 浮点 LP 可能因退化、容差或尺度问题漏报可行点或给出不稳定的支持；
3. `exact` 只重算该脚本恢复出的有限等式，不检查外部 `cone` 的策略覆盖全部有序历史、不检查 `cone.Bs` 是否覆盖了所需的合法背景集合，也不独立重建 `Frows` 和 `cone.rows`；
4. 源文件没有保存原始 LP、求解器版本、输入 cone 指纹或输出 JSON，故无法从本源追溯一个具体数值证书。

因此，本源的正确处置是“算法来源/有限证书生成器，尚无可认证运行结果”。若后续取得输出，必须同时保存输入策略、所有有序历史的 `Gamma` 行、背景元组列表、Fraction 重算脚本和 SHA-256；只有 `exact=true` 且逐行独立核验通过，才可把它并入固定策略锥对象。

# 与既有对象的关系

已有[完整策略锥的静态安全值对偶](../定理/完整策略锥的静态安全值对偶--定理.md)给出了更一般的 Farkas/minimax 等价：对固定策略和固定查询分布，存在 (Q,lambda,r) 的充要关系。此源尝试的是更强、更具体的接口——同一 (Q) 对所有查询主题同时工作，并且目标向量 `target` 固定。它不是该等价的证明，也没有把任意策略或任意 (p) 的证书构造出来。

已有[固定安全预算锥的五个失败实例](../障碍/固定安全预算锥的五个失败实例--障碍.md)记录了固定策略和特定安全分布下的负预算；那些负值只否定指定预算接口，与本源允许任意静态背景混合 (Q) 的证书问题不同，不能互相替代。已有 `iid_security_conditional_36.json` 则是固定 36 客户策略、固定均匀 iid (q) 及其对称 Nash 权重锥的条件证书；它不是本源的共同 (Q) 生成结果，也不覆盖全部客户锥。

若某个固定案例最终取得共同 (Q) 的 exact 证书，它最多说明该案例指定完整策略锥中的所有非负客户重数都满足相应的静态安全上界。它不能推出任意完整纯 SPE、任意共同目录、任意人数的聚合桥，更不能直接推出当前六人目标“每份完整历史纯 SPE 覆盖至少达到最大覆盖人数一半”。反之，某个案例 LP 失败也只表示这一证书模板或这组固定策略的失败；要构造主目标反例，仍需给出真实完整 SPE 的客户实例、全量有序历史激励核验和 ‪OPT>2W‬。

# 本次复核与接续命令

本次先通过 `clean show b6621c0eab4c5bcda04a` 导出并逐行阅读源文件；确认其 SHA-256 与库存记录一致。对导出的独立副本执行了 Python 语法编译检查。由于 `attack` 依赖、固定 cone 输入和 `common_Q_*` 输出不在本源或当前工作树中，本次没有伪造运行，也没有把历史摘要当作输出。

后续若补齐依赖，最低复现步骤应是：

```sh
python3 common_q_generator.py
```

随后先检查每个 JSON 的 `success` 与 `exact`，再用纯 `Fraction` 重建每个 `(a,k)` 等式、验证 Q 在 `cone.Bs` 上归一且非负、验证所有 `cone.rows` 对应真实完整有序历史，最后才按固定策略锥语义归档。当前源保持 `in-progress`，不登记 `done`。
