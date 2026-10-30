# 局部权带作者核验的执行证据

正式数学合同和全部覆盖见[计算资源](../../../state/计算/局部权带份额与选择器的作者精确核验--计算.md)。本目录仅处理程序源 `23daf26f771898d45fcf`；Boss2 的报告 `8e829fa93d0c431621ad` 是全文读取的比较依赖，不重复登记。

- `original/verify.py`：原始 12056 字节代码，没有改写。
- `comparison/frozen-verification.json`：单独从冻结来源取得的原报告，5347 字节。
- `rerun/generated-verification.json`：本轮唯一一次原程序执行的完整输出。
- `rerun/stdout.txt`、`rerun/stderr.txt`：该次执行的完整 stdout 和 stderr。stdout 不包含两个序列数组，不能代替完整 JSON。
- `run-manifest.json`：实际 Python、argv、cwd、退出码、耗时与源码/输出 SHA。实际运行发生在外部缓存，之后逐字节保全到这里，没有更改历史 argv。
- `provenance.json`：两个源的完整冻结位置、源码依赖、已有执行检索及相关正式数学对象。
- `compare_reports.py` 与 `comparison-result.json`：只读取 JSON 的全字段/原字节比较，没有调用原审计。其单独执行信息见 `comparison-run.json`。
- `delivery-check.json`：来源 hash、全字段比较、回执/正文链接与稳定 ID 自查；不代替数学阅读。

原程序只使用 Python 标准库。实际执行为 Python 3.12.14，退出 0，stderr 为空；完整 JSON 与单独取得的冻结报告逐字节相同，没有排除字段。该次使用 `--generate`，没有再运行缺省比较模式。没有使用不同的 `independent_shapley_envelope.py` 作为本源码的旧执行，也没有额外重跑任何已通过的独立程序。

在仓库根用尚不存在的路径执行：

```bash
python3 archives/weighted-congestion/tools/evidence/weight-band-verifier/original/verify.py --generate NEW_WEIGHT_BAND.json
python3 archives/weighted-congestion/tools/evidence/weight-band-verifier/compare_reports.py
```

第一条会运行原数学检查；第二条只检查本目录保全的两份 JSON。源码的生成接口先检查不存在再写入，拒绝已有目标，但不提供原子独占创建；缺省接口读取源码旁的 `verification.json`，本目录应使用显式新路径。不要使用 `-O`。固定 seed、费用网格及游戏只构成有限证据。
