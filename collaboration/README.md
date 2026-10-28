# 共用程序：长期分支、启动、交流和保存

程序只负责恢复、通信、同步和保存，不绑定任何数学求解路线。当前先做 [语义清洗](CLEANUP.md)，随后在同一分支继续研究；数学 Agent 和正式研究提示词另行接入。

## 给新对话的文件

附本分支的最新版根 `work.py`、仓库外 `githubtoken.txt`，再提供 [清洗启动词](CLEANER_START.md)。代理自动识别实际附件路径和自己的独立目录，用户无需填写路径或身份。运行：

```sh
python3 <附件work.py> --repo <本对话独立目录> start --token-file <仓库外凭据实际路径>
```

新clone的默认值已经固定：

| 设置 | 当前值 |
| --- | --- |
| GitHub | https://github.com/SOMEBODYJUN/co-work-anl.git |
| 长期文件分支 | cleanup/research-foundation-20261028 |
| 共用公屏分支 | wcg/board-cleanup-20261028 |
| 当前新对话任务 | repository-cleanup / cleaner |
| 唯一清洗入口 | collaboration/CLEANUP.md |

新clone不会默认进入main，不会自动创建新分支。十个对话是十个独立clone，仍读写同一文件分支和同一公屏。`cleanup`只是现有分支名称，清洗结束后可以继续用它研究和定期整理，不按题目、对话或轮次另建分支。

附件文件承担稳定启动职责：先恢复并同步约定分支，随后调用该clone里最新的根work.py；仓库程序自身更新时启动也会转用同步后的版本。以后的阶段规则和提示词更新在GitHub上完成，不用每次把新版大文件重新附给所有人。稳定的Git地址和分支不变时，同一份本轮新版附件可持续用于启动；第一版旧附件需换成本轮交付版一次。

程序需要Python 3.10+、Git和POSIX环境（Linux、macOS或Windows的WSL）。无需安装数学Agent CLI、Lean或数据库。程序从可访问的GitHub仓库获取更新；凭据仅用于认证，保留在仓库外，不在remote、正文或消息里。

## 同一对话接续

进入clone后统一使用仓库根程序。启动回执包含actor、workspace.path、文件分支、公屏分支和context_entry。

```sh
python3 work.py start
python3 work.py sync
```

已绑定clone复用actor、存档、角色和分支；旧main或其他研究存档不自动改绑，使用独立clone加入新协作。角色/题目不同只需为新对话选择相应存档，无需创建新的远端分支。清洗结束后，新研究Boss可在同一长期分支以 `start --save customer-attraction --role boss` 加入；正式研究提示词本轮尚未重写，届时由仓库更新提供。

`sync`只合并绑定的文件分支，保留已暂存、未暂存和未跟踪工作。当前分支与绑定不一致时停止并保留内容；不会自动切分支。真实冲突保留备份再处理，不能用强推或覆盖解决。

## 交流

```sh
python3 work.py read --thread repository-cleanup-20261028 --limit 20
python3 work.py inbox
python3 work.py send --thread repository-cleanup-20261028 --text-file <UTF-8正文文件>
python3 work.py dm --to <另一actor> --text-file <UTF-8正文文件>
python3 work.py ack <消息ID>
```

启动默认不读公屏；默认上下文安排不限制全仓访问。公屏允许idea、未完成发现、异议、明确障碍和接续需要。局部工作由各人自行完成，不把每次脚本运行和备份都广播。新清洗者先读实际认领再选择写入范围，出现跨范围问题时找协调者。

消息发送失败用 `pending` 查看，`retry <消息ID>`沿用原ID，`discard <消息ID>`只放弃本地待发消息。`ack`表示已读，不表示采用数学结论。公屏已初始化；日常无需反复init，更不能因新对话加入而清空现有讨论。旧公屏不作为默认上下文。

## 保存与访问

```sh
python3 work.py checkpoint <本次明确修改的路径> -m '整理内容、用途及准确范围'
python3 work.py visit <另一actor> --path <其工作区内相对路径>
```

checkpoint仅正常推送绑定文件分支，并确认远端可达；只有回执 `status=pushed` 才表示远端保存。清洗显式列路径，避免把同行草稿顺带提交。它不会合main、默认创建其他分支或强推。未成熟研究和有价值片段也可保存，不要求先通过正式入库审核。

visit默认读取同存档、同文件分支的同行已推送文件；`--branch main`可只读另一分支上的同行材料，不切换本地工作分支。全仓其他正文直接按需访问本地文件。尚未推送的本地工作不会自动对其他clone可见，公屏也不能替代正文保存。

GitHub上的Markdown正文就是共同知识库；每主题一个README导航和维护准确现况，实际数学在对应正文中。清洗按 [具体准则](CLEANUP.md) 阅读、比较、重组和说明用途；不是简单删文件或改目录。
