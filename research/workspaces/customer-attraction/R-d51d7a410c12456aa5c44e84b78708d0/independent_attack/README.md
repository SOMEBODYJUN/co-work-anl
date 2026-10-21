# 第六研究员：独立攻击与可接续资产

目标仍为一般 `Q-CAG-HALF`，OPEN；固定有限单位客户、共同目录、任意完整历史纯 SPE。仅本目录有写入；不登记共享结论，不提交。

## 已保存阶段资产

- [全局外部残余桥的二人反例族](residual_cover_family.md)：新加强桥 $R_m(C)\le W$ 为假，固定两人、任意整数 $q\ge2$ 的完整 SPE，$W=4q+5$ 而 $R_2(C)=\operatorname{OPT}_2=4q+6$。自足候选，待独立审查；不是主猜想反例。
- [生成器与本人精确展开审计](residual_cover_family.py)：已运行 $q=2,\ldots,12$；[精确报告](residual_family_audit.json)、[27客户实例](residual_family_q2_instance.json)、[完整策略](residual_family_q2_strategy.json)。
- [LP发现程序](lp_residual_two.py)、[初始浮点解](residual_two_lp_witness.json)与[随机全续局筛选](search_residual.py)：过程材料，不作一般正面论据。

## 独立文献条件核对

Brethouwer 2018 硕士论文，University of Twente 官方原文：
https://essay.utwente.nl/76986/1/Brethouwer_MA_EEMCS.pdf 。
§7 的 payoff guarantee 要求 shared misery；其 SPE→PNE 定理限于 symmetric singleton。一般 CAG 不满足前者：先选 $A=\{a,b\}$，后选 $B=\{a,c,d\}$，先者被降至 $3/2$，后者收益 $5/2$。因此不能迁移保底定理来解决一般目录。本结论只是条件核对，无普遍上界导入。

## 下一步

绕开被击穿的外部残余总支付。寻找真实策略分支之间允许交叉支付的新不变量；特别需要保留最优覆盖中落在实际覆盖内的那部分贡献，而不是把整个实际覆盖都花在纯外部残余上。
