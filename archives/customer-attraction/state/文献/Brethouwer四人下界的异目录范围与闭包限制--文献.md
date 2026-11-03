---
id: customer-attraction/Brethouwer-four-player-lower-bound-model-scope-and-closure-obligation
kind: literature
type_tag: 文献
title: Brethouwer四人下界的异目录范围与闭包限制
status: original-scope-note-fully-read;university-primary-sections-rechecked
truth_status: model-boundary-and-unfulfilled-transfer-obligation;no-common-catalog-counterexample-certified
review_level: internal-definition-comparison;primary-PDF-local-section-check;no-reconstruction-of-unprinted-four-player-instance
summary: 保2018文献四人2.0558498235下界的异目录/未打印证书范围和向下闭包改变SPE的实际警告；shared-misery小反查复用既有正文。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/induction/brethouwer_scope.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/induction/brethouwer_scope.md
---

# 来源和本对象的独有范围

2595B原笔记全文实读，两个冻结提交同SHA`57e919a9e68ae4c2a999a1de1babb3929405419f78472d94534ccffcce3bd17d`。它是文献适用范围核对，不是四人数值下界的独立重证。原件完整见[来源](../../tools/evidence/background-induction-source-replay/source-root/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/induction/brethouwer_scope.md)，其它八件背景探针在[计算对象](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/c5277dbbe668c725a823.md>)。

文献为Jan-Tino Brethouwer，*The quality of equilibria in generalized market sharing games*，University of Twente硕士论文，2018-12-03；[大学入口](https://essay.utwente.nl/essays/76986)、[大学PDF](https://essay.utwente.nl/fileshare/file/76986/Brethouwer_MA_EEMCS.pdf)。本轮重新查阅下列指定章节及四人结果所在整页；不冒原笔记的浏览器source ID为本轮认证，也不声称阅读了该论文每个证明、取得作者ILP或核了全球后续文献。

# 原论文的模型接口

Definitions3.4/3.8/3.12采用完整过去观察、每个子局的SPE及最坏SPE效率。Definition4.2另加向下闭包；Definition6.15移除此条件，并允许各玩家自己的集合族S_i。§6.2.4/Theorem6.22报告四人28项、比值至少2.0558498235的ILP结果；该页没有四人重数、完整关联表或完整策略，且未要求各S_i相同。§6.2.3在给Example6.21补向下闭包后实际改变了SPE。§7的shared-misery附加式(60)及逐历史availability才导出Lemma7.4；Theorem7.6/Corollary8.2只处理对称singleton范围。

上段是本次指定页核对的内容，详细印页位置沿原笔记保在[核对路由](../../tools/evidence/background-induction-source-replay/literature-check.json)。本文剩下的迁移判断是按本仓模型作的推论，不把外部数值报告误标成已经由本仓程序认证。

# 为什么尚不能导入共同目录六人目标

本题所有玩家共享同一有限非空标签目录，客户均为不同单位客户，完整有序历史纯策略与全部离轨平局保留。论文的各S_i可以不同；直接取它们的并集会给每个角色增加原先不合法的动作，也增加每个历史的偏离和后继义务。原SPE因此不自动保留，原坏福利也不自动成为扩目录后某份SPE福利。原论文四人下界尚不足以构成本题反例，这个结论是**未满足迁移前提**，不是证明异目录下界不能迁移。

要使用该四人结果，需要取得具体项值、每个S_i和全历史策略，先按均分定义逐节点核验；若项值非整数，还须给出保持严格/弱IC的单位客户实现。然后另外证明一份共同目录变换，并把新增动作、全部离轨历史和任意所用平局纳入认证。最后即使得到四人共同目录实例，变成六人也有独立义务，不能免费加入dummy而保持原策略。

同理，向下闭包或删除被包含主题会改变早期偏离后的可信后继；末位面对固定历史时更大集合收益单调，不能推出所有较早角色的动态支配。论文闭包改变SPE的例子恰警告这种推理缺口。已有[不交极大主题定理](../定理/不交极大主题锐福利界--定理.md)则另外证明特定结构下的动态删除，条件是去共同核心后的不同包含极大主题两两不交，不能推广成任意目录的闭包/删除原则。

# 已充分整理的shared-misery部分按来源复用

一般交叠CAG不自动满足式(60)：两客户x,y，共同A={x}、B={x,y}，先A即时1，后B使旧人1/2、新人3/2，因此旧人下降后的收益未达到新人的收益。这个定义级小计算及availability完整量词已在[安全桥与文献资源](../资源/独立全局攻击入口的安全桥均匀接口与文献范围--资源.md#shared-misery原文的适用范围)充分写出，本源对此按duplicate复用；无需另立一个“主目标反例”。选一个主题通常覆盖多个客户资源，不能因每名提供者只选一个标签就把它改称论文singleton资源博弈。

本对象的新归档内容是四人异目录数值声明的证据缺件和向下闭包迁移限制；已有shared-misery反查与singleton锐界只连到原充分对象。当前半覆盖问题、文献优先权与外部同行审查均未由此裁决。关系是模型边界、迁移义务和受限工具前提，不以数值大于2或文献年份生成六人反例边。
