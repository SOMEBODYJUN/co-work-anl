# Q-CAG-HALF-5：已证明

本包给出恰五名提供者、任意有限单位客户与有限非空共同目录、每份完整历史依赖纯 SPE 的

$$2W\ge\mathrm{OPT}_5$$

的精确计算机辅助证明。

- 从 `PROOF_ZH.md` 阅读完整证明、全部 53 个整数乘子和全域余项表。
- `ACTIVE_ROWS_ZH.md` 定义主证书的每一条必要行及其真实策略节点。
- `LOCAL_LEMMAS_ZH.md` 和 `MAXROOT_LEMMA_ZH.md` 给出局部推导。
- `certificate.json`、`row_manifest.json` 和 `components/` 是完整精确数据。
- `verify_certificate.py` 是独立重构的全域核验器；不需要原研究包或优化器。

复核（Python 3，主核验另需 NumPy）：

```sh
python components/verify_local_components.py
python verify_certificate.py --manifest row_manifest.json --output checks/independent_full_domain.json
```

预期结果：53 个正乘子，公共分母 `10000000000000000000000`，全部 6144 个条件通过，最小整数余项 0，负类型为空，共同 K 列余项 2264870。

本证明保留全部离轨历史、任意平局、重复主题、空主题及零客户，不对客户数和目录大小设置固定上界。
