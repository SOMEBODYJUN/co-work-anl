# 仿射线 tuple-group / global-dummy：正式statement与作者Proof读后 v1

审查者：rank_deficiency_fee，2026-10-18。获准后实际全文读取本轮正式statement及root作者Proof，另冻读后；未改原独立记录或其它原件，未写仓库、Work或Git。

## 1. 实际路由与读取对象

正式ID：`UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1`。

实际全文读取：

* `/workspace/scratch/038d9dcc4cac/affine_line_tuple_groups_global_dummy_statement_v1.md`，SHA256 `bfaea112b1c005cd64a32233170cf3ffb27db9cd41cdb2e150f29a8002f567b6`。
* `/workspace/scratch/038d9dcc4cac/affine_line_tuple_groups_global_dummy_proof_v1.md`，SHA256 `9f1b98b2446cdeb4eb5877328ab0fdf9d07314bc8aec6017de08c489f988a804`。

先行独立记录：`affine_line_tuple_groups_global_dummy_rank_exact_first_review_v1.md`，SHA256 `e8eed1514605e6f39a277172efd4a3e4b9bbed4e139810a292e7d3d04d6c0a14`，本次重新核hash未变。

**时间/输入顺序如实保留：** 先行独立重构的输入是root消息中的完整精确陈述及公开current第1–27行source定义；当时正式statement文件尚未冻结，作者Proof也未给本审查者。不得倒称先行记录已读过本轮statement。Root实际读先行记录后才正式冻结这两文件，本轮才由本审查者读取。

## 2. 正式statement与先行重构的一致性

对象相同：primeR≥2、k≥1，变量relation-degree≤R、每变量incidence注入j_x，tag分离的仿射线资源，A_g可空；每allowed indexed tuple独立group。n=Σ|A_g|、m₀非空表数、1≤q≤m₀、d=n−q、D=kR。每group恰一个原D-set state及d个global dummy singleton states，全部state jobs都存在，资源unit、selector1、原private1/D、dummy private1，所有state质量1。

正式statement没有扩大成任意tuple-group或任意guard桥；它陈述此特定dummy计数/归一化compiler的全原jobs≤3/2实际构造，以及unit iff原full-set packing≥q。与独立记录的域及两结论相同。

## 3. 作者Proof逐项核查

1. **Finder与line不变量。** 作者任取q个不同非空relations，各表首项，故不输入源assignment/full-set matching/OPT。只有这q个groups采用原state；任意其子族F中每变量r_x≤R、intercepts不同，保障line不重合。没有在全部n个tuple groups上错误套原degree≤R。

2. **全部Hall子族。** 同slope不同intercept平行、异slope一交，Bonferroni给r_xR−C(r_x,2)≥r_x(R+1)/2。按tag求和得|N(F)|≥k(R+1)|F|/2≥ceil(kR/2)|F|，含oddD、F空、r_x=0。整数容量Hall给每group恰b=ceil(D/2)真实不交资源，而非只检查全体union；构造不用枚举F。

3. **全部原jobs的共同实际上界。** 其余d个groups与d枚globaldummy双射。Selected real只外送b件，selected dummy外送唯一incidence；所有其它state的全部incidences留原private。Selected real负载2−b/D，selected dummy及所有unselected private≤1；U/dummy资源各至多一unit。没有省略未选state jobs、复制dummy或混用各机不同见证。

4. **任意unit actual提取。** Selector1占其selected private，该state每件private时间严格正，因此全部必须外送；资源unit容量1使selected dummy groups≤d，故≥q个原full states全量不交。Unselected exports只占资源，不破坏提取。反向q个原full不交sets加其余dummy双射确给完整unit。此是存在性等价，不声称≤3/2算法求出unit解。

5. **q=n与空relations。** q=n推d=0及n=m₀，各非空表一tuple，Hall与全原job回填无需dummy也有效。空relations不生成groups；m₀仅作本候选域与选择数量，不偷改primary value分母或near-perfect promise。q>m₀、m₀=0域外，未虚构处理。域内q≥1保证n≥1；所有selectors/incidences都有finite端，完整UM有正机器数。

6. **精确规模与位长。** Private n(d+1)，resources vR²+d，jobs n(D+d+1)，finite n(2D+3d+1)，dense乘积与statement一致。选q表首项、显式line枚举、qD边flow、qb≤nD slots、dummy双射及所有原job输出均按完整显式编码长多项式。没有对binaryR承诺poly(logR)生成vR²资源；固定sourcek,R时才直接为原source-polynomial。私有时间1/D位长O(logD)，不按更大分母或未知OPT数值展开。

## 4. 结论与认证边界

正式statement和完整作者Proof与先行消息Exact-first重构相合；本次未发现standing fatal objection。可按正式ID记录这个具体tuple-as-group+globaldummy桥的actual≤3/2逃逸及unit等价。

本次不认证外部LST论文hardness证明或全球新颖性；标准line pair-overlap、Hall和完整flat回填已扣除。没有从full-set packing难直接导入partial-set soundness，也没有证明原set packing可容易求解。只关闭所列uniform/dummy计数compiler，仍不排其它source-to-UM桥、资源权重或真实全局guard/medium机制；near2主目标仍OPEN。
