# 同源回复再查询的分离程序证据

[自足正文](../../../state/程序/同源回复再查询的分离程序--程序.md)保七条真实行、同一源预算、两个分支共享C和交叉B、六参数精确H/隐藏min、16查询、ct归一行、浮点函数筛选与CLI有理接受的完整合同。

[原码](original/early_reply_requery_cuts.py)4424B、[直接分组依赖](related/old_query_reply_cuts.py)4128B、[查询/解析依赖](related/terminal_portfolio_cuts.py)5223B及[传递加载模块](related/priced_hidden_reply.py)2908B均完整读取、冻结SHA核对。后者只因oq import加载，本源不调用其投影函数；各依赖main均0运行。[源清单](source-manifest.json)区分唯一primary、相关输出和共享输入，不为相关源代done。

本轮[原执行](replay/execution.json)只一次默认CLI：24LP，1.529447613秒、exit0、stdout300B、stderr空，原断言生效。保[原stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)及[完整新输出](replay/report.json)。输入是上批共享[823005B5180点](../nested-reply-projection-program/related/combined_branch_latest_exact.json)，同SHA的[输入接口报告](../nested-reply-projection-program/input-interface-report.json)直接复用，0重复schema/全图运行。原四源码与点前后SHA均不变。

[原运行组织器](run_original.py)使用临时最小布局：仅未执行work.py路径标记、原源码及namespace priced模块；不运行旧完整包初始化、协议工具或凭据。重现默认24LP可在本目录运行：

```sh
python3 run_original.py
```

此命令会覆盖本包replay中的新输出，不是只读已有证据。本轮没有运行384全查询、依赖发现器或新图优化。

[6165B历史全查询报告](related/early_reply_requery_master_all_queries.json)仅相关全文读取和保存：原384LP/14项。其query5五项cut/slack与新默认输出按顺序完全相同，见[纯字段对比](historical-record-comparison.json)；另9条历史负值未在本程序任务独立回代，更不称当前384LP重放。

同批另一代理在[联合表报告](../local-reply-portfolio-joint-cuts/exact-audit.json)负责v2五条requery的5×1905坐标、24个独立min/384隐藏候选及五个精确slack。本源只复用结果，未重跑其入口；base4/v2五模板、历史14项和本次默认5项分别保各自序与范围。

[相关全文比较](comparison-manifest.json)、[关系判断](relation-review.json)与[执行计数](execution-scope.json)记录来源/实现/有限核验的准确身份，未写第三阶段超图。[封包自查](self-check.json)只核字节、语法、链接与已记录输出一致性，不重复任何数学程序。
