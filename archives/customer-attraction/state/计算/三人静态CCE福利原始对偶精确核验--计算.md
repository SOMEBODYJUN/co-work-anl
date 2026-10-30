---
id: "customer-attraction/static-cce-welfare-exact-certificates"
kind: "computation"
type_tag: "计算"
title: "三人静态CCE福利原始对偶的精确核验资源"
status: "complete"
truth_status: "finite-rational-certificates-replayed"
review_level: "full-code-read-original-byte-replay-and-input-integration"
scope: "八客户21历史/84比较/64静态终局与十三客户31历史/155比较/125静态终局；三份原审计及历史独审"
summary: "保全两个单位客户输入、两个完整策略JSON、三份原字节Fraction审计、三份内部审查和完整复跑；原始/对偶匹配精确得到最低CCE福利544/87与2785/297。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_eight_cce.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_eight_cce_independent.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_worst_cce_welfare.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/customer_attraction/eight_cce_welfare_gap.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/customer_attraction/worst_cce_welfare_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/eight_cce_welfare_gap.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/worst_cce_welfare_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/customer_attraction/eight_customer_cce_welfare_gap.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/customer_attraction/worst_cce_welfare.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_transport/cce_independent_review.md"
---

# 三人静态CCE福利原始对偶的精确核验资源

## 资源身份与数学用途

[反例正文](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)给出三人原共同目录模型的两个自足实例、全部策略、静态CCE不等式及锐值证明。本对象保存实际可执行的有限证据及审查身份；它不是一个六人SPE或half反例，也不将历史审稿文字当作可执行证明。

独立证据目录 [cce-welfare-counterexamples](../../tools/evidence/cce-welfare-counterexamples/source-manifest.json) 中，`source/`保留七个原字节程序/输入/证书，`original/reviews/`保留三份原字节内部审查。清单逐一记录完整冻结commit、原路径、源ID、字节数和SHA-256。复制未更改原程序；十三客户脚本的 `Path(__file__).parents[2]` 仍能定位 `source/examples` 和 `source/evidence`，不依赖旧结果树。

| 原字节文件及源ID | 实际功能、完整阅读和本轮执行范围 |
|---|---|
| [八客户主审计](../../tools/evidence/cce-welfare-counterexamples/source/tests/audits/customer_attraction_eight_cce.py)，`751c1dead05499ea6589` | 直接列出八名单位客户、根/次/末完整策略、两套CCE乘子、五点计数分布和安全值原始/对偶；逐客户Fraction收益；21历史84比较；20计数列；11有序分布支持及12个体CCE约束；十竞争计数的安全值匹配。**输入及策略硬编码**，不读取另存的JSON。 |
| [八客户独立审计](../../tools/evidence/cce-welfare-counterexamples/source/tests/audits/customer_attraction_eight_cce_independent.py)，`d755069ffb2aadd08a1f` | 按兴趣mask展开互异客户；另写收益、真实后继和全部21历史；84比较与64有序终局的福利恒等式及两套对偶；显式11点分布与12项CCE约束。当前 `SMALL=True`，本轮只运行八客户分支；代码保留的42客户分支不计作本轮复跑。它也不读取输入/策略JSON，且不核安全值。 |
| [十三客户独立审计](../../tools/evidence/cce-welfare-counterexamples/source/tests/audits/customer_attraction_worst_cce_welfare.py)，`b94f56b0e9f953655929` | **读取下述单位客户输入和完整证书**，检查三玩家、五不同覆盖主题、31个唯一且无遗漏的历史；155个真实后继比较；125有序终局/35多重集；两套对偶及250次逐客户逆负载恒等式；十格解析表；18有序原始支持/15项CCE约束；合法安全背景和half范围。默认只打印摘要，`--output`排他创建完整报告。 |
| [八客户输入](../../tools/evidence/cce-welfare-counterexamples/source/examples/customer_attraction/eight_cce_welfare_gap.json)，`8ad153389623fee10a3a` | 四主题、三玩家、四兴趣类型重数2、4、1、1，等于八名不同单位客户；不是客户/玩家权重。 |
| [十三客户输入](../../tools/evidence/cce-welfare-counterexamples/source/examples/customer_attraction/worst_cce_welfare_failure.json)，`a684c7b0c712d79e6bff` | 五主题、三玩家、六兴趣类型重数2、1、1、2、4、3，等于十三名不同单位客户，直接被十三客户审计读取。 |
| [八客户完整策略](../../tools/evidence/cce-welfare-counterexamples/source/evidence/certificates/customer_attraction/eight_cce_welfare_gap.json)，`91db4f6c6916b3529699` | 全部21行有序历史动作及终局计数 `[1,2,0,0]`；不含CCE乘子/分布或安全值证书。两原八客户程序硬编码同一策略，另由本轮包装器核对JSON及客户输入逐项相同。 |
| [十三客户完整证书](../../tools/evidence/cce-welfare-counterexamples/source/evidence/certificates/customer_attraction/worst_cce_welfare_failure.json)，`625c2e102057a2ad1c50` | 全部31行策略；终局路径/计数/收益/W/OPT；简单与锐CCE对偶；五个计数原始概率；固定安全背景(0,4)及五个查询值。每项均被原十三客户审计重算。 |

