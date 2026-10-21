# Round3：全树行与局部正性的真实边界

一般 Q-CAG-HALF 仍 **OPEN**。本目录只为 Boss6 研究员6.2 的个人研究资产；状态与新颖性分开，无外部新颖性或独立数学审查声明。

- `local_positive_boundary.md`：每个m≥4满足全部m标签局部正性、全部完整历史SPE行、W=1/OPT=2的星形伪矩族；给出低次但跨m+1标签的真实布尔分离式。m≥5严格离轨slack限制局部余项half证书乘子。另对实际终局A^m给出不调用Farkas的显式局部余项half证书及真实模型锐界2−1/m。
- `audit_star_boundary.py`、`star_boundary_exact_audit.json`：标准库Fraction从有符号类型表独立核验参数族、全部历史计数、局部正性、布尔分离及构造恒等式。伪矩不是原客户模型实例。
- `probe_local_cone.py`、`local_m*p*.json`：浮点策略锥探索及候选；有限搜索不证明上界，未搜索全策略。

当前信息边界：未找到局部正性+全树SPE下的half反例，也未证明其普遍half；更没有解决原模型任意策略的half。下一步若采用局部布尔余项，可以用星形紧伪矩强制审计乘子模板；若要更强常数，必须使用超出局部锥的正性信息或另一机制。
