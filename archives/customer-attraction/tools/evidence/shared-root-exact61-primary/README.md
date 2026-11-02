# Shared-root exact61 原证据与复现

本包保全 `R-ae18a85a07214b22b7b9d614c34779e0/dual` 六源及 `countersearch` 四源，合计55902原字节。manifest 给十件源ID、两份完整冻结出处、SHA/大小、包内路由和两项已归档同SHA依赖；receipts 记录逐件完整实读及独有内容去向。原目录名、同名报告身份和原字节不改。

数学出口为三页：

- [61行历史精确福利定理](../../../state/定理/五人共同最大主题的六十一行有理福利界--定理.md)：完整61项整数表、行定义、完整型域和K抵消。
- [原数学复核](../../../state/审查/共同最大主题六十一行证书的原数学复核--审查.md)：COPY128、二值尾4096/1280、容量5整数/64补集、2048固定系数和完整定价的不同义务。
- [恢复程序及两报告](../../../state/程序/共同最大主题证书恢复与两份定价报告--程序.md)：作者恢复/另写定价/数学评审层级、缺输入的joint程序和历史状态。

## 输入和原事件

精确β约2.017183609421193、61正乘子、K余项0。原作者报告2753生成列、全类型最小0；原separate实现两报告均6144条件、160缓存、43零条件，无负；它们除了seconds完全一致。原数学报告分别记录128/4096/64/2048的完整系数义务。历史报告不提供可恢复的全部原argv、退出码或stdout/stderr，不补造这些字段。本次执行次数在execution-record.json：恢复、定价与原math有限域入口均0次。

两份已归档真实输入按manifest复用而不再永久复制：二值1999精确十三乘子JSON；Ra277的1.8MB完整浮点CG，后者仅用于输入绑定及活跃K列对账。没有把该CG的primal当作SPE或重新证明它的最优性。

## 可复现准备和可选原核验

从结果仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/shared-root-exact61-primary/prepare_replay.py --runtime /tmp/shared-root-exact61-replay
```

准备程序要求新runtime不存在或为空，验证十源及两依赖SHA后逐件复制原字节。只新增一个明确声明、从不被导入的 `customer_attraction/model.py` 注释标记，用于原math审计的根目录查找；它不是数学实现或缺依赖的替身。preparation-record.json 保存完整输入路由、SHA和0科学入口调用。

随后可选择原样运行：

```sh
python3 /tmp/shared-root-exact61-replay/research/workspaces/customer-attraction/R-ae18a85a07214b22b7b9d614c34779e0/dual/separate_shared_root_audit.py
python3 /tmp/shared-root-exact61-replay/research/workspaces/customer-attraction/R-ae18a85a07214b22b7b9d614c34779e0/countersearch/audit_shared_root_math.py
```

前者需要NumPy，后者纯标准库。原报告只会在runtime中被覆盖，本包不改。本准备脚本不补齐两份作者恢复程序的历史模块：shared仍需原Universe/精确消元等真实依赖，joint另缺冻结清单未见的输入/模块，不能借shared结果替代。

只做本次静态/标量核对：

```sh
python3 archives/customer-attraction/tools/evidence/shared-root-exact61-primary/reconcile_sources.py
```

它不导入或执行原核验，不枚举128/4096/6144域，只核字节、完整乘子表、目标/K、两报告字段及依赖输入绑定。reconciliation.json 是这种对账结果，不新增数学独立审稿人。

## 范围

β是历史可行上界，当前五人因子二已证；原OPEN文字仅历史。该61行证书不证明最优常数、匹配primal、SPE反例、外部评审、新颖性或六人结论。程序joint输出未见，保持输入和证据缺口。本次原字节保全、数学转写与成熟证据复用均为Boss3同一身份，Git端点由父方串行。
