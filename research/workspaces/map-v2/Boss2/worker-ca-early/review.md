# 第三阶段审读：early-opportunity-count-and-alternating-price-saved-samples

任务 `customer-attraction-3a-3a-694c3cbd09cdfcf4`（3A），核心对象 registration pin `8c7aa36f6be8d6d2c2b84b1c056f71fc85d6978c23230b3771d960f01a6bb3cd`。本审读按任务声明的 15 个分段（含重复文件的两个精确区间）完成；13 个去重来源全部按声明字节读取并 SHA 核对。大 JSON 不是只看摘要：对四个 report 的字典/列表/标量和全部保存记录做了完整解析，另做了逐表整数 IC 统计；账本见 `reading-ledger.json`。没有运行发现器、原 LP、随机搜索或规范求解器。

## 模型、域和量词

共同模型是有限单位客户、有限非空**标签**目录及任意覆盖映射；允许空覆盖、同覆盖异标签、重复行动与所有有序离轨历史。m 名单位权提供者依次行动，终局客户在覆盖者间均分；完整纯 SPE 的 IC 量词是每个玩家、每个有序历史和每个合法替代标签，偏离后沿同一策略在改变后历史的真实后继。把客户按可接受标签集合压缩为非负质量只改变表示，不把完整历史策略自动限制为计数策略。

核心对象固定一个合法旧计数 b（根 b=0 是特殊情形）和完整计数动作表 α。对每个非叶计数 q（|q|<m）定义 α(q)，并递归 `end(q)=end(q+e_{α(q)})`、叶 `end(q)=q`。若客户类型为 B，终局中选择 a 的系数为 `1[a∈B]/sum_{j∈B}end(q)_j`（零分子为 0）。全部 q 和全部 b≠α(q) 的精确 IC 行

`Σ_B x_B( p_B(end(q+e_b),b) − p_B(end(q),α(q)) ) ≤ 0`

在完整键域上恰好等价于 `σ(h)=α(q(h))` 对该计数策略子类的所有对应有序历史都是纯 SPE。对 b>0，这只是固定合法前缀后的后缀 SPE；它不给旧玩家激励，也不等价于根 m 人 SPE。非零背景下后缀利润一般不等于完整覆盖，不能用 `R_b` 代替 W。

固定客户质量和固定 query 时的覆盖/价格目标是线性的 LP；price_alternating.py 先固定客户 LP，再固定返回菜单解客户 LP，属于局部交替提议，没有联合 x,z 全局最优或对偶证书。总客户质量 1 和价格目标玩家收益归一为 1 是两套不同归一。

## 全量有限证据的精确边界

四个保存报告共 395 张表（count_m5k6=100、count_m7k7=95、strong_count_m5k6=100、price_m5k7=100）。四 JSON 的全字段和全记录已解析；`saved-table-audit.json` 的两种恢复输入统计为：

* `encoded_decimal` 通过 146/395，计数状态 238020、非自身 IC 1386120，按计数等价代表 13630515 个有序决策历史。
* `limit_denominator_1000000` 通过 323/395，最坏负 IC 仍可能出现；通过只认证相应恢复的单表/单客户点和完整 α，不认证原二进制浮点输入、原 LP 最优性或整个策略锥。
* 分报告通过数（十进 / 限分母）为 count_m5k6 17/83，count_m7k7 46/68，strong 19/86，price 64/86。

限分母恢复的失败是实质的：例如 strong trial90 在 q=(0,0,3,0,1,0) 规定动作 5 对偏离 0 的精确收益差约 −3.77699474035×10⁻⁷；不能用“很小”或重新归一把它改成 IC。反之，通过点是有限实例证书：count_m5k6 trial4/97 给 W=1/2、u=1/10、覆盖 9/10；count_m7k7 trial61/69 给 W=7/11、u=1/11、差 −3/11；strong 的七个 `-0.0` 点满足 OPT₅−W=4u（系数 4 的等号家族），都不是系数一般定理。price trial0 是精确整数客户点、完整 330 动作和 1980 条 IC 通过，所存 z0=z2=1 给 C=6、τ=2、B(1)=4<W=5；这是固定实例的精确菜单值，不替其余 99 条成为全局最优或一般上界。

相关源也逐项核对：逐位置 path LP 只给同一路径的必要保底行，不能当完整 SPE；prefix 固定族的 330/1980 审计只认证该恢复点；合法背景/strong 保存锥仅给固定旧前缀或固定根表的有限点；整数全集探针的 4 根与 9 合法前缀全历史量词及其 37 节点证书和 180 价格点明确不授普遍预算。原审计/价格/1000+1000 随机探索均未重跑，旧报告中的“完成”仅为有限运行范围。

## 可交付的数学贡献和缺口

**contribution.result:** 固定完整计数表 α、完整合法计数键域、非负有理客户质量和全部真实后继 IC 行，确实给出该计数策略子类在相应有序历史上的纯 SPE；通过的恢复点可以统一清分母实现单位客户。固定查询/角色的目标值可作为该单点的精确算术证据；price trial0 的两标签查询还可精确证明该实例 `B(1)=4<W=5`。

**contribution.remaining:** 未证明所有完整历史 SPE 可计数化，未证明 `OPT_m−W≤m u_i`、系数 m−1/4、`B(u_i)≤W` 或六人 half；未给固定策略锥全目标对偶/全局最优。有限阴性和局部交替不能推出一般不等式。背景点未给旧玩家激励；逐坐标有理化失败点须换新有理质量并重验全部 IC，不能修饰原值。

## 边判断与 overlap

本任务 `read_object_ids` 为空。共同模型、path/prefix/background/price 程序和审计文件都是本核心的定义/实现/证据，不是独立已登记的端点；共享前提不造 hub 边。所有候选关系均在同一核心内部，且有限实验没有承担一般结论，因此本包不写 `implies`/`refutes`/`specializes`/`transfers` 逻辑边；coverage 为 `isolated-after-review`。

任务声明的 overlap：core `customer-attraction/early-opportunity-count-and-alternating-price-saved-samples` 与 peer `customer-attraction/early-individual-opportunity-path-relaxation-prefix-policy-cone-contract`，依据 `逐位置保底松弛与前缀族固定锥的原始合同--程序.md`，状态为 3B follow-up。该文件已实读；path 松弛的必要行（同一路径、未编码全部真实偏离）与本核心的完整计数 IC 不能直接互换，prefix 330/1980 固定点也不等价于本 395 表。需要后续的具体问题是：在保持“完整真实后继/全部有序历史”量词下，是否存在一条严格迁移或严格包含（以及哪些额外条件使其成立）。当前没有已发布 3B task ID，故不虚构 `follow_up_tasks`；receipt 中保留明确的待发布处置。

## 证据与 SHA

见同目录 `reading-ledger.json`，逐项列出 13 个去重来源、完整 SHA256 和字节数；核心/任务与所有 evidence SHA 均保持当前绑定。

## 完成状态

没有改源文档、registry、任务定义或他人文件；未 commit/push。最终收据写入 `map/receipts/customer-attraction-3a-3a-694c3cbd09cdfcf4.json`，边目录仅保留本审读报告。
