# 当前：独立六人半覆盖研究

用户最新任务：五人已证后，只吸收可迁移工具，独立攻六人，六名子代理使用 GPT-6-astra ultra。
当前 `Q-CAG-HALF-6`：原有限单位客户、任意有限非空共同目录、恰六名单位提供者、每份完整历史纯SPE的 `2W≥OPT_6`；零客户、空主题、重复和任意离轨平局全部保留。六人仍 OPEN。
最新已读取远端 `cb1eabe4` 的五人精确证明、一般报价/回复再查询与六人701行障碍。不能把无背景五人定理当作有背景五尾利润，也不能把五人特殊乘子换成六人。

当前材料在 [六人研究桌面](round3_six/WORKING_SIX.md)；旧五人探索的准确停界见 [round2](round2/README.md)。六名指定模型已实际启动，父方直接推导多实际位置共同报价的隐藏续局投影。身份复用本clone，不冒用其他工作区；由父方统一Git保存。

## 之前的 GPT Pro 五人交接包

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
