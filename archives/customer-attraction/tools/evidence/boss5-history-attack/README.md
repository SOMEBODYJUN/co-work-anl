# 早期机会全历史与逆向归纳攻击证据

正文：[早期机会全历史与逆向归纳攻击](../../../state/计算/早期机会全历史与逆向归纳攻击--计算.md)。本目录保四个主来源的全部独有语义，不包含新优化结论。

- `source-manifest.json`：四主来源和三项只读相关来源的冻结size、SHA256、blob和双commit定位。
- `original/full_bi_attack.py`、`original/full_history_attack.py`：原发现器字节；`original/cone_opportunity_attack.py`为fresh程序真正导入的prepare依赖。原始runpy保历史相对路径，直接运行需要还原冻结目录并安装NumPy/SciPy；下述审计不需要这些。
- `saved-policy-semantics.json`：两大JSON的完整可逆语义。40个策略共112040动作，无损编码为按历史深度递增、同层词典序的动作串；保全部质量、每条元数据、原cert键名及列表顺序。`unpack`与原JSON逐字段、逐条及顺序完全相等，源字节排版由冻结blob恢复。
- `audit_saved_policies.py`：独立标准库固定点核验器；无原程序导入、LP、BI或随机数。默认读语义编码，亦可用`--source-dir`绑定两个原大JSON、核完整往返相等后重新编码。
- `fixed-policy-audit.json`：每份原动作图在精确十进文本、精确binary64和另定义的限分母10^6质量下的全部IC资格、失败位置/数量、真OPT及实际收益。每份16806个非自身IC；不保存逐目标LP对偶，不认证原LP最优。
- `execution.json`：最终核验真实命令、退出码、输入前后指纹、代码/输出SHA和计时。此前首轮核验成功；第二轮增加无损往返验证并重算，单轮图/IC统计不可把两轮相加当不同策略。
- `relation-review.json`：与实际已读模型、锥表示、路径松弛、其它精确固定点和精确对偶扫描的关系理由；并非阶段三已建超图。

从仓库根可重复固定点核验：

```sh
python3 archives/customer-attraction/tools/evidence/boss5-history-attack/audit_saved_policies.py
```

BI保存28条，配置60不证明运行完60；fresh保存12条。限分母点通过25+12份，其余三份仍失败。原十进解释仅3+8通过，binary64为0+8通过。恢复点不冒原浮点输入，负浮点目标不充当精确锥上界，37份有效恢复点都不是half反例。
