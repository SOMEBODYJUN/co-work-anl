# 安全值搜索报告与循环种子证据

对应[自足审查对象](../../../state/审查/安全值搜索报告与循环种子--审查.md)。本目录只处理四primary：86baaa948961a2dcdb57、70b13b2c9d0ce481c738、6249d81b166c8d2b4b87、56bd7b24afb2d39b51b5。父方正常clean show串行导出的原文经本目录prepare脚本逐size/SHA核同后原样保存；未自行fetch/show、修改冻结原件或操作Git。

- [source-manifest.json](source-manifest.json)：四primary、完整来源路径、两冻结commit、size与SHA。
- [original/](original/)：四完整原字节JSON，不是截断摘要。
- [complete-record-read-index.json](complete-record-read-index.json)：全部根字段与124条含best/30bank的完整记录。相同整记录只存一次并列全部原位置；60组分别为cyclic30、n4/k5十四、n4/k6六、n5/k6十，可按位置重建全部原语义记录，原字节仍独立保存。
- [prepare_record_index.py](prepare_record_index.py)：仅保全、分组和全记录恢复等值检查，无原模块/DP/LP/随机运行。已执行一次。
- [verify_static_doubts.py](verify_static_doubts.py)：仅为n4/k5微负与生成器不相容、cyclic轨道/整数安全身份疑点作精确检查，恰执行一次。
- [current-static-doubts-check.json](current-static-doubts-check.json)：14个n4/k5输入的纯静态鞍点/PNE/OPT4，与30循环输入的126背景/全部原最小背景/轨道展开/所列叶覆盖。结论PASS_EXACT_STATIC_DOUBTS_ONLY。
- [current-check-event.json](current-check-event.json)、[stdout](check.stdout)、[stderr](check.stderr)：实际唯一checker事件、环境、耗时、脚本前后SHA、exit0及空stderr。
- [comparison-manifest.json](comparison-manifest.json)：实读成熟对象与原搜索器、指纹及比较角色。
- [related-initial-identity-comparison.json](related-initial-identity-comparison.json)：只提取另三报告的initial作完整字段/权向量等值比较，非三报告全文处置或其数学核验。common4、cone4明确复用search4保存记录；common5不等于当前search5任何保存权向量。
- [relation-review.json](relation-review.json)：实际数学关系及不能建立的推导，正式超图留第三阶段。

n4/k5的原微负是精确W−4v=0，保存4T3终局静态增益0；这不证明其SPE资格或全部最坏列表。循环30点的真正静态值及所列叶的正差精确核同，但没有独立恢复原SPE列表。其它两search报告的静态鞍点、SPE/IC/LP均未新增认证。

实际原程序导入、main、DP、SPE、IC、LP、随机搜索新执行均0；没有重跑已有双块成功证据。现生成器与报告存在可定位差异：n4/k5缺两诊断字段且bank都是PNE终局；n4/k6含38/42/43名全主题客户，而现main每次删全主题并只存nonPNE。保原字节与身份差异，不回填旧命令或制造原运行元数据。

所有结果仍为本地正文/证据，未由本子任务checkpoint、push或done；这段状态供交接使用，不能作为远端保存回执。
