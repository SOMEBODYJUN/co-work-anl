# 原程序与完整输入证据

五primary原件20616B，source-manifest逐一记录冻结blob/commit/SHA。comparison-manifest是五份全读现有正文的独立快照，非本批新done。dependency-manifest为空：原程序无外部输入或local import。

原2939B入口仅调用一次；run-original-once.py先创建全新replay，原字节放原repo相对路径但独立source-root。原write_text会覆盖相邻JSON，隔离防止碰旧文件；runpy主入口/标准argv和被动profile记录实际输入/action键/gap，不额外调用源函数。原run失败会保存stderr且不自动retry，实际exit0，无失败。不要重新执行包装器或原程序。

replay/execution-state.json保存Python/cwd/argv/optimize/真实次数，原stdout626B与新报告626B和旧报告完全同SHA，stderr0。program-built-input-and-runtime.json是唯一run的原局部数据被动快照：20likes、43策略键、258含self gap、20个ell、实际路径和返回字段。不是外加穷举新研究程序。

derived-static-and-bank-correction.json为解析数值代入：本20客户B3=17/5与单装饰比值2/5，以及另一个既有银行m4族真最优价−19/588。原审计程序未计算这些值，未运行银行新输入。旧626B的EXTRA OPEN历史scope保持原字节；正式正文另注明当前反族纠错，HALF没有被本批反驳。
