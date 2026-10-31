# R-23ab promotion/reset evidence

九个冻结源均以 `clean show` 全文读取，绑定和 SHA 在 `source-manifest.json`。

## 重放

- `independent_zero_source.py`：exit 0；85 个 ordered-tree states、21 个决策历史、84 个 IC 比较，实际 `(0,1,2)` 与 promotion `(2,3,2)`，势能差 1、首位源 regret 0、`W=OPT_3=7`。
- `verify_promotion_reset.py --t 1`：exit 0；13 个有序历史、39 个含自身 IC 行，三主题强 pair reset tax=1，`W=OPT_3=7`。
- `verify_zero_regret_promotion.py --t 1`：exit 0；21 个有序历史、84 个 IC 行，零来源 regret 仍有势能差 1。
- `promoted_fork/verify.py`：在同批 raw 目录下因缺失外部冻结点 `R-964.../combined_702.json` 以 `FileNotFoundError` 退出；保留失败，不伪造 full replay。

所有 exact 输出明确写明不是 HALF 反例；promoted fork 的两个 point evaluation 也明确为单行 necessary-system 检查、无 SPE claim。
