# 五人背景候选、六人结构证书与前缀包络证据

实际EP主源仅四份，合计15911B。[原claim回执](claim-receipt.json)为Boss4、pushed/synced、tip `416783d940ecedea4ac07ec23f1038ebd787b384`，四owner/progress与源SHA均核对。全部源由已有本地缓存读取，重新核size/SHA256/Git blob SHA1；无show、网络fallback、共享Git写入或额外claim/done。本文正文为本地成熟，待Root串行保存。

| ID | 原文 | 字节 | SHA-256 |
|---|---|---:|---|
| 8227a5cc6d9b86680893 | [R211协调稿](original/research/workspaces/customer-attraction/R-2118664d5481486fb34eb4b7f788af5a/notes/coordination.md) | 6118 | df8c6a15c190e0a12647dec470327963b47994e51165939fb7de26f861ed4415 |
| 0dacd024eb96954fd0c7 | [BG5候选审查](original/research/workspaces/customer-attraction/R-2118664d5481486fb34eb4b7f788af5a/notes/researcher_b_bg5_profit_candidate.md) | 3739 | a2ff47b4835117c4393f9d717a1e1664db0fb7ffb358bf2cbe70ad235080cf93 |
| 5c9a4ea8ec3529ce76cd | [R216入口](original/research/workspaces/customer-attraction/R-21674f0a89d74b80ae16410012678daf/README.md) | 2959 | 557e2d42bda0a1a0d88350320618db1a4645dedbb1e55501eae81072e74aab43 |
| f52629029fafc986e75a | [完整可信攻击入口](original/research/workspaces/customer-attraction/R-21674f0a89d74b80ae16410012678daf/credible_search/README.md) | 3095 | 40874ba38dc01520f7846bf953f3beadba993fa29cd0db42bf9e680990a2124d |

[primary inventory](primary-inventory.json)与[本地原导出清单](primary-local-export-manifest.json)保冻结完整commit/path、原字节、行数和owner。两冻结提交同字节不算两次独立数学复核。

## 四个自足对象

- [五人背景利润候选](../../../state/候选/五人任意背景利润的范围与索引接口--候选.md)：实际五人尾利润、合法背景/任意外生背景区别、零分子、462索引行、已知零背景及全部可覆盖客户b≥2子域，保原有限探针/负LP余量，仍候选。
- [旧玩家前缀包络](../../../state/引理/有序前缀旧玩家的双边终局收益包络--引理.md)：任意完成、不需SPE的双边收益及全树整数模型有效cut，性能未认证。
- [六人双包含证书与K障碍](../../../state/证明/六人倒二双包含证书与统一K模板边界--证明.md)：G三类真实行/消h恒等式、H/L真实早期与末位IC、全部1960域及32类最小值，和另一统一K模板的三行矛盾。结构特例不是一般六人定理。
- [协调与逐人缺口资源](../../../state/资源/六人协调前沿与逐人缺口探索的范围证据--资源.md)：十项协调范围、根覆盖支撑锐界/根遗漏触及量的完整证明、原有限gap发现及Gram身份、旧研究者先验与停止点。

## 必要比较与未认证原件

[comparison inventory](comparison-inventory.json)有完整本地2462B K障碍、3465B双包含作者稿、4974B根支撑稿、2201B真尾利润投影，以及6376B全树模型。这五份**只作EP必要比较**，没有额外primary receipt/done；未来认领不能把本次比较阅读当先前primary完成。

[本地比较清单](r3-ep-related-local-inputs-manifest.json)同时准确列十项缺blob：两个gap报告、prefix cut benchmark、structured程序/383291B点、三人机会候选审计/证书/报告、Gram代码/197381B点。[别名清单](r3-ep-formula-comparison-inputs-manifest.json)另记原1227B双包含replay缺失。新旧路径的6376B完整树代码同SHA `06f97056fd6534274120425f6adc18b072908fc51643f76cf08fa4ba7f815b70`，只存一份代码和两个来源定位，不重复运行。

原BG5的旧临时 `test_bg.py/search_bg.py` 未在本批提供冻结字节/输出/seed，不从路径文字推断已取得；原64/1000/500/500/100与LP前五余量仅来源声明。R211的四主题32767二值输入、R216旧两次45秒/structured 0..8/Gram负平方也未复跑。其他数学独立审查自报按原先验保留，缺实际审查稿/报告不升级为本次新盲审。

[formal-context inventory](formal-context/inventory.json)区分8篇实际全文比较和6段精确scope/接口摘录。已完整入库的大型定理复用其已证内容、核本次需要的量词，不假称本批重新独立重审全部旧证书；摘录保来源原SHA/大小/行段。快照链接按其原正式路径解释，未改共享页。

## 本次唯一新程序及正确计数

[完整标准库程序](check_ep_coefficients.py)在新空输出目录只执行一次，exit0：

| 检查域 | 实际结果 | 身份 |
|---|---|---|
| 双包含所有允许早期四位/末两位/比较与真回复计数 | 1960条，32压缩类，最小Q=0；六角最小值逐类一致 | 完整客户系数域证明，不是有限游戏样本 |
| 统一K指定模板 | 三行Fraction值与sumλ≥4、各λ≤5/3一致 | 精确模板障碍，不是SPE反例 |
| 前缀倒数核 | 196个b/k/c组合 | 有限实现回归，普遍结论由倒数证明 |
| 所有前缀/完成的旧位置收益包络 | 810+384=1194项，后者96个空主题位置 | 固定静态完成，未核SPE |
| BG5范围算术 | 462索引、若三坐标为A/B/AB负载则64中10合法、257/455高背景系数 | 不是旧BI探针复现或BG5全域证明 |

全部完整输入规格及1960逐条系数/32类表见[524663B结果](new-coefficient-check/result.json)，[stdout](new-coefficient-check/stdout.txt)、[stderr](new-coefficient-check/stderr.txt)、[event](new-coefficient-check/event.json)绑定实际程序SHA/命令/环境。原程序入口0、LP/MILP0、SPE游戏采样0；未重新运行同SHA完整树模型。没有从空目录PASS、异schema输入或表内数字回填任何原候选认证。

完整版本/证据层级见[boundaries](version-and-evidence-boundaries.json)及[execution](execution-boundaries.json)。新数学是proof-aware语义重构，无新增盲审者、外审、新颖性或一般half认证；候选未提升，比较源不额外done。
