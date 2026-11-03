# 根work.py：启动、源阅读、清洗勾选和图

新对话使用本结果分支的新版work.py和仓库外凭据，自动找附件路径及独立--repo目录：

```sh
python3 <新版work.py> --repo <本对话独立目录> start --actor Boss编号 --token-file <仓库外凭据路径>
```

默认结果分支rebuild/research-v2、公屏wcg/board-cleanup-20261028、repository-cleanup/cleaner；身份由提示词明确指定，程序只绑定校验。第三阶段新对话加`--role mapper`。已有其他绑定clone不改绑，另建独立目录。附件启动后转用结果分支根最新程序；本次换结果分支后需换用此次新版附件一次，旧版仍指向来源分支。

以后新研究明确指定父存档和子问题，例如`start --save facility-games --subarchive common-two --role boss`；回执会给出该子存档入口，工作室在其内部。继续同一clone复用绑定，换研究问题使用独立clone。新问题目录先按实际数学建立，不能让一个子存档暗中变成别的题。

同步/保存/交流沿用：

```sh
python3 work.py sync
python3 work.py checkpoint <本次明确路径> -m '内容及准确范围'
python3 work.py read --thread rebuild-v2 --limit 20
python3 work.py send --thread rebuild-v2 --text-file <正文文件>
python3 work.py inbox
```

## 冻结源与协作勾选

```sh
python3 work.py clean status
python3 work.py clean list --prefix research/current/customer_attraction/ --limit 20
python3 work.py clean list --available --prefix research/current/customer_attraction/ --limit 20
python3 work.py clean list --owner self --state in-progress
python3 work.py clean list --owner self --full
python3 work.py clean search '精确数学关键词' --path '*.md' --limit 30
python3 work.py clean show <源ID>
python3 work.py clean show <二进制源ID> --out <本地临时文件>
python3 work.py clean claim <源ID> <另一源ID>
python3 work.py clean claim --prefix research/current/customer_attraction/ --limit 20
python3 work.py clean done --record-file <一个或一组语义处置JSON>
python3 work.py clean release <本人未完成源ID>
```

数字limit只控制领取/显示批量，按实际工作调整，不是研究时间/方法配额。list默认只给ID、路径、状态和owner，完整指纹/来源/记录用--full。--available看本地快照中未认领的项；--owner self恢复本人当前批次。查看其他人的最新进度可先sync；claim始终以远端最新状态裁决。

按prefix领取下一批只选尚无人认领的文件，不会重复领取本人上一批；该范围已领完返回status=empty。显式ID仍可用于继续本人已有认领。认领和勾选使用正常Git推送重试；两个对话不能同时获得同一项。返回pushed才确认操作；根程序随后自动同步本地清单并保留暂存、未暂存和未跟踪草稿，无需每次另敲sync。若回执local_sync.status=needs-attention，远端操作已经成功，但本地恢复有冲突；先按说明处理，备份仍保留，不能把它当作未领取再抢一批。公屏说“我看这部分”不能代替正式认领。

新clone只下载结果分支最新快照；原始来源先按冻结提交取元数据，再按需取回所读文件；文本搜索批量预取所需类型，减少网络往返，服务端不支持过滤时回退完整快照。清洗事务使用本clone内可复用的Git对象缓存，各事务的写入工作树仍独立，避免每领取一批就重新下载整棵结果树。

处置文件格式见cleanup/receipt-example.json，可为单条或JSON数组；一源可对应多对象、多源可对应一个自足正文。正文先checkpoint，完成登记会检查目标已在远端分支存在，不能拿本地未推送文件勾选。integrated/retained/duplicate/retired为完成处置，needs-decision不算完成。read/compared等字段是清洗者的实质工作声明，程序校验不能替代数学阅读。

cleanup/CHECKLIST.md及checklists/分册会自动从逐源记录生成勾选。inventory分母固定，后续来源增量另行冻结与登记，不静默重写旧清单。

## 2.5第一步/第二步：设计与部署状态

新入口见[分步设计](../research/CURATION.md)、[第一步提示词](../prompts/02.5-1-inventory.md)、[第二步Boss](../prompts/02.5-2-distill.md)与[worker](../prompts/02.5-worker.md)。当前交付的是分类、程序和协作规格；新材料批次与对象群认领程序尚未实现，不存在可直接复制的新完整启动命令。

现有`work.py curate scan`只枚举当前正式候选及SHA，不给材料定性。`clean claim/done/handoff`只管旧冻结来源。`start --board-branch`可选新公屏，但curator的工作区/登记目前仍硬编码cleanup域，新save也不直接支持；部署前不可冒称新2.5已可运行。现有checkpoint、正常同步和公屏消息机制可以复用。

详见[程序待实现规格](../research/PHASE25_PROGRAM.md)与[工作区、公屏、交接和退役](../research/CURATION_OPERATIONS.md)。第一步单Boss收回六名gpt-6-sol/high内部代理批次，不需要逐材料远端claim；第二步多Boss按对象群使用最小单任务事务。

`tools/curation.py`、`tools/maps.py`及现有schema保留为[上一版原型](../research/CURATION_PROTOTYPE_V1.md)，不是本次1/2步骤验收协议。2.5第三步、第三阶段结构和研究Agent由后续设计负责，不用原型格式倒逼数学拆页。

## 固定身份、认证与重置

新对话显式start --actor Boss编号；旧同一clone迁移用--adopt-legacy。doctor检查实际写端点，公开读取不代表认证成功。登记失败不可新认领；暂停用clean handoff --all，认证受阻仅checkpoint --local-only保全。

HTTPS令牌模式为--auth token --token-file 仓库外路径。SSH模式为--auth ssh，使用当前运行环境的SSH agent并忽略旧PAT文件；GitHub默认remote转为SSH地址，新建SSH clone后同clone继续会复用模式。SSH公钥不是token，私钥不进入程序包/仓库。本地Windows SSH不会自动提供云端身份。本程序运行环境仍为Linux/macOS/WSL；Windows原生Python兼容性不在本次已验证范围。

reset plan只生成保全清单，不改远端。reset apply由明确协调Boss执行：重新读取最新远端核实done，清掉未完成状态/未引用的临时协作区，公屏重建为1条成果入口；结果与公屏两个分支使用正常--atomic推送，一起成功或一起失败。保留Git历史，不强推。执行前停止旧客户端认领并先部署此程序，失败不报告重置完成。
