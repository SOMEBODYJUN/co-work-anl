# 多见证共享收费规范 Fraction 程序的实际源码审读

对象：`co-work-anl-boss11/tests/audits/unrelated_machines/multiwitness_shared_job_fee.py`，实际 SHA256 `0697e1b9da8a26c4ba1e7808e272ffa720a52e7ea09b975c962a101adaae64c6`。

时序：此规范代码是在此前独立 Exact-first 数学审查、独立枚举、作者 Proof 读后与 canonical 第6节终审之后才提供。本次确实读完源码全文，不将此前数学/独立程序审查冒充已审此代码；没有再扩大完整分配枚举。

源码审查通过，未找到 standing fatal：

- `construct`显式列原q/x/f各两个原目的地，机器编号`H_r=r,A_r=p+r,R=2p,S=2p+1`互异且与正文一致。
- `actual`对每个原job的原资格直接按mask取一个端，使用Fraction逐台相加；未调用OPT或费用公式求真实峰。循环从0到`2^(2p+1)-1`覆盖全部完整原合法分配，低p位恰是原queries模式，f位恰是原f的owner费用。
- 每个pattern、每个fee分别保留穷举出的最小实际峰及原assignment mask；这些实际值独立于`formula_fee`与OPT公式。随后才将实际最小峰/费用与待审公式比较，所以主oracle没有循环论证。
- 全部pattern包含空集。beta集合含1、3/2、近2，以及`B,c+B`和两种实际fee最小峰的准确端点及其两侧区间内点；保留`B=beta`、`c+B=beta`的闭阈值比较。对beta=2另核fee0分配存在。strict1 iff、原OPT1与sigma0/sigma_r也直接由原分配峰核验。
- 非空tradeoff另用公式singleton条件作为触发器；它不是额外独立singleton oracle。但此前对同一case每个pattern的实际fee已独立比较过，主费用/OPT审计仍独立。没有把这个辅助循环冒称新的普遍证明。
- 统一容量、异权、精确`c+sum b=1`、nearunit费用源、tiny查询初态及p=1均有明确cases；原v1空集严格和式反例作为可执行断言保留。有限范围没有冒充一般证明或source decoder。
- `--output`为required，先以`exists()`拒绝现有路径，最终以`open("x")`写入，避免检查与写入间竞态覆盖；输出另保源码及可选source-file的SHA。它不会默认重写冻结结果。

只补做了一个不进入枚举的拒覆盖实际检查：把`--output`指向此前独立审计已存在的`multiwitness_fee_fraction_audit.json`，程序立即退出2并报`output already exists; choose a new path`；未执行新的枚举。该旧JSON读后SHA仍应为已冻值`d76e97007447f87c3c1c4d7d5d7ec520a8a3bbb1f85dd63f71761597f61f9afc`。

本记录只认证已读源码和上述有限程序合同；root报告的113cases/287104assignments/3004patterns/19832thresholds由root实际执行，本记录不冒称本审查者也重跑了这一批枚举。
