# 共享外端四任务环：作者 Proof v1 实际全文读后

对象：`shared_outside_four_job_query_return_cycle` 的固定 4-job/4-machine 边界例。2026-10-18，首次实际读取作者 Proof 后另冻；不改原 Exact-only 记录，不另立新 Claim。

## 实际读取与源版本

作者 Proof：`/workspace/scratch/038d9dcc4cac/shared_outside_four_job_query_return_cycle_proof_v1.md`。

字节数 4,109，实际核对 SHA256：

`43f9bbfc184b7283250b6a5930bab08fabf675c7186babe3fdd7b798ef989fc7`。

对应 Exact：`shared_outside_four_job_query_return_cycle_exact_v1.md`，SHA256 `c2f73db04495292714a6a083029b707f3c4c246647e4975f1f58bfdcaf15fe19`。

旧独立记录：`shared_outside_four_job_query_return_cycle_v1_independent_review.md`，SHA256 `d77a2e3b911b1f31ebc939fb52c14145d8994d36e82baddf4ecfaff6fb73dce1`。

后两个文件同在 scratch 根，本次再次复核未变。

## 结论

**PASS。** 作者 Proof 与原 Exact、此前独立的四布尔变量/16-assignment 分类完全一致。无新增 standing fatal，不要求修改源文件。它作为一般交换正文的一个标准 matching 边界例保留，不单立新颖性、算法或困难性 Claim。

## 实际全文核对

1. **完整矩阵和两个峰1见证。** 所有四原 jobs 各有唯一内端/外端，未述资格 infinity。作者列出的 aligned assignments 逐机负载正确，包含外端共享且所有原 jobs 恰执行一次。q_1 的所有有限时间为1，故 OPT 下界1正确。

2. **作者的全模式证明。** 在 `C<2-epsilon` 时，H/I/E_1/E_2 上各自两件 eligible jobs 的总时间分别是 `2,2-epsilon,2,2`，均大于 C，故每台至多一件。四件 jobs 和四台机器必形成一个完整 perfect matching。该资格环恰有两份 perfect matching，作者从 H 的 q_1/q_2 分支逐步推出两 aligned，正确涵盖所有其它 internal subsets。这是完整结构论证，不依赖有限扫描代替 proof。

3. **bad 模式的精确峰。** inactive 的 I 负载为 `2-epsilon`；cross(2,1) 在 E_1 合并两件 unit jobs，cross(1,2) 在 E_2 合并两件 unit jobs，均精确峰2。外端确实共享，未被私有化或删 job。

4. **阈值严格性。** 作者正确只用 `<2-epsilon` 和 `B<2-epsilon`。它没有声称等号也只剩 aligned。独立记录的额外等号分类仍保留：在等号处共有五份 assignments，其中三份非aligned；作者未逐一重列全部等号例，并不影响其严格结论。

5. **delta 与位长。** `epsilon=delta/3`、`B=2-delta` 在 `0<delta<1` 时满足 `1<B<2-epsilon`。非aligned 最小峰与 B 间隙为 `2delta/3>0`。只有四机四 jobs、八个有限条目；有理数编码随输入 bitlength 多项式，不按参数倒数或分母展开。

6. **内外 scope。** 内部本身允许的错配，完整外端成本可能不能补齐；作者没有用本例否定只承诺内部交换的理论。两 strict witnesses 每台都有一件 job，是相同 machine-presence 状态，不是对外提供空余 slot 的可读取状态。I 的 `1-epsilon` 非机制核心，epsilon=0 的 unit 环也成立。

## 明确保留的未完成义务

没有读取外部 primary source 或认证 global novelty。本例仅是标准交替 matching 环的带权边界，不据此认证任意 external identification、clause query、额外 job、cascade、固定 source embedding 或 near-2 hardness。若以后把 E_1/E_2 与变量环/锁定机器合并，必须重新给完整实际矩阵、全部原 jobs 的 YES 和所有低峰 assignments 的 NO decoder。

此次未发送作者 Proof 给其它 agent，未改 repo/Git/Work 或旧冻结记录。此前有限辅助枚举只归 reviewer 自行执行，不记为 root 或作者运行，也不作为一般证明前提。
