# 调和末对钱包：原件、先验与一次原审计

本目录支持[调和复制付款引理](../../../state/引理/同一实际福利对末对钱包的调和复制付款--引理.md)和[原审计/审查身份计算对象](../../../state/计算/调和末对钱包的原审计与审查身份--计算.md)。

## 本批来源

Boss4确认5源claim pushed `c201c14b2a6773b8706f7464c6f22f4c0288e649`、synced。正式确认后重新完整读取五主源并核库存SHA，原件按完整仓库相对路径放在 `original/`。两个冻结提交位置均核字节相同。

|ID|文件|字节|
|---|---|---:|
|f811c6617841fee2c723|round9/exchange/harmonic_terminal_wallet.md|4680|
|70c3ea6d4f224667baf7|round9/exchange/audit_harmonic_terminal_wallet.py|4111|
|24605d29e47dc547a839|round9/exchange/harmonic_terminal_wallet_exact_audit.json|2487|
|1deb05327659c64eae69|round9/credible/review_harmonic_terminal_wallet.md|1544|
|1a2500b24700429ddb8f|round9/exchange/README.md|2154|

五源14976B，共同源前缀 `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/`。完整blob/path/SHA/双commit/角色在[source-manifest.json](source-manifest.json)。比较原件和运行依赖都不额外done。

四个真实运行依赖46744B：round8钱包审计源码 `3beb17d5735520b90e84`、旧52完整实例/动作 `a7579960b289fff40c97`、1953实例 `ff1a437e39e730d230eb` 与完整动作 `be317a14860bf5650dfe`。所有必要本地blob现成，提取设置GIT_NO_LAZY_FETCH=1，不触发认证或查备用凭据。原件已全部核同SHA并保完整字节，详见[runtime-input-manifest.json](runtime-input-manifest.json)。

## 唯一新增原入口执行

原HW主程序与四依赖置于独立 `replay-tree/` 原路径，保importlib相邻模块路径和round8的ROOTparents6。HW main实际运行一次，exit0、0.8558840751647949秒、stderr空；代码及输入前后字节未变。新2487B报告与原冻结JSON逐字节相同，SHA
`d2b90892178ffcaebd90d23c636e72e6a680e9a3a3bbdd0110096af3dca4a61a`。

[execution.json](replay/execution.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[新报告](replay/harmonic_terminal_wallet_exact_audit.json)与旧报告分开保留。新入口调用round8的audit函数两次，每例再调loader一次：总四次loader、总1812项含自身IC、继承12条末对查询，再核COPY/CLIENT/HW/REFUND。没有调用round8 main，没有运行弱Q LP或peer程序。旧批只import/load或只读未运行的身份不回填。

两例分别m4/52客户、m3/1953客户；C'为0及496/3，REFUND为47及8671/9。没有五人游戏fixture，报告m5字段只有H5求和与两项有理字面量，准确代数关系由一般证明/审查核实；非五人SPE测试或half证明。

## 全文比较与审查先验

八份comparison-only原件均全文读并保存：menu9审查、原root陈述重构、weak-Q攻击py/JSON、peer_component_reviews、最优交换曲线、根响应协方差/背景域、round10直接静态吸收接口。它们不额外登记完成。

credible9本批主review是读作者全文后重构，明确非盲、未跑原审计；menu9是先收候选消息/读稿前重构、后核精确退款；root是先陈述重构、收到menu确认后再对稿。三种先验不合并为全盲审，本批读后复现不改历史。peer审查只对credible稿§1/§3核代数/背景后果，不冒称重审其旧完整证书；两份弱Q浮点infeasible输出也无精确对偶。

全仓冻结Markdown按HW/原文件名检索后，读到round10 `direct_terminal_surplus_and_early_gap`：静态S+|A\B|/m吸收C，使直接half接口无需单独使用HW，但EARLY仍未付。新引理保完整对比和DIRECT等式，不将后接口重排视新资金。当前末对钱包、循环污染条件调和付款、强指派反例与弱匹配资源均全文比较；五人定理/六人问题只核模型状态，未重审全证书。

新正文完整保全COPY/CLIENT/REFUND、A∩B退款、m2/零域、m5正余额和m6不足；钱包已经使用同一actual早期行与末对利润，不能叠加给另一银行。一般弱指派、早期全树付款和六人目标未由本批升级，原五人OPEN标签按当前另证状态分别处理。

工作区有5条semantic receipts、self-review、relations、next候选及checker。checker只核字节/链接/记录，不再运行数学原程序；[verification.json](verification.json)与人的数学自查分别承担证据。

上一批非必要非MD检索在中断后报 `Proxy CONNECT aborted`、exit130；未观察到目标HTTP认证挑战，也未重试/换凭据。完整非秘密错误、观察阶段及边界另写在本批工作区 `prior-read-network-boundary.md`，不将其误称本批必要来源缺失。
