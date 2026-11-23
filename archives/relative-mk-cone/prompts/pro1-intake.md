# Pro 1：文献、数学对象和超边，一次持续完成

本次身份 Boss1。任务是资料建设，不是宣称证明成功。

我授权你使用本次上传的 githubtoken.txt 对 SOMEBODYJUN/co-work-anl 认证，自行克隆、同步、修改本题研究文件、登记、提交并推送 rebuild/research-v2，无需逐次请示。Token 放仓库外，只通过 --token-file 使用，禁止输出或提交。后续只用 clone 根 work.py；不要恢复旧公屏或阶段队列。

用附件实际路径执行：
```sh
python <work.py路径> --repo <本Boss独立目录> start --actor Boss1 --role boss --save relative-mk-cone --branch rebuild/research-v2 --token-file <仓库外Token路径>
```
进入返回的 clone，读 `AGENTS.md`、`prompts/research-runtime.md` 和 `archives/relative-mk-cone/README.md`。本存档已创建，不使用六人子档。

给自己的 RUN 选唯一 ID；把 `archives/relative-mk-cone/research-spec.json` 复制到 `research/workspaces/<RUN>/spec.json`，按已登记且实际有关的目标选择 seed_ids，其他原题、定义、范围和 SHA 不变。执行：
```sh
python work.py research studio init <RUN> --spec research/workspaces/<RUN>/spec.json --expect-branch rebuild/research-v2 --expect-remote https://github.com/SOMEBODYJUN/co-work-anl.git
```
新 Boss 使用自己的 RUN，不写 Boss2 的工作室。Boss1、Boss3 是本新存档的建议分工编号，不是程序自动分配：启动若发现该编号已有其他实例，不得用 --resume 冒领，改用新的明确编号并同步替换命令。同身份真正恢复时才用 start --resume 和 studio status。

独立线只拿新 RUN 的原题与中性 model_input；不给 Pro1 文献、候选路线或其他线的推导。资料建设阶段不必假设已启动盲线。

Main 看相关超边及短回执，工作者读原文、提 idea、做推导和复核；Work 中如实际调用子代理，最多三个。上下文将满先保存准确断点，再开 fresh worker（fork_turns:none）。不要假称已启动 Pro 或后台任务；没有子代理工具时由当前研究者分阅读轮次完成并照实记录。

有用推导、失败、证据和下一步持续写各自 journal，使用现有 research save / studio line。Main 串行 checkpoint 指定路径，只有返回 pushed 才算远端保存；认证失败先 --local-only。成熟结果按准确冻结版本交非作者复核，再按 studio promote 返回的命令 register、校验和 checkpoint --review-plan。保存未完笔记不需要等待成熟。先同步，保留其他存档和并发增量。

先读本存档 `state/problem.md`、`state/definitions.md`、`state/intake_contract.md`。原题是：证明所有相对维数≤2的 terminal Calabi–Yau 纤维空间的**有效相对可动锥**有强有理多面体基本域，不假设闭可动锥非退化、不假设基底 Q-factorial，不限制绝对维数、K3 或特殊纤维类型。

一口气推进“收集并实读原文→精确登记数学对象→建立有推导证据的 ALL 超边→新读者接手”，不要停在文献列表。首先完成 Li–Zhao v8及正式版、Li (II)预印本及2026期刊版、Moraga–Stark、Faucher及已发现承重引用和后续研究的核查。版本、URL、下载状态、原字节 SHA、定理/定义编号、完整假设及证明位置必须真实；缺失正文明确记缺失。

重点分别处置弱→强、Mov_+→有效锥、闭包线性部分 W→有效锥线性部分 L、商群作用核，以及零边界推论→一般 log pair 的适用性。完整共同前提保一条 ALL 边；未证桥为开放义务，条件边不消债，有限例子不升级为定理。已有结论也登记其准确范围，不冒充原创。

只用现行唯一 registry 和 map/edges；登记的是当前完整候选总表，不得用本题小批次覆盖全库。交付可读取的正文、资料清单、对象/边、精确未付义务及给 Pro2 的短交接。按 intake_contract 验收，最终只报 INTAKE_READY / INCOMPLETE / BLOCKED；这三个状态都不等于 G1–G8 PASS。没有读全必要版本或承重资料，不得报 READY。
