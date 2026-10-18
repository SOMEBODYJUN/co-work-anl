# 均匀定基数first/pair证书：递归显式列与基本解证明

2026-10-18，boss11。对应另冻Exact，尚待只据Exact的独立构造；不称新颖性。

令v(A)列为(1,所有1_r(A),所有1_r(A)1_s(A),r<s)，维D_d=1+d+binom(d,2)。目标b_(d,h)恰为均匀h-subset的列均值，其first/pair是Exact所给有理数。d=1直接输出空集或单标签，d0递归块可省去；h0/hd亦可直接唯一集合。

递归把[d]分成a=floor(d/2)、b=d−a两个非空块。对子块的全部合法大小u分别递归生成稀疏列集合S_(a,u)和S_(b,h−u)。对max(0,h−b)<=u<=min(a,h)，将每个A∈S_(a,u)、B∈S_(b,h−u)的并A∪B列出作为父候选。每个父列恰有h个标签。每个子支持≤D_a,D_b，故父列数≤(d+1)D_aD_b=O(d^5)，无需枚举全部h-subsets。

父候选列的非负包络包含目标b_(d,h)。证据只用于数学可行性：取u的超几何权binom(a,u)binom(b,h−u)/binom(d,h)，再在左右子支持按其权独立选取。每个子分布具有正确first/pair，故给定u时左右内部单/双边际及跨块pair均与“左右分别均匀给定大小、独立选择”的first/pair相同。对u混合后就是均匀h-subset的first/pair。这个见证不需要作为算法输入列出，不用任何原全slice最优化。

对已显式生成的O(d^5)个0/1父列，解普通有理可行LP：Σα_A v(A)=b_(d,h), α>=0。取一个基本可行解，则正列数≤rank<=D_d，输出它们及α。可先用任意标准deterministic rational LP得解，再用有理nullspace沿可行线消列至独立列；或者直接请求标准basic解算法。所有矩阵entry为0/1，目标分母整除d(d−1)，基本权的determinant位数O(D_d log D_d+log d)，总位长poly(d)，不随递归中间概率连乘爆长。

算法同时计算递归树每块的全部大小0..块长，缓存每个块/大小。层分块固定，块总数O(d)，块大小状态总数O(d log d)（粗O(d²)也够）；各状态至多poly(d)候选和LP维数，故总次数为绝对poly(d)。每子集合用长度d bitset，构造并/候选去重也poly。正确性按d强归纳。此为显式列生成与已知可行目标的普通LP，不是NP难的quadratic pricing/separation oracle。

七态应用时只将K_v六个uniform-cardinality类别逐个改成这组first/pair等价support；C在类别内固定，所以C、CH及所有Y first/pair保留，每个子集的H固定故rowload完全不变。整体支持≤6D_d并保有理权。u、z为单job Bernoulli。原L仍严格采用原uniform law生成所有degree<=6矩与globalq证明，不能把新rowCFG稀疏law当另一共同L，也不声称保uniform slice三阶矩。无软件执行/全球新颖性认证，主目标正反面OPEN。
