# 十八主题保底保护松弛的原审计

[正式计算对象](../../../state/计算/十八主题保底保护松弛的精确审计--计算.md)自足保108单位客户、18根、三收益10/12/12和末位21的严格偏离；全部18原表、程序副作用、九报告字段、相关解析推广及后来逐人反族纠错均在正文。

original保1647B源码和4155B原表。唯一新原CLI在隔离runtime直接以正常assert运行，约0.066244秒、exit0、stderr空；新表逐字SHA e3937fa5f1e0138383a07df35272c1cfcee1750145d475bbead5bbb23c0b03ad 同冻结，源前后SHA同。replay保原始真实事件与输出；runtime代码是original的精确临时副本，不额外提交第二份。0独立重复数学扫描、0SPE/DP/LP。

复现入口是run_original_once.py，三个参数依次为original/audit_floor_only_protection.py、original/floor_only_protection_audit.json、一个尚不存在的输出目录。它拒绝已有输出目录，复制源码到其中再执行。原源码在模块顶层运行、无CLI参数，导入也会执行并覆盖自身旁同名JSON；请勿把原件目录作为可写运行目录。包装器不替换任何helper，也不负责一般m的解析控制器。

manifest记录两主源及实际相关阅读；self-check仅作原字节、指纹、JSON/AST、元数据和本地链接静态核对，不是另一遍收益计算。源中noncredible/no-SPE身份始终保留，passed只表示固定有限断言通过。
