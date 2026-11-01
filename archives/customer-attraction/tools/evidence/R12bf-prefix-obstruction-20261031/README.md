# R-12bf direct-cover prefix obstruction evidence

本目录处理 clean IDs `c92b9d5a36aaf85d4cb4` 与 `0d96bd111b904835c9f0`。正文为 `archives/customer-attraction/state/障碍/R12bf实际前缀比例嵌入统一族与61客户有理复核--障碍.md`。

- `original/incumbent_lipschitz_obstruction.md` 是五客户统一族的完整解析源：任意 $k\ge1$，`f_3(A^k,P)=1`、`f_2(A^(k+1),P)=2`，精确否定 `f_r >= (r-1)/r f_(r-1)` 的辅助桥。
- `original/verify_actual_prefix_obstruction.py` 是 61 客户证书的独立定义级核验器；其 related material `actual_root_B_certificate.json` 由 clean show 读取但不是本批认领源。
- `runs/verify_actual_prefix_obstruction.stdout.txt` 为真实 exit 0 输出；stderr 记录首次缺依赖运行的失败以及补齐 related material 后的成功重放。
- `source-manifest.json` 保存两项 clean source 的冻结路径、blob、SHA-256 和大小；`comparison-notes.md` 记录与 direct-cover README、既有 Lipschitz 反例页的逐项比较。

这批是辅助桥的 exact obstruction 和有限证书核验，不是当前六人主目标的完整反例或证明。
