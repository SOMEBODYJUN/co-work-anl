# 平等协作基础设施验证

2026-10-14 UTC。此记录验证工具和提示词，不证明 WC-TARGET。

## 一键 checkpoint 补充验证

2026-10-14 UTC 新增 tests/test_checkpoint.py，实际临时 bare Git 远端的 22 项测试全部通过。与既有 20 项公屏测试合计 42 项；数量另用 Python AST 逐一数 test_ 方法核对，两套实际 unittest 运行结果一致。没有调用真实研究 agent 冒充并发测试端。

覆盖：真实 commit/push 与 SHA-256 blob 反核；重复运行无空 commit；默认范围保留其他未提交研究；范围外已暂存文件拒绝并保持 index；显式根文件和中文空格路径；删除文件；断网保存后同命令重试；推送成功但响应丢失；远端不冲突变化自动 merge；真正相同文件冲突 abort 并保留 checkpoint；其他 tracked 脏工作阻止自动合并；同 clone writer lock；detached HEAD / 公屏分支拒绝；越界、未知路径、凭据式内容与标题拒绝；已暂存敏感内容但工作树恢复原文不泄漏；外部认证只记路径；继承 Git 路由变量不触碰其他 index；commit 与 push 之间插入真实 peer 推送；没有 Git identity 的 commit 与自动 merge；完整 shell 入口从 checkout 外运行；无效或仓库内凭据文件拒绝；fetch/push 目的地不一致拒绝。

根维护检查 build_map.py --check、build_crosswalk.py --check、check_assets.py 与 git diff --check 通过。新增的是保存入口与来源澄清；既有公屏算法没有改动，全部公屏回归仍通过。checkpoint 通用 Git merge 不能用于公屏认领，入口对 wcg/board 分支明确拒绝。

## 本地验证

Python 标准库 unittest 以实际临时 bare Git 远端验证，执行：

    python3 research/weighted_congestion_frontier/tests/test_board.py

当前 20 项全部通过：同一具体 scope 同时提出/认领只一位成功；不同义务都成功；无需协调者的现成 idea 认领；到期边界接替与旧 token 阻断；仍允许旧成员公开 salvage；release 后继续与 finish 仅关闭单元；丢失 push 响应同 ID 恢复；已提交结果在资产分支删除后仍恢复确认；首次资产网络失败保存 intent、不堵其他消息；同 clone 同 ID 并发重试的原子 outbox 及确认期间文件消失恢复；错误 hash、未发布 commit、越界路径、目录对象拒绝；脏 checkout/HEAD/FETCH_HEAD 保留，以及继承 GIT_INDEX_FILE/GIT_DIR/GIT_WORK_TREE/GIT_OBJECT_DIRECTORY 时原暂存区保持；未来 discussion 不延长别人的新租约；字段、未知ID、期限边界；凭据式内容发布前拒绝；部署脚本在本地真实远端完成全流程并要求显式 --live；数学符号大小写不被哈希混同。

根仓库维护检查通过：git diff --check、research/build_map.py --check、research/build_crosswalk.py --check、research/check_assets.py。本轮没有更改已有数学算法，未重跑其全套回归。

## 独立检查与修复

先有两位平等 peer 独立提出协议及并发反例；其后实际启动 gpt-6-astra / ultra 与 gpt-6.1-sol / ultra（fork_turns=none）分别独立攻击实现和提示词。双方确实复现了：

- 资产校验联网在 outbox 保存前导致 intent 丢失；
- 已成功推送结果的恢复错误依赖资产分支仍可访问；
- 非原子 outbox 可在同 ID 并发时读到半写 JSON；
- 目录 tree listing 被误当文件内容；
- 未来时间戳通过单调钳制延长另一成员的新租约；
- 队内认领、全局认领及共享账本/Git写入隔离的措辞冲突。

均已修复并纳入回归：先原子保存、先确认既有事件、新消息才验证资产；blob 类型检查；序号排序而不钳制 UTC；统一全局成功认领与独立 Git 工作区。两位指定模型已经独立复跑各自复现脚本并重读提示词，主要修复通过。Sol 追加发现同 ID 确认清理与另一读取之间的 TOCTOU，已用循环原子保存及容忍消失的 CLI retry 修复、纳入回归。另关闭继承 Git 上下文变量导致临时 checkout 污染调用方 index 的问题；只清仓库路由变量，保留认证。两项追加修复均已由 Sol 独立复跑原复现通过。测试临时文件移入 Git common cache，避免并发复验时误归档。公屏已成功建立，真实 GitHub 收发亦通过，下节给出可核对事件。

## 真实 GitHub 部署验收

运行 tools/live_smoke.py --live 后，两个并发发布端在同一真实 idea 的首个 push 前同步。一个 claim 成功、一个被 Conflict 拒绝；后者实际发布了关联讨论和因果 reply。赢家 finish 校验 main 上已推送的完整 commit/file SHA-256，任务关闭且 owner 为空。全过程无中心 assignment。

实际 trace 为 evidence/github_smoke.json；该次从零条到四条事件，分别是非数学测试 idea、唯一 claim、讨论回复、含冻结工具文件的 finish。事件ID、冲突详情和 source_asset 的 commit/hash 可由 board.py view --json 重核。发布端是部署脚本中的独立 Git 工作区，不冒称两个实际研究对话。冻结版本为 main@23c6378；随后数学符号大小写去重澄清由本地回归覆盖，最新工具再次读取此流成功。

复现部署脚本会向指定公屏新增明确标注的非数学验收事件，只有显式 --live 时执行。公屏初始测试单元已结束，不占数学研究的认领。所有团队可以自主提出新数学 idea。

## 范围限制

确切字符串 scope 哈希不理解数学语义，overlap 由同伴公开处理；过宽 idea 也需同伴识别。租约要求同步 UTC、遵守截止规则，不能强制暂停断网 worker。拥有写权限者绕过工具可制造无效历史，本轮没有服务器端校验守卫。冻结 commit/hash 不代表证明正确或新颖。运营消息保存在独立公屏分支，不升级研究账本。
