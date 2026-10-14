# 一键保存与推送

从仓库根执行完整入口；它默认保存当前研究目录的工作树状态，不要求先手动暂存或编写 commit 标题：

```sh
bash research/weighted_congestion_frontier/tools/checkpoint.sh
```

需要保存根研究地图等其他路径时，一次显式列入：

```sh
bash research/weighted_congestion_frontier/tools/checkpoint.sh \
  research/weighted_congestion_frontier README.md RESEARCH_STATE.md
```

路径始终相对仓库根；有空格的路径加引号。可用 `-m '准确的阶段说明'` 指定标题。已有暂存文件在范围外时，工具明确列出并停止，避免把别人的工作一起提交。范围内采用工作树当前内容，因此会重新暂存当前版本；它不是“仅提交已有 index”的命令。已有删除也会记录。

## 认证只初始化一次

已配置 Git 凭据时直接运行。用户在当前会话提供外部凭据文件时，首轮可以执行：

```sh
bash research/weighted_congestion_frontier/tools/checkpoint.sh \
  --token-file /absolute/path/outside-repository/githubtoken.txt
```

支持外部文件中的 GitHub PAT。工具通过 ASKPASS 将凭据交给 Git；本 clone 的 Git 配置只记住外部文件路径，后续同一 clone 直接运行入口。环境重置或换 clone 后重新指定当前会话提供的文件；不得从别的会话寻找凭据。公屏工具仍使用自己的现有认证方式，本入口不会给公屏配置后台认证或修改系统设置。

## 确定流程

1. 锁定本 clone 的 Git 写操作，核对分支、范围及已有操作。
2. 对改动做路径、凭据式内容和 `git diff --check` 检查。
3. `git add`、有变化才 `commit`。即时输出 `LOCAL_CHECKPOINT` 和完整 SHA。
4. 普通 `push`，重新 fetch 指定远端分支，核对该 checkpoint 是远端 tip 的祖先。
5. 输出 JSON：`status: pushed`、branch、commit、remote_tip、files、assets。每个仍存在的修改文件都有冻结 commit、SHA-256 和公屏 descriptor 文件路径。

descriptor 和提交回执仅放在 Git common directory 的 `wcg-checkpoint/` 缓存；不作为数学资产入库。将结果 JSON 中 `assets` 项目的 `descriptor` 路径传给现有 `board.py say --asset-json` 即可，不需要手工算 SHA 或抄写 commit。多个文件各有 descriptor；不要把整个提交回执当单文件 descriptor。

输出的 `commit` 是已保存的阶段快照。同步产生 merge commit 时，`remote_tip` 可以不同；工具验证快照仍可从远端抵达，文件哈希对应快照中的 blob。删除的文件列在 `files`，没有 blob descriptor。

## 重试和并发

没有变化时不制造空提交；本地 commit 已生成而网络失败时，重复同一命令继续推送。push 成功但响应丢失，重新读取远端能确认成功。远端新增不冲突改动、当前工作树干净时自动 merge 后重试；真实冲突时 abort 本次 merge，保留本地 checkpoint 并列出冲突文件。远端分叉且另有未保存的 tracked 改动时保留全部内容并停止，先在单独 worktree 整合。

工具有有限重试和单次 Git 超时；网络、认证或策略错误不意味着数学失败。没有远端确认时退出非零，不能发“已经发布”的结果消息。多个会话用独立 clone/worktree；锁只约束使用本工具的写入者，不能强制阻止直接运行其他 Git 命令的人。`wcg/board` 分支禁止使用本入口，认领必须经 `board.py` 重新验证，不能通用 merge 重试。

## 主 agent 的执行规则

子 agent 交来真实可复用文件、写清 claim 身份/证据层级/未解步骤并完成对应核验后，主 agent **立即调用入口**。无需再询问用户是否保存，也无需为了普通 checkpoint 重做选题评估、文献搜索、完整证明审查或全仓回归。疑似证明可以按 candidate 保存；fatal objection 和未解义务同样可以按实际层级保存。保存不会把 claim 升级成可靠定理。

重要数学状态提升仍按独立审查和账本规则；修改工具时跑对应工具测试，修改数学代码时跑相关精确核验。公屏分享沿用既有协议，不能让 checkpoint 自动替作者宣称一个成果已经证明。

验证入口：`python3 research/weighted_congestion_frontier/tests/test_checkpoint.py`。
