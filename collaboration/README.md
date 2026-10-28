# 协作程序：文件分支、公屏和个人工作

本轮先完成[清洗工作](CLEANUP.md)。数学研究当前题目是 **Q-CAG-HALF-6**，存档 `customer-attraction`；全仓清洗另用 `repository-cleanup`，避免把基础设施工作登记为数学成果。

## 加入清洗

每个独立对话用独立 clone。把本分支的最新版根 `work.py` 和仓库外 `githubtoken.txt` 附给新对话，并提供[清洗启动词](CLEANER_START.md)。代理自动找附件路径，不让用户手填路径或身份。

```sh
python3 <新版附件work.py> --repo <新的独立目录> start --save repository-cleanup --role cleaner --branch cleanup/research-foundation-20261028 --board-branch wcg/board-cleanup-20261028 --token-file <仓库外token实际路径>
```

程序为每个 clone 绑定存档、actor、角色、文件分支、公屏分支；继续同一 clone 时复用绑定。已有其他绑定不改写，另建 clone。启动不自动读公屏；工作从 `context_entry` 开始，然后按需访问其他文件。**只读一个启动文件是默认上下文安排，所有 Solver 和 Boss 仍可主动读取全仓材料、使用全部实际可用工具。**

进入 clone 后统一用根程序：

```sh
python3 work.py sync
python3 work.py read --thread repository-cleanup-20261028 --limit 20
python3 work.py inbox
python3 work.py send --thread repository-cleanup-20261028 --text-file <UTF-8消息文件>
python3 work.py dm --to <另一actor> --text-file <UTF-8消息文件>
python3 work.py checkpoint <明确列出本次修改路径> -m '整理内容及准确边界'
```

`sync` 只合并绑定文件分支；`checkpoint` 只向该分支正常推送并确认远端可达，回执 `status=pushed` 才表示保存。它们不自动把清洗分支合入 `main`。分支不一致时停止并保留工作；不同存档、角色或分支不在同一 clone 中来回改绑。

`visit <actor> --path <工作区内相对路径>` 默认读绑定分支上的同行文件；加 `--branch main` 可只读另一分支的已推送材料，不改变本地工作分支。其余全仓资料直接读取本地文件或明确 fetch 对应分支后查看。草稿、本地计算及尚未被正式接纳的结果都能 checkpoint；无需先登记 Claim 或更新全仓 JSON。

## 分支建立和公屏换代

本轮协调者已建立 `cleanup/research-foundation-20261028`。后续参与者直接加入，不各自重建总分支。未来另起一轮时，由协调者从已经同步的 `main` 建分支，再绑定并首次发布：

```sh
git switch -c <新文件分支>
git config --local wcg.branch <新文件分支>
python3 work.py checkpoint <本轮具体路径> --create-branch -m '建立新一轮基础'
```

只有首次发布需要 `--create-branch`；程序先以远端 `main` 审计全部未发布提交，拒绝遗漏范围和凭据。普通 checkpoint 不偷偷创建远端分支、不强推、不改历史。之后新 clone 用 `start --branch` 加入已发布分支。

新公屏用独立分支。`work.py board-init` 只初始化绑定公屏，已有公屏不删消息。本轮新公屏为 `wcg/board-cleanup-20261028`：空白启动、保存清洗交流。旧 `wcg/board` 不作为清洗启动上下文；无需把旧公屏复制到工作树里再造一份档案。已有 Git 提交保留恢复能力。

## Boss、Solver 与交流

Boss 负责理解整题、接收工作、去重整理、维持目标和跨上下文交流；内部研究 subagent 都是 Solver，拥有同一完整目标和资料访问能力。它们自由选择方法，也能自查、计算、查资料、互相交流；不预分证明组、实验组或文献组。Boss 可把某条新 idea 转给相关 Solver，不能用提示词强制大家沿同一路线。

大部分推理资源给 Solver。检查在具体证明、反例、关键论证出现后按需进行；整理按实质变化进行。没有固定检查轮次、固定通信频率、固定方法配额或代码先行步骤。自然语言证明是本轮产出形式，形式化工具按实际可用性选择，不作为启动依赖。

公屏允许未完成的想法、异议、问题和接续请求。发言应含实际数学内容、影响范围或明确协作需要。每次备份、每次脚本运行无需广播。未入库不等于无价值，也不等于该方向停止。
