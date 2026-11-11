# Stage16 发布空白修正与原稿恢复

第一次 Stage16 checkpoint 在 Git whitespace 检查退出2，尚未提交或推送。
只有新引理公式 NU 的一处行末空白，同时存在于正式正文和已冻结草稿。
正式正文将该 TeX 空白写作 `\quad`，并遵循登记规则升为版本2；数学内容不变。
计算对象版本13仅刷新引理正文SHA引用，其正文与已核计算证书逐字不变。

已冻结草稿没有修改。其原始 body.md 以及未推送的正式版本1，均逐字节
保存为本目录的确定性 gzip；original_bytes.json 给原路径、原SHA和压缩SHA。
解压 frozen_draft_body.md.gz 到原 stage16_new_lemma/body.md 可完整恢复
原冻结草稿，之后原 SHA256SUMS 仍可核验。当前本地原稿仍在原路径。
为满足正式发布的空白检查，仅该原草稿正文不作为文本文件入此次提交；
全部原稿信息已在无损压缩归档中，原检查结果和原候选登记保持历史原样。

恢复示例（目标不存在时执行；不覆盖后续稿）：

```python
from pathlib import Path
import gzip, hashlib
here = Path(__file__).resolve().parent
payload = gzip.decompress((here/'frozen_draft_body.md.gz').read_bytes())
assert hashlib.sha256(payload).hexdigest() == 'ea90cd908a69723b725225bdeee9fe9d95912b651d1359952fcbdc31ecaf41b8'
with (here.parent/'stage16_new_lemma/body.md').open('xb') as target:
    target.write(payload)
```

没有绕过任何 Git 检查、改动优化输入、重跑优化器或覆盖失败回执。
原 Stage16 checkpoint 回执亦按原字节收在本目录。Stage16b 必须重新
正式 register、edge-bind/check、checkpoint，只有返回 pushed 才算远端可恢复。
