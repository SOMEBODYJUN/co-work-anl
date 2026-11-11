# 重复Z真实分支：尾第一源、半折扣的完整19参数锥

## 实际结论

按 Main 指定，只考察 actual 尾第一源 h=(Z)、θ=1/2、初始标签对 (previous,current)=(Z,Z)。静态查询允许十个可见合法标签 A,B,C,D,E,U,V,W,X,Y、五比较主题的均匀菜单以及 Z；动态查询为 current 与 previous。五个来源/价格/容量参数加十四个查询参数，共19个**全局非负**参数，一并优化，按总和一归一。

在已经通过66条行的65原子对偶测度上，这个完整参数锥不能分离。已保存一个有理 occupation-flow 证书，独立重放给出

\[
\boxed{\mathcal B-\sum_x\mu_x\Psi_x(b_x,b_x)
>\frac7{100}
\qquad\text{对全部19参数的非负归一向量。}}\tag{NZ}
\]

完整有理证书的更强下界约为0.07193801195993763；数值发现返回的有理参数行余量约为0.07193801195993820。两者未被宣称精确相等，故没有声称求出整个参数锥的精确最优值。严格非分离由全部19个坐标的有理对偶残差承担，不是因返回行非负而推断。

这只封住上述单一源、折扣、初态、静态菜单及65原子测度。不扩展到其他源/折扣，不说明一般正价、重复Z真续局或五人背景half无效，更不把对偶 occupation 视为可共同实现的 SPE。

## 1. 来源、负载与真实轨道

先实读 Main 的 main_previous_theme_price.md、既有 previous_price_search/discover.py 与独立 verify.py。复用的是已证四状态预算合同；本次重新构造明确的背景五尾参数锥，没有调用旧六人的点输入或将旧90案结论移植到本点。

固定原完整纯SPE与合法前置标签Z。尾第一源实际规定主题为A，尚余k=5人。对任意合法强制主题T，返回**同一个源历史 h=(Z)**，强制该源选择T，再沿原策略完成；记真实末题为 C_h(T)，三个中间主题的会员总数为s。C_h 是同一有限标签目录上的真实映射，保任意弱平局，不冻结另一条强制支路的后继。

逐客户记背景位 b=1_Z，十个可见会员 bits，以及五比较计数 d。源背景负载与 actual 末价前缀分别为

\[
p=b,\qquad \ell=b+1_A+1_B+1_C+1_D.
\]

源收入 r1 是 actual 尾第一人的真实收入，u5 是 actual 尾末位E的真实收入，两者都按终局分母 b+c_tail 计算。没有把前置者自己的收入混进尾源预算。

初态为 (a,t)=(b,b)，对应合法标签对(Z,Z)；不要求 C_h(Z)=Z。之后的标签对严格沿

\[
(Z,Z)\to(Z,C_h(Z))\to(C_h(Z),C_h^2(Z))\to\cdots
\]

变化。每次强制仍从同一h返回，来源预算按几何权只支付一次。

## 2. 19参数、单步成本与完整预算

参数依次为

\[
\sigma,\alpha_m,\alpha_l,\beta_m,\beta_l,
\mu_A,\ldots,\mu_Y,\mu_{\rm mean},\mu_Z,
\mu_{\rm current},\mu_{\rm previous}\ge0.
\]

其中从 A 到 Y 精确指 ABCDEUVWXY 十个标签。令

\[
q_x=\sum_{Q\in\{A,B,C,D,E,U,V,W,X,Y\}}\mu_Q1_Q(x)
+\mu_{\rm mean}d_x/5+\mu_Zb_x,
\]

\[
M=\sum_Q\mu_Q+\mu_{\rm mean}+\mu_Z
+\mu_{\rm current}+\mu_{\rm previous}.
\]

d/5 只表示对五个真实合法查询索引的线性平均，不作为分数强制主题。对四状态(a,t)、后继末位会员c∈{0,1}、三中间总数s∈{0,1,2,3}，成本为

\[
H_x(a,t,c,s)=
\frac{\sigma t-Mc}{b+t+s+c}
+\left(\beta_m+\frac{\alpha_m}{\ell+1}\right)s
+\left(\beta_l+\frac{\alpha_l}{\ell+1}\right)c
+\frac{q_x+\mu_{\rm current}t+\mu_{\rm previous}a}{b+t+s+1}.
\]

