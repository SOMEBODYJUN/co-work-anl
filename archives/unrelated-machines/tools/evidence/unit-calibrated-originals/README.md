# 强计数证书、独立实现、严格单位见证与三反例原件

[正式审查](../../../state/审查/单位读出强计数证书与严格单位五三的原实现--审查.md)完整解释数学模型、强证书充分性、条件必要性、固定D两分支、严格CONFIG(1)整轨见证、五三构造、三反例证明及有限实现边界。

`original/` 是本批四个 actual `clean show` 的原字节：

- [规范模型/三个构造模式](original/unit_readout_calibrated_cardinality.py)，SHA `039ac7db…f175c4`。给强见证、均匀校准和固定D构造互为不同入口；自身 audit 才有三个小例的有限 OPT 枚举。
- [独立 tuple 模型与有理槽审计](original/unit_readout_calibrated_independent.py)，SHA `b87e5c38…608b1e`，不 import 规范程序；只提供 `--output` 有限审计入口，没有用户 JSON 输入或 LP solver。
- [整轨字面量见证→五三原程序](original/unit_readout_literal_gap.py)，SHA `8dfc9770…833b25`，复用规范模型/负载/Hall，只检查给定精确见证，不寻找或求解 LP。
- [三个完整原矩阵证书](original/unit_readout_calibrated_counterexamples.json)，SHA `56bd2e6f…347f4e6`，每例保原输入、资格、完整σ与全负载。其真实OPT依次1、7/4、2，全部合法σ数162、512、1024。

`comparisons/` 保全文实读的强计数 canonical、配置阈值 canonical、完整校准审稿及其版本纠偏；这些比较源不在本批四源 claim/done。全部7原件的完整commit/path/ID/大小/哈希见[provenance.json](provenance.json)。规范核同上一批已全读依赖实际 byte-identical，本次未为完成声明无故重读相同字节。

本批从仓库根只运行一次[replay.py](replay.py)：

```sh
python3 archives/unrelated-machines/tools/evidence/unit-calibrated-originals/replay.py --run-dir /workspace/scratch/37f0f9248cfc/boss4-next-cache/unit-calibrated-originals-run-001
```

Python 3.12.14，exit0。程序先把四源原字节复制到外部run的 `source/`，避免同期Git同步短暂隐藏未跟踪文件影响子进程；执行文件hash与这里 `original/` 完全相同。三个audit及四个不同CLI各一次，全exit0，命令、cwd、stdout/stderr及退出码在[commands.json](replay/commands.json)。没有重跑前批成功的叶流/selector-mixing入口，也未重跑本批已成功程序。

实际产物原样复制到 `replay/`：

- [cardinality-audit.json](replay/cardinality-audit.json)：seed110841，1464输出/85094jobs，895穷举wiring/r、240强见证、320固定D及边界。
- [independent-audit.json](replay/independent-audit.json)：seed430691，90常规有理证书、空、522比特分母、188条件C1 profile、288固定D。该程序同时打印[2102字节stdout](replay/independent-audit.stdout)，与JSON输出一致。
- [literal-audit.json](replay/literal-audit.json)：seed1101717，4337输出/59121jobs，4168穷举wiring/权重、160随机源见证及边界、15非法输入拒绝。
- 三core模式的显式输入/输出：`calibrated-input.json` / [calibrated-cli.json](replay/calibrated-cli.json)，`bounded-input.json` / [bounded-cli.json](replay/bounded-cli.json)，`witness-input.json` + `witness-t.json` / [witness-cli.json](replay/witness-cli.json)。见证分母为 `10^5000+151`，读取端已解除Python默认十进制位数上限。
- literal的[显式payload](replay/literal-input.json)与[输出](replay/literal-cli.json)，5jobs、实际峰值3/2。此CLI返回给定见证的调度，不是求LP或调用通用promise判定器。

其余六入口stdout为空，七stderr均为空，空文件也原样保留。多数audit样本由不可变源码和seed确定，输出仅含汇总及选定边界证书；没有捏造全部样本独立矩阵日志。

新checker不import三原程序，从显式叶输入重建机器及所有原job资格，再核完整σ和Fraction负载。它实际查17份已保存输出记录（含重复实例）/376任务归属/310列机负载，另从原JSON三例重建资格并全枚举1698份合法σ。规范自己的1698与新枚举是同三个输入的不同实现，不相加成更广的覆盖。结果见[verification.json](replay/verification.json)，外层执行及全部28运行文件hash见[execution.json](execution.json)。

复现时给一个尚不存在的新目录；脚本和原CLI均拒绝覆盖。需要的只是Python标准库；无网络、Git或LP依赖。独立数学证明、原软件内部有限assertions、新checker有限重算、外审及一般UM目标各自分开；没有实际通用LP/CONFIG/不可行性后端，也没有为这些未实现算法提供伪实验。
