# R51背景剩余利润探针：原件、重放与完整策略核验

[正式审查](../../../state/审查/R51背景非单调探针--审查.md)区分程序边界、18客户完整有限反例及静态背景定理。

主源 `db0a56f6801a92b9cff9`经 `work.py clean show`完整实读并导出到 [original/probe_background.py](original/probe_background.py)，2551字节，SHA256 `03233ccd894931bbf85cf792ea57148c9ffdbaf57760813db3f15b33f9489a38`。关联 [background_nonmonotone.json](original/background_nonmonotone.json)为1142字节，SHA256 `d39c34ac24c04ffb5bc321b4d41b6915bc9703e3cb72c3776a293f7e6c7c439e`。四项规范依赖逐字节复用已保存冻结版本并完整实读；六项来源、双冻结提交与各原SHA见 [source-manifest.json](source-manifest.json)。关联件和依赖是比较/运行责任，不由本次主源回执代填完成。

从仓库根执行：

```bash
python3 archives/customer-attraction/tools/evidence/R51-background-probe/replay.py
python3 archives/customer-attraction/tools/evidence/R51-background-probe/independent_check.py
```

[replay.py](replay.py)先核全部原件SHA，在临时工作目录用当前Python原样调用CLI、显式 `minimize()`、显式固定输入 `check()`；环境只把本目录original设为PYTHONPATH并禁写bytecode。原CLI/函数无网络或文件写入。三份stdout、stderr、argv/exit及Python版本均在 [replay/replay-summary.json](replay/replay-summary.json)旁保存。

- 默认CLI：seed99、trial8，32客户，最小剩余利润 $17\to109/6$。
- `minimize()`：18客户，$9\to11$，stdout与冻结JSON逐字节相等。
- 固定输入 `check()`：原总人数3、新总人数4，均余两人，精确确认上述最小值与计数。

当前minimize能重生原件，且原件结构与其返回值一致；历史调用命令及环境仍未记录，不由本次运行倒填。该贪心过程只保证其单客户删除固定点，不保证最少客户。

[independent_check.py](independent_check.py)不导入规范模型/求解器/证书核验器，自行展开18名单位客户，在每侧穷举 $4^5=1024$张完整两人策略，得到3张和1张SPE、两项和一项终局计数，最小利润9和11。[完整报告](replay/independent-full-policy-check.json)包含末位4×4收益表、最佳回复集合、两张最小见证和各20项含自身动作比较。它认证这个有限反例，没有外推一般half、根可达性、最小规模或分数门槛结论。

原样重放复用规范全集代码；独立枚举是另一实现。两者身份分开，不把重复调用同一求解器称双独立数学核验。所有新输出只写本证据目录，不覆盖来源或其他对象证据。
