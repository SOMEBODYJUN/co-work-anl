# 本源自查

- 范围：只负责主源 `55c5313fb9336914e54f`。完整读取 18,546B JSON 的全部 60 条、每条全部 11 字段；逐条参数/规模和全部数字保在原件及 `analysis.json`。没有将旧 atomic 的“120”继承为事实。
- 规则：已读根 AGENTS.md、cleanup/OBJECTS.md、receipt-example.json；未修改共享正文，未进行 Git 写入、claim/checkpoint/done、未运行 work.py、未读取或输出凭据。
- 跨读：完整读同目录 type_count_potential_lp.py、verify_universal.py、verify_universal.json；读 finite_weight_scaled_potential.md、round2_independent_root_review.md 的对应全人数证明与版本边界；读正式 37/33 审计、共同类型缩放定理、自由尺度计算、原子候选线资料、有限双权不同合同资料、原子重选题审查；读有限权类别三角排序势的模型/一般结论及关键边际合同；读后续 atomic-games 的完整 toy_checks.py、候选报告和 cubic K=50 全部 14 系数/三个域外见证。
- 独立核验：原字节程序隔离完整运行一次，exit0、stderr空，输出与冻结 JSON 字段及字节都相同；环境/比较在 analysis.json。独立 Fraction 核 $N=1$ 全 12 组 48 边，并提供匹配两路径下界的显式 $F$；精确参数取十进制有理数，不假装它等于浮点输入。未重跑更大网格以求精确 F/dual。
- 有理化陷阱：q=1.01 的两个 N=1 原 rational 字符串严格不等于精确两路径最优值；差的有理表达已保存。不能将本源任何 rational 字符串未经核验称最优分数。
- 后续纠错：从 K=50 cubic 候选14个有理系数独立重算三个域外比值，全部等原报告且<1；明确是不同三角域多项式，不反驳此矩形网格，亦不支持外推。
- 独有内容：全 12×5 扫描表、q=10 随人口上升的变化、全部数值诊断、60/120纠正、q=1.01 有理化反例、一次完整原程序复现。现有37/33定理不覆盖这些资料；拟合入程序代理同一个计算对象，不立重复定理。
- 证据等级：所有较大N数值平台保 finite-floating-only；没有无限人口猜测升级，没有PNE阈值/新颖性/多项式时间声明；verify结果不代无限域证明；正残差不被称为严格证书。
- 正式目标：`archives/weighted-congestion/state/计算/有限双权真实权缩放边际势的网格合成--计算.md`。本子任务只提交增量草稿；receipt target是Boss将整合的位置，暂未声称正式已保存或done。主源和复现交Boss搬正式 evidence。
- 关系：已给出实现、精确认证、变缩放推广与不同ansatz纠错的解释；未编辑第三阶段图。

实际交付：`draft-increment.md`、`receipt.json`、`analyze_results.py`、`analysis.json`、`replay/type_count_potential_lp.py`、`replay/type_count_results.json`、`replay/stdout.txt`、`replay/stderr.txt`。
