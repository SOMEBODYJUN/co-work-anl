# 三叉底层调色板放大候选 v2：陈述先行范围修正复核

本稿只读新 v2 Exact，尚未读作者／shared 新 proof。不是对 v1 内容的零信息再发现；独立数学已在 v1 Exact-first 稿中自行闭合，v1 的真实异议记录保留不改。

- 新 Exact：`/workspace/scratch/038d9dcc4cac/ternary_palette_tensor_obstruction_v2_exact_statement.md`。
- 实际 SHA256：`11ead3e74a0d9309174d2ad3dee16a1b30b1691ee03b0493635656f7bd8940df`。
- 原独立稿：`/workspace/scratch/038d9dcc4cac/ternary_palette_tensor_obstruction_v1_statement_first_review_literal.md`，SHA256 `fb59cbb90a782f7e8b7452a6046e89f6b12689431ba0779014f8fead74016cc2`。
- 为核输出palette曾实读旧三叉 canonical，SHA256 `9314ea1777df138b047587a391bba7ddf487ab5a3ecc94ef928425ed23e654c0`。

v2 正确收紧了第4项：先限两套已明示的非退化 SAT 构件；对常量明确规范采用高1(A,B,A)／(A,A,A)，其中选择A≠B（例如binary ID 0、1）。这两个合法常量各自底层2色／1色。因此新的整个**规范输出族**确实满足前提；不再声称未指定的任意合法常量YES都满足。原 v1 的来源／量词异议已关闭，不倒称其原字节陈述成立。

v2 另明确一般 U 的高度H≥1，pin machine存在，原高度0定义缺口关闭。所有其它数学保持 v1 已独立证明内容：

1. 对齐张量的每末父palette≤2^k；给定rainbow binary F，其对齐积F^[k]为rainbow满2^k子树，所以YES精确q=2^k。
2. 任意高度≥1的完整d叉U，给q见证可回填全部原jobs得到2−q/d；任意actual C<2可抽出ceil[d(2−C)]叉rainbow，故真实OPT=2−q/d。路径给所有U的2−1/d上界。
3. 比值G_k交乘差为 `(3^(−k)/3)[2·2^k−4+2^k3^(−k)]`，所有k≥1严格正；G1=5/4，极限1。无需假定NO原谓词经张量保持。
4. 纯k层收缩的末macro父只含3^(k−1)份原末palette，因此q≤2·3^(k−1)<3^k−1（k≥2）；k|h使宏高度≥1。
5. 两套非退化编译器的Rigid／Dead底层都≤2色，AND／OR／Pad不新增越过构件的叶层父节点，规范常量如上。这里只认证该结构前提，不重审其整个SAT困难性证明。
6. Tensor节点数≤|T|^k；颜色有序tuple编码和time1/3^k位长须计入显式输出。无按binary k的多项式输出承诺，允许巨大展开不改变等式。P给所有原边jobs有限端，未删inactive jobs。

结论：v2 四项均独立闭合，无standing fatal；v1已报告异议经准确新域修正关闭。范围严格限对齐Cartesian tuple与纯均匀k层收缩，不推出所有改色／padding／跨副本归约失败。无代码、新有限审计、新颖性或一般UM结论认证；作者proof仍未读。
