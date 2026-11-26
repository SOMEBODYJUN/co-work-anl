# CA07 第一页右中分区观察勘误

定向重开第一页右中区、第一页整页及三个原生源单元，确认图前草笔、尖点双枝和图外孤点都清楚落在该区。原分区路径和图像哈希正确。先前的读图记录把图前的草笔误记为“闭于 k”，把下枝右外孤墨记为句后点，漏记尖点图及两条粗枝。

## 原句

> 上左只余前行末划与逗；中见闭于k、句后小点及代入行末 t 上高钩、方括和 ⊆k(t)。底线左边 t 主体几乎截去，但其上 2 的曲头、斜回与低脚可见；横线后 a 主体全，a 上笔较窄且低处仅短挑；其后 =0、‘不’后连笔、a∈k、低点。

## 改句

> 左上仅余前行“数”的交斜末笔及逗。中上图前见 e/U 形起笔、中部上下相连的折笔及末尾两团墨，按同排上文恢复“的表示”。尖点图左端见回圈浓墨和短扫，横向短展后分两粗枝，分别向右上和右下弯出。下枝末端右外有一独小点。再下由左缘切入商式右侧的左括，见两个 t 的高位弯、逗、右括，继以带离体底横的包含号及 k(t)。底行左边 t 的主体几乎截去，仍见其上 2 的曲头、斜回及底挑。减横后见 a 和其高位窄短弯钩，按上下文作 2，继以 =0、连写的“不能”、a∈k 及行末低点。

## 实际图证

- 这张分区上左有前行字尾与逗，中上图前多团草笔，图左回圈浓墨、先短展后分出的两粗枝，以及下枝末右外的一枚孤小点。下有商式右端与另一参数式的尾部。 [p0001-r2c2.png](../../../regions/p0001-r2c2.png)
- 整页确认“在 A² 中”与图前草字和尖点图同排。向下依次是商式、参数式。用于核位置及句子上下文。 [p0001.png](../../../pages/p0001.png)
- 短语首呈 e/U 形起笔，中有上下分层的弧折，末两团分别有短横与下直扫、斜起及低回圈。“的表示”依图前语境恢复。 [CA07-P001-U13-800.png](../../../audit/source-units-800/CA07-P001-U13-800.png)
- 双枝从左端回圈与短扫附近先共用短横向墨迹，再分向右上和右下。独小点在下枝末端右外，隔白可辨。 [CA07-P001-U14-800.png](../../../audit/source-units-800/CA07-P001-U14-800.png)
- 商式右端完整写 k、左括形、两个高位弯及两项间的逗、右括、底横离体的包含号、k(t)。请求勘误的分区在左 k 之后切入。 [CA07-P001-U16-800.png](../../../audit/source-units-800/CA07-P001-U16-800.png)

原 400 dpi 分区框为 `[1553,1465,3306,3212]`。下枝右外孤小点约在页坐标 `[2459,2159,2463,2162]`。它与底行末的小点分居两处。

## 输入与输出 SHA-256

| 文件 | SHA-256 |
| --- | --- |
| `proposals/ca07_visual/post-second-pass-1/reconciled-source-observations.json` | `44d602eaadfe0d3a8e01b12c16868db624e6939458c25f2b80f998ba1b9a87b1` |
| `proposals/ca07_visual/post-second-pass-1/viewed-images.json` | `65276055c08a68be1e71f5b5d7afd2daba4ff75b78fbe37cb637d366df1c9e2d` |
| `manifest.json` | `71f3708f90674ac982e53c8d51c58e52370d175a732d3bfd931b1a1bc8866ed9` |
| `source.pdf` | `e0fac422cbee2ac1d7076d4b68961656de0b5b3ecb876b057a43121e6afb1df2` |
| `source-transcript.md` | `1d8563780fef910ada59bd17fa4deff3a63fa89af03f13df1f9ea408636a2ea6` |
| `study-notes.md` | `617cd468582950e8f917013da27f9c4a6b1e6eee6109810bbb30b28d8c4cd232` |
| `source-target-map.json` | `a36f150c3fb9855053440e782bdee7e6e2f1c3d1eff0cf5b6582e50096c6030d` |
| `proposals/ca07_visual/post-second-pass-errata/reconciled-source-observations.json` | `6275ab8b61ca3f183fe8acb85913ccda239f1c84ec721e5165a481ac3009dcd4` |

新版八页四十八区记录仅改该区的 observation 字段。两份正文与映射的前后 SHA-256 已核对一致。逐张所见及原图哈希见 [erratum.json](erratum.json)。
