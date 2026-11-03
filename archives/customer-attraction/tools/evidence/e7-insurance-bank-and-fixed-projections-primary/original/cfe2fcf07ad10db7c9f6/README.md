# 一般全槽路径预算：未闭合候选与定向检错

2026-10-25，`global_proof` 子研究员给 root 的准确交接。**Q-CAG-HALF 仍 OPEN。本文没有完成一般证明，没有新增无条件福利常数，也没有目标反例。** 仅在本人获分配目录保存草稿及候选检错，不修改 canonical 账本。

## 1. 对象与已排除的误用

对象严格为原 CAG：有限单位客户、有限非空共同目录、任意人数、完整有序历史依赖纯 SPE，重复、空主题及任意离轨平局全保留。固定同一份完整策略 sigma，实际路径 z=(S_1,...,S_m)，实际收益 u_i，总福利 W=sum_i u_i。

在实际前缀 h_i=(S_1,...,S_(i-1)) 强制当前 A 后，沿**原 sigma 的真实后继**得到完整 m 槽终局 Z_i(A)。后继不冻结。以下 K_i 为一个独立额外查询的收益：

    K_i(T,A)=sum_(x in T) 1/[1+c_x(Z_i(A))].

每列是合法 m 主题静态背景。root 已通知：全局零根逐人 extra 安全值及更弱逐人 OPT/(2m) floor 已被完整保险反族否定。因此不把旧 `general_half_proof.md` §8 的个体 Mfull 标签当现行开放状态；本文只考虑聚合预算。

## 2. 准确候选 SUMmin-full（未证）

对任意固定合法主题分布 p，定义

    R_i(p)=min_A sum_T p_T K_i(T,A).

候选为对全部原输入、全部完整 SPE 及全部 p 有

    SUMmin-full:   sum_i R_i(p) <= W.

这是**未证明的全范围候选**，允许个别 R_i(p)>u_i。纯 p=delta_T 时，选 A=T 给

    R_i(delta_T) <= K_i(T,T) <= u_i(Z_i(T)) <= u_i,

所以纯查询逐人可付。但 min 与 p 的期望不能互换，纯点验证不证明混合 p。

准确充分性有两种写法。

1. 记 Mpath=max_p min_(i,A) sum_T p_T K_i(T,A)。若 SUMmin-full 成立，则对每个 p，min_i R_i(p)<=W/m，故 Mpath<=W/m。每列合法给 Mpath>=v_(m+1)(0)，共同目录静态预算给 OPT_m<=2m v_(m+1)(0)，于是 half。
2. 取真正 m 槽静态安全游戏的最优查询 p*。每个 R_i(p*)>=v_(m+1)(0)，故 SUMmin-full 同样足够。

这不是把候选的充分推论当成证明。一般半覆盖目前卡在 SUMmin-full 自身。

按主人要求把同一一般机制直接代入 m=5：若 SUMmin-full 成立，则 Mpath<=W/5，进而 OPT_5<=10 v_6(0)<=2W。此处是**依赖未证付款的条件结论**，不是一般五人 half 已证；本分支没有生产五人专用加行或调系数，也没有新的无条件五人常数。

## 3. 更强平均候选与精确全槽折扣账

还可取强制 A 与查询 T 独立同分布 p，定义

    C_i^full(p)=E_(A,T) K_i(T,A).

由于 R_i(p)<=C_i^full(p)，更强的 `sum_i C_i^full(p)<=W` 足够。这里没有证明它。

为准确接到已有 m-1 槽去相关账，令 B_i(A) 为 Z_i(A) 删去当前行动 A 后的竞争元组，n_x(A)=c_x(B_i(A))，q_x=Pr_(T~p)(x in T)。定义

    D_i=E_A sum_(x in A) 1/[1+n_x(A)],
    C_i^old=E_(A,T) sum_(x in T) 1/[1+n_x(A)],
    e_i=u_i-D_i >= 0,   kappa_i=D_i-C_i^old.

逐客户精确相减得到非负折扣

    L_i=E_(A,T) sum_(x in A intersection T)
                         1/[c_x(Z_i(A))*(c_x(Z_i(A))+1)] >= 0,
    C_i^full = C_i^old - L_i,
    W-sum_i C_i^full = sum_i e_i + sum_i kappa_i + sum_i L_i.

