# 本轮精确 Claim 与未闭合义务

主目标 Q-CAG-HALF 的对象、定义、全部有序历史与任意平局量词均依 CAG-MODEL，仍 OPEN。

## B7-PROTECTED-ROOT-OBSTRUCTION-v1

- Exact Statement：存在27单位客户、六个不同共同主题、两人、空背景根的完整纯SPE，
  实际收益(6,7)、W13、OPT2=14；某个最优并集D包含14名实际全部遗漏的客户；
  精确连续价格B_D(6)=2>max(0,7−6)=1。
- Objects/Domain/Quantifiers：有限单位客户和共同目录，存在性辅助桥反例；SPE包含全部七个决策历史。
- Assumptions/Definitions：均分收益、重复行动合法、纯全历史策略，无特殊匿名或有利平局假设。
- Scope/Conclusion：否定任意保护集两比较主题利润支付、每个最优并集遗漏支付及sharp保护价格；不否定一般half。
- Dependencies：仅CAG-MODEL。
- Evidence：完整手工收益表、发现者单位客户Fraction核验、另一研究员独立重构与精确程序。
- Objections：有其他最优组合B,T/B,Q，不否定存在某个最优组合的弱版本；一般GLOBAL尚未被本例反驳。
- Status：完整构造及内部独立审查通过；个人资产，未外审、未认证新颖性。
- Related Files：[正文](parent/protected_root_counterexample.md)、[发现者审计](parent/protected_root_audit.json)、
  [独立审查](background/protected_root_independent_review.md)。

其他分支按各自文件实际状态读取，未登记为已完成一般结果。

## B7-ACTUAL-PREFIX-GLOBAL-OBSTRUCTION-v1

- Exact Statement：存在52单位客户、六不同共同主题、四人、空根完整纯SPE，实际路径
  A,B,A,B、收益8,9,8,9、W34、OPT4=52；在实际前缀A,B后，尾部P17、Δ0、freshOPT2=18。
- Objects/Domain/Quantifiers：原模型完整全有序历史SPE及其实际合法前缀；存在性辅助桥反例。
- Conclusion/Scope：P+Δ≥freshOPT失败；同例对每个固定实数λ均否定P+λΔ≥freshOPT。
  未反驳空根half或任意背景半利润。
- Dependencies：CAG-MODEL；完整有限策略以规范全集BI构造，仅其显式证书承担反例。
- Evidence：完整259节点JSON，发现者与root互不导入的52客户Fraction全树重放，
  全部1554含自身比较/1295非自身偏离通过；根与fresh最优覆盖独立穷举精确核验。
- Objections：任意合法背景反例不足以自动推出实际前缀反例；这里已提供实际路径完整根证书，缺口消除。
- Status：完整构造及root独立内审通过；外审/新颖性未认证，个人资产未自动canonical。
- Related Files：[正文](background/global_actual_prefix_counterexample.md)、
  [完整策略](background/global_actual_prefix_complete_spe.json)、
  [root独审](parent/actual_prefix_independent_review.md)、[精确核验](parent/actual_prefix_independent_audit.json)。

## B7-RESPONSE-DEBT / 结构价格 / 共同客户正性

`security/extra_one_response_debt.md`给精确协方差债务及条件性全人数half，正在独立审查；
不声称该客户级条件对所有SPE成立。
`early_price/symmetric_singleton_price.md`给关联度正则价格及对称单占主题块预算，正在独立审查。
`coupling/parity_symmetric_difference.md`的CC-PARITY-1/2及CC-TRI-NO已由root解析独立重构；
见 `parent/parity_independent_review.md`。它们区分共同客户正性层级，不提供一般根福利支付。
