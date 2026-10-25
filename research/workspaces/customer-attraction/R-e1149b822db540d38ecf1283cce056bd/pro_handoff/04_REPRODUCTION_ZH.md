# 可复核交接与精确计算

## 先验证 ZIP 的逐字完整性

解压后，在 `Q-CAG-HALF-5/` 内运行：

```sh
python3 verify_bundle.py
```

这只检查本包清单的路径、大小、SHA-256 与无额外未登记文件；不等于数学审查。源文件由冻结提交逐字提取，并以 Git blob 身份校对；原证书未因打包而修改。

## 原模型求解器

在 `source/` 内运行：

```sh
python3 -m unittest tests.test_customer_attraction -v
```

核心 `customer_attraction` 包只用 Python 标准库和 Fraction。`Instance`、`ExactSPESolver`、`verify_certificate` 的精确合同见 `customer_attraction/README.md`。完整证书的 actions 以有序历史为键，核验全部节点的一步偏离。压缩客户整数重数是多个不同单位客户，不是更换玩家权重。

## 数学证书的可选重放入口

仍在 `source/` 内：

```sh
python3 research/workspaces/customer-attraction/R-ae18a85a07214b22b7b9d614c34779e0/countersearch/audit_shared_root_math.py
python3 research/workspaces/customer-attraction/R-ae18a85a07214b22b7b9d614c34779e0/dual/separate_shared_root_audit.py
```

第一份不导入发现器，核根 COPY、四尾二值背景、容量和精确乘子/K 列；第二份是独立于发现器的活跃行全类型整数定价实现。后者使用 NumPy，并按原脚本的默认行为输出 JSON。

需要做重放时，请先复制工作树或重定向脚本输出位置，保留本包原始冻结证据供比较。已有审查中区分了“另写实现”“复用已审实现重跑”“独立数学重构”；不要把重复运行称为新的独立审查。

探索脚本常用 NumPy、SciPy（HiGHS/线性代数）和少量 SymPy。各历史实验版本、seed、输入与输出沿原文件保留；本包不虚构统一的版本锁定，也不保证旧脚本在任意新环境无改动运行。静态可解析的仓库内 Python 导入依赖已补入，运行某条探索路线前仍需读它的自身 README。

## 证明与发现的判据

- 浮点 CG/LP：仅发现乘子或分离点。受限 primal 是原问题的外松弛，不必能补成 SPE。
- 有理恢复：检查乘子非负、每条实际使用行的真节点语义、全客户类型域非负及所有辅助标量列。
- 只有完整类型域定价并经过数学适用性核对，才可以把证书用于任意目录和客户数。
- 真反例：必须有整数客户、共同目录、完整有序策略/解析规则、全部子博弈激励和严格 2W<OPT₅。

本次打包只完成文件级来源与完整性核验，引用原记录的实际数学审查范围，没有重新执行全库数学审计。
