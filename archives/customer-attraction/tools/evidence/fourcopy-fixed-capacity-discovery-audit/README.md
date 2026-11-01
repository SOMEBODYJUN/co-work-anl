# ebd53a3e84a17c3430eb：原四复制发现JSON的完整语义清洗草稿

负责源：`research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/discovery_n6_c4.json`。已使用`clean show`完整读取并按冻结字节导出；7985字节、两个冻结提交同内容。只写本工作区，没有Git、claim、done、checkpoint、push或正式共享正文修改。

主要草稿是[最大根四复制定系数发现点的精确审计--计算.md](最大根四复制定系数发现点的精确审计--计算.md)。建议父Boss在避免与发现器源对象重复的前提下，提升为`archives/customer-attraction/state/计算/最大根四复制定系数发现点的精确审计--计算.md`，或保留其中完整独有内容后合入父方对象。提升时需改数据链接到正式证据目录；不要直接把本工作区receipt当已提交登记。

## 实质结论

* 原四点C=−12,−8,−4,0、B有理近似和全部141个非零乘子均保全。其HiGHS Optimal仅为浮点状态。四份分别限分母的原λ均有精确ΣPAIR/LAST<1，并在扩大域出现负余项，不能直接当作有理证书。
* 新`audit_discovery.py`只用标准库、固定n6整数公式，未导入旧发现/恢复/核验器，执行65536会员型与o=0/1原系数审计。全部四份有负余项；最简ω=0,o=1见证就是Σλ−1<0。完整分数和计数在`raw-discovery-exact-audit.json`及`audit-summary.json`。失败只针对所给λ表示，不否定相同原常数界，不构成SPE反例。
* 活跃原乘子均无PAIR:4/FLOOR:4:*。原build仍生成非法的PAIR:4，原verify不检查其真末两人前提；具体四点避开此行，通用程序仍须守卫。C=−8原点甚至未用第四枝或标签15，不能逐点都声称第四枝带来改进。
* 原恢复后B略增、λ改变；父Boss`r566-recovery`中恢复/核验回放分别逐字节重现原exact_cuts/exact_check。我对其做完整字段/字节比对，未重复运行这两个程序。结果见`parent-replay-comparison.json`。
* 恢复后具体线是有效根必要关系及近饱和充分条件，原JSON自身既不证明其精确性，也不证明一般half/图最优。后续齐次阈值点另有源身份，不混入本四点。

## 已完整实读与比较

已先读根`AGENTS.md`、`cleanup/README.md`、`cleanup/OBJECTS.md`及`tools/README.md`。主源原JSON全文；以下源/对象均实际全文读取而非只看命中：

| 材料 | 本次作用 |
|---|---|
| 原fourcopy_discover.py（a7871dcfea436346714e） | 矩阵、行、λ截断、有理化和默认参数 |
| 原fourcopy_recover.py（104f216890e7258dcbaa） | 网格、统一CAP修复、归一化与B外修复 |
| 原fourcopy_verify.py（b8087c1520fc41170d0e） | 纯整数逐型逻辑及缺少PAIR语义守卫 |
| fourcopy_exact_cuts.json（5f31af1e2864cf62f036） | 四个不同于原发现的精确后继证书 |
| fourcopy_exact_check.json（fc4c2103c836d84569d1） | 四份65536型全部64分组报告 |
| fourcopy_root.md（c4ee9ac772eef3426940） | 原路径、支持线、阈值、旧实现来源、非half边界 |
| research_1 README/HANDOFF | 原交付范围、浮点探索与精确成果身份 |
| 旧six_maxroot/NOTE_ZH.md（28a95425505cdeb41199） | 两/三复制常数、同策略路径及精确桥 |
| 现“共同目录完整历史模型” | 单位客户/全部有序历史SPE/重复与零边界 |
| 现“末两人重叠比较与任意索引聚合” | PAIR独立自足证明及六索引聚合 |
| 现“四复制支持线的近饱和半覆盖条件” | 后续PAIR:4纠错、具体证书与旧审查范围 |
| 现“四复制根阈值的有理证书回放与发现器守卫” | 后续阈值点身份、40乘子与合法行区别 |

对全冻结源用`clean search 'discovery_n6_c4'`及`clean search 'fourcopy' --path '*.md'`检索，结合当前全仓`rg`检查相关正文。`PAIR:4`在冻结Markdown没有命中；该明确守卫来自当前已清洗正文，并通过程序与具体乘子复核。未把后来正文的“已通过”字段当作本次原四点的证明。

本次唯一负责处置主源ebd53a3e84a17c3430eb；比较源清单不表示替父Boss领取或完成那些源。`receipt.json`是建议，主源可按integrated：原数据与独有数值细节保全、与恢复证书明确分离，并新增其原λ表示失败的精确说明。关系语义写在草稿末节；未创建阶段三图。

复现本次新增审计：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 cleanup/workspaces/Boss1/r566-discovery-json/audit_discovery.py
```

程序只覆盖本主源的固定n6/c4参数，不是通用发现器接口测试。无数值LP新运行，未创造有理最优性证书。
