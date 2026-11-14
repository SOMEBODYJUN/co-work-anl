# R105 source-refresh repair review

## 变更定位

上一任务 `boss5-r105-threshold-3b-3b-4ca52e241f3fd837` 的完整后继门槛比较已逐行核对：旧 edge、旧 comparison、旧 reading-ledger 以及旧 receipt 均已实读。当前登记的障碍对象 `customer-attraction/closeout-bf614929b6e50c3900f6fc7e` 从旧 pin `a2e56f7de6c33bfd4b839880b85d9fe3e0961e194549525a17f8ffce4d803211` 更新为 `81bf2dd8f2c1edf1541252c8e8f9f84581d1992bbc7386320c62889c07166b78`；其正文仅有一处数学字面勘误：在根偏离到 `T` 的末位行，选择 `A` 的收益由 `f/2` 改为 `f`。当前正文 SHA-256 为 `6edfe368bfa3f3a0cb795fe14b3cc1345b48856bb13faa87b4c2a6631fa2545f`，旧字节为 `40dfab06dd1bdbe7d1c9acf6bd862dc5a626429d817d0ab493bce890f32fb7be`。

资源端点 `customer-attraction/closeout-67a92b6751929baa34cc1de3` 未变，SHA-256 为 `9d8ab71d9a269651754ed48114eb9803e65a90bc8eb7946f8c8fcf1a0b4250a7`。原负面分析 `switch_reachability_negative.md` 未变，SHA-256 为 `ae96d67cff50959a1daf40b3708c27562f5136be2976b70a9920622df5b89b78`。

## 数学复核

四块同一共同目录仍取两两不交的 `(F,P,H,Q)`，大小 `(f,p,h,q)`，满足 `f,p>0`、`h≥0`、`q=f+2p`；主题为 `A=F`、`B=F∪P∪H`、`T=H∪Q`，强制历史继续计入最终均分分母。

* 删除第一步后的两人子局：强制根 `A,B,T` 的末位最佳响应仍唯一为 `T,T,B`，完整终局仍恰为 `AT,BT,TB`。根最低可信收益分别为 `f`, `f+p+h/2`, `q+h/2`，故父门槛 `Θ=q+h/2`。虚拟 `BT` 的根收益与门槛差恰为 `p`；真实完整两人 SPE 的实际路径仍唯一为 `TB`。`BT` 与 `TB` 都覆盖整个目录并集，因此这条比较不支付福利缺口。
* 当前源勘误位于根 `T` 行的末位 `A` 列。修正后该列为 `f`，而 `B` 列为 `b=f+p+h/2`，`T` 列为 `t/2=(q+h)/2`；`b>f`（因 `p+h/2>0`）且 `b>t/2`（因 `f>0`），所以末位的唯一最佳响应仍是 `B`。旧 comparison 的两人表已经写成修正后的 `A=f`，因此门槛、唯一 `TB` 终局和缺口 `p` 不变。
* 原三人控制者强制改选 `T`：完整可信后继仍恰为 `TBT`。末位行 `TA,TB,TT` 的最佳响应分别为 `{B,T}`, `T`, `B`；第二人在每一离轨分支都严格选 `B`，故控制者收益精确为 `q/2+h/3`。相对拟议 `ABT` 的 `f/2` 严格增加 `p+h/3>0`。此处使用的 `A` 上界至多 `f` 与当前勘误一致，且严格差不变。
* 量词保持精确：门槛结论只对这四块、三主题、无前缀负载的共同目录实例成立；“任一可信完整后继”的严格偏离仍只针对源中给定 R105 切换族。不能把三主题唯一终局外推到更广目录，也不能把此边当作沿任意全局 SPE 的跨枝共同付款或一般 `OPT−W`/half 证明。

上一任务复核中已有的完整 `R_h,L_h,Θ_h` 递推、选中枝与两人根/三人强制子局边界继续有效；本 repair 没有重新运行旧枚举或求解器，有限 80 个整数参数检查按原任务的已验证结果复用。

## 交付判断

数学关系保留，但旧 edge 的 endpoint pin 和障碍证据 SHA 已过时，不能直接绑定当前登记。新 successor edge 复制同一 `checks/context` 关系，更新当前对象 pin、当前源 SHA，并把本 review 与更新后的旧 comparison/reading-ledger 纳入证据。旧 edge 作为历史资产逐项标为 `replaced`；旧 comparison 与旧 ledger 原路径保留并追加本 repair 的处置与当前 source pin。