以上三程序只使用标准库，不导入仓库规范模型/求解器、作者发现LP或其他候选验证器。原主审计和原独审属于不同历史实现；本轮重跑它们不增加一次独立外部数学审查。所有终局和全部历史是穷尽有限集合，未从随机抽样外推。

## 真实复跑与补充输入检查

本轮逐原字节运行三审计，生成完整的[八客户主报告](../../tools/evidence/cce-welfare-counterexamples/replay-eight-main.json)、[八客户独审报告](../../tools/evidence/cce-welfare-counterexamples/replay-eight-independent.json)和[十三客户独审报告](../../tools/evidence/cce-welfare-counterexamples/replay-thirteen-independent.json)。三者分别与冻结报告源 `7b3d422130b0ffd3cb7f`、`1177706c965e42303f38`、`251b0b0b011d22de9284` 的JSON结构及完整字节一致，SHA均在清单保存。冻结报告只是比较源，未被本批冒记完成。

本轮新增[重放包装器](../../tools/evidence/cce-welfare-counterexamples/replay_bundle.py)先核十份原件指纹；由于两份八客户程序不读外部JSON，它还核验保存的八客户输入展开后与两程序的客户表相同、21个策略动作与两程序逐历史相同、终局计数与证书相同。随后在临时目录复跑三程序并把**全部**报告与保存的本轮输出比较。[包装器输出](../../tools/evidence/cce-welfare-counterexamples/verification.json)全部通过；它是输入集成及原实现重放，不称新独立证明。

从仓库根完整复验：

```sh
python3 archives/customer-attraction/tools/evidence/cce-welfare-counterexamples/replay_bundle.py
```

也可分别运行原程序，默认只打印：

```sh
python3 archives/customer-attraction/tools/evidence/cce-welfare-counterexamples/source/tests/audits/customer_attraction_eight_cce.py
python3 archives/customer-attraction/tools/evidence/cce-welfare-counterexamples/source/tests/audits/customer_attraction_eight_cce_independent.py
python3 archives/customer-attraction/tools/evidence/cce-welfare-counterexamples/source/tests/audits/customer_attraction_worst_cce_welfare.py
```

八客户实际路径011、收益(2,2,2)、福利6、OPT8，两套静态下界56/9和544/87；11点达到分布的每玩家偏离slack为(220/261,0,0,0)，真正安全值44/23。十三客户路径044、收益(3,3,3)、福利9、OPT12，简单下界137/15、锐值2785/297；18点达到分布的每玩家slack为(277/297,0,0,0,0)，固定背景查询为(2,3,3,3,3)。所有SPE最小slack均为0，平局不是可以删掉的错误。

## 三份历史独立内部审查的独有内容

| 原审查 | 内容及与其他源的区别 |
|---|---|
| [八客户独审](../../tools/evidence/cce-welfare-counterexamples/original/reviews/eight-review.md)，`22c96eb380d594a55d01` | 记录先核发现者另一完整策略，再核简化后的计数依赖策略；共享程序使用后者。按互异单位客户及全部有序历史/终局重算，确认84比较、64终局、11点分布、12项个体CCE约束及锐值。42客户初版另存个人审查，不是该八客户程序当前执行分支。 |
| [十三客户正式独审](../../tools/evidence/cce-welfare-counterexamples/original/reviews/thirteen-review.md)，`a17cd0fc96442b09a2a9` | 六项逐定义审查覆盖输入合法性、全树完整性、CCE无对称假设、简单十格证书、锐原始/对偶及安全/half边界。特别说明“所有终局的对偶列”不要求每个静态终局是均衡；对称化只用于达到分布。 |
| [十三客户工作区独审](../../tools/evidence/cce-welfare-counterexamples/original/reviews/thirteen-pre-publication-review.md)，`524cac7f63daa4eb7948` | 记录先独立重求CCE LP，再用Fraction高斯消元重建有理原始支持，最终正式验证只依赖有理证书；保全逐客户逆负载恒等式、十格表及18点/15约束。独立审计不强制同计数历史同回复。它与正式独审是同一十三客户研究/审查链的个人版和共享版，不当作两个新增外审。 |

三份原审查均明确只认证指定福利替换桥失败，没有规模最小性、全球新颖性或外部同行评审。独立重求的浮点发现状态不承担锐值证明；逐终局有理下界和匹配CCE才承担证明。完整策略JSON也不是只有在轨终局的证书。

## 全仓比较、关系及使用限制

现有[强/弱iid福利支付反例](../反例/独立同分布福利支付--反例.md)已经保存八客户策略和安全值，并用显式Nash证明强iid桥失败；它没有保存本批两例的全部任意CCE锐原始/对偶和十三客户完整树，因此本资源与正文有新增内容。后续关于强iid状态的纠错沿用本CCE包含关系，没有推翻两个锐值。十三客户与另一个十六客户PNE实例必须分开，不能给PNE证书附上未经验证的CCE最小值。

数学关系为：程序实现客户均分公式、完整策略最优性及静态CCE原始/对偶；报告是其完整有限精确输出；历史审查记录实际独立实现和范围；包装器保证保全输入与硬编码八客户实现一致。它们共同支持[反例正文](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)的指定有限结论。真正安全值、half及恰六人的主问题没有被这些输入反驳。本批未生成图，关系类型应区分实现、核验、来源和范围边界。
