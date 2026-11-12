# 585 行与新 full4177 v6 的真实后验诊断

Boss1 / RUN `six-boss1-20261111` / agent `/root/source2_cap3_tradeoff`。

## 结果

- 585 条 raw 513 列行：580 正、5 零、0 负。
- 每条行在新完整面上恒定：5265 个参数系数全部为零。
- 因而本二维 cap3 族没有负行切除新点或新面。
- 两个正付 C 零行仍对同一个真实后继施加共同弱态；正 CAP 强制 `R3=R4=C`，继而 `v4=K/5`。
- 真实 SAFE4 下界与此相差一个面上恒正的精确有理数，排除该完整面的 SPE 实现。
- 这个条件等号障碍尚未被宣布为新的无条件全模型行。

## 文件

| 文件 | 内容 |
|---|---|
| `proof.md` | 付款、全类型复建、单点/整面区别与真实 C/SAFE4 矛盾 |
| `diagnose.py` | 显式 SHA 输入的标准库主检查器 |
| `check_diagnostic.py` | 不导入主程序的独立逐列检查器 |
| `input_binding.json` | 唯一新 v6 的五份显式路径/SHA及冻结源身份 |
| `source_true_COST_recheck.json` | 225 顶点、74880 COST、4680 全弱态、完整顶点 metadata |
| `full_v6_core_recheck.json` | 全 4177 primal/dual、完整面和 513 非负条件的独立核验 |
| `complete_face_parameter_domain.json` | 原完整面全部字段和 4177+513 条参数条件 |
| `point_slacks_all585.json` | 全部原 metadata、真权/K/freeEC和精确点 slack |
| `face_affine_all585.json` | 全 585 条九参数仿射式及排除范围标签 |
| `zero_point_true_equalities.json` | 点上五零行真实等号清单 |
| `zero_face_true_equalities.json` | 五零行在完整面上的类型质量与全弱态 |
| `positive_true_payment_support.json` | raw 4012/4067/4107 的实际对偶权逐项乘真 IC/CAP/SAFE/BR及自由EC |
| `shared_C_zero_SAFE4_obstruction.json` | 同 C 后继及条件真 SAFE4 障碍的机械证据 |
| `negative_true_deviation_obligations.json` | 空集；本次无负行 |
| `independent_diagnostic_check.json` | 第二套标准库检查结果 |
| `failure_log.json` | 保留首次工程错误的完整失败记录 |

所有确切坐标均用整数或有理数字符串，浮点发现摘要不参与证明。九个自由坐标只是仿射参数数；不声明可行相对维数九，不删减任何面条件。

## 使用

主检查器的 `prepare` 只复核冻结 585 行源，不读任何 LP 点。

正式运行必须显式传入 `--solve-id full4177_v6`，以及 `--input`、`--certificate`、`--face`、`--certificate-check`、`--face-check` 各自的绝对路径和对应 `--*-sha256`。本次精确引用存于 `input_binding.json`，没有旧点或猜测路径回退。

`python check_diagnostic.py` 独立复核已完成的诊断；冻结后复跑应在目录副本中进行，以保持原包字节不变。所有程序不调用优化器，不改 REPO，不写旧冻结包。
