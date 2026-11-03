# 均匀组合偏离旧程序的原件与重放

`original/` 保留两份主源码原布局和原字节。[来源清单](source-manifest.json)给主文件、四份共享规范模块及19对冻结同名实例／证书的路径、ID、SHA-256和冻结提交。规范模块复用同目录的既有发布原件，冻结输入通过 `work.py clean show ID --out PATH` 可按清单恢复。19对仅为有同名配对的冻结文件，9份符合原脚本要求的顶层 `actions`。证书外壳内即便另含完整策略，也由原脚本跳过。此包未更改原文件和原入口，也不替输入或依赖另行完成清洗。

从结果仓库根目录可按下面步骤在独立目录重组原布局。浮点部分需要 NumPy、SciPy，精确原入口仅依赖标准库及规范模块。

```sh
repo=$PWD
pkg="$repo/archives/customer-attraction/tools/evidence/uniform-portfolio-legacy"
run=$(mktemp -d "$repo/../uniform-replay.XXXXXX")
python3 - "$repo" "$pkg" "$run" <<'PY'
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

repo, pkg, run = map(Path, sys.argv[1:])
manifest = json.loads((pkg / 'source-manifest.json').read_text())
for group, entries in manifest.items():
    for entry in entries:
        destination = run / entry['path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        if group == 'frozen_replay_inputs':
            subprocess.run([sys.executable, 'work.py', 'clean', 'show', entry['id'],
                            '--out', str(destination)], cwd=repo, check=True)
        else:
            source = (pkg / 'original' / entry['path'] if group == 'primary'
                      else repo / entry['repository_path'])
            shutil.copyfile(source, destination)
        raw = destination.read_bytes()
        assert len(raw) == entry['size'] and hashlib.sha256(raw).hexdigest() == entry['sha256']
shutil.copyfile(pkg / 'replay/audit.py', run / 'audit.py')
PY
source_dir="$run/research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/global"
OPENBLAS_NUM_THREADS=1 python3 "$source_dir/uniform_portfolio_cone.py"
python3 "$source_dir/uniform_portfolio_search.py"
python3 "$source_dir/uniform_portfolio_search.py" --random
python3 "$run/audit.py"
```

[运行元数据](replay/execution.json)绑定本轮的三个原入口执行。[独立审计](replay/audit.py)在实际九个完整策略及一个人工控制实例上，用原始客户类型、完整有序终局和 `Fraction` 逐历史重算IC、逐有序比较元组重算覆盖及真查询，并核对原 `attack` 和浮点 `cone_data` 的结构与系数。[审计结果](replay/audit.json)保留各输入的精确目标、比较覆盖、真实覆盖最优和检查规模。审计没有为随机策略锥生成精确对偶，也没有把默认100轮无正浮点或随机1000轮未见严格正值提升为普遍结论。
