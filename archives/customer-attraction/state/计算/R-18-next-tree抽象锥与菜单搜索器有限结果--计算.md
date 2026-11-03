# R-18 next_tree：抽象锥与菜单搜索器的有限结果

## 稳定来源与范围

本页处置三个清洗源：`08f7bce19d1d835bfbd4`（`next_tree/abstract_cone.py`，1895 字节，SHA-256 `75b6fdc7f27c1d02e3570eae8ad7e303fe14474641f7378ad3e098c20a6ca379`）、`e77639427f0940cb0f13`（`abstract_test.py`，1212 字节，SHA-256 `70a49e1128da9d6570a4f74db2f3b3e16ddc67e56a63510449cfaa8850fcf1f7`）和 `abb5ed83a401bad92cd0`（`menu_search.py`，2283 字节，SHA-256 `42fb7be32b2009d71bd34f17dac17af4c37377aa26598e5c2b150d96ebbf234f`）。原字节、运行输出和相关输入保存在 `archives/customer-attraction/tools/evidence/R-18-next-tree-20261031/`。

三份程序都是探索性有限搜索，不是当前六提供者、六主题 CAG 的一般证明。`abstract_cone.py` 在三人四动作的匿名势函数空间中随机生成可实现的动态最优响应树，再用线性规划寻找“最差 SPE welfare 与菜单均值”的正差；`abstract_test.py` 在三人三动作的整数匿名势模型中随机生成势/基线，并直接测试菜单上界是否严格超过 SPE welfare；`menu_search.py` 从冻结的 `individual_security_failure` 策略读出完整历史动作，构造个体客户类型的覆盖矩阵和固定策略 SPE 约束，在一组 Dirichlet 菜单分布上最大化共同菜单价值。

## 实际运行与结论

- `abstract_cone.py` 逐字运行 300 个种子（每种子 `n=3,p=4`，10 个菜单查询；SciPy HiGHS），退出码 0，输出 `none`。没有返回正 gap 候选；这只是该随机锥搜索的有限负结果。
- `abstract_test.py` 逐字运行 10000 个种子（`n=3,p=3`），退出码 0，输出 `none`。没有找到 `n*v_menu>W` 的匿名势候选；不等价于对所有势函数的证明。
- `menu_search.py` 的原始默认输入集合在本 clone 只有 `individual_security_failure.json` 可用，因此按真实边界只运行这一项。输入来自已保存的三提供者六主题完整策略，路径 `(0,3,4)`，得到 5 个菜单，最优 `n v_menu/W=0.9999999999999998`，在浮点误差下等于 1，没有严格菜单超越。运行时曾直接执行默认列表并因缺失其它输入失败；该失败已保留为 stderr，随后用明确单一参数重跑成功，未把缺失源伪装成零结果。

## 数学解释、比较与缺口

`abstract_cone.py` 的约束同时编码完整历史动态最优反应（`rows`）和菜单付款上界（`M`）；其 `linprog` 目标是测试一个特定匿名势类中的有限候选，不产生 CAG 单位客户数、六提供者约束或纯 SPE 全树证书。`abstract_test.py` 的整数势与基线独立随机化，结果 `none` 只说明 10000 次采样没有命中，不排除构造性或非匿名反例。`menu_search.py` 与已归档的个体安全证书共用策略骨架，但其 `types=1,...,2^p-1` 只表示六提供者二元标签类型，且矩阵按固定策略终局菜单计算；它只检验该冻结策略与有限查询菜单，不检验其它完整历史策略，也不证明 `menu cap <= W/n` 的一般命题。

因此三源均作为 `finite-search-retained`：保留代码语义、准确运行范围和负结果，供第三阶段把“抽象锥无采样命中”“固定个体证书菜单比值约为 1”与 CAG 主目标分开引用；没有新增半覆盖反例，也没有消除 Q-CAG-HALF 的开放缺口。
