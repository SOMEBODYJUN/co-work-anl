# KS14 测试相关系数、解析参数与三一致超图承诺范围

Boss2，2026-11-12。数学身份为既有 `M-9f8033b6e1a4485b97636171b09f8218` 的证明与范围澄清；不新增同义定理节点。两份独立审读分别见同目录 `hypergraph-threeuniform-3d-review.json` 与 `ks-correlation-narrow.json`。本页给出可直接使用的局部替代证明，保留完整 typed/约束 ID 归约的其余有效部分。

## 一、当前命题与分离阈值

对每个先固定的 (0<\delta\le1/2)，区分有限未加权三一致超图的完整二着色 YES 与不存在比例至少 (\delta) 的独立集的 NO 为 NP-hard。内部取正有理 (\alpha<\delta)，并可取 (\alpha<1/2)；归约实际给 NO 独立集比例严格小于 (\alpha)。全部构造常数在源字母表和输入规模之前固定。

这里把 FMW Corollary 1.10 的“任意正固定阈值”惯例展开为分离的承诺域。每个二着色超图有至少半数顶点的独立色类。四点上全部四个三元组构成的 (K_4^{(3)}) 可按二加二染色，且最大独立集恰为二点。因此 (\delta>1/2) 时，原字面 YES 与 NO 两类可能重叠；(\delta=1/2) 因 NO 使用严格小于仍分离。对较大的阈值，内部更小 (\alpha) 的构造仍有相应更强 NO 输出保证，但该输出事实不另构成两类全域分离的承诺问题。冻结作者原句和共享文献页保持来源身份，当前登记以本节精确域为准。

## 二、真实测试分布与精确二部相关

固定 (0<\theta<1/2)，实际层差 (h\ge1) 的 fiber 大小为 (r=4^h\ge4)。先独立均匀取 (X,Y_1,\ldots,Y_r\in\{-1,1\})，令 (Z_i=-Y_i)。以概率 (\theta) 均匀选择 (J\in[r])，把 (Y_J,Z_J) 同时改成 (-X)。测试分布本身不改。

令 (S=\{\exists j:Y_j=Z_j\})。未修改时所有坐标均相反；修改时恰有一个相等坐标，且该坐标等于 (-X)。所以 (S) 正好是修改事件，其唯一坐标 (J) 可由 ((Y,Z)) 识别，且
\[
\Pr(S)=\theta,\qquad
m(Y,Z):=E[X\mid Y,Z]= -\sum_{j=1}^rY_j\mathbf1_{\{Y_j=Z_j\}},\qquad E[m^2]=\theta.
\]
无修改时 ((Y,Z)) 与 (X) 独立，故上述条件期望在 (S^c) 上为零。取 (f(X)=X)、(g(Y,Z)=m(Y,Z)/\sqrt\theta)，两者均值零、二阶矩一，且 (E[fg]=\sqrt\theta)。反向，均匀二值 (X) 的每个中心化函数均为 (cX)，由条件期望与 Cauchy–Schwarz，任何归一 (g) 的相关至多 (\|m\|_2=\sqrt\theta)。因此
\[
\boxed{\rho(X;(Y,Z))=\sqrt\theta.}
\]
KS14 冻结物理19／印18页 Lemma 5.9(ii) 的 (\rho\le\theta) 不成立；例如 (r=4,\theta=1/4) 时实际为 (1/2>1/4)。后续二部 Gaussian 比较使用 (\rho_0=\sqrt\theta<1)。

## 三、另外两种相关量与最小原子

修改与未修改的支撑不交，最小正原子准确为
\[
a=\min\left\{\frac{1-\theta}{2^{r+1}},\frac{\theta}{r2^r}\right\}.
\]
在实际范围 (r\ge4,\theta<1/2) 中，(a=\xi:=\theta/(r2^r))。原文任意概率和任意正 (r) 的更宽原子声明不能用于本范围之外。

