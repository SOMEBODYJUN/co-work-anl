# continuous_old_query_cuts.py 原源与局部重放

主源 `1d6018b818d7ff99f974`，4531B，SHA256 `d6b618e95afa4ee287a8ed6e23c6b06248d82d2a07ee64c6065f30caa63649b6`。这里只清洗该程序；15013B cut表及815911B旧点作为实际输入保存，不额外宣称它们已由本任务完成独立来源处置。所有冻结原件的ID、两提交、源路径、字节数和SHA在 [manifest.json](manifest.json)。

- [数学正文](../../../state/程序/旧查询回复的连续分层分离程序--程序.md)说明八字段、180结构、逐客户min、价格LP方向、真实量词和float/exact边界。
- `original/` 是未改源码；`related/` 是两直接数学依赖、原64cut/旧点，以及后32cut与其调用者的比较原件。
- [verify_continuous_rows.py](verify_continuous_rows.py)自写六索引轨道计数与逐二元后继公式；不调用作者groups或快速投影来生成独立值。它调用原row/psi作被测端，不构建4971、5108或其它整图。
- [replay/local-row-audit.json](replay/local-row-audit.json)保64条全部cut/精确slack/系数SHA：121920列比较及3000投影比较通过；194组joint质量检查通过。overlap的原图含义及4971原约束没有重验。
- [rerun/execution.json](rerun/execution.json)是本任务**唯一一次**作者发现入口记录；180次LP尝试，exit0、空stderr，输出 [report.json](rerun/report.json) 与原64cut表逐字节同。该报告不是LP最优性证书，`negative_structures=64`是截断后的返回数。
- [comparison.json](comparison.json)保前64与后32的完整元组比较：21相同、43前表独有、11后表独有，后表不是前表的前32条。

当前原入口使用clone外最小冻结布局，含从未执行的 `work.py` 路径标记，以及仅含原 `priced_hidden_reply.py` 的 `customer_attraction` namespace目录。三份实际数学源码字节不变；没有声称运行旧包初始化或完整旧仓库CLI。NumPy 2.3.5、SciPy 1.17.0、Python 3.12.14；版本记录是本次环境，不是源文件的版本声明。

自足复核（默认只做局部系数核验，不启动原发现入口）：

```sh
python3 -B run_local.py --out /path/to/new-local-audit
```

`run_local.py` 检查四项原输入SHA后创建临时最小目录，将未改源码放回冻结相对位置，核验结束删除临时目录。显式加 `--mode original` 才重复作者发现；本包安装后没有再执行这个模式。已有唯一原入口记录在rerun，后续读者不必为检查精确负余量重做浮点发现。

自写核验器开发时曾将旧点字段strict_half_gap误写为O/2−W而触发断言；全文核原分数后改为该字段真实定义O−2W。该失败是当前核验器的字段解释错误，不是冻结源码或必要点的失败。最终保留的结果为更正后的完整通过；原作者入口仅一次且通过。

当前不重复research_5联合master验证，不声称所有有理乘子的分离完备性、原点为SPE、任意六人half或全域不可行。已有正式引理证明局部合法性；本包补实际源阅读和有限数据/实现对照。
