# Aggregate security checkpoint — 2026-10-21

主目标：原CAG，任意共同有限目录、单位客户/提供者、全部历史依赖纯SPE，`2W≥OPT`。本分支没有解决或否定主目标、`W≥m v_m`或`W≥(m−1/2)v_m`。

先读`dr_boundary.md`。新增精确边界是**扩大到一般单调DR边际势后**，真正静态安全值强桥和首两人桥均失败：六主题三人完整SPE，`u=(0,105,56)`、总收益161、安全值56。它明确不是CAG；`verify_dr_boundary.py`是自含标准库精确核验，冻结输出`dr_boundary_exact.json`。独立审查待完成。

最有用的正面接续是孤立CAG的support不变总预算：`|q|Φ(q)=W(supp q)+Σq_aΦ(q−e_a)`。三人的混合重复恒等式`6Φ(2a+b)=Φ(a)−2Φ(b)+8Φ(a+b)`恰是重复动作不改变总收益的势语言。一般DR反例不满足此预算。

`dr_potential_probe.py`为数值诊断工具；所有`*_n*k*.json`及`dr_groups_*.json`均是扩大模型有限计算，除`dr_boundary_exact.json`外不属于精确证书。完整策略锥随机样本未分离不证明一般定理；任意完整随机policy易使可行锥退化，这也是后来加入实际势生成及分组策略的原因。不要把这些无反例样本当正面数学进展。

下一步：从support预算或覆盖矩非负性构造跨真实分支支付；或者寻找合法CAG反例。不要用本扩大模型的161<168宣称原安全值桥失败。没有git提交、没有work.py、没有接触token；root统一checkpoint。
