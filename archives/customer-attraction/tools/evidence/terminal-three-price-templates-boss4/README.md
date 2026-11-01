# 三价模板与均匀质量证书证据

本目录保留 Boss4 对六个冻结源的逐字导出与隔离重放材料。冻结来源同时存在于 `legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；源文件 SHA 见 `manifest.json`。

`three_price_template.py` 与 `three_price_template_weak.py` 均在隔离目录运行一次并退出0。两者调用 SciPy/HiGHS 浮点 LP，运行输出分别保存在 `replay_strong.stdout.json`、`replay_weak.stdout.json`；弱模板输出与冻结 `source-weak.json` 逐字段相同。模板生成的邻接 JSON 只作复现产物，不冒充原冻结源。

三个 `uniform_mass_*_certificate.json` 是源文件给出的有理乘子记录。本文按其自身字段保存 `rows=800`、`min_exact_slack=0`、`exact_nonnegative=true`；没有生成脚本，不能由 JSON 反推更多历史或客户语义。
