# R-18 terminal clone equality 续审计

`cd13e15cb52e71489d07` 是 two-topic equality family 的定义级 exact audit。它对 `m=2,...,10` 构造客户重数 `(m−1)`（主题 A）和 `2`（主题 B）的五人式路径策略，调用 `verify_certificate` 检查完整历史证书，并验证 `2u_i=u_last`（前 `m−1` 人）、`2W=(m+1)u_last`。源字节 SHA-256 为 `ceb078193388d6f64da717b98faca31b16637c9e3e9ff1efee78dd1f981e8f`。

实际回放退出码 0：m=2..10 的 `histories=deviations=3,7,15,31,63,127,255,511,1023` 均 `valid=true`，且每个 `W=OPT=m+1`，收益为前置玩家 1、末位玩家 2。m=5 的独立证书与实例源（`d0088fa6d8d70b075c79`、`8d2e492dc71fd54c3106`）逐字保留，分别为 31 个完整历史动作和 5 人、6 客户的两主题实例；SHA-256 分别为 `48ba182bfd1500865dd10c9eaff9231bb50a546140c74e7cedfdb855e49d9b67` 与 `b859259c8337896ed8f0d5e66271f1685cfa8f546ce45891399c5c6c9f950afb`。

这是有限 exact regression 和定义级族证据；README 所称一般等式证明仍依赖解析推导，不把 m≤10 枚举升级为任意 m 定理。它也只说明 W=OPT 的 equality family，不能提供 half 反例。
