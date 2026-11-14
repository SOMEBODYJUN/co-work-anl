# 任务审读与数学范围：一位背景五人利润收费

任务：`customer-attraction-3a-3a-c78ccf1b61bc0ed1`

核心：`customer-attraction/one-prefix-five-profit-exclusive-charge`

核心 pin：`a12c836333e609725e285c501ac8b7ee8d28601e0e62dd699c10a3e0cab60aeb`

read-add：`degree-two-shared-customers-complete-spe-negative-stationary-flux-family`，pin `ead26a4f21f7e18c8edf9e4ae56d638dec34f9825819526618cf059eab1a651d`

## 读取范围

任务声明给出 60 个唯一文件、68 个有序 reading pass（同一大 JSON 的连续段按声明重复出现）。本轮按声明顺序读取全部文本，并对全部 JSON 做完整解析；SHA-256 全部匹配。唯一字节总数为 7,063,895；完整记录见同目录 `readledger.json`。对端 basis 正文已经随 read-add 纳入当前 task 的 `read_object_ids`，但其数学比较仍按声明保留到 3B。

## 数学判断

核心正文的量词是：任意有限单位客户、有限非空带标签共同目录、任意合法长度一历史 `Z`、其后五名提供者沿一份定义于全部有序历史的完整纯 SPE 行动；允许空覆盖、重复、同覆盖异标签、任意平局和零客户。对任意五个合法比较标签，比较重数保留重复。把物理收益和保证分母都统一加上 `b=1_Z`，冻结 53 条外乘子和所有原局部源权，在完整二元客户系数域中取隐藏变量最小值。

已证的整句是：

`R_Z(T_1,...,T_5) <= 2 V + epsilon E_Z`,

其中

`epsilon=62212762317811658581/1250000000000000000000 < 1/20`.

因为 `E_Z<=r_Z`，还得 `R_Z<=2V+r_Z/20`；若 `Z` 被五尾完全覆盖则 `R_Z<=2V`。该结论不要求首位在根上最优，且不把五尾新覆盖当作五尾利润。

## 证据核验

`shift_local.py`、`shift_certificate.py` 和 `verify_literal_and_bridge.py` 的完整代码与保存表逐一读取；独立字面检查报告 `ALL DIRECT WITNESS AND CHARGING CHECKS PASSED`。53-b 恒等式保留 `kappa=2264870/10^22` 共同 K 项；利润 6144×2 条件态中仅 b=1、实际尾全零的 32 格收费前为负，最小值 `-epsilon`，加入独占客户收费后全非负。覆盖模式另行全非负。

六删一 ROOT-6 账、11客户完整 SPE、单新增 Z 查询空区间、自由53及66行锥有理下界和 71 行根投影均已从保存正文/JSON/程序核对。程序输出也明确：

- 11 客户模板的删槽债务 `13/3` 大于 `2u_1=2`，但 `2W=12>OPT_6=11`；
- 66 行锥 `EXACT-LITERAL-66-ROW-LOWER-BOUND-PASSED`，下界约 `7.93164968486e-5`；
- 根桥 27 原子证书标注不是完整 SPE，不能当 half 反例。

## 对端比较与边界

二元共享客户构造给出参数化完整 SPE 的负驻留通量 `L-H=-(q-1)(b-a)/2`，但 `W=OPT`，统计量不是 `R_Z-2V`。只有 q=5 才与“一背景+五尾”人数对齐；当前 q=5/a=1/b=2 审计点的 `W=OPT_6=64`、root IC gap=0 且收费后 slack>0，只排除一处模板冲突，不支付全参数迁移。由于尚未逐合法比较标签建立共同端点和量词保持，本轮没有跨对象逻辑边。

## 未付义务

核心仍欠：任意背景零收费 BG5；从 ROOT-6 同时支付六个真实根偏离的 `D_W+s`、删槽 `Delta`、共同 `K` 和 `E_Z`；把六根五尾共同实现为同一完整策略，或给出满足全部有序历史 IC 的精确反例。有限 LP、固定点和方法锥下界均不替代完整 SPE。3B 需继续比较 q=5 degree-two 族中的根背景、五尾利润、比较税和独占客户。

## 执行边界

本轮只写任务指定目录中的 `one-prefix-five-profit-scope-boundary.json`、`support.md`、`review.md`、`readledger.json` 与任务 receipt；没有修改正文、registry、coverage 或 integration。未执行 commit/push/checkpoint/done。
