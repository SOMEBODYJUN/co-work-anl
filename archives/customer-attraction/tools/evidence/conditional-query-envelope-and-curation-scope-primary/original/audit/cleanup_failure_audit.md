# 一般桥失败与开放接口：只读清理审计

2026-10-25。仓库 `/workspace/scratch/ad730879ba4e/co-work-anl`。已读根 AGENTS、CLEANER、CAG-MODEL、共享 FAILED_ROUTES/RESEARCH_STATE/general_half_proof 及下列实际来源；没有 Git、通信、凭据读取或共享文件修改。本报告是既有资产整理，不新增数学结论。个人草稿、内部审查、有限重放与一般证明严格分开。下文路径均相对仓库根。

**结论：Q-CAG-HALF 仍 OPEN。真正安全值强/弱聚合也维持 OPEN；但背景 GLOBAL、逐位置 Mfull、任意背景首两人桥的若干入口仍错误地标 OPEN。** 52 客户 GLOBAL 反例和 179 客户逐角色退款反例已在本次用禁写重放重新核验。其余表项按已读解析原文/原内部审查标级，不宣称本次全部证书均重放。

## 1. 需要实际修复的状态与最小盖帽

| 入口/位置 | 问题 | 最小修复，保留原证据 |
|---|---|---|
| `research/customer_attraction/FAILED_ROUTES.md`；`RESEARCH_STATE.md`；`RESULTS_LEDGER.md`；`research/questions/customer_attraction_general_handoff.md` | 52 客户“根 SPE 实际前缀”GLOBAL 致命反例只在 WORKSPACE_RESULTS 的个人区概述，未进入短失败桥/接续主入口，容易再派发同一整体归纳 | 增加一条硬停界：合法背景，甚至根 SPE 实际前缀，`P+λΔ≥freshOPT` 对每个固定实数 λ 都假。指向下文 S52；不改原 half，也不把它并成纯“首步余额可负”。 |
| `R-2fc8878b4bdd4328bbc1bcf1df8ca831/README.md:12,13,40`；`RESEARCH_STATE.md:7,16,17`；`CLAIMS.md:9,11`；`background_induction/README.md:9,25,32`（均在 `research/workspaces/customer-attraction/`） | 一般 `P+Δ` 整体式仍 OPEN、继续攻击；弱逐人 `u_i≥OPT/(2m−1)` 仍 OPEN；实际税 `mM≤W+G` 未盖帽 | 本 actor 根 README 顶部加状态勘误：S52 否定整体；零根保险族 m≥5 已否定更弱 `u_i≥OPT/(2m)`，故旧 floor 也假；13 人旧证书已否定精确实际税。各旧正文保留历史声明，链接此帽和准确反例。其真正 v 聚合仍 OPEN。 |
| `R-d22a706a03c5499d941a6a97f94128a8/README.md:50`；`induction/full_root_menu_mixed_obligations.md:3,15`；`tree/full_terminal_menu_interface.md:11` | 共享 general_half_proof §8 已撤销逐位置 Mfull，但仍把这两份标 OPEN 的稿作为“原唯一正文”链接 | 在个人根 README 及两源稿顶加窄勘误：逐位置 FM/Mfull≤u 已由真正零根保险族反驳；保留矩阵 minmax、静态充分归约和 Mpath 开放。不能只说旧 PB 反例“不在实际根”而继续把 FM 开着。 |
| `R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/README.md:7`；`R-ffea274483aa4105a317300038fe04ce/aggregate_security/README.md:3,7`；`R-7e9f44beea424d469713364afe7dd180/aggregate_security/README.md` 的 Open candidate 2 | 任意合法背景 `u_1+u_2≥2v_r(b)` 旧 OPEN | 各 actor 根入口加帽并在子入口提示：较弱 PB-extra `2v_(r+1)` 已有完整解析反证（PB，见下）；原实际前缀专用弱化没有因此失败。R-2fc 根索引的首两人候选也应限定域。 |
| `R-cd789330fc7141299ac491bbb3ffa420/CLAIMS.md:158` | 该旧条仍称空根自由 Mfull/actual-prefix 专用桥 OPEN；同 actor 根 README:7 已说明收到后续保险反例并停止 GLOBAL-extra | 无须覆盖后续轮次：在 :158 条目尾加“逐位置 Mfull 已被后续零根保险族关闭；全路径聚合另开”的窄注，避免从旧轮次复活。根 README 可加统一按最新精确反例校准的入口帽。 |
| `research/current/customer_attraction/dynamic_iid_debt_boundary.md:333`；`research/customer_attraction/WORKSPACE_RESULTS.md:35,50` | 前者结尾仍称“仍开放的全局义务”，后者夹写“与共享仍 OPEN 冲突”，但两处已有上方/后文明确纠正 | 属历史措辞歧义，不是未纠正数学真值。可换成“当时的全局候选；现已由弱 iid 反族否定”，保持恒等式/Farkas 归约；不要重新把弱 iid 列 OPEN。 |
| `R-ab4b3c24c8f949198e194dd45bb66105/mixed/next_general.md:3` | 首段“待独立审查”与根 README:25、mixed/README:9 的“独审完成”不同步 | 最小盖帽注明审查文件 SHA256 绑定范围，原文快照可保留。已审是等价/条件编译，不是强安全桥或 half 证明，也无反例种子。 |

