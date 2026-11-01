# 实际末主题三人尾投影的含交集审计器证据

主源e64b0160f4a4aebd598b；正式对象为[实际末主题三人尾投影的含交集审计器](../../../state/程序/实际末主题三人尾投影的含交集审计器--程序.md)。保原1416B父方程序及本次原入口的一次真实执行，复用先前已保存的作者表、旧点和知情独立重构，不重复其数学运行。

## 原件和共享输入

original/audit_tail3_B_projection.py为正常clean show取得的完整原字节，SHA-256为51fe3c73f7c394ce14517678b31dbd72d3c1e08aa5221728d93c7bdf74a67462。冻结源位于research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/audit_tail3_B_projection.py，68fad804ec5946cb296f77dc5b336308a66abf12及aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c两提交同字节。

原程序只实际读取两份数据，本包不复制第二份：

- [作者448表](../tail3-B-projection-program/related/tail3_B_projection_certificate.json)，源ef49ddbe23cec45b1352，36617B，SHA4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df。
- [旧1033点](../tail3-B-projection-program/related/full_new_reply_closure_exact.json)，源9e51f2c756ebb1a91fbf，56652B，SHA24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11。

完整源码、448表及证书字段已实读；旧点实际用于计算的全部16hist和元数据已读，其他194个new-reply及K列不由本程序核查。相关3075B生成器、4806B数学稿、原审查稿/403B历史review、上轮独立核验器及报告、当前联合图程序/对象均实际读过，阅读时态和各自运行身份在正式正文保留。

## 本次唯一原入口

run_original_once.py先核冻结代码及两份数据SHA，将其复制到clone外临时根的原相对路径。原审计器向上寻找work.py祖先；包装器复制本仓库40777B work.py作为路径标记，SHAf64c1c23affad048f7d0966982ca0ec07998c0b85f3f4d2606e5008e76e4f901。该标记既未被导入也未执行，不承担数学计算，不需要复制凭据。

原1416B脚本没有main保护，导入即执行；本次只用独立进程执行一次，未先导入探测。Python3.12.14、-B、assert开启、退出0、stderr0B；stdout223B，SHA739b8ed44049d76d84e0a57f01d6c0a8ba89aac96313cf211c87f36b8a74e759。临时布局删除，所有输入前后字节不变。

rerun/stdout.json保原stdout字节；rerun/stderr.txt为空；rerun/execution.json保实际argv、路径、时间、原程序输入与包装器比较输入的不同角色。运行在只读阶段于clone外完成；写入开放后归档，不为改路径重跑。

包装器按参数顺序接收：原脚本、作者证书、旧点、work.py路径标记、历史review、上轮独立报告、新输出目录。最后三项中的历史review和上轮报告只由包装器作结果比较，未复制进原程序布局；原审计未读取它们。新输出目录独占创建，避免覆盖旧运行。

## 四字段结果及历史报告差别

原stdout实际为states=21504、visible_types=448、point_value=-76248331950086821053066283859725637/10861094041779216693185920113322280、old_sha256=24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11。

历史tail3_B_projection_review.json在actual-last-theme-families-and-menu-prices-primary的related-small-original下，403B、SHAb7f89f0eb5ab9ba1ecc03302f637a73fb02ad16ad78231bc6a1988338f6f01bc。它另含status和review_scope，数学字段名部分不同。本次只核以下对应值，不声称逐字节复现：states↔raw_states_with_overlap，visible_types↔visible_types，point_value↔old_point_value，old_sha256↔old_point_sha256。原脚本本身只打印四字段，不写历史报告。

[上轮独立报告](../tail3-B-projection-program/independent-audit.json)SHA544aede7b50eae50d02293e06974f913203d8f528d7a1a3e1592aac137ca6758，四个对应核心字段同样一致。其21504状态、h抵消、端点与全域、16hist及8正边缘贡献由上轮知情实现承担。本任务未重跑该代码，也未重跑3075B投影生成器或联合5108核验。

## 界限

原程序从S/Z/V含交集式枚举，核全部448格的完整隐藏域最大值，再核指定旧边缘负值。它没有单独测试ell端点，不验证旧1033行、完整策略或一般half；不校验证书weights/domain/status，也只打印实际旧SHA而不与证书哈希字段作等号断言。当前包装器新增的SHA及字段一致性检查不能写成原源码已有。

21504=64×4×C(9,3)是局部会员计数状态，不是游戏或策略数。负投影只排指定旧边缘的隐藏完成。普遍必要行仍依赖同一完整SPE上八族真IC及max上包络证明，详见正式正文；后续K投影与Yi菜单价有不同合同，当前PASS不覆盖它们。
