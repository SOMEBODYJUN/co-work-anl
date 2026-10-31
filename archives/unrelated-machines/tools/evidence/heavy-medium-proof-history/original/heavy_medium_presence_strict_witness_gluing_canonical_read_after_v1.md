# Heavy–medium strict presence：canonical §8 最终 read-after

审查者：general_query_response_review。2026-10-18。

对象：`co-work-anl-boss11/research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md` 新§8。

最终审查 SHA-256：`0b9ab7d50bba3b4b7c5825c6208e51d23d20cdb5460d8e7478a6ef866f986e00`。

先后次序：先仅据新 Exact 和获准旧基础独立重构并冻结；再首次读新作者 Proof 并冻结单独 read-after；本轮才实际通读 canonical §8 及其组合上下文。独立证明及旧记录字节保持不改，审查者未修改 repo 或 Work。

**最终判断：修后 canonical 新§8 通过，数学结论、定义域及算法承诺与冻结 Exact/Proof 一致，无 standing fatal。**

## 最终组合核对

1. 新 ID 明确为 `UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1`，有理 T>0、两完整实际见证均≤T、`0≤ε<1/2`、`0≤a<1−ε`。未把旧§7的精确 unit、全矩阵两档或 `T=1+a` 偷加到新域。
2. 端点档次只约束各 job 在 σ0/σ1 中实际使用的端；未用有限端任意。输出只用两个实际原端，全部原 job 恰一次。heavy-presence 读取的是机器实际收到 heavy，未锁定占位 job 身份、其它边界或源标签。
3. `ε+a<1` 同时给 gap 与式(6)的 `<2T`。两种等价写法

   `3/2+(ε+a)/2 = 2−[(1−ε)−a]/2`

   正确；gap≥κ>0 给 `(2−κ/2)T`。00/11直接返回原见证，mixed分量构造不需要未知见证 oracle。
4. heavy 匹配由 `2(1−ε)T>T` 重新证明，复用旧§2的只是组合分解。测量机为颜色1的不同 machine 端点分量，能同时实现一个0、一个1。
5. 单 job–machine 翻转明确计入内部 heavy 成本最多增加 εT，且新 medium 成本 aT 可能叠加在同机；`(1+ε+a)T≤式(6)` 正确。没有误用精确 unit 的内部成本不变。
6. 通用分支全部 job–machine active；真实 medium jobs 与 job–job virtual items 的半半 medium 质量≤两原见证 medium 均值。virtual 仅编码路径方向，不新增执行任务，最终恢复全部原 jobs。
7. 旧§7加权半整化仅按成本上界 aT 缩放使用，不继承其见证容量规则。两个 medium 选项成本允许不同，同机选廉、相邻配对二着色同时给全部机器增量≤aT/2；其选择不会改变测量 presence。
8. 三行完整负载分别为 `(1+ε+a/2)T`、`[3/2+(ε+a)/2]T`、`(1+a/2)T`。均不超过式(6)；00类原机没有任何使用过的 heavy 边，因此不会新接 heavy。该表控制全部机器，不只测量端。
9. 静止原 job 保持原端；共同 heavy 边固定；a=0、ε=0、相同 virtual 目的机及零成本均由同算法处理。图、items、排序、二着色、恢复与有理比较均为总输入位长多项式，不按参数倒数展开。
10. 未加入新参数上界的全参数锐性、一般 UM 算法或困难性。旧§1–7字节与先前读取的旧基础精确匹配：去掉为新§8追加的两个 LF 后，前缀 SHA-256 仍为 `1d5d27a9a80c64dbcca319531da735f23b1d65e29d1ef1f16a011a85a4adf4ba`。

## 本轮发现并修复的呈现/范围文字

- 首次读取组合时，式(6)的部分 LaTeX 反斜线被字符串转义成 TAB/FF/VT/CR 控制字节。root 已在发布前定向修复；最终逐字节扫描除了正常 LF 外无任何 ASCII 控制字节，`\tau,\frac,\varepsilon,\right,\tag` 均为真实反斜线命令，公式可正确渲染。这不是数学证明的新版本。
- 原句“T=0不在本ID域，由旧身份分别处理”的末尾缺乏本文件旧身份支持：旧 unit/tiny 身份固定正容量。root 已删去末尾，最终仅“T=0不在本ID域。”，与新 Exact/Proof 一致。正 T 定理没有因此改变。

最终哈希对应上述两项均已修复后的字节。冻结 Exact、独立证明及作者 Proof 的原字节均未更改。

**最终批准范围：仅上述哈希的 canonical 新§8 数学与组合；不认证外部新颖性或主研究目标。**