共享安全值 OPEN 标签（general_half_proof §5、短义务、RESULTS_LEDGER:81–82）本次没有发现足够证据支持改成 FALSE。

## 2. 按数学机制合并的失败桥

表中“最小见证”指本轮适合接续复用的最短已存见证，不主张全局最少客户。

| 数学机制与失效的准确合同 | 可复用见证、原文/核验路径 | 保留什么；不能推出什么 |
|---|---|---|
| **冻结背景的状态信用丢失**：`P+λΔ≥freshOPT_k(b)`，任意合法背景，甚至完整根 SPE 的实际前缀 | **S52**：m4、6 主题、52 客户，根 ABAB，收益 8,9,8,9；实际前缀 AB 后 P17、Δ0、freshOPT₂18。`R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md`；完整树 `global_actual_prefix_complete_spe.json`；独审 `parent/actual_prefix_independent_review.md`、`audit_actual_prefix_independent.py`。本次 259 历史/1554 含自身比较全过。 | 此整体反例比 R-2fc 的 23 客户首步式反例强；后者只否定裸首步归纳，整体当时反而有正余额。S52 任意固定 λ 都无效，因为 Δ=0。不能否定零根 half、任意背景 2P 型预算，或保留过去收益/负载/分支信用的新状态。 |
| **遗漏需求算错或逐角色围栏**：纯遗漏 L≤W；遗漏半额 R≥L/2 被当 half；逐角色 `u_i+e_i≥Δf_D` | **O71**：两人6主题71客户，W35、唯一最优38、I2、L36、E33，故 L>W 但净差 L−E=3。原 `R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md`；并行同证书 `R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md` 及 `parent/audit_optimal_omission.py`。**RF179**：三人7主题179客户，实际 PAB，u=(34,35,38)、W107；唯一最优 ATQ=111，L72 E68，e=(34,0,34)，f_D=(0,36,72,72)，倒二 35<36。`R-b659ddeec819493bb10dc58441fa7b3d/refund/unique_optimum_refund_floor_counterexample.md`、`audit_unique_refund.py`、`unique_refund_audit.json`。本次重放57历史399比较全过。 | 净需求必须 `OPT−W=L−E`。R≥L/2 与 W≥R 只给 OPT≤3W，标量反推例不是 SPE 反例；审查在 `R-65d0f88edf3849b39ca5eb79760e970b/parent/route5a_independent_review.md`。RF179 只否定固定分账，存在最优 O 版本也假；跨角色共同退款仍可，余额 W+E−L=103。`Σ[Δf−u]_+≤E` 仍更强于 half、未证；允许全部利润和退款自由共池则 L≤W+E 仅是 half 等价改写。 |
| **把真实可观察分支替成静态均衡/独立基准**：SPE→PNE、最差 PNE/CCE 福利下界、强/弱 iid W≥Z 或 W≥(1−1/(2m))Z | 共享 `worst_pne_welfare_counterexample.md`：16客户 W15、全部 PNE16。`eight_customer_cce_welfare_gap.md`：8客户 W6、min CCE=544/87；原13客户 CCE证据另存，不是同一实例。`iid_security_and_flow_barriers.md §1.2`：多花瓣完整族，m20,J100，W40 OPT59，严格否定弱 iid；原 `R-d321c149379b425493c5e8a5e03c6f39/security/weak_iid_bridge_counterexample.md`、两路独审。 | static smoothness、`mv_m≤Z_m≤OPT` 保留。两种 iid 桥均已败；Z 不是 v。八客户真正 v₃=44/23，W−3v₃=6/23>0；多花瓣背景给 v≤2且W=2m。均不否定真正安全值聚合/half。 |
| **把逐人或逐步加强当总量**：u_i≥v_m、θ全员/聚合、每期/每前缀非负、M_i≤u_i、OPT/(2m) floor | 最短老逐人证据：`individual_security_counterexample.md` 的34客户完整三人 SPE，安全最优分布仍不能逐人付款。真正零根保险全族 `R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md`：m≥4 有 u₁=m/(m−1)<δ_(m+1)=3/2−1/(2m−1)≤v_(m+1)≤M₁；m5 为 5/4<25/18。m≥5 连 u₁≥OPT/(2m) 都假。独审 `R-e7c3c9a51d38458aa551eec469e04cf2/independent/mfull_insurance_scope_review.md`。局部债/负前缀另见共享 `security_chain_and_local_boundary.md`、`prefix_balance_family.md`。 | 不能用旧 PB “任意背景未证实际到达”替零根保险族开脱。保险族 W=2m、OPT=3m−2，M₁=2−1/m−1/[3(m−1)]<2=W/m，未否定 Mpath≤W/m。真正 `W≥mv_m`、较弱充分桥及总债条件仍未证；局部亏损允许跨角色补偿。 |
| **任意背景两人块/同 p 推送与自由菜单混同** | **PB**：`R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md` 和 `CLAIMS.md:88–97`。r2475，48,495,120客户，合法 singleton 生成背景，完整解析子 SPE，u₁=u₂=u<s≤v_(r+1)(b)，精确正分数已存；dynamic/credible/root 分工内审。**SP34**：`R-12bf6a96d24c48eca828620d6642e203/parent/extra_slot_independent_review.md`：34客户+空主题，D(pε)−G⁺(pε)=12ε²−ε，ε=1/24 时 D=21/16<G=4/3。 | PB 背景已覆盖全部客户，未证根实际到达；只关闭任意背景 PB、2v_r 及其逐背景 Mfull/WP 推论。SP34 只关闭全分布强付款 ΣG≤ΣD，弱 ΣG≤W 尚未败。Mpath、自由背景、同 p、r−1/r/extra 槽必须分开。 |
| **实际负载代理/全查询固定税** | 共享 `fractional_actual_load_counterexample.md`：m≥4 四主题族 W=m²、OPT=m²+1，(m−1/2)M>W。其 §5 恢复 `R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md` 的13人36客户旧完整证书，mM−W−G=29481/123025；全树自动机112050 IC。较新 `R-cd789330fc7141299ac491bbb3ffa420/round10/security/old13_alpha_one_tax_arithmetic.md` 另给 α=1 差37/66。 | 静态 `OPT≤(2m−1)M`、`OPT≤mM+W−G` 代数保留。四主题族本身没有击破精确税，应分别引用13人证书；真正自由静态安全值 v₁₃≤5/2、W33≥13v，仍被支付。不能凭代理值 M 失败称 v 失败。 |
| **丢掉同尾信用、后继返还、或只以 regret 修复删位** | `R-e05f01e191354b028004b433016ae1c9/all_big_completion_slack_obstruction.md`：m≥3，m客户大主题B与m−1个不交singleton，全历史选B，W=m、OPT=2m−1；删 ξ及η 的菜单加强最小坏差 `(m²−3m−2)/2+H_m>0`，m3=5/6。同区 `actual_root_deletion_upward_repair_obstruction.md`：删第二位，实际/逐层最坏 regret 分别2a/(m−2)、4a/(m−2)，但每份真删后 SPE 福利高a。`three_remaining_decorrelation_residual.md`：旧34证书两 IC 91/164、返还−113/164，净−11/82。 | 原完整恒等式和后继 IC 保留；固定比例削 ξ 仍失败（其余原系数固定）。只删η且保留全部ξ仍未证/未否定；保留ξ及η的全式只是目标重写。删位仅否定绝对C倍 regret 单独付款的上向合同；可加利润/退款/OPT边际。去相关负值不否定早期净 ROW。 |
| **无实际碰撞仍有离轨福利损失；势/span/模板不是非负付款** | `collision_free_occupancy_obstruction.md`：5客户 W4 OPT5，c∈{0,1}，排除所有 f0=0,f1=1 加性纯负载支付。任意人数族 W2m OPT3m−1 迫使普遍 f1≥3/2。`R-1740705e79f14baba6326b951a52152f/route1/potential_branch_obstruction.md`：4客户完整 SPE，W=OPT₃=4，势强制分支差−1/2；`coverage_moment_geometry.md` 的 span不提供非负锥。五人LP坏点、2of4−1/8、节点平均分离向量各未认证为合法 SPE。 | 不能调 f2,f3 修复无拥挤见证，也不能从 signed span 或 Farkas 等价得到普遍非负乘子。只排除写明模板，不可推 half 不成立/不可证明。 |
| **水位/删客户改变 IC，互斥子树信用不可免费合账** | `R-cd789330fc7141299ac491bbb3ffa420/round2/relay/review_waterfill_credibility.md`：53客户真 SPE、400历史/2800比较，真正阈值28481/2924；高尾保1时任一可行2/11<ρ<1均翻转孩子根及第三位IC，重选末回复也不能保原叶。 | 窄“高尾保持1”承重；放宽成全部高尾共同缩权有全c族正修复。统一可信缩尾还需全历史避非核心背景及实际谱条件；单叶水位、同枝prefix回推、同客户密度≤1均没有自动给跨全部历史同角色钱包容量。 |

