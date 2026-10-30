# Boss4 dynamic-flow 四源交付

对应实际claim d548561b8587681002f4e3f70207db04fcb61d86，四主源43f659120e2d351cc306、b6add4ee419ea93ffdd1、54114b48e0b2229ea580、ca3996e6d6ac1421476b均全文clean show实读，原3md+1py共15063字节。

新增三正文：

- state/引理/根重置对恒等式与辅助尾份额协方差--引理.md
- state/障碍/根重置局部账本的笛卡尔放大--障碍.md
- state/反例/同分布额外查询高于平均强制收益--反例.md

完整路径在formal-targets.json；证据archives/customer-attraction/tools/evidence/dynamic-flow-workspace，14原件1516795字节，包括4主源、6真实执行依赖、4比较稿。完整来源、hash、程序和输出均自足，无stub。工作区semantic-receipts.json为4条integrated实质回执。

关键纠错：原diagonal脚本docstring/stdout及一份md开头把13/1722说成G-实际u，实际assert比较G-pD。给定p下G=1501/1722、pD=248/287、实际u=7/3，G-u=-839/574。covariance原稿(5)无条件期望内含a_A时多一个p_x，后续原源3ae90da81455d49a541d已有同一勘误；F_A仅在A覆盖该客户时是真实尾份额，其他分支是多一单位占位的辅助量。原件和错误原输出原样保留，正式正文准确纠正。

真实执行：原三人脚本__main__一次全过，原31历史124非自身偏离；原独立raw-DAG verifier一次全过，13872节点6435终局/59496含自身比较。新定义级校验重建三人全部31策略节点/155含自身份额，150对实际节点RESET、八人根64对RESET、1280标量身份；DAG路径重数覆盖2396745决策历史和16777216终局。基pair R(3,7)=9/10、两e/J均0，但两点iid G=359/120<u；全部整数k笛卡尔放大由正文代数证明，不枚举巨大乘积树。

四份比较稿只读，未额外done，未运行驻留审计/随机搜索/LP/SLSQP；已成功两个原入口均不需重跑。驱动器执行后只修正真实launcher cwd与base子进程cwd等记录字段；精确执行版replay-executed.py及两hash保留，原程序没有修改或重跑。

verification.json已通过：14原件原SHA/长度、Python AST、28链接、4回执目标、日志hash、驱动器只有元字段差异、关键正负gap及基额外槽分数。三人/八人辅助例与当前恰六人每份完整纯SPE半覆盖目标明确区分；不把平均D、实际u、自由Q和路径聚合混用。关系已解释，不造第三阶段超图边。

未执行任何Git、claim、done、checkpoint或外发；未改旧52批正文或他人文件。请Boss串行checkpoint上述三件正文、证据与本工作区后再提交4条回执。外部原件/运行副本仍在/workspace/scratch/37f0f9248cfc/boss4-next-cache/cag-dynamic-flow-cleanup，不是正式复现依赖。
