# 五个不同审计合同的原代码、比较与真实运行

BN实际claim pushed/Boss4，tip5b3523d8701fec6fd7019b9d927e241e372221c1。原[claim回执](claim-confirmation.json)保留local_sync needs-attention；Root实际恢复后给[独立resolution](independent-sync-resolution.json)与[完整备份保全检查](sync-preservation.json)，stash b583…的2tracked/2untracked全字节恢复、无缺失/差异/合并冲突。本批随后读取5个[实际owner/in-progress](actual-owner-verification.json)，才clean-show导出/核SHA/完整读primary。未改原回执为synced，不重领，不作共享Git写。

## 五个自足资源

1. [异构微任务奇偶分割](../../../state/计算/异构微任务两汇点奇偶分割原程序--计算.md)：固定六item64子集，实际代码只压缩算术，相关宏/filler矩阵与一般归约、ST正面合同分开；旧输出源码SHA不同。
2. [真实矩HS与state](../../../state/计算/真实最优矩上全空间HS与单状态贪心原程序--计算.md)：210真实OPT点、17D、全迹δ66，全部得分和两种实际分配，不误用NF或rank1一般保证。
3. [incidence tiny](../../../state/计算/关联环秩tiny原入口的七次穷举与生产缺口--计算.md)：五矩阵七brute、4为字面helper数，反馈/叶/环DP未实现；先前旁读不替此次primary。
4. [长路径gluing](../../../state/计算/长路径联盟分布的基线独立粘合原程序--计算.md)：1265联盟/10360正联合状态+3556路径方向，单机完整law和全任务补全，外机无T保证。
5. [稀释逃逸独立重算](../../../state/计算/稀释共享逃逸独立原程序的部分探针与全部匹配--计算.md)：427/521，58/44条件点样本，4394/4914全部匹配、352z额外，peer只指纹不执行。

## 24份冻结原件与实际阅读

5 primary原文全部本批完整读；4依赖全部同SHA核验：baseline AX已完整读；diluted底座/扩展AQ已完整读且BN运行段/guard重读；peerGHMR AQ/BE已完整读，本次仅指纹。15 comparison（数学正文/review/作者对照源码及旧JSON）全部完整读/结构全字段比较。不是用同SHA替代未知原文的阅读；manifest逐份read_scope分清真实复用及历史先验。

共同冻结commit为68fad804ec5946cb296f77dc5b336308a66abf12、aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c。

