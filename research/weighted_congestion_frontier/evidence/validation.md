# 平等协作基础设施验证

2026-10-14 UTC。此记录验证工具和提示词，不证明 WC-TARGET。

## 本地验证

Python 标准库 unittest 以实际临时 bare Git 远端验证，执行：

    python3 research/weighted_congestion_frontier/tests/test_board.py

当前 16 项全部通过：同一具体 scope 同时提出/认领只一位成功；不同义务都成功；无需协调者的现成 idea 认领；到期边界接替与旧 token 阻断；仍允许旧成员公开 salvage；release 后继续与 finish 仅关闭单元；丢失 push 响应同 ID 恢复；已提交结果在资产分支删除后仍恢复确认；首次资产网络失败保存 intent、不堵其他消息；同 clone 同 ID 并发重试的原子 outbox 及确认期间文件消失恢复；错误 hash、未发布 commit、越界路径、目录对象拒绝；脏 checkout/HEAD/FETCH_HEAD 保留；未来 discussion 不延长别人的新租约；字段、未知ID、期限边界；凭据式内容发布前拒绝。

根仓库维护检查通过：git diff --check、research/build_map.py --check、research/build_crosswalk.py --check、research/check_assets.py。本轮没有更改已有数学算法，未重跑其全套回归。

## 独立检查与修复

先有两位平等 peer 独立提出协议及并发反例；其后实际启动 gpt-6-astra / ultra 与 gpt-6.1-sol / ultra（fork_turns=none）分别独立攻击实现和提示词。双方确实复现了：

- 资产校验联网在 outbox 保存前导致 intent 丢失；
- 已成功推送结果的恢复错误依赖资产分支仍可访问；
- 非原子 outbox 可在同 ID 并发时读到半写 JSON；
- 目录 tree listing 被误当文件内容；
- 未来时间戳通过单调钳制延长另一成员的新租约；
- 队内认领、全局认领及共享账本/Git写入隔离的措辞冲突。

均已修复并纳入回归：先原子保存、先确认既有事件、新消息才验证资产；blob 类型检查；序号排序而不钳制 UTC；统一全局成功认领与独立 Git 工作区。两位指定模型已经独立复跑各自复现脚本并重读提示词，主要修复通过。Sol 追加发现同 ID 确认清理与另一读取之间的 TOCTOU，已用循环原子保存及容忍消失的 CLI retry 修复、纳入回归。实际 GitHub 收发尚待完成，不能称公屏已经部署。

## 范围限制

确切字符串 scope 哈希不理解数学语义，overlap 由同伴公开处理；过宽 idea 也需同伴识别。租约要求同步 UTC、遵守截止规则，不能强制暂停断网 worker。拥有写权限者绕过工具可制造无效历史，本轮没有服务器端校验守卫。冻结 commit/hash 不代表证明正确或新颖。运营消息保存在独立公屏分支，不升级研究账本。
