# 冻结64支持背景行：五来源和固定点补闭

本批Boss2只处置以下5个已claim来源，总原字节26299B。claim pushed `5a6e293ad99e4de7e6f7e3d41d8952a4698af66d`。所有原程序及三JSON十二字段/各64有理坐标均完整实读，准确双冻结定位在[source-manifest.json](source-manifest.json)。只写新独立对象，未更改既有BNS/AP证明、版本资源或旧v1审查。

| ID | 冻结文件 | 字节 |
|---|---|---:|
| afa4ad1e53f27ca5c63f | background_rows_fixed_support_actual_only.json | 4642 |
| 599d07b2c55cfa73bff9 | background_rows_fixed_support_full_v1.json | 4172 |
| cd4c8e73a9ab9f06c7bb | background_rows_fixed_support_v1.py | 5964 |
| b2e5a96895f0e6fba591 | background_rows_fixed_support_v2.json | 4709 |
| d9b4ac0be0fb3853eb93 | background_rows_fixed_support_v2.py | 6812 |

原件保存在original/下原冻结路径。full_v1和v1.py分别与旧报告24e8313ac2c86cbfbbfd、旧程序ac5bc2bdfb7f895f6d57同SHA；[same-byte-aliases](same-byte-aliases.json)明确复用，非第二次历史实验。两新正文是输入/程序合同和有限三点核增量，不重复原普遍AP数学。

## 实际输入和运行范围

[dependency-manifest.json](dependency-manifest.json)绑定现有已发表five-player-indexed中17182B helper与77420B证书，均完整读；原程序只执行helper首次`from pathlib import Path`前定义段。原根标记__init__.py仅供is_file查根，不导入其代码。其余17件已读相关对象/原件身份见[comparison-bindings](comparison-bindings.json)。五源范围不随相关读取扩大。

[check-saved-points.py](check-saved-points.py)是标准库固定点核。其旧437行复用helper定义，新1430行按完整AP公式重建；actual-only只取前400行。原两入口没有actual-only生产开关，本批没有该历史入口，不能声称重放了它。

准确事件是2次新实现入口尝试：第一次在新增行/三点检查前误要求证书列表顺序等于evaluate插入顺序而exit1；[attempt1代码](attempt1-check-saved-points.py)、[stderr](attempt1-fixed-point-check.stderr.txt)、[事件](attempt1-fixed-point-execution.json)和空stdout原字节保全。修正为按名字核对应关系后，第二次exit0，完整固定检查成功1次，见[最终事件](fixed-point-execution.json)。原失败事件中的代码SHA对应已归档attempt1原字节；未改原输入或原报告。

最终[stdout](fixed-point-check.stdout.json)保完整4571本域有理slack、三域交叉、原点新增行亏损、所有共同M_C。短表见[fixed-point-summary](fixed-point-summary.json)。三个新点各自通过837/1867/1867行；actual-only点入完整域38负行；fullv1点入v2有3负行；v2通过三个域。只4组共同M从5降4，43条行/2040项实际改变。行名对齐单独说明于[row-name-alignment](row-name-alignment.json)。

复核入口使用已保存版本并将输出导向新外置文件：

```sh
python /absolute/staged-or-published/path/check-saved-points.py --repo /absolute/result/repo
```

本批成功后未再执行该入口。原v1/v2程序、NumPy/SciPy LP、helper6144全域审计和SPE求解均0次。若未来确需原生发现器，须另在仓外根按原research/workspaces路径放原程序、按tests/audits及evidence/certificates路径放两个同SHA依赖，并放根定位标记customer_attraction/__init__.py；需要NumPy/SciPy，版本历史未给，且程序导入就会求LP并写旁边报告。不能在冻结证据目录调用后覆写报告。新固定checker无需该marker/NumPy/SciPy，也不会写其输入。

## 数学边界与关系

三个x是必要投影的非负有理质量，不是完整游戏策略。通过全部所写行且O>2足以阻断这些有限行单独推出O≤2W；不提供精确最优性、新全域dual或SPE可补全。五个比较主题并集O未在新点认证为真正OPT。单位客户清分母不会补跨历史动作一致性；同覆盖异标签、空题、重复、有序离轨平局均未删去。

[relation-evidence.json](relation-evidence.json)保5条人工解释的实现/有限检查/别名/补闭/版本关系与明确不造的边。旧BNS资源的当时缺件声明原样保留，当前取得由新对象衔接；原八SPE审计和ordered mutation不在本批主来源范围。
