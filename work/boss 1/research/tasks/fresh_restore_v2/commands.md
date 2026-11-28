# 复现与查验

设 `SRC` 为包含冻结提交的来源仓库、`DEST` 为尚不存在的新目录、`PROOF` 为本证据目录的绝对路径。下面的分支调整只在刚创建的独立克隆内执行。使用完成旧版恢复时的隔离 venv 或按同一组已记录的约束新建隔离 venv。

```bash
test ! -e "$DEST" || exit 1
git clone --no-hardlinks --single-branch --branch work/cn-crisis -- "$SRC" "$DEST"
cd "$DEST" || exit 1
commit=7394ed770c1b47d134bc51e64aa3bb721dc157e0
if test "$(git rev-parse HEAD)" != "$commit"; then git switch -C work/cn-crisis "$commit"; fi
git remote set-url origin https://github.com/SOMEBODYJUN/co-work-anl.git
git config --get user.name >/dev/null || git config user.name 'Research Workbench'
git config --get user.email >/dev/null || git config user.email research@users.noreply.github.com
p='work/boss 1/research/tasks/fresh_restore_v2'
mkdir -p "$p" .fresh-v2/logs .fresh-v2/tmp
cp "$PROOF"/{run_replay.py,capture_monthly.js,pack_months.py,verify_and_pack.py} "$p/"
export TMPDIR="$PWD/.fresh-v2/tmp" PYTHONDONTWRITEBYTECODE=1
# 本次实际解释器。不同目录布局可改为已验证隔离环境的绝对路径。
py=../fresh-restore-boss1/.venv-methods/bin/python
"$py" "$p/run_replay.py" > .fresh-v2/runner.stdout 2> .fresh-v2/runner.stderr
node "$p/capture_monthly.js" > .fresh-v2/logs/full-months.stdout 2> .fresh-v2/logs/full-months.stderr
"$py" "$p/pack_months.py" > .fresh-v2/logs/pack-months.stdout 2> .fresh-v2/logs/pack-months.stderr
"$py" "$p/verify_and_pack.py" --formal-peer "$SRC"
```

若要另建 venv，在调用 `run_replay.py` 前执行以下命令。此举是另一台机器上的重建方法。本次记录中的实际运行复用了已建的旧恢复环境。

```bash
PIP_CONSTRAINT="$PWD/work/boss 1/research/tasks/fresh_restore/resolved-environment.txt" python bootstrap.py --research
py=.venv-methods/bin/python
```

`run_replay.py` 会在初始状态记录 12 项账本、复原原 actor、实际运行数据准备和一个新 ID 的 v3 作业；随后保存追加后的 13 项账本及阶段过期检查，再将新目录的活动账本还原为当前提交。在同一克隆重复操作会沿用既有生成文件，验证新目录请使用新的空目标。核对旧版迁移时，两代引擎和示例都从本次克隆读取，旧版通过本地 `git show` 取冻结对象。若来源仓库的正式文件已更新，使用匹配冻结提交的只读对照目录，或省略 `--formal-peer` 只比较冻结 Git 对象与新目录。

原始证据包中 `repo/` 是仓库相对路径，`audit/` 下有命令、退出码、stdout、stderr、两版账本和新构建的正式 HTML。10 个未变模型的旧实跑原输出仍完整收在同一提交的 `research/tasks/fresh_restore/raw_evidence.zip`，新验证再次核对其归档成员和指纹。逐项结果见 `verification.json`。

## 读取一个策略情景的完整月账

`monthly_ledgers.npz` 采用 NumPy 的无损 ZIP 容器，字段各自存独立的二进制数值字典与索引。下面例子在本证据目录运行，读出 S464、严重下行情景、第 27 月的全部 43 个字段，旧新可分别选择。金额保留 JavaScript 输出的二进制双精度；布尔和空值有独立标识。

```python
import json
import numpy as np
from pack_months import decode

with np.load("monthly_ledgers.npz", allow_pickle=False) as book:
    m = json.loads(book["metadata"].tobytes())
    pair = next(p for p in m["pairs"] if p[:2] == ["S464", "severe"])
    for version, trajectory in zip(("old", "new"), pair[2:]):
        start, length = m["unique_trajectories_start_and_length"][trajectory]
        assert length >= 27
        row = {name: decode(book[f"k{i}"][book[f"v{i}"][start + 26]])
               for i, name in enumerate(m["fields"])}
        print(version, row)
```
