# 实际前缀关联预算：父方解析复核

2026-10-24。对 [提出者正文](../credible_attack/root_reachability_incidence_budget.md)
读稿后的独立数学核对，不称盲审。主目标仍 OPEN，无外审/新颖性认证。

1. 若没有 D-singleton，任意 x∈D 的 b_x 次覆盖各消耗至少 a 个 R-incidences，
   因而 b_x<=I/a。B>I/a 保证至少一个 D-singleton，且 B>0。
2. 取最后一个 D-singleton 的原实际角色。其后留在指定前缀中的每个动作贡献
   至少 alpha 个 R-incidences，所以个数 L<=floor(I/alpha)。被检查玩家的规定
   payoff<=1/B；这仅使用其 singleton 主题与目标前缀中该客户的负载。
3. 改为正文的合法 T，不论真正后继如何，每个所选 R 客户的终局分母至多
   beta+L+r+1。qB>beta+floor(I/alpha)+r+1 严格保证盈利。没有冻结后继。
4. source round5 PB 目录只有 regular topics 与真实/虚拟 singleton。每个触 D
   的 regular topic 在 d=20 个 segment 各含一个12客户的真实块，故 a=q=240；
   非 D-singleton 的真实 singleton 说明 alpha=1 合法。
5. 逐整数重算：I=20*2063*(12*10^9+1)=495120000041260，
   beta=1000000001，B=10^14，r=2475；
   240B=24000000000000000>I，且
   beta+I+r+1=495121000043737<240B。两条所需严格不等式都成立。

结论限定为原 PB **同一目录、同一背景负载、同一剩余人数**的任意有序实现；
没有反驳任意背景 child 的 SPE，或排除加入其它主题/激励后的新构造。
这是一条一般关联预算 lemma 的明确应用，不能据此声称任意合法背景都能被同一
阈值排除，也未证明一般 half。作者 proof 无已发现致命异议。
