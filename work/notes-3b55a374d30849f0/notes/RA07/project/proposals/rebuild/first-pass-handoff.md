# RA07 REBUILD 作者首遍交接

记录时间（运行环境 UTC）：2026-11-24T08:49:34.547821+00:00

状态：13 页首遍视觉和全部可读原内容已完成；第 13 页整页空白。已写两稿、148 个手工来源单元、422 个目标单元、13 个首遍整页观察和 78 个首遍逐区观察，另实际查看 11 张有坐标裁图。没有填写第二遍或最终复核占位。

正文：`source-transcript.md` 按物理页序；`study-notes.md` 按 17 节复习依赖顺序。完整目录、原题及相邻蓝色解答、重复路线、两幅原图、原错误和未完证明均保留。内测度部分另补完整内外逼近与等价判据。

| 物理页 | 来源单元数 | 首遍范围 |
| --- | ---: | --- |
| p0001 | 16 | 整页及六区；逐区观察见 observations-first.json |
| p0002 | 13 | 整页及六区；逐区观察见 observations-first.json |
| p0003 | 13 | 整页及六区；逐区观察见 observations-first.json |
| p0004 | 13 | 整页及六区；逐区观察见 observations-first.json |
| p0005 | 14 | 整页及六区；逐区观察见 observations-first.json |
| p0006 | 13 | 整页及六区；逐区观察见 observations-first.json |
| p0007 | 13 | 整页及六区；逐区观察见 observations-first.json |
| p0008 | 10 | 整页及六区；逐区观察见 observations-first.json |
| p0009 | 15 | 整页及六区；逐区观察见 observations-first.json |
| p0010 | 11 | 整页及六区；逐区观察见 observations-first.json |
| p0011 | 13 | 整页及六区；逐区观察见 observations-first.json |
| p0012 | 4 | 整页及六区；逐区观察见 observations-first.json |
| p0013 | 0 | 整页及六区；全页空白，不造来源单元 |

## 当前正文哈希

- source-transcript.md：`df0e9e45491ef2345a5de8d2585e9bed5785b25f029cb66d9e5bc92215edf594`
- study-notes.md：`c80abe60b72787b9701fdd1a52c67dfec254216e9a182721955d935b13a7aba6`

## 审计边界

ledger 的 JSON Schema 已实跑，0 错误。首次 check 的 5 个 RESOLUTION_CONFLICT 已修正为保守继承未决来源状态。最终作者阶段 check 另存 `audit-first-pass-final.json`；缺少第二遍整页/区域及连续三轮终审应继续显式报错，不能称最终通过。正文与目标哈希、双向映射、来源边框及图像记录将由该结构检查核验。

正式 recoveries 留空；作者候选、前向/逆向数学检验和真实回图记录在 `author-recovery-notes.md`，供非作者独立检查后另建正式记录。四处未决见 `unresolved.md`。

## 生成与维护

可编辑 `pages/p001.json` 至 `p013.json` 后运行 `build.py`，它会原子更新两正文并刷新 ledger、mapping、source-units 与 observations-first。`study-order.json` 决定学习顺序，并断言所有主体只出现一次；补充单元紧跟其来源主体。旧的 write_pXXX.py、repair_q001.py、refine_first_pass.py 是历史起草工具，含一次性补充，勿重新执行以免重复插入或回退后来订正。

图像路径与 SHA256 在 manifest；两正文图像使用 work/notes 分支的 raw URL。作者未执行 Git 写入；所有本次文件位于获配 RA07/project/。参与身份见 participants.json，/root 的局部复读不计 VISUAL_SECOND。
