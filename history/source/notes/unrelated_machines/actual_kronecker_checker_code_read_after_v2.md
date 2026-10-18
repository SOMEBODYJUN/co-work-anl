# 规范完整矩阵检查器的修复读后与实际错误证书拒绝

## 本次读取、执行与作用

已实际全文读修复版 `co-work-anl-boss11/tests/audits/unrelated_machines/actual_kronecker_product.py`，SHA256 `bb7d555bdfacc5b35e298ba57e20c72b243c09394932157f336aef765bd75d5b`。原版本异议/实际事件另冻在 `canonical_checker_original_objection_v1.md`，未覆盖。

实际运行修复版正确输入，输出另存本目录 `canonical_checker_baseline_run_v2.json`。实际变异只对本目录 `checker_mutation_fixture_v2/` 内的代码和三个数据文件的独立副本进行，不导入优化器，不改共享冻结材料；脚本 `review_checker_mutations_v2.py`，完整结果 `checker_mutation_review_v2.json`。

## 与canonical数学合同的一致性

base `time` 的八机十job顺序、两个finite端与F₂资格公式一致。ROOT按__file__定位仓库，不依赖当前工作目录。完整square输入的100job对、64machine对和每job finite mapping直接重建并比对，共400个唯一有限端。

seed每job恰两个finite端，1024份完整原job分配全部枚举，峰最小值精确3/2。两份证书分别是整数扁平目的地schema和含实际job/机器名的dict schema；dict分支逐项检查全部100个原job身份与真实处理时间，不把tuple身份忽略。两份完整分配都经同一Fraction实际负载回算且确实不同。

结构初态、15件同时替换、两对角2/两非对角0的初始缺陷及最终64行1都核到。四次幂确实遍历全部10000件原任务，按64×64机器编号聚合，4096个实际负载均1；这是有限四次幂核验，不能替代所有偶次幂解析证明。

本版现显式构造各job两端各半的primal并核八行全1；对偶八权总和1及目标1也精确回算。输出primal-dual value现在与代码所核内容一致。代码完全没有一般LP求解器、一般tensor算法或source-hardness编译，报告的limitations准确。

## 实际变异结果

在上述确切代码hash上，以下错误都实际返回非零，未写出成功结果：

- 所有100个扁平machine ID改成v−64；
- 一个机器0的ID改成JSON false；
- dict schema追加第101条row；
- int schema追加第101条或缺第100条；
- AA任务改派到原不可用RR端；
- AA任务改到另一个合法SS端、使实际负载不再全1；
- dict原处理时间改错；
- 原输入删去一条finite端。

失败点分别是严格类型/范围、raw总长度、资格、负载、原时间、完整矩阵mapping比较；不是依赖优化器。

另对已经存在的 `canonical_checker_baseline_run_v2.json` 再请求同一输出路径，程序实际拒绝，提示Refusing to overwrite frozen output；运行前后文件SHA256一致。预检查和open('x')均防止原位覆盖，后者也覆盖检查/打开间文件出现的情形。

## 精确保留的序列化边界

本版向某job的finite_edges原始list追加一条完全相同pair会被dict归并并接受；完整结果中如实记录了该accepted case。它没有增加或改变任何实际finite资格/时间，唯一矩阵仍400端，因而不是错误调度获通过；但本版**不保证原始稀疏list恰400条且每row无重复**。若需要严格冻结序列化合同，须另加row长度4、ID唯一与严格整数/范围检查后再审，不能把这一case记成已拒。

## 范围裁定

原负ID/额外dict记录/未显式primal三项实质异议均已修复并读后核验；错误实际分配/缺失任务/不合法端/错负载得到实际拒绝。当前规范数学检查作用通过，无一般LP-solver实现或一般hardness声明。重复同端序列化是明确保留的小范围接受行为，未抹去或误报。
