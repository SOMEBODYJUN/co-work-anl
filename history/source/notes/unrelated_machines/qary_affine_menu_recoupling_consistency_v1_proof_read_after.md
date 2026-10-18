# q 元 affine 菜单：作者 Proof v1 实际全文读后

审查 ID：`UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1`。

日期：2026-10-18。本记录是首次实际读取作者 Proof_v1 后另行冻结，未改此前 Exact-only 独立记录。作者 Proof、Exact 和旧独立记录保持原字节。

## 实际读取的固定文件

- 作者 Proof：`/workspace/scratch/038d9dcc4cac/qary_affine_menu_recoupling_consistency_proof_v1.md`，6,160 bytes，SHA256 `bc9aa19019bb8466932192253ff148824589aedfc587061df64f016f6bb8461d`。
- 对应 Exact：`qary_affine_menu_recoupling_consistency_exact_v1.md`，SHA256 `9d5d0cebf3daa9c78217d32e95f71b80696cd4732f442a22beaf8b22ef50dbd6`。
- 此前独立记录：`qary_affine_menu_recoupling_consistency_v1_independent_review.md`，SHA256 `cdd8fcbe71dd9b2d282871b71f9be15321d14d5bca624a1efeb677da411575df`。

后两个文件同在 `/workspace/scratch/038d9dcc4cac/`。Proof hash 在全文读取前实际核对；另两个 hash 在本记录冻结时复核。

## 结论

**PASS；作者全文证明与此前独立推导一致，没有新增 standing fatal。** 需要保留的范围条件、floor/ceil、原 jobs 和全局 partial matching 均正确。没有要求修改作者 Proof 或源 Exact。

作者第4节以一维 concurrent lines 的 fractional allocation tensor 作为普通二分图 fractional-flow 证书，再依整数容量获得真正的全局 partial subsets。独立记录用一般 affine map 的统一 fiber/Hall 公式证明同一下界。这是两个一致的具体论证，不是把 tensor fractional 证书误当成最终必须 product 的整数输出。

## 逐节实际核对

| 作者节 | 读后结果 |
|---|---|
| 1. 全部 affine union 上界 | 对固定 a 的映射确为 `g -> (A-diag(a))g+c`。不同 a 的资源块互异。det 关于末坐标的系数有非零最高全乘积项，有限网格归纳给至少 `(q-1)^(t-1)` 个 singular a。每个亏损至少 `q^t-q^(t-1)`，正确得到所有 A,c 的整数配额上界。 |
| 2. cyclic 达到 | 核递推 `delta_(i+1)=a_i delta_i` 给原方程中的乘积条件 `prod a_i=1`；作者明确区分加号写法须经 `a -> -a`。singular 层的图左度 L、右度 q，整数 b-matching 给每组 `floor(L/q)`，与 floor/ceil 公式一致。没有完全扔掉 singular 层。 |
| 3. 任意 coordinatewise functions 上界 | 所有一维 q 条不同斜率线都被覆盖，包括 nonlinear f_i。每维 union 上界及全部 groups 为 Cartesian 全 tuple 给真正的 union product。只限制 selector 域，不限制 B_g 为 product。 |
| 4. concurrent 下界 | 独有点权 1、公共点权 `1/q` 是合法一维 fractional allocation。tensor 后每组质量 alpha^t，每个真实资源总负载至多 1。缩放到整数配额 floor(alpha^t) 后，普通整数 maxflow 给合法不交 subsets。缩放系数至多 1、每边权至多 1，容量方向正确。 |
| 5. 全部原 jobs / 反向提取 | 正向只 export 选中 states 的领取 jobs，所有其它 jobs 含未选 states 的全部 incidence 留在原 private；负载完整核算。反向对任意 C<2 的完整调度提取所选 state 实际 exports，即使其它 states 也 export，所提集合仍互斥。C>=2 的下界平凡成立。 |
| 6. 极限和 explicit complexity | 固定 q 的 cyclic 缺项趋零、coordinatewise 上界指数衰减，足以否定限定 repair 合同的存在性。全部规模按显式原实例计，不按 t、log q 的简短参数计。没有 q>2 全 nonlinear、general UM 或 hardness 升级。 |

## 关键端点与符号

1. `t=1` 时循环矩阵是 `[1]`，空 prefix/minor 的 determinant 是 1，singular a 恰为 a=1。作者的计数 L=1、singular 配额 floor(1/q)=0 均有效。
2. `q=2,t=1` 得全部三个域的 V=1/2、实际峰 3/2。场中的负号退化不会改变原方程的正确核递推。
3. 对任意 characteristic，cyclic 的核递推只给一个自由坐标，因此 singular 时核维数恰为 1；不需要 characteristic 不整除 t，也不需要循环矩阵可对角化。
4. ceil 和 floor 只作用于普通有理数配额。`q^t-L+floor(L/q)=q^t-ceil((q-1)^t/q)` 没有在场中取整。
5. 作者第4节取 tensor 的对象是 fractional edge weights，而非最终领取集合；整数 flow 允许完全自由的全局 partial allocation。

Exact 提到 q=2 的已知无约束 nonlinear 数值。作者本 Proof 主要证明 cyclic/affine/coordinatewise 三域，并不重写那个旧二元结果；此前独立记录第6节已经用逐坐标互异的两组支持必相交，补给自足的 q=2 无约束上界。因此这一背景句与已核结论一致。q>2 同一两组交叉只给较弱的 `1-1/q^t` 上界，不被当成 affine 精确式的 nonlinear 推广。

## 全原矩阵、输出与实验归属

令 n=q^t。真实普通 P 有 `2n^2` machines、`n^3+n` jobs；finite 条目 `2n^3+n^2`；dense 条目 `2n^2(n^3+n)`。private rational 为 1/n，位长 `O(log n)`。达到式子的 selector 不需枚举所有 A 或所有函数：cyclic 与所有 f_i=0 已给明确见证。全局 flow 图只涉及显式 resources/incidences；最终逐个输出所有原 jobs 的机器，不把 fractional certificate 当成输出。

此前 1,504 矩阵、24,664 rank 计算、3,412 一维函数的有限辅助核验，由本独立 reviewer 在 Exact-only 阶段执行。它们不被记作 root 亲自运行，不被记作作者 Proof 的必要步骤，也不代替任意 q,t 的完整论证。本次没有继续作局部参数扫描。

## 下一阶段的真实 source 边界

本家族普通 P 本身允许 cyclic recoupling 的高值实际调度；coordinatewise 限制不是 P 的物理约束。因此其差距定位的是一个必须付费实现的全局一致性义务，不能直接拿 C_sep 充当 ordinary-P 的 NO 下界。

真实 source/compiler 若要用 coordinatewise soundness，必须在其**实际 jobs、eligibilities 或共享资源**内迫使相应 selector 函数关系，并证明任意低峰完整调度能被解码；不能先让 unconstrained state copies 任意选择，再假设常数保值事后修复。这里已否定的正是该 repair 合同，尚未给出一个物理一致性 compiler 或 hardness source。

本次后续数学工作应转向具体 primary source 的全局选择/一致性结构及真实 ordinary-UM 编译，不再以本家族局部 q,t 数值作为新证据。没有新增 general-UM 算法、硬度、新颖性、外审或实现认证。
