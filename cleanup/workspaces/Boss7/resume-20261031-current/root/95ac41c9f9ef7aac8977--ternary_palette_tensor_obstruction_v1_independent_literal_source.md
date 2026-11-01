# 三叉底层调色板放大候选 v1：独立陈述先行审查

## 读取与隔离记录

仅先读新 Exact `/workspace/scratch/038d9dcc4cac/ternary_palette_tensor_obstruction_v1_exact_statement.md`，实际 SHA256 `f6166e0961307f0b69d6c67541d38cf3863be64b05c1b915caae19c108278f22`。

为核第4项实际读既有 canonical `research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md`，实际 SHA256 `9314ea1777df138b047587a391bba7ddf487ab5a3ecc94ef928425ed23e654c0`。这是此前已知的三叉源背景，不是本次新 tensor proof。冻结本稿前未读作者／shared 的新证明或询问思路。root 已在本人报告后通知将另冻 v2；本稿仍先冻结 v1 的真实独立结论，尚未读新 v2。

## 结论与实际异议

第1–3项核心数学独立闭合。第4项的非退化构件输出满足 palette 前提；但 v1 的常量分支在既有 canonical 中仅写“固定YES/NO实例”，未指定着色，不能从“合法YES”推出底层≤2色。例如高1三个叶用互异(A,B,C)是合法YES，却不满足前提。因此 v1 第4项“整个输出族（含合法常量分支）均满足”存在真实的来源／量词缺口，需要明确采用(A,B,A)／(A,A,A)常量，或相应限定。

一般 d 叉 U 的 P 定义也应明确高度≥1：若只说同深而允许高度0，则根不是 internal machine，pin 无定义。核心公式对所有高度≥1成立。

这些异议不反驳底层palette条件下的一般 tensor／纯收缩定理，不是主目标突破。

## 1. 一般着色树与实际 P 的精确等式

取任意显式满 d 叉高 H≥1树 U，d≥2；q=q(U)∈[1,d]。每个原 leaf path是rainbow1，所以q≥1。

给任意 rainbow q叉见证，把 root pin放root，见证内所有边jobs下送，所有其它原jobs父置。活跃内部机恰一incoming unit和d−q枚small，负载 `1+(d−q)/d=2−q/d`；非活跃机全d枚small负载1；见证叶色不同，外机≤1。完整所有原jobs恰安排一次，因此 OPT≤2−q/d<2。

反向给任意实际 C<2。Root pin强迫root active。每active机已含一unit incoming（root为pin），其父置small枚数≤d(C−1)，故至少

\[
 r=\lceil d(2-C)\rceil
\]

枚 outgoing jobs真实下送。按固定顺序每机取r个并递归至原深H，得满r叉子树。外机上的unitjobs最多1，因为C<2，所以所取全部叶色不同。故q≥r≥d(2−C)，即C≥2−q/d。C≥2时该下界自然成立。于是

\[
 \operatorname{OPT}(P(U))=2-q(U)/d.
\]

该等式是最优值／存在性结论，不宣称可多项式求q。给定实际σ时提取子树与给定子树时回填全部jobs均按显式P多项式。路径给所有U的完整C≤2−1/d。

## 2. 对齐 Cartesian 张量的精确 q 与 YES 值

T^[k] 的每个最后一层父节点是 k 个原最后父节点组成的有序tuple。原每个父节点至多2种叶色，所以其tuple孩子最多2^k种不同有序颜色tuple。任何满r叉rainbow子树在其每个末父下都要r个不同色孩子，故 `q(T^[k])≤2^k`。

若T有rainbow binary见证F，取F^[k]。每个父tuple有2^k个孩子，树高仍h，全部叶颜色tuple互异：相同颜色tuple逐坐标由F叶色单射推出原叶相同。因此q≥2^k，与上界合得q=2^k。以d=3^k代入前节完整P等式，YES的实际OPT恰为

\[
 2-2^k/3^k=2-(2/3)^k.
\]

这里未声称NO原谓词经张量保持；它可能产生更大rainbow branching，也不影响方法上界。

