# q元 affine 菜单 recoupling/坐标一致性：作者 Proof v1

对应 `UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1`，Exact SHA256 9d5d0cebf3daa9c78217d32e95f71b80696cd4732f442a22beaf8b22ef50dbd6。先冻Exact再写本Proof；未主动发给仍在Exact-only阶段的reviewer。对象与全部original jobs以Exact为准。

## 1. 任意 affine 选择的资源union上界

固定ℓ(g)=Ag+c。对固定a，可能被这些states领取的b集合正是映射

g↦(A−diag(a))g+c

的image，大小q^rank(A−diag(a))。不同a是不同resource blocks，故整个selected-state资源union大小Z为这些image大小的和。若每group都领取至少m项，q^t m≤Z。

需要如下有限网格事实：r变元、每变量次数≤1、最高乘积项系数非零的多项式，在F_q^r上至少(q−1)^r个非零点。r0时非零常数有1个点；归纳将最后一变量写成x_r h+h0，h最高乘积系数非零，至少(q−1)^(r−1)个前缀使h≠0，每个前缀至少q−1个x_r使整个式非零，结论成立。

det(A−diag(a))关于a_t的系数，是前t−1变量中最高乘积系数为±1的multiaffine多项式。因此至少L=(q−1)^(t−1)个前缀使此系数非零；对每个前缀，有唯一a_t令行列式为0。t1时前缀是唯一空tuple，仍给L1。故至少L个a使rank≤t−1，其余rank≤t，从而

Z≤q^(2t)−L(q^t−q^(t−1))
 =q^(2t)−q^(t−1)(q−1)^t。

因此m≤q^t−ceil((q−1)^t/q)，对任意A,c成立。

## 2. Cyclic选择达到该整数上界

固定ℓ_i(g)=g_(i+1)。固定a的kernel递推为δ_(i+1)=a_iδ_i，故非零kernel存在当且仅当Π_i a_i=1；所有这些a_i必非零。奇异a恰L=(q−1)^(t−1)个，此时kernel恰一维、rankt−1；其它a映射可逆。符号严格按实际方程b+g*a=ℓ：这里是P−diag(a)。若改写P+diag(a)，经a→−a才得到Πa_i=(−1)^t；不能在原方程直接混用。

对每个非奇异a，每g对应的resource只有这一个g能用，全部给它。每g先领取q^t−L项。

再看奇异a的resources。建立二部图：左为全部q^t个groups，右为所有奇异a下实际出现在image内的resources；g连到它在该a下唯一对应的resource。每左degree恰L，每右degree恰q。令d=floor(L/q)。任意左侧X的邻集大小至少L|X|/q≥d|X|，所以整数b-matching可以给每g再分d个不同右resources。d0时直接不领奇异项。

每group总领取q^t−L+floor(L/q)=q^t−ceil((q−1)L/q)=q^t−ceil((q−1)^t/q)。结合第1节，V_cyc=V_aff，精确为Exact所列式。没有只丢掉所有奇异a，也没有假设不同g最终领取的a集合相同。

## 3. 任意 coordinatewise 函数的上界

若ℓ_i(g)=f_i(g_i)，第i坐标的selected lines是q条不同斜率的线

L_(r,f_i(r))={(a_i,b_i):b_i+r a_i=f_i(r)}，r∈F_q。

首条有q点；每条后来线至少与首条交一点，所以它对已有union最多新增q−1点。因此该坐标的union大小≤q+(q−1)^2=q²−q+1。

由于groups确实包含全部tuple g，第t维完整selected-state union正好是这些一维line unions的Cartesian积，而不只包含于该积。故其大小≤(q²−q+1)^t。任意partial allocation若每group至少m项，必q^t m≤此union，得到

m≤floor((q²−q+1)^t/q^t)=floor((q−1+1/q)^t)。

此上界没有要求B_g是Cartesian积，也没有声称每个固定非affine f都能达到它。

## 4. Concurrent coordinatewise 函数达到整数上界

取每个f_i≡0。每坐标q条线共同经过(a,b)=(0,0)，其它各线的q−1点只属于自己这条线。给单坐标的每条线分配如下fractional资源：独有点各1、共同点1/q。每条线共得α=q−1+1/q，每resource承受总分配≤1。

对t个坐标取上述fractional allocation的tensor乘积，只用作一个普通二部fractional matching证书：对g与其resource x=(x_i)，权为各坐标分配权的乘积。固定g的权总和为α^t；固定resource对全部g的权总和为各坐标负载之积，≤1。每边非负且≤1。

令m=floor(α^t)，把fractional flows统一乘m/α^t，即给每group整数需求m的可行fractional flow。资源容量1、group需求m的网络有整数容量，maxflow整数性输出真正不交的m项/组。于是V_sep=m/q^t，达到第3节上界。最终partial subsets可任意全局，不必取坐标subset的Cartesian积。

## 5. 全jobs实际调度与反向任意exports

对任何固定selector函数ℓ及其B_g，把J_g放M_(g,ℓ(g))，只导出这些selected states中对应B_g的incidence jobs；其它所有incidence包括未选states的jobs全部留原private。resource因B不交至多一unit，未选state private负载1，selected private负载2−|B_g|/q^t。因此上述达到的V都给全部原jobs峰≤2−V。

反向给任意完整actual C<2，不预设未选states jobs留private。每resource至多一unit。取每J_g实际所在stateℓ(g)，其selected-state实际exports B_g跨groups不交；它的private负载是2−|B_g|/q^t≤C，故每组导出质量≥2−C。若actual selector函数在所讨论cyclic/affine/coordinatewise域，该提取仍在同一个域，因此C≥2−相应最优V。C≥2时同下界平凡成立。所有jobs仍各一次，未选state额外exports只占更多resource，不能逃过该提取。

两向给每个受限selector域的actual最优值2−V。它只是受限selector条件下的数值；普通P没有这些免费条件，不能把C_sep用作无约束OPT下界。

## 6. 常数保值修复不可能及复杂度

固定q，cyclic缺项比例≤(q−1)^t/q^(t+1)+q^(−t)→0，故V_cyc→1。另一方面V_sep≤[(q²−q+1)/q²]^t→0，因为括号严格小于1。给任意常数c>0，充分大的t使V_sep<c V_cyc，所以连存在性上都没有coordinatewise一致输出保留输入cyclic值的c倍。该结论不排其它译码目标/其它一致性。

所有图/finite资格均按Exact显式枚举；二部整数flows在q^(3t)级别的显式incidences内完成，输入有理权q^(−t)位长O(t logq)。多项式按该显式总位长而不是按t或logq单独计。标准有限域线性代数、multiaffine网格计数与整数matching只作自足重构；没有新hardness结论。