所有零分子份额取零。来源IC、三个中间与一次末题的 actual 末价/共同容量、同一真实末节点的合法查询给出一次预算

\[
\mathcal B=\sigma r_1+(3\alpha_m+\alpha_l)u_5
+(3\beta_m+\beta_l)K.
\]

四状态 Bellman 方程为

\[
V_x(a,t)=\min_{c,s}\{H_x(a,t,c,s)+\tfrac12 V_x(t,c)\},
\qquad \Psi_x=\tfrac12V_x.
\]

由同源真实轨道的几何加权或有限目录平方上的最大化证明，普遍有

\[
\mathcal B\ge\sum_x\Psi_x(b_x,b_x).
\]

局部极小域允许每客户独立选c,s，是对真后继的放松；未将其认作原策略。这条普遍合同来自解析证明，本次只研究它在指定65原子上的整个参数锥能否分离。

## 3. 一次完整参数优化，而非网格

对65原子按 (b,十位bits,d) 合并，恰有37个正类型。每型保四个自由 Bellman 值，所有19个非负参数共享于全部类型。以每型每状态的全部8个(c,s)动作建立 Bellman 线性不等式，得到167变量、1184不等式、一个参数归一化等式的 LP。

该 LP 一次优化整个连续19参数单纯形；没有为不同客户单独挑参数，也没有固定旧的隐藏极值模式。返回的有理非零权为

\[
(\sigma,\alpha_m,\beta_m,\mu_V,\mu_W,\mu_{\rm mean})
=\frac1{3708}(3228,40,5,5,5,425),
\]

其余13项为零。其一次预算为

\[
\mathcal B=\frac{3228r_1+120u_5+15K}{3708}.
\]

返回权没有使用 previous，但发现与对偶核验都保留了它和其他全部参数；不能据此把 ν=0 当成完整锥的先验限制。

对该有理权，程序独立枚举16个确定下一位策略，并对每条边全部s取极小，恢复四状态精确值。点上精确余量保存在 single_case_result.json，为正约0.07193801195993820。

## 4. 为什么能够给全部19参数的非分离结论

每个可见类型有一份精确有理的归一动作概率与折扣占用流 ξ。初态质量为 δ_(b,b)，流满足

\[
f_s-\frac12\sum_{r,a:\,\mathrm{next}(r,a)=s}\xi_{r,a}
=\frac12\delta_{s,(b,b)},\qquad
\xi_{s,a}=f_s\pi_{s,a},\quad\sum_sf_s=1.
\]

这些流只用作 Bellman 参数 LP 的对偶对象。对任意参数λ，最小 Bellman 值不超过这份固定 occupation 的费用。因此将一次预算减去该费用，得到19个参数坐标残差 r_j，并有

\[
\mathcal B-\sum_x\mu_x\Psi_x(b_x,b_x)
\ge\sum_{j=1}^{19}\lambda_jr_j.
\]

全部r_j均由保存的长分数精确计算，且逐项严格大于7/100。参数和为一即得(NZ)；未归一的参数则得到下界 (7/100)Σλ_j。这个结论涵盖完整参数锥，且不要求把各类型的对偶动作拼成一个真实目录策略。

## 5. 独立验证及封界

verify_one.py 不导入发现器或优化器。它用路径/环几何和计算16个确定策略值，按三个**字面**中间会员位重建单步费用，独立审计37类型的2368个 Bellman 比较、148个精确流方程和全部19个参数残差。实际返回

INDEPENDENT-19-PARAMETER-NONSEPARATION-PASSED。

复核入口：

```sh
python research/workspaces/six-boss1-20261111/background_reweight/repeated_z_price/verify_one.py
```

本次只做这一案，发现与两份精确算术合计为秒级本地检查；没有启动批扫描或外层收费重优化。原58行云任务依赖未改。文件输入SHA、源码、完整参数/占用证书与独立报告均在本目录；单案主结果 SHA 为 81199eaab876ce9730cb78d5fd1e2f74d1629da7c7d9c1f26217441a431a6e85，最终指纹见 manifest.json。

下一缺口必须比“固定本案后继续改这19个全局权”更强。当前结果不排改变来源、初始标签对或加入与已有真实分支联合会员保持同一性的查询，但不能把未测的选择说成有效分离，也不据此自动启动扩大扫描。
