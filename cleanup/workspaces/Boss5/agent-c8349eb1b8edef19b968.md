# 来源清洗草稿：`c8349eb1b8edef19b968`

## 来源身份

- 冻结路径：`history/research_operations/customer_attraction_transition/original/USAGE.md`
- 稳定源 ID：`c8349eb1b8edef19b968`
- blob：`a744b3f7a643a0f517fb0074f34f812c677986de`
- 文件大小：11,534 bytes；SHA-256：`670c5147fb89a49b6ee54920831c0ddd4f9f45327cf3fe9d7fbdb35920fea76a`
- 冻结版本：`legacy-cleanup` / `68fad804ec5946cb296f77dc5b336308a66abf12`，以及同路径 `main` / `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。
- 读取方法：用 `work.py clean show c8349eb1b8edef19b968 --out /tmp/c834_source.md` 取得完整 11,534 bytes，并逐段阅读；未把来源列出的命令当成我实际运行的证据。

## 实际内容

该文件是历史 `USAGE.md` 操作与接口手册，不是客户吸引模型的自足数学证明。开头把当时的默认研究题标为 `UM-TARGET-v1`（一般不相关并行机统一 (2-arepsilon) 目标），说明启动/通信/提交入口和“主目标仍未解决”的边界。随后主体转入设施模型的程序使用说明，逐项列出：

1. 共同目录双设施的 φ 证书接口；任意 (k) 共同目录的因子二构造；规范贪心完整盒接口；等重轻客户无约束流接口。
2. 异构目录因子二、有限实例最优、异址交叠精确比较、至多单交叠和 MITM 程序，以及五地点固定倍率困难性实例生成器。
3. 输入合同：有限正有理权、覆盖列表、标签目录、空地点/未覆盖客户的处理，JSON 小数按精确十进制读取，Python API 拒绝二进制 float/bool；共同目录与异构目录的参数不能混用；该模型没有退出、距离、开设费、容量或第三设施。
4. 共单例补编译接口：`q,B,u,A` 的字段、显式 (k=1+sum q) 的收费、`decode_ne` 与带区间版本的语义；明确“编译没有求解均衡”。
5. 等重流的抽象接口和三类审计入口；说明无约束流不展开二进制重数，但一般异权时间仍未解决。
6. `verify_phi` 的独立检查合同：重算条件成本、实际偏离、未列布局和默认续局；默认字符串必须精确为 `guarded_repair of all common customers at facility 1`；通过只证明给定实例/证书的合同，不证明菜单最小、实例最优、普遍定理或运行时间。源文还保留了精确 φ 输入限制、默认修复的最大严格改善客户规则、平局按最小客户编号处理，以及零收益时不能除零的边界。
7. 回归命令清单。文件没有附这些命令的本次运行输出，所以不能把命令列表升级成通过记录。

## 与现行材料的比较

完整比较了现行结果分支上的相关归档入口和可检索的冻结来源：

- `archives/facility-games/state/计算/共享目录旁支程序的接口与精确复现--计算.md` 已逐项保存 `shared_phi`、异址精确程序、独立 `verify_phi`、输入边界、默认续局字符串、全规则检查器和“不承担普遍/最优/运行时间主张”的合同；该现行对象比本手册更明确地区分了曾实际执行的模块、缺失依赖和有限审计范围。
- `archives/facility-games/subarchives/common-many/state/审查/结构盒选择与等权流的源版本及接口闭合--审查.md` 已保全 `SC-K-INCIDENCE-BOX-DP`、`SC-K-LOCAL-WEIGHT-BOX-DP`、`SC-K-EQUAL-LIGHT-FLOW-BOX` 的精确量词、参数域、流实现和“无 canonical DP 实装/异权仍开放”的边界。
- `archives/facility-games/subarchives/common-many/state/审查/任意设施数命题登记与证据分层--审查.md` 已吸收任意设施数 README/claims 的完整合同、因子二存在、规范贪心盒存在、共单例编译和 MAX/RANGE 时间责任；它明确把账本登记、数学证明、有限运行和外部审查分开。
- `archives/facility-games/state/审查/三组讲义盲读与更新复查的完整证据边界--审查.md` 记录了同一批设施算法接口的证明范围、有限复算和未覆盖项，可用于核对本手册中的“命令/接口不等于定理”边界。
- 当前 `archives/unrelated-machines/README.md` 仍明确 `UM-TARGET-v1` 及一般反面均 OPEN。来源开头的 UM 研究路由属于历史运作背景；它没有给出新的不相关并行机数学证明，也不能迁移成客户吸引半覆盖结论。

来源所引用的 `research/...` 路径是冻结提交中的历史路径，当前结果分支没有这些旧路径的工作树副本；不应从路径名称推断其现行状态。源文本中设施部分的具体接口和限制与上述现行对象实质重复，现行对象还补充了版本差异、哈希、独立重构和审计边界。

## 独有内容、去向与处置判断

**建议处置：`duplicate`（历史操作手册的内容已被现行设施计算/审查对象吸收）。** 该判断不删除或退休冻结来源，只表示本源不需要再建立新的数学定理。它没有客户吸引半覆盖的定义、证明、反例或六人量词；把其中 `UM-TARGET-v1` 开头的运作提示写入 customer-attraction 正文会造成模型串线。

建议在语义回执中将其指向以下已推送的现行对象：

- `archives/facility-games/state/计算/共享目录旁支程序的接口与精确复现--计算.md`
- `archives/facility-games/subarchives/common-many/state/审查/结构盒选择与等权流的源版本及接口闭合--审查.md`
- `archives/facility-games/subarchives/common-many/state/审查/任意设施数命题登记与证据分层--审查.md`
- `archives/facility-games/state/审查/三组讲义盲读与更新复查的完整证据边界--审查.md`
- `archives/unrelated-machines/README.md`（仅作为历史 UM 路由和 OPEN 边界的交叉定位，不把该源升格为 UM 数学结果）。

若回执系统要求“duplicate”必须保留具体历史证据，可在对应 evidence manifest 中记录本源的两冻结 commit、blob、SHA-256 和上述“未运行命令”的边界；无需再复制 11,534 bytes 到新的数学对象。

## 适用范围与后续

- 本源可支持“历史操作手册曾规定哪些程序合同”的来源追溯；不能支持任何新的普遍设施定理、客户吸引半覆盖结论、UM-TARGET 反面结论或外部文献优先权。
- 现行数学对象已经保留本源中有用的输入验证、默认续局和输出语义；后续 mapper 只需建立来源到这些对象的“来源/版本”边，不需造新的数学边。
- 本草稿未执行源文列出的回归命令，也未检查外部论文；若未来需要运行，应按现行对象的证据入口和独立审计合同执行，并单独登记运行结果。
