# 有限模板刚性、暂态植入与严格替代

八源完整字节、稳定ID、双冻结commit/path和SHA256在`original/`及`source-manifest.json`（36787字节）。数学和有限覆盖说明见[正式计算对象](../../../state/计算/有限模板刚性植入与严格替代的精确核验--计算.md)。四原程序只依赖Python标准库，输入内嵌，整数/Fraction，无随机、solver、浮点容差。

四`replay-*.json`是默认stdout原样实际输出，四stderr均空，exit均0。`replay-comparison.json`保存全部字段差异：刚性取冻结执行包装的result，二列取全报告，均无差异；两植入各只有历史--output与本轮stdout导致的command差异，所有数学字段相同。独立植入的result是状态字符串，不是包装对象。原冻结报告没有改写。

额外`export_two_column_certificates.py`复用原审计函数导出819个完整精确证书；新`replay-two-column-certificates.json`的证书流hash与冻结报告一致。它是透明导出，不声称独立第二实现。导出器exit0、stderr空，命令和hash记录在comparison。有限数据不代一般实参数证明，未外审、新颖性未认证。
