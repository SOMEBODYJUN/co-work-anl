# 完整156主题父方尾报告证据

[正式对象](../../../state/计算/完整156主题固定前缀的两人尾报告--计算.md)完整解释主源c51fd65f01191bd76a89的16字段、全部两人尾判据及范围。original目录保原报告、相关父方代码和代码实际读取的三份大数据；manifest.json逐项保源ID、冻结提交、字节数和SHA。

[verify_report_fields.py](verify_report_fields.py)是本轮新增标准库核验器，不导入父方枚举器、不运行客户矩生成器。它遍历全部24336矩位置、所有末位平局及全部可实现尾，再逐键重建完整原报告；[field-audit.json](field-audit.json)保156个BR数量、127个旧末位BR、精确门槛和成本差。

~~~
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/full156-tail-parent-report/verify_report_fields.py
~~~

原入口隔离复跑由同批程序任务负责，证据在[审计器目录](../full156-tail-parent-auditor/README.md)。该代码会覆盖其旁报告，不能直接在本冻结original目录运行。复跑不形成第二份客户矩实现；本轮独立字段核对同样仍依赖作者冻结矩。

收益共同分母是单位客户尺度的60倍，福利使用单位尺度。初版新核验器曾把八桶三位会员hist误当64型，已按实际文件纠正；正hist十项各有六个索引计数且T会员恰一。文件名10344和point内verified_rows5108分别保原身份，没有由名称补造行验证。原数据完整保留，相关源只作依赖阅读，不代为done。
