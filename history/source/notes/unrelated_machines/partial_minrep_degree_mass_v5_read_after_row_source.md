# 度数比例正规化 v5：作者冻结证明读后回执

读取目的：在非空 typed 域的 Exact-only 独立重构后，核作者证明的不同 fiber 暴露、两侧 copy 质量和真正 source alphabet 同步复制语义。

## 实际读取与顺序

先行记录 `degree_mass_copy_regularization_v5_statement_first_review_row.md` 的 SHA256 为 `fab9db01a1e7b483d6e0659ab98c869ea3153697a41c5c376837f86cd9b5ddfd`。该记录先冻结并通知 root，其中保留了独立发现 v4 空 alphabet 域缺口、继而收到 v5 已知修正的顺序。

之后才收到、实际 SHA 并全文读取 `degree_mass_copy_regularization_v5_root_frozen_proof.md`，实际 SHA256 为

`e2e60ca49cb6fcaf14a865a83c1d537d3213eb01a8d60c1e1f6baa1054b86c29`。

哈希匹配。没有读取原 v4 proof 或他人本次新审查，不把原 v4 的字面完整域追认为已成立。

## 读后攻击

1. **degree-mass 质量。** 固定一侧时每个真实 copy 的命中概率恰为 \(\deg(v)/(M_0t_v)=1/(M_0z)=2/N'\)。把左右 heavy copies 的数目加起来，重端概率至多 \(2\#\mathrm{heavy}/N'\le2g/H\)，不会额外多出一个因子 2。作者 \(\gamma H^2=16\tau/1000\) 的常数计算正确。新预算始终是全部 copies 的 \(gN'\)，并未偷偷替换为原点不加权预算。

2. **variable permutations。** 每份 permutation 可分别用其自身 \(t_v\) 作点态密度比较；所有不同 template edges 的两端仍恰涉及 \(2k\) 个不同 (permutation,slot)。因此 \(e^{2k}\) factorial moments、typed token 数上界 \(QN'\)、实阈值尾界和全部列表并界与先行重构一致。

3. **最后 slot 暴露。** simple prefix 中当前 copy 与起点在末色均未用，已揭 slots 又对 template matching mate 封闭；故当前 fresh slot 的 mate 确实 fresh。若它不在起始原点的 fiber，闭合概率为零；若在该 fiber，分母是该起始点的 \(t_v-G\)。按起始原点先求和 \(t_v/(t_v-G)\le2\) 是必要且正确的抵消，未用最小 fiber 粗乘全部 \(N'\)。平行 2-cycle 的末首异色同样成立。

4. **repair 与 bounded bits。** 作者的较强禁点排除（全部短 cycle vertices）仍只花 \(GB_0\)，bucket matching 保证可选 \(f\)。新短 cycle 的全部单新边/双新边配对都被覆盖。\(M'=zm_*\) 正确给出统一 \(2B_0/M'\le\rho/4\)。实际 draws 恰 \(K_0=d\sum_v(t_v-1)>0\)，没有沿用旧稿 \(2dN\) 份数的保守写法。接受事件不偏置 typed permutations，FAIL 和 NO 成功概率均充分。

5. **source 同步标签是真语义。** 新标签是实际源 alphabets 的 \((\alpha,s)\)、\((\beta,s)\)，每个投影严格保 s。新满足边丢掉 s 后仍满足旧边；旧最优赋值取全局同 s 给逆向，因此 value 恰相同。每个新右标签 \((\beta,s)\) 的原像数量恰等于旧 \(\beta\) 的原像数量，exact 4 fibers 等逐表性质完全保留。此为真实 source 变换，不是把一些 route aliases 当作源标签。

6. **PCP 接口与复杂度。** 固定 \(g,\rho,G\) 时同步 tag 个数、alphabet 与 d 都是固定常数；原 graph degree 可增长、两侧不等且有平行边均已由度数复制和修复处理，确实不再需要额外正规化前提。若只知一般 fixed-error PCP，没有新增 \(Q=\operatorname{poly}_\rho(g)\) 定量；作者保留了这个限制。非空 alphabet 修正、固定 G 的位复杂度、随机归约只推出 \(\mathrm{NP}\subseteq\mathrm{BPP}\) 的假设区别也均准确。

## 结论与范围

未发现新增 fatal objection。冻结 v5 proof 与先行独立重构一致，v4 域缺口只由 v5 新版本修复，不倒改旧字节或审查事实。没有新增实现、有限测试或外部新颖性认证；本回执不代替 ECCC primary theorem 的完整 PCP 证明，也不提供 UM compiler。
