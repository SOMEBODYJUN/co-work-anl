# 真实跨树运输：本轮交接与精确候选检查

2026-10-24。对象始终是 Q-CAG-HALF 的任意人数、任意有限共同目录和每份完整历史纯 SPE。**本轮没有新增已证的全输入付款关系，没有完成 half，也没有反例。** 本目录只保存一次可复现的明确候选检查及尚缺的解析步骤，不把阴性计算称为一般进展。

## 1. Owner/SOURCE-NET 接口的实际状态

已读并从定义重构了 `boss20/route_flow/dual_owner_budget.md`、`boss20/clean_audit/owner_theta_audit.md`、`R-cd789.../round3/credible/owner_hybrid_transport.md` 和 `increasing_role_capture_flow.md`，以及 `R-b6d.../direction_review/continuation_general_scope/incoming_payment.md`。

已证的同叶 Hall 容量和同时 source 初始化支付没有被改动。尝试把一个强制叶中的真实捕获者 IC 留在其诚实历史，再拼回实际路径预算；未得到跨前缀比较。捕获者的 IC 只约束它自己所处有序历史中的行动和原策略后继。将此前的强制行动换回实际行动会改变它的前缀，因而旧叶中的捕获利润不能直接付实际前缀下的新查询。

没有将这种失败再包装成一个新的 flow/LP 等价式。现有缺口仍是：同一份实际 W 如何一次支付 incoming 重置费用，或者用更自由的查询预算绕过该重置。不同强制叶的 Hall 容量、旧利润、I 查询信用都没有相加。

## 2. 被明确检验的更弱逐人候选

候选为

\[
\tag{IP-OPT?}
(2m-1)u_i\ge\operatorname{OPT}_m
\quad\text{对每份完整纯 SPE 及每位实际玩家 }i.
\]

它弱于已失败的 `u_i>=v_m`，因为静态定理只给 `OPT_m/(2m-1)<=v_m`。若它成立，则对 i 求和得到 `W>=m OPT_m/(2m-1)`，所以它比 half 更强；它不能作为已证前提。

本轮仅用两个现有完整策略检验这个**同一一般候选**，没有另开固定人数正面结果。全部非空客户兴趣类型均可自由取非负实质量，总质量归一为一；固定的是原证书的每个有序历史上的行动。每个比较元组、每个历史 IC 都保留。

| 现有完整策略 | 自由类型 | 核查角色 | `max [coverage(T)-(2m-1)u_i]` |
| --- | ---: | --- | --- |
| `individual_security_failure`，m=3、6主题 | 63 | 第1、2、3位 | `-1/6,-1/6,-1/19` |
| `root_tax_failure`，m=4、6主题 | 63 | 第1位 | `0` |

这些数是对应**固定策略锥**内对所有 m 槽比较元组的最大值，不是一般模型的最大值。第一项保留56个无序比较元组，第二项保留126个；重复主题允许。前者每角色保留258条含自身动作的 IC，后者保留1554条。

浮点 LP 只提出证书。随后用 Fraction 核对每个返回的原始权重和对偶乘子。若目标系数为 `c_T`、全部原 IC 组成矩阵 Gamma，则对每个 T 检验

\[
w\ge0,\quad\mathbf1^Tw=1,\quad\Gamma w\ge0,
\qquad
\lambda\ge0,\quad \mu\mathbf1-\Gamma^T\lambda-c_T\ge0,
\qquad c_T^Tw=\mu.
\]

因此每个固定 T 的最优值及上表最大值都有精确有限证书。它们只排除了这两个指定锥内的候选反例，不能用于证明 (IP-OPT?)，也没有证明或否定动态门槛 SM/TB。没有继续增加实例或人数。

## 3. 原总人数不变时的准确归纳义务

若研究 (IP-OPT?)，可固定同一 m 人实例及

\[
t=\operatorname{OPT}_m/(2m-1)
\]

并在所有有序前缀上保持此同一个 t。对任意末位历史，固定前 m-1 个主题就是合法静态竞争背景；原静态比较给末位最佳回复至少 t。这一基底不切换到 `OPT_r` 或剩余者利润。

若 (IP-OPT?) 在某个有序节点失败，取深度最大的失败节点，则其每个严格后继决策节点的 prescribed mover payoff 都至少 t，而当前节点的全部 prescribed action-continuation 收益仍可至多为当前收益 `<t`。一般 induction 所缺的正是排除这个 threshold crossing 的新关系。这里没有证明这种排除；已失败的 `u_i>=v_m`、`u_i>=theta_m` 不能替代它。

root 另指出可尝试用同一静态对手 Q、同一最优比较负载 d 下的精确静态余项支付 crossing。已读 `R-3d253.../audit/background_static_security_remainder.md`；该余项来自指定比较和静态对手，不能从另一个真实叶或另一个 Q 借用。本轮没有证明它界住跨树负 reset。

## 文件与复跑

- `check_individual_opt_floor.py`：只重放上述两个既有完整策略锥的候选检查，浮点发现后逐项 Fraction 核对，输出只写本目录。
- `individual_opt_floor_fixed_cones.json`：来源证书 SHA256、全部比较元组的精确对偶乘子及达到最大值的原始点。

从仓库任意位置运行：

```sh
python research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/transport/check_individual_opt_floor.py
```

本次执行输出 `exact_primal_dual_checks=PASS`，四项最大 gap 依次为 `-1/6,-1/6,-1/19,0`。没有访问凭据，没有变更 git，没有运行 work.py，也没有修改共享数学正文。