最后两式是恒等式，不是新的付款定理。客户出现在 A 时 c_Z>=1，故无零分母。本文独立推导了同一折扣式，随后 root 发来同式核对；**来源合并，不认领重复的新机制**。旧全 p、m-1 槽预算的反例不能直接否定 full 槽候选；反过来，L_i>=0 也不能自动支付已经可能为负的 sum(e_i+kappa_i)。L_i 的客户份额在不同真实枝上计算，不能当作同一实际客户可反复提取的余额。

尝试继续去相关时，仍出现已知的删除中间动作返还差；后继合法 IC 给非负项，但此返还差无固定符号。本文没有证明全路径返还可由 sum L_i、实际客户池或其他共同预算支付。因此**额外槽没有在本文产生新的无条件一般金额**。这正是交接断点。

## 4. 两个脚本实际检验什么

`probe_uniform_path_menu.py` 读取五份已存完整策略及原客户重数，对精确有理 K_i 建立有限 LP，数值最大化 `sum_i R_i(p)`。LP 变量为 p 及各 R_i，约束为全部强制 A 的上界。随后把返回的 p 近似为分母最多 10^7 的有理分布、重新归一，并用 Fraction **精确重算该一个 p 的 R_i**。

这区分两种证据：LP 全 p 最优值是 HiGHS 浮点输出；有理 p 的重算只证明该 p 的数值，不认证 LP 的全 p 最优性。没有保存有理对偶证书，所以不得把浮点负最优写成精确全 p 不等式。

五个原权重实例的有理重算结果为：

| 来源游戏 | W | 返回有理 p 的 sum R_i-W |
| --- | ---: | ---: |
| root_tax_failure | 38 | -790691/145597 |
| global_decorrelation_failure | 85 | -7978583/375060 |
| aggregate_theta_failure / onpath_budget_failure | 34 | -473/48 |
| individual_security_failure | 32 | -1203/136 |
| local_security_increment | 105 | -145669/5041 |

`probe_uniform_path_cone.py` 则固定这些完整策略，在全部非空主题兴趣类型上允许重数变化，施加全部真实 SPE 比较行以及 W=1。对一份**固定 p**，最大化 SUMmin-full 左侧是一个线性规划；测试的有限 p 列表仅含 uniform、证书自带安全最优 p（若有）、以及全部两点等权 p。它还测试更强的平均 full 槽预算。全部系数先以 Fraction 构造再转 float 交给 HiGHS；输出权重及最优值均为浮点，**没有精确认证锥最优值，也没有遍历全部 p**。

这五种固定策略/有限查询列表未返回 SUMmin-full 或平均 full 预算的阳性。无阳性只是定向检错，不是一般证据。脚本不重新证明源完整策略的全历史认证；原证书身份从源正文读取。

脚本中最后附带测试过更强的固定 A、T 列界 `sum_i K_i(T,A)<=W`，出现一个浮点阳性。它比 SUMmin-full 远强，root 指示不继续精确编译、不另立 Claim；此交接**不使用该捷径**，也不把浮点阳性当作已证反例。没有为此扩张搜索。

## 5. 冻结输出、来源与下一步

`finite_tests.json` 保存两脚本的完整有限输出、实际读取的源文件 SHA-256 及 Python / NumPy / SciPy 版本。原权重输出同时保留浮点 LP 最优值与有理 p 的精确重算值。锥输出均按浮点材料标记。脚本及输入证书的 SHA 也在其中，便于确切重放。

重放命令（从仓库根）为：

    python3 research/workspaces/customer-attraction/R-e7c3c9a51d38458aa551eec469e04cf2/global/probe_uniform_path_menu.py
    python3 research/workspaces/customer-attraction/R-e7c3c9a51d38458aa551eec469e04cf2/global/probe_uniform_path_cone.py

当前最诚实的后续义务：直接证明 SUMmin-full，或为更强平均 full 预算建立对全部真实枝有效的共同付款。若只能再次得到上面的有符号返还，则没有跨过已有断点。本文停在这里，不扩大阴性检索，不将未闭合接口包装为一般证明推进。
