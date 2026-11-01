# 23c59afb9f2a6498f7c7：two_player_collision_free_bound.py 语义处置草稿

## 来源、依赖与输出

- 来源路径：`research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/construction/two_player_collision_free_bound.py`。
- 来源 blob：`5b8711b49b0f1bd956878e9d26779986d01a7592`；SHA-256：`867f6f89eb97ab84a4098ed3fb5bd8113e3b3710a2dda2fabf7f037799e79ad3`；1945 bytes。
- 依赖只有 `Fraction`、`Path`、`json`、`numpy` 和 `scipy.optimize.linprog`；没有项目内模块。脚本在 `Path(__file__).with_suffix('.json')` 写 JSON，因此把源临时命名为 `source.py` 时输出名为 `source.json`；冻结原件的同字节输出是 `two_player_collision_free_bound.json`（blob `83e7c1877a47a52aa9356e3ca4836d8c26f7e929`，SHA-256 `b3d276debe470caa39b299fe7dafcdefe3924b832f1cc20721528bbaaa3efbdb`，1324 bytes）。
- 本批复制在 `active_batch/23c59afb9f2a6498f7c7/source.py` 和 `source.json`，两者 SHA 与冻结对象一致。

## 源码算法与精确输出

源码定义六个抽象主题 `C,D,T1,T2,R1,R2`（位 0--5），枚举 47 个非空兴趣 mask；删去同时含 `C,D` 的 mask（碰撞自由实际终局），不包含空兴趣客户。对一个 mask (v)，`u(a,b)=1_{ain v}/(1+1_{bin v})`，`unit(a)=1_{ain v}`。实际福利行是 `W=1_{C∨D}`，比较行是 `O=1_{T1∨T2}`。

LP 以客户类型质量为变量，约束 `W=1`、所有所列行非负，最大化 `O`。16 行分为：

1. `root_T1`,`root_T2`：`unit(C)-u(Tj,Rj)`；
2. `actual_last_T1/T2/R1/R2`：`unit(D)-u(a,C)`（代码循环 `a=2..5`）；
3. `BR_Rj_a`：`u(Rj,Tj)-u(a,Tj)`，每个 `j` 对六动作排除自身动作，共 10 行。

因此这是固定 `C,D,Tj,Rj` 模板的必要真回复松弛：省略了根对其它动作、末位对 `C,D` 等比较，扩大了可行域；任何满足同一固定模板的完整 SPE 类型质量仍可行，但脚本本身不枚举所有策略树。

HiGHS 浮点 LP 返回 `Optimization terminated successfully (HiGHS Status 7: Optimal)`，目标 1.25。脚本将目标、边际和原变量以 `limit_denominator(1_000_000)` 有理化，并逐 mask 做独立 Fraction 断言。冻结 JSON 的确切对偶为

- β = `5/4`；
- 非零乘子：`root_T1=3/4`、`actual_last_T2=1/4`、`actual_last_R1=3/4`、`actual_last_R2=1/4`、`BR_R1_T2=3/4`、`BR_R2_T1=1/4`；
- 对每个 47 mask 检验 βW − O − Σμ_r r ≥ 0，最小残差 `0`，24 个正残差、23 个零残差；
- 原始可行点支持四个 mask：`6={D,T1}` 权 `1/4`，`26={D,T2,R1}` 权 `1/4`，`36={T1,R2}` 权 `1/4`，`57={C,T2,R1,R2}` 权 `1/2`。它给 `W=1`、`O=5/4`；所有 16 行的 Fraction 松弛非负（根和实际末位行为 0）。

所以，**源码+输出构成了该固定 6 坐标必要约束 LP 的精确 5/4 上界和达到点**。它不是浮点数值猜测：有理化后对偶残差和原始行均再次精确断言。但是该证书只约束一个固定模板的部分 IC，不能单独提升为所有二人完整 SPE 的定理；坐标主题若在实际策略中重合，需按合并后的兴趣指标重新编码或说明提升映射，源文件没有单独处理别名量词。

## 复现与测试

在该 active batch 的源副本上运行：

