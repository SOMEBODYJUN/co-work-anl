# owner势、锚定资金与联合取消：原件及一次A/B审计

正式五源共23959B，全部原bytes在`original/`，[主manifest](source-manifest.json)给原Git blob、SHA、大小及双冻结来源。claim确认提交`5f8c95e7db12ca44fbe3f21f8b8416198f512399`后重新全文核读，不以此前旁读摘要代替。两份后续rankwise/README旁读7554B保于`related-original/`，[旁读manifest](related-source-manifest.json)明确不替这两源done。

7096B审计原程序只import标准库，输入是源码内九个CASES及三owner规则；[runtime-inputs.json](runtime-inputs.json)用AST只读抽取完整字面数据/导入/selector，不执行源程序。无外部游戏JSON、策略、solver或marker依赖。

在全仓及cache未找到当前同SHA成功run后，新空`replay/source-root`只预放原py。外部[execute-once.py](replay/execute-once.py)一次runpy调用原源码，断言启用；原写出target不存在断言实际通过。冻结2518B报告在original，新2518B报告在原py旁，互不覆盖。stdout同原SHA、stderr0；实际argv/cwd/Python版本/时间见[execution.json](replay/execution.json)。

[execution-state.json](replay/execution-state.json)是同一次运行的外部观察，记录原maxflow入口、原正增广行及返回净role边，不替换函数/输入/循环，结束后不再调用源函数。A/B各852次流、各424正源428零源；合1479正增广、467图最终正净role转运。原报告不新增这些字段，旧bytes保持完整。

这是九个固定静态目录、三规则所选14owner、852含重复标签的组合记录；全割/积分11474。不含SPE/IC、锚定资金、owner UNIT/REPEAT、激活或SOURCE-NET程序验证；一般数学由各解析证明承担。[计算对象](../../../state/计算/最优归属运输的全割与有理增广回归--计算.md)详述真实范围与逆角色见证。

五自足对象还有[owner势](../../../state/定理/最优归属势的单位分解与同叶联合预算--定理.md)、[锚定资金](../../../state/定理/锚定最优主题的普通利润联合资金--定理.md)、[联合取消](../../../state/定理/联合查询库存的Hall取消与初始化付款--定理.md)、[版本审查](../../../state/审查/归属势与联合取消的版本及运行范围--审查.md)。workspace含5receipt、16项解析自查、关系、文件检查、exactcopy及下一实际候选；六人half和一般incoming未由本资源闭合。
