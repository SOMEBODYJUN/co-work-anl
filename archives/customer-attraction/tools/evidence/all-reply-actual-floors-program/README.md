# 全部显式回复的actual前缀地板程序证据

[正式程序对象](../../../state/程序/全部显式回复的实际末位报价地板程序--程序.md)保存完整语义、参数与可复现范围。`original/`中4342B主源，`related/`中的oq/mixed/cut及新4963行点，均以清洗inventory原字节/SHA保全；来源映射见[manifest](manifest.json)。继承图源码、旧4927点和联合5108点使用manifest列出的同批共享原件，避免大数据重复保全。

新增[audit_floor_rows.py](audit_floor_rows.py)只从主源AST摘取三个常量及`added_rows`函数。独立侧把16hist各展开六索引并字面枚举66有序边，核36行全部68580系数；对旧cross、新floor和combined三点还遍历全部列/权，比较完整列描述符，检查权非负、O与W并逐行精确回代。此次本地运行一次，结果为[floor-row-audit.json](floor-row-audit.json)：旧点4负5零、新floor点0负7零、master点0负6零。

此脚本不导入原整图、不调用build/main或linprog，也不核其它行族。解析合法性在正式正文的真实偏离证明；有限点计算不证明全类型或完整SPE。

从仓库根可按以下命令重现同一有限数学检查（`--out`应指定隔离临时路径；文件名来源元数据会随输入路径basename改变，不要求输出逐字节相同）：

```bash
python3 -B archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/audit_floor_rows.py \
  --source archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/original/all_reply_actual_floors.py \
  --point archives/customer-attraction/tools/evidence/cross-source-graph-program/related/cross_source_priced_optimum_exact.json \
  --point archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/all_reply_floors_exact.json \
  --point archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json \
  --out /tmp/all-reply-floor-local-check.json
```

原floor CLI本包执行0次，浮点发现0次。联合代理唯一一次运行原combined默认`--verify`，自动带全四flags，确实调用本函数和build：5108行1905列、min0、W原精确值，退出0、stderr空、所有预检查原件未变；[执行记录](../combined-branch-master-program/rerun/execution.json)、[stdout](../combined-branch-master-program/rerun/stdout.txt)、[stderr](../combined-branch-master-program/rerun/stderr.txt)共享，不复制或重复入口。该全图运行沿用原实现，本包独立计算范围仍是36条新行。

原floor `--verify`只按位置读取权，不比较列描述符；tag不编码`--priced/--optimum`。因此单看PASS不能识别检查的是3995行子图还是历史4963图。原默认无verify模式会在脚本旁写exact/status；所有发现应在完整隔离布局执行，本包未启动发现。

[自查](self-check.json)核frontmatter、所有JSON、Markdown链接、回执targets和原件SHA；状态仅`local-prepared`，由主Boss串行保存与提交。
