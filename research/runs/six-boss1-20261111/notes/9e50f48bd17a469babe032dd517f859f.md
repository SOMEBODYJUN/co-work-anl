# 正式回流草稿交接

## 已完成的可审结果

唯一对象 ID：`M-a90ca74cfdc848cb8f628fac8dd35f0a`；version 1；lemma；truth_status proved。未申请新 ID。

拟正式正文：`archives/customer-attraction/state/引理/六标签真实第三源重查询与根收益投影--引理.md`。该路径在草稿交付时尚不存在，草稿席没有写入它。可审正文为本目录 `body.md`，SHA256：

`ea90cd908a69723b725225bdeee9fe9d95912b651d1359952fcbdc31ecaf41b8`

正文包括：任意合法两行动历史后的同一完整 SPE 真实四尾；九个真实预算、显式 Phi36/Phi30、完整矩区间及有符号质量付款；C36/C30、逐型增量与 actual 256 型提升；真正最大裸大小根条件下的 ROOT36、ROOT30 和同一第二尾容量反馈 ROOT30-CAP2；ROOT30 真实取等迫 K=O；全部十个原未缩放根预算与权、两质量自由乘子、容量权更新，以及三份 131 列身份。

附表列齐全部 128 型 m36/m30，并用统一正整数 S=2291851735510680 将三份根余项列为整数。附录 B 的 28 项 evidence 均为实际存在的原域模型、承重证明、精确输入/证书、状态或检查程序/输出，完整 SHA 已逐文件计算。其他源组合和全局求解字段明确不并入。

## 文件职责

| 文件 | 作用 |
|---|---|
| `body.md` | 可直接亲审的完整正文候选；其相对正文链接按拟正式目录编写 |
| `object.draft.json` | 单对象登记数组；model/statement/quantifiers/assumptions/scope/objections 完整 |
| `relations.draft.json` | 一条 ALL 联合 whole_result 关系建议；未 bind/accepted |
| `draft_exact_check.py` | 本草稿独立标准库 Fraction 重放；只写本目录，不运行任何旧构建器或优化器 |
| `draft_exact_check.json` | 本次重放结果及必要来源 SHA 清单；不是另立数学节点 |
| `SHA256SUMS` | 本目录交付文件的最终字节校验和 |

## 精确核验结果

`draft_exact_check.py` 运行通过。它从真实份额重建 320 个菜单/D 平均、C36/C30 各 2048 个新状态及各 128 个完整包络，并重建三份根付款的每个原子/u/K/O 列。与原根输入的十个承重未缩放行、冻结旧新证书及新增容量反馈证书逐项相等。

- C36 状态余项：1758 正、290 零；最小 a1−a0=113681/4。
- C30 状态余项：1786 正、262 零；最小 a1−a0=85250/3。
- ROOT30 旧零原子仅为 0、2、125，故真实取等有 p=o，得到 K=O。
- 容量反馈 delta=77334949597/572962933877670，在 o=1,y2=0 中唯一由 h=9 达到；新零型为 0、2、9、125。
- 三条根线分别核完整 131 列，K/O 保独立；未固定 O=1 来省略参数列。
- 优化器调用为 0；冻结 checker/builder 均只读，未导入或执行。

## 必须由 Main 完成的字段和动作

1. 亲审 `body.md` 全文及附表，确认根附加条件与容量比较域。ROOT30-CAP2 本身允许任意六查询并；只有 O≥K 时支配 ROOT30。原 half 仍 OPEN。
2. 决定正文最终内容后写入拟正式路径，并按实际写入字节计算 SHA。`object.draft.json` 的 `body.sha256` 特意保留为 JSON null；这不是缺失证据的伪 SHA。若逐字节复制本候选，则实际 SHA 应为上列值；若修改任何字节，必须重算。
3. Main可按实际审定状态更新正文 front matter 的 `review_level`。它现在明确标记待 Main canonical review；这类字节修改也需重算 body SHA。
4. 在关系草稿中补 Main 的实际 reviewer/status，并按现行串行流程生成最新 endpoint/evidence pins 与 review digest。当前 status=draft，不冒称已accepted。目标正文先实际写入并登记，再 bind/check；不要把草稿 wrapper 当作已完成 canonical edge。
5. Main按既有RUN和Git职责串行登记、构图、保存与推送。草稿席没有进行 Git、RUN、registry、canonical 图写入，也没有读取凭据。

## 数学身份与不提出的机械关系

推荐的联合来源为 `CAG-MODEL` 与 `M-e960d7f4ebca40a38760eb3ae044cc19`。前者具体支付全历史真实源 IC、旧源查询同一新尾的合法性、根 IC 和真实大小帽；后者支付真实末两人保交叠钱包及 M=6 的索引平均。关系以 ALL 联合支付目标 whole_result，不能删为模型定义单源 hub。

不把既有“最大主题真实尾部的根收益加强”v1 三条旧线当作本次必要前提；本稿没有改写该旧对象。一般 PAIR 索引聚合继续归旧 owner。31/25 源组合族继续归已有 portfolio。旧72发现锥的匹配最优性只属原系统，任意查询并的量词只由实际十个正权证明承担。没有新根锥最优性、SPE反例或 half 证明声明。

本草稿席无待解数学错误；本义务在完成候选与复核后停止，等待 Main 串行接管。
