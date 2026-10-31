# Santa 值桥最终 scope 延续核验

对象：`co-work-anl-boss11/research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md`。

本次实际 hash：`ce1c320ecd4d3833030307e4b4e3f4959ecd187281187c5914e80bddae8d13c5`。

此前全文实读版本 hash：`42450690b6dc42cf8a40371071a890aa14e272ef6295c7853c4f1b9bb7fdfcad`。

实际核验：读取新文件，在 §5 发现且仅发现一处下列新句：

> 它们的均匀权clause在任意至多d项上的和至多d/t=η，取support内d项达到，故确实满足，给第二个锐端点。

仅在内存中把它逆替换成此前句子：

> 它们的均匀权clause的任意d项和d/t=η，确实达到，给第二个锐端点。

逆替换后的**整文件** SHA-256 精确恢复为上述 `42450690…dfcad`。因此两快照除这一个 §5 字句替换之外字节完全相同；§1–3 与前置说明的 prefix 字节未变，其 SHA-256 为 `e8f0de12fb720519dac902e1d7f4a45e8efa6a19f16fa59571d6263268e68bf6`。

此前实读记录 `normalized_weighted_menu_santa_canonical_scope_review.md` 的 SHA-256 仍是 `af52cc08b9cf363124c4dcd82d29da6bdc5c8d88b046593e78218878bc4657d0`，本次未改其原字节。

**结论：本审查对 §1–3（`UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`）的通过认证保持有效。** 改动在本审查认证范围之外的 §5；本次不重新认证 §4–6 的规模 Claim，也不扩展先前范围。

未修改 repo、旧来源、旧实读记录、Work 或 Git；只写本 scratch 补充记录。没有运行后端或有限枚举。
