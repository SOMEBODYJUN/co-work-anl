# 成本支持失真与移动者补偿证据

[正式计算对象](../../../state/计算/成本支持失真与择证补偿的精确核验--计算.md)解释四程序的模型、内嵌参数、全部功能、计数单位与失败边界。10份原件及双冻结commit/path/hash在`original/`和`source-manifest.json`，原字节147385字节。

四程序仅依赖Python标准库，从`original/`运行规范相对路径，无外部输入。四份`replay-*.json`为本次完整原样stdout，四个对应stderr文件均空；`replay-comparison.json`记实际命令、环境、exit与所有差异。四次exit0，和对应完整冻结JSON比较差异均为空，无字段豁免。

独立近似支持程序使用`random.Random(20261015)`；其他三程序无随机性。全部费用及margin使用整数/`Fraction`，无solver、浮点或容差。full计数包含proper子集，奇环独立列数按每列两倍率计、外层degree之间可重复，不把它们误作不同列总数。有限验证不代一般证明，未外审、新颖性未认证。
