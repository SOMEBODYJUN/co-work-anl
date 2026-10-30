---
id: "weighted-congestion/repository-curation-finite-replay-resource"
kind: "resource"
type_tag: "资源"
title: "Weighted-congestion仓库整理与有限回放资源"
status: "finite-workflow-evidence-integrated"
truth_status: "workflow and replay evidence only; no mathematical status promotion"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/repository_curation.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/weighted_congestion/repository_curation.json"
---

# 来源身份与范围

稳定来源 ID 为 `1e317280189558c4e59a`，冻结 JSON SHA256 为 `c77ef2d7a2db572068959c2abc2c149f93feab606201c171d308434d48637a1c`。报告 schema 为 1，基线提交 `93c44282d3739c06951710a453f2a1c76c9e2df4`，Python 3.12.14。scope 明确限定为仓库整理、主分支协作与有限精确 WC audit replay，不提升任何数学状态。

# 实际记录

本地 workflow 测试命令为 `python3 -m unittest discover -s research/weighted_congestion_frontier/tests -p 'test_*.py'`，通过 65 项；网络只使用隔离的本地 bare repository，不发送生产测试消息。报告收录 21 个 exact replay，全部 exit code 0，覆盖 odd-ring 参数与独立 envelope、quadratic triad/source、source degree 32、crossover、density padding、weight bands、polynomial curvature、heterogeneous endpoint、step DAG、weighted power bridge、source topology、multicolumn 等。runner SHA256 为 `d3bb4004b675e796817e259ac5c4c5b6de918810ebd9ea212c5bb0cb0dcd4a07`；每个 replay 的 source/stdout SHA、耗时和命令在冻结 JSON 中逐条保存。

固定检查清单包括 map/crosswalk/build 预检、资产检查、`git diff --check`、本地 Markdown 链接、远端分支 exact-tip 与原提交 ancestry、以及学习导出一致性检查。参数与 seed 仍以各冻结源为准；Fraction/integer 比较是精确的，诊断十进制不能承担一般数学断言。

# 用途和限制

这份资源用于第三阶段复现时确认：清洗结果分支可从 recorded commits 重建，原审计程序和输出的 SHA 能逐源追溯，协作工具链的隔离本地测试通过。它不证明任何 weighted-congestion 定理，不替代各审查正文中的定义域、量词和数学推导，也不认证全局优先权、外部同行评审或生产网络行为。删除的 current-tree 快照和分支仍由记录的 Git 提交恢复；当前教学源与导出匹配，过期页面构建只作为 Git 来源留存。
