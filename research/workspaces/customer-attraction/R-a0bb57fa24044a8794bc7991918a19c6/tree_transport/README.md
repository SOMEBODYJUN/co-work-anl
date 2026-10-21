# Boss10：全历史树运输探索

本目录仅为本轮个人研究备份，没有证明一般半覆盖，没有修改共享正文或调用git/work.py。

- `benchmark_deviation_obstruction.md`：自足解析障碍，任意最优比较组J作为唯一偏离字母表，即使保留全部有序历史的独立行，也不能推出任何常数福利界；策略非SPE。尚待独立审查。
- `benchmark_deviation_audit.py`、`benchmark_deviation_audit.json`：对应有限Fraction核验。
- `benchmark_restriction_probe.py`、`benchmark_restriction_probe.json`：发现障碍之前的候选生成器与有限结果，限制偏离字母表的集合值递推与LP；数值点没有精确恢复时明确标记exact=false，不称SPE。

当前新方向：研究真实回复行动闭包，允许每个查询引入其真实续局所用的新查询行动，并允许无界离轨秩。上述字母表障碍不能否定这种闭包，也不能否定任何完整SPE结论。已有全深度收益形式图已经精确保留所有逐历史乘子，故不重述其Farkas等价为新证明。
