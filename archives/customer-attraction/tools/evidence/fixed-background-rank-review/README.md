# 固定背景收益切片的后继独立审查证据

正式对象：[固定背景收益切片的后继独立秩审查](../../../state/审查/固定背景收益切片的后继独立秩审查--审查.md)。

主源为后继审查程序 dc16c13a3d177b155261（4461 B）、报告 b5644b42ce76842a15e2（375 B）、审查稿 29186a82220f6a599450（3390 B）。三原件逐份 clean show 全文读、与已保存原件逐字比较；复用 [program](../fixed-background-circuit-basis/related/check_fixed_background_rank.py)、[report](../fixed-background-circuit-basis/related/fixed_background_rank_review.json)、[review](../fixed-background-circuit-basis/related/fixed_background_rank_review.md)，不新增副本。

- [source-manifest.json](source-manifest.json)：冻结身份、完整来源、各源独有内容、完整有限输入与九字段。
- [comparison-manifest.json](comparison-manifest.json)：实际读过的作者原文/程序、正式成果与旧事件；旧事件只复用，不重新运行。
- [replay/execution.json](replay/execution.json)：本次唯一后继原 CLI，clone 外隔离直接 subprocess，0.8138817440049024 秒，exit 0，stderr 空。
- [replay/fixed_background_rank_review.json](replay/fixed_background_rank_review.json)：新生成的 375 B 输出，与冻结原表逐字节相同。
- [replay/stdout.txt](replay/stdout.txt)、[replay/stderr.txt](replay/stderr.txt)：完整实际输出，未合成日志。
- [run_original_once.py](run_original_once.py)：原事件封装原样保存。固定 scratch 路径、拒绝复用已存在运行目录；不会由自查脚本调用。
- [check_static.py](check_static.py)、[self-check.json](self-check.json)：仅指纹、JSON/AST、链接、回执及现有事件一致性检查；不导入原程序，不跑数学。

实际新执行仅后继原 main 一次：152 基本背景/M 点、406 基向量、270 四槽组、90 聚合秩点、8 单位背景秩点。672 次 rank 是源码循环结构计数，不是动态追踪记录。作者成熟的 525-rank 入口没有重跑；无额外 helper、独立矩阵扫描、LP 或 SPE 求解。

无限参数结果依赖正文保全的 Cauchy/根计数/残数证明。输出的 universal_proof 是描述字符串，不是自动定理证明；本源不核聚合完整基或六收益恒等式。线性核、非负客户锥、真实激励锥及任意完整历史的全局付款分别保留；Q_CAG_HALF 为 OPEN。

原执行记录中的绝对路径标识实际事件；正式包不改写它们来假装在新路径重新运行。过去相关包写“本次未重跑后继”描述的是过去事件，不因此变成错误；这次是后来追加的唯一直接复现。
