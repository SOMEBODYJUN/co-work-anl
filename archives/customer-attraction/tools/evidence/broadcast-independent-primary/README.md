# 独立broadcast审查与非零fresh实现

五主源共40050字节，全部全文读取、按inventory原字节/SHA保存：9312B程序、1149B报告、16375B作者快照、2871B先消息重构、10343B后读稿审查。见source-manifest.json。

正式交付：[独立重构与范围校正](../../../state/审查/鲜广播消元的独立重构与两处范围校正--审查.md)、[非最优源非零fresh计算](../../../state/计算/非最优比较源的非零鲜广播与实际券复用--计算.md)。

- original保五件原字节及原相对路径。快照与现16669B长稿只有两段区别，author-version-diff.txt与author-version-comparison.json完整保留；快照待审标签不覆盖随后实际审查。
- pre-execution-current-file-search.json记录运行前repo/external当前文件大小/SHA扫描，无同SHA副本或run。名称/完整SHA文字检索只命中库存/claim/前批候选。
- replay仅复制原.py后实际运行一次，无外部输入、无-O；exit0、stderr空，新1149B JSON和stdout逐字节同冻结报告。execution.json绑定准确命令、cwd、UTC和指纹。原程序用write_text覆盖同名输出，因此旧报告单独存在original，执行前replay未含JSON；再跑应另建干净目录。
- input-contract.json说明真实输入全在源码内，旧14客户对象只是明确重定义的数学来源，非漏存的外部依赖。
- derive_fixture_details.py/json是本批读后直接定义展开：明确43动作、216覆盖值、两节点/取消/每券需求。不是第二次运行原程序，也不称新的盲/历史独立实现。
- supplement/rejected-initial保初次补充策略表的两处平局误写、原补充py/JSON及自查失败；纠正为(B,H)->T、(T,H)->B后，仅重算补充表，原程序没有再跑。原报告与活动两节点金额始终相同。
- related-manifest.json与REVIEW.md记录全仓比较和后续SAFE纠错；逐源receipt、关系与精确文件清单在workspace。

有限实现覆盖22客户、43完整历史、258含自身IC及三种43行核。subset循环只枚举future，三模式共156项，不覆盖含past角色全部子集。合法非最优(D,H,B)比较覆盖17<OPT18，rho总2=source当前1+注入1；真正fresh边传1/8，末端all past券1/40；gross23/20-refund3/20=1。取消后第一节点即吸收1，不能沿用旧退款。本例不是最优owner非零初始化、cap1反例或half证书；旧两SPE无fresh正边的范围未被改写。
