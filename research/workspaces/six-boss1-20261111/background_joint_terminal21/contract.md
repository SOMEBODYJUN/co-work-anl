# 固定 actual 尾第一源的21参数共同末题合同

本页在计算前明确合同；它不预设65原子上的符号。原六人有限单位客户、有限非空共同标签目录、完整有序历史纯SPE模型不变。目录可有空覆盖、重复标签覆盖；比较五元组可重复；弱平局不作择优强化；客户集合可为空。65原子仅是证明方法反测度，不能解释为一个可共同实现的SPE。

## 1. 同一策略、背景及旧AB记录

固定一份完整纯SPE，固定合法先行标签Z，令客户背景位为 b_x=1_Z(x)。其后尚余五人，actual路径为(A,B,C,D,E)，十个固定可见合法标签为ABCDEUVWXY；U,V,W来自(A,E,U,V,W)，X,Y来自(A,B,E,X,Y)，均按原策略在对应有序历史取得。五个比较标签(T_1,…,T_5)先固定，保留所有索引。每客户 d_x=Σ_j1_{T_j}(x)。

旧AB第j路为(Z,A,B,T_j,X_j,Y_j)。第三尾位T_j被强制，第四、第五尾位依原策略续局；只对真正末位Y_j使用最佳回复。定义

\[
p_{j,x}=b_x+1_A(x)+1_B(x)+1_{T_j}(x)+1_{X_j}(x),\qquad
D_x=\sum_{j=1}^5\frac1{p_{j,x}+1},
\]
\[
L_x=\sum_{j=1}^5\frac{1_{Y_j}(x)}{p_{j,x}+1_{Y_j}(x)},\qquad
U_{AB}=\sum_xL_x,\qquad \bar y_x=\frac15\sum_j1_{Y_j}(x).
\]

收益份额零分子取零，包括0/0。D的分母总是正。对任意合法标签F，五个旧真实末位各比较F后相加，得到

\[
\sum_xD_x1_F(x)\le U_{AB}.\tag{AB-price}
\]

这是五笔旧离轨末位收入之和，不能替换为actual的u_E。重复标签仍按五个索引支付、比较；上述不等式对所有合法F同时成立。客户为空时两边均为零。

## 2. 唯一固定源与新末位

始终返回同一真实源 h=(Z)。固定原完整策略，对任意合法强制主题T，强制actual尾第一人选择T后依原策略续局，得到三个中间主题R_1(T),R_2(T),R_3(T)及真实末题C_h(T)。完整纯策略已固定全部平局的行为，因此C_h是合法目录上的一个确定映射；不能用另一强制历史的后继替换它。

对客户记 t=1_T(x)，c=1_{C_h(T)}(x)，s=Σ_{i=1}^3 1_{R_i(T)}(x)。上一轨道标签P也必须合法，a=1_P(x)。新末位真实收入的逐客户份额为 c/(b+t+s+c)，偏离任一合法F的份额为1_F/(b+t+s+1)。

设r_A为actual尾第一人的终局收益、u_E为actual尾第五人的终局收益、K为同一共同目录的最大主题大小；ell_x=b_x+1_A+1_B+1_C+1_D是actual末位前缀负载。源SPE给

\[
r_A\ge\sum_x\frac{t_x}{b_x+t_x+s_x+c_x}.
\]

actual真正末位可比较每个新中间主题和新末题，因此对任意合法F有u_E≥Σ_x1_F/(ell_x+1)。容量亦给|F|≤K；每个中间分别支付其一次价格/容量预算。

## 3. 全部21个客户无关非负参数

参数依次为

\[
\sigma,\alpha_m,\alpha_l,\beta_m,\beta_l,
\mu_A,\mu_B,\mu_C,\mu_D,\mu_E,\mu_U,\mu_V,\mu_W,\mu_X,\mu_Y,
\mu_{\mathrm{mean}},\mu_Z,\mu_{\mathrm{cur}},\mu_{\mathrm{prev}},\lambda,\mu\ge0.
\]

这21个参数对所有客户、所有真实轨道步骤相同。它们可任意取零；不要求源权与查询总权平衡。归一化Σ参数=1只为随后完整锥LP去除正齐次尺度，零向量独立给0≥0。

令

\[
q_x=\sum_{Q\in\{A,B,C,D,E,U,V,W,X,Y\}}\mu_Q1_Q(x)
+\mu_{\mathrm{mean}}d_x/5+\mu_Zb_x,
\quad M=\sum_Q\mu_Q+\mu_{\mathrm{mean}}+\mu_Z+\mu_{\mathrm{cur}}+\mu_{\mathrm{prev}}.
\]

静态标签先固定；d/5和ybar只表示各五次合法最佳回复比较的平均，不把分数会员强制为一个主题。令

\[
H_{0,x}(a,t,c,s)=\frac{\sigma t-Mc}{b+t+s+c}
+\left(\beta_m+\frac{\alpha_m}{\ell_x+1}\right)s
+\left(\beta_l+\frac{\alpha_l}{\ell_x+1}\right)c
+\frac{q_x+\mu_{\mathrm{cur}}t+\mu_{\mathrm{prev}}a}{b+t+s+1}.
\]