## 3. 安全值“历史已反例但未恢复”的处理

较新 `R-a4671b9ccb664300b43d3216ce45c934/security_review/security_scope_and_optimum_projection.md §1` 明确记载：实际读取 `R-ab2c6df20538474c948f5f24e59437ee/` 后，只有任意背景逐人 extra-one 边界、末位完整菜单和 meta-Nash/minimax 静态差；没有空根真正聚合反例的参数与完整历史证书，进一步核对仅是口头候选。此应作为**待恢复线索**，不能抹成“历史从未声称”，更不能把 OPEN 改 FALSE。

本轮辅助只读检索共享/个人/history 也未找到精确原 CAG 聚合反例的输入、完整策略、安全值原始/对偶；这不是不存在反例的证明。已确认丢失目录入口 `R-acd97406d8c4409d962eab2adcdc520c/README.md:43–46` 只说旧 continuation_global/saturation/security 未物化，不能凭摘要制造结果；明确“旧聊天未恢复”的 `R-0f99797b33de46bfb498541a0bc5fae9/credible/two_theme_root_repair.md:7` 是+2根修复，不是安全聚合。

扩大模型必须单列：`R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/independent/concavification_theorem.md:135–159` 的单调DR匿名势完整SPE有 U28、v₃12，但其重复同主题关系直接不符 CAG；R-2fc DR 例也非 CAG。二者不能补足丢失的原模型反例。

