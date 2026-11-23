# 强形式相对 Morrison–Kawamata 可动锥主问题

存档 ID：`relative-mk-cone`；范围：`archives/relative-mk-cone`。**原固定主命题已给出完整证明（V3），并通过两份全范围独立内部数学复核。**

## 当前完整证明

- [主定理与全部几何证明](state/strong-rel2/informed-b/proof.md)：完整处理相对维数 0、1、2，任意总维数及闭可动锥含直线的情况，并构造满足 Li–Zhao Definition 3.4 的强基本域。
- [准确陈述与共同应用](state/strong_rel2_statements.md)、[垂直核与基本域提升](state/vertical_kernel_and_domain_lift.md)、[半正定算子基本域](state/projected_operator_domain.md)。
- [原始文献与三版修订审计](state/strong-rel2/informed-b/source_audit_v3.md)、[泛曲面标记下降证明](state/strong-rel2/informed-b/marked_generic_descent_v2.md)。
- [第一份完整独立审查](../../research/workspaces/rmkc-boss1-20261123-a1/records/reviewer1_full_report_v3.md)、[全新非作者的整篇终审](../../research/workspaces/rmkc-boss1-20261123-a1/records/final_reviewer_full_report_v3.md)。

证明先在泛纤维的实际 Picard 商空间中建立半正定平移算子结构，再构造包含全部降秩边界的有理多面体域，最后经有限垂直核提升并作有限群切割。泛曲面覆盖由几何域上的 Totaro 定理和正文给出的标记下降获得。原题的有效锥、全支集保持群和强分离要求均以 [固定题面](state/main_problem.md) 及 [验收条件](state/acceptance.md) 为准。

完整正文 SHA-256：`c27e24be990f43c82b6c63e852e9ddfc2fbefd7e045363d5734cee4dbb62a0f2`。复核等级为内部数学复核；尚未进行证明助手形式化或外部同行评审。全部计算只作为独立压力检查，主证明不以有限枚举为依据。旧版的具体缺口与修复记录保留在本 RUN 中。

## 研究与复核入口

唯一现役启动词：[Pro 持续研究](prompts/pro-loop.md)。把它与当前 `work.py`、仓库外的 `githubtoken.txt` 交给新对话，按真实可用的平台工具开工。

不再分资料 Pro 和证明 Pro。文献读取、超边采用、引理、计算和反例审查都嵌入同一持续研究循环，局部成果不构成完成。运行持续到严格解决、用户明确暂停或真实资源上限；保留工作室、推导和计算断点以便接续。

## 原题与工作室

- [唯一主命题与完整范围](state/main_problem.md)、[数学完成条件](state/acceptance.md)。
- 每个 Boss 独立 clone 和 RUN；新 RUN 复制本档 [research-spec.json](research-spec.json)，再执行现行 `studio init`。真实恢复用自己的 `--resume` 和 `studio status`。
- 所有共同前提、条件和剩余义务按原超边规则实读；已有候选路线可替换，不强制沿一条辅助路线走到底。

## 早先研究资产

- [初始文献与版本缺口](state/literature_audit.md)、[原始资料清单](sources/manifest.json)。按当前证明需要补读，不等待一轮独立资料验收。
- [凸锥局部证明](state/proof.tex)、[反例边界](state/counterexample_audit.md)。这些均不解决一般几何主命题。
- 主对象 `RMKC-STRONG-REL2` 与现有完整条件路线可用 `research frontier/context/show` 调用。

计算沿用 `work.py compute`、`work.py github`、Codespaces 和 Actions。启动词给出实用命令；按实际权限、机型和额度执行承重计算，取回日志与证书，不把提交计算或进程成功当证明。

此前已冻结的 Boss2 初始读取 RUN 保持原字节以便准确恢复；其旧资料阶段说明不再是现役运行规则。程序没有新增调度系统，Git 写入和成熟结果回流仍沿用原工程。
