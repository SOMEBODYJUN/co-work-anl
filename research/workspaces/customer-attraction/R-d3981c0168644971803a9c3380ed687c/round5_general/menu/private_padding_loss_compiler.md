# 线性私有填充：fresh 损失游戏与 ADM 的精确条件

2026-10-24。一个解析表示/构造组件，未独立审查、无外审或新颖性认证。没有给出满足最终正分离条件的实例；不是 ADM 或 Q-CAG-HALF 反例。原目标仍 OPEN。

## 1. 任意共享客户输入及填充

取任意有限 q 主题标签、任意人数 1<=m<=q。对每个大小至少二的标签兴趣集 B，给非负整数 r_B，代表 r_B 个不同单位 shared 客户。定义主题 shared 度数

    d_A=sum_(B contains A) r_B,   D=max_A d_A.

取整数 K>2D。为每个主题 A 加 K-d_A 个只喜欢 A 的不同单位客户。所有客户/玩家仍单位，共同目录的每个主题单独大小精确为 K；每主题的正私有块还保证经济覆盖两两不同。

记全客户类型为 H（shared B 加 singleton {A}）；重数 w_H。终局客户负载为 c_H(y)=sum_(A in H)c_A(y)。对任何已选主题 A，无论是否重复，恒有

    u_A(y)=K-ell_A(y),
    ell_A(y)=sum_(H contains A)w_H[1-1/c_H(y)].        (LOSS)

## 2. 全有序历史的 fresh 支配

**结论。** 每份完整纯 SPE 在每个有序历史都规定一个尚未选过的主题（fresh）。这里包括已经含有重复的离轨历史。

证明对剩余人数向后归纳。任一长度 t<m 的历史至多使用 t 个标签，q>=m 保证至少一个 fresh 标签。最后一位若选旧标签，主题中每个客户最终都至少由两人覆盖，收益<=K/2。选 fresh 标签时，其私有客户不被任何他人覆盖，收益至少 K-d_A>=K-D>K/2，故严格优于所有旧标签。

归纳假设规定所有更后玩家在其每个历史都选 fresh。当前玩家若选 fresh A，则之后没有人复制 A，其私有块仍全归自己，收益>=K-D。若当前选旧主题，其收益仍<=K/2。故在任意完整 SPE 子局，所有旧动作严格劣于每个 fresh 动作。归纳完成。

上述 fresh 收益保底依赖理性后继归纳，不能声称它对任意非理性的复制后继也成立。

## 3. 完整损失游戏的准确对应

在每个有序历史 h（允许 h 自身含重复）只允许当前选择 fresh 标签。未来也执行此限制。当前/未来玩家所选主题 A 的 singleton 私有块最终只由自己覆盖，故其 LOSS 中私有项为零，其收益为

    K - sum_(B contains A)r_B[1-1/c_B(y)].            (FRESH)

因此可定义一个有限 perfect-information 损失游戏：在每个 h 只选 fresh，最小化 FRESH 中 shared 拥挤损失；背景 h 的重复仍按真实计数保留。有限逆向归纳提供全部有序历史纯 SPE。

任何这种限制损失游戏的完整纯 SPE，按相同动作表用于填充 CAG，即是完整 CAG SPE。fresh 偏离由损失游戏 IC 支持；旧标签偏离收益<=K/2，而 prescribed fresh 收益>=K-D，严格不利。反过来，§2 表明每份完整 CAG SPE 都属于这个 fresh 策略类，其 fresh IC 与损失游戏完全相同。这是完整策略的对应，不只是一条无重复路径的验证。

## 4. 福利及额外查询的精确损失账

任意根 SPE 的实际叶 z 全部 m 标签互异。令

    L(z)=sum_B r_B(c_B(z)-1)_+.

把每个 shared 客户的重复使用损失加总，得到

    W(z)=mK-L(z),  ell_i(z)<=D,
    u_i(z)>=K-D,  OPT_m<=mK.                         (W)

特别地 K>2D 给 2W(z)>mK>=OPT_m，所有 m 同时满足 half。此填充只能用作辅助 ADM 桥的攻击表示，不能生成原 half 反例。

取任意目录查询分布 p，写 t_H=sum_(A in H)p_A。对任意终局 y（含重复也成立），定义查询损失

    Lambda_p(y)=sum_H w_H t_H c_H(y)/(1+c_H(y)).

因为每个主题单独大小 K，有

    G_p(y)=K-Lambda_p(y).                            (QUERY)

具体分解为

    Lambda_p(y)
      =sum_B r_B t_B c_B(y)/(1+c_B(y))
       +sum_A p_A(K-d_A)c_A(y)/(1+c_A(y)).            (PRIVATE)

当 y 全 distinct，第二项为 (1/2)sum_(A used in y)p_A(K-d_A)。对于实际 h_k 强制一次重复动作后、跟随完整理性尾得到的端点，恰有一个标签可重复至二，其私有项系数为 2/3，其余所用标签为 1/2；不能用 distinct 公式漏掉它。

## 5. ADM 条件及全部强制重复列

固定任意原完整根 SPE 的实际 z，原利润 u_i=K-ell_i(z)。对实际 h_i 强制主题 A 后跟任意完整尾 SPE，admissible cap 等价于

    ell_A(y)>=ell_i(z).                              (CAP-LOSS)

若强制的是实际前缀已经用过的主题，则该玩家收益<=K/2<K-D<=u_i，故每个这样的完整尾 SPE 端点都 cap 合法。这些强制 repeat 列必须全部留在 D。其后所有理性玩家依 §2 继续 fresh。

对当前完整 D，固定 p 的 ADM 正分离精确等价于

    max_(y in D) Lambda_p(y) < L(z)/m.               (SEP)

因为 min_D G_p=K-max_D Lambda_p，而 W(z)/m=K-L(z)/m。要反驳 ADM，需要给一个具体 shared 客户输入及完整损失游戏 SPE，使某 p 满足 SEP；本轮没有这样的 witness。

私人查询惩罚在所有一次强制后的理性端点上有一个粗界：若 p_max=max_A p_A，则

    private term <= (K/2) p_max sum_A c_A(y)
                  =Km p_max/2,

因为 c/(1+c)<=c/2 对整数 c>=1 成立。故稀释 p 可能减少私有填充对查询的惩罚，但增加标签会加入全部 IC 和全部 D 端点，不能免费加一批无 shared 客户的新标签；这些零损失动作会改变原实际损失游戏。

## 6. 一般机制与 m=5 压力

本组件适用于任意 q>=m、任意 shared 超图，没有固定主题数或固定人数项目，也没有枚举/扫描。它绕开旧全兴趣类型均匀偏置的指数成本，但只适用于 shared 客户非负、负的单独规模差可以由 singleton 填充吸收的构造；没有声称能编译任意 signed 势函数。

代入 m=5，W>=5(K-D)>5K/2>=OPT_5/2，无条件成立；同一全 m 机制已自动过 half。ADM 仍需 max_D Lambda_p<L(z)/5，未给输入满足它。因此不能把这个自动 half 当成原一般证明进展，也不能把 SEP 条件当成已经构造出的辅助反例。