新末位比较十静态标签、比较五元组、Z、当前T、上一P，分别给对应的非正增项“查询收益减自身收入”。加源IC、三个中间及末题的actual末价/容量，得

\[
B_0:=\sigma r_A+(3\alpha_m+\alpha_l)u_E+(3\beta_m+\beta_l)K
\ge\sum_xH_{0,x}(a_x,t_x,c_x,s_x).
\]

把同一个合法新末题F=C_h(T)代入(AB-price)，产生λc_xD_x并完整支付λU_AB。再由这个新真实末位逐一比较五个旧Y_j、以μ/5加权，得到非正增项

\[
\mu\sum_x\left(\frac{\bar y_x}{b_x+t_x+s_x+1}
-\frac{c_x}{b_x+t_x+s_x+c_x}\right)\le0.
\]

因此定义

\[
\widehat H_x=H_{0,x}+\lambda cD_x
+\mu\left(\frac{\bar y_x}{b+t+s+1}-\frac c{b+t+s+c}\right),
\]

每个真实步骤均满足唯一共同预算

\[
B:=B_0+\lambda U_{AB}\ge\sum_x\widehat H_x.\tag{Step}
\]

这里两新增项的c严格是同一新末题、同一客户的会员；D,L,ybar始终由同一客户的完整AB直方图计算。未为各客户或轨道时刻选择不同乘子。

## 4. 半折扣、初态ZZ及零权面

对每客户的全部四个(a,t)∈{0,1}²，定义

\[
\widehat V_x(a,t)=\min_{c\in\{0,1\},\ s\in\{0,1,2,3\}}
\{\widehat H_x(a,t,c,s)+\tfrac12\widehat V_x(t,c)\},\qquad
\widehat\Psi_x=\tfrac12\widehat V_x.
\]

这是有限动作、折扣1/2的收缩算子，任意有限非负参数下有唯一有限值，包括任意零权面。所有候选分母只有原收益份额可能为零；此时t=c=0，分子σt−Mc也为零，按零定义连续合法。其它分母均至少1。

令T_{−1}=T_0=Z，T_{n+1}=C_h(T_n)。第n步的上一/当前标签对为(T_{n−1},T_n)，每步都返回同一源h，取这一真实强制分支。它不要求C_h(Z)=Z。逐客户Bellman极小值不大于该真实(c,s)的费用加后继值，结合(Step)得

\[
B\ge\sum_x\widehat V_x(1_{T_{n-1}},1_{T_n})
-\tfrac12\sum_x\widehat V_x(1_{T_n},1_{T_{n+1}}).
\]

以2^{−n−1}加权并求和；总预算权为1，有限目录、有限客户使尾项消失。于是

\[
\boxed{\sigma r_A+(3\alpha_m+\alpha_l)u_E+(3\beta_m+\beta_l)K
+\lambda U_{AB}\ge\sum_x\widehat\Psi_x(b_x,b_x).}\tag{Joint-AB-21}
\]

λU_AB只支付一次，未消失或移动到actual收入。逐客户选独立(c,s)是对共同真实主题的放松；不声称这些局部路径可共同实现。所有权为零时V=0；客户为空时V求和、r_A、u_E、U_AB、K均为零。弱平局、空题、重复行动、同覆盖异标签均只用非严格IC，原样保留。

客户行系数为σu_{A,x}+(3α_m+α_l)u_{E,x}+λL_x−Psi_x(b,b)，共享K系数为3β_m+β_l。这是本次输入、LP和独立字面核共同采用的唯一收费口径。

## 5. 本次计算范围

只在既有65原子及其共同容量质量上检验上式的完整21维非负归一锥；每原子保留原mass与完整witness，绝不按旧37个(b,bits,d)类型平均AB信息。每原子四自由Bellman值，全部8动作；共281变量、2080不等式、一个归一等式。源、折扣、初态及静态菜单固定；没有重跑58云任务、来源扫描、折扣扫描或外层优化。

精确非分离的充分证书是每原子的非负归一折扣occupation ξ满足

\[
\sum_a\xi_{s,a}-\tfrac12\sum_{r,a:\,next(r,a)=s}\xi_{r,a}
=\tfrac12\mathbf1_{s=(b,b)}.
\]

设h_{i,j}(s,a)是第j参数的单步系数、β_j是一次预算系数，
r_j=β_j−Σ_i m_iΣ_{s,a}ξ_{i,s,a}h_{i,j}(s,a)。对任意非负参数v，Bellman极小值不超过任意这类occupation费用，因此B−Σ_i m_iPsi_i(b,b)≥Σ_jv_jr_j。逐项精确r_j≥0才能封住全锥；仅返回一条正参数行不够。

本页公式依据实读的 main_previous_theme_price.md、background_reweight/pending_joint_terminal_price.md、repeated_z_price/contract.md 与“五人证书活跃行--证明.md”。实际输入记录其SHA以及完整65原子来源SHA。
