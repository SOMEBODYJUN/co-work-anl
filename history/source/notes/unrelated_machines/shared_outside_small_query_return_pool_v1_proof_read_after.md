# 共享外端 small-query／return-pool：作者 Proof 实际全文读后

对象：`shared_outside_small_query_return_pool`。2026-10-18，首次实际读取解封作者 Proof 后另冻。未改源 Exact、作者 Proof 或此前 Exact-first 独立记录；只新建 scratch 文件。

## 实际读取版本

作者 Proof：`/workspace/scratch/038d9dcc4cac/shared_outside_small_query_return_pool_proof_v1.md`。

实际字节数 5,219；核对 SHA256：

`ed5b9c15e075db63c6bfae57511ad025ed254d422b4dd92000ad4a05d1449b99`。

对应 Exact：`shared_outside_small_query_return_pool_exact_v1.md`，SHA256 `37304837169ba1e11595c9681528dfe21efe2ccf8a04e6bafc73b7c2b8cf2e4e`。

此前独立记录：`shared_outside_small_query_return_pool_v1_independent_review.md`，SHA256 `859691b410ae5ab0033c541508307108e42097400c3c4a42f38c042889f4baf1`。

后两文件均在 scratch 根，本次再次复核未变。

## 结论

**PASS。** 作者六节证明与此前独立 reconstruction 完全一致，覆盖所有 k、全部 S/T、任意实际 pool 分配及全部原任务；未发现新的 standing fatal。无需修改 Exact 或 Proof。

这个结论只认证明确 shared-outside pool 模型，不认证其它主 Claim、任意外接、source embedding 或 near-2 hardness。它可作为后续正文的 small/multiquery 边界接口，不能单独充当源 NO。

## 逐节实际核对

1. **完整域。** k>=2、a_i正有理总和至多1、H/P/E互异、全部2k件 q/b jobs、唯一 query outside端、所有 return pool端和 outside端齐全。P上共居明确是普通 UM 选择，不预设slot容量1。所有 b 的 unit 时间给全局峰下界1，H任意query subset负载至多1。

2. **good pattern最优。** 若 `empty!=T subseteq S`，作者按索引把 k-|T| 枚 pool returns 单独注入 k-1台P，所有 q、outside b、pool b 恰一次。E没有冲突，H<=1，故峰1。作者明确这只是存在最佳安排；同一 good pattern 的其它 rho 可以峰2或更大。

3. **bad pattern下界。** T为空时 k枚unit b 在 k-1台P的 pigeonhole 下界2；T不包含于S时相应 E_i实际同收 q_i+b_i 两unit，下界2独立于rho。这两条件并覆盖所有 bad patterns，无匹配失败即删job的偷换。

4. **bad pattern上界。** 作者对所有 S,T 给逐job峰至多2的安排。m<=k-1时池内单独分配，m=k时多出最后一枚放P_1；k>=2保证该机存在。故坏模式精确OPT2而非可能infeasible。所有原jobs及外端峰均计算。

5. **任意真实弱解。** 取 C<2 后由unit负载推出P/E各至多一件，再推出非空containment及这份sigma本身峰1。作者没有先重排rho后宣称原解已峰1。S可严格包含T，queries/returns都可以多枚。阈值B<2、aligned/inactive/cross及delta取法正确。

6. **位复杂度与scope。** pattern构造和实际目的地解码不枚举所有子集。finite条目 `k^2+2k`、dense `4k^2`、machines/jobs各2k及binary rational算术界正确。孤立模块S=T全部indices给全局OPT1，所以它没有source NO。作者明确额外outside端、识别资源、guards或新增H任务需另证，未免费扩域。

## 等号与输出边界

`C=2` 的边界不能排除 bad patterns：每一S,T都至少有一份完整峰至多2的调度。相反，即使 good S,T，在k>=3时也能用不佳rho制造峰2或更大；因此不能把“pattern OPT1”写成“该pattern每份assignment峰1”。原 Proof 正确区分了这两个量词。

q_i的小时间允许多query真正在H共居；本证明并未把H也当成一机一job。只有P/E在严格弱阈值下被推出unit capacity。k=1与正值域均保持原范围，没有扩展到不存在pool的输入。

此前对k=2,3,4全部4,328份assignment的有限辅助检查只由本reviewer在Exact-only阶段执行，不记为root运行、作者实验或代码实现认证。一般结论以上述任意k的负载/pigeonhole证明为据。本次未新增有限扫描。

## 状态和保留义务

原来的三份source/review文件哈希保持。未修改repo/Git/Work，未向其它agent发送Proof。没有外审、新颖性、实现或任意source编译认证。后续canonical若指定§4四环/§5pool审查，仍应分别限定范围，不能代审其它主Claims。
