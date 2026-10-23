# signed_harmonic：有符号终局 ghost 预算

当前状态：一般目标与本目录的充分预算仍 OPEN，无新一般福利定理或反例。

- `optimal_exchange_moments.md`：一般最优性随机等槽交换行及1/r、逆向加权的调和闭式；全部是已有最优性行的非负组合。第5节代入已有全树尾深障碍，精确证明新静态行仍不能替代早期真实中继。
- `audit_exchange_moments.py` / `exchange_moment_audit.json`：5850组系数闭式、1295组子集概率的Fraction核验；只审计恒等式。
- `audit_identities.py` / `identity_audit.json`：支持交换差和ghost删除/末位系数的算术核验。
- `support_reduction.md`：精确充分性、重复槽消去、最优支持少于m时必全目录覆盖、静态子模 J 目标、最小J最优支持交换式、删除与真实末位接口。它把需证明的弱版本固定成某个最优支持的 J≤2W，不把所有最优元组当必要量词。
- `scan_examples.py` / `example_scan.json`：21个规范examples的全部可实现纯SPE终局×全部最优恰m槽元组，用Fraction计算signed harmonic/linear余量，同时区分任意最优元组与有利重选版本。全部余量非负；有限诊断不证明一般桥。
- `cone_probe.py`：随机完整计数策略的全类型激励锥LP发现器，支持最优性约束、重复元组和取消最优性。尚未输出任何负候选；浮点无分离不作证明。

实际运行（所有 trials 均只诊断一个明确一般候选）：

1. p6,m3,200策略，distinct optimal d，harmonic：未分离。
2. p6,m3,150策略，all repeated optimal d，linear：未分离。
3. p7,m4,100策略，distinct optimal d，linear：未分离。
4. p6,m3,200策略，all repeated d、无最优约束，harmonic：未分离。
5. p7,m4,all repeated d、无最优约束，linear：运行到trial20后主动中止，未报告负候选，不宣称完整100策略。

后续：不继续扩阴性扫描。真正未证交换义务在`support_reduction.md`第4节：正coverage损失的替换不能由最优支持最小J性自动收费，必须利用真实离轨收益和全后继最优性。可使用某个有利最优支持，不必证明所有任意比较元组预算。
