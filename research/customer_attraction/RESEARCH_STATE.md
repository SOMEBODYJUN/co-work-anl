# 当前前沿：一般顺序半覆盖

**Q-CAG-HALF**，存档 **customer-attraction**，状态 **OPEN**。没有任意人数、任意共同目录的完整证明，也没有经全部有序历史核验的目标反例。对象与量词见[模型](../current/customer_attraction/model.md)；本页按数学义务组织，不继承旧会话身份或轮次任务。

当前突破：恰五人已由[精确有理证书](../current/customer_attraction/five_player_half.md)证明半覆盖；完整类型域复跑及两路分工独立内审通过，未记录外审。旧五人松弛只作为历史方法边界。下一步主攻一般人数，六人用于检验参数化共同末位价格、隐藏回复投影及索引耦合。

## 已知范围

| 结果 | 准确边界与正文 |
| --- | --- |
| 三人锐 `5/3`，四人 `1499/750<2` | 任意目录、全部完整历史纯 SPE；[三人](../current/customer_attraction/three_player_sharp.md)、[四人](../current/customer_attraction/four_player_bound.md) |
| **五人半覆盖 `2W≥OPT_5`** | [精确证书证明](../current/customer_attraction/five_player_half.md)：53 正整数乘子、完整类型域；同一完整策略，任意平局、空/重复和零客户保留。内部独立审查，未记录外审；不含任意背景五人利润版或六人。 |
| 五人共享437行历史松弛约 `2.06169478572>2` | [原Claim与精确界](../current/customer_attraction/five_player_indexed_bound.md)，不把后来常数静默换进旧ID |
| 五人个人557行，独立全域对偶已审 | `β557=178528430822287579296070598592537012737/87421565922360356032366460363114422206≈2.042155490337931>2`；[独立审查](../workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_independent/full_pricing_review.md)支持任意五人共同目录/完整历史SPE上界。该独审不接受匹配primal最优性；远端前批已重放，本批只核原文和范围 |
| 五人个人728行，作者证书层 | `β728=903491829723556246762087795616829492745/442437259121664928475146048173419016656≈2.042078986560006>2`；[作者证书](../workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/README.md)、[父方审查边界](../workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_parent/README.md)未独立接受全域对偶。模板坏点均不是完整SPE或目标反例 |
| 无界人数的若干已解子类 | 至多六极大覆盖、层级关联、极端关联、受控分数覆盖、最优遗漏全私有、部分末两人路径条件；[逐项范围表](../current/customer_attraction/README.md#已有地基与未闭合范围)。条件仍承重，不外推一般目录 |

这些结果有各自的内部证明/审查范围；没有因本轮清理获得外审或新颖性认证。已有特例供引用，新研究仍面向一般人数、一般目录。

## 可直接复用的三条关系

固定一份任意完整历史纯 SPE，实际终局为 z，最终收益 u_i，`W=Σu_i`。

1. **真实全历史 IC。** 对任意有序历史 h、当前位置 i 和目录主题 A，令 Z_h 是原策略的规定终局，Z_(h,A) 是强制 A 后沿**同一原策略**的终局，则 `Γ_(h,A)=u_i(Z_h)−u_i(Z_(h,A))≥0`。后继全部可以改变；同计数历史可以采用不同续局。精确压缩须保存可实现续局全集，不能强制匿名平局。
2. **真实前缀预算。** 非空可覆盖比较集 C 有合法分数覆盖总重 τ≥1，r=m−i+1，`P_(i−1)=Σ_(j<i)u_j` 为实际同一终局的最终旧利润，则
   `|C|≤P_(i−1)+rτu_i`，因而
   `W≥|C|[1−∏_(r=1)^m(1−1/(rτ))]`。
   [完整证明](../current/customer_attraction/fractional_cover_path_budget.md)。最优并集可选总重 τ≤m 的覆盖，不能推出 half；m=5 只用此条件得 `W≥(6049/15625)OPT_5`，仍不过二。
3. **独立静态安全比较。** 定义 `f_B(A)=Σ_(x∈A)1/(1+c_x(B))`，其中 B 是 m−1 个合法主题的元组；`v_m=max_p min_B E_(A∼p) f_B(A)` 的 B 不观察查询抽样。已证 `OPT_m≤(2m−1)v_m`；[定义与证明](../current/customer_attraction/oblivious_security.md)。动态充分桥 `W≥(m−1/2)v_m` 及更强 `W≥mv_m` 均 **OPEN**。静态比较不自动支付真实顺序收益。

[一般工作稿](../current/customer_attraction/general_half_proof.md)串联这些关系及其他工具，问号处仍未证。[联合前缀席位预算（§3.1）](../current/customer_attraction/general_half_proof.md#31-冻结真实前缀的联合客户席位一般付款的精细加强)是有效强化；[真实孩子覆盖缺口（§3.2）](../current/customer_attraction/general_half_proof.md#32-最优首动作的真实孩子覆盖缺口不冻结后继的全范围关系)是保留信用的准确恒等式；水位是终局共同信用。它们各自尚无通用跨树付款，不能把等价重写算作新增福利结论。

新增[共同报价投影](../current/customer_attraction/priced_hidden_reply_projection.md)：对任意m、任意真源节点，以真实源IC、同一实际末位的全目录报价、共同K和分支真末位IC生成合法行；隐藏位可按人数排序精确消元。一般性有解析证明，六人全历史测试用于核验实现。它还未给出全m主闭合，也没有六人half证书。

另已提取[同源回复再查询](../current/customer_attraction/same_source_reply_requery.md)：任意余k≥3人的真节点可先强制T、再同源强制其真末回复C；保持C及交叉查询主题身份后，以七条非负行生成一般投影。隐藏位精确压成16(k−2)²候选；独立六人检查及指定旧387行点的严格分离通过。全m共同主权仍未找到；新44/60完整证书包本轮尚不可读，未作整包复跑。

## 承重缺口与按需来源

固定最优并集 O、实际覆盖 U，令 `L=|O\U|`、`E=|U\O|`，则 **`OPT_m−W=L−E`**。真正需要支付的是净差；不能只给遗漏半额付款就称 half，也不能丢掉 E。早期改一个主题会改变整段真实后继；核心缺口是跨互斥分支、不同查询或不同位置共同使用一次利润预算。

另有[近期机制来源补充](WORKSPACE_RESULTS.md#2026-10-25补充按义务选择近期来源)，含末位剥离、因果删除、时钟、signed价格与pair差；按义务再取用。

下列来源是可选择的接续工具，不是已经闭合的统一证明，也不是方法白名单。个人区材料按自身审查范围使用。

| 数学义务 | 已有可复用信息；仍缺什么 | 直接来源 |
| --- | --- | --- |
| 真实最优查询总支付 | 末位及倒二行已付；全体早期行的净残差未共同付清 | [动态查询信用](../workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_optimal_queries/dynamic_query_credit.md)、[倒二真实行](../workspaces/customer-attraction/R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md) |
| 安全值/完整路径菜单 | 静态比较、产品归约有效；合适查询与真实续局之间的相关性及跨位置付款未知 | [工作稿§5、§8](../current/customer_attraction/general_half_proof.md)、[PRODUCT-MENU-TIME](../workspaces/customer-attraction/R-4243b113e6fc4c25a197dec299f08049/parent/product_menu_time_obligation.md) |
| 同一查询跨历史合账 | optional未来负载截面有共同库存上界；不同query的整行总金额未付 | [同查询聚合组件](../workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/jointflow/same_query_history_aggregation.md) |
| 可信swap/bubble与signed流 | 合法真实孩子转移及signed差可望远镜；行动平衡、跨row source容量与diagonal余项尚未同时闭合 | [完整条件与残差](../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/GENERAL_PROOF_WORKING.md) |
| 反例编译与共同价格 | pooled-successor门槛、一次舍入及有限字典精确seed LP可用；尚无负种子，也无普适反向预算 | [共同门槛与seed LP](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/README.md) |
| 删除/水位/中继 | 同叶守恒和有条件可信修复可用；真实重置、旧玩家返还及跨枝共享信用未付 | [工作稿§6](../current/customer_attraction/general_half_proof.md)、[正确尾删除账](../workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/global/aggregate_tail_deletion_identity.md) |

## 不能复活的加强与下一动作

冻结实际前缀的 `P+λΔ≥freshOPT` 也已由[52客户真实根SPE](../workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md)反驳，不能把“新增覆盖＋后继总收益”当作已证归纳。

逐位置 `Mfull_i≤u_i`、逐人安全值、强弱 iid 福利桥、固定实际缩放精确税桥均已 **FALSE**；`M_path≤W/m`、真正 v_m 聚合与原 half 仍 **OPEN**。非根 relay 必须保留旧玩家利润变化。准确失败范围、反例与重试条件见[失败机制](FAILED_ROUTES.md)。

下一轮选一条仍开放的全输入义务，读其唯一正文与实际审查，新增能支付真实残差的关系，或构造真正目标反例。也可完全换方法。一般推导代 m=5 时须说清无条件结果与未证付款；不扩同策略锥阴性表，不把局部结果、文件整理或审查通过当作一般研究终点。

本页只给导航和现况。全 Claim 身份在[精确账本](../current/claims.md)，来源覆盖及本轮未重放范围见[清理记录](CURATION.md)。
