# GPT Pro 五人攻坚交接包

本次用户要求把现有研究资产整理为 ZIP，交给 GPT Pro 直接攻 Q-CAG-HALF-5。
范围是**五名提供者 m=5**，客户数与共同目录大小任意有限，原模型全部历史纯 SPE，
目标为 `2W≥OPT_5`；方法不限，其他目标暂停。主命题仍 OPEN，本次不新增数学结果。

## 可恢复资产

- [完整任务提示词](pro_handoff/00_PROMPT_ZH.md)：自足精确命题、自由方法、量词与交付判据。
- [阅读入口](pro_handoff/01_START_HERE_ZH.md)、[五人状态](pro_handoff/02_FIVE_PLAYER_STATE_ZH.md)、[资产导航](pro_handoff/03_ASSET_GUIDE_ZH.md)：区分精确2.017183证书、后续局部组件与待审作者候选。
- [复现说明](pro_handoff/04_REPRODUCTION_ZH.md)：文件完整性与数学复核的不同范围。
- [构建器](pro_handoff/build_bundle.py)：从固定提交82e7d5e5的Git对象逐字取源，收录全部本题路径资产、关键总账与静态可解析导入依赖，生成分层ZIP和每文件SHA-256。
- `pro_handoff/BUILD_REPORT.json`：实际ZIP大小、SHA-256、源文件数及通过的文件级检查；不等于重审全库数学。

生成命令在仓库根运行：

```sh
python3 research/workspaces/customer-attraction/R-e1149b822db540d38ecf1283cce056bd/pro_handoff/build_bundle.py --output /absolute/output/Q-CAG-HALF-5-GPT-Pro.zip
```

ZIP作为单独交付文件保存；Git保存提示词、导航、冻结来源和可重建配方，避免重复提交全部原始资产。
凭据与Git元数据不进入ZIP。个人备份不改变共享Claim/审查等级，也不覆盖其他会话任务。