在 (((X,Y),Z)) 的支撑二部图中，未修改边把 ((x,y)) 接到 (z=-y)。对任意右点 (z) 及坐标 (j)，左点 ((x=z_j,y=-z)) 同时有未修改边到 (z)，和修改第 (j) 位后的边到 (z^{(j)})。故所有右点沿超立方体单坐标翻转连通，每个左点也通过未修改边接入。由 (Y,Z) 对称性，(((X,Z),Y)) 同样连通。KS14 Lemma 5.2 于是给相应二部相关至多 (1-\xi^2/2)。又 (\xi\le(1-\theta)/4)，所以 (\sqrt\theta\le1-\xi^2/2)。三空间平滑可继续使用
\[
\rho(X,Y,Z)\le1-\xi^2/2.
\]
Lemma 5.9(iii) 最后等号右端另漏印了 (1-)；实际使用的是左边的 (1-\xi^2/2)。

给定 (Y)，(Z) 以概率 (1-\theta) 等于 (-Y)，以概率 (\theta) 把 (-Y) 的均匀一位翻转。均匀边缘下，Fourier 角色 (\chi_A) 的转移特征值为
\[
\lambda_A=(-1)^{|A|}\left(1-\frac{2\theta|A|}{r}\right).
\]
故在实际 (0<\theta<1/2) 中
\[
\rho(Y;Z)=\max_{1\le k\le r}\left|1-\frac{2\theta k}{r}\right|
=1-2\theta/r=:1-\eta.
\]
这一直接计算支付 Lemma 5.18 所需 ((1-\eta)^{s/r}) 尾界；仅引用更弱的 Lemma 5.9(iv) 不足以说明该显示式。

## 四、重新固定全部解析参数

令 (L=\lceil32\alpha^{-2}\rceil)，先固定测试噪声 (\theta\in(0,1/2))（可取 (1/4)）及 (\rho_0=\sqrt\theta)。对有限个 (h=1,\ldots,L-1)，设
\[
r_h=4^h,\quad \xi_h=\frac{\theta}{r_h2^{r_h}},\quad
\eta_h=\frac{2\theta}{r_h},\quad b_h=(\alpha/2)^{4/\eta_h}.
\]
(\Gamma_\rho) 在此指原 Definition 5.3 的下 Gaussian 稳定性函数。分别取正 (\nu_h<\min(e^{-1},b_h/20)) 足够小，使
\[
\Gamma_{\rho_0}(\alpha/2,b_h/2-5\nu_h)-2\nu_h>0.
\]
因为 (\rho_0<1)，两个正边缘处的 Gaussian 概率严格为正，连续性给出这种选择。再取足够小的绝对系数 (c_\gamma>0)，使
\[
0<\gamma_h\le c_\gamma\frac{\nu_h\xi_h^2}{\log(1/\nu_h)}
\]
支付三空间平滑的两次误差。二部不变性阈值可保守取
\[
0<\tau_h\le
\nu_h^{\,C\log(1/\xi_h)\log(1/\nu_h)/(\nu_h(1-\rho_0))},
\]
其中 (C>0) 足够大。这里保留物理22／印21页 Lemma 5.14 原显示式指数中的额外 (\log(1/\nu_h))；该更小阈值足以满足 Theorem 5.8。一般 Gaussian、不变性、reverse hypercontractivity 工具按 KS14 的精确成熟接口复用；此处新付的是本分布的相关量及其正确调用。

取整数
\[
s_h\ge\max\left\{\frac{r_h}{\xi_h}\log\frac1{\nu_h},
\frac{r_h}{2\gamma_h}\log\frac{32r_h^2}{\tau_h}\right\}.
\]
精确 (Y,Z) 相关和三空间平滑界分别支付这两个高阶尾项。随后取 (T_h) 使
\[
4(s_h^2/T_h)^{1/4}\le\min\{b_h/2,\alpha^2/128\},\qquad
2(s_h^2/T_h)^{1/4}\le\tau_h/(16r_h^2).
\]
一次统一取整数 (T\ge\max\{2,T_1,\ldots,T_{L-1}\})，最后取正有理
\[
0<\zeta<\min_h\frac{\alpha^2\tau_h^2\gamma_h^2}{2048r_h}.
\]
有限个严格正余量的最小值仍为正。需要显式编码时，可在上述严格界内选有理 (\nu_h,\gamma_h,\tau_h)，再上取整 (s_h,T_h,T)。最后才调用 FMW 的源 soundness (\zeta/2) 和独立正规化误差 (\zeta/2)，确定常数字母表。

