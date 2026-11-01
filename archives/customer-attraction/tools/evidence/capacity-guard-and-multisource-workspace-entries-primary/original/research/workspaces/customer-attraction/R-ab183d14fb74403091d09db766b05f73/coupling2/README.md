# 同人数互惠运输的第二轮：单源末端吸收

2026-10-22。原 Q-CAG-HALF 仍 OPEN，全部文件为个人备份，未作外审或新颖性认证。

* `terminal_absorption_and_capacity.md`：独立审查原 NP-TRANSPORT 的 (7)→(8)；用末前玩家真实复制偏离证明单源完整终局税吸收，并接续既有两人税的更强端点 K≤最后两人收益+τ_{m-1}；明确初始最优覆盖、逐客户 hit/回复容量、负交集信用和实际收益总乘子的一般多源合同。辅助证明 W+最后税增量≥(H_m+1/2)u_m。未构造一般最优组合的全树运输。
* `audit_terminal_absorption.py`、`terminal_absorption_audit.json`：定义级精确恒等式、全部有限二元路径与有限真实 SPE 核验。有限检查不证明一般目标。
* `multisource_kernel_merge_interface.md`：根提出的整合核从最优 m 主题出发，固定同一 pivot 至多两条真实行制造重复、每层删重并由该层实际收益支付，前缀正税逐客户容量一，最后落到真实两人 endcap。路由总是可构造；高阶有符号债尚未支付。精确净债预算与主目标等价，不能据此宣称一般证明推进完成。
* `audit_multisource_merge.py`、`multisource_merge_audit.json`：有限任意回复映射的两步删重、真实 SPE 中逐步精确债、复制付款、前缀信用和总账恒等式；不证明高阶债支付。

接续：构造根最优并集的多源运输，同时控制逐客户截面容量、端点质量及负交集信用。强线性末位支付 m u_m≤W+τ 已由旧23客户真 SPE 否定，不重复作开放桥。
