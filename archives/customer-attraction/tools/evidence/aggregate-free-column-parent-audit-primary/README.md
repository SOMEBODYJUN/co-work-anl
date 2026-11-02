# 自由删槽列父方余额与原审计证据

本包独立保全parent/free_column_balance.md、audit_free_column_certificate.py及最终JSON三主源9143B，source-manifest.json记录其全部冻结元数据。原件按source ID和原文件名放original；未改原脚本的必要输入与四个规范包文件放dependencies。两份旧36客户输入和potential_menu_dual.json均复用既有已交付的精确字节，不重新搜索或改变实例。

- [一般势余额及未付跨项](../../../state/引理/自由删槽列的激励松弛与跨势余额--引理.md)
- [父审真实合同、依赖、输出与范围](../../../state/程序/自由删槽列父审的精确合同与四种边界--程序.md)
- [一次原入口事件](runs/original-parent/event.json)、[stdout](runs/original-parent/stdout.txt)、[最终新生成JSON](runs/original-parent/audit_free_column_certificate.json)

复现时建新ROOT，把原py放ROOT/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/parent/，将dependencies完整相对目录复制到ROOT，确认同名.json尚不存在，再用正常未优化Python运行原py。它无CLI或--help处理，在模块顶层执行并覆盖同名输出两次。stdout含两个相继JSON对象；最终1027B文件才与冻结JSON比较。本次exit0、stderr空，最终完整字节相同。

该程序先调用规范全历史verifier，再自己展开36单位客户核258含自身比较、18列、匹配164/5、80坐标12项身份和四例BALANCE；它不调用全SPE求解器，不依赖优化器，也不验证任意策略/游戏的一般候选。原件与依赖的完整来源/哈希在manifest中，不因复制而额外声明这些依赖主源done。