Lemma 5.14 及其 Eq. (16)、(17)、(30) 的 Gaussian 下标均应为 (\rho_0)，τ 分母为 (1-\rho_0)；三空间 γ 则仍使用 (1-\xi_h^2/2)。真实测试噪声 θ、ξ、η 不因 Gaussian 下标修正而机械替换。旧数值阈值不直接沿用，按上面次序重选。

## 五、完整归约的接合

现有两输入仍为 perfect exact4 PCP 源与保 perfect 的整数双正规化桥。均匀层顶点、均匀 incident 约束 ID、typed 有序坐标、每层对 soundness、weak density 和 smoothness 的组合推导不使用错误的 ρ 上界，按现有完整 proof-review 保留。对独立集质量至少 α，heavy 块之间有至少 α²/64 的约束；上述 (T) 保下至少 α²/128 的 heavy-good ID。修正后的 Lemma 5.14 和影响比较给每条此类 ID 至少
\[
\tau_h^2\gamma_h^2/(16r_h)
\]
的解码满足率，所以该层对值至少 α²τ_h²γ_h²/(2048r_h)>ζ，矛盾。抽标签只看每个顶点自己的影响，不看 incident ID；源约束不能因同端点而去重。

真实测试分布未变：未改坐标的 Y/Z 相反，改位则同时为 -X，故一致 dictator 染色无同色超边。每个 fiber 至少四位而至多改一位，所以 y≠z；x 位于另一层，超边确有三个不同顶点。权 (2^{-K_l}/(Ln_l)) 的完整整数 cloud 展开精确保最大独立集比例及二着色。所有解析常数独立于 long-code 维数且先于源字母表固定；固定阈值后显式规模仍为输入的固定次幂。

因此修正后仍得到第一节整条硬度，两个共同前提保一条 ALL；无需新增开放前提。

## 六、精确来源与本次范围

- KS14 冻结文件：`map/edges/unrelated-machines-3a-3a-19cf10a88593d40b/khot-saket-1308.3247v2.pdf`，SHA256 `2dcb03c6bc10dda5503452719c74bb57c5463e8b34bdbef5d06463cb7d74dc24`。定义及原误式见物理19／印18页；调用见物理22／印21、物理25／印24与后一页解码。
- FMW 冻结文件：`archives/unrelated-machines/tools/evidence/retired-literature-four-to-one-20261031/fei_minzer_wang.pdf`，SHA256 `48baa160d5d15e61aaf99b24b6fc15518c20f204d165fc96de1251d9d8a82ea0`。Corollary 1.10 原句见物理／印6页。
- 完整组合接口：`map/edges/boss5-mz-visual-repair-9fa9ce8a7e4a75ec/proof-review.md`，SHA256 `87b2cf6a26b8bfc7e440f6701d6969a25e8726c239e964c86b88a19ebf705868`。其中 KS14 参数调用由本页第四节明确覆盖；其余有效数学保留。
- 独立完整3D报告 SHA256 `840122245088d22a67f600e422fa8b62857d3d7bd3d38cb7bd0fc037402cacb1`；独立相关量报告 SHA256 `0904e459616d1549c478371a00315ca6853d420cd95a6b636f0872962d80dae3`。

Root 另目读上述物理19、22、25页，独立复算条件期望、Fourier 特征值、支撑图连通性、阈值分离和固定参数顺序。本次没有重跑旧科学程序，也没有把结构检查当作数学证据。
