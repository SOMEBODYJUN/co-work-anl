# R-2fc independent_mechanism 四源复核

四个已认领源均在 `clean-show/` 返回 0 后全文读取，源字节、冻结提交、blob、大小和 SHA 保存在 `source-manifest.json`。这是对已有五客户障碍与任意 (k) 碰撞自由族的独立机制包；它们与 `global_proof` 的发现脚本身份不同，不能相互冒充。

## 源级处置

| ID | 文件 | 处置 | 内容与边界 |
|---|---|---|---|
| `9c88e282902193a10afc` | `audit_collision_free_spe.py` | integrated | 标准库 `Fraction` 独立审计四主题五客户策略；枚举根及四个末历史的 20 项比较和 16 个终局覆盖。|
| `765c3b41163d0e50febe` | `collision_free_spe_exact_audit.json` | integrated | 完整报告：`W=4, OPT=5`，实际 `(2,3)`，负载 `(1,1,0,1,1)`，`half_coverage_holds=true`。|
| `20c89386263335ea5d0b` | `root_collision_free_family_audit.json` | integrated | `k=1,2,3` 的独立有限摘要，分别 `(W,OPT)=(4,5),(6,8),(8,11)`。|
| `bac0e0159f6d432c8c0a` | `root_collision_free_family_audit.py` | integrated | 以类型负载公式、后向归纳和单位客户复核构造上述三端点；代码自身只运行 `k=1..3`，不能单独充当任意 k 证明。|

## 精确结果

五客户策略的全部历史比较均为有理数，指定根收益和末位收益均达到各自最大值，实际福利为 4，最优二主题覆盖为 5。实际没有负载超过一，因此任意规范化可加负载函数 `f(0)=0,f(1)=1` 在该实例的值都是 4；这否定该辅助桥，但 `2W=8>5`，不是 Q-CAG-HALF 反例。

独立族审计逐个检查 `k=1,2,3` 的所有有序历史与所有动作：`5/20`、`57/399`、`1111/11110`（历史/含自身比较），路径分别为 `(2,3)`、`(2,5,6)`、`(2,5,8,9)`，比率 `OPT/W` 为 `5/4,4/3,11/8`。该代码的“arbitrary-k symbolic family”标题不等于执行了任意 k；一般 k 的状态归纳仍由既有 Q/B 正文承担。本包只把有限端点的独立复放作为交叉证据，并记录 `2W>OPT`，没有推出一般半覆盖命题的真或假。

`validation.json` 为 `passed=true`；两个生成报告与冻结 JSON 逐字节相同，脚本 `py_compile`、stderr 清洁。未修改全局图，也没有把旧摘要、有限端点或独立脚本升格为外部新颖性认证。
