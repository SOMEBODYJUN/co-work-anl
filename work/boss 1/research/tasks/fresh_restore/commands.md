# 执行命令和路径修复重放

命令在本地 Bash 的新克隆根目录运行。用 `SRC` 指向保存冻结提交的本地仓库，`DST` 指向一个不存在的新目录，`PROOF` 指向本记录所在的绝对目录。原执行中新 clone 一开始已经在指定 SHA 上。若源分支后来向前推进，下面的 switch 仅在刚创建的新 clone 中移动自己的分支。

```bash
test ! -e "$DST" || exit 1
git clone --no-hardlinks --single-branch --branch work/cn-crisis -- "$SRC" "$DST"
cd "$DST" || exit 1
frozen=1580e869769a9410b88d040acf08bab394c6f9d2
if test "$(git rev-parse HEAD)" != "$frozen"; then git switch -C work/cn-crisis "$frozen"; fi
git remote set-url origin https://github.com/SOMEBODYJUN/co-work-anl.git
git config --get user.name >/dev/null || git config user.name 'Research Workbench'
git config --get user.email >/dev/null || git config user.email research@users.noreply.github.com
ws='work/boss 1'
a="$ws/research/tasks/fresh_restore"
mkdir -p "$a/logs" .fresh-restore-runtime/tmp
cp "$PROOF"/{replay_plan.json,portable-jst-plan.json,portable-jst-experiment.json,replay_supplements.py,verify_replay.py,resolved-environment.txt} "$a/"
export TMPDIR="$PWD/.fresh-restore-runtime/tmp"
python work.py --workspace "$ws" status > "$a/logs/status-before.json"
python work.py --workspace "$ws" session start --actor 'boss 1' > "$a/logs/session-start.json"
python bootstrap.py --research > "$a/logs/bootstrap.log" 2>&1
py=.venv-methods/bin/python
"$py" crisis.py methods doctor > "$a/logs/doctor.json"
"$py" -m pip check > "$a/logs/pip-check.log"
"$py" -m pip list --format=json > "$a/logs/pip-list.json"
```

上述 bootstrap 是原执行命令。再次重建时可在 bootstrap 之前设置 `export PIP_CONSTRAINT="$PWD/$a/resolved-environment.txt"`，固定当次另外观测到的 cloudpickle 版本。已在实际新环境执行过以下命令。

```bash
"$py" -m pip freeze --all
"$py" -m pip install --dry-run --no-index --disable-pip-version-check -r requirements-research.txt -c "$a/resolved-environment.txt"
```

**原执行记录**。先对四份冻结计划的任务加 `fresh-` 前缀，合并为 `replay_plan.json`。对计划参数的逐项断言在 `verify_replay.py`。第一次执行的原始参数如下；绝对路径问题仍保留在本批历史记录里。不要依赖这个原计划来证明所有数据来自新目录。

```bash
"$py" work.py --workspace "$ws" compute plan --file "$a/replay_plan.json"
"$py" work.py --workspace "$ws" compute run --file "$a/replay_plan.json" --session-seconds 1800
"$py" work.py --workspace "$ws" compute plan --file "$a/replay_plan.json"
"$py" "$a/replay_supplements.py"
"$py" work.py --workspace "$ws" compute plan --file "$a/portable-jst-plan.json"
"$py" work.py --workspace "$ws" compute run --file "$a/portable-jst-plan.json" --session-seconds 1800
"$py" work.py --workspace "$ws" compute plan --file "$a/portable-jst-plan.json"
```

**纯新目录重建**。直接使用相同的十项和已修复路径的一项，不必重现那次外部读盘。下列代码断言每个作业输入和外接 CSV 均在当前新克隆内且存在。运行后按冻结输出逐字段验证，每一项都必须有实跑账目。整个流程不需要浏览器。

```bash
"$py" - <<'PY'
import json
from pathlib import Path
p = Path('work/boss 1/research/tasks/fresh_restore')
get = lambda name: json.loads((p/name).read_text())
plan = get('replay_plan.json')
fixed = get('portable-jst-plan.json')['jobs'][0]
plan['jobs'] = [fixed if j['id'] == 'fresh-historical-warning-audit-v2' else j for j in plan['jobs']]
for job in plan['jobs']:
    spec = Path(job['input'])
    assert spec.is_file() and spec.resolve().is_relative_to(Path.cwd())
    csv = json.loads(spec.read_text()).get('csv')
    if csv:
        assert Path(csv).is_file() and Path(csv).resolve().is_relative_to(Path.cwd())
(p/'all-local.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2))
PY
"$py" work.py --workspace "$ws" compute plan --file "$a/all-local.json"
"$py" work.py --workspace "$ws" compute run --file "$a/all-local.json" --session-seconds 1800
"$py" "$a/replay_supplements.py"
"$py" - <<'PY'
from pathlib import Path
import sys,json,subprocess
w=Path('work/boss 1'); p=w/'research/tasks/fresh_restore'; c=w/'compute'
sys.path.insert(0,str(p)); import verify_replay as v
old=json.loads(subprocess.check_output(['git','show',v.COMMIT+':'+str(c/'ledger.json')]))
new=json.loads((c/'ledger.json').read_text()); assert new['runs'][:len(old['runs'])]==old['runs']
rows=new['runs'][len(old['runs']):]; assert len(rows)==11 and len({r['id'] for r in rows})==11
for r in rows:
    key=r['id'].removeprefix('fresh-').removeprefix('portable-')
    initial=next(x for x in old['runs'] if x['id']==key)
    before=json.loads(v.before(c/initial['output'])); after=json.loads((c/r['output']).read_text())
    assert r['status']=='complete' and r['wall_seconds']>0
    assert v.canonical_sha(v.walk(before,'',{}))==v.canonical_sha(v.walk(after,'',{}))
    print(key,r['output_sha256'])
PY
```

在实际一次性验证克隆中，对首批和补跑完整账本分别保存为 `.fresh-restore-runtime/ledger-replayed.json`、`.fresh-restore-runtime/ledger-portable.json`，再把已归档账本位置的活动文件恢复为 `git show "$frozen:$ws/compute/ledger.json"` 的原字节。用 `python work.py --workspace "$ws" status` 和 `python work.py --workspace "$ws" session check --actor 'boss 1'` 核对 17/20，后者退出 3。在实际验证 clone 运行 `"$py" "$a/verify_replay.py" --formal-peer "$SRC"` 得到原提交严格移植检查单项为假，脚本退出 1。其他数值和修复后路径检查均为真。原始日志和对应快照保存在归档内。
