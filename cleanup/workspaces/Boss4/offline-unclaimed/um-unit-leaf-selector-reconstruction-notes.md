# unit5 认领前的比较推导笔记

仅据前批已全文读的dce主稿和本地四源审查；未读其余新原件、未执行任何程序、不作完成声明。待claim/READY后核原字节与全部独有内容。

## 固定高度真实叶流

原类：每变量两棵满k叉深h私有树，k,h≥1；内部机器、两根selector时间1，内部边父1/k子1，叶父1/k或其clause任一unit1，A_c非负整数；无pins额外资格，所有变量必选，所有叶地址显式。非空1≤OPT≤2；空变量必须先旁路，不能先算可能巨大的k^h。A_c可二进制，只用min(A_c,d_c)台unit，输出全原任务σ、其余原机器0负载语义。

流忽略轨/祖先但不更改叶身份：source→变量容量b→每原叶容量1→clause→sink容量A_c，共需b|V|流。二分最大整数b∈[0,2N]，N=k^h；每个叶仍有原轨和地址。C<2真实σ给每变量至少一条selector到外部unit的根叶路径，故b0必OPT2，父置达2。

b≥1，每变量在流中较多的一轨≥m=ceil(b/2)叶；保这轨已有外部注入，删其余，不再另求容量。令q=floor((N−m)^(1/h)), rhat=k−q。叶命中可独立重建：r-free marked集合最大M_h=(r−1)k^(h−1)+(k−r+1)M_(h−1)=k^h−(k−r+1)^h，M_0=0。m>N−(q+1)^h故含rhat正规子树，DP以≥rhat好孩子提取。全外部注入仍是原flow的子集，单位容量无冲突。其余原任务父置，负载≤2−rhat/k。

实际OPT<2时正规形有某整数r*，OPT=2−r*/k，且b≥r*^h。x=r*/k, f=(1−x^h/2)^(1/h), c=2^(−1/h)，rhat/k≥1−f，ratio≤(1+f)/(2−x)。f≥c、−f'≤c；导数分子≥1−c+cx>0，x1端ratio1+c。算法只算整数根/流/DP，不算c。h1单独无奇异导数，k1路径兼容；固定H给统一<2，无界h分析趋2而非原UM已解。

## 完整YES见证重组

给同P的p≥1完整σ^t，全部机器≤1；每变量指定轨至少在一见证中被selector采用，非空N≥p。被采用根已有incoming1，所有正small被迫下传，递归整轨N叶均外送。因此指定轨在每clause总叶数d_c*≤pA_c，只针对指定轨，不对从未采用轨作全局密度假设。

另一轨全parent，最终负载1；仅指定轨建槽。k≥p取r=floor(k/p)，x0=1，x_l=(r−1+x_(l−1))/k，row总分数任务数incoming+k(1−outgoing)=k−r+1整数。incoming先放首槽；一次全局Hall匹配覆盖所有原任务，收到incoming的行至多L−1 small，峰≤2−r/k；没收到incoming的行≤1。k>1递推从1降向(r−1)/(k−1)，x_h≤r/k≤1/p；故clause总外质量≤A_c。k<p但N≥p取r1，x_h=1/N≤1/p。k1N1≥p只容p1，直接原YES。k≥p有k≤pr+p−1≤(2p−1)r，故统一2−1/(2p−1)。N<p需反例保留，不能默认删除。

锐：p变量k2p−1,h1，正轨同shared clause容量k，负轨各private容量k。第i完整YES仅i正其余负，真实C1。指定全正，低于2−1/k迫每根外≥2，共需2p>k unit；每变量外1叶可达2−1/k。锐的是指定模式最优值，整个P仍OPT1。p2 k3为5/3；不能当一般近二困难性。NO输出若没完整YES，不在本合同域。

## 取源后必须确认

- 两code是否复用builder/load core，canonical/independent与root记录互相独立到哪层；不能按文件数叫全栈独立。
- f973既有总JSON只依赖：核leaf_flow43dbf6…和selector dd c771…完整hash与实际exit0记录；只有同hash真成功才复用，不把摘要passed等同新执行。
- 主源码完整CLI/输入/原子输出、sharp_profiles所有案例/矩阵/YES/指定模式、异常/空/二进制大容量边界均需实读。
- 按原数据保实际范围：既有四源审查声称leaf-flow7实际调度、selector7调度361任务等；未读f973原件前不沿用为本批核验结论。
