# Boss21 potential：变背景势与连续基准检查

2026-10-24。输入始终为一般共同有限目录、任意人数、全部有序历史纯 SPE，目标 Q-CAG-HALF 仍 OPEN。本目录不宣称新增 half 证明。

## 当前工作状态

1. 已读模型、一般工作稿及调和势分支单调、下一最优势增量 PI 的明确反例。没有复活这些断言。
2. 曾考虑在 `sum_A q_A=m` 上最大化 `sum_x log(1+c_x(q))`。KKT 价格 `lambda=max_T sum_(x in T)1/(1+c_x(q*))` 确实满足 `m lambda=sum_x c_x(q*)/(1+c_x(q*))`，从而 `OPT_m<=2m lambda`。这是旧连续势接口的重新推导，不计作新一般进展。
3. 已撤回“Jensen 直接给 `lambda<=v_(m+1)`”的推断。Jensen 只给自由连续 minmax cap 不大于真正静态安全值；不能把任一 log 最大者的 cap 与该 minmax 值等同。旧同一撤回见 `R-6bb0323d87294932af2aa23b47b9d4ad/independent/route_status.md`。
4. 为攻击上面**准确的静态价格比较**，临时运行了零背景有限数值诊断（log 优化与真正有限静态安全 LP；另以给定有理背景分配、KKT 价格为变量做 LP）。未取得严格分离。这既不是该比较的证明，也不是 half 的新证据；临时代码未被包装成研究资产。
5. 根据 parent 的优先级，暂停连续基准探索，完成 security 分支背景反例族的独立定义级重构，见 `review_background_security_plateau.md`。静态双证书、统一 B>=3 的主收益排序、所有单例离轨拼合及 1464 历史策略均通过，准确排除有限斜率局部安全值增长桥。该结论严格区别任意合法前缀背景命题与零背景根福利命题。

另已向 random_portfolio 分支独立核查任意 owner 的逐客户 `H_a-1` 预算，以及固定实际终局的两项 owner 平均公式；完整独审由 branch_budget 分支负责。

## 下一步

本轮独审文件为 `review_background_security_plateau.md`，独立重构程序为 `audit_background_plateau.py`，自含全部有序历史策略的输出为 `background_plateau_independent_audit.json`。盲重构完成后已读作者稿对稿，十二个代表前缀的可实现完成集合全部吻合；作者三点静态对偶与本审两点静态对偶均正确。

一般 half 仍缺跨分支或跨位置信用；不把本局部桥的排除称为主目标的正面闭合。
