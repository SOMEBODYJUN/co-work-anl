# manuscript-build 6源交付

正式claim已由Boss确认pushed `692c11e49f21eb65f875113fc440555853d6f663`。
六份canonical原件共44463字节均全文实读、按hash核同并保留；没有修改已完成paper10、共享README/图或他人正文，也未执行Git/claim/done/sync。

## 正式目标

1. `archives/facility-games/state/资料/设施均衡两篇成文的模型与审查链--资料.md`
   - ID `facility-games/two-manuscripts-model-and-review-ledger`。
   - 两阶段原子客户/存在完整精确NE续局与顺序均分/每份有序历史纯SPE、拥塞PNE分开。
   - 两设施phi与任意k的2、算法/有限构造/短证书各自保留；给因子二字典序/四预算/装箱/cap/默认续局的承重接合。
   - 保留第一篇false quota等修复但review仍pending的台账状态；第二篇初始FAIL三修复及较后round2闭环分开；完整hash/来源/历史策略/工具快照均保全。
2. `archives/weighted-congestion/state/资料/结构方法成文的跨稿版本与转换范围--资料.md`
   - ID `weighted-congestion/structural-manuscript-cross-record-and-conversion`。
   - 保存总台账独有b177历史diff冻结点、旧59页/26页构建及f6f→3ee2→5691先后。
   - 完整说明原prepare_mor的固定源码/marker/模板复制/披露/证明/附录合同；真实当前输入实际生成历史0729源码hash，不升级私有32页PDF或官方class认证。
3. `archives/facility-games/state/计算/三稿构建及结构稿转换的隔离执行--计算.md`
   - ID `facility-games/manuscript-build-and-conversion-interface-replay`。
   - 两原程序原样隔离执行：12构建控制流case＋5转换case，完整动态结果和真实失败。
   - 默认无参数argparse失败、局部诊断门/Underfull允许、跨稿批次非原子、缺模板部分复制、缺appendix标记仍exit0均如实保存；原件不改。

## 证据和回执

- `tools/evidence/manuscript-build/`：6源`source-manifest.json`及`original/`完整原路径；`source-link-audit.json`；新`replay_interfaces.py`；实际`interface-replay.json`；`EXECUTION.md`；`delivery-self-check.json`。
- `cleanup/workspaces/Boss4/manuscript-build-receipts.json`：6条各自read/comparison/decision语义回执，targets全为上述正式正文。
- `cleanup/workspaces/Boss4/manuscript-build/delivery.md`：本交付。

程序输入和全部正式原件可由持久保留的`original/`及相邻manifest复现，不依赖临时调度assignment；当前结构TeX/Bib为已完成paper10保留的明确比较输入，不重复认领其源。

## 实际执行与范围

Python3.12.14下原build.py复制至外部canonical树；`kpsewhich/pdftex/latexmk`为明确受控命令fixture，不执行真实TeX。显式三键成功复制三份标记输出；格式缺失分支被实际走到；warning/Overfull/Undefined/编译非零/无log不覆盖当前目标；Underfull允许；无参数exit2；三稿第二稿失败时第一稿已更新、其余旧值不回滚。原源hash不变。

原prepare_mor.py使用实际当前TeX5691…和Bibdfdb…，4模板为明确非官方复制哨兵。生成TeX SHA完整为

`0729d63bd9fb0e7f5d47c02f0a41461b5c983da37f2e0a7493941aba5ec2e422`，

恰历史私有MOR TeX所报hash。24正式块字节相同、24proof规范标题/Halmos/空白后论证相同、123label次序保留、119显示数学仅appbasecap一块纯alignment差；Bib不变。根内输出拒绝，缺第二模板留首文件，缺附录marker仍成功返回却环境不配对。模板真实性、任意TeX有效性与新PDF页数均不由这些测试推出。

最终run003从仓库内已保留原件/manifest执行交付harness，全部预期观察通过，完整stderr/returncode均保留。exit0是harness断言通过，不是17个原程序全部exit0。生成MOR TeX、哨兵class/logo及标记PDF全留外部work树；自查确认公共证据包无`.pdf`/`.cls`/生成MOR全文。未重编已通过27页PDF，未取得/阅读/编译私有32页PDF，未安装官方模板或拉取历史skill仓库。

## 最终自查与限制

`delivery-self-check.json`：6ID与assignment全等，6source hash/size匹配；三正式ID全仓各唯一；26个新正文相对链接实际存在；26个旧源导航中24匹配inventory，旧venue两个WC源码/PDF链接多退一层，已保存正确canonical路径/源ID而不改原源；12+5case结果齐全，真实输入仍不变。交付harness SHA为`061c28e8e40066c3128dbf485374a67c512bf8050b43fd33140ae28ffe4e5ffb`。

各源实际语义均独立记入回执，未把旧外部政策当今天核过，未把历史skills/范文阅读冒称本次应用/重读。数学证明、审查/编辑状态、程序控制流、文本hash、PDF版式、官方规则、外审和作者责任保持分离。下一步若做真实期刊转换或第一篇修复证明审读，应按所写未决项实际取原件，不由本批归档伪造闭环。

| 源ID | 正文落点 |
| --- | --- |
| `591b726ce83d4cb20f5e` MANUSCRIPT_REVIEW | 两份资料 |
| `17c8e5318c879ceacb29` README | 三正文 |
| `6acf2e7a2282803aed5c` skills/protocols | 两份资料 |
| `f825cc9bda4c0dae367a` venue round1 | 两份资料、计算 |
| `2193b82340454049aa2f` build.py | 计算 |
| `acbc0c3e74a3b742b7c6` prepare_mor.py | WC转换资料、计算 |

本批没有修改第三阶段图；正文已说明模型分离、证明依赖、历史审查版本、源程序实现及有限控制流检查的不同关系，供Boss后续按语义建边。
