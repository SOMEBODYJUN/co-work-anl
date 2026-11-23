# Pro 2：攻原定理，严格 G1–G8 验收

本次身份 Boss3。实际目标是证明原题，不能止于建议或综述。

我授权你使用本次上传的 githubtoken.txt 对 SOMEBODYJUN/co-work-anl 认证，自行克隆、同步、修改本题研究文件、登记、提交并推送 rebuild/research-v2，无需逐次请示。Token 放仓库外，只通过 --token-file 使用，禁止输出或提交。后续只用 clone 根 work.py；不要恢复旧公屏或阶段队列。

用附件实际路径执行：
```sh
python <work.py路径> --repo <本Boss独立目录> start --actor Boss3 --role boss --save relative-mk-cone --branch rebuild/research-v2 --token-file <仓库外Token路径>
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

先读 `state/problem.md` 与 `state/acceptance.md` 的不可变合同，再读 Pro1 的实际交接及未付义务；资料未齐先补读，不把 INTAKE_READY 当数学正确。先检查截至执行日是否已有完整证明，避免重新包装为原创。

主目标：任意复数域 terminal Calabi–Yau 纤维空间 f:(X,Δ)→S，X正规射影Q-factorial，K_X+Δ≡_S0，dim X−dim S≤2；对 C=overline(Mov)(X/S)∩Eff(X/S)，Gamma 为 PsAut(X/S,Δ) 在 N¹(X/S)_R 上的作用像，构造有理多面体锥 Pi⊂C，证明 Gamma Pi=C，并满足 Li–Zhao Definition3.4 的强基本域分离与平凡稳定子。不得添加非退化、Q-factorial基底、K3、绝对维数或特殊变形型条件。

从 frontier/context 选完整 ALL 路线，执行者逐条读正文、核假设及证明；idea 线可提出替代路线，障碍线严格审查。每个关键引理给完整证明及边界检查。重点攻实际有效锥上的弱域、稳定子和线性部分；商域存在不能自动提升。若路线受阻，保存最小缺失引理并继续攻它或寻找反例。抽象剪切锥反例不是几何反例；必须核齐原题全部几何假设和真实群作用。

不要把已有论文结论、条件结论、数值/有限证据、复核一致或 accepted 边当作主定理已证。完成以下六个真实文件，统一存于本 RUN 的 manuscript/，成熟正文再回流本存档 state/：main_theorem.tex、proof.tex、literature_audit.md、counterexample_audit.md、research_paper.tex（完整英文）、verification.md。

最终第一行严格为 `✅ PASS` 或 `❌ FAIL`；逐项列 G1原创性、G2一般性、G3全覆盖、G4强基本域、G5退化情形、G6完整证明、G7独立核查、G8英文论文的证据。全部为 TRUE 才能 PASS。发现反例或达到真实资源界限均报原证明任务 FAIL，明确哪些已证、哪些未证、最小障碍、潜在反例及可核文件。持续保存可让下一对话接棒；不得伪造完成。
