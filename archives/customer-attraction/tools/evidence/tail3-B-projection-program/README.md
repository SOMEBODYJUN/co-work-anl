# 实际第四步B分支的三人尾投影程序证据

主源0eede36b323de30ee462，正式对象为[实际第四步B分支的三人尾投影程序](../../../state/程序/实际第四步B分支的三人尾投影程序--程序.md)。完整程序、原448系数表、其唯一旧点数据依赖、原父方审计器、当前原入口输出和独立重构分别保存。

## 冻结来源和实际阅读

下列原件通过Boss7正常clean show取得，当前文件逐字节核对。主源在68fad804ec5946cb296f77dc5b336308a66abf12及aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c同字节。研究工作区R5662为research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1，旧点则在R-c4f1ef099fad483c9f81283b61eb0b53/six_astra。

| 本包路径 | 源ID | 字节数 | SHA-256 |
| --- | --- | ---: | --- |
| original/tail3_B_projection.py |0eede36b323de30ee462|3075|63677e14e8c9f257b32f385642bfdf47c71932ce7b251c5970013cf1993c6d01|
| related/tail3_B_projection_certificate.json |ef49ddbe23cec45b1352|36617|4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df|
| related/full_new_reply_closure_exact.json |9e51f2c756ebb1a91fbf|56652|24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11|
| related/audit_tail3_B_projection.py |e64b0160f4a4aebd598b|1416|51fe3c73f7c394ce14517678b31dbd72d3c1e08aa5221728d93c7bdf74a67462|

3075B程序和1416B审计器均全文实读。证书全部8顶层字段、64实际位×d0…6的448有理系数全文读完；没有只看schema或正支持。旧点全部元数据及16个被原程序访问的hist完整实读；其他194个new-reply列及K列未被这个投影器使用，本任务不冒其全部语义审计或1033行重放。

4806B原数学稿6c1d35e3c1089f382432、原审查稿aaef98293a6b1434c64b和review JSON dc4b55af2246c76b838c亦完整读取，现有冻结副本在actual-last-theme-families-and-menu-prices-primary包中复用，不重复持久复制。正式旧上包络、三源K投影、条件联合及菜单报价对象均全文比较。当前combined_branch_master.py全文读，确认联合build只调用table()而不读取旧1033点或已导出证书。

## 一次原入口执行

run_original_once.py在执行前核三件源码/旧点/冻结表SHA，将源码和旧点放入临时根下原相对布局，以满足源码固定parents[5]的ROOT合同。运行未修改的原CLI一次，参数--export，Python3.12.14、-B、assert开启；没有调用发现LP或父方审计器。

实际退出0、stderr0B。新36617B证书与冻结原件逐字节相同，SHA为4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df。stdout906B等证书除table外的全部字段，SHA为bd22d8e2e78e43681eb84b96af00d6d88757d24f24d7260a735020e93b1c5b0c。来源文件前后SHA不变，临时目录已删除。

rerun/execution.json保实际argv、隔离路径、输入路径/大小/SHA、时间及比较结果。该执行在本批clone只读阶段于clone外完成；写入开放后将当时字节归档，没有为更换日志路径再运行一次。run_original_once.py按NEW_OUTPUT_DIR独占创建输出，避免覆盖既有运行证据。

如需将来另一次有意复现，可从本证据目录执行：

```sh
python3 run_original_once.py original/tail3_B_projection.py related/full_new_reply_closure_exact.json related/tail3_B_projection_certificate.json new-rerun
```

原程序本身的默认CLI不写表，--export仅在目标不存在时写表；本包不应直接运行original目录下的原源码，其ROOT路径也不是原工作区布局。应由包装器隔离恢复布局。

## 当前独立系数重构

audit_raw_menu.py不导入任一原程序，按S/Z/V的未消交集式遍历21504个可行h状态，覆盖12544个(q,r,ell)状态与448个可见格。每状态G的h抵消；每可见格的完整最大值、ell端点最大值、冻结表值全等，原表顺序亦等。

旧16hist当前核非负、八桶计数与d、总质量1；10正hist合8正可见边缘。独立投影值严格为

`-76248331950086821053066283859725637/10861094041779216693185920113322280`。

independent-audit.json保全部16hist、8正边缘质量/系数/贡献、状态计数、SHA及未认证范围；代码SHA为813b053d3d99e2dcd5df5bf32915579f815c74a20bf67260227e5ffee6adff67，报告SHA为544aede7b50eae50d02293e06974f913203d8f528d7a1a3e1592aac137ca6758。实际只执行一次，结果PASS；后续持久化与自查未重跑该数学循环。

可独立重现而无需旧LP环境：

```sh
python3 audit_raw_menu.py related/tail3_B_projection_certificate.json related/full_new_reply_closure_exact.json new-independent-audit.json
```

原程序本身只算消过交集的系数，不能冒它进行了21504含h检查；这里单独的知情实现承担该项。本任务读过原父方审计器但执行次数0。

## 使用边界

普遍结论来自同一完整策略上的八族真IC及max上包络，系数枚举仅核展开。最大赋值不必都能由完整SPE实现；该放松仍包含全部真客户。负值只排这个旧边缘，当前未读1097/3889扩展原件、未重核旧1033行、未求新联合LP、未输出完整策略或half定理。

联合图只要调用table就不需要旧点数据。actual2/3/4保K投影、后来Yi菜单价格以及完整156目录的真实尾停界都是不同对象，不能以当前表PASS替代它们。正式正文完整保实际分支、各分母、量词、隐藏交集消去、原CLI行为、后续接口及接续范围。
