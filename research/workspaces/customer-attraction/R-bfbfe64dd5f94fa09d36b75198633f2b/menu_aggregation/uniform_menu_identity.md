# SUMmin-full 恰是均匀位置菜单值，且产品精确可加

2026-10-25。**一般解析关系；direct_exchange 已从定义独立核对 (U)、(P1)—(P3)，未发现致命异议。不提供福利付款，不认领新颖性。**

## 1. 同一完整策略和三个不同的域

固定任意原 CAG 实例、人数 m、完整有序历史纯 SPE sigma。实际叶为 z，福利 W。对实际位置 i 与合法主题 A，令 `Z_i(A)` 是固定实际前缀、当前强制 A、以后沿原 sigma 的完整 m 槽终局。定义

    K_i(T,A)=sum_(x in T) 1/[1+c_x(Z_i(A))],
    R_i(p)=min_A sum_T p(T)K_i(T,A).

完整策略在后继的真实反应全部保留。以下极小极大恒等式本身对任意有限这些矩阵成立；不偷偷强化 SPE。

自由位置菜单值是

    Mpath = min_(Q on {(i,A)}) max_T E_Q K_i(T,A)
          = max_p min_i R_i(p).

均匀位置菜单值是

    M_unif = min_(q_1,...,q_m) max_T
                 (1/m) sum_i E_(A~q_i)K_i(T,A),

其中每个 `q_i` 是目录主题分布。这里位置边际必须等于 `1/m`；强制主题的条件分布可以按位置选择。`Mpath<=M_unif`，因为前者极小方可以自由选择位置。

另一个对象是先平均全槽负载再取倒数的均匀凸负载值 gamma+。同系数 Jensen 只给 `gamma+<=M_unif`。它与 `Mpath<=M_unif` 不能合成 gamma+ 和 Mpath 的大小关系。

## 2. 精确恒等式

有

    m M_unif = max_(p in Delta(S)) sum_i R_i(p).       (U)

证明如下。有限双线性极小极大允许交换 p 与元组 `(q_1,...,q_m)`。也可以把极小方视为在全部主题元组 `(A_1,...,A_m)` 上混合；目标只依赖各坐标边际，所以这种表示与独立选择 q_i 完全等价。于是

    m M_unif
      = max_p min_(q_1,...,q_m)
            sum_i sum_(A,T) q_i(A)p(T)K_i(T,A)
      = max_p sum_i min_(q_i)
            sum_(A,T) q_i(A)p(T)K_i(T,A)
      = max_p sum_i min_A sum_T p(T)K_i(T,A).

第二行的分离仅针对极小方的各 q_i；所有 i 仍使用同一个查询 p。目录有限使最大最小均达到，不需要极限或任何平局规则。

因此全称候选

    for every p: sum_i R_i(p)<=W                  (SUMmin-full)

**恰等价**于 `m M_unif<=W`。这个身份比“SUMmin 蕴含 Mpath 桥”更准确，但不是付款。

## 3. Cartesian 产品策略下 M_unif 精确可加

取同一人数 m 的有限组件 `K_1,...,K_s`，客户宇宙互不相交。目录取各组件主题的全部 Cartesian 组合；在每个完整产品历史逐坐标执行组件完整 SPE。任意产品偏离的收益增量等于组件合法偏离增量之和，故这是一份完整产品 SPE。此处只构造这份策略，不声称所有产品 SPE 都分解。

对产品查询分布 p，令其组件边际为 `p_k`。产品强制主题为 `A=(A_1,...,A_s)`。各组件必须共用实际位置 i，但行动坐标可以独立选。逐客户可加和自由元组行动给

    sum_T p(T)K_i^prod(T,A)
         =sum_k sum_(T_k) p_k(T_k)K_i^k(T_k,A_k),
    R_i^prod(p)=sum_k R_i^k(p_k).                  (P1)

任何边际元组 `(p_1,...,p_s)` 都可用独立积查询实现；相关查询没有额外影响。因此由 (U)，

    m M_unif^prod
       =max_(p_1,...,p_s) sum_k sum_i R_i^k(p_k)
       =sum_k max_(p_k) sum_i R_i^k(p_k)
       =m sum_k M_unif^k.                         (P2)

同时 `W_prod=sum_k W_k`，故精确缺陷也可加：

    m M_unif^prod-W_prod
       =sum_k [m M_unif^k-W_k].                   (P3)

所以分别满足 SUMmin 的组件不能经这种产品策略变成 SUMmin 反例；一个产品若严格违反 SUMmin，至少一个组件已严格违反。自由位置值 Mpath 没有 (P2) 这样的精确可加式：那里 `min_i` 与组件求和不能交换，正是既有 PRODUCT-MENU-TIME 义务中的时机耦合。仅各组件分别满足自身 Mpath 桥，不能由这里推出产品 Mpath 桥；若各组件均满足 SUMmin，则产品当然仍经 SUMmin 和 `Mpath<=M_unif` 满足 Mpath 桥。

## 4. 未完成的承重关系

(U)、(P1)—(P3) 不使用激励为查询值付款，因而不能证明 `m M_unif<=W` 或 `m Mpath<=W`。均匀 M_unif 付款比自由 Mpath 付款强，失败也不会自动否定后者或原 half。

当前没有 M_unif 反例，没有把产品闭包当作一般福利证明。唯一用途是准确识别 SUMmin 的优化域，并排除“用时机冲突把逐组件 SUMmin 合成坏产品”的无效方向。

## 来源

- `R-e7c3c9a51d38458aa551eec469e04cf2/global/README.md`：R_i、SUMmin-full 及全槽折扣账。
- `R-d3981c0168644971803a9c3380ed687c/round6_general/convex/terminal_pooled_full_payment.md`：M_unif 定义与 Jensen 的准确位置域。
- `R-4243b113e6fc4c25a197dec299f08049/parent/product_menu_time_obligation.md`：完整产品 SPE、R_i 产品分解和 Mpath 的共用位置耦合。

本页把这些现有对象接成 (U)、(P2)、(P3)，不宣称既有产品机制或有限极小极大的新颖性。