## 4. 真正还开的接口，按需求/容量分开

1. **直接净缺口**：支付 `L−E=OPT−W`，并证明总可用容量≤W。只建容量或把需求换成 L/2 都不够。私人遗漏席位谱、联合前缀席位已给普遍有效下界，但全私有块空时退回旧分母，不能宣称共享遗漏已付。
2. **真正安全值**：`W≥(m−1/2)v_m` 或更强 `W≥mv_m`；等价全路径债务分别 `ΣD≥−v/2`、`ΣD≥0`。保留静态对手不观察查询抽样。历史反例未恢复前维持 OPEN。
3. **自由全路径 extra 菜单**：Mpath≤W/m；逐位置FM已败。`R-4243b113e6fc4c25a197dec299f08049/parent/product_menu_time_obligation.md` 只给其全实例成立等价于存在只依m的统一位置权λ；没有构造λ，也没有不相容真种子。
4. **最优客户投影**：R-a467 §2 的 `存在最优O：W≥(m−1/2)v_m^O` 是较弱充分候选；投影删O外客户不继承SPE，路径投影 regret≤E不自动支付跨查询安全债。只限查询支持到最优主题会破坏原静态2m−1常数，不可偷换。
5. **共同退款/真实树流**：RF179 的共享正缺额≤E是未证更强候选；更自由全池只是half重写。R-cd789最新 ROLE/OPT-coordinate/同客户源密度及共享凸菜单提供合法表示和局部容量，角色全部历史总额仍未付。
6. **exact-M累计**：`R-ab4b3c24c8f949198e194dd45bb66105/mixed/next_general.md` 已有绑定快照独审：真正强安全桥与“任意末位BR目标路径 Σ exact-M_i≥mv_m”精确等价，并给条件违例的显式有限编译。这里 exact-M 是强制动作后在**所有真实子SPE中取最坏收益再极大化**；不要与 actual-policy 矩阵 Mfull/Mpath 同名混并。无反例种子、无新付款、无half闭合。

