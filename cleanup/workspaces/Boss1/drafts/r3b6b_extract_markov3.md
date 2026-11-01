# R-3b6b extract_markov3.py 清洗摘要

源 `0fcebf2f4f2f4fd36ce8` 先枚举二步计数状态的最佳末位菜单，再为根和第二位构造候选，最后生成 StrategyCertificate 并执行 verify_certificate 的完整有序历史检查。它是固定小实例的证书提取器，区分计数降维的候选生成与最终 full-history 验证；不证明全部策略或六人目标。处置 retained。
