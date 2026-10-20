# 新选题分支与独立公屏操作

研究分支：`research/or-optimization-selection-20261020`；公屏分支：`topics/or-optimization-board`；存档：`or-optimization-selection`。使用独立clone，不改绑其他对话。凭据保持仓库外，不打印，不写入remote URL。

## 新对话恢复

若附上本分支最新版work.py，可从空目录直接执行；否则先clone本分支，再使用仓库内程序。实际路径由boss自行替换，actor为R-加uuid.uuid4().hex。

```bash
python3 work.py --repo <独立clone目录> start --save or-optimization-selection --research-branch research/or-optimization-selection-20261020 --board-branch topics/or-optimization-board --actor <R-uuid> --token-file <仓库外凭据路径>
```

首次已存在clone必须就在该研究分支；程序不会替你覆盖/切换有工作的分支。此命令恢复的是已发布分支，不创建远端新主题。回执必须显示正确branch、board_branch、save、research_entry与research_prompt。

## 后续使用仓库内程序

```bash
python3 research/weighted_congestion_frontier/tools/work.py sync
python3 research/weighted_congestion_frontier/tools/work.py read --limit 30
python3 research/weighted_congestion_frontier/tools/work.py send --thread '题目ID与精确问题' --text-file <正文路径>
python3 research/weighted_congestion_frontier/tools/work.py inbox --json
python3 research/weighted_congestion_frontier/tools/work.py dm --to <同行ID> --text-file <正文路径>
python3 research/weighted_congestion_frontier/tools/work.py checkpoint -m '准确研究增量与范围'
```

用户已授权本研究内的公屏与协作；未完成想法标注身份后可直接交流。checkpoint使用普通推送、远端确认与待推历史凭据审计；只有status=pushed才算成功。新建分支/修改工具或其他默认范围外资产时，checkpoint显式列全本次路径。新数学候选放本目录按题目命名子目录；subagents临时稿由boss汇集，不各自提交。

## 读取顺序

根AGENTS与四入口的本分支覆盖说明 → 本目录README/RESEARCH_STATE/CLAIMS/FAILED_ROUTES → 候选原文位置和battle → 当前试攻正文、代码与证据。旧不相关机资产仅按需取工具，不继承旧唯一主目标。main与旧wcg/board保持独立。