## 5. 本次重放的可复现命令与结果

以下原脚本会写同目录冻结JSON。为满足本次只读约束，用 AST 仅删除 `write_text/write_bytes` 表达式，其他断言及原始证书读取原样执行；不改共享文件、也不覆盖冻结证据。命令在仓库根运行：

```sh
python3 - <<'PY'
import ast, contextlib, io, json
from pathlib import Path
paths = [
 Path('research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/parent/audit_actual_prefix_independent.py'),
 Path('research/workspaces/customer-attraction/R-b659ddeec819493bb10dc58441fa7b3d/refund/audit_unique_refund.py'),
]
class ReadOnly(ast.NodeTransformer):
 def visit_Expr(self, node):
  if (isinstance(node.value, ast.Call) and
      isinstance(node.value.func, ast.Attribute) and
      node.value.func.attr in ('write_text', 'write_bytes')):
   return ast.copy_location(ast.Pass(), node)
  return self.generic_visit(node)
for p in paths:
 tree = ast.fix_missing_locations(ReadOnly().visit(ast.parse(p.read_text())))
 capture = io.StringIO()
 with contextlib.redirect_stdout(capture):
  exec(compile(tree, str(p), 'exec'),
       {'__file__': str(p.resolve()), '__name__': '__main__'})
 print(p.name, json.dumps(json.loads(capture.getvalue()), ensure_ascii=False))
PY
```

实际结果：

- S52 源证书 SHA256 `d6c01c7f18969bbfee52c657075736b19feabe21ca04f75f3719b1a51438fa3f`；259历史、1554比较，最小IC差0；path0101，利润8/9/8/9，W34 OPT₄52；tail P17、Δ0、freshOPT₂18；全部断言通过。
- RF179：57历史、399比较，最小IC差0；path PAB，利润34/35/38，W107 OPT₃111；唯一最优ATQ；L72 E68，f=[0,36,72,72]，e=[34,0,34]，倒二差1；全部断言通过。

S52 最小原始数据指纹（主题序A,B,T,Q,R,S；mask→单位客户数）：`1:10, 2:12, 4:5, 8:5, 20:2, 24:2, 36:2, 40:2, 49:6, 50:6`。完整259节点策略必须继续由原JSON读，不应只转抄在轨ABAB。

上述两次重放核实具体证书，不把有限核算升为任意实例证明；其余已存全人数机制本轮仅按实际读到的解析证明与审查范围记录。
