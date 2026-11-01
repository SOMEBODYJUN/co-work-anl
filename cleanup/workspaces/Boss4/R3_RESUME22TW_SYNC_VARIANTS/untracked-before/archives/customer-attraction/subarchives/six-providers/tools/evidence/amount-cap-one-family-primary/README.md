# 金额cap1完整策略族的五源证据

正式说明见[原程序与四百动作证书](../../state/程序/金额cap1完整策略锐族的原程序与四百动作证书--程序.md)。五件均为实际冻结源原字节，合计54013B；源ID、大小、SHA、blob和两提交路径在source-manifest.json。

- [全n原稿](original/coupling/amount_cap1_family.md)：6880B，完整SPE与列比2−3/(n+1)。
- [原3332B生成器](original/coupling/audit_amount_cap1_family.py)：标准库Fraction；顶层执行并写同目录JSON，import也执行。当前未运行或import。
- [原36652B n3证书](original/coupling/amount_cap1_family_n3.json)：全部400有序决策前缀动作，原报告2800含自身比较；n3是四人，非六人证书。
- [credible原审查](original/credible/review_amount_cap1_family.md)：3622B，解析逐类型重构，无独立代码运行声明。
- [independent原审查](original/independent/amount_cap1_family_review.md)：3527B，明示先重构后对照；历史复跑为原样脚本，不是独立实现。

另保两份实读后续原稿：[deep精确交接](related/deep_amount_handoff.md)、[deep粗界](related/deep_amount_bound_check.md)。它们仅为相关比较，不在本批五源receipts里，也未冒新done。

prior-certificate-structural-readout.json与prior-execution-and-review-scope.json来自本地此前同SHA缓存：原件现已全字节对等核实；前者只是键域、标签、顺序和实际链的结构PASS，后者明确原入口/import/payoff/IC全部0。复用报告不算当前重新验证2800项IC，更不算当前原程序运行。当前运行边界见execution-scope.json。

源码内嵌单位likes，不依赖项目Instance。一般结论由正式说明完整解析证明及父档锐cap2定理承担；六人n5取值由公式代入，不需新全树运行。JSON的optimum字段来自全覆盖上界达到，不来自独立最优搜索。原JSON无argv/环境/代码SHA/exit日志，未倒填。
