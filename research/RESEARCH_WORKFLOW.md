# 用登记与超边持续做数学研究

本流程把已有数学接到真实研究，再把有价值的新内容写回。研究启动词见 [Main](../prompts/research-runtime.md)，命令见 [IMPLEMENTATION](IMPLEMENTATION.md)；前置的登记和建图分别按 [PHASE3_READINESS](PHASE3_READINESS.md) 执行。阶段配置存在不表示真实登记、正式图或 Solver 团队已经产生。

## 研究实际接收什么

| 产物 | 研究中的作用 |
| --- | --- |
| research/registry.json | 稳定对象 ID、版本、精确陈述、模型、量词、假设、状态、正文及必要证据位置 |
| registry.edge_files 指向的关系正文 | 每条关系的完整端点、共同条件、各前提作用、数学解释、证据与实际状态 |
| map/graph-v2.json 及存档/子档投影 | 可重建的导航视图，跨边界保留完整端点；不另维护第二份数学真值 |
| archives/.../state 与必要 evidence | 完整可使用的证明、构造、反例、方法、具体障碍及开放义务 |
| research/runs/RUN 下的 packet、笔记与事件 | 本次实际送入的材料、原 Solver 接续链、反馈和断点，不替代正式数学正文 |

Solver 用 search 找对象，用 show 读正文，用 context 取相关关系。一个逻辑支持选项的全部 source_ids 是 ALL；不同证明是 OR，必须分别保条件，不能把多个分支的前提揉成一条证明。已选分支继续递归其必要前提，导航距离不截断这个闭包。定义按问题和条件读，不为每个模型建一个连接所有对象的枢纽。

`research search QUERY --model MODEL --truth-status STATUS --kind KIND` 按需筛选数学对象；状态和类型可重复。`research show ID --body` 读取精确正文，绑定改变或附件缺失会明确报告，不遮住仍可读的正文。`research context ID...` 默认给 accepted 正向支持的完整前提闭包，并列相关 accepted/proposed 线索；`--edge EID` 可选择某个替代证明分支，`--edge-status rejected` 可查看已拒关系，`--relation-kind refutes` 可定向查看反驳。`--hops` 默认 0，只增加导航范围；这些线索筛选不删掉必要的逻辑前提。

反驳和失败关系精确指向被否定陈述；proposed、rejected、启发、引用、实现和有限观测可以按需取来研究，不能作为已证支持。对象与边的版本改变只触发相关内容的定向重判，不要求每次研究先重扫全仓，也不能把过期误判为命题为假。

## 一次完整研究循环

1. 恢复本对话 clone、精确原题和最近断点，保留已有工作。
2. Main 选实际所需的 obstacle/full 输入，生成 packet，通过平台真实 spawn 启动 Solver；记录真实 agent_id。两类默认空历史，用户另有要求则按其要求并记录实际输入。
3. Solver 自选数学方法，按需读完整前提、正文和证据，直接推导、构造或处理具体缺口。Main 也参与实质研究。
4. 有价值的中间结果立即写 workspace 和必要输入，Main 持续 checkpoint。普通批量计算优先可用云端批处理，短计算可在当前环境完成；Codespaces 留给确需持续交互、长进程或特殊环境的任务。
5. Main 把具体反馈送回原 Solver 接续。原进程不可用才从同一 profile、packet、最近笔记、事件和待答问题恢复替代者；不重置已经成立的推导。
6. 成熟数学回写相应 state，代码/输入/证据跟随数学 owner，更新有关对象与超边。只处理受影响部分，不重做清洗阶段。

循环持续到原题闭合或真实运行边界；不以一批、一次提交或一次工具调用结束。候选可保存，开放义务可保留。交接明确已推送、仅本地、具体疑点和下一动作；不虚称后台仍在工作。

## 两条真实的取用路径

六人共同目录研究可以取“真实前缀均匀组合接口”。若 UP_actual 与完整 SPE 的实际偏离比较、价值守恒同时成立，就有 OPT_m≤(2−1/m)W；取 m=6 才能给目标的充分条件。UP_actual 本身仍是猜想，推导包必须显示这项未付前提。52 客户的冻结匹配反例否定的是固定实际后缀的 Q≤W，不能移来否定沿同一策略真实后继的 V_ij。五人半覆盖与六极大主题半覆盖也保各自人数/目录量词，不能仅因“六”或“half”接成一般六人证明。

加权拥塞研究中的有限权类别势，只有在全局权类别数 k 的限制下给 A_(d,k) 或相应 d/ln d 保证。全状态线性次数无均衡族允许类别数随次数增长，否定全类固定 C 的 Cd/ln d 保证；它不反驳前述受限类。这里需要 scope、量词和实际映射，不是把同含“势/次数”的节点相连。这两类区别应由登记陈述、边条件和 Solver 阅读同时保留。

这些用例用于说明如何调用成熟数学，没有新增固定数值搜索或重复运行旧证书。

## 计算与持久保存

Python/云计算执行实际数学程序，不启动模型 Solver。GitHub 保存已经推送的正文、证据和运行断点，也可提供已有批处理通道；增加 CPU 不增加模型并发。Main 通过真实 spawn/followup 调度模型，通过 work.py checkpoint 保存并确认 pushed。

现有批处理入口是 `compute request EXP --manifest PATH --request-id C-ID --timeout-minutes N`，随后 checkpoint 请求、代码和输入并确认 pushed SHA，用 `github runs --head SHA --request-id C-ID` 定位，再由 `github run RUN-ID`、`github artifacts RUN-ID` 和 `github download ARTIFACT-ID --out PATH` 读回真实结果。新分支包含新计算请求文件的推送会触发工作流；普通代码/正文推送不触发计算。`workflow_dispatch` 只有默认分支实际具备对应工作流时才可使用，不能把命令存在当作云任务已经运行。

计算从具体数学疑点出发：能直接证明就推导；需要代码才编写。有限阴性、数值收敛、接口检查和语法通过不代替一般证明，也不值得单独制造数学节点。现有云端能力及结果取回入口见 [GITHUB_RESOURCES](GITHUB_RESOURCES.md)；按真实可用通道执行，不把尚未接通的接口写成已完成实战。

新增成果先有完整数学内容和必要证据，再更新登记/关系。无需每出一个引理就重做全仓分类；反复维护无用审计包装、旧身份副本和历史交付包会妨碍下一轮研究，确认无独有数学、必要输入或未完草稿后直接清掉。
