# 全阶共同矩整数提取桥的独立核对

审查对象：`UM-FULL-DEGREE-MOMENT-DECODING-v1`，正文 `research/current/unrelated_machines/full_degree_moment_localizer_decoding_bridge.md`。

## 先陈述再重构

给定次数至多 `2n+1` 的有理泛函 `L`，Boolean/one-hot 理想、次数至多 `n` 的平方正性以及每台机器的次数 `n` 负载局部化器正性。对每个合法分配定义完整原子 `m_sigma`。需要核对的结论是：`w_sigma=L(m_sigma)≥0`，权重和为1；若 `w_sigma>0`，每台机器负载不超过T。

## 核对

`m_sigma^2=m_sigma` 只用 Boolean 与同任务冲突恒等式。`sum_sigma m_sigma=prod_j(sum_{e in E_j}x_e)=1` 只用 one-hot 守恒，因此 `sum w_sigma=1`。将 `K_i` 乘以 `m_sigma^2` 后，所有非 `sigma` 端被同任务冲突项消掉，得到 `(T-L_i(sigma))m_sigma`；代入局部化器取 `q=m_sigma` 合法，因为 `deg(q)=n`。故超载原子权重为0，正权原子必为T可行。

## 边界攻击与状态

空任务时唯一原子为1；T=0 时正负载原子被局部化器剔除；零处理时间不产生除法。该证明依赖最高次数 `2n+1` 和完整原子族，不能由次数四矩自动替代。原子总数可以是 `m^n`，所以这不是位多项式解码器，也没有给出从普通P生成L的算法。审查未发现正文量词或理想化简的致命漏洞；状态保留为 stated-scope proof、未外审、主目标开放。
