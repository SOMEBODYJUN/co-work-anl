# RA12 非作者第二遍出处增量复核

复核人 `/root/ra12_adversarial`。原稿转写和学习稿与我刚完成的全文第二遍复核版本逐字节一致。此次逐条核对两稿的新增出处、双向映射、图证及 REC21／ISSUE21，并重查 111 个源单元、96 个目标的映射投影和行段哈希。旧 20 条恢复与 20 条问题的记录一致，新 REC21 的精确来源补链与图证均实查接受。当前接受 21 项，前轮三项出处发现已解除。

本轮实际重开 6 个相关分区和 11 幅已登记的定向图，其中 7 幅支撑新加的 9 条直接图证链接。另从原 PDF 渲染并查看了第 4 页一张 1200 dpi 局部图，确认「有／个」之间的横提。7 整页和其余 36 分区沿用此前独立逐张实读，并重核同源 49 幅图的哈希。第 6 页视口补证在内存内只扩边框及一条现有矩形裁指令，逐像素对得原PDF重渲，并验证原流的绘画字节不变。

## 内容来源

两个方向的来源关系由 538 增至 556。18 条新增关系逐条回查正文与物理来源，旧关系没有删除。目标行段、正文哈希、源框坐标和区归属均保持一致。

| 目标 | 新查证来源 | 原图和正文对应 |
| --- | --- | --- |
| `RA12-STUDY-052`（学习稿第 482 行） | RA12-P001-U05、RA12-P001-U06、RA12-P001-U07 | U05 是有限测度题面及其右弧，U06 是并号点状下限与两左一右括，U07 是提纲第三条的微短提及独立笔簇。新来源对应表中各原迹。 |
| `RA12-TRANSCRIPTION-015`（转写第 87 行） | RA12-P004-U14、RA12-P004-U15、RA12-P004-U16、RA12-P004-U17、RA12-P004-U18 | 蓝注援引第 4 页局部化。P4U14 起无限测度，U15 是球差，U16 是与 E 交后的可数并，U17 是各片一个闭集，U18 明说需用局部有限。 |
| `RA12-STUDY-013`（学习稿第 101 行） | RA12-P004-U15、RA12-P004-U16、RA12-P004-U17、RA12-P004-U18 | 说明环带证明为何使用局部有限。U15、U16 给环带和分片，U17 给各片选闭集，U18 明说所用性质。 |
| `RA12-STUDY-021`（学习稿第 151 行） | RA12-P004-U14、RA12-P004-U15、RA12-P004-U16、RA12-P004-U17、RA12-P004-U18 | 明确援引第 4 页的无限测度路线，U14 给该情形，U15–U16 给环带覆盖，U17–U18 给闭近似及局部有限。 |
| `RA12-STUDY-045`（学习稿第 393 行） | RA12-P006-U01 | 引用第 6 页已证明的方向。P6U01 的独行题首直接写 Pf. (1)→(3)，下接全空间延拓。 |

## 直接图证

T004 和 S005 分别引用第 2、5 页同手「是」字。T029 的三个图链接对应第 1 页「要求」及第 3、4 页两处「用」。T043 的两图对应第 4 页「考」与第 6 页原矢量补证。清楚的同手比较支持现有的有限置信校读，正文中的其他候选和不确定性仍适用。

| 目标 | 直接图证 |
| --- | --- |
| `RA12-TRANSCRIPTION-004` | 第 2 页题面的“是”有上回折、纵笔和向右下长扫。 [p0002-lusin-shi-1200.png](../../../../proposals/ra12_visual/final-f733447a84a1/p0002-lusin-shi-1200.png) |
| `RA12-TRANSCRIPTION-004` | 第 5 页前件“是”有纵笔、曲回和下长扫；与第 2 页同手异写。 [p5-is-in-statement-1200.png](../../../../proposals/ra12_adversarial/final-f733447a84a1/p5-is-in-statement-1200.png) |
| `RA12-STUDY-005` | 第 2 页题面的“是”有上回折、纵笔和向右下长扫。 [p0002-lusin-shi-1200.png](../../../../proposals/ra12_visual/final-f733447a84a1/p0002-lusin-shi-1200.png) |
| `RA12-STUDY-005` | 第 5 页前件“是”有纵笔、曲回和下长扫；与第 2 页同手异写。 [p5-is-in-statement-1200.png](../../../../proposals/ra12_adversarial/final-f733447a84a1/p5-is-in-statement-1200.png) |
| `RA12-TRANSCRIPTION-029` | 第 1 页“要求”的求有右上独点、中央过横及下钩，与第 4 页并估计前目标字可比。 [p0001-yaoqiu-reference-1200.png](../../../../proposals/ra12_visual/final-f733447a84a1/p0001-yaoqiu-reference-1200.png) |
| `RA12-TRANSCRIPTION-029` | 第 3 页“或用”的用有中央轴下探至右钩以下。 [p0003-second-egorov-yong-1200.png](../../../../proposals/ra12_visual/crops/p0003-second-egorov-yong-1200.png) |
| `RA12-TRANSCRIPTION-029` | 第 4 页底“需要用”的用有同样下探中轴和两短横。 [p0004-second-annuli-yong-1200.png](../../../../proposals/ra12_visual/crops/p0004-second-annuli-yong-1200.png) |
| `RA12-TRANSCRIPTION-043` | 第 4 页“考虑”的考有交叉上体和回环下部，可与第 6 页考察首字比较。 [p4-kao-of-kaolu-1200.png](../../../../proposals/ra12_math/second-review-crops/p4-kao-of-kaolu-1200.png) |
| `RA12-TRANSCRIPTION-043` | 第 6 页原矢量补证显示围笔内分立两墨。放宽视口增加可见笔画，但易、另仍不逐笔唯一，也不能判断边字一定与考察连成句。 [p6-left-expanded-clip-1200.png](../../../../proposals/ra12_math/second-review-crops/p6-left-expanded-clip-1200.png) |

## 版本及复核记录

| 本轮起止文件 | SHA‑256 |
| --- | --- |
| source-transcript.md | `c0b24c688ef9683e9dce98cf83d8c573c17207941292731f34a4a791a2bee42b` |
| study-notes.md | `20fee3e5fb5baa0955e4a80f43f095a036ffba9c466800f5cf576c5e8f409abe` |
| source-target-map.json | `3ca526170b3621e449376cee9deba51baef7f4cdf14d7c2a2e2c43986f144b39` |

49 幅原图及 292 项已登记工件的 SHA‑256 已重核。结构比较确认本次只更新约定的源关系、目标图证及 REC21／ISSUE21 所需元数据。当前三项出处问题解除，未发现新的阻断项。

本次记录沿用先前相同正文的[全量第二遍审查](../second-pass-report.md)及同源[原图独立逐张重读](../../final-f733447a84a1/source-first-reread.md)。当前逐页、逐区和 21 项恢复的独立判断见相邻 [second-pass-report.json](second-pass-report.json)。[第 4 页补图](p4-annuli-closed-phrase-1200.png)及[crop-index.json](crop-index.json)。
