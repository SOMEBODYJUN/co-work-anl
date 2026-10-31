# 全历史策略与最优静态指派代码证据

主源为 `source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/terminal_query/independent_assignment_audit.py`，另一个冻结提交同字节；源ID `c9ed1adac413b4127fc0`。完整算法、输入/输出合同和发现的状态位边界见[正式算法对象](../../../state/算法/全历史策略与最优静态指派的双通路精确审计--算法.md)。

- `original/independent_assignment_audit.py`：292行原字节，SHA256 `1a4d5aabe8922f6cc03bd2a8e1c8508ef24653663ddee6f5adc47848655b9c5f`，没有修改。
- `manifest.json`：源与依赖SHA、保护文件未变、与冻结报告的比较范围、三个探针结果。
- `replay/`：原入口对1953客户输入一次真实复跑的JSON、stdout、stderr和运行清单。依赖直接引用相邻 `../dynamic-exchange/original/assignment_instance.json` 与 `assignment_full_policy.json`；不再复制依赖。
- `probes/non-spe-low-welfare/`：完整但非SPE的三人两主题策略，7个IC违规，演示half反例状态位遗漏SPE前提。不是数学反例。
- `probes/zero-customers-single-topic/`：合法m=p=1、零客户边界，非自最小松弛为null。
- `probes/missing-offpath-history/`：缺少一个离轨历史的输入被断言拒绝，exit1，未写输出报告。

每个探针仅执行原入口一次，写入其新建 `run/` 子目录。原1953输入入口也只执行一次，未执行发现、简化、Möbius编译器或项目solver。主复跑输出仅两条raw路径字符串与冻结报告不同，其他全对象相同；不是逐字节同文件声明。

从仓库根复现时选一个**尚不存在**的输出文件，并预先建好其父目录：

```bash
python archives/customer-attraction/tools/evidence/r105-code/original/independent_assignment_audit.py \
  --instance archives/customer-attraction/tools/evidence/dynamic-exchange/original/assignment_instance.json \
  --policy archives/customer-attraction/tools/evidence/dynamic-exchange/original/assignment_full_policy.json \
  --output /path/to/new-directory/new-audit.json
```

保持Python断言开启；输入变化、schema或求值断言失败与“IC违规但正常生成报告”是不同退出机制。所有结论须结合报告中的 `is_full_pure_spe`，不能只看exit0或half反例状态位。运行时长只描述本次环境，不是复杂度承诺。
