# 叶资源重数gap一阶渐近：作者证明读后审查

审查者：boss11 内部 cover_consistency。实际全文读取 `private_tree_multiplicity_gap_asymptotic_frozen_proof.md`，SHA256 `0f3852e0b2326518316769cbd433502e79590f7b6ea0cddfd0515af628412397`；对应已读Exact SHA256 `fb1283d4bd3346be0dedae6e19acbef50876d68643fafdccbe537d7051156adf`。

先行独立稿 `private_tree_multiplicity_gap_asymptotic_statement_first_review.md`，SHA256 `4464041c06febb6107f118735098cf996ca315f96cd8eb71dfb3995a73588ed5`，原字节保持。该稿的完整配置、实际OPT和sup/limit在未读作者proof或其它摘要前形成；本记录为第二阶段。没有程序运行、Git/Work、新外部文献审计或新颖性认证。

结论：未发现standing fatal objection。作者全部四节与本人先行推导一致。

1. **完整配置而非仅λ。** 每根selector单件权1/μ、全μ父端leaf配置权1−1/μ，两者负载1且权和1；每独立Z_s的μ个真实leaf单件配置各权1/μ。selector全机器覆盖恰1，每leaf两端恰覆盖1，不合并同色jobs。unit selector排除T<1，故Tconf精确1。

2. **实际OPT。** selector所在state若C<2，唯一外机最多放一leaf，其根至少留μ−1个small，加unit得到2−1/μ；C≥2分支更不可能破坏该下界。恰外送所选state一leaf、其它全部原leaf父置达到此值。所有未选states仍保原μ个jobs，机器与resources互异如对象所述，完整σ合法。精确比值不是仅渐近或有限实验。

3. **同一个C_μ的sup。** 作者上界明确对全部P∈C_μ调用v3全CONFIG(T)，而非只对给定共同full-state λ的CONFIG1子类。显式平星族给该sup的一个成员下界，未要求sup达到。非空selector令Tconf≥1、全父置令OPT有限，比值良定义；所有d,h、root数、菜单与输入长度确被同一上确界遍历。

4. **极限方向。** μ/(μ+2)≤μ[2−G(μ)]≤1的两个方向正确，沿整数μ夹逼趋1；误差2/[μ(μ+2)]由同一逐μ界相减，非交换sup与limit。这个结论只是一阶锐，未给固定μ的exact G，也未宣称v3有限μ上界锐。

5. **显式位复杂度。** μ个根、μ个资源、μ²个leaf jobs加一个selector，完整表可按其输出长度生成。每非整数时间1/μ只有O(logμ)bits，但输出本身Θ(μ²)jobs，不能称poly(logμ)生成。作者准确保留此限制；完整配置和最优σ都是该显式族上可直接列出的证书。

6. **身份。** 下界族可显式求解，配置gap不提供NP-hardness、TFNP困难性或一般算法近似下界。整数μ无界令相对CONFIG的gap趋2，与固定μ时v3的常数离2上界一致；未推出UM-TARGET-v1正反面。一般上界依赖v3整体真值/审查，不是本页自己证明或有限运行所替代。

未发现需修正的公式、参数或负载文字；本报告不覆盖尚未读取的最终canonical整合稿或实现。
