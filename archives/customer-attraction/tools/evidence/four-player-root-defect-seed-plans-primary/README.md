# 四人根缺陷四种子的证据说明

对应正文：[四人根缺陷四种子的完整计划与版本差异](../../../state/资源/四人根缺陷四种子的完整计划与版本差异--资源.md)。四primary为caf0a6e05a87748367c4、397a11a3aebb0a75bf68、9019138f2770c8cf5e5b、71bb086422d9f9255f6d。

四份原JSON全部实读；本批正常clean-show导出与已有冻结副本逐字节相同，不另造一套原件。准确原路径、两个source commit、blob、size、SHA256、正常导出路径与receipt摘要保于[结构和差异报告](structure-and-differences.json)；正常show的原始receipt保于[receipt目录](clean-show-receipts/)。原JSON最终路径均为`../root-regret-discovery-and-frozen-audit-four-primary/original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/seed_source_m4_v*.json`。

[完整动作矩阵](ordered-action-tables.md)每份保259历史，四份共1036动作，深度各1/6/36/216；矩阵可逆地对应原二元对schema。新检查确认客户重数正整数、兴趣/动作范围合法、无重复历史、六覆盖签名不同、actual等于按动作表读取的路径，并准确列出两组单动作差异。客户行数和重数和为v0的5/7、v1的16/31。

新`check_structure.py`只核字节、JSON/动作域、元数据转录及版本差异。它没有导入或执行原程序，没有计算效用，没有做IC、OPT枚举、LP、BI或扫描。脚本第一次完成旧副本结构检查，随后加入本批正常show绑定并执行；最终报告只表示最终这些只读断言。复现命令为：

```bash
python archives/customer-attraction/tools/evidence/four-player-root-defect-seed-plans-primary/check_structure.py --repo /path/to/result-repository --primary-dir /path/to/normal-show-exports --output /path/to/new-check-output
```

原数学核验成熟证据复用[2516B原程序](../root-regret-discovery-and-frozen-audit-four-primary/original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/audit_frozen_sources.py)及[3397B原精确报告](../root-regret-discovery-and-frozen-audit-four-primary/original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/frozen_sources_exact_audit.json)，两者均已完整读过；[4565B原发现报告](../root-regret-discovery-and-frozen-audit-four-primary/original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/root_regret_discovery_report.json)也全文比较。三者的精确SHA/size在结构报告中，不把其旧数学执行记为本批新执行。四源原6192项含self正深IC与24根值属于冻结报告的范围；没有新逐行日志或新求解器状态。

原JSON布尔true保原意义：只指正深度IC。四个根遗憾均正，故没有任何一份被本批称作完整纯SPE。固定原点负修复余量与浮点重优化锥的负数各自保留，未相互认证。一般三倍根修复、私有遗漏及HOM理论均引用已有正式对象；未做第三阶段建图。
