# 七份静态CCE发现快照与整数证书

`original/`是七次正常`python3 work.py clean show ID`取得的冻结全文。逐份size、SHA-256、blob、双冻结来源和命令记录见[source-manifest.json](source-manifest.json)；空的`acquisition/*.stderr`保留实际无报错状态。全仓按七个源大小预筛再核SHA，未找到任务开始前可复用的同哈希原件。

四十二客户已有完整原核验输出`../eight-and-forty-two-client-cce-exact-primary/rerun/forty-two-replay.json`恰等于本批`cce_exact.json`加一个末换行；这里复用它，不重跑原验证器、不另存一份同数学完整42客户报告。另位内部只读比较代理确实复跑过该已有包的`replay_bundle.py`并通过，这不冒算本目录新实现或新外审。

正式正文为[静态CCE分离搜索快照与四十二客户证书--计算.md](../../../state/计算/静态CCE分离搜索快照与四十二客户证书--计算.md)。本目录的新[audit_snapshots.py](audit_snapshots.py)直接从全部七快照读入数据，只用标准库Fraction，从真实有序历史重构全部激励，逐个有序静态终局计算偏离总收益，并与逐客户逆负载恒等式、无序压缩交叉相等。

```sh
python3 archives/customer-attraction/tools/evidence/security-cce-seven-snapshots-primary/audit_snapshots.py
```

[verification.json](verification.json)保存新内部审计的全部四浮点点和八客户旧乘子行；42客户仅保存新比较结论，逐21/20行和13个顶层字段必须与冻结`cce_exact.json`完全相等才通过。

- 四十二客户：完整纯SPE W32、OPT42；所有CCE福利≥33。固定对偶未给达到分布，不认证33为锐最小值。
- 八客户早期整数点：完整纯SPE W6、OPT8；沿旧有理乘子给所有CCE≥85/14；最终544/87另在已有正式反例。
- 两个正gap浮点点：按存储十进制作为精确有理输入分别有2、7个负SPE余量，仍是发现候选，未作有理修复。
- 两个零gap点：重复覆盖标签的软件实例，可精确认证W=C为4/5、3/4；不代表穷尽搜索，不改变数学集合目录。

本包原发现程序/验证器导入、调用、随机搜索和LP调用均为0。发现器全源码已实读且复用另一批的`../security-cce-search-program-primary/original/search_cce.py`，本包不复制。当前新独立实现不是外部审查；未认证规模最小性、新颖性、弱CCE桥、安全聚合或六人half。