| ID | 原路径 | 字节 | SHA256 | 保留件 |
|---|---|---:|---|---|
| 454bf51d5beefcda9b2f | tests/audits/unrelated_machines/heterogeneous_macro_3partition_barrier.py | 1143 | `7faddb50e676977907b3ce46c34b07cb0b5147b2d41d3b160d6823836e26c4c4` | [原件](original/tests/audits/unrelated_machines/heterogeneous_macro_3partition_barrier.py) |
| cd7597c69d8924fb8c0f | tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py | 7379 | `9adc3f3a95346b944b1169990c9be64b64ab4993e5f2e4fa8b67a8c9421edcda` | [原件](original/tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py) |
| f4c32edec8faa5dd71db | tests/audits/unrelated_machines/incidence_cycle_rank_exact.py | 1887 | `a46f115cf05d992196b122feb0a9514c5f11a20777dc10e02fef0ed11520f6d8` | [原件](original/tests/audits/unrelated_machines/incidence_cycle_rank_exact.py) |
| 60286686302e507de71f | tests/audits/unrelated_machines/independent_coalition_gluing.py | 5328 | `6e29e69a0fbd8b0418ae159ecc6e8bd3f0e3dd9ee9519d1ae24e57550859efee` | [原件](original/tests/audits/unrelated_machines/independent_coalition_gluing.py) |
| b7575ad08722bda19415 | tests/audits/unrelated_machines/independent_diluted_escape_audit.py | 7061 | `599e238c36fed3ffbe36f98046bc5e860ba548c2162735c187f127366a3a3783` | [原件](original/tests/audits/unrelated_machines/independent_diluted_escape_audit.py) |
| e57947bc795251d373c3 | tests/audits/unrelated_machines/rounding_and_gap.py | 12108 | `5ba0dc52ddbb90ffece75e5accd2e801957c1172e337b9bdf033e22a64cbd75a` | [原件](original/tests/audits/unrelated_machines/rounding_and_gap.py) |
| 02411e208331973f0c82 | tests/audits/unrelated_machines/diluted_sink_probe_gap.py | 11101 | `9aa9c7c3390b658da10b925618ff0fed2762c61e768cf6e2c232fc3936fd9092` | [原件](original/tests/audits/unrelated_machines/diluted_sink_probe_gap.py) |
| 878f5e7c59363b3e2928 | tests/audits/unrelated_machines/diluted_escape_probe_gap.py | 8623 | `a56a90992101d73a404c92578cebe0ad048b7dbf6782309bcf95a3c9e4c160c8` | [原件](original/tests/audits/unrelated_machines/diluted_escape_probe_gap.py) |
| 2dd3413231d9b1499f4c | tests/audits/unrelated_machines/heavy_matching_residual.py | 14747 | `63f64a5497223e451374c74359dade6bec14ea507b3ed901d8f9495a699f2deb` | [原件](original/tests/audits/unrelated_machines/heavy_matching_residual.py) |
| cd484ee6b4f82c43337a | research/current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md | 5968 | `8a4daf9ea3266e74c543a8c8ed09b36476174ae014f2f2b025e4f0c8af4186e9` | [原件](comparison/research/current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md) |
| 4a0005dd9bfe3e08bf35 | research/reviews/unrelated_machines/heterogeneous_macro_uniform_residual_review.md | 3090 | `9c7dc6887683ad5dc9ef9e1317104e1caead7e545d93c7f3e54f3f562a2bae52` | [原件](comparison/research/reviews/unrelated_machines/heterogeneous_macro_uniform_residual_review.md) |
| ee815a77dcd3fe452451 | evidence/runs/unrelated_machines/heterogeneous_macro_3partition_barrier_audit.json | 622 | `c8627371d2b1e718e5a8dc8e19c891ec64866153f33e270951bc493032e462d9` | [原件](comparison/evidence/runs/unrelated_machines/heterogeneous_macro_3partition_barrier_audit.json) |
| 43aee4f76d83e01522ad | research/current/unrelated_machines/global_assignment_moment_rounding.md | 17973 | `c49e7d8dd13757f16ce6bd451c32999966739bed9be5c40d0bade4fce63cb1f0` | [原件](comparison/research/current/unrelated_machines/global_assignment_moment_rounding.md) |
| 0db3d973e7d68bc734c1 | research/reviews/unrelated_machines/global_assignment_moment_rounding_review.md | 9154 | `854bcc711cf9aa9b60625aff8524db96ee831ac6c9355e2056b00da16a17aee5` | [原件](comparison/research/reviews/unrelated_machines/global_assignment_moment_rounding_review.md) |
| 7ae41ce4d0f4baf510f5 | evidence/runs/unrelated_machines/hs_effect_greedy_exact_m3_audit.json | 6214 | `07d752e9fdd5683a2f20d2c118b3cc721a41bfd6686841c9edb711e61f447e97` | [原件](comparison/evidence/runs/unrelated_machines/hs_effect_greedy_exact_m3_audit.json) |
| 2deeaca59ffa4fd6f5b4 | research/current/unrelated_machines/incidence_cycle_rank_exact.md | 7413 | `03dec47c13b4244d2cfe017d714b872455c563dcfb6df30ac59194620530cbce` | [原件](comparison/research/current/unrelated_machines/incidence_cycle_rank_exact.md) |
| e7faed81ea53ac5394c5 | research/reviews/unrelated_machines/incidence_cycle_rank_review.md | 1574 | `3038d4fbe3c45cfcb0523b8c9e5c5b0536b63a67a33b61cf52701308816c91bf` | [原件](comparison/research/reviews/unrelated_machines/incidence_cycle_rank_review.md) |
| 7d8533e6d4a2dfeb379d | research/current/unrelated_machines/long_path_coalition_gap.md | 9974 | `71694578be6a110ad993fd0039c039edfeca2f5c509e1049ca204e4fe42b8aa6` | [原件](comparison/research/current/unrelated_machines/long_path_coalition_gap.md) |
| 3b0c1560ee8abc49e3d0 | research/reviews/unrelated_machines/long_path_coalition_review.md | 5877 | `f3cd0cfba881f2a657ebe36dbb554aff36b054f9e2e69996ed84ed5bd395bc23` | [原件](comparison/research/reviews/unrelated_machines/long_path_coalition_review.md) |
| e206d008d16b3d8734bf | tests/audits/unrelated_machines/long_path_coalition_gap.py | 12826 | `8e822e4cba475d7de9e68e283b0cfb785e66223b95236a7a4f1580dc5a4c2925` | [原件](comparison/tests/audits/unrelated_machines/long_path_coalition_gap.py) |
| 649e8a41070019034b4e | evidence/runs/unrelated_machines/long_path_coalition_gap_audit.json | 7406 | `c0d459e740c05426eab434ad6e04d33c662e5c39c603571d4772690ed5e39282` | [原件](comparison/evidence/runs/unrelated_machines/long_path_coalition_gap_audit.json) |
| 07f075f376fc5aa958fe | research/current/unrelated_machines/diluted_sink_probe_gap.md | 23305 | `08c7d787759fd48b65cada97c052bdab80556bedde1e14f4601b8e4447b52ffd` | [原件](comparison/research/current/unrelated_machines/diluted_sink_probe_gap.md) |
| 5756d2e4aa79d8ee9588 | research/reviews/unrelated_machines/diluted_sink_probe_review.md | 16218 | `7cf3851cf0cd93da53c2a6f9d86bf85a5394dca0a90e539f37cf2c31426f3569` | [原件](comparison/research/reviews/unrelated_machines/diluted_sink_probe_review.md) |
| b714940853db4b866782 | evidence/runs/unrelated_machines/independent_diluted_escape_audit.json | 1423 | `e8678929d6c16927181961311040ffa3449606949683e34cd03f198153aa010e` | [原件](comparison/evidence/runs/unrelated_machines/independent_diluted_escape_audit.json) |

