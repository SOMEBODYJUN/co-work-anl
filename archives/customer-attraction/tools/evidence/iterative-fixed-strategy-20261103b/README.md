# 迭代固定策略：原件、依赖与执行边界

正式正文为[程序合同](../../../state/程序/迭代固定策略的可信续局与重数优化--程序.md)和[双保存点](../../../state/计算/迭代固定策略的五人双保存点与证据边界--计算.md)。

`original/`保存本批三个primary的完整原字节，共1074563B。`source-manifest.json`逐项保源ID、完整冻结路径、两个commit、Git blob、SHA256与size。逐源取得方式均为根work.py clean show ID --out，原始本轮工作路径在cleanup/workspaces/Boss2/resume-20261103b/iteration/acquisition/；没有替其它相关源认领或done。

`related/`另保真实生成器5036B markov_joint.py及9824B原工作区完整README，related-manifest.json给准确指纹。这两个是比较源，没有本批receipt。`dependencies/`给规范四模块及实际20567B/13242B两个helper，六件59284B，dependency-manifest.json同时保已有同字节证据位置和冻结定位。原入口在祖先寻找规范包，证据目录不是恢复原工作区的可直接运行布局。所有相关源与六件依赖均已完整实读；没有执行其import或main。

`lossless-reading.json`是两份完整JSON的可逆阅读表示：保全部元数据/日志/证明字段，仅将完整有序动作表改为330态计数表、127克隆改为精确稀疏表。只对这两份原表逐项确认同计数一致后才作此压缩；解码与原JSON完全同值。它不声称一般策略都可计数化。`markov-count-table.json`含00011点全部330动作，reading-stdout.txt亦含完整紧凑打印表；iteration全2801动作均0。

`saved-review.json`记录5602个动作键值全部消费、两个127坐标向量全部消费、实际rollout与声明根相合，并确认iteration的完整strategy及每个portfolio_proof字段，同既有R8九客户常值点完全相同。既有fixed-audit及其真实执行事件保原路径引用；本轮没有重跑或冒领该事件。

`reading-event.json`是本轮唯一一次新标准库读取检查，退出0、stderr空，精确耗时0.18319362299996556秒；`reading-script-executed.py`是当时执行代码的同SHA副本，原argv指cleanup工作区read_saved.py。该脚本读完整冻结文件、核指纹、重建表、作逐值往返和旧证据绑定；不导入原代码，不调用BI、LP、MILP、随机搜索或完整收益验证器。它不是一次新发现搜索或全仓重证。为保本轮实际执行历史，不以相同名字覆盖旧事件。

九客户点的全部SPE比较、四索引对偶由正式正文中的自足解析及明确同输入绑定承担；全兴趣单客户点每人在任何历史/行动下恒得1/5，所以任意合法完整动作表均为SPE，W=OPT=1，不需要另跑求解器。

完整程序及两个保存点的数学量词、浮点/精确边界、模板点/原模型反例、五人已知定理/恰六人开放均在正式正文分开。原报告没有保存的argv、环境、MILP连续解、对偶界或未导出策略不补造。
