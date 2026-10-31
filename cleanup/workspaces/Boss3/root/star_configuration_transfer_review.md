# 极小星配置保持与收缩稀疏族的独立冻结攻击

审查先从旧极小星整数接口独立重构，随后才读主证明。未读取其他未入库证明。

## 冻结对象

- minimal_star_contraction_and_capacity_gap.md：974332b1d8f919cc8dd994aadbd66f79c4b0703e15f1868bab4a2516e09dcaa0，第8节。
- sparse_conditioned_configuration_gap.md：88af645ff4ee5bd81afdeef2b67824ca34ed9183630c180373d1efa2d63c25f2，末尾收缩族章节。

## 攻击结论

没有仍成立的fatal objection。

- 外部逐配置至多一F保证占用质量Q等于外部任务质量，后者由v配置均为真子集而至少一。
- 前向其实只需Q≥1；配置包含多个F仍可先删全部F，再放一个最小值任务。Q并非宣称所有可能方法的必要条件。
- 保留普通边的强制质量不变。新e边须从指定机器优先选mass1；普通顺序可给完全错误的机器，独立负控制精确得到目标质量0与优先后1。
- 逆向用argmin和补集分布恢复可行性，但不能恢复全部原单边探针。两机例子已精确枚举合法配置验证。
- 每步全球最多一个拆分，支持界S-Sv+1成立。前向只加减与min，初始共同分母D足够，无迭代分母乘法。
- 逆向恢复v行按遗漏任务合并至多|F|，Σ|F|≤n_initial+m。
- 稀疏族端点F外部域不交；k=3左右任务不交、共享t2无妨。终态所有存活terminal三unit任务；core含一个unit入任务和k个small项；z的微小任务数不变，因此没有剩余极小星。
- 精确OPT下界用T恢复，上界改阈值theta再次正向压缩，双方向均有凭据。

## 已落实的非fatal措辞建议

- 明确“配置点转换位多项式”相对矩阵加给定显式证书总编码长度；不提供通用配置求解oracle。
- 显式说逆向不保全部probe，防止双向标题误读。
- 证据段分开主程序的整数调度恢复检查与独立程序的矩阵/配置/全部probe检查。

上述三项已逐条复核落实。最终无剩余实质objection。

## 独立实现范围

规范程序位于tests/audits/unrelated_machines/star_configuration_transfer_independent.py。只导入旧instance/certificate生成器；不调用旧verify，不导入主转换。自写实际矩阵收缩、全局greedy、强制边祖先跟踪、逐配置负载/归一、逐任务覆盖、强制边、大任务基数、支持增量与无极小星检查。展开k3 H5全部最终有限边，另有缺失互斥反例、反向probe反例及优先序负控制。程序仅stdout，不改旧冻结证据。

主目标UM-TARGET-v1仍开放。内部审查不认证全球新颖性、独立论文价值或外部同行评审。


## 主研究者核对与实际运行边界

被审基线为main e0e88bd1d1f5f1edf7516ff1fa189b8e733cae43加上本次两正文增补；
冻结正文hash由独立审查者实际读取后重核，记录见上节。内部子研究者不等于外部同行评审。
主研究者另从外部占用质量重建正向证明、以补集分布重建逆向证明，核查每一步
当前互斥、指定机器优先和批量支持不累乘；收缩后OPT上界与下界分别使用正确方向。

主转换代码将旧证书重复列合并后再转移；这是一项表示实现要求，不能直接用dict覆盖
相同配置的质量。程序另外检查零/空T0无规则、有理一次split、指定机器优先、缺占用拒绝、
完整逆恢复和旧整数上界压缩。全部最终1778条有限边（含972条替代任务边）均实际核验。
独立实现不导入主转换/验证器，只共享旧instance/certificate生成器；两路并非独立原始数据源。

序列化的终态矩阵与一个最高z配置负载的条件点另从JSON逐行重算：所有行归一、
配置容量、大任务槽、全任务覆盖、强制边质量1，整数上界5/3与无规则均通过。
具体输入/证书hash和软件版本在star_configuration_transfer_audit.json，旧冻结证据未改写。
有限证据只覆盖k3,H5；没有展开一般k，也没有求通用配置LP。

复现（仓库根；将输出定向scratch新路径）：

```sh
python3 tests/audits/unrelated_machines/star_configuration_transfer.py
python3 tests/audits/unrelated_machines/star_configuration_transfer_independent.py
```

主程序可选`--export-dir <全新scratch目录>`生成完整终态矩阵和条件点/整数上界证书；
拒绝覆盖同名文件。默认只stdout。没有通用近似算法实现或统一epsilon声明。

结论：两个新Claim在准确范围内可内部使用；无尚成立fatal objection。
Truth/Mechanism有自足证明；Value是可组合证书接口和具体预处理界面；Novelty、
独立论文价值与外部评审未认证，Ambition仍未达到UM-TARGET-v1。
