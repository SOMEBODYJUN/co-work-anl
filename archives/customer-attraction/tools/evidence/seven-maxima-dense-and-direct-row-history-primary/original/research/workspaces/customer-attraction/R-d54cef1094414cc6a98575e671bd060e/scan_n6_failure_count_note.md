# 七极大六人扫描的失败计数核对

更新：2026-10-27。本文是证据口径核对，不是 Q-CAG-HALF-6 的证明或反例。

## Exact scope

输入是冻结包 `evidence/certificates/customer_attraction/seven_maxima_partial_checkpoint.tar.gz` 中的 `seven_maxima_new_rows/scan_n6_seat.json`。该扫描属于七个极大覆盖、六名提供者的必要条件/席位行证书搜索；它不是完整原模型 SPE 证书。

## Exact observation

JSON 的 `certificates` 数量为 877。逐项统计：

- 832 项含 `multipliers`，可以由已有席位行审计重放；
- 45 项没有 `multipliers`；其中 1 项有 `rounding_failed: true`，即路线 `[0,0,1,1,1,1]`、target `125`，记录值 `0.5454545454545454`；
- 因此真正未获该必要条件证书的是 `45-1=44` 项。

正文写“44 条缺口”与这个含义一致；若直接把 JSON 的 `failures` 数量称为 44 会少数一项。为避免歧义，今后写作使用“45 failures = 44 genuine failures + 1 rounding failure”。

## Reproduction

在仓库根目录运行：

```sh
python3 - <<'PY'
import json, tarfile
from pathlib import Path
p = Path('/tmp/seven_maxima_partial_checkpoint.tar.gz')
# 将仓库中的冻结包复制到临时目录后读取，避免修改冻结证据目录
with tarfile.open('evidence/certificates/customer_attraction/seven_maxima_partial_checkpoint.tar.gz') as z:
    raw = z.extractfile('seven_maxima_new_rows/scan_n6_seat.json').read()
d = json.loads(raw)
assert len(d['certificates']) == 877
with_mult = sum('multipliers' in x for x in d['certificates'])
rounding = sum(bool(x.get('rounding_failed')) for x in d['failures'])
assert with_mult == 832 and len(d['failures']) == 45 and rounding == 1
print({'certificates': len(d['certificates']), 'with_multipliers': with_mult,
       'failures': len(d['failures']), 'rounding_failures': rounding,
       'genuine_failures': len(d['failures'])-rounding})
PY
```

(The unused `/tmp` assignment in this snippet is only a label; the script reads the frozen archive directly and writes no evidence.)

## Status and limitation

This count does not change the mathematical status. The 44 genuine failures are failures of the specified necessary-condition certificate search, not target counterexamples. The one rounding failure is a search/serialization issue. No complete all-history pure SPE strategy is supplied by this scan, and no statement about `2W\ge OPT_6` follows from its ratios.
