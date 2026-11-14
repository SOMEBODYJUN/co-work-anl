# CA-SECURITY-CONE-DUAL 与共同 Q 生成器：3A 数学审查

## 任务与阅读范围

本包对应 `customer-attraction-3a-3a-4f1d0dce96900444`。任务原定义的主对象是 `M-7656d999834541f2a815087f764149e3`（同一背景混合支付固定完整策略锥全部纯查询的 LP 生成器）；按 Boss 指定的比较重点，将其与 `CA-SECURITY-CONE-DUAL`（完整策略客户锥与不受限静态安全值的精确对偶接口）逐项核对。任务声明的 13 个阅读段（其中审查页重复出现一次）全部按原字节读取并核对 SHA-256；没有新增未声明依赖，故不需要 `map read-add`。

共同模型、固定策略对偶定理、共同背景审查页，以及 `cone_common_background.py`、`search_security.py`、`cone_optimize.py`、三份完整 JSON 报告、无损内容索引、重构 DAG、`verify_common_reports.py` 均已实读。源文件哈希与任务声明一致。

## 两个端点的精确数学内容

`CA-SECURITY-CONE-DUAL` 固定有限标签目录、人数 `n`、完整有序形式策略 `sigma` 与有理查询 `p`。令 `Gamma` 为沿 `sigma` 的全部真实历史偏离收益差行，

`K_sigma = { w >= 0 : Gamma w >= 0 }`，

其中同覆盖异标签、空覆盖、重复动作、独立离轨平局、所有有序历史及偏离后的真实后继都保留。因此 `K_sigma` 正是该固定形式策略成为完整纯 SPE 的全部客户质量锥。对静态竞争元组 `B`，

`beta_B(p)_T = (sum_{a in T} p_a)/(1 + number of B_j in T)`，

`W = c dot w`。定理对每个固定 `sigma,p` 给出精确等价：

`forall w in K_sigma: c dot w >= n min_B beta_B(p) dot w`

当且仅当存在静态分布 `Q`、非负历史偏离乘子 `lambda` 和非负余项 `r`，满足

`c - n E_Q beta_B(p) = Gamma^T lambda + r`。

`Q` 可以依赖 `sigma,p`，但必须一次支付整个锥，不能随 `w` 改变。无证书时，定理给出有理 LP 严格正见证；清分母后才是整数客户的真实聚合反例。该接口本身不声称普遍证书存在。

`M-7656...` 的生成合同固定同一完整 `sigma`，取 `L = lcm(1,...,n)`，并对全部纯查询 `a` 共同寻找一个 `Q` 和每个查询自己的非负 `lambda_a`，使每类客户类型满足

`c_T/n - E_Q b_{B,a,T} = (G/L)^T lambda_a + r_{a,T}`，

其中 `G/L = Gamma`，`r_{a,T} >= 0`。竞争背景枚举允许重复和任意相关；共同 `Q` 不观察本次查询。该方法的输出合同仍明确是生成器/冻结候选，成功状态为 `UNCERTIFIED_NUMERIC_CANDIDATE`，不是自动认证的定理。

## 已证的迁移边

若上述生成器条件被**精确**恢复（`Q` 归一、所有 `lambda_a,r_a` 有理且非负、全部类型恒等式通过），则对任意有理查询混合 `p`，逐查询恒等式按 `p_a` 加权并乘以 `n`：

`c - n E_Q beta_B(p) = Gamma^T (n sum_a p_a lambda_a) + n sum_a p_a r_a`。

因此生成器的共同 `Q` 条件给出 `CA-SECURITY-CONE-DUAL` 的 `T` 证书，而且对每个 `p` 都成立；内积任意 `w in K_sigma` 后得到

`W_sigma(w) >= n E_Q beta_B(p) dot w >= n min_B beta_B(p) dot w`。

再对 `p` 取最大值，得到该**固定策略锥**上的 `W_sigma(w) >= n v_n(w)`。这正是从共同-Q算法合同到 security-cone dual 下界/证书接口的充分特化，因而边记为 `conditional` 的 accepted `implies`。它没有承担 dual 定理本身的 minimax/Farkas 双向证明；双向证明仍由 `CA-SECURITY-CONE-DUAL` 自身承载。

## 不能迁移的部分及证据边界

1. dual 定理只对每个固定 `p` 要求存在一个 `Q_p`。它不推出一个同时服务全部纯查询的共同 `Q`；因此反向的“dual 已证，所以生成器共同-Q LP 必可行”不成立。
2. 共同-Q生成器也只涉及一个固定 `sigma`。它不量化所有完整策略、所有目录或所有人数；不能把有限候选外推为普遍 `forall sigma,p` 证书存在，更不能闭合一般聚合安全桥。
3. 现存数值输出不能替代精确证书。`common_n4_k6.json` 的原十进制 `Q` 归一和 378 项余数有微小误差；定义级有理重构把四人首个固定锥恢复为 `Q=(3/4,1/4)` 并通过全部 378 项非负余数，说明这是一个固定锥实例。`common_n5_k6.json` 的保存数字有 123 个负余数，分母上限重构也未通过；这只是该候选未认证，不是共同-Q不可行反例。`cone_n4_k6.json` 的 20 个终点全是 mask 63 的全兴趣客户、`W=OPT=1`、`v_4=1/4` 的等号点，不是普遍证书或反例。
4. `search_security.py` 的整数 DP 和 `verify_common_reports.py` 的重构确实保留了完整有序历史及真实后继；但程序合同没有把浮点 LP 状态提升为 exact proof，也没有运行本轮新 LP。`cone_optimize.py` 明确标注 `UNCERTIFIED_LP_POINT`。
5. security-cone dual 的下界是总福利 `W >= n v_n`。它没有逐人 `u_i >= v_n` 的结论；更不自动给 `OPT_n > 2W`，所以不能把本边写成 half 反例/定理或 SPE 逐人付款。

## overlap 处置

任务草案把 `M-7656...` 与 `CA-SECURITY-CONE-DUAL` 标为后续比较。上述线性组合已完全解决两者的可迁移逻辑：共同-Q生成器是 fixed-`sigma`、all-query 的充分特化；dual 是 fixed-`sigma,p` 的充要接口；两者之间没有反向蕴含。剩余的普遍证书存在性、五人候选的有理重解和一般 half 桥是各自开放的数学义务，不是尚未澄清的端点比较，因此在回执中记为 `closed_overlaps`，不虚构新的 3B 任务。
