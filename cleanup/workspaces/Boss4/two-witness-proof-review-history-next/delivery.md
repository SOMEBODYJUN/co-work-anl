# 两源交付

external staging根：`/workspace/scratch/37f0f9248cfc/boss4-next-cache/two-witness-proof-review-history-staging`。

只创建一个新审查页、一个新evidence目录及本独立工作区；没有修改任何既有正文，没有Git写、sync、claim、done、checkpoint或认证。两源的逐文件receipt在`semantic-receipts.json`，均为integrated；正文及必要依赖须先由Boss拷入并checkpoint，receipt才可由Boss提交done。

交付新增内容：完整v2合同/目标端染色证明/费用/字长/T0、作者六机sharp；general和typed两种五机实例的不同处理时间；旧组合审查canonical指纹与当前全文区别；pending与之后root软件记录的时间边界。当前v3/多见证和单home强合同只作相邻范围比较，未借旧审查升级。

`source-manifest.json`保存2源的冻结定位和SHA，`comparison-manifest.json`保存7份相邻历史及当前全文的精确副本；这些比较源未新增done。所有副本由只读clean show取得并核size/SHA。

实际自查仅一次运行`verify_delivery.py`，exit0：10份来源副本字节/SHA一致，6个当时已存在的JSON可解析，9个新增页本地链接存在，数学定界符成对。报告`delivery-verification.json`，命令和标准输出见`verification-command.json`。它不执行数学程序。本轮数学检查是读后逐式检查，记录在`mathematical-self-review.json`；没有未解决的两源数学冲突。外审和新颖性不认证。

实际未领候选见`candidate-sources.json`，由本地当前结果快照只读`clean list --available`得到，候选应在新claim前再按公屏核对。所有七份历史已经本轮作为比较全文读过，仍未替它们做来源done。
