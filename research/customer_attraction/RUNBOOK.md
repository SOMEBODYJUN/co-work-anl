# 顺序客户吸引：三角色的启动、通信与保存

本轮只保留三个当前角色：[Boss](BOSS_START.md)、[清洗者](CLEANER.md)、[整理者](EDITOR.md)。
共同目标是 `Q-CAG-HALF`，存档 `customer-attraction`；根目录 `work.py` 是完整统一程序。
程序不规定研究方法、团队规模、路线名额或探索审批。

## 新对话启动

给新对话相应角色提示词，附最新版根 `work.py` 与仓库外的 `githubtoken.txt`。
由 agent 根据本对话附件清单确定实际路径及独立 clone 位置，执行附件程序的 `start`。
命令必须显式带 `--save customer-attraction`、角色 `--role boss` / `cleaner` / `editor`，
首次带外部凭据实际路径的 `--token-file`；需要恢复新目录时用 `--repo` 指定实际位置。
这些参数由 agent 填入，用户不需要手动改程序、填写身份或猜测路径。

先检查当前目录、`git status`、分支、origin 与远端。保留未提交成果；
已绑定其他存档的 clone 保留原绑定，为本题另建独立 clone。
一个独立 Work 对话对应一个 clone；成果统一进入 `main`，不另建研究分支。
首次身份由程序自动生成 `R-` 加完整 UUID；同一 clone 接续复用本地 `wcg.actor`。
只有确实接续远端已有同一身份时才使用 `--resume`，新对话不接管同行编号。
凭据留在 clone 外，不写入 remote URL、正文、公屏、日志或 Git。

仓库已恢复且凭据已绑定后，可在仓库根启动或接续相应角色：

```sh
python3 work.py start --save customer-attraction --role boss
python3 work.py start --save customer-attraction --role cleaner
python3 work.py start --save customer-attraction --role editor
```

以上是三个角色的可选启动方式，每个独立对话只使用自己的那个角色。
核对启动回执：`branch=main`、`save=customer-attraction`、正确 clone 和本人工作区；
`research_entry=research/current/customer_attraction/README.md`；
`research_prompt=research/customer_attraction/BOSS_START.md`；
`research_runbook=research/customer_attraction/RUNBOOK.md`；
`role` 与 `role_prompt` 对应所选角色。恢复后使用仓库内根 `work.py`，不用旧附件继续操作。

## 阅读与研究

先读根四入口和适用 `AGENTS.md`，再读本题[模型](../current/customer_attraction/model.md)、
[数学地图](../current/customer_attraction/README.md)、[当前前沿](RESEARCH_STATE.md)、
[精确账本](CLAIMS.md)和[失败机制](FAILED_ROUTES.md)。后续沿当前证明义务按需读原文、审查和审计。

Boss 直接带团队研究；清洗者检查并整合可复用资产；整理者评估成稿并表达贡献。
三个角色可以直接合作，半成形思路也可交流，注明猜想、观察或草稿即可。
成熟结果的独立攻击用于准确升级状态，不是探索或普通候选保存的前置审批。

## 日常通信

在仓库根运行，程序复用本 clone 的身份、凭据和存档：

```sh
python3 work.py sync
python3 work.py read --limit 30
python3 work.py inbox --json
python3 work.py workspace
python3 work.py pending
```

发公屏使用 `send --thread '精确数学主题' --text-file`，其后传实际消息文件路径；
回复可用 `--reply-to`，提及用 `--mention`。私聊使用 `dm --to` 指定实际同行 ID，
有正文时加 `--text-file` 和实际路径，无正文只读取双方私聊。
`visit` 后跟同行 ID，只读访问其已推送桌面；`ack` 后跟实际读完的消息 ID，只表示已读。
长正文通过文件传入，避免 shell 转义损坏公式。

公屏默认不混入私聊，但这不是仓库级保密机制。跨存档合作须显式开新消息并标明数学来源；
旧 pending 的重试保留原 ID 与原存档，不把它重新解释成本题消息。
subagents 由本对话 Boss 汇集成果，不冒充独立 Work 身份，不各自推送。

## 文件、检查与 checkpoint

可复用证明放 `research/current/customer_attraction/`；
候选和开放义务放本题已有 `research/questions/` 位置；
审查、规范程序、输入、证书及冻结运行沿本题现有目录保存。
本轮短期个人材料位于 `research/workspaces/customer-attraction/<actor>/`。
共同地图和精确登记沿 `research/GROWTH.md` 与 `research/REPOSITORY_GUIDE.md` 更新。
同一数学内容优先修订既有资产；原始来源和冻结证据不原位重写。

修改对应的数学或程序后，运行实际覆盖该变化的精确审计、边界测试与回归；
结构登记按需重新生成，再核对：

```sh
python3 research/build_catalog.py
python3 research/build_map.py
python3 research/build_crosswalk.py
python3 research/build_catalog.py --check
python3 research/build_map.py --check
python3 research/build_crosswalk.py --check
python3 research/check_active_research.py
python3 research/check_assets.py
python3 research/check_wc_assets.py --check
python3 work.py checkpoint -m '具体成果与准确范围'
```

依赖生成结果的检查顺序执行；不要并行运行目录生成与资产检查。
有限审计不能代替一般证明。候选可以按候选保存，保存不升级数学状态。
默认 checkpoint 只选择本存档的已登记范围、共同登记和本人的桌面；
修改默认范围外文件时，在 checkpoint 中显式列全本轮应保存路径，
因为显式路径会替换整个默认范围。不能把他人桌面或别题草稿顺带提交。

真实冲突保留双方并按内容处理，不 force push、不自动选 ours/theirs，不另开研究分支逃避合并。
只有回执 `status=pushed` 才报告远端已保存；核对提交包含本轮应交文件。
自动合入同行更新后，重读受影响的证明、异议和登记，再运行必要检查。

## 旧存档与历史

已有数学成果保留独立模型与精确状态。旧角色提示词和重复交接说明移入历史后，
不作为本题开工必读；入口以当前三份角色文件为准。归档不改变 Claim 的真假或审查等级。
旧绑定继续使用其原存档，旧工具路径只作兼容转发，不选择本题默认方向。