- `python source.py`：HiGHS 状态 7，输出 `ratio=5/4`，Fraction 断言全部通过，生成 `source.json` 与冻结 bound JSON 同 SHA。
- `python two_player_collision_free.py`：4 主题 `A,B,C,D`、实际 `C,D`、固定 `replies[2]=D`，枚举 64 个回复表和 6 个比较对，共 384 个 LP；浮点只提出候选，最佳记录为 `replies=(B,A,D,A)`、比较 `(A,D)`、`ratio=5/4`，四种客户质量 `1/4,1/2,1/4,1/4`，逐行 Fraction 检查通过；输出 JSON SHA `8470454396d1ae7e138a08c7b01451c648bcc58c7ea7230693f9af91d329958e`。
- `python audit_two_player_overlap.py`：64 个二值 ((c,d,t_1,t_2,r_1,r_2)) 精确恒等式，残差最小 0；两个端点 `(W,I,OPT)=(4,0,5)`、`(2,2,3)`，笛卡尔积端点 `(6,2,8)`；输出 SHA `1987f247cd03167e3a8d1597a5b07f2cdc05ae5c76c862349c85d7d31285f9d5`。
- `python audit_background_two_player.py`：背景 `0,1,2,3,4,7,10,100,10^9` 各 64 个二值格，共 576 个 Fraction 恒等式检查，ψ 最小 0；输出 SHA `a8351d053b18f99ef3f02a4c7c0cc742db4cd7e846d22a74a28bc7ff03b111e3`。
- 全仓同族独立重放：`audit_collision_free_obstruction.py` 的五客户完整 SPE 20 项比较全部通过，实际 `W=4, OPT=5`、负载 `(1,1,0,1,1)`；`audit_collision_free_family.py` 的 (k=1,2,3) 分别 20、399、11110 项比较通过，给 `(W,OPT,ratio)=(4,5,5/4),(6,8,4/3),(8,11,11/8)`，每个实际客户负载至多 1。

## 全仓同族与定位

1. 同目录 `two_player_collision_free.py` / `two_player_collision_free_best.json` 是 4 主题回复表的有限 LP 搜索；它找到了上述 5/4 端点，但没有保存每个 LP 的对偶上界，不能单凭“遍历 384 次”宣称一般上界。
2. `two_player_overlap_refinement.md` 与 `audit_two_player_overlap.py/json` 给出真正全称的两人结果：对任意共同有限目录、任意完整有序历史纯 SPE（允许平局），逐客户恒等式证明
   [
   8\,OPT_2\le 10W+2I,
   qquad OPT_2\le 5W/4+I/4,
   ]
   其中 (I=|C\cap D|)；碰撞自由 (I=0) 时为 (OPT_2/W\le5/4)，两个端点及笛卡尔积说明区间锐。该解析证明比本源固定 LP 的量词更强，是本源应挂靠的正式数学对象。
3. `background_two_player_refinement.md` / `audit_background_two_player.py/json` 把最后两人放在任意整数背景中，证明比较总利润的背景税界与 `R_b(T1,T2)\le5R_b(C,D)/4+I_new/4`；只比较背景利润，不等于全终局覆盖，也不能直接累加成人数无关 half。
4. `collision_free_occupancy_obstruction.md` 及独立 review 是同一个五客户、两人、四主题精确完整 SPE：根 `C`，回复 `(B,A,D,A)`，实际 `W=4`、`OPT=5`、无实际重叠，正是 4 主题候选的整数缩放端点；它仅否定“实际无拥挤即可由可加负载函数支付 OPT”的辅助桥，`2W=8>5`，不是 half 反例。
5. `collision_free_three_halves_family.md` 及独立 review 给 (k+1) 玩家、(3k+1) 主题、(3k+2) 客户的完整 Q/B 归纳族，实际路径无重叠，比例 ((3k+2)/(2k+2)\to3/2)；(k=1) 正是上面的五客户端点。该存在族不是所有 SPE 的上界，也不反驳 half。
6. R-486 `joint_collision_free_probe.py`、`joint_collision_free_m3p6*.json` 是三人六主题的低预算完整历史 MILP 提案；均为 timeout、`floating_bound_not_a_certificate=true`，精确端点仅 `W=OPT=3` 的一个策略。R-2fc `collision_free_ratio_probe.py` 是随机固定 Markov LP 探针；这些均不能替代本源的固定 LP 对偶，也不能合并成一般结论。

## 处置建议

建议将本源及其 1324B JSON **作为现有两人碰撞自由 5/4 解析定理的 supporting computation 保留并集成**，在正式记录中明确“固定六坐标、部分 IC 的必要松弛 LP；有理对偶/原始达到 5/4”。不要把它单独登记为 Q-CAG-HALF 反例、一般人数上界或所有 SPE 搜索证书；4 主题脚本的有限枚举与 MILP/random 探针均只作候选/复核。保留源+JSON 的配对关系和本批命令输出，避免把 `ratio=5/4` 当作未加量词的全局结论。
