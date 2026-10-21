# Boss5：一般顺序客户吸引半覆盖

发布身份 `R-18e993ca519949aba29e030d3d7b15b3`，存档 `customer-attraction`，独立 main clone。本轮唯一主目标 **Q-CAG-HALF 仍 OPEN**：任意有限共同目录、任意人数、全部历史依赖纯SPE，2W≥OPT_m。根模型与 canonical 状态以共享研究文件为准。

## 已产生的可接续资产

- [利润机会单步支付的发散系数障碍](dynamic_induction/profit_opportunity_boundary.md)：同一合法大主题下界族，在空背景真实根节点否定任意固定有限系数 α 的 `F_m(0)≤αu_1+F_(m−1)(1_A)`。精确差额 `min_(1≤j≤m)(j+m/j)−1`；平方人数给 `2√m−1`。仅为方法边界，原半覆盖仍成立。原作者全历史 Fraction 审计和Boss5独立代数审查均已通过；尚未外审、新颖性未认证。
- `terminal_balance/`：主线程提出并以完整五人SPE否定末位单独支付条件 `(m−1)u_m≤W`，再否定加入实际税项后的 `m u_m+τ≤2W`。`failure.json`、`refined_failure.json` 有完整输入与策略；两份probe为可复现发现脚本，暂为个人探索记录，待结构化/进一步独审。
- `literature_mechanism/`：一手文献条件核查及 `W_SPE≥min_PNE W` 的独立完整反例，作者与global_proof交叉审查中。不能用一个福利更低的静态NE转接所有SPE。

## 活跃的一般目标路线

- `global_proof/`：直接证明、跨分支复制，重点较弱逐人候选 `u_i≥OPT_m/(2m−1)`；尚未证明或反驳。
- `counterexample_search/`：完整策略锥相邻面攻击、五人必要条件坏点的真实策略落地；所有有限无反例只作有限观察。
- `dynamic_induction/`：已保存局部利润机会障碍后继续允许跨节点欠债的非局部势。
- `strategy_duality/`：全历史乘子与跨节点流；并探索所有根终局能否由计数依赖SPE实现，尚无一般结论。
- `aggregate_security/`：真正安全最优查询分布的聚合补偿预算；逐人安全值和全分布预算的旧失败不会被重新当作定理。
- `literature_mechanism/`：弱逐人最优缺口支付候选与 coalitional smoothness 导入边界。

六名子代理均由本对话汇总，不设独立发布身份。当前所有候选、有限观察、个人备份都不自动提升canonical状态。

## 中断后如何接续

先读项目根四入口与本题前沿，再读本页及各子目录说明。实际未闭合义务仍是利用完整可信离轨回复控制跨分支的总福利。不能用冻结后继、逐步非负、静态NE替代或有限锥证书冒充一般证明。保存完成以根work.py checkpoint的 `status=pushed` 回执为准。