## 3. G_k 的全 k 严格单调性

任意NO张量实例都是d=3^k叉树，路径始终给实际OPT≤2−3^(−k)。所以任一YES／NO对的最大可分乘性比值≤

\[
 G_k=\frac{2-3^{-k}}{2-(2/3)^k}.
\]

令x=3^(−k)、y=(2/3)^k=2^k x，两个分母都正。交乘的分子差为

\[
 (2-x)(2-2y/3)-(2-x/3)(2-y)
 =\frac{x}{3}\bigl(2\cdot2^k-4+2^kx\bigr)>0.
\]

k=1时括号前两项相消但末项正；k≥2时前两项已正。因此G_k>G_(k+1)对所有整数k≥1成立；x,y→0给G_k→1。精确Fraction回算G1=5/4、G2=17/14、G3=53/46、G1−G2=1/28，与一般符号推导一致。故G_k≤5/4，没有靠有限样本证明单调。

若某YES族为空，比值比较按逐YES／NO实例对的陈述理解即真空；不声称空集合最大比值有定义。

## 4. 纯 k 层收缩

取k≥2、k|h，末macro父位于原深h−k，其3^k个原叶后代下方共3^(k−1)个原最后父节点，每个叶palette≤2。所以该macro父的全部children最多 `2·3^(k−1)` 种颜色。任何rainbow满r宏子树必须在每个末macro父选择r个不同色孩子，故q≤该数。

`2·3^(k−1)<3^k−1` 等价于3^(k−1)>1，正好由k≥2保证。h=k的单macro层也成立。未涉及k∤h的尾层、非对齐收缩、重着色、跨副本边或padding，因此不能把结论升级到这些操作。

## 5. 既有 SAT 输出的末层 palette 核查

v1的Rigid高1是(A,B,A)，只有2色；高≥2的Rigid最后父仍是递归高1模板。Dead的底层全同色。Atom为高1 Rigid。AND／Pad接的是高度≥1的子树，OR接高度≥2的option和filler，所以它们不新建一个三个叶都来自不同构件的末父，已有底层palette不变。非退化v1公式输出全部满足前提。

v2的bounded-multiplicity模板中，Dead每个末父三叶同一fresh色；R高1仍(A,B,A)，高≥2各接一份A/B和dead。Atom、AND／OR／Pad同样保持已有末层palette。v2最后明确常量YES (A,B,A)、NO(A,A,A)，所以连常量都满足。

v1的常量“fixed YES/NO”没有在该现行文字中指定，不能静默用v2常量填入v1的历史定义。应明确约定／收紧当前方法候选的适用输出族，不倒改旧冻结字节。任意合法YES如(A,B,C)的例子说明该缺口实质涉及前提，不只是排版。

## 6. 输出大小与退化

令N=|V(T)|，tensor深ell的节点数为3^(kell)，所以总节点数Σ_ell3^(kell)≤N^k。颜色是有序k-tuple，不能当无序多重集或直接无分隔拼接；可用定长重编号后tuple编码，长度按k及原色ID位长计。d=3^k的binary位长O(k)。显式P有每边job加pin，机器为内部节点及distinct色resource，稀疏资格数线性于expanded树；dense矩阵仍为expanded规模多项式。

因此本定理允许巨大展开但不保证只按binary k或原N多项式输出。固定k时tensor是原规模多项式；变参k时不能把N^k隐藏进bit复杂度。纯收缩的macro节点／边由原显式树按k层后代给出，规模不超原树，k|h且k≥2保证macro高度≥1。

k1恢复原树和G1=5/4；h1的tensor末层证明仍正确，而纯k收缩无合域k≥2。全同色NO、颜色ID可为任意binary字符串、q1、q=d边界均不破一般P等式。所有jobs有finite端，pin保证非零OPT。

## Status

v1陈述先行独立重构完成；一般数学1–3成立；第4项v1常量输出的声明需要上述真实范围修正，U高度应明示≥1。未读新作者proof，未认证hardness放大或新颖性；没有新通用实现。UM-TARGET-v1仍OPEN。
