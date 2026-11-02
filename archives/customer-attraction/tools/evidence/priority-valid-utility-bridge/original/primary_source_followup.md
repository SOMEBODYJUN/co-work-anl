# 2026-10-21 一手来源补查及 valid-utility 直接反桥

身份：个人研究补遗。`Q-CAG-HALF` 的目录、均分、单位客户与全部历史 SPE 量词均不改变。以下没有得到一般半覆盖证明或均分 CAG 反例。

## 已有记录复核

已读根 `AGENTS.md`、四入口、本题 README、模型及现行 `literature.md`。最初检索再找到的 Brethouwer 2018 硕士论文并非新资料，现行正文已经精确区分 downward-closed generalized market sharing、任意目录 equal-sharing covering、symmetric singleton 与一般多资源主题；不建议重复登记。

## 本轮新增查过但不能导入的来源

### Blum–Morgenstern–Sharma–Smith

一手来源：[Privacy-Preserving Public Information for Sequential Games, arXiv:1402.4488v2](https://arxiv.org/pdf/1402.4488)，ITCS 2015；论文前两节及 Appendix D。

**Paper Fact**：主体 resource-sharing 模型的收益只取决于此前使用该资源的人数，玩家的行动为一个资源（另有可分投资扩展）。完全计数器下 greedy 是 dominant，Theorem 1 给竞争比至多 4。Appendix D 改为终局总使用人数决定的 future-dependent 效用；Theorem 13 针对 greedy 策略和 `(w,n)`-shallow value curves，给出 `O(w alpha beta)`，不是所有纯 SPE 的定理。

**Interpretation**：将 CAG 的客户当作资源时，一个主题一般使用多个客户资源；将主题当资源又丢失跨主题客户造成的交叉拥塞。主体还缺少后继效应；Appendix D 保留后继效应但仍只分析指定 greedy 行为。均分曲线 `1/k` 的前缀和与终值之比随人数为调和量级，不能从该浅度结论读出与人数无关的 2。不能将“full-information greedy dominant”从主体移到 future-dependent 部分。

### Avni–Henzinger–Kupferman

一手来源：[Dynamic Resource Allocation Games, SAGT 2016 author preprint](https://research-explorer.ista.ac.at/download/1341/5073)，后续期刊版为 [TCS 807 (2020), 42–55](https://doi.org/10.1016/j.tcs.2019.06.031)。核查的是可取得的 2016 作者全文，不能把预印本定理编号当作 2020 版编号。

**Paper Fact**：玩家分多阶段、逐资源构成一个可行资源集合，scheduler 可让某些玩家同时动；目标最小化资源成本。Theorem 6 的动态 PoA/PoS 等于静态版本只针对 singleton cost-sharing 及 symmetric singleton congestion 子类；成本分享为 `c_e/k`，拥塞为随人数增加的成本。

**Interpretation**：这是逐资源动态选择与成本最小化模型。均分 CAG 的 `1/k` 是收益，加入使用者带来负外部性；不能因相同分母而套用正成本 `c_e/k` 的结果。一般目录也不满足 singleton。该文没有提供本题所需的一般桥梁。

### 检索范围及否定性结论的界限

本轮用 sequential valid utility / market sharing / Shapley coverage / symmetric congestion / lookahead 等组合检索；还核对 Paes Leme–Syrgkanis–Tardos 的 [The Curse of Simultaneity](https://www.cs.cornell.edu/~renatoppl/papers/spoa-ics.pdf) 与 Groenland–Schäfer 的 [The Curse of Ties in Congestion Games with Limited Lookahead](https://arxiv.org/abs/1804.07107)。未找到直接涵盖任意共同主题目录、匿名均分、全部历史依赖平局与所有纯 SPE 的半覆盖定理。“未找到”不构成不存在性证明。

## 直接构造的唯一正文

共同目录+预算平衡valid utility不足以推一般顺序半覆盖的精确构造、承重假设和审计，统一见 [priority_valid_utility_counterexample.md](priority_valid_utility_counterexample.md)。该模型非匿名、非CAG，未反驳本题。构造已获独立定义级内审；外审与新颖性未认证。
