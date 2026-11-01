# R-31bbb saturation projection cleanup（2026-10-31）

本包保存六个源的 clean-show 原文、源 SHA/大小清单、源码编译和三次 LP 复跑，以及有理 projection witness 的独立复核。所有原始 stdout/stderr 均在 `clean-show/`，复跑在 `replay/`。

## 结果

- AP m=5 一般 mask：1023 variables、450 rows、HiGHS status 0、objective `2.3158682560504453`。
- AP m=5 对称 mask：32 variables、450 rows、objective `2.3158682560504418`。
- 指定 maxima 的 BNS 对称投影：32 variables、930 rows、objective `2.225443383452107`。
- `exact_projection_witness.py` 用 `Fraction` 审计恢复的有限支持：W=1、comparison union `3311537042/1488034729`、gap over 2W `335467584/1488034729`；50 floor、400 AP、250 BNS 行全部通过，最小 AP slack `6484381029/74401736450`。

这些是 necessary projection 的有限结果。没有 continuation tree、支付或 SPE 证书；有理 witness 只证明行约束可同时满足而投影并集超过 2W，不能称原模型 half 反例。

`validation.json` 为 `passed=true`。验证器检查六个源的冻结 SHA/大小、本地副本、两个 Python 源的 `py_compile`、三次 LP 的 status/行数/目标以及有理 witness 的精确字段。
