# 因子二存在性逆向审计的冻结代码重放

这是[因子二逆向审查对象](../../../state/审查/因子二逆向审查与证据边界--审查.md)的必要复现资源。本次 Boss3 逐份实读两个源程序，从冻结提交 68fad804ec5946cb296f77dc5b336308a66abf12 原字节导出后，实际重跑逆向审计。未修改算法，未把重跑称为新的独立算法实现。

| 本地文件 | 冻结源 | SHA-256 |
| --- | --- | --- |
| [definition_check.py](definition_check.py) | tests/multi_facility/definition_check.py，来源 ID a3aba04c18309f931c43 | 8d67c24a98643b79aa7f4f8d6c8cd1386516d95d3f04aff914b37663129a0cc1 |
| [run_reverse_audit.py](run_reverse_audit.py) | tests/multi_facility/run_reverse_audit.py，来源 ID c6789b73feeb28f3fe39 | 3ea7b07f8d46e1176242e518fb12205cd495bb27b7da7f6b3c0f8f760fd7b716 |

本次实际生成的[完整 JSON](replayed_reverse.json)与冻结 evidence/runs/kfac_two_reverse.json（来源 ID c83a0ca89061ee73d3ef，SHA-256 e99925c782c09debb127dd3342832be8cde3e831b73d52c4d698be5c8e383aed）在仅排除顶层 python 字段后逐内容完全相等。旧版本为 Python 3.13.5，本次为 Python 3.12.14。比较详情及所用文件哈希在[比较回执](replay_comparison.json)。

检查 612 个输入、全部 1728 个并列带标签站点分配最大者、6845 次实际偏离纯 NE 坐标极值、3479 个不同子博弈、6845 个转移预算；包括 83 个正交叠源客户预算和 555 个消失源检查。另对 7 个对称菜单族参数检查 274 次实际偏离。

两个程序不导入主构造器、装箱例程或纯改善动态。定义检查器直接重算含自身重量的原子条件成本；逆向程序直接枚举小输入全部纯 NE 并取偏离者最小收益，另检验对称菜单族显式零收益偏离见证。其独立性是相对于构造器的代码路径，而非独立同行评议。

从结果仓库根执行，输出另选新文件，保留这里已保存的本次结果：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-reverse-review/run_reverse_audit.py --output /tmp/factor_two_reverse_fresh.json
~~~

程序的唯一运行依赖是 Python 标准库和同目录 definition_check.py。源程序本身允许覆盖输出，因此调用者应选择新输出路径。

有限检查不能证明任意输入的定理，也没有枚举所有混合 NE。本轮没有重跑历史构造审计、布局障碍审计、CLI 或原完整仓库回归；相应数字在审查正文中保留为有版本范围的历史记录。必要依赖被引用和保存，不等于给这些额外源 ID 申报清洗完成。
