# Boss2：末位标量与静态福利桥接的九份原始来源

本证据目录保全 R-c4732bee2f7b4e50a70568170e3334ae/global_exchange 的九份冻结来源，共95844B；完整路径、稳定ID、blob、SHA256与两个相同内容的冻结提交见 [source-manifest.json](source-manifest.json)。来源实际经过 clean show 导出后逐字节校验，不以旧摘要代替原策略或输入。

## 数学对象

- [四人完整策略的末位标量桥接反例](../../../state/反例/四人完整策略的末位标量桥接反例--反例.md)：两份完整四人策略，15与85个历史；有效末位上界和错误的额外标量桥接分别说明。
- [五人五十五客户的顺序静态最低福利分离](../../../state/反例/五人五十五客户的顺序静态最低福利分离--反例.md)：55客户完整SPE福利50、全部静态PNE福利55，连同56客户前身、贪心过程和版本边界。

原件不改写。特别是 original/static_dominance_result.json 虽以 .json 结尾，内容实际是39B纯文本“1000个有限游戏未发现”；不对它执行JSON解析，也不把它当作现存10000循环的完成输出。

## 一次新固定实例核验

[check_global_exchange.py](check_global_exchange.py) 仅依赖Python标准库。它按客户均分定义计算精确有理收益，不导入原模型/求解器，不调用LP、随机探针或贪心最小化。它验证：

1. 两个四人实例与55客户五人实例的完整有序历史策略，合计881个非终局历史、4275个行动比较，包括规定行动自身。
2. 55与56客户两个五人实例各126个终局人数向量、252个集合值倒推状态。每个非PNE保存一个严格偏离，每个状态保存全部可达纯SPE终局结果。
3. 同一55客户目录下2、3、4、6提供者的四个固定参数，以核对原日志。它们不是随机搜索的新样本。

本批成功执行这个入口一次。报告为 [new-global-exchange-exact-check.json](new-global-exchange-exact-check.json)；代码、输出哈希和精确执行范围为 [execution-record.json](execution-record.json)。报告全部逐历史比较及集合值结果保全，摘要不是唯一证据。

在仓库根可复现到一个新的临时输出，避免覆盖保存结果：

    python archives/customer-attraction/tools/evidence/global-exchange-resumed-boss2/check_global_exchange.py \
      --original-dir archives/customer-attraction/tools/evidence/global-exchange-resumed-boss2/original \
      --out workspaces/global-exchange-recheck/result.json

末位两策略对应报告 bridges 字段；五人原完整策略对应 minimized_policy；五人两个固定实例分别对应 minimized_equilibria 与 sparse_equilibria；其他提供者数对应 same_55_customer_instance_other_player_counts。

## 必要边界

全集策略检查不等于只检查实际路径。集合值倒推缓存的是所有可实现终局，不能将其替换为每个人数状态唯一行动而限制历史依赖。原 spe_count=3 是终局结果数量，不是完整SPE策略数。贪心输出没有全局最小性结论，早期未发现日志没有一般证明意义。

已成熟的另一56客户十二型实例及其核验只用于数学比较，未重复执行。这里的55/56数据是另一具体实例。新增结果分别否定两个桥接命题，均不反驳半覆盖，也不解决当前六人原目标。
