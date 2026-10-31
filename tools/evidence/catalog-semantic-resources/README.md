# 旧研究目录两源的实际语义清洗证据

两源正式claim `33571b39ae6cff72af5c94065dec119d0eb367c1` 已由Boss确认actual pushed/synced。全部2099条已实际阅读；原JSON/MD在original冻结，相关字节范围在related-manifest。

`catalog-semantic-records.json`保每条完整source_record、原索引、用途ID、正式资源去向、旧MDClaim前三/总数及两种关联索引；`purpose-dictionary.json`保1484不同完整用途；source_record回译与原JSON精确相等。`reading-progress.json`是实际阅读确认，不是数学认证。UM后部无损reading-views只在原用途字符串逐字相同时引用既读字典；视图生成不会自动确认阅读。先前会话中的原字段阅读没有补造转录。

`full-md-binding.json`是整份1596733字节静态重建结果，不是旧build_catalog执行；实际原JSON+assets+AST常量完整依赖均归档。`hidden-related-fields.json`说明14个related键未被旧validate/render读取，4空10非空。

当前正式五人半覆盖、弱iid反例和局部漂移全文实读副本/哈希在comparison；只有这些实际数学用于校正目录旧状态。未检查所有目录目标证明、未重跑旧成功suite、未额外done这些旁读源。source_refs是冻结原来源，不把历史当前目标/角色/授权当成现行指令。

本批新有限检查命令是`python tools/evidence/catalog-semantic-resources/check_resources.py`，这里只对派生完整性与真实字节绑定作2211项检查。若在结果仓执行，新脚本默认B为其所在证据路径向上三层；外部绝对比较repo路径只用于本地链接兜底，不是数学前提。

格式恢复：Root prepare发现总合同3个C0字符，前2198项未覆盖C0；仅派生正文将两formfeed+rac和一backspace+ar恢复为字面LaTeX控制序列，并补全部13页C0检查，新2211项通过。详见format-recovery.json，原件不动。
