# 本批证据与冻结勘误范围

actual-claim.json是唯一服务端成功回执的原字节副本。五主源当批全文读，13连续覆盖块；支持8份只比较，不额外receipt。source-manifest.json区分本批新显示与前批实际已读、核同SHA复用；linked原来源表不扩称原件全读。

errata11文件已按root实读确认冻结；manifest内三旧页全文SHA、原段行号、canonical/primary/代码证据与建议patch可直接审查。worker没有应用共享修改、没有触冻结源或进度。parent后续串行应用不改变此包。

三有限JSON都是既有报告阅读，程序新run0；arity代码只复用前批确切选段173行。F2的历史section8972抽取规则未复现，本轮精确边界切片a6be另记；whole9ef与primary相同，不假填切片等同。

check_delivery.py仅做字节/覆盖/receipt/新ID/本地链接/版本/冻结patch包的结构检查，不运行任何归档数学程序或外部论文。work-in-progress.json为被最终manifest排除的历史草稿阅读checkpoint。
