# 完整历史纯SPE规范求解器

本目录保全冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 的规范实现、原始11项回归及两个数据依赖；逐文件来源和SHA-256见 `PROVENANCE.json`。数学说明见 [全集递推](../../../state/算法/完整历史纯SPE终局全集--算法.md) 与 [有限复现](../../../state/计算/完整历史求解器的精确复现--计算.md)。

在本目录运行 `python3 -m unittest discover -s tests -p test_customer_attraction.py -v`。包只用标准库。CLI为 `python3 -m customer_attraction 输入.json --certificate --output 新文件.json`；验证为 `python3 -m customer_attraction 输入.json --verify 证书或报告.json`。

所有策略是任意完整有序历史依赖的纯策略；计数缓存只缓存可实现终局集合。有限运行不证明一般福利界。
