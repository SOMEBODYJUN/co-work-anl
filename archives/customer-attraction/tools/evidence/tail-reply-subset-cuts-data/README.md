# 回复子菜单查询的空报告

主源 `a11f2102ef9c4b9e2cc7`，534B；正文为[回复子菜单查询的空切面报告](../../../state/计算/回复子菜单查询的空切面报告--计算.md)。这份文件不是非空切面表：`selected=[]`、`best_float=[0,null]`。保原字节并解释全部六字段，不能凭“exactly negative”scope把空表认作精确无分离证明。

## 本包内容

| 文件 | 作用 |
| --- | --- |
| `original/tail_reply_subset_cuts.json` | 完整冻结原报告，SHA `90d4421d8de0b5012cba1554e6469d19fb4d2a9c629134c7fb7d5c34951de4c3` |
| `source-manifest.json` | 主源身份、共享输入/源码/已有核验路由、正式数学比较与事件边界 |
| `inspect_report.py` | 六字段语义、源码静态循环域、完整输入解析及已有审计绑定；不导入原模块、不调用helper/main/discover或LP |
| `data-interpretation.json` | 全字段原值和解释、1905记录消费域、原5075核验的引用绑定 |
| `planned-domain.json` | 96个源码结构键，每条明确标为静态计划域；不是96次成功LP或新价格点 |
| `selfcheck.py`、`selfcheck.json` | 静态文件、链接、源SHA、空表和96结构自查，无数学搜索 |

共享直接输入为 `../continuous-query-refinement-program/related/continuous_refinement_exact.json`（816661B，SHA `abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246`）。完整5730B生成器已保在该目录的 `tail_reply_subset.py`；本包不重复复制大点或源码。输入的全1905列结构/局部行审计在 `../continuous-refinement-necessary-point/point-audit.json`，已有原5075行verify在 `../continuous-query-refinement-program/rerun/`，这些都不是本空报告的发现过程重放。

## 本次处理与严格范围

数学上逐式保真实源IC、r名真实后继的背景利润定理及实际末位对每个真实后继的共同报价，解释两种非负乘子alpha/gamma和逐客户z最小化。四比较族包含均匀r子集、含a、排a，以及含a/b；最后一族在a=b、r≥2时合法重复两次T_a，r=1时只取T_a。固定结构为4实际源×2个R/Z×3轨道×4查询=96，不把重复查询记作独立线性方向。

原空文件没有保存每个LP的状态、价格、矩阵、对偶或运行时间。原代码失败LP跳过，best初始为0/null，精确检查仅在浮点候选足够负并有理化后进行。因此空selected既不是全结构成功记录，也不是全连续价格域非分离证书。

数据侧只做源码静态和已保存数据的解码绑定，0原helper、0原main/discover、0LP、0新切面评价；没有重复原5075核验。开发静态脚本经历两次不写结果的失败：初版将96误写为192的计数断言、随后将已有Python-dict stdout误按JSON解码；更正为96和 `ast.literal_eval` 后通过。两次失败均发生在新静态工具，未执行旧入口或发现LP。最终脚本与报告保最终合同，不隐去事件种类。

配套[程序对象](../../../state/程序/索引回复的真尾利润子集投影程序--程序.md)唯一承担原helper的组合查询/有限价格行实现核查；实际结果共用 `../tail-reply-subset-program/helper-audit.json`。96结构×3价格 `(0,0),(1/3,2/5),(7/5,3/2)` 得288行、548640个系数相等，288个所选价格余量全正；14336次显式元组比较和520辅助查询检查。首轮末尾计数误写192，保失败记录，更正后第二轮PASS。数据侧不重复该数学探针；固定价格结果不等于历史发现LP已重放或全连续域无切面。本包也不推断同W的5108点、3949阈值点或后10344点有相同搜索结果。

在仓库根可静态复核：

```bash
python -B archives/customer-attraction/tools/evidence/tail-reply-subset-cuts-data/selfcheck.py
```

若要重新生成纯数据解释，`inspect_report.py` 接受 `--repo`、`--report`、`--output`；输出选新目录。当前全部记录已处理，无需为了增加次数重复。下一次实质搜索若需要原main，应另用隔离目录、绑定源SHA并保每方向状态；不能把本空表当作全部合法切面的终止证书。
