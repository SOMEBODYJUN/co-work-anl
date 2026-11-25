# RA09 REBUILD 作者首遍交接

**角色与范围**：REBUILD 作者，`/root/ra09_rebuild`；实际 session 同名。只写本 RA09/project，没有 Git 写入，也没有启动子代理。

## 两份完整正文

| 文件 | 行数 | SHA-256 |
| --- | ---: | --- |
| source-transcript.md | 549 | `93c973df02dfa7cf182571006991206d209d7ac95ce817284afafb5a05b567bf` |
| study-notes.md | 882 | `79d2a1db1b1bb58067e1c31a8cdd569c2c36c5e32711fc3bd5fd2ee72876ad0c` |

保真转写按 12 个物理页顺序；复习稿有完整目录与 9 个主题章，基础工具先于使用，题目和详细证明相邻，连续性直接路线及原稿拓扑路线分别保留。普通正文保留原式、重复起笔、原错误、图示、旁注；蓝色块提供补充和纠错；原明确待填为红色。

## 首遍覆盖

| 物理页 | 源内容单元 | 全页检查 | 区域检查 |
| --- | ---: | --- | ---: |
| 1 | 14 | 已实际查看 | 6 |
| 2 | 13 | 已实际查看 | 6 |
| 3 | 17 | 已实际查看 | 6 |
| 4 | 9 | 已实际查看 | 6 |
| 5 | 13 | 已实际查看 | 6 |
| 6 | 12 | 已实际查看 | 6 |
| 7 | 15 | 已实际查看 | 6 |
| 8 | 15 | 已实际查看 | 6 |
| 9 | 13 | 已实际查看 | 6 |
| 10 | 13 | 已实际查看 | 6 |
| 11 | 2 | 已实际查看 | 6 |
| 12 | 0 | 已实际查看 | 6 |

共 136 个源单元、345 个目标单元、12 条首遍全页记录、72 条首遍区域记录和 25 个实际查看的额外裁图。第 12 页为实查空白页；第 11 页仅两行，未虚构续页内容。

## 当前疑点

唯一开放字迹问题 5 项：Q001（第1页拓扑反例旁注）、Q002（第2页逼近过渡语）、Q003（第6页“是…σ代数”连接字）、Q004（第6页邻域与线序拓扑连接语）、Q005（第8页“用生成…”末字）。独立位置清单见 issues.md。

审计的 unresolved_count=20 是 5 个源单元、对应两份正文的 10 个目标单元和 5 条 issue 的重复计数，不是 20 个独立问题。数学补证只关联可辨的定义或公式；未决字形仍在自己的源/目标单元保留。

M001 原断言已经通过局部有限化与解析集普遍可测性补证确认，研究记录保留作者和贡献者的实际角色，学习正文不含协调或验收记录。

## 实际验证

- manifest 与 ledger 的 JSON Schema 合法。
- `qa/first-pass-audit-v3.json` 是当前实际审计结果：非复核门槛结构错误 0；工具核验原 PDF、全页像素、区域与额外裁图像素、坐标、哈希、目标逐行覆盖及双向映射。
- 正式全审计仍为 NeedsHuman / audit_pass=false：缺 12 个第二遍全页记录、72 个第二遍区域记录及最终三轮，共 85 条预期门槛错误。未代填任何独立记录。
- `recoveries` 和 `final_rounds` 均为空。已有候选与数学核对存 author-restoration-notes.md，供新审阅者独立恢复复核。
- 有限枚举：1728 组逆像交并补检查、40 组示性函数阈值检查、有限区间/上射线的端点模型、256 个二进制有理数的 floor 数位和三进制单射检查通过。输入代码和输出在 qa/finite_checks.py、qa/finite-checks.json；不把有限检查当作一般定理证明。
- 两正文行末无空格，文件末尾恰有一个换行。
- Pandoc MathML 预览转换无警告；Chromium 实际截图被沙箱 socket 权限阻止，**未完成代表性渲染视觉查看**。详情在 qa/render-status.md；请独立阶段在可用环境补看。

## 交接文件

- 正文：source-transcript.md、study-notes.md。
- 原件与图：../../source.pdf、../../manifest.json、../../pages/、../../regions/、../../crops/。
- 内容清单与映射：source-units.json、mapping.json。
- 实际首遍观察：observations.json。
- 恢复候选、来源、术语、证明依赖：author-restoration-notes.md、source-provenance.md、terminology.md、dependencies.md。
- 疑点及修订历史：issues.json、issues.md。
- 统一台账：../../ledger.json；主生成入口 build.py 读取最终手工 page-data。finish_pages.py / finalize_author.py 是一次性作者历史辅助脚本，不应重跑覆盖最终数据。

后续工作：新 VISUAL_SECOND 应先从原图独立盲读，再比对当前正文及清单，处理 5 处字迹和潜在遗漏，并完成独立恢复记录。此作者首遍交接不代表第二遍或终审通过。
