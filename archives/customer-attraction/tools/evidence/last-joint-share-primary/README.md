# 两种份额搜索的八主源与固定输入证据

正式对象：[程序合同](../../../state/程序/非极小可信菜单与联合树的收益份额搜索--程序.md)、[单行条件证书](../../../state/引理/重复根主题与一次末题的单行份额证书--引理.md)、[全部保存点计算](../../../state/计算/五份份额扫描与四个联合树保存点--计算.md)。类型分别是程序、已证条件引理和有限计算；一般CAP、固定σ锐值、有限阴性和half不混。

## 原件、版本与必要依赖

`original/`保存八直接源，共531654B，逐份按本次正常clean show的size/SHA/blob核真。两个冻结commit同字节时仍保两位置，不算两次证据。

- 两原程序`last_share_probe.py`9514B、`joint_share_probe.py`1698B完整读；未import或执行。
- 五普通报告和一joint报告所有字段完整读。全部九份3315个history/action逐值读，所有客户类型、source_clones全数组、归一化值、原dual标量、检查数、MIP字段及历史时间均未省为摘要。
- `related-original/README.md`2388B、`fixed_path_goal.py`5333B、`pair_probe.py`2743B完整读，仅相关比较，不代这些源及其它JSON做primary done，也不改变原作者身份。

`source-manifest.json`共18绑定：八主、三相关、七项真实本地导入依赖。依赖复用结果仓库中`archives/customer-attraction/tools/evidence/strategy-cones/original/`下的完整冻结同SHA原件：tests/audits的customer_attraction_strategy_lp.py20567B、cone_attack_joint_milp.py7637B、cone_attack_credible_variants.py13242B，以及customer_attraction四模块。三helper本次全文读、四规范模块沿已建立正式模型/算法合同复用；不重跑其自测、导出或验证main。

joint模块即使只调用joint_candidate，也在顶层import credible_variants的exact_export/verify，故列入真实导入闭包；该模块没有再引入其它本地文件。NumPy/SciPy/HiGHS是外部运行依赖，历史版本未记录。cached路径按结果仓库根解释；若未来运行原入口，须在隔离树恢复manifest所列原source path，不在冻结original旁运行。

历史README内相对链接保持原工作区语境，不改原字节，也不为让旧导航可点而导入本批未处理文件。新正式正文及本入口的相对链接按结果目录检查。

## 可逆全值视图

`views/`六份同名JSON完整保存所有非动作字段；只有每个actions数组换成有显式p/m的depth/lex动作串。逐层解码回history/action数组，与原JSON结构逐值全等；原数组确按该顺序保存，零重数向量和浮点原值不改。

`all-policy-actions.md`给全部九份完整动作表，计算正文也包含这份全表。五人2801节点按深度4前两位分49行，每行含全部49后缀动作，不是计数商、只在轨表或统计摘要。

原五报告cone字段合计2648只是各文件记录的历史计数，不是本次执行量、互异策略总数或逐锥认证总数。前四报告可能经正常结束final write；m5由README明确为中断前改进快照，快照1/1不能决定中断前真实总工作量。缺失参数、argv、完整进度和库版本均不补造。

## 一次新固定输入精确执行

`audit_saved_share_points.py`是本轮新标准库实现。它不import作者或规范包，不调用solver、LP、MILP、BI或随机；只读六原JSON的九个优化整数点和五个source_clones。

实际只执行一次，输出`fixed-points-audit.json`与`exact-ic-data.json`：九保存点3315历史/19278非自身比较，五seed另3191历史/18782非自身比较，合6506历史/38060非自身（44566含自身）均精确通过。所有路径、终局计数、利润、W、OPT、value和源检查数吻合。label空主题/别名保持字面域，未合并策略。

整数L=lcm(1,…,m)精确代表每名不同单位客户的分母；类型计数乘份额等于逐单位求和，不物化大客户表仍为原单位模型。精确IC文件保每个节点的所有合法当前行动真续局收益，用完整payload与depth/lex索引无损表示，未只保min slack。

五普通保存σ均由真实路径匹配独立得到一个解析上界：β=2/(m+1)、单根IC乘子2(m−1)/(m+1)、交集余项(m−1)/(m(m+1))。代码在全部非空类型逐坐标核恒等式，完整等号原始点全IC另验，因此五固定锥锐性真实成立。不是复现原作者没保存的λ，也不把引理附到四joint σ。

四joint原始点全通过，包括23客非Markov提取σ的91strict/33tie；最后MILP的超时/gap正只属发现状态，不妨碍精确存在性证明。四joint的原dual标量保留为原例程内部检查记录，当前没有λ支持，未新认证固定路径/联合MILP全局最优。

逻辑复核命令（会写指定输出，复核时选新输出名）为：

```sh
python3 audit_saved_share_points.py --input-dir original --output fixed-points-audit.json --ic-output exact-ic-data.json
```

本次原程序/导入/LP/MILP/BI/随机均0，新固定输入审计恰1次，没有新增blind或外审者。`selfcheck-results.json`记源字节、可逆数据、语法、metadata、链接和回执目标检查；字段校验不代数学证明。

`relation-evidence.json`供父方阶段三逐边审阅，区分实现、条件推导、上界与原始点联合锐性、联合搜索来源和23客辅助桥反驳。没有复制旧图或从历史阴性向half造边。旧23客户Markov正文仅另给增量路由片段，不覆盖其历史证据责任。
