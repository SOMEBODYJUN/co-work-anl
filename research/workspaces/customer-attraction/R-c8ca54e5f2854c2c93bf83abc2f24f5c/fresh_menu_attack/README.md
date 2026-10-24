# AFC fresh-menu candidate: independent attack and exact menu envelope

身份：本目录仅服务于一般候选 AFC 的反例检验。原一般半覆盖及 AFC 均未解决；本轮没有分离出反例，也没有一般付款证明。没有读取 `aggregate_security` 旧稿，没有复用 old36 输入、没有外发、没有 git 操作。

- [`contract.md`](contract.md)：一般候选的精确合同、全历史菜单包络/实际顺序递推的自足正确性证明、公共客户无损删除。
- [`full_menu.py`](full_menu.py)：固定原类实例和查询 p，最大化全体完整历史纯 SPE 的 AFC gap；`best(p, exact=True)` 对有理 p 使用精确分数。可 materialize 一份完整有序历史策略。
- [`attack.py`](attack.py)：最初固定计数策略锥的数值反例攻击；同时提供有限计数/收益及固定策略 p-LP 基础设施。不是一般证明或逐 n 项目。
- [`verify_oracle.py`](verify_oracle.py)、[`oracle_audit.jsonl`](oracle_audit.jsonl)：独立按定义枚举完整策略，对比菜单包络；含空主题、零客户、重复覆盖及全部平局边界，精确一致。
- [`runlog.md`](runlog.md)：本轮实际运行及其限度。

下一步若重用工具，只针对 AFC 的明确构造/机制作攻击；不要用更多阴性种子制造正证据。解析承重点仍是：后继全部真实 IC 如何使混合查询的跨位置菜单核满足共同付款。这里的包络把任意历史选择完全保留，但没有提供那条新不等式。
