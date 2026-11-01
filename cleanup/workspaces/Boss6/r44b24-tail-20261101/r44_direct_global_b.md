# R-44b24 direct_global LP 三源独立实读审查

## 范围与源指纹

本批按冻结清单 `work.py clean show` 导出并逐字节实读三个源；没有修改共享 clone、没有远端写入、没有把读取或运行当作 `done`。

| source ID | 冻结路径 | SHA-256 | 大小 |
|---|---|---|---:|
| `6bf3acc5acb5526210d3` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/direct_global/ordered_early_floor_lp.py` | `1d1e760a6f70e929877852996c88422e833c54196a16f03697c4b522d208f80f` | 1205 B |
| `2d47a57f327bf665147d` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/direct_global/repeated_prefix_lp.py` | `29d5a3fb237e9c903083c33b968c2d66b3c29d7e7baa76cae64861ce9f00c331` | 1108 B |
| `abd449559ab683bdb4e1` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/direct_global/repeated_prefix_sharp_lp.py` | `644aeb05338168ef0b9a0c329fbf6ad6048c8121340c3510f53f01e0edc7adcd` | 783 B |
三个源均有同一冻结路径的 `legacy-cleanup`（68fad804ec5946cb296f77dc5b336308a66abf12）和 `main`（aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c）来源版本。

## 直接实读内容

### `repeated_prefix_lp.py`（2d47…）

程序对每个 `m=2,...,20` 枚举 `a,b∈{0,1}`、比较计数 `d,ell∈{0,...,m}` 和交集计数 `h` 的全部合法范围。对每个客户类型构造 7 个不等式行：

1. `m*uA - d/(p+1) + h/((p+1)(p+2))`；
2. `m*uB - d/(p+a+1)`；
3. `m*uB - ell/(p+a+1)`；
4. `(d*ell-m*h)/((p+1)(p+2))`；
5. `m*uA - ell/(p+2)`；
6. `uA - b/(p+2)`；
7. `m*uB-a`。

目标右端为 `2·1[a+b>0] − 1[d>0]`，用 `scipy.optimize.linprog` 寻找一个全局非负乘子向量。每个 `m` 都打印 `PROOF`；浮点解显示：

- `m=2`：仅第 2 个乘子为 `1`；
- `m≥3`：向量稳定为 `(1,0,1/(2m),1/m,0,0,0)`（打印为浮点近似）。

这是发现原统一 `G` 证书乘子的 LP，不是完整策略树、SPE 构造或客户实例搜索。程序本身没有输出文件、没有 exact Fraction 证书，也没有对所有目录/客户量词作证明。该结构与已归档的“共同倒二主题 half”解析证明相关，但不能以本程序的 `PROOF` 标签替代解析正文。

### `repeated_prefix_sharp_lp.py`（abd449…）

程序复用相同的 7 行，增加第 8 个变量 `t`，把目标改为最小化 `t`；每个 `m=3,...,20` 的输出均为正：

| m | 最小 t（浮点） |
|---:|---:|
|3|1.6666666666666665|
|4|1.7680722891566263|
|5|1.8266666666666669|
|6|1.863544813695871|
|7|1.8884254431699685|
|8|1.9061387900355873|
|9|1.919290626131017|
|10|1.9293877551020409|
|11|1.9373528026377766|
|12|1.9437780698871727|
|13|1.9490591292024249|
|14|1.953469139026726|
|15|1.9572021857923496|
|16|1.960399610790498|
|17|1.9631665750412313|
|18|1.9655828074647435|
|19|1.9677097701626975|
|20|1.9695955510616785|

该 `t` 是这个有限 LP 模板的浮点优化值；脚本没有证明它是一般福利界、锐常数或真实 SPE 的可实现值。README 明确要求“不声明为锐福利界”，现有“倒二菜单条件证书精确审计”也把它定位为发现乘子的入口。没有新数学对象；应作为已有菜单/系数计算资源的保留依赖或重复版本说明。

### `ordered_early_floor_lp.py`（6bf3…）

程序固定原统一 `G`，加入每个早期角色的 `R_j`、`L_j` 真实前缀最坏分母行，仅枚举客户位 `(bits)` 和六个 `(d,ell)` 极端组合。对 `m=3,...,10` 的原 LP 全部 `NO`。其第二个 LP 生成数值 Farkas 型分离，目标值为：

| m | dual.fun |
|---:|---:|
|3|−0.3333333333333333|
|4|−0.6666666666666666|
|5|−1.0|
|6|−1.3100775193798457|
|7|−1.6037934668071652|
|8|−1.8866699950074888|
|9|−2.158848783590395|
|10|−2.4224124751567047|

输出仅保留 LP 数值支持点和小数权重，不保存 exact dual、可验证的有理分离证书或任何真实目录/客户实例。README 将它准确描述为“未冻结的一般模板探索”：这些负点是固定 `G` 加早期 floor 行的松弛模板不可行性信号，不是完整 SPE，也没有数学真值含义，不能当作六人 half 反例。应保留其失败机制（仅增加这些早期保底行且固定 `G` 仍不足），但不要把 `NO` 或负 `dual.fun` 升级为普遍定理。

## 运行核验

在 Python 3.12.14、numpy 2.3.5、scipy 1.17.0 上，用导出的原字节直接执行：

```text
python3 ordered_early_floor_lp.py
python3 repeated_prefix_lp.py
python3 repeated_prefix_sharp_lp.py
```

三个程序均正常退出，未读入外部输入或本地 helper；运行只打印 stdout，不写报告文件。`repeated_prefix_lp.py` 的 `PROOF` 输出和 `repeated_prefix_sharp_lp.py` 的数值序列与源代码定义一致；`ordered_early_floor_lp.py` 的 m=3..10 全部 infeasible，输出与其 LP 构造相符。由于输出是 numpy/scipy 浮点结果，不能直接当精确系数/对偶证书。

## 与现有 canonical 正文的关系

1. `archives/customer-attraction/state/定理/倒二主题共同包含半覆盖--定理.md` 和 `archives/customer-attraction/state/计算/倒二菜单条件证书精确审计--计算.md` 已有自足解析证明及独立 Fraction 审计；本批三个 LP 源只提供发现阶段的乘子/失败诊断，不能替换正文。
2. `archives/customer-attraction/state/计算/末菜单系数模板的发现与缩放证书--计算.md` 已记录另一组固定 G / 缩放 G 的 LP 模板、m=3/4 精确系数与 m≥5 数值失败；当前三个源是 R-44b24 direct_global 的独立入口，应在该计算资源或一个新的“R44b24 direct_global 探索 LP”资源中以 source_refs 和运行范围补记，避免将入口遗漏或重复包装成新定理。
3. `archives/customer-attraction/state/障碍/固定末菜单的非均匀前缀付款边界--障碍.md` 已给固定 G + R/L 行的全 m 解析障碍；`ordered_early_floor_lp.py` 应作为该障碍的有限探索依赖/失败证据，不应产生新的反例对象。
4. `direct_global/README.md` 明确 `repeated_prefix_lp.py` / `repeated_prefix_sharp_lp.py` 只用于发现乘子，`ordered_early_floor_lp.py` 是固定 G 下的未冻结模板探索。现有 canonical 文件尚未在 source_refs 中列这三个 source ID；建议逐源登记为 `retained`，目标统一指向上述计算/障碍资源，并在清洗回执写明 `read/compared` 与“无新增数学对象”的处置理由。

## 建议处置

- `6bf3acc5acb5526210d3`: **retained**，canonical target 为 `archives/customer-attraction/state/障碍/固定末菜单的非均匀前缀付款边界--障碍.md`（有限 LP 失败诊断）及/或补充计算资源；保留 m=3..10 数值输出，不升级为定理。
- `2d47a57f327bf665147d`: **retained**，canonical target 为 `archives/customer-attraction/state/计算/末菜单系数模板的发现与缩放证书--计算.md` 或新增 R44b24 direct_global 探索资源；记录 m=2..20 的数值乘子模式，解析真值由现有 half 正文承担。
- `abd449559ab683bdb4e1`: **retained**，同上；记录 t=1.666…→1.969… 的有限浮点序列仅作探索，明确不是锐界或福利定理。

无需新增 state/定理、state/反例或 state/问题文件；这三源都没有直接构造真实 SPE、完整客户实例、精确有理对偶或新普遍量词。