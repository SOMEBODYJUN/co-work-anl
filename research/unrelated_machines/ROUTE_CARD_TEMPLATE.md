> 保留的调度存档入口：当前全仓主攻为Q-CAG-HALF（customer-attraction），见[当前入口](../customer_attraction/README.md)。下文仅用于显式选择unrelated-machines的旧题对话，不是新会话默认任务。

# Route Card 模板：`UM-TARGET-v1`

这是研究存档 `unrelated-machines` 的可选整理模板。探索可以完全不填；当一个想法已经形成较完整候选、准备进入 canonical、跨线合并或升级状态时，再用它整理精确身份和攻击范围。

## 必填字段

```text
ID/version:
route: P0-F 或 R0-R
builder/owner:
blind attacker: （不能是 builder，且先不读证明正文）
integrator:
唯一承重义务 O: 共同容量状态 / 全机整数输出 / sound FAIL / 统一余量 / 位复杂度
候选 Claim 或问题入口:
相比 LST/ST/configuration-LP 新增的信息:
首个可判别输入族:
成功条件:
失败条件与 kill line:
oracle、阈值搜索和位复杂度假设:
本轮交付物:
状态: closes / partial / blocked / salvage / retire
下一动作:
```

## 两条主线的固定合同

### `P0-F`：任意输入共同容量桥

对任意合法 `P,T`，从输入本身产生共同状态 `S(P,T)`。成功必须同时给出：若 `OPT≤T`，具体全机整数分配并满足固定统一余量；若 `OPT>T`，可独立验证的 `FAIL⇒OPT>T` 证书。首轮攻击族固定为两树配置 gap、`{1/2,1}` 唯一 tiny 选择障碍和 shared-sink/block escape。若 `S` 只是逐机 probe、`H+small` 精确 oracle、已知最优支撑或给定 home/sink 分组，就退为局部接口。

### `R0-R`：近二真实整数 gap 与 decoder

固定一个严格小于 `2` 的目标比例，构造真实调度的 YES/NO 族。NO 侧必须同时压低所有中间 quota 层，不能只压最低或最高层；YES 侧必须保持完整整数可行性。还必须给出：任意低于目标比例的真实调度都能在位多项式时间解码为源问题的 YES 解。若中间层逃逸、复制使 NO 变 YES，或低负载调度不能解码，立即登记为障碍并停止扩大参数。

## 成熟候选的可选 Blind attack 顺序

在读取 Builder 的证明前，blind attacker 必须独立提交三项：

1. 最小边界/退化输入；
2. 量词、oracle、`FAIL` 语义和总位复杂度攻击；
3. 现有已知族是否已经击穿该候选。

随后才读证明，标记 `passes / fatal / unresolved`。Integrator 只在两份材料都存在时登记 canonical；否则留在个人工作区或 `questions/`。
