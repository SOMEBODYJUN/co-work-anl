# 恰六人半覆盖

启动参数为 `--save customer-attraction --subarchive six-providers`。

恰六名单位权提供者、任意有限单位客户和有限非空共同目录；每一个完整历史纯SPE覆盖数≥最大六主题覆盖数/2，允许空、重复、零客户及任意离轨平局。

## 研究入口

恰六人半覆盖仍开放。以[正式原题](state/问题/六人完整历史半覆盖目标--问题.md)和[共同模型](../../state/定义/共同目录完整历史模型--定义.md)固定研究范围。

### 新 Boss 做同一个 n=6 原题

例如 Boss3 首次开工，在空的新目录用最新版启动器。把示例的凭据和程序路径替换成实际路径。

```sh
python <work.py路径> --repo co-work-anl-boss3 start --actor Boss3 --role boss --branch rebuild/research-v2 --save customer-attraction --subarchive six-providers --token-file <凭据路径>
cd co-work-anl-boss3
RUN=n6-boss3-20261118
mkdir -p "research/workspaces/$RUN"
cp -n archives/customer-attraction/subarchives/six-providers/research-spec.json "research/workspaces/$RUN/spec.json"
python work.py research studio init "$RUN" --spec "research/workspaces/$RUN/spec.json" --expect-branch rebuild/research-v2 --expect-remote https://github.com/SOMEBODYJUN/co-work-anl.git
```

新 Boss 使用自己的 clone 和尚未使用的 RUN ID。已有自己的同名 RUN 用 `studio status` 续接。Boss2 的 [研究笔记](../../../../research/workspaces/n6-boss2-astra-20261118/main/journal.md)可供成果线参考。本 [开题 spec](research-spec.json)只固定原题和模型，独立线只收 obstacle packet 的节选。idea 和执行子代理从 spec 的 `registry_object_id` 按需读当前超边，再打开相关正文和证据。已发布的[部分分数覆盖边](../../../../map/edges/n6-boss2-astra-20261118/partial-fractional-cover-to-six-half.json)和[四种额外覆盖边](../../../../map/edges/n6-boss2-astra-20261118/four-extras-to-six-half.json)分别处理各自的条件子类。

第一次 checkpoint 明确列出 `archives/customer-attraction/subarchives/six-providers/workspaces/Boss3`、`research/workspaces/$RUN` 和 `research/runs/$RUN`。以后 Boss3 从空目录接续这个 RUN 时，用相同存档参数和 `--resume`，再运行 `python work.py research studio status "$RUN" --session-tag <实际会话标签>`。

两份 RUN 可以并行保存。正式成果共享 `research/registry.json`，回流前同步。若其他 Boss 已先发布，保留自己的草稿和检查记录，把本 RUN 的增量重新合到新基表；承重证据或端点变动时重新复核。父档已有成果保原 ID 和正文，新成果归本子档。

已有数学与断点可直接打开：

- Boss1：[主笔记](../../../../research/workspaces/six-boss1-20261111/main.md)、[普遍界证明](../../../../research/workspaces/six-boss1-20261111/main_v6_exact_audit/proof.md)、[真实末回复重查询族](../../../../research/workspaces/six-boss1-20261111/main_terminal_reply_requery/proof.md)。
- Boss2：[主笔记及未完运输审查](../../../../research/workspaces/six-boss2-20261111-cross/main.md)、[一般收入合同与未付预算](../../../../research/workspaces/six-boss2-20261111-cross/coverage_bridge/formal_shared_rz_income_bridge_v1.md)。
- 承重勘误：[全局X须保同一实际背景下的最大潜力条件](../../../../research/workspaces/six-boss1-20261111/visible_maximum_joint_v6_model_erratum.md)；[旧ROOT显示式漏加号的更正](../../../../research/workspaces/six-boss1-20261111/root270_replycaps_iter3_main_review.md)与[当前根付款证明](../../../../research/workspaces/six-boss1-20261111/main_root_reweighting/proof.md)。旧冻结证据须合读这些更正，不取消独立有效支持。

Boss1主笔记提及的后继_stage目录不在当前已推送快照，不冒称其草稿已恢复；Boss2新矩阵仍待完整独立审查，未付预算不是半覆盖证明。保存的working不证明会话在线，后续从实际文件接续，不据旧公屏派工或重跑已认证计算。

## 内容位置

- [登记原题](state/问题/六人完整历史半覆盖目标--问题.md)
- `state/`：按数学对象类别组织自足Markdown，可随清洗增加新类别。
- `workspaces/`：Boss/清洗者个人临时研究，可自由保存未成熟内容。
- `papers/`：论文稿件及其必要依赖，保留与正式数学对象的对应。
- `tools/`、`evidence/`：本题计算程序、真实输入与核验证据。
- [现行登记](../../../../research/registry.json)：研究时用 `research show` 和 `research context` 按对象 ID 取原文与超边。
