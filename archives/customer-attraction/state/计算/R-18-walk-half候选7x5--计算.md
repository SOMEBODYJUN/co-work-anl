# R-18 walk_half 7×5 有限 LP 候选

`708d828eb133b561ad99` 是 `n=7,m=5` 的 walk 搜索记录，源 SHA-256 为 `92ed78812272ca2e757463034c189ae7d19a98107d0ae0076a44054deec70664`。记录在 iteration 930、seed path `(5,5,6,6,6)`、175 个比较行、1554 个 rows 下给出 `mode=half`、LP objective `1.8`。其权重向量是浮点/LP 候选，JSON 没有完整整数化客户实例、全历史 Fraction certificate 或 deviation proof。

因此 1.8 只能说明该搜索器在固定候选锥/比较矩阵上的半覆盖目标值，不能说是 `W<OPT/2` 的 CAG SPE 反例，也不能直接和已验证的 full SPE W、OPT 比较。该记录与 earlier cone/walk probes 一起保留为 candidate-retained；第三阶段若要使用，必须补齐 exact cone reconstruction、整数客户克隆、完整策略证书和 OPT。
