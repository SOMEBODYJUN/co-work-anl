# Santa 无常近似条件反面双源审查

## 来源身份、版本与阅读范围

本批完整读取两个冻结来源，并比较 v1 与规范化 v2：

- `320c21caaf68f30f0f5e`，`research/current/unrelated_machines/santa_conditional_reverse_barrier.md`，blob `9fa0825e75e40c41ca56736cb44b672880f2ddb2`，SHA-256 `058a59d5dd03297bfce56cce16527ab7fb49140d642a6572cfe1ee8949d3eec9`；
- `a8ec98c7bc5bce1b0d3e`，`research/current/unrelated_machines/santa_conditional_reverse_barrier_v2.md`，blob `6147656be3b21734d340c6b6f688cbd9187c0654`，SHA-256 `54b7f77a099dad089be5eca3e9236bb9b48c449fd08e339f0b5b3ce65d7d054f`。

两源均冻结于 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）。同步读取了 `research/unrelated_machines/LITERATURE.md`、`literature_manifest.json`、BLMRS Makespan-to-Santa Claus 论文事实及相关配置/舍入审查。v2 只规范化 v1 的输入位长、二进制有理价值和量词，核心数学命题相同；两源合并为一个条件审查正文，未重复宣称两个独立障碍。

## 条件命题及证明

定义 `SCHA_det^N`：对每个固定整数 (c\ge3)，一般 Santa Claus 最大化最小总价值问题（输入价值为二进制非负有理数）不存在确定性位多项式 (c)-近似算法，近似方向为输出 (V\ge\mathrm{OPT}/c)。这是未经证明的强假设；已知的固定 (\gamma>0) 次多项式近似与它相容。

来源命题 `UM-SANTA-NO-CONSTANT-CONDITIONAL-v1/v2`：若 `SCHA_det^N` 成立，则不存在统一 (\varepsilon\in(0,1)) 和确定性位多项式算法，对所有一般不相关机实例输出
\[
C_{\max}\le(2-\varepsilon)\operatorname{OPT}.
\]

证明使用 BLMRS Theorem 1 的方向性桥：若 makespan 存在 (2-1/\alpha) 算法，则 Santa Claus 存在 (\alpha+\eta) 近似。给定固定 (\varepsilon>0)，取固定 (q\ge\max\{2,\lceil1/\varepsilon\rceil\})，有 (2-\varepsilon\le2-1/q)，所以假设中的算法也是 (2-1/q) 近似；将 (alpha=q)、任意固定 \(\eta>0)（例如1）代入得到固定常数 (q+\eta) 的 Santa 算法，与 `SCHA_det^N` 矛盾。(q,\eta) 只依赖固定 (\varepsilon)，不是输入参数，也不引入准多项式搜索。

该证明是条件逻辑闭合的；它没有把 Santa 的现有 factor-2 困难性误读为 `SCHA_det^N`。对 \(\alpha=2\) 的桥只给 (2+\eta) 近似，不能推出无任何常数近似。LST 的更强材料可在 \(\varepsilon>1/2\) 时触及 (3/2) 型边界，但不是本命题的主要证明。

## 适用性、位复杂度与数学边界

v2 把 Santa 输入价值明确为二进制非负有理数，保留 v1 已指出的适用性义务：BLMRS 论文给出 polynomial-time 归约和实际资源分配（Lemma 12），但没有在本题正文中完整展开有理缩放、有限取整、配置枚举和中间分母的位增长。固定 (\alpha,\eta) 时，仍需一个独立位增长引理，才能把文献的运行时间解释为本任务所需的确定性位多项式。当前正文把这一点作为待补义务，没有静默补成已证事实。

该条件反面只覆盖一般无额外限制的 Santa 与一般不相关机模型，使用的是确定性算法方向；没有论证随机算法、受限机器结构、固定树宽或其它配置合同。配置 LP、Sherali–Adams 或固定 gadget 的整数间隙只说明松弛/舍入路线的障碍，不能替代复杂度假设。

若未来证明 `SCHA_det^N`，或者直接构造对每个固定 (\varepsilon) 的实际整数 YES/NO gap，则本桥会给出 `UM-TARGET-v1` 无统一 (2-\varepsilon) 算法。当前既没有 Santa 无常数近似定理，也没有绕开 Santa 的一般实际归约，故不能把本页写成主目标的无条件否定。六人 SPE 的客户目录、六提供者完整历史、终局均分和任意平局语义不属于此对象，SPE 覆盖目标保持独立开放。

## 比较、证据与第三阶段接续

v1 的独有内容是首次明确写出条件命题、固定 (q=\lceil1/\varepsilon\rceil) 的反证和已知结果的强弱边界；v2 的独有内容是把输入价值、近似方向、位长和固定参数量词写成规范合同，并把位增长义务放在正文中。两者数学结论合并后只保留一个条件来源身份。

第三阶段 mapper 使用本页时应标注 `conditional_reverse_barrier`，并同时记录假设、归约方向、确定性范围和未完成的位复杂度审计；不能把 `SCHA_det^N` 当作已证障碍，也不能用已知 Santa factor-2 结果填补其缺口。相关文献原字节只按 manifest/冻结来源引用，本页不改写原始论文。

## 处置

两源均 `integrated`。条件命题、证明、适用性义务、反面解释和未解缺口已写入本页；未把条件假设升级为 hardness、算法不存在性或六人 SPE 结论。
