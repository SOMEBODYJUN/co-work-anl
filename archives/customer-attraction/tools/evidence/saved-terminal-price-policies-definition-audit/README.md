# 保存价格策略的定义级有理核验

本次新建标准库Fraction实现，直接读取两份冻结JSON的客户类型、整数重数及全部有序动作表；不导入规范验证器、原发现器或LP。顶层actions为列表对，certificate.actions为字典对象，先规范化为history→action并核全域相等，再逐历史比较沿同一策略的真实后缀收益。首次运行因误以为两编码字面相同而断言失败；修正为上述语义比较后运行成功，未改变输入/策略。报告完整保存1812项含自身比较、静态带重复最优与输入SHA；四人6客户实例W5/OPT6、三人1客户W1/OPT1，全部IC非负。价格z/score和clones不参与核验，不声称任何价格最优或一般定理。

运行：`python3 audit_saved_price_policies.py <four_price_best.json> <three_price_best.json>`。原输入路径和SHA见report.json。
