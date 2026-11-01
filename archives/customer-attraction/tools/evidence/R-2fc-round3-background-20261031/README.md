# R-2fc round3_background 三源清洗

三份源码均在认领后用 `clean show` 返回 0 并全文保存。源库存提交、blob、大小、SHA 和原始 stdout/stderr 见 `source-manifest.json` 与 `clean-show/`。本包补充既有人工背景/fresh 模板对象，保存独有的响应链闭包 LP 与全历史锥探针实现。

## 源级内容与运行

| ID | 文件 | 运行读数 | 数学处置 |
|---|---|---|---|
| `97d54543c818784dc7a5` | `two_player_closure_certificate.py` | `depth=2, mode=whole`: 8 labels, 39 slacks, HiGHS infeasible；`depth=0,1,3` 与 residual 变体也只作为有限复跑记录。 | 预设根 A→B、T/S 响应链的非负系数模板不可行；不否定其他付款结构。 |
| `2c9be9ee6595c5f0531d` | `two_player_full_closure_certificate.py` | `depth=2, mode=whole/residual`: 10 labels, 69 slacks, infeasible。 | 扩展为 B/T/S 三条响应链后，同样只否定该有限模板。 |
| `01e00a94dcb2d744c30b` | `whole_gap_cone_walk.py` | q=4,k=2,五次随机 trial smoke 退出 0，best=0；程序默认 q=6,k=3,trials=1000,seed=640130。 | 全有序历史策略锥上的浮点发现器；未发现不等式负点不构成证明。 |

两个 LP 程序把客户成员模式压缩成二值 bit，并以 `Fraction` 近似乘子只在 LP 可行时检查 residual；本批各运行均 infeasible，因此没有生成证书 JSON。`whole_gap_cone_walk.py` 将完整有序历史策略、单步 IC 差和 fresh 覆盖写成浮点 LP，候选需另做精确回放；本批 smoke 没有候选。

## 与现有对象的关系

既有 `R-2fc背景人工探针与两人fresh模板--计算.md` 已记录独立背景输入不是合法共同目录过去、以及另一份 17-slack/192-row fresh 模板的 infeasible 边界。本组三源的响应链闭包是不同的预设模板：`97d...` 仅含 T/S 两条链，`2c9...` 增加 B/T/S 三条链和更深命名回复，不能将其 infeasible 合并成“所有两人证明不可行”。`whole_gap_cone_walk.py` 进一步把比较放入完整有序历史策略锥，却仍是随机浮点搜索。

此前已有 52 客户完整根 SPE 精确证书反驳全局 `P+Delta>=freshOPT`，这里的有限 LP 与锥探针不替代该合法原模型证书，也不产生六人 Q-CAG-HALF 反例。空主题、重复动作、零客户、离轨历史平局均未从主模型删除。

`validation.json` 为 `passed=true`；三个源均 `py_compile` 通过，LP stderr 为空，smoke 探针 stderr 为空。没有任何运行结果给出一般半覆盖真值或反例。
