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
