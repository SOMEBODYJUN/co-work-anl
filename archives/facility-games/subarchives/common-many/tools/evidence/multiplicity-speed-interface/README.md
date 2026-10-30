# 混合重数成本接口的两例算术核验

本资源对应[混合重数与相关机器转换边界](../../../state/障碍/混合重数与相关机器成本的转换边界--障碍.md)。

restricted_related_formula.py为源ID7fd34baa9214775b1841、冻结提交68fad804ec5946cb296f77dc5b336308a66abf12下 tests/audits/restricted_related_formula.py 的原字节副本，共1270字节，SHA-256为a61855c813389b795848948b597e34210c00234a058ddf115e8cef9b32a198fc。

程序仅依赖标准库Fraction。它有四个算术函数，main只检查一组等重数正样本和一组混合重数不匹配样本。它不搜索均衡，不处理任意原始JSON，不证明一般等价或复杂性。

本批已实际执行：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/multiplicity-speed-interface/restricted_related_formula.py
~~~

返回码0和完整stdout、所用Python、固定输入及范围见[formula_run.json](formula_run.json)。重做只输出终端结果，不写其他文件。请使用普通模式，不用 -O 关闭四个assert。

正文中的一般等重数结论来自代数推导；混合反例在正文另实现为完整三原子客户实例。历史论文链接、具体版本和后续仓库证明位置均列在正文，原论文未作为完整文件复制。本批没有运行blocking flow、贪心构造器或一般盒选择器。
