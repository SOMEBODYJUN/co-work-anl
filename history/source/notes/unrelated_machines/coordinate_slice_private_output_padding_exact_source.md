# 坐标切片的私有输出padding：v3精确陈述增补

精确身份：`UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v3`。v1/v2均为未登记的中间冻结候选；保持原字节。v3继承v1 A–D及v2精确单位阈值（Exact hashes分别2d889e2109657bffda860acbad4ce64accd06fd207d47c96fa803647fc15b6a8、6f547983c9bdb112db07d17e0a246ea2ef57c3f72919f440c6f4141995623abf），新增下面的padding结论。只给陈述，不含证明。

输入Π是任意显式、非空、simple、平衡D-regular二部全投影游戏，D≥3、共同旧字母表Σ₀大小Q₀≥2、左右各n点、N=2n、M=DN/2。参数为二进制整数g≥2和有理0<ρ₀<ρ≤1，并假设ρ₀+2g/D≤ρ。列表总cost和边覆盖定义与v1一致。

令冲突图H顶点为原左点；两个不同左点相邻当它们有共同右邻居。按输入中的左点顺序贪心proper coloring得到χ:A→[s]，s≤D(D−1)+1。给旧字母表增加两组互异且不在旧Σ₀中的符号：一个α*，以及p₁,…,p_s。公共新字母表Σ′=Σ₀∪{α*,p₁,…,p_s}。保持图、顶点、边和邻居index。沿原边(a,b)，新投影为

π′_ab(α)=π_ab(α) 若α∈Σ₀；π′_ab(α)=p_χ(a) 若α∈Σ′\Σ₀。

Claim E：padding为统一确定性位多项式变换，Σ′大小≤Q₀+D(D−1)+2；perfect YES保留。若旧Π任意cost≤gN列表覆盖严格少于ρ₀M条边，则新Π′任意cost≤gN列表覆盖严格少于ρM条边。图仍simple、Dregular、平衡、全投影。这里不承诺每右公共投影像非空，亦不需该条件。

Claim F：将任何这样的Π′输入v1明确的坐标切片树/实际任务编译，不论旧Π的value如何，所有玩家均可在同一个新增状态α*获得满(D−1)-叉根子树且所选资源两两不交；完整实际P有C≤1+1/D的具体调度。

Claim G：若Π为Claim E的NO，Π′无完美赋值（g≥2、ρ≤1）；依v2的精确单位阈值，完整实际P的OPT恰1+1/D。若Π为perfect YES，Π′对应P的OPT恰1。

复杂度：padding本身关于全部显式原输入及binary参数为统一多项式；后续坐标树展开仍有D^{|Σ′|}叶，不承诺D、Q₀变化时的统一原输入poly编译。固定D、Q₀及满足条件的g,ρ₀,ρ时，s可按固定上限D(D−1)+1补空颜色，新字母表和树深有固定上限，随后展开及具体分配/σ输出对原图大小为多项式。若在这个固定参数域已经有hard源族，则padding保留所列YES/NO promise，但本文不擅自引入未核的simple hard源定理。

结论范围：源promise甚至可被一个保真padding保留，而此坐标slice硬件对所有padded源均实际低负载。没有否定一般q-allocation/其它叶排列/具有额外纤维正则条件的特殊源，也没有证明UM主目标反面。

Status：root及另一研究者已有独立推导，此文件先冻结Exact。对新E–G审查者应先独立重构，再读证明。
