# next_tree：在轨节点真实菜单的聚合安全候选

身份：探索笔记，未证猜想；Q-CAG-HALF仍OPEN。只覆盖本文明确的有限实验，不能从零反例外推一般定理。2026-10-21。

## 已读基线

已读根AGENTS、模型、根/本题RESEARCH_STATE与FAILED_ROUTES、strategy_cone、security_cone_duality、terminal_reply_transport、iid_security_and_flow_barriers、security_chain、dynamic_iid_debt、stationary_pair_transport、continuation_security_barriers。旧单人根菜单、固定根stationary核、固定节点内平均均已失败；以下候选不等同这些接口。

## 精确新候选 A：所有在轨节点菜单的自由混合

固定任意有限共同目录、m名单位玩家和一个完整有序历史纯SPE sigma。令实际有序路径为 z=(S_1,...,S_m)。对每个在轨位置i和每个合法行动a，从实际前缀(S_1,...,S_{i-1})改选a后，后继沿同一个原sigma真实执行，得到有序终局 z_i(a)。定义

C_i={B_i(a): a合法}, B_i(a)=z_i(a)去掉位置i；
M=并_{i=1}^m C_i。

每个B是m−1个合法主题构成的静态竞争元组。不同顺序但同计数的B可在该静态矩阵里合并；这不合并原完整策略节点。
对纯查询主题t定义 f_B(t)=sum_{x∈t}1/(1+load_B(x))。

候选：

cap_M := min_{Q∈Delta(M)} max_t E_{B~Q} f_B(t) <= W(z)/m.  (A)

Q可以依赖实例、完整sigma；B抽样不观察独立查询t。M包含所有实际节点的真实竞争菜单，未添加任意离轨节点的菜单。若添加全树末层全部历史，则已等于所有静态m−1元组而失去该候选的结构内容。

(A)比真正W>=m v_m充分桥强，因为允许背景全集的安全值v_m<=cap_M；再用已证v_m>=OPT_m/(2m−1)即可得更强OPT_m<=(2−1/m)W。尚无证明。旧单i菜单cap(C_i)<=u_i已假；它不否定(A)。

## 更强探索 B：分菜单值总和

令z_i=min_{Q_i∈Delta(C_i)} max_t E f_B(t)。更强候选为sum_i z_i<=sum_i u_i=W。它蕴含min_i z_i<=W/m及(A)。该式亦未证。

## 抽象势游戏外推（纯探索）

对共同有限行动集A，终局只看多重集。令任意实值函数Phi_m定义于m元多重集，Phi_{m−1}定义于m−1元多重集，效用
u(a,B)=Phi_m(B+a)−Phi_{m−1}(B)。

这是一般对称精确势形式；无需非负客户、单调性或效用正性。CAG取Phi_k=sum_x H_load。因此若(A)甚至(B)在此大类成立，会给不需要逐客户非负余项的纯势运输恒等式。当前只有有限LP线索，没有已证定理。

## 代码与有限实验范围

- menu_search.py：固定已有完整CAG策略sigma，枚举2^p−1客户类型，重构全部逐(h,a)真实Gamma行；按W=1归一。固定查询分布p，LP最大化m t，约束t<=E_p f_B对每个B∈M。它只生成浮点候选，未输出精确证书。六棵策略（individual_security_failure、root_stationary_kernel、root_tax_failure、worst_cce_welfare_failure、empirical_iid_kernel、local_security_increment），各约200个随机/均匀/纯查询p，观测最优m t<=1（浮点误差范围）。不穷尽查询分布或策略。
- abstract_test.py：随机抽象势->逆向归纳完整SPE->计算cap_M。10000次n3p3（势上层0..29、下层0..9）无失败；另临时变体2000次n3p3与2000次n3p6（上下层0..99）无失败。这些临时变体未单独落盘，源代码可按记录替换常数复现。
- abstract_cone.py：sigma先由随机势生成，再固定sigma；对其全部真实SPE行和固定查询p，在自由signed势变量[-1,1]上LP最大化cap下界−W/m。300棵n3p4、每棵10个p；临时变体100棵n4p4、每棵10个p；均未见正差。固定sigma可被零势实现，LP本身允许退化锥，但sigma采样仍来自随机势，存在严重选择偏差。
- 一个未落盘临时变体把每i查询p_i独立，测试更强(B)；100棵n3p4、每棵10场p_i，未见正差。不应把这些数字称为定理、全称证书或可靠概率估计。

Boss要求停止加样本，转证明。global研究员正在独立用随机形式sigma（区别随机势产生sigma）攻击上述抽象外推；其任务可检测稀有/退化策略锥。

## 当前数学义务

固定任意sigma、固定查询p，若(A)在抽象势类成立，应能给Q>=0、sum Q=1、lambda_{h,a}>=0满足精确势变量恒等式

W_sigma/m − sum_{B∈M}Q_B E_{t~p}u(t,B)=sum_{h,a}lambda_{h,a} Gamma_{h,a}。

这里效用对自由signed势线性，不能再使用逐客户非负余项r；完整sigma与全部有序历史仍保留。一般存在性仍待证，不能循环引用(A)加Farkas。

下一步：把势表示成m层/ m−1层多重集二部图上的边差，尝试由真实节点比较产生非负流；全在轨菜单限制是承重范围。若global找出抽象反例，检查CAG正重数能否实现，不能把signed反例直接称为半覆盖反例。
