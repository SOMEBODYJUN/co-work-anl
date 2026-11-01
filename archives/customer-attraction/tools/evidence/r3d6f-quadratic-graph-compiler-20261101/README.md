# R-3d6f quadratic graph compiler evidence

本包保存 `9323c104d32cc08cc3c3` 及本轮补读的 `79d1d48e3736cc7459d5`、
`9858a49a31ed95b8e5f5`、`adf13c4bae60ea7cbc3c` 四个关联源的可复核副本。

- source review SHA-256: `5d767857b7962b61ec30d5d8491a35b19e92775af007449357f9145c40fa4c13`
- compiler SHA-256: `05253eee6b12148b99cf8b3ca3919fabfbebe4d8027748b4dadbe24fb6435b7e`
- audit SHA-256: `faae2d4c12b407eb8ce73e90123b4c965a1498c4f8827c635f532268a1ff9d2a`
- workspace metadata SHA-256: `7eae95a069ba841005e7a4424ac3a97ad87f860b6ad0ff289d2c792e1d3def52`
- finite scope: 2288 inputs, 4041 ordered paths, 8861 penultimate prefixes, 13566 subgames, 23523 certificate histories

证据只支持受限表示候选和列明有限回归；fresh 逐人保底、一般 Q-CAG-HALF 和新颖性仍开放。

本轮将编译器放入隔离的完整 `customer_attraction` 依赖副本实际运行一次；exit 0，
输出审计 JSON 与源文件逐字节一致。`workspace.json` 仅作为来源身份与存档的
provenance，不能承载数学结论。
