# Complete Morrison–Kawamata mission — continuous research

本次存档 `morrison-kawamata-cone`，主问题 `MKC-ULTIMATE`。完整任务以 `state/mission_original.md` 为准；先读 `state/definitions.md` 和最新 `state/research_status.md`。唯一完成标准是任意维数、绝对与相对、nef 与 movable 及两项双有理有限性全部严格成立。不得把相对维数 ≤2、三维、K3、阿贝尔或某变形类型替换成主目标。

用户已授权使用所附仓库外 `githubtoken.txt` 为 `SOMEBODYJUN/co-work-anl` 认证、读取、修改研究、提交并推送 `rebuild/research-v2`；按当前会话实际授权执行。Token 只经 `--token-file` 使用，不输出、不写入仓库。

新对话用当前 `work.py` 和附件实际路径启动自己的独立 clone：

```sh
python <work.py> --repo <独立clone> start --actor <Boss编号> --role boss --save morrison-kawamata-cone --branch rebuild/research-v2 --token-file <仓库外githubtoken.txt>
```

进入返回目录后只用根 `work.py`。读 `AGENTS.md` 与 `prompts/research-runtime.md`。新 Boss 取唯一 RUN，把本档 `research-spec.json` 复制到 `research/workspaces/<RUN>/spec.json`，执行 `research studio init <RUN> --spec ... --expect-branch rebuild/research-v2 --expect-remote https://github.com/SOMEBODYJUN/co-work-anl.git`。恢复同一 Boss/RUN 用 `start --resume` 和 `studio status`，不覆盖别人工作室。

Main 看超边和短回执；最多三个子代理槽按用户实际设置使用。idea 线提出能检验的全维数路线及替代；执行线实读原文、沿完整 ALL 前提做证明与计算；障碍线构造满足全部假设的反例或排除具体错误桥。尚有缺口时至少两条线做实质推导、反例或替代构造，最多一条定点文献/证明核对。派工写清要证或反驳的精确命题、可用前提和数学交付；不反复派“再审全文”。

旧 `RMKC-STRONG-REL2` 属受限子题。先读其精确假设和版本，不把旧 accepted、内部通过或编译 PDF 当成全维数输入。既有定理保原作者和条件。Li2023的有理包、弱域与用户实际有效锥目标分开。任何商空间提升、非零相对不规则度、有限覆盖下降、klt/terminal 归约及非 Q-factorial 扩展都须付清证明义务。

研究持续执行“选具体缺口→推导/构造/必要计算→定点文献比较或非作者核验→把新证据用于下一步”。存在缺口就继续实际做数学。普通成果及时写本线 journal，并由 Main 串行 `research save` 或 `studio line`，再 `checkpoint`；关键可复用成果按已有冻结/非作者复核/登记/超边流程回流。保存或推送不是数学停机条件。上下文接近上限先保存完整推导和精确断点，再用 fresh 子代理接续。

符号计算、格点和退化面实验使用真正可用的 Python/Sage/SymPy 等；大计算按当前 `work.py compute --help` 与 `work.py github --help` 调用实际有权限的远端资源，并取回日志、输入和精确证书。不得把请求排队、有限枚举或工具成功当作一般性证明。没有承重计算需求时不空启云机器。不要求 Lean/Coq。

不得因“完成了一个阶段”“资料已齐”“成果已推送”或“已做几轮”宣布主问题完成。用户叫停或平台真实阻断时，保存实际已证最强结论、精确未证步骤及可执行接续点；不得编造已达到资源上限。不能解出时诚实报告 PARTIAL/OPEN，不得虚构证明或原创性。
