# 循环查询与补位核边界的精确证据

对应正式对象：

- [循环污染查询的加权调和付款](../../../state/引理/循环污染查询的加权调和付款--引理.md)
- [同主题在途查询的补位核预算](../../../state/障碍/同主题在途查询的补位核预算--障碍.md)
- [完整策略核验](../../../state/计算/循环查询与补位核的完整策略核验--计算.md)

`original/`为六份冻结原件。`dependencies/`为基础实例/证书及四个规范模块的逐字节依赖副本，来源、两个完整冻结commit、ID、SHA与已有原件复制路径在[source-manifest.json](source-manifest.json)。不将依赖复制当成这些已清洗源的新完成记录。

[reproduce.py](reproduce.py)在临时旧深度布局运行两个原Python各一次，源码字节不改；生成报告与原2510/796983字节JSON分别逐字节相同。完整stdout、空stderr、报告及运行元数据在`replay/`。不得直接在`original/`运行会覆盖同名JSON的原主入口。

[audit_full_data.py](audit_full_data.py)只用标准库，完整读取JSON的全部结构/数据，不导入原审计或求解器。它独立重建四成员的全部5130个有序历史、40536项含自身IC、全部字段和28条负载见证，枚举2/6/24/120种匹配，并核每类比较客户的跨主题末节点逃逸。新报告为[replay/independent-full-data.json](replay/independent-full-data.json)。

从仓库根复现：

```sh
python3 archives/customer-attraction/tools/evidence/cyclic-padding-boundary/reproduce.py
python3 archives/customer-attraction/tools/evidence/cyclic-padding-boundary/audit_full_data.py
```

两个入口均拒绝关闭断言。原大JSON只有m=2,3,4,5；全m构造由正式数学证明承担。本例为受限付款接口边界，且允许跨主题节点复用后有明确逃逸，不是一般HALF反例或一般可支付路由存在性证明。
