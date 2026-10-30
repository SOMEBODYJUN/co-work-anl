# 规范贪心全局审计的八文件快照

本目录保存 `ea34d2bb6de57b31bb46`（`tests/audits/kfac_greedy_box_global.py`）实际读取和运行所需的八文件 API/审计树。快照由既有 `reconstruct_snapshot.py` 在冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 重建，8 个文件共 45937 字节；`snapshot_manifest.json` 和 `reconstruction_check.json` 逐文件记录 SHA。八个原件也保存在 `source/` 下，避免把临时工作区当作复现依赖。

`current_original_run.json` 是本批对**冻结原版**全局审计的一次实际执行记录，随机种子 2026100703，退出状态全通过。它核对了抽象输入 1161、非负状态 1548、溢出 174、H 改善攻击 210、外部归家攻击 200、完整证书 528、实际标号偏离 2556、完整布局求值 4535（默认规则 2728），并记录 87 次单例重置、2469 次非单例补全、最大实证因子 (950/537)。测试还验证了不可达归位被拒绝、CLI 首次成功和拒绝覆盖既有输出。

这些数字是有限重放和实现级证据。审计没有取得历史 Pro ZIP，也没有把有限检查升格为普遍证明；总时间多项式、所有离轨调度器的统一上界和外部文献优先权仍是开放边界。原版 `construct` 全局审计与第 10 批报告字段适配保持两个身份；本批没有运行适配版，也没有把 equal-light-flow 纳入这份八文件审计。

复现（使用新输出路径）可从仓库根运行：

```sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-global-audit/source/tests/audits/kfac_greedy_box_global.py --output NEW.json
```

脚本的 `ROOT` 是其 source 树，若移动树需保持相对目录；输出路径不能覆盖已有文件。保存的运行记录来自相同字节树，不把再次运行计作独立数学证明。
