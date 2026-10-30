# 半密度半槽与独立profile原程序

[正式审查](../../../state/审查/半密度半槽与指定根锐族的独立原程序--审查.md)保全部模型、量词、证明、真实森林、锐族和本次发现的十进制文本限制。

本批两个actual `clean show` 原件：

- [unit_readout_half_density_three_halves.py](original/unit_readout_half_density_three_halves.py)，17491字节，SHA `050e0534…b2b3fb`：全变量/全job、两轨所有实际叶 `d≤2A`、任意显式深度和wiring、半片一次matching与r=ceil(k/2)真实森林。无SAT、LP、OPT或YES寻找。
- [unit_readout_selector_profile_independent.py](original/unit_readout_selector_profile_independent.py)，8559字节，SHA `3c54c735…54aa1a`：不import仓库核，自建p1..4双共享clause完整nullable矩阵，序列化重读，再核全部资格/σ/负载和符号整数容量下界。它是指定profile锐族生成器，不是一般mixing算法。

两冻结commit/path/ID/完整hash与四份先前已全读比较依赖见[provenance.json](provenance.json)。数学正文和旧完整profile JSON按相同SHA复用；本批没有重跑其旧成功入口。

实际只运行一次新[replay.py](replay.py)，从仓库根：

```sh
python3 archives/unrelated-machines/tools/evidence/unit-density-profile-originals/replay.py --run-dir /workspace/scratch/37f0f9248cfc/boss4-next-cache/unit-density-profile-originals-run-001
```

Python3.12.14，外层exit0。源码先逐字节复制到外部 `source/`，五个子进程的实际argv、环境覆盖、expected/actual exit与stdout/stderr在[commands.json](replay/commands.json)，原捕获全部保存：

- [half-audit.json](replay/half-audit.json)：seed110803，1160穷举wiring、300随机、3深树大A、3空、1非空零容量空clause、1既有split锐例，共1468内部构造检查，6非法输入拒绝。输出只有汇总/选定sharp记录，多数输入由冻结生成器和seed确定，不是1468完整外部矩阵日志。
- [half-input.json](replay/half-input.json) / [half-cli.json](replay/half-cli.json)：14机15job sharp的真实输出，42有限边、20槽、3个forest叶，峰3/2。新无import checker另核全部原资格、匹配、σ、每机负载及森林。
- [giant-capacity-input.json](replay/giant-capacity-input.json)：k1h1、容量 `10^5000+151` 的5001位十进制字符串，符合半密度。
- [half-giant-default-limit.stderr](replay/half-giant-default-limit.stderr)：显式 `PYTHONINTMAXSTRDIGITS=4300` 重现Python默认上限，原CLI在capacity_integer的int转换失败，exit1，没有创建输出。这是实际软件环境限制，不是调度不可行证据。
- [half-giant-unlimited.json](replay/half-giant-unlimited.json)：仅环境改为 `PYTHONINTMAXSTRDIGITS=0`、同输入同原字节，exit0；3jobs、4列机负载、8有限边、3槽、1forest叶，峰1，原巨大机器区间与未用unit零负载保留。没有静默修原源码。
- [selector-profile-audit.json](replay/selector-profile-audit.json)：新独立程序首次运行，完整p1..4原矩阵/全部YES/指定输出/负载/下界证书；3002矩阵格、1166有限边、480归属、300全机负载，未全调度枚举。其scope+certificates与已冻结旧JSON全字段相同；外围报告不同，不声称整文件byte-equal。

四个子进程成功exit0，一次parser边界exit1按预期保留；全部stdout为空（结果用`--output`），只有默认位数边界stderr非空。完整结果见[verification.json](replay/verification.json)，18个运行文件hash及外层命令绑定见[execution.json](execution.json)。未来复现给一个尚不存在的新目录；原程序及本runner拒绝覆盖。

这个冻结半密度源没有自行解除4300位文本上限，后来的校准core已修相同问题；两版本不能混称。大整数复现的环境要求、数学位复杂度和默认CLI实际支持范围在正文分开记录。

自由根的半密度三半、任意密度固定h的自由根叶流、给同一P完整YES后的指定profile重组是不同合同。p2锐族甚至满足半密度，但指定全正OPT5/3并不反驳其自由选根4/3界；原全局OPT仍1。单个14机sharp仅作绝对上界锐例。所有有限检查未升级一般UM、hardness、外审或新颖性。
