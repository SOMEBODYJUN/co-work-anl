# 对角基础行拆分原点的全行回代

正式对象：[对角基础行拆分后的有理必要点](../../../state/计算/对角基础行拆分后的有理必要点--计算.md)。主源 `dcb82d5dd75f34db2ecf` 的814800B原件复用 [split-basic-graph-program/related/split_basic_exact.json](../split-basic-graph-program/related/split_basic_exact.json)，SHA-256 `b12c4aa6b3cd106f3fb8e8a56be7469988456c0cb6e02b1741db8c09d587b34a`。不重复复制同一大点；源身份和共享依赖路由在 `source-manifest.json`。

## 本次实际事件

`audit_saved_point.py` 在隔离runtime导入未改原程序，仅调用原 `build()` 一次，取得3945×1905矩阵。先核全部列长度和非weight描述符，再以Fraction回代全部行、O/W/gap及元数据，另外核194组四态、2612交叠上界和actual均分收益。全部3945行非负，最小0、2232条为0。没有执行原CLI、优化器、旧73728型检查或独立全矩阵生成器。

已有 [56行独立报告](../split-basic-graph-program/independent-report.json) 的全部当前slack与本次精确相同；它的独立系数证据仍保原身份。此事件补足的是新split向量上的3889继承行，不能反向改写旧程序清洗时的实际运行范围。

`replay/execution.json` 记录真实argv、UTC、40.751秒、退出0和50个可用输入前后字节相同。构图30.540秒，完整审计脚本计时38.967秒。`runtime-input-manifest.json` 是47份冻结源、注释root标记、主点及旧56行报告共50个可用文件，不是加载追踪。`materialization.json` 是共享物化工具的输出。stderr原件为空。

## 复现

先选择仓库以外的两个新目录；以下 `REPO`、`RUN`、`OUT` 均应换成实际绝对路径。Python须开启assert，原模块导入需要NumPy和SciPy。命令中的复制保原字节，不修改归档原件；执行时间可以不同。

```sh
REPO=/absolute/repository
RUN=/absolute/new-empty-split-runtime
OUT=/absolute/new-split-output
python3 "$REPO/archives/customer-attraction/tools/evidence/combined-branch-master-program/materialize_runtime.py" "$RUN"
cp "$REPO/archives/customer-attraction/tools/evidence/split-basic-graph-program/related/split_basic_exact.json" "$RUN/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/split_basic_exact.json"
cp "$REPO/archives/customer-attraction/tools/evidence/split-basic-graph-program/independent-report.json" "$RUN/prior-independent-split-report.json"
python3 -B "$REPO/archives/customer-attraction/tools/evidence/split-basic-exact-point-boss3/audit_saved_point.py" --runtime "$RUN" --out "$OUT"
```

第一条物化47份冻结源及供原程序寻根的纯注释 `work.py`；它不是仓库控制器或认证入口。上述命令不会重新生成本次事件的UTC/进程记录；新事件须另记，不能覆盖历史事件身份。

## 文件和结论边界

|文件|保留内容|
|---|---|
|`audit_saved_point.py`|此次增强回代脚本原字节|
|`source-manifest.json`|主源双冻结身份、原件路由和共享依赖SHA|
|`materialization.json`、`runtime-input-manifest.json`|隔离目录物化及可用输入身份|
|`replay/all-row-slacks.json`|3945具名行的全部精确余量|
|`replay/summary.json`|O/W/K、165正列、全部组、交叠和旧点差异计数|
|`replay/overlap-lower-bound-failures.json`|189个低于真实交叠下界的完整见证|
|`replay/old-point-coordinate-differences.json`|与3889点之间222个质量差异|
|`replay/execution.json`、`stdout.txt`、`stderr.txt`|真实运行事件与输出|

189个辅助交叠不具当前边缘的字面实现，说明扩大域有限点不能直接当共同客户游戏；它不推翻原已列上界系统的精确可行性。改变这些量须重新核对应行。其它未列约束、精确最优性、可实现目录和完整历史SPE分别需要相应证据；本对象只认证所列3945行在这个冻结向量上的可行性，并不解完六人half。
