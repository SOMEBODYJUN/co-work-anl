# 末回复运输的删人表示与共同早期乘子的精确测试

2026-10-21。个人研究备份，strategy_dual；任务 Q-CAG-HALF，仍 OPEN。
本文没有提出新的半覆盖 Claim。下面的普遍恒等式是现有
`terminal_reply_transport.md` 式 (2)、`terminal_tie_quotient.md` 式 (3) 的另一表示；
平方方向是其二次分子的一个可支付充分方向。新增价值是把全部转移写成少一位
incumbent 的普通查询差，并把“共同重选早期乘子”明确还原为一个配对质量锥。
没有外部新颖性或独立数学审查结论。

## 一、对象及删人恒等式

固定 n 位单位提供者、p 个共同主题标签和完整有序历史形式策略 sigma。
客户类型为非空 T，记 x_s=1{s in T}。对非负整数计数 q 定义

R(q;a,b)(T)=(x_a-x_b)/(1+q·x).

q 可以是任意长度的前缀计数；这里的 R 只是查询收益差，不能自动称为同一个
n 人游戏中的真实激励行。固定末前缀 ell，q=q(ell)、原末回复 a、规范回复 b。
在 q_s>0 时，已有的 incumbent 转移张量为

delta(q,s;a,b)(T)=x_s(x_a-x_b)/[(q·x)(q·x+1)],

分子零时取零。令 e_s 为第 s 个单位向量，则逐类型精确成立

**delta(q,s;a,b)=R(q-e_s;a,b)-R(q;a,b).**                       (D)

证明：x_s=0 时两边均零；x_s=1 时 q·x>=1，右侧为
(x_a-x_b)[1/(q·x)-1/(q·x+1)]。涵盖 q·x=0、重复主题及 a/b 不在前缀的情况。

另一个可核验但不是福利界的递推是，令 k=sum_s q_s，

**(k+1)R(q;a,b)=sum_s q_s R(q-e_s;a,b)
                  +1{q·x=0}(x_a-x_b).**                    (D2)

这是将 (D) 按 q_s 求和；删人后的查询差必须保留未覆盖边界项。

## 二、完整误差的商空间降阶

沿用现有运输图：每条真实早期行 (h,t) 给边
(ell_ht,t) -> (ell_h,sigma(h))，边权 lambda_{h,t}>=0。
令 kappa_{ell,s} 为入流减出流。已有精确式是 E=sum kappa delta。
设 H 是全部同计数末回复相反行的显式线性包。每个 R(q(ell);a_ell,b_q)
都在 H 中，并且其任意符号倍数有原真实末行的非负表示。
因此 (D) 立即给出

**E ≡ sum_{ell,s} kappa_{ell,s}
       R(q(ell)-e_s;a_ell,b_q)  (mod H).**                  (Q)

这不是用一个伪行代替真实行的许可。右侧 ghost 查询在 n-2 长度背景中，只是
同一个商空间元素的精确表示；尚缺把它们用 n 人真实分支共同支付的机制。
与旧稿的关系是：它把二次 numerator / p(p+1) 改写为两条一次查询差，没有扩大
已证明的可提升锥，也没有解决一般构造义务。

若已给规范化证书 d=barGamma^T lambda+r，r>=0，则 (Q) 可用于选取商空间
余项的代表；原商空间条件 r+E in R_+ + H 完全等价于
r+sum kappa R(q-e_s) in R_+ + H。并非更弱或更强条件。

## 三、平方可支付方向及真实可达性

若某改变叶的净 incidence 满足

kappa_{ell,s}=t_ell(1{s=a_ell}-1{s=b_q}), t_ell>=0,

且这两个主题在前缀中，则该叶误差为

**t_ell (x_a-x_b)^2/[p(p+1)]>=0**, p=q·x。                (S)

所以不必要求 E=0；已有条件性提升定理也允许逐类型非负 E。
(S) 是旧二次公式直接导出的充分方向，不单独登记新 Claim。若 a/b 不在前缀，
缺失的 incumbent 顶点不允许凭空加流；不能把任意给定 kappa 宣称可由真实边实现。

