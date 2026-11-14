# Boss4 fresh-worker 数学复核：737 terminal dual/primal repair

- **任务**：`boss5-map-final-repairs-repair-7d327e4f2df08f26`
- **被替代任务**：`customer-attraction-3a-3a-faf81fb510d6f97b`
- **核心对象**：`cag-dual-terminal-737-exact-primal-and-full-type-dual`
- **当前 registration pin**：`15580782318ac4dc7937322618e16c81a097367225f6bb80827b01d6c266cf14`
- **任务文件 SHA**：`f9fcd6044b508edc443509bb38d026be2eaa666e399d93f146ef430719932592`
- **复核结论**：十个 declared reference 的数学字节均未变；737 exact result 应保留。变化在旧 receipt/coverage 的集成语义：旧包仍写成 `isolated-after-review` 与 “Root native validation pending”，而当前图已有 728↔737 canonical cross 及 HQR 定向 checks。旧 cross 的数学内容正确，但以单向 `implies/unconditional` 编码互不包含，需修复为两个有向 `checks/context` 关系或由 owner 退休旧封装并保留两条分离事实。

## 1. 输入新鲜度与改变量

### 1.1 十个 declared references

逐字节 `sha256sum` 与 repair task 的 `reading_refs` 全部相同：

| 路径 | SHA256 | 结果 |
|---|---|---|
| `archives/customer-attraction/state/计算/终端系统精确最优的七百三十七行双证书--计算.md` | `b92765a902a79015fc34c5c85ac2ff9333acf2a4377650761b1830b889b55479` | match |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` | match |
| `archives/customer-attraction/state/程序/终端列生成定价的双源条件分解与浮点保存--程序.md` | `2548aee6fc2ab4a41e2b2d52e511a20874c93df35714513f57a2038ae11e8d40` | match |
| `archives/customer-attraction/state/资源/直方图定价与父代复核的输入合同--资源.md` | `c2ee2ac2c4906c0a87d9f8fc45e2874c356c91ff9b1b5c83b1da02a4c521b543` | match |
| `archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/original/exact_optimum_primal_dual_terminal.json` | `1c7b256ee4e72c686bb8bb7db4ac2d199cc2890463bf7138cd2761f8756c62fd` | match |
| `archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/original/exact_dual_dual_terminal.json` | `ad85b8a1aad07e9e2a5630fff0bd166e785440bb57d5d91f4f716c74725e122c` | match |
| `archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/saved-737-check.json` | `e8cdae9b70c3480891cb39a3f421ca68041e83b64232b6a96dca6565fa69634f` | match |
| `archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/execution-record.json` | `841cea019af76a7ed8c9ac634a9ae04de7353ba1f08e2f54712d48411bbaeec8` | match |
| `archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/executed_check_saved_737.py` | `8a829051e4edc75940db6346b768ee698eef63187126f153165f59ab0fe5d622` | match |
| `archives/customer-attraction/tools/evidence/terminal-column-generation-pricing-primary/complete-field-check.json` | `d9ef1858a1ab545b036265c4f10c5878274fdd06ed08d04c8c816846f6363e46` | match |

核心 registry 记录仍为 version 1、`truth_status=proved`、body SHA `b92765...`; statement 仍明确写出 `737=717+20`、不含 728 的共同 OO、76 点 primal 与 57 权全型 dual。没有发现 object pin 或 declared evidence 的数学版本变化。

本轮只读验证还包括：逐字段解析 76 个原子并重算 bit/hist/d/menu 合法域、质量和 `W/O`；核对 saved replay 的 `737×76` 矩阵维度、88 个零 slack、57 个乘子键和 `I_r/D` 对应；核对当前 canonical cross 运行 `python work.py research edge-check` 返回 `edge-structure-valid-not-a-mathematical-verdict`。没有运行新的优化器或 SPE 搜索。

### 1.2 prior assets

repair task 声明的三个 prior asset 也逐字节匹配：

| prior asset | SHA256 | 处置建议 |
|---|---|---|
| `map/edges/customer-attraction-3a-3a-faf81fb510d6f97b/review.md` | `fecb9cb4e2eb0468374edc24942066109b94fa2605c279ea3d9f4038ac9719d2` | 数学正文保留；覆盖/交叉边段替换 |
| `map/edges/customer-attraction-3a-3a-faf81fb510d6f97b/support.md` | `20f2bb6900b8e2133e31ca9b3ab45f908feae87e361d1cef28c897a44a7d9b7c` | 737 证书、浮点边界保留；旧 isolated 语句替换 |
| `map/edges/customer-attraction-3a-3a-faf81fb510d6f97b/readledger.json` | `dcb3e1e80235cd73752ea1ff74e8cdb792154d6d726e2388ac03b7cda720ef36` | 按当前 repair 重新记载 canonical cross/HQR 读取和 supersession |

旧 receipt `map/receipts/customer-attraction-3a-3a-faf81fb510d6f97b.json` 当前 SHA 为 `8c4797c03f50a940271d50dc731dc2787fa7b744297250839e0a8b306974680d`；其中旧任务 definition pin `242c732b...` 是当时 claim 快照，而当前旧任务文件（随 `state/receipt` 回写）SHA 为 `87d87d2f5e78e4dace8378789f13006b1dc4b39254d86a56c8a65216b771b361`。这是队列/收据元数据变化，不是数学输入变化。旧 receipt 中 `isolated-after-review`、`Root native validation pending` 和 “无 endpoint comparison” 已与当前图状态不一致，应由本 repair receipt supersede；旧 receipt 作为历史保留，不当作当前 coverage。

## 2. 模型、量词、假设逐项核对

共同目录模型是有限单位客户、有限非空**标签**目录（同覆盖异标签及重复主题允许），五名单位权提供者按固定顺序依次行动，并观察所有先前有序历史。纯策略是每一有序前缀上的标签函数；SPE 量词包含每个玩家、每个合法前缀和每个合法单步偏离，并沿偏离后的真实续局完成。终局覆盖福利是客户并集，玩家收益按实际负载均分。737 页不重新构造目录标签、完整策略或每个离轨历史后继，只取真实五人 SPE 投影必须满足的终端必要信息，因此不能把终端质量点写成真实 SPE 或 `OPT_5` 见证。

每个 737 原子包含：

- 十个 membership bits `ABCDEUVWXY`；
- `AB_hist`、`AE_hist` 各 8 个 `(t,r,s)` 桶；`second_hist`（代码名 Sbranch）16 个 `(t,h,i,j)` 桶；每族总数 5；
- 三族共享 `t=1` 槽数 `d∈{0,…,5}`；
- `actual/second/third` 三个旧菜单 `(ℓ,h)`，满足 `0≤h≤d`、`0≤ℓ−h≤5−d`。

令 `w(a)=1_{A∨B∨C∨D∨E}`、`o(a)=1_{d>0}`。737 松弛为

\[
P_{737}=\{x\ge0:Gx\ge0,\;w^Tx=1\},\qquad V_{737}=\max o^Tx.
\]

前 717 行是旧保交叠/跨族系统；新增 20 行为

- `AB→AE` positions 1,2 的 D/O（4 行）；
- `AB→Sbranch` positions 1,2,3 的 D/O（6 行）；
- `AE→AB` positions 1,2 的 D/O（4 行）；
- `AE→Sbranch` positions 1,2,3 的 D/O（6 行）。

共同 `t` position 0 不在 single 行中。728 的 `AB→Sbranch` positions 2/3 **共同 OO** 不属于 737，因此不能写成“728 再加 9 行”或由行数推出包含关系。

全类型 dual 的假设是 1024 个十位掩码、6 个 `d`、AB/AE 各 792 个完整 histogram、Sbranch 15504 个完整 histogram，以及每族 4 个旧菜单角点；AB/AE 两 source 的签名同时固定。对每个允许原子必须逐型满足

\[
\rho(a)=\beta w(a)-o(a)-\sum_r\lambda_rG_r(a)\ge0,
\]

且 `λ_r≥0`。这一量词不是只对保存的 1141 列或 76 个正支持原子。

## 3. 737 primal 证据

原始证书 `exact_optimum_primal_dual_terminal.json`：

- `row_count=737`；76 个严格正有理 `exact_mass`；
- `W=1`；
- `O=\beta=`
  `913780818510707039481129588377221884004224809337659/447470471154075773671105653556364606136051881479274`
  `≈2.042103060239853`；
- 737 个聚合 slack 全部非负，恰 88 行为 0；
- saved replay 逐原子重算 76×737=`56012` 个系数，保存的 737 个 slack 逐值相等；每个原子的位、hist、共同 `d` 和三个菜单域均通过。

`exact_mass` 只给必要信息松弛中的非负质量；它没有给同一完整目录的标签实现、同一历史的共同后继，亦没有给真实最优五元组。

`saved-737-check.json` 的关键字段再次核为：`primal.rows=737`、`primal.atoms=76`、`zero_slacks=88`、`all_saved_slacks_match=true`、`original_main_LP_QR_recovery_CG_runs=0`、`wrapper_successful_invocations=1`。

## 4. 737 full-type dual 证据

`exact_dual_dual_terminal.json` 给 57 个正乘子。共同分母与 beta 分子为

\[
D=2237352355770378868355528267781823030680259407396370,
\quad
B=4568904092553535197405647941886109420021124046688295,
\quad \beta=B/D.
\]

原始 integer multipliers 与 rational multipliers 逐键相等为 `I_r/D`；`minimum_scaled_integer_residual=0`、`negative_columns=[]`、`full_pricing_nonnegative=true`、`score_contexts=47574`。saved replay 的 `dual_full_type` 使用 arbitrary precision object arithmetic，并与原 dual metadata 一致。

因此对任意 737 松弛可行质量 `x`，逐类型不等式求和给

\[
\beta W-O
=\sum_a x_a\rho(a)+\sum_r\lambda_r(Gx)_r\ge0.
\]

76 点给 `W=1,O=β`，故 `V_737=β` 精确成立。这个结论是**737 必要信息松弛的 exact optimum**，不是原博弈真实 `OPT_5` 或完整 SPE 定理。执行记录明确 `independence="shared-original-production-code arithmetic, not a second independent implementation"`；本次没有 LP、QR、recovery、CG main、BI 或 SPE verifier 新运行，故不要把 arithmetic replay 写成第二套独立定价实现。

## 5. binary64 发现快照必须与有理证书分离

`complete-field-check.json` 确认 1141 保存列结构有效、无结构重复、20 新行的 22820 个系数逐项等于原定义，但把保存的 binary64 `mass` 按实际二进制有理数代入时：

\[
W-1=-\frac{22055}{147573952589676412928}\ne0.
\]

20 条 single 聚合中有两条严格负：

- `crossfinal:AB:AE:2O = -903509/442721857769029238784`；
- `crossfinal:AE:Sbranch:1O = -419795/885443715538058477568`。

所以 binary64 CG 快照只能作有限发现/实现轨迹，不能替代 76 点有理 primal。任何把“1141 列 float 已是精确 737 可行点”的边或说明均应判为被否定；这不影响独立有理 76 点与 57 权 full dual。

## 6. 现有 object-related edges 逐项复核

### 6.1 `cag-exact-728-and-737-feasible-sets-cross`（当前 SHA `729a924acac2542aa7986d28ddf19578d0448904b80ef841e439648f3ea61d80`）

路径：`map/edges/customer-attraction-3a-3a-319e676fff137944/exact-728-and-737-feasible-sets-cross.json`；其 receipt SHA `f2552194fa0e2179b478095183f43871cc07be06fa56ac4b5153b6db45f26ec9`。

**数学内容是对的**：在同一 717 基底上，728 与 737 都是加行后的归一可行集。冻结 728 的 65 点满足 728 全行但其 `crossfinal:AE:AB:2O` 对 737 的精确聚合值为

\[
-11184644019172119707794458826327155614707/
55747094649329780987868402069850796098656<0,
\]

故 `P_728\not\subseteq P_737`。冻结 737 的 76 点满足 737 全行但其 728 独有 `jointfinal:AB:Sbranch:2O+3O` 值为

\[
-34835181401157636064926624409276654055302863422723/
447470471154075773671105653556364606136051881479274<0,
\]

故 `P_737\not\subseteq P_728`。两个扩展均严格收紧共同 `P_727`，现有 `crossed-terminal-rows.json` 还保存 727 点对各自新增行的负值。模板值的 exact order `V717>V727>V737>V728>2` 也正确；它不表示真实 CAG OPT/SPE 值。

**需要修复的是 edge encoding**：文件将双向“互不包含”写成单一
`kind="implies"`, `relation_mode="unconditional"`, `source_ids=[737]`, `target_ids=[728]`。单向 implication 不能表达上述两条相反方向的 set-separation；若按 schema 语义解释，当前 edge 的方向与其 `whole_result/contribution` 不一致。不能把整条数学关系判假，但不能原样继续作为 active `implies` edge。

推荐由 edge owner 任选下列安全方案之一：

1. 退休当前 `cag-exact-728-and-737-feasible-sets-cross` 封装，保留其数学文本作为历史，然后新增两个 `checks/context` edges；或
2. 将其改成明确的 comparison/context edge（source/target 同时列两端，`whole_result` 只写 “P728、P737 互不包含”），并重做绑定。

更稳妥的是方案 1，两个方向各自可审计：

```json
{
  "edge_id": "cag-737-point-violates-728-common-oo",
  "kind": "checks",
  "status": "accepted",
  "source_ids": ["cag-dual-terminal-737-exact-primal-and-full-type-dual"],
  "target_ids": ["customer-attraction/three-cross-family-terminal-templates-matching-exact-certificates-and-floating-traces"],
  "premises_mode": "all",
  "relation_mode": "context",
  "conditions": "同一五人必要直方图域、相同717行、W=1；728额外有AB→Sbranch positions 2/3共同OO，737额外有20条AB/AE single D/O。",
  "roles": {
    "cag-dual-terminal-737-exact-primal-and-full-type-dual": "76正有理点满足P737。",
    "customer-attraction/three-cross-family-terminal-templates-matching-exact-certificates-and-floating-traces": "其728系统定义目标独有共同OO行。"
  },
  "whole_result": "737的76点满足P737但使728独有jointfinal:AB:Sbranch:2O+3O的聚合值为 -34835181401157636064926624409276654055302863422723/447470471154075773671105653556364606136051881479274；因此P737不包含于P728。",
  "scope": "仅为两个必要信息松弛可行集的非包含检查；不比较交集最优，不构造SPE/OPT。"
}
```

```json
{
  "edge_id": "cag-728-point-violates-737-ae-ab-2o",
  "kind": "checks",
  "status": "accepted",
  "source_ids": ["customer-attraction/three-cross-family-terminal-templates-matching-exact-certificates-and-floating-traces"],
  "target_ids": ["cag-dual-terminal-737-exact-primal-and-full-type-dual"],
  "premises_mode": "all",
  "relation_mode": "context",
  "conditions": "同一五人必要直方图域、相同717行、W=1；728额外有共同OO，737额外有AE→AB position 2 的single O。",
  "roles": {
    "customer-attraction/three-cross-family-terminal-templates-matching-exact-certificates-and-floating-traces": "65正有理点满足P728。",
    "cag-dual-terminal-737-exact-primal-and-full-type-dual": "其737系统定义AE→AB:2O目标行。"
  },
  "whole_result": "728的65点满足P728但使737的crossfinal:AE:AB:2O聚合值为 -11184644019172119707794458826327155614707/55747094649329780987868402069850796098656；因此P728不包含于P737。",
  "scope": "仅为两个必要信息松弛可行集的非包含检查；不比较交集最优，不构造SPE/OPT。"
}
```

这两个建议 edge 需要由持有 728 endpoint 的 owner（当前 endpoint pin `cf619efbbeb49431c5e2ca98d5e939db45e34e65e15d1ba03d55e1d24205ca06`）完成最终 endpoint/evidence binding；本 Boss4 repair 不应伪造一次新的 728 full-object read。若继续复用现有 canonical edge，则至少把它标为 comparison/context 而不是 `implies/unconditional`。

### 6.2 HQR/actual-third 三条现行 checks 边

以下三条边均为 `kind="checks"`, `relation_mode="context"`, `status="accepted"`，方向和数学用途一致，**可保留**：

| edge | 当前 SHA | 作用 |
|---|---|---|
| `cag-actual-p7-separates-four-frozen-terminal-points` (`map/edges/boss5-terminal-hqr-cross-3b-fd17eddf65273af3/p7-separates-four-frozen-terminal-points.json`) | `ca4e625692f5eb1a7e673809a45a78a524fa957e2b57aa42a6617f6ac8a789db` | P7 共享旧字段上界逐一排除四个冻结终端点，其中含 737 的 76 点。 |
| `cag-7497-projection-violates-shared-terminal-1o` (`.../7497-projection-violates-shared-terminal-1o.json`) | `9af26903e3cc7566f2cb5025025f6c819493340c08052747ed20f0dc846d3b29` | 7497 投影保留 W/O 但违反 737/727/728 共用 `crossfinal:AB:Sbranch:1O`；含 737 endpoint。 |
| `cag-actual-p13-separates-four-frozen-terminal-points` (`.../p13-separates-four-frozen-terminal-points.json`) | `e87f79e9cc5800c3948df91b8cefa2ad15986d19af08206a239b4fdcd41c2075` | P13 共享实际 HQR 原行和根 IC 排除四个冻结终端点；含 737 endpoint。 |

三条边的数学 scope 都明确“不把必要点写成真实 SPE/OPT”；没有看到应退休或否定的内容。Boss4 仅需在新 ledger/receipt 中记录它们为已存在 canonical context，不重复发边。

## 7. prior assets 的逐项处置

| 资产 | 处置 | 具体理由 |
|---|---|---|
| 旧 `review.md` | **replaced（保留数学段）** | 737 模型、primal/dual、float 障碍和 SPE 边界均正确；替换其“本包无任何比较/isolated”及“canonical edge 仅检索不读”的表述，加入当前 cross encoding 修复和 HQR 现行边。 |
| 旧 `support.md` | **replaced（保留全部证书数值）** | exact 76/57 证书、双 source 分解和两条 float 负余项均可保留；补充 `P728/P737` 双向不包含的精确 fractions，并将 728↔737 关系降为 checks/context。 |
| 旧 `readledger.json` | **replaced** | 保留十个 declared refs 的完整读取与 SHA；新增旧 receipt/现行 canonical edge/HQR receipt 的审阅记录、当前 integration 状态和“未重跑独立 solver”的边界。 |
| 旧 `map/receipts/customer-attraction-3a-3a-faf81fb510d6f97b.json` | **superseded（历史不覆盖）** | 不改其历史 SHA；新 repair receipt 要明确 supersedes，纠正旧 `isolated-after-review`、pending validation 与 stale comparison closure。 |
| `cag-exact-728-and-737-feasible-sets-cross` | **数学内容保留、edge 封装需替换/重绑** | 两个负值和 exact order 均真，但单向 `implies/unconditional` 不能表达 mutual noncontainment；建议拆成上述两个 checks/context edges。 |
| 三条 HQR checks edges | **retained** | 当前 endpoint/evidence pins、方向、scope 与 737 object 一致；不重复发边。 |
| binary64 “精确可行点”解释 | **rejected** | `W−1<0` 且两条 single-O 总和严格为负；仅保留为 finite discovery/implementation evidence。 |
| “728=737+9”或任一自动嵌套解释 | **rejected** | 728 的共同 OO 不在 737；两个冻结点给出相反方向的严格负分离。 |

## 8. 建议的新 repair receipt 内容

建议新 receipt `map/receipts/boss5-map-final-repairs-repair-7d327e4f2df08f26.json` 至少包含以下语义（具体 schema/绑定由 Root 完成）：

```json
{
  "task_id": "boss5-map-final-repairs-repair-7d327e4f2df08f26",
  "supersedes": ["customer-attraction-3a-3a-faf81fb510d6f97b"],
  "coverage": {
    "cag-dual-terminal-737-exact-primal-and-full-type-dual": {
      "state": "linked",
      "object_pin": "15580782318ac4dc7937322618e16c81a097367225f6bb80827b01d6c266cf14",
      "comparison_scope": "737 exact self-certificate plus existing 728↔737 cross and HQR checks; no new independent 728 endpoint proof claimed",
      "reason": "737 exact optimum remains proved; cross mathematical content remains valid after replacing the mis-typed implication with two directional checks/context relations; P7/P13/7497 context edges remain accepted.",
      "edge_ids": [
        "cag-737-point-violates-728-common-oo",
        "cag-728-point-violates-737-ae-ab-2o"
      ],
      "reused_edge_ids": [
        "cag-actual-p7-separates-four-frozen-terminal-points",
        "cag-7497-projection-violates-shared-terminal-1o",
        "cag-actual-p13-separates-four-frozen-terminal-points"
      ]
    }
  },
  "follow_up_tasks": [],
  "closed_overlaps": [
    {
      "core_id": "cag-dual-terminal-737-exact-primal-and-full-type-dual",
      "peer_id": "customer-attraction/three-cross-family-terminal-templates-matching-exact-certificates-and-floating-traces",
      "reason": "Existing canonical evidence already gives both exact directional separations; no new 728 full-object proof is owed in this repair. Replace the old implication encoding or retain it only as historical context."
    }
  ]
}
```

若 Root 不愿在本 repair 中创建新 edge（因任务没有 `read_object_ids`），则将 coverage 保持 `isolated-after-review`，把上述 cross/HQR IDs 记为 `reused_edge_ids`/`canonical_context`，并在 `closed_overlaps` 明确“数学上已由现行 canonical edge 解决、未新增逻辑边”。**无论采用哪一分支，都不能继续把旧 `implies/unconditional` 作为双向不包含的唯一 active edge。**

## 9. remaining obligations

1. 737 exact optimum 仅覆盖声明的有限必要信息松弛；仍缺将 76 点实现为一个共同标签目录及全部有序历史的完整策略锥见证。
2. `O` 只有在另行给出真实五元组/标签映射并证明其为最优覆盖时才等于 `OPT_5`；当前 `O>2` 不反驳真实五人 SPE half。
3. 完整 CAG half 仍需独立的真实历史 IC、续局一致性和实际 `OPT_5` 论证；737 dual 不能替代这些条件。
4. 728↔737 交集本身没有新的 joint primal/dual optimum；现有 cross 只证明各自固定点的双向非包含及值序，不证明交集最优。
5. full-type replay 是共享生产代码的 arbitrary-precision arithmetic replay，不是第二独立实现；若 future claim 需要独立实现，必须另派任务。
6. 若采用两个新 checks edges，必须由 owner 用现有 728 endpoint pin、原 evidence pins 完成 edge-bind/edge-check；Boss4 不应把未声明的 728 全对象读取冒作本轮新读。
7. 任何后续增加 joint OO 或多菜单 rows，必须重新保存共同 tuple/联合负载向量；不能由本次双 source single-row 分解自动推出更强完整策略结论。

## 10. 最终判定

- **可保留**：737 v1 object、76 rational primal、57 full-type dual、全部十个 declared evidence、float 快照的“非精确发现轨迹”用途，以及三条 HQR `checks/context` edges。
- **需修复**：旧 receipt/coverage 与 old review/support/readledger 的 integration wording；`cag-exact-728-and-737-feasible-sets-cross` 的 `implies/unconditional` 封装。
- **被否定**：binary64 快照是精确 737 可行点；728 与 737 按行数自动嵌套；737 `O>2` 自动等于真实 `OPT_5` 或真实 SPE 反例。
- **不应否定**：737 exact relaxation 的数学结论和两个冻结点给出的双向 feasible-set separation；这两部分均有 exact rational evidence。
