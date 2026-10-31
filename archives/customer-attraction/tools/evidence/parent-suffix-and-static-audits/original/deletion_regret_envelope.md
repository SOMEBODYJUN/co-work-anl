# 删除固定背景后的真实续局激励误差包络

2026-10-24。个人一般证明组件；身份 `B16-DELETION-REGRET-ENVELOPE-v1`。
作者解析推导完成，盲独立重构通过。没有外审或新颖性认证。
**Q-CAG-HALF 仍 OPEN；本文不证明删除后仍为 SPE，也不证明一般福利界。**

## 精确合同

有限单位客户集 N、有限非空共同目录 S、任意 n>=1 位单位尾部玩家。
固定非负整数客户背景 b,d；原背景为 b+d，删除背景为 b。
当这些向量来自固定过去玩家时，删除 d 的含义就是移除指定过去玩家的负载；
证明本身只使用背景的非负整数性，不需要为每个坐标单独创造合法行动。
固定原背景 b+d 下的一份全部有序历史纯 SPE sigma；其实际尾元组为
q=(S_1,...,S_n)，负载 c_x，尾位置 j 前的实际尾负载为 p_j(x)。

在删除背景 b 下保留**同一份全部有序历史策略** sigma。只将它作为策略，
不假设其仍理性。对每个实际尾节点 j，令 q_j(T) 是保留该实际前缀、强制
当前选合法主题 T、以后仍沿 sigma 的完整真实尾元组。定义该节点删除后的
最大单步正 regret

    R_j = max(0, max_(T in S) [u_j^b(q_j(T))-u_j^b(q)]).

规定动作 S_j 也是可选偏离，故内层最大值本身已非负。这里 q_j(T) 的后继
全部可以改变，且每个有序离轨历史使用原 sigma 的原规定。

定义真正目录上的前缀误差包络

    K_j = max_(T in S) sum_(x in T)
          d_x / [(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)],

以及同一实际终局中全部尾玩家的共同删除返还

    E_d(q) = sum_(x:c_x>0)
             d_x c_x / [(b_x+c_x)(b_x+d_x+c_x)].

所有被使用的分母严格为正；d_x=0 的项为零。结论是

    R_j <= K_j-delta_j(q),
    sum_j R_j <= sum_j K_j-E_d(q),                         (DR)

其中

    delta_j(q) = sum_(x in S_j)
                 d_x / [(b_x+c_x)(b_x+d_x+c_x)].

右端逐位置非负。重复主题、空主题、零客户、全部历史依赖平局均保留。

## 作者的一般证明

对任意完整尾元组 z 和其中第 j 位玩家，逐客户相减得

    u_j^b(z)-u_j^(b+d)(z)=delta_j(z)>=0.                  (1)

该客户被当前玩家覆盖，故 z 的对应总尾负载至少一，不出现零分母。
原背景完整 SPE 在实际节点给真正比较

    u_j^(b+d)(q_j(T))-u_j^(b+d)(q)<=0.                   (2)

将 (1) 分别用于规定叶与真实强制叶，代入 (2)，得

    u_j^b(q_j(T))-u_j^b(q)<=delta_j(q_j(T))-delta_j(q).   (3)

对 x in T，强制叶尾负载至少 p_j(x)+1。函数
d/[(b+s)(b+d+s)] 对 s>=1 非增。因此

    delta_j(q_j(T))
      <= sum_(x in T) d_x/
         [(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)] <=K_j.       (4)

实际叶同样可用 (4)，所以 delta_j(q)<=K_j。由 (3) 对 T 取最大，
正部不改变上界，得到 (DR) 的逐位置式。

最后同一实际叶按客户合账：每名覆盖 x 的尾玩家贡献同一个
d_x/[(b_x+c_x)(b_x+d_x+c_x)]，共有 c_x 名，故

    sum_j delta_j(q)=E_d(q).                             (5)

把逐位置式求和即得总式。没有把互斥强制叶的返还当成同一实际返还池。

## 真正改善和没有完成的连接

原单插入主题 A 的情形为 d=1_A。本轮 harmonic_menu 分支先得到对应的
真实目录 max_T 版本，并另给全 A 求和的粗化。本文将 d=1_A 推广到任意
非负整数删除背景，允许删除多个固定过去玩家；真实目录 max_T 在前驱中已存在，
不将它认领为本页新增机制。证明只用真实原 IC 与逐客户单调性，不用有限计算。
固定终局的插入/返还守恒是旧机制，不认领为新；本合同的状态仅是
对删除后实际节点 regret 的可复用一般上界。

这条上界没有给 sum K_j 的人数无关付款。harmonic_menu 的解析反族在
每个 n 上有 K_j=1/2、delta_j(q)=0、E_d(q)=0，恰给 sum R_j=n/2，
而被删玩家在原叶收益为1。所以不能把 (DR) 再改写成常数倍原叶利润，
也不能免费把删除后的策略称为 SPE。一般 half 仍缺跨互斥叶的共同容量。

## 来源与后续核验

- 本轮前驱推导：[单插入池与真实误差](../harmonic_menu/insertion_pool_and_dynamic_regret.md)。
- 既有固定终局及旧玩家返还账本：
  [全深度账本](../../R-2e5a6ea95aff4f4c89f75237a74ba472/relay_credit/full_depth_ledger_and_harmonic_obstruction.md)。
- [盲独立重构](../independent_general/background_deletion_blind.md)仅收到上述合同，
  未读本证明或 harmonic_menu 原稿；重新推得逐位置界和总界，并给精确非负余项。
- [独立核验代码](../independent_general/audit_background_deletion_blind.py)自行构造原背景
  全历史 SPE，不导入仓库求解器；[冻结结果](../independent_general/background_deletion_blind_audit.json)
  包含65例/469节点/1676个原IC比较。有限核验不承担上述一般证明。

下一步只有在能从真实后继 IC 进一步控制 sum K_j 或用可证明的权重消去
多叶误差时，才可把本组件接入一般归纳。恒等式、目录 max 和误差记账本身
均不能算作 Q-CAG-HALF 的闭合。
