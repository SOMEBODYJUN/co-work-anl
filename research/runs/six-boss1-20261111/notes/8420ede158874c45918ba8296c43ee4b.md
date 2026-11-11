# 根72行：真实第三源重查切面带来的第二条精确根界

Boss1；RUN `six-boss1-20261111`。只写本摘要及 `maximal_root_tail_wallet_v2/`。原71行、全部128型和129列保持，唯一新增已冻结的 requery 切面；一次小型 LP 后，精确匹配原始/未缩放对偶与独立检查完成。

## 结果

原共同目录完整历史纯 SPE 的 actual 根收益满足

\[
\boxed{229185173551068u-23463022015563K-4570807634338O\ge0.}
\]

K 为全目录最大裸大小，O 可取 OPT6；因分支并集帽是零权，O 也可取任意六合法查询的覆盖并。它不是最锐根界、half 或完整 SPE 声明。

在新指定
`K=1125421575458286230366665/6570307807568935468436467`、O=1，root72 必要锥精确最优值为

\[
\frac{56437404288554023143588507160747011241}
{1505817135161623567660845859624137996756}
=0.03747958697687182\ldots.
\]

上一根线在同 K 为 `0.03687655399041506…`，本轮精确提高
`908057404074278075736924821996328401/1505817135161623567660845859624137996756`
≈`0.0006030329864567611`。两线之差为

\[
\frac{469495349990602267375O-209559252391468449011K}
{719032227213871806553080}.
\]

所以 O=OPT6>0、0≤K≤O 时，本轮根线在整个该比例域严格更强。

## 来源、尺度和正预算

[source_review.md](maximal_root_tail_wallet_v2/source_review.md) 独立确认九权 requery 切面对任意准确两行动有序历史后的真实四人续局、任意六合法查询并成立；不需要 C 最大性、原根 u 或旧71等号。取 actual 两步历史时可复制到含 X 的全256原子；这只是来源说明，本包没有加入 actual 联合行。

正预算是根 IC、五尾大小帽、真 SAFE4/SAFE6(Omean)、原 full36 PAIR(Omean,Omean)，以及 requery 新切面。新切面原行的精确权为 `2312374/6366254820863`。浮点求解只将新行除以正数126000；因此 solver 行权需再除126000才是原行权。两个版本都保存在证书，全部129列等价关系精确核验。

整数预算公共分母 `458370347102136` 是显示 primitive 根线 u 系数的**两倍**；证明正文明确支付根行2倍后整体除2。两个自由质量乘子及五个K帽贡献全部保留。全128原子余项13零/115正，u余项0。匹配原始点有10正原子，但不认证SPE。

## 文件和冻结接口

| 文件 | 内容 |
|---|---|
| [proof.md](maximal_root_tail_wallet_v2/proof.md) | 新根线、十整数预算、正确双倍尺度、精确匹配点与比较 |
| [source_review.md](maximal_root_tail_wallet_v2/source_review.md) | 求解前量词推广、原71对接、Knew和缩放恢复说明 |
| [exact_input.json](maximal_root_tail_wallet_v2/exact_input.json) | 原未缩放72行；SHA `86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d` |
| [exact_certificate.json](maximal_root_tail_wallet_v2/exact_certificate.json) | 匹配原始/未缩放对偶；SHA `8b38a322e3b6ddffefee25d3db157e3fbbddb284a4b636143360bd00d4db5b46` |
| [all_129_column_checks.tsv](maximal_root_tail_wallet_v2/all_129_column_checks.tsv) | 全部原子与u的精确原始值和余项 |
| [check_literal.py](maximal_root_tail_wallet_v2/check_literal.py) | 不导入builder、不调用优化器的独立标准库检查 |
| [literal_certificate_check.json](maximal_root_tail_wallet_v2/literal_certificate_check.json) | 全72原始行、131列参数身份、尺度及精确目标PASS |
| [freeze_manifest.json](maximal_root_tail_wallet_v2/freeze_manifest.json) | 最终冻结与全部新工件哈希 |

42个旧来源字节不变。仅一次129列72行LP，未追加后来讨论的30异索引新预算，未重解、未改旧包、Git、RUN或登记表。后续更强系统应独立另建输入并经Main释放。
