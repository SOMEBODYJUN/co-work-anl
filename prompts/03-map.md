# 第三阶段数学超边

## 工作目标

2.5.3已经登记了有什么结果、到哪里读。第三阶段要找出这些结果怎样共同推出目标、怎样迁移到另一模型、哪条路线被反例切断、哪里还欠证明。以后研究者从原题或候选路线出发，沿图能够找到完整前提、适用条件、实际推导和精确证据，决定接着证哪一步。

例如，一个结果给局部下界，另一个结果给合成规则，两个都要用时只写一条联合边。合成规则尚未证明时，仍可以交代两者怎样推出全局目标，并留出规则本身的缺口。只完成阈值的一步，就准确保留这一步。转移证明中，解码或等价是可用的桥，目标是经过桥后得到的新保证。

后续1个Main与3个Solver研究同一原题。1个障碍组从原题、定义和障碍独立研究，2个成果组可调用这里的证明及线索。本阶段准备这套数学依据。

## 启动、恢复和分工

本次身份Boss【用户指定唯一编号】。未给先问，子代理沿用父Boss身份。默认gpt-6.1-sol/ultra，用满用户要求且实际可用的并发。Boss和子代理都做实质数学。同clone的Git写入由Boss串行。

先检查本地目录、Git状态、远端和已有草稿。同一对话恢复原clone及未完批次。新对话用独立clone和仓库外凭据，从当前分支启动。

```sh
python <当前work.py> --repo <独立clone> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外凭据>
cd <独立clone>
python work.py doctor
python work.py board-init
```

此后用clone根work.py和公屏wcg/board-map-v2。读AGENTS.md、当前registry、research/IMPLEMENTATION.md及prompts/03-map-worker.md。同步后用map list --owner self恢复已有批次。所有Boss都能起草、领包、重派、纠错和集成。只按实际空位领取。认领后按回执核对实际任务版本，必要时sync，再把仍归本Boss的任务交给 `fork_turns:none` 的fresh worker，给出clone、任务路径和内部词。批内反馈交回原worker，空位随成熟交付继续补新worker。

## 围绕数学问题分包，保留相关重叠

从最深子档已有的承重关系开工。先看哪个结论可作下一步前提、哪个反例针对同一陈述、哪些版本需要核对假设、哪两种结构有可检验的映射。按这个问题组织一组核心对象，跨包需要的对象列为共享阅读端点。每个对象的3A主覆盖由一个批次负责。同一对象可以在多包作为前提、被检验的主张或模型映射端点。有明确问题的共享端点也要实读和比较。共同定义可以共享读，有具体数学作用时再建立比较。

草案的 `overlap_comparisons` 列出核心、对端和精确引用。in-packet在本包一起读并核清作用。follow-up保留到实际3B或3C范围，先判断是否确有值得继续的数学问题。通常由使用证据或检验主张的一方负责这项比较。互引的同一线索由程序分给一个主包，推理方向由实读判断。不同推导、假设或反驳目标可以共用对象。主题、目录和模型名可引导检索。精确引用到另一对象的正文时，即使模型标签写法不同，也按实际假设核对。大对象按同一个问题分段读。较短的独立组可以合领，各组分别比较。

先看已领范围和已有成果，再用实际子档与原领取前缀起草。新发现可在本包解决的真依赖用map read-add。确需跨包、跨子档或超出本包预算时，把准确对象ID、具体数学问题、证据和所缺条件接入已有比较包，或发布定向任务。实际比较需后续完成时，将已发布的承接任务ID写入收据的 `follow_up_tasks`，本包先交自己的数学结果。已有同一问题的有效成果就复用。普通可领单对象包可用map compact按子档合并。

```sh
python work.py sync
python work.py research map-draft --stage 3A --scope <实际子档> --task-prefix <原领取前缀> --output map/planned-tasks.json
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next --prefix <同一领取前缀> --count <实际空位>
```

3A先核最深子档的对象族。3B处理同一存档内有依据的跨包或跨子档比较。3C处理有明确数学问题和模型映射的跨存档比较。后两层用--object-id或--objects-file给端点，用--comparison写具体问题。同一对象可以同时参与不同问题，各包写各自的产物。局部成熟就往外接。3D贯穿全过程，任何Boss都可集成已有成果。

## 实读、判定、交付

按任务实读原陈述、模型、定义域、量词、条件、异议及必要证明。写边前先用一句精确数学话写实际得到的结论，再核对目标对象原句。用已知前提、附加条件和给出的推导确能得到整个目标，才给整结论支持。只证明一个阈值、分支或算法部件，用contribution.result写已完成的精确步骤，用contribution.remaining写目标还欠什么。已有独立节点可直接引用。只有确有复用价值且缺失的数学对象才补登记。

一条证明使用共同前提时保一条ALL边，独立证明各保一条。等价要给双向推导。反驳准确指向被否定的陈述或步骤。模型迁移把原结果和等价/解码桥列为前提，终点放实际转移得到的命题，并写清模型、量词和条件对应。完整推导依赖开放前提时标条件关系。推导本身有缺步时标候选并写明缺步。引用、实现和有限计算各按实际用途入语境。

按write_paths提交独立边JSON和coverage。每个核心说明实际比较对象、证据、得到什么和还欠什么。零边包也交准确比较和原因。只找到语境边时可以保留，并在覆盖中说明数学比较结果。身份、版本或证据未辨清时才记needs-decision，明确开放问题照实交付。Boss在原有交付中核对推导方向、目标范围、条件和证据。按IMPLEMENTATION用edge-bind --write、edge-check和checkpoint确认pushed，再map done，可批交。成熟包及时交付。

原文错误按现有流程作最小勘误并同步受影响的登记。追加只读依赖用read-add，核心改版先保草稿并交接后重派，已done批用map-draft --repair-task定向替代。其余批继续。明确原Boss无法接续时用map reclaim <任务ID>或map reclaim --owner BossN并给真实原因，再从已保存的数学继续。认证故障先用local-only保全。

## 持续推进与完成

每轮恢复旧包、补空位、实读、交付、核跨包线索、接下一包或下一层。公屏只发值得共享的数学结果、可检验的前沿或实际阻碍。边收边sync、assemble，写清实际比较过的子档、存档和跨档范围。远端有先提交的成果时按新快照集成。

队列空时核对仍未覆盖的核心、已发现但未接住的具体比较以及尚未整合的交付。范围内的已知工作都得到准确处置，再用research check --final、build --final核实，并checkpoint所有实际投影、coverage、integration和registry。开放的数学命题照实留下。真实暂停用map handoff --all --reason保存实际成果、断点和下一步。