`deletion_audit.py` 给 n=4、p=3 的真实两边形式策略：标签 A,B,C；除以下行动
外全部节点选 C：sigma(A)=A，sigma(AA)=B，sigma(AC)=A，sigma(ACA)=A。
只把末回复 ACA 从 A 改成 C，其计数代表 AAC 原来选 C，根 CCCC 保持。
给真实行 (A,偏离C)、(AC,偏离C) 各权一，边分别为

(ACA,C)->(AAB,A)，(ACC,C)->(ACA,A)。

只有改变叶 ACA 留下 kappa_A=1,kappa_C=-1，故 E=(x_A-x_C)^2/[p(p+1)]。
这是形式策略上的全类型恒等式；不声称它在有不同覆盖主题的客户数据上为 SPE。
全兴趣客户使任何形式策略为合法 SPE，但在该质量上这个平方为零。

一般仍缺：为每个完整策略和比较 portfolio 构造非负规范化证书，同时让真实
边的 kappa 落在这类平方方向、跨叶相消、H 支付和余项预算之和中。
只写一个非负平方不提供这样的构造。

## 四、允许共同重选早期乘子的配对锥

把原 Gamma 拆为早期 E0 和末位 L，把规范矩阵拆为 E1、L1，按同一真实
(h,t) 次序排列早期行。两形式策略有相同根覆盖向量 c。给比较并集行 o，令
d=beta c-o。考虑比固定提升更宽的共同乘子要求：存在 lambda,alpha,eta,r,s>=0，

d=E0^T lambda+L^T alpha+r,
d=E1^T lambda+L1^T eta+s.                                  (C)

两边可重新挑选全部末行，早期乘子共同选。原 quotient-lift 成功会导出 (C)，
反向未证，因为 quotient-lift 对末行拆分和纠正有额外结构。

**精确 Farkas 判别。** (C) 成立，当且仅当对所有非负配对客户质量 (u,v) 满足

L u>=0，L1 v>=0，E0 u+E1 v>=0，                            (P)

都有 d·(u+v)>=0。证明是对有限生成锥
diag(E0,E1)、分开的末行以及坐标非负射线应用有理 Farkas；逐项与 (u,v)
内积给必要性，锥分离给充分性。

这里的 (P) **不是完整 SPE**：两个不同客户总体的早期激励 slack 可以互相抵销。
若找到 (P) 且 o·(u+v)>2c·(u+v)，只能否定共同早期乘子机制，不能反驳主目标。
也不能把两个总体分别称为原/规范化 SPE；它们只各满足末位约束。

把 c·(u+v)=1 归一化后截面紧。根的 pooled 最优性给每个主题总规模
size_a(u+v)<=n c·(u+v)，继而总质量<=np；因此这个辅助模板的最坏比例
可由有限有理 LP 实际取得。`paired_lift_search.py` 实现此 LP 并用 Fraction
复核每个接受的配对原始点。未实现严格的全部对偶恢复，不把浮点最优值称证书。

## 五、实际运行、身份和未解决部分

2026-10-21 的运行：随机 5000 个 (n,p)=(3,3) 形式策略，最高**发现的可行**
配对值 4/3；随机 1000 个 (4,4) 且根全部选择同一标签的形式策略，最高发现值 1。
随机形式策略通常使锥过窄，这不是对共同乘子机制有力的证据。
已有冻结 m4p5 策略锥样本的 70 个策略、每个 5 个四主题比较集合，最高发现
配对值 7/4。全部只保存精确原始可行点；没有覆盖所有策略，也不证明模板上界。

可重现命令（仓库根）：

```
python3 research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/strategy_dual/deletion_audit.py
python3 research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/strategy_dual/paired_lift_search.py --trials 5000
python3 research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/strategy_dual/paired_lift_search.py --topics 4 --players 4 --trials 1000 --root-single
```

下一步应先用稀疏 LP 联合挑选早期乘子，并精确约束真实 kappa 的平方/零流锥。
若该模板失败，保存配对或网络分离证书；若有限样本成功，仍需寻找无界树的
构造规则。主目标 Q-CAG-HALF 仍 OPEN。
