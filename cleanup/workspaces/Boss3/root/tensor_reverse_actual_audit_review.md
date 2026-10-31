# Cartesian tensor 反向放大：独立 actual sparse-P audit

分类：**audit_only**。本记录及有限运行不替代任意 t 的一般证明，不认证任意其它 tensor/source/compiler。

## 1. 读取与隔离

先实际全文读取 `normalized_flat_cartesian_tensor_reverse_amplification_exact_v1.md`，核 SHA-256：`60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac`。

未读取作者 Proof。root 明确提供并授权使用见证 ell_i(g)=g_(i+1) 循环，选中 state 只导出 a≠allones 的 incidence；其余全部原 incidence 留 private。本 audit 使用该见证，不冒称独立发现它。

仅写 scratch；未改 repo、Work、Git。

## 2. 冻结代码与运行方式

代码：`audit_normalized_flat_cartesian_tensor_reverse_amplification.py`。

代码 SHA-256：`efa03ab9bc976f899e7a1b9bd7af6a96a68ef76c18decbbb7e31921eb18d262c`。

运行必须显式给全新目录，例如：

    python audit_normalized_flat_cartesian_tensor_reverse_amplification.py --output-dir /absolute/fresh/output_dir

目录用 mkdir(exist_ok=False)，每个文件用 open('x')。实际再次指向旧输出目录时得到 FileExistsError，旧 manifest hash 保持不变；未覆盖冻结结果。

本次冻结目录：`tensor_reverse_audit_run_v1/`。其中 manifest SHA-256：`f5814519643ca0f56d8b735a068f7f11a30808827b5c4ba8c7ad393165091c59`；summary SHA-256：`2341a19f7c59c410db5b5090efa0c31f987662f4060c9bcc7acfb87a8669cbd9`。

## 3. 具体输入矩阵与全 job 输出

对每 t=1,2,3,4 独立枚举全部资源 tuples U^t。支持由实际检查 b_i+g_i a_i=ell_i (mod 2) 筛得，未从 witness exports 倒造支持。

输出 `tN_sparse_P.json` 包含全部 resource/private machines、全部 selectors、**每个 indexed state 的全部 incidence jobs**，以及每 job 的全部 finite processing entries；其它全部时间显式约定 infinity。每 resource tuple 只有一个全局 R_u ID，不按 incidence 私有化。t=1 的四个 base supports 另外对照 Exact 的硬编码集合检查。

时间统一为整数单位 1/D，D=2^t：private incidence=1 unit，selector/resource= D units。无浮点输入、计算或输出；每个 JSON 值写出前还检查未混入 float。

输出 `tN_all_original_job_schedule.json` 包含每枚原 job 的唯一目的机、处理时长、开始及结束整数时刻，以及全部机器（包括 idle machines）的回算负载。checker 逐条读取实际 sparse P 行核资格、原 processing time、job ID 恰一次、时间区间与机器不重叠、全机峰和所有原 job 计数。

选中 state 恰留一个 a=allones 的原 incidence，故负载 D+1；未选 state 的 D 枚 incidences 全私有，负载 D；每个被使用 resource 恰一枚 unit，负载 D。所有 selector 和未选 state jobs 均真实执行。

## 4. 全互补 pair 与仅 t1 完整优化

`tN_all_complementary_intersections.json` 枚举**全部有序** g、complement(g)、ell、ell'，共 D³ 条；反向的同一 unordered group pair 也保留，因此对应 D³/2 个 unordered state pairs。每条从实际 P 支持取集合交，要求恰一个真实 resource，并与独立坐标解 a_i=ell_i xor ell'_i、b_i=ell_i xor g_i a_i 比较。

只有 t=1 调用 `exhaustive_t1_actual_opt`：从完整 ordinary P 的每 job 全 finite row 取 Cartesian product，共 1024 个完整 assignments，直接逐机加原处理时间求峰，不使用 V 身份、部分资源 allocation 或后端 oracle。结果 exact OPT=3 units /2，即 3/2。

该函数对 t≠1 有硬拒绝；main 在 t=2,3,4 从未调用 brute。t≥2 只检查给定 all-jobs witness 与全部互补 pair，不执行寻找 optimum 的枚举。

## 5. 实际结果

| t | groups | state/private | resource | 原 jobs | finite entries | D | 实际峰 units | ordered complementary pairs |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 4 | 10 | 20 | 2 | 3 | 8 |
| 2 | 4 | 16 | 16 | 68 | 144 | 4 | 5 | 64 |
| 3 | 8 | 64 | 64 | 520 | 1088 | 8 | 9 | 512 |
| 4 | 16 | 256 | 256 | 4112 | 8448 | 16 | 17 | 4096 |

逐 group exports 数为 1、3、7、15；总用 resource 数为 2、12、56、240，unused 为 2、4、8、16。每原 job 均在原有限端执行一次，所有时刻和资格检查通过。

精确规模检查为：groups D、states D²、resource machines D²、private machines D²、incidences D³、selectors D、finite entries 2D³+D²。dense 若物化分别有 80、2176、66560、2105344 项；本 audit 保持 sparse 表，不把未写出的 dense 项计成 finite。

t1 完整优化输出 `t1_full_original_opt_enumeration.json`，SHA-256 `4672a50ee41dde141dcc36519f92d066f85fdd7fe2efc568724e0ef4fb550c18`；含 1024 assignment 计数、peak histogram 和一份最优原 assignment。其余全部具体输入、schedule、交点证书的逐文件 hash 均在 manifest。

## 6. 准确结论与局限

列明四个有限显式实例的 all-jobs 上界见证、资源一致性、资格、互补交点及规模 checks 通过；t1 的完整实际最优值独立穷举为 3/2。输出的 witness mass 为 (D-1)/D、实际峰为 (D+1)/D。

没有据此把有限 t=1..4 运行冒称全部整数 t 的证明；没有优化 t≥2，没有作者 Proof 认证，没有任何其它 product 或 source hardness 结论。构造/检验的规模按显式 matrix 输出收费，不能说 polynomial in t。
