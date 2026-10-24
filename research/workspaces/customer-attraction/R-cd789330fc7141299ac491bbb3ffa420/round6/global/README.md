# 第六轮：完整续局换位与PB-extra

2026-10-24。已读恢复的round5一般稿及两位置安全值归约。只研究一般Q-CAG-HALF及全输入组件；half、PB-extra、FLOOR均OPEN。旧私有退出正规形只针对FLOOR，不等于half正规形。

[credible_adjacent_transposition.md](credible_adjacent_transposition.md)复用可信全集拼合，给出同终局负载的相邻完整SPE换位条件。固定PB坏点取第一利润最大见证，若α<β，则下一主题B的无祖先承诺子SPE阈值μ_B必>α；否则可重选旁枝交换首对、提高第一利润而保持坏首对总和。固定half坏计数的收益序列字典序最大实现也满足同样相邻上升障碍。mixed收到自足陈述后独立重构通过。

独审见 `../mixed/adjacent_swap_review.md`。root另在读稿后逐式独立重构通过（非盲审），包括阈值、BA条件、ancestor整组真实query保持及LAST-DIP的严格范围；审查通过不升级福利结论。mixed的最后利润静态界还给直接half坏点定位：τ=2W/(2m−1)，最后一个u_i<τ后必有u_(i+1)≥τ，且对应μ_child>u_i；不能无证升为μ_child≥τ。正文已记录这个全人数必要结构及同终局负载子树替换对全部严格ancestor IC的保持性。

剩余义务是利用最小坏点全部proper历史的配对信用，支付或排除这些μ_B>α障碍。尚无新的普遍付款界，不将阈值改名或有限样本当half证明。无git、无覆盖round5、无固定人数专项或新增扫描。
