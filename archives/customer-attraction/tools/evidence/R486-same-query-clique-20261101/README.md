# R-486 same-query 2396 clique evidence

本目录保存 R-486 的 exact clique evaluation、其关联的冻结 2396 投影输入和独立重建脚本。

- `evaluation_2396_clique.json` source SHA-256: `820a01f89662c9dfd6d479f07d900c472b5ab67101c293e8f73fbf602ea136b9`
- `enhanced_2396_exact_obstruction.json` related source SHA-256: `ce1f9d8b1036256b7e40e1eb5c990fdcc4f33c7fed3f2aa796bdf8245b9d0c4f`
- replay: `evaluate_2396_clique.py`, exact rational local reconstruction, eight unit-weight directions
- result: `exact_evaluation_passed_no_cut`; new-row slack range `4.713989929899356`–`6.383809335069987`

该证据只覆盖相同前置查询族和冻结投影点。它不认证底层 2396 行 LP 的全局最优性、完整 SPE、真实 OPT 或五/六人半覆盖结论；未记录的真实回复菜单也没有被补造。
