# Q-CAG-HALF：一般共同目录、任意人数的半覆盖

研究存档：customer-attraction；目标身份：Q-CAG-HALF。

**状态：OPEN，当前主攻。** 完整模型及目标身份不变；研究入口为[专题首页](../customer_attraction/README.md)，当前正面地基、缺口和已失败机制分别见[前沿](../customer_attraction/RESEARCH_STATE.md)、[命题](../customer_attraction/CLAIMS.md)、[失败记录](../customer_attraction/FAILED_ROUTES.md)。

## 精确命题

有限单位客户集 \(N\)，有限非空共同主题目录 \(\mathcal S\subseteq2^N\)，任意整数 \(m\ge1\)。所有提供者单位权，按固定顺序各选一次主题，观察全部有序历史；客户在最终覆盖自己的提供者之间均分价值。设 \(\sigma\) 为**任意完整历史依赖纯 SPE**，实际终局为 \(\alpha(\sigma)\)，则欲证

\[
2W(\alpha(\sigma))\ge\operatorname{OPT}_m,\qquad
\operatorname{OPT}_m=\max_{(T_1,\ldots,T_m)\in\mathcal S^m}
\left|\bigcup_iT_i\right|.
\]

全部离轨历史的最优性、任意平局、空主题、重复选择和零客户均保留。整数兴趣类型重数仅编码不同单位客户；不扩大到带权提供者、异目录或混合行为 SPE。定义见[CAG-MODEL](../current/customer_attraction/model.md)。

## 原文与本研究的身份

**Paper Fact：**[Deng 等，arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2)，§5 Theorem 5.2 给两人的 \(3/2\) 结果，Example 2 给一般人数趋近二的下界；§6 明确提出超过两人时 sPoA 上界二的猜想。本研究固定上述共同目录输入类，原文措辞与范围复核见[文献导入记录](../current/customer_attraction/literature.md)及[后续量词复核](../current/customer_attraction/literature_followup.md)。

文献下界家族使用一个覆盖 \(m\) 客户的大主题和 \(m-1\) 个互不交单位单例。某个完整 SPE 全选大主题，覆盖 \(m\)，最优为 \(2m-1\)，比为 \(2-1/m\)。这说明统一常数二若成立即不能统一改进；没有证明每个固定人数都达到该上界。

## 已有答案与剩余范围

- 任意目录、恰三人的[锐 \(5/3\) 界](../current/customer_attraction/three_player_sharp.md)已内部证明。
- 任意目录、恰四人的[\(1499/750<2\) 界](../current/customer_attraction/four_player_bound.md)已内部证明，未证锐性。
- 一般五人共享旧437行[\(\beta\approx2.06169478572>2\) 界](../current/customer_attraction/five_player_indexed_bound.md)尚未达到半覆盖；对应有限必要条件模板有[精确二以上障碍](../current/customer_attraction/five_player_indexed_obstruction.md)，该点不是完整 SPE。个人区另有[557行独立已审上界及728行作者证书](../customer_attraction/RESEARCH_STATE.md)，证据层须分开，均未达到half。
- [至多六极大覆盖、任意人数](../current/customer_attraction/six_maxima_joint_bound.md)已内部证明；[恰七极大、七人以上](../current/customer_attraction/seven_maxima_checkpoint.md)有完整来源证明与审查，五人和六人仍有明确缺项。
- [向日葵](../current/customer_attraction/sunflower_maxima_bound.md)、[层级关联](../current/customer_attraction/laminar_incidence_bound.md)类有任意人数锐界，其结构假设仍承重。

这些结果没有闭合一般目录、任意人数的量词。证明来源、现行重构、内审、外审、实现及优先权分别记录。

## 一般命题的承重义务

早期玩家改选主题后，所有后继可以改变行动。需要比较原策略在各**真实离轨分支**上的行为，建立对最终覆盖损失有效的共同支付、结构定理或其他全局机制。不能冻结后继、默认 SPE 终局为静态 NE、把有背景的剩余利润当总覆盖，或要求所有局部/前缀余额非负。

[现有数学接口](customer_attraction_general_handoff.md)给直接覆盖证书与候选聚合安全值桥。Boss 可以自由改方法，无需先接受某条路线。已失败的税、逐人保底和规定模板集中到[失败记录](../customer_attraction/FAILED_ROUTES.md)，不再在本目标页按轮次追加。

完成标准是覆盖本页全部量词的证明；若发现目标反例，必须给合法单位客户实例、完整纯策略及全部历史偏离核验。新增结构特例、固定策略锥证书或有限无反例搜索均准确保存为阶段资产，不称本题已解决。
