# k=2 取向到 diamondless 调度：当前版本采用说明

## 当前输入与历史证明

本正式修复采用 `M-af28c29d24b14be393e56add3cebfc7c` v4（pin `3d006e3f06c9570a8ccbbb50cf299c465c4a37e8b1d04d1e56d90cb0527365fc`）到 `M-1b8213b483df41bd9fa149b10255daa3` v2（pin `b1f641db6d0df9cc8be5e7fd3d69b3c37578f403733ceea79a752742808b0069`）的单向完整迁移。源中文全文 SHA 从旧边的 `58b4be48da7c01dac6a3e5eeff733d7e211dbae675690684e4142742d5bc4740` 刷新为 `3fe059248d81113e400a7c5fe3084cccc9eb53267d4c4f1a570e086bc1a06e0f`；当前登记说明变动为同页第3节 join 计费及另节 gate 轻边方向澄清，Theorem 13 的数学合同不变。冻结 Asahiro PDF 的 SHA 仍为 `5db93652d80fd92b6440e0a0e22edfdeb09f78e2b886c95cb4adf171c67ee147`，Page 正文、PDF 及目标 pin 也未变。

原独立证明 `map/edges/unrelated-machines-3a-3a-6231f96071b186d2/planar-bipartite-k2-to-diamondless-proof.md` 以原 SHA `d9ad5dd8c4b1d2f46ed93eb18d01dac25fb516acada99a73ad2553bfa057ba21` 原路径、原字节采用。其“当前两个 v2”及全文阅读叙述属于原 Boss5 审读时点，不是本次版本或阅读量声明。旧边由新目录内同 edge_id 的当前绑定 JSON 替换；不改写历史证明。

## 本次实读与数学复核

本次直接核对当前两个完整登记对象、正式新任务、旧任务/收据、旧边及独立证明；直接读当前 Asahiro 中文的身份/模型和第4.3节，以及 Page 中文的身份/模型和无菱形硬度段。冻结 Asahiro PDF 直接读第3、16–18页文本，并逐页目视第16–18页；Page PDF 直接读第2–3页文本并目视第3页。复用已存 3D 审查对623关系的完整复核，不重读其无关算法章节，不冒称本次重读两篇全文，也未做历史中文全文逐字 diff 或重跑科学实验。

再次核实：k=2 的实际 Planar 3SAT 构造简单、二部、最大度≤3、权仅1和2；special 容量耗尽迫外边指入，变量环一致定向，子句给出满足性与 OPT≤2 的双向等价，整数性给 NO 时 OPT≥3。令机器为原顶点、任务为原边，任务分给取向尾端，与合法调度逐机保负载双射；Page 的入端 convention 只需逐弧反向。资格交叠图恰为 L(G)。简单三角形自由图的线图三角形来自共同端点，菱形的两个共边三角形将迫四条原边同接一点，违背最大度3；故排除普通菱形子图，包含非诱导情形。

以上同时支付目标的两个结构限制及完整2/3 gap；任意固定1≤c<3/2的合法近似在 YES 输出≤2c<3、在 NO 输出≥3，故 P≠NP 时不可多项式实现。保持 accepted / ALL / unconditional / whole，不加入新前提。该桥专用于k=2；仅有二部性或k≥3均不足，K1,4 的线图K4含普通菱形。目标登记中的 At-most-3-SAT(2L) 是其原论文证明路线，本边提供另一条 Planar 3SAT 完整证明；两者不构成联合前提。本范围无新数学 follow-up。
