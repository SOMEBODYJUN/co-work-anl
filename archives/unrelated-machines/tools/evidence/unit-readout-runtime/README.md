# 单位读出叶流与选择重组：冻结原件和一次新运行

数学合同、完整证明、锐族、历史审查顺序与适用边界见[正式审查](../../../state/审查/单位读出叶流与选择重组的原程序及锐矩阵--审查.md)。这里保存四个本批源原件和一个使原 import 可工作的精确冻结依赖，原字节均与 inventory SHA-256 相符。依赖文件仅供复现，不属本批四源 done；完整来源定位见[provenance.json](provenance.json)。

`original/` 中：

- [冻结审稿](original/unit_readout_global_leaf_flow_and_selector_mixing_review.md)：先陈述重构/读后攻击/构造者复核、软件复用、历史运行与数学边界。
- [原叶流程序](original/unit_readout_leaf_flow.py)：每变量饱和的共同整数流、精确整数根、真实祖先 DP 和全任务调度。无需给定 YES；因子 `1+2^(-1/h)` 只在固定高度时统一小于 2。
- [原重组程序](original/unit_readout_selector_mixing.py)：给同一实例的完整真实 `C≤1` 见证和覆盖的指定 selector sign，非空 `k^h≥p`，active-only 校准槽和 Hall；其余轨全部父置。
- [原锐矩阵](original/unit_readout_selector_mixing_sharp_profiles.json)：p=1..4 的完整 machine-by-job nullable 矩阵、10 份给定 YES、4 份指定全正输出和全部机器负载。null 是不可用边。原全局 OPT 都是 1，指定 profile 精确值分别是 1、5/3、9/5、13/7。
- [精确模型核依赖](original/unit_readout_calibrated_cardinality.py)：两原程序复用 builder、负载核；重组还复用 Hall matching。文件里的小实例枚举工具未被本次两入口调用，不能据其存在声称实际完成 OPT 穷举。

本批只运行一次[replay.py](replay.py)，命令从结果仓库根发出：

```sh
python3 archives/unrelated-machines/tools/evidence/unit-readout-runtime/replay.py --run-dir /workspace/scratch/37f0f9248cfc/boss4-next-cache/unit-readout-runtime-run-001
```

Python 3.12.14，exit 0。实际运行产物随后原样复制到 `replay/`；命令日志中仍保留当时的绝对输入/输出路径。以后复现必须提供另一个尚不存在的目录；脚本拒绝覆盖，原程序也用 `--output` 独占创建新文件。无需网络、Git、外部 LP 或第三方数学包。

[commands.json](replay/commands.json) 保四个原入口的实际 argv、cwd、退出码和 stdout/stderr 文件名。两个 audit 的完整自带输入/结果在 [leaf-audit.json](replay/leaf-audit.json) 与 [mixing-audit.json](replay/mixing-audit.json)；两份 `--input` payload 为 [leaf-input.json](replay/leaf-input.json)、[mixing-input.json](replay/mixing-input.json)，对应输出为 [leaf-cli.json](replay/leaf-cli.json)、[mixing-cli.json](replay/mixing-cli.json)。每次原入口 stdout/stderr 均为空，因为结果通过 `--output` 写入文件；空日志是实际捕获的文件，不表示遗漏记录。

新 checker 不 import 原程序或模型核，从显式叶地址重建全部原资格，再比较输出 jobs 并累计 Fraction 负载；锐 JSON 的所有有限和 null 单元格都与双共享子句数学族逐格比较。完整结果见 [verification.json](replay/verification.json)，外层执行和文件哈希绑定见 [execution.json](execution.json)。

新 literal 部分计 15 份输出记录（包括两 CLI 的重复实例输出）、731 个任务归属、620 条列出机器负载；另查 12 份给定 YES/642 个任务归属。原重组 audit 有 empty 检查，但没有把 empty 保存到其 `full_original_certificates`，所以新 literal 的该数组检查只覆盖其中六份输出；没有擅加一个独立检查数。叶流的额外 OPT1 见证只由原 audit 核对，亦未加入新 literal 计数。锐 JSON 部分是另外 14 份完整调度/480 个归属/300 条全机负载、3002 矩阵格、1166 有限格。

两原程序有限 audit 通过、独立负载 checker 通过和一般数学证明是三个不同层级。这里没有通用 OPT、全局 CONFIG LP、森林枚举算法，也没有相应性能/全域实验；没有重演历史盲读，没有认证外审、新颖性或一般 UM 的统一次二目标。5001 位十进制容量由所有 JSON 读取端显式解除 Python 默认十进制位数上限，原数与原源码没有改变。
