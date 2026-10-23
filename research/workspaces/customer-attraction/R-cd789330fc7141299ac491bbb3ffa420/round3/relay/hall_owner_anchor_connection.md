# owner 查询与 Hall-B 回流的同叶兼容：零流锚定角色

2026-10-23。一般任意有限共同目录、任意人数、任意完整元组。新增正组件，**未证明 half 或多叶共同支付**。

相关正文为 credible 的 `../credible/owner_hybrid_transport.md`：命题 A/B 的全割容量由 root/shared 独立重构；本页只独立连接其 B 图与本分支的 owner 势/查询信用。零流锚定角色由 relay 提出，credible 在收到陈述和证明后独立重构核对；不称严格盲审。两分支均不更改原策略。

## 1. 固定对象

T 为最优 m 槽元组，O=union T，固定 Q_i subset T_i 分割 O。固定一个合法完整叶 B。x 的 owner 是 o(x)，覆盖数 c_x；E={x in O:x notin B_o(x)}。

Hall-B 使用客户 x in E 的边：

    o(x) -> 每个覆盖者 l，容量1/(c_x+1)，
    o(x) -> t，容量1/(c_x+1)。

每个角色的源为

    b_i^H=sum_(y in B_i outside O) H_(c_y)/c_y。

全部有理、非负。命题 B 保证存在满足 out_i-in_i=b_i^H 的流；可去循环后只含进入 t 的有限路径。这里角色边可以向前或向后，不把流当游戏中的行动序列。

## 2. owner-complete 角色必无外部客户

若 Q_i subset B_i，则 B_i outside O 必为空。

证明：在槽 i 放合法 B_i，其他槽先放 Q_l，全部 O 客户仍被覆盖。若 B_i 还有 O 外客户，将其他 Q_l 扩到合法 T_l 后得到覆盖严格超过 OPT 的合法 m 槽组合，矛盾。等价地，HYB 的单点割给 |B_i outside O|<=|Q_i\B_i|=0。

这一事实只用最优性，适用于任意固定的 owner partition。Q_i 为空也没有漏洞：此时原最优元组有可由其他槽代替的分析库存，存在外部主题就能改进 OPT。

## 3. owner-complete 角色在 Hall-B 中必为零流

若 Q_i subset B_i，则所有 owned 客户均不在 E，所以 i 在 Hall-B 图中没有出角色边，也没有终点边。上一节又给 b_i^H=0。非负流守恒因此强迫

    out_i=0,    in_i=0。

这是任意可行 Hall-B 流的性质，不只是可选择某个特别流。即使图上有未来角色指向 i 的正容量边，它们的使用流量也只能为0。

特别，若当前角色 i 强制查询其配对的 T_i，则 Q_i subset T_i=B_i，它的 owner 势查询信用 e_i 不会被 Hall-B 外部调和回流消费。此处 e_i 可来自它覆盖的其他 owner 客户，但所有对应入边仍为零流。

该结论**不能**照搬到 Hall-A：A 图也使用 owner-present 客户边，owner-complete 节点仍可能有正出边。

## 4. 同叶两种运输的容量不重叠

在当前 owner 查询叶 B_i=T_i 中，对 x in Q_i，当前查询获得1/c_x，其他覆盖者的总份额为(c_x-1)/c_x。这些捕获份额正好是 owner-present 客户的非owner插入信用边。

Hall-B 只用 owner-absent 集 E 的客户容量；Q_i 与 E 不交。因此当前 owned-Q_i 捕获分流和该叶的 outside 调和回流可以在同一叶同时标记，客户容量不重叠。更一般，所有 owner-present 客户的非owner边都与 Hall-B 的 owner-absent 边不交。

这不增加新的福利：只是证明两项已定义的同叶容量没有重复使用。它也不允许把不同叶里出现的同一个实际客户容量各收费一遍。

### 将源降为真实外部利润时的预留预算

H_c>=1（c>0），故 b_i^H>=b_i^G，其中 b_i^G 是该叶 O 外真实利润。对 Hall-B 可行流作源路径分解并删去多余源流，得到只运输 b_i^G 的流。其角色入流只用 owner-absent 客户的 e_i^E 容量，所以

    role-out_i+sink_i=b_i^G+in_i
        <=b_i^G+e_i^E<=u_i(B)-ell_i^Q(B;O)。

因此这一路由预留了该叶 O 上的全部 modified 势边际，另外 owner-present 的 e 也未被消费。若 B 是原实际叶，留下的势边际总和正是 kappa，而不是一份额外的 I 福利。

owner-absent 的已覆盖客户 x 的终点价格1/(c+1)，恰等于该客户所有 coverer 的 modified 边际总和。可将这个终点改接到每个 coverer，容量各1/[c(c+1)]；合并原 e 边1/(c+1)后逐客户得到1/c真实份额边。这一步只描述 owner-absent 客户；要得到完整 Hall-A，还需加入其原本不用的 owner-present e 边。A/B不能当两份独立货币。

## 5. 强制最优前缀时的全深度隔离

固定一次最优槽排列。原 sigma 在任意最优前缀(T_1,...,T_k)后的真实 rollout，所有 j<=k 都满足 Q_j subset B_j=T_j。于是 Hall-B 流完全支撑在角色 k+1,...,m 上，不能回到任何已锚定前缀角色。

此结论保持同一原完整有序历史：没有删掉祖先，没有匿名化历史，也没有要求未来 prescribed 行动避开祖先背景。k=m 时 E 为空且 outside 源为0。

它解决的是一条真实的边界义务：外部调和回流与已锚定查询的信用不冲突，也不穿过已固定的最优前缀。未来角色内部仍可能向较早未来角色运输；离开最优前缀改回原实际前缀时，其他祖先也可能 owner-incomplete。

## 6. 剩余一般承重

目前还没有证明：各真实 rollout 的 Hall-B 流可共同选择，且其 missing-owner 终点价格可以跨叶接入下一条完整 IC，最终仅用一次原实际 I、G 预算。

在本分支 `optimal_exchange_potential_and_query_credit.md` 的 ROLL 中，联合项 sum(e_i^-+D_i)仍未付。锚定零流提供一个严格的未来支撑性质，但它本身不控制该联合项的总大小，也不把形式去槽 profile 变成较小 SPE。继续主攻这一多叶衔接，不能把同叶 max-flow 存在性冒充一般 half 的证明。