[5 primary](source-manifest.json)、[4依赖/指纹源](dependency-manifest.json)、[15comparison](comparison-manifest.json)。没有将shared正文中的引用视为本轮那些外族原件全部已读。8份已读正式页的独立原快照随[关系审查](relation-review.json)保留，后续共享页变化不破坏本次比较的SHA。

## 实际5原CLI，各一次、全部exit0

| 入口 | stdout | stderr | 记录 |
|---|---|---|---|
| macro partition | [原文本](runs/macro-partition.stdout) | [stderr](runs/macro-partition.stderr) | [记录](runs/macro-partition.execution.json) |
| HS effects | [完整两种history](runs/hs-effects.stdout) | [stderr](runs/hs-effects.stderr) | [记录](runs/hs-effects.execution.json) |
| incidence tiny | [原Python repr](runs/incidence-tiny.stdout) | [stderr](runs/incidence-tiny.stderr) | [记录](runs/incidence-tiny.execution.json) |
| coalition gluing | [四组输出](runs/coalition-gluing.stdout) | [stderr](runs/coalition-gluing.stderr) | [记录](runs/coalition-gluing.execution.json) |
| independent diluted | [完整汇总](runs/independent-diluted.stdout) | [stderr](runs/independent-diluted.stderr) | [记录](runs/independent-diluted.execution.json) |

[完整argv/cwd/秒数/原代码SHA](runs/execution-manifest.json)、[16运行附件指纹](artifact-manifest.json)、[数学运行scope](mathematical-execution-scope.json)。补充数学进程0；gluing/diluted本身是无main guard的顶层原审计，两者已各计入五次，不另算两次。导入的baseline/base/extension都有main guard，导入主audit体0；peerGHMR不import。没有执行作者longpath541184方向、nearflat主程序/validator、dilution候选全点main或基线main。检查器不会import/execute这些代码。

原参数与输入来自完整原码、保存生成器、seed及指定--repo。原脚本未输出所有矩阵/算子/逐查询证书，本包不伪造这些全量附件；HS确有完整两种history，coalition确有四组统计，diluted只有58/44实际点的重算通过统计而非4914完整向量dump。一般数学论证与有限实现分开。

## 旧新边界与后续纠错

[历史比较](historical-comparison-and-version-scope.json)：HS及independent diluted新旧JSON全字段同；gluing只对旧报告independent_audit子对象全字段同，不把作者primary当本次运行。macro旧JSON script_sha256=31d74…与当前7fadd…不等，只有PASS文本/参数同；原旧JSON保真，不改hash不解释未取得旧源码。incidence没有虚构inventory旧运行JSON，先前同码旁读和本次新一次分别计数。

全仓后续对照保长链三项修正：首向左不强制全左；v侧概率1−1/k、t侧1/k；只知Tconf≤给定Tk，不把Tk称精确最小阈值。HS canonical尾空格规范化及review先后也保历史，不倒填此次blind。稀释正文旧§1–10与新§11分审身份明确；现全篇实读不把wholeSHA当自动新增审查。

## 语义回执、自查与精确交付

[5逐源receipt](../../../../../cleanup/workspaces/Boss4/r3-um-following-audit-contracts-primary/semantic-receipts.json)、[exact copy list](../../../../../cleanup/workspaces/Boss4/r3-um-following-audit-contracts-primary/copy-files.json)、[实际下一5候选](../../../../../cleanup/workspaces/Boss4/r3-um-following-audit-contracts-primary/next-candidates.json)。[关系审查](relation-review.json)解释每种接口的前提、计算/证明/版本身份及不应合并的量词；仅阶段二，不写第三阶段超图，不覆盖共享正文或旧done。

[自查代码](verify_delivery.py)只做原件/输出字节、字段、链接、回执与清单一致性，不替代数学审查；stage模式exacttree，repo模式仅核列出文件存在。[真实自查报告](delivery-self-check.json)。
