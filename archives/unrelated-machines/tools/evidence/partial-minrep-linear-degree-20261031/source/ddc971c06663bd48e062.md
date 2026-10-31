# 线性degree源v2与最近primary结果的边界核查

日期：2026-10-17。作者：内部子研究者pcsp_occurrence。仅scratch核查，不改Work/Git/共享登记，也不改已冻结v2两文件。

## 已实际读取的原始主文

1. Manurangsi，`https://arxiv.org/pdf/1807.00936v1`。本地原始PDF：`primary_originals/manurangsi_minrep_degree_1807.00936v1.pdf`，SHA256 `259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8`。本轮重读§3全证明及§4讨论；PDF/印4–7。不是只读搜索摘要。
2. Minzer–Zheng，ECCC TR24-027原版：`https://eccc.weizmann.ac.il/report/2024/027/download`。实际通过web reader打开90页原始PDF，读取§7.3.2以及§7.4，PDF/印46–47。§7.4只说明组合Laekhanukit和Manurangsi的已有归约，省略完整Min-Rep参数证明。
3. 同文2026-05-13 Revision1：`https://eccc.weizmann.ac.il/report/2024/027/revision/1/download`。ECCC报告页`https://eccc.weizmann.ac.il/report/2024/027/`在本次检索列出该修订。实际打开106页PDF，读取主结果与定义（PDF/印1–4）、§7.3中相关bounded-degree结果、§7.4的Lemma7.12和Theorem7.13（PDF/印60–61）。对2026版只检索相关章节，不冒称读完106页证明。

本轮ECCC PDF的shell下载尝试超时，没有把下载请求当作取得原始字节，没有为其发明本地路径、hash或manifest。以上ECCC内容的实际阅读来源是primary网站PDF reader。已有Manurangsi原件保持原字节。

## 最近结果实际提供什么

Manurangsi的Displayed Theorem1给随机归约下Min-Rep gap g，degree O(g log g)、alphabet O(g⁴ log²g)。其generic Lemma7的degree量为O(logQ/√γ)，cheap-list门槛为常数倍N/√γ；本文以almost-perfect Chan源证明Displayed Theorem1，不能把其YES直接改写成singleton完美来源。

其§3.3先证明cost O(N/√γ)的lists在原图不能覆盖半数边，再控制采样图中unsatisfied边的常数偏差下尾，并对cheap lists union bound。该证明没有把原覆盖率压成g的负幂，也未使用与全图总采样边数共同下界配合的rare-covered上尾。

2026 Minzer–Zheng修订版的§7.4，Lemma7.12仍明确导入Manurangsi Lemma7，degree显示为10⁶·2log(2R)/√γ。Theorem7.13的结果是degree O(g log g)、alphabet O(g^{2+ε′})，对任意固定ε′>0及充分大g成立。这改进了alphabet-to-soundness起点，保留该Min-Rep degree形式。其YES是almost-perfect的来源，不是v2所用的singleton perfect PCP。

该文bounded-degree **Max**2-CSP的near d/2困难性也确实存在，但对象是单label最大满足比例。直接用单labelNO value约O(1/d)再随机舍入cost gN的lists，只会经平均list长度损失，不能未经新证明改成v2的linear-degree partial-Min-Rep声明。

## v2相对这些公式的确切增量

v2选择更小的原source soundness γ=ρ³/(10⁹g⁸)，由截长lists证明原cheap coverage<τ=ρ/(100g²)。对固定cheap ψ，用采样covered边数X的上尾，在共同总边数下界之前得到

Pr[X≥ρH₀/2]≤exp(−ρH₀ ln g)。

cheap lists数量仍为exp(O(gN logQ))。因perfect-complete PCP可有Q=poly_ρ(g)，logQ/ln g为固定常数，采样degree可取O_ρ(g)。证明的数学变化是**rare upper tail + 全图共同边数事件**；不是把Manurangsi Lemma7里的γ直接换成g^(−8)，后者会给O(g⁴ logg)。

v2没有声称达到2026文的Q=O(g^{2+ε′})，也没有给出最优degree常数。较粗的polynomial alphabet可能让connectivity归约的最终k参数更差，所以不能宣称在其所有应用上统一改进。这里对UM候选的用途是把source degree预算从g logg改成g，使足够的物理component费用由logg变为某个固定常数；实际费用仍未实现。

## 新颖性判断的准确层级

本次对上述三份primary版本的具体相关章节和若干定向检索，没有找到“以较差的polynomial alphabet换取Min-Rep linear degree”的明确已有定理。这只能支持“尚未定位最近同结论”，不能支持“已证明新颖”或“足以独立成文”。

尚需进一步核查更早的三参数tradeoff、generalized sparsification定理、以及是否存在对上述upper-tail观察的已有说明。v2的正确性独立于新颖性；有限检索不证明不存在先前结果。

Status：实际primary阅读与参数比较已完成；新颖性未认证；UM-TARGET-v1未由此解决。
