# 单隐藏末回复的配对投影恒等式：证据说明

主源 `99fc07ef9726df36da2b`，冻结路径 `research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/tail_r1_pair_identity.py`；两冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`、`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 同字节。原件561B，SHA256 `f5f11fe5eb3627e527900b40d3320e1bb0a13484c7eff65e442da1bf4175a403`，blob `21b868ffeb2cab135174b85b376c1673c7407d16`。

[数学与程序正文](../../../state/程序/单隐藏末回复的配对投影恒等式核验程序--程序.md)自足说明变量、40值、一般解析证明、三真实IC、全部程序合同和有限证据边界。源码的r=1表示倒二源之后的一次隐藏末回复，Q=actual B。它不是完整SPE枚举或half验证器。

| 文件 | 职责 |
|---|---|
| [original/tail_r1_pair_identity.py](original/tail_r1_pair_identity.py) | 未改完整561B原源，顶层40态Fraction断言；导入也会执行。 |
| [run_original.py](run_original.py) | 本次透明单子进程记录器；不导入或重写原数学循环。 |
| [rerun/execution.json](rerun/execution.json) | 一次实际入口的argv、Python版本、断言开关、退出码及前后SHA。 |
| [rerun/stdout.txt](rerun/stdout.txt) | 原116B输出；Python dict repr，不是JSON。 |
| [rerun/stderr.txt](rerun/stderr.txt) | 原空stderr，0B。 |
| [manifest.json](manifest.json) | 主源、实读比较材料、交付物SHA与运行责任。 |
| [self-check.json](self-check.json) | 静态SHA、语法、输出合同、全部正文链接及回执目标自查。 |

本次原入口只运行一次。它精确检查 `p∈{0,…,4},a,b,z∈{0,1}` 共40外态，每态最小化y=0、1共80候选；输出states40、exactTrue，exit0，stderr为空，源前后SHA相同。运行时用普通Python `-B` 且清除子进程 `PYTHONOPTIMIZE`，保留assert。没有额外导入执行，没有第二遍本源枚举，没有跑旧网格、mixed、portfolio、图优化或原SPE求解器。事件中的scratch路径是当时执行路径，归档后不改写为虚假的归档执行事件。

本包不增设重复40态的第二实现；正文直接推出任意p≥0时 `H₁−H₀=−a/D` 及完整余项 `a(1−y)/D`，一般真值由这一解析论证及真实三IC承担。40态是原实现的有限回归核验，不是一般量词的唯一根据；40格数值表是解析公式的完整展开，不另记为一次程序运行。

如需在新环境重放，选一个尚无execution.json的输出目录后执行：

```sh
python -B run_original.py original/tail_r1_pair_identity.py /new/empty/output-directory
```

记录器拒绝覆盖已有事件以免静默重复原入口。新重放会产生新事件，不能冒称本次已保存事件。直接运行原件也可以，但使用 `-O` 会删除assert，仍可能打印exactTrue；这样的输出不能继承本次断言结论。

实读比较包括原 `shared_terminal_portfolio.md` 全文、原 `review_terminal_portfolio.md` 全文、research_5阶段README全文、五人 `PROOF_ZH.md` 的§1—§2及相关强PAIR段；另全文读完整模型、三份局部引理、旧网格和mixed程序正文及2908B通用priced核心。原稿的多查询/多人尾审查数字和其它阶段图均仅作为比较，不算本任务执行。checkpoint manifest及逐文件verification只核此源记录，未将文件清点冒称数学重放。共享比较文件只在manifest记录既有路径与SHA，不复制大型证据包。
