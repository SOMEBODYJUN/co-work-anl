# 精确阶段Claim

本区Claim不自动进入共享canonical账本；一般Q-CAG-HALF仍OPEN。无外审或新颖性认证。

## B8-REFINED-ACTUAL-TAX-NO-v1

- **Exact statement / conclusion：** 存在CAG-MODEL实例和完整历史依赖纯SPE，使 `mM>W+G`；其中 `α=(m−1)/m`、`M=max_(T∈S) Σ_(x∈T)1/(1+αc_x)`、`G=Σ_(c_x>0)1/(1+αc_x)`。
- **Objects / domain：** 有限单位客户、有限非空共同主题目录、单位权提供者；本反例m=13，六个不同覆盖主题，36单位客户。
- **Quantifiers / assumptions：** 这是存在性反例，所示完整策略定义全部有序历史的最优行动，无平局限制。原全称桥对每个实例和每个完整纯SPE量化，故一个此类证书足以否定。
- **Definitions / scope：** 收益、福利与OPT沿用现行model.md。只否定固定实际缩放背景及其精确税充分接口；不是half、真正安全值或其他静态背景的反例。
- **Dependencies：** 原11客户coverage_opportunity_failure输入（新模型需重新证明完整SPE）；自动机逐行动封闭与逆序收益比较的自足归纳；有理逐客户代数。
- **Evidence：** 实际 `P^10 AAB`，W=33、OPT=36、M=3、G=708669/123025，违反量29481/123025。全部112050个自动机节点行动比较精确通过；每个历史的运行对应已查节点。盲算研究员独立重建BI及策略；root另外从单位客户直接重放并做负控。
- **Counterevidence / objections：** 未发现固定证书的fatal objection。任意k推广未证；不能将固定反例误称无限族。
- **Status：** 完整有限反例，发现者、独立研究员和root定义级内部核验；共享清洗/外审/新颖性未认证。
- **Related files：** `security/refined_tax_counterexample.md`、`security/refined_tax_k10_packet.json.gz`、`security/audit_refined_tax_packet.py`、`credible/audit_refined_tax_blind.py`、`credible/audit_security_packet.py`、`root_audits/check_automaton.py`与各自冻结输出。
