---
id: "unrelated-machines/kronecker-checker-version-and-sparse-guard-audit"
kind: "computation"
type_tag: "计算"
title: "Kronecker核验器版本与稀疏输入拒绝"
status: "version-matched-and-targeted-guards-replayed"
summary: "完整保留v2十项输入变异及拒覆盖、v3五项新增guard报告；由六行差分重建hash匹配的v2程序，另以新明确fixture定向复查最终v3五项拒绝，不重跑完整审计。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/actual_kronecker_checker_mutations_v2.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/actual_kronecker_checker_mutations_v2.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/actual_kronecker_checker_sparse_guard_v3.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/actual_kronecker_checker_sparse_guard_v3.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/actual_kronecker_product.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/actual_kronecker_product_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_checker_original_objections.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_checker_code_read_after_v2.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_checker_sparse_guard_addendum_v3.md"
---

# Kronecker核验器版本与稀疏输入拒绝

本对象整理两份不同代码版本的实际变异记录。**v2 并非全部拒绝：十项证书或矩阵输入变异中，九项被拒，一项“追加同端同时间记录”被接受；另一次已有输出路径请求被拒。v3 只新增复查五项稀疏列表规则，五项均被拒。** 这两个运行范围不能相加后宣称同一最终版本已经重跑所有旧案例。

本轮全文阅读两报告及其对应原始读后说明，依据 v3 报告内的六行差分重建出了与 v2 报告 hash 完全匹配的程序。另编写一个明确标注为本轮新实现的定向驱动，对最终 v3 的五类稀疏输入错误各运行一次；全部在种子穷举前拒绝，没有重复[完整Kronecker矩阵与双平方证书审计](完整Kronecker矩阵与双平方证书核验--计算.md)。原报告及原代码字节未改。

这些证据说明固定平方输入与两种完整调度证书的具体拒绝边界，不是任意输入格式的完备验证器、一般 UM 算法或新的数学反例。v2 接受冗余的相同边记录不改变其代表的矩阵，因此也不是接受了一份错误的调度。

## 资源、版本及真实依赖

| 对象 | 来源与保存位置 | 字节/版本 |
|---|---|---|
| v2 原报告 | 来源 ID 1d492950d6725c9890ee；[actual_kronecker_checker_mutations_v2.json](../../../../tools/evidence/private-tree/kronecker-checker-mutations/actual_kronecker_checker_mutations_v2.json) | 7700 字节 |
| v3 原报告 | 来源 ID 9836b2dba11f078bb586；[actual_kronecker_checker_sparse_guard_v3.json](../../../../tools/evidence/private-tree/kronecker-checker-mutations/actual_kronecker_checker_sparse_guard_v3.json) | 4324 字节 |
| 规范最终 v3 | [actual_kronecker_product.py](../../../../tools/evidence/private-tree/actual-kronecker/tests/audits/unrelated_machines/actual_kronecker_product.py) | 原字节 7505 字节；上一计算对象已保存其三个输入依赖 |
| 有据重建的 v2 | [actual_kronecker_product_v2_reconstructed.py](../../../../tools/evidence/private-tree/kronecker-checker-mutations/actual_kronecker_product_v2_reconstructed.py) | 7265 字节；由差分重建，非单独取回的旧源码文件 |
| 版本及范围核对 | [version_comparison.json](../../../../tools/evidence/private-tree/kronecker-checker-mutations/version_comparison.json) | 原报告 hash、重建方法、匹配结果和驱动缺口 |
| 本轮新定向驱动 | [replay_v3_guards.py](../../../../tools/evidence/private-tree/kronecker-checker-mutations/replay_v3_guards.py) | 仅新建独立副本并复查五项前置检查 |
| 本轮新结果 | [replay_v3_guards.json](../../../../tools/evidence/private-tree/kronecker-checker-mutations/replay_v3_guards.json) | 明确新变异内容、输入 hash、拒绝位置及原件未改核对 |

原 v2 报告 SHA256 为 fb37045f9d50e1bb89a62f647a355e1b3ed67a8d15cf7525e83445ec3f324b69；原 v3 报告为 227aa0c0a225cc8d482cecedaeeb9b2bceeaeafbbcaaaee01404f2c7a0f34159。报告中的 checker hash 与报告文件自身 hash 是不同身份，不可混用。

### 三个版本及其证据身份

| 版本 | checker SHA256 | 可据此断言的范围 |
|---|---|---|
| 初版 v1 | bf559a00581730d68684ddf28e8a331975ca86f5cdc5246c89506d2df0fd3f62 | 原说明记载正确输入曾通过，三项缺陷由读代码得出；旧变异尝试因版本已变化而中止，没有 v1 已实测接受错误输入的结果 |
| 修复后 v2 | bb7d555bdfacc5b35e298ba57e20c72b243c09394932157f336aef765bd75d5b | 本批 v2 报告对应此版本：九拒、一接受，另拒绝已有输出；半半 primal 已实际回算 |
| 最终 v3 | 8e95e8c4b00654b2e85efbd37e294837796755ce189e7e933e5200752abebbb3 | 唯一新增为六行稀疏输入检查；本批 v3 报告只重跑五类新增检查，完整正确输入由另一规范报告承担 |

v1 负编号问题有明确语义机制。对原合法机器编号 v=8i+h，同改为 v−64 后，有 divmod(v−64,8)=(i−8,h)，Python 的机器数组和负载数组负索引都别名回原位置；False 也可与编号 0 混同。初版未做严格类型/范围检查，会沿这条路径把错误编号解释成合法端。原记录明确这是代码语义推导，未虚称已经对旧版本运行该变异。

初版的字典证书分支只遍历前 100 项，多出的第 101 项可能被忽略；输出又称 primal_dual，而当时仅显式算了 dual。v2 增补 raw 长度、严格编号和原初八行负载检查。上述历史与本轮只读核对不能混记为本轮重新实施了 v1 或 v2 实验。

## v2 完整报告：接受行为也必须保留

v2 顶层 reviewed_code_sha256 绑定上述 bb7d555b… 版本；两个布尔字段记载当时只改独立 scratch 副本、未改共享文件。这是原运行者的冻结记录，本轮原样保存，不用它替代本轮另外记录的原件 hash 检查。

| 原 case | 原报告结果 | 代码拒绝点或接受机制 |
|---|---|---|
| negative_all_machine_ids | returncode=1；accepted=false | verify_square 的严格 int 与 0≤ID<64；原读后说明明确全部 100 个编号改 v−64 |
| boolean_machine_id | 1；false | 同一严格类型检查，False 不能当 int 0 |
| extra_101st_dict_row | 1；false | 两种证书分支之前的 len(raw)==100 |
| duplicate_sparse_input_entry | **0；true** | 追加完全相同端/时间后，字典构造合并重复键，代表的完整矩阵仍相同 |
| ineligible_aa_machine | 1；false | 原种子双坐标资格检查，AA 改到不可用 RR 端 |
| missing_100th_integer_assignment | 1；false | len(raw)==100 |
| wrong_dict_processing_time | 1；false | 显式 p 必须等于两个原处理时间之积 |
| finite_edge_but_wrong_loads | 1；false | 目的地虽有限，重算后全部 64 行不再等于 1 |
| extra_101st_integer_assignment | 1；false | len(raw)==100 |
| missing_finite_input_edge | 1；false | 重建矩阵与输入字典列表完全相等的检查 |
| refuse_existing_output | returncode=1；refused=true | 输出已存在，给出 Refusing to overwrite frozen output；原报告另记 output_hash_unchanged=true |

前十项是输入变异，最后一项是输出写入行为。九项拒绝的 stdout 均为空、stderr_tail 给出对应断言及历史路径；接受的重复端案例保留正常通过摘要，包含 1024 份种子分配、两证书、十五项改派、四次幂及种子 primal/dual 的旧运行结果。不能把这个完整成功摘要删除后只摘录“多数错误被拒”，也不能把摘要当作本轮又完整运行了一遍 v2。

重复端的接受只表明 v2 未承诺原始稀疏列表恰为 100×4 条且每行不重复。对同端同时间的追加，去重后仍为同一 400 条有限边矩阵，未改变任务、可用机器或负载。它是序列化合同的缺口；不能据此指称数学反例失效或 checker 接受了不合法实际调度。

## v3 的六行收紧与五项实际拒绝

v3 报告的 v2_to_v3_diff 保存了以下唯一新增代码，位置在完整矩阵映射比较之前：

~~~python
    assert len(inp['finite_edges']) == 100
    for row in inp['finite_edges']:
        assert len(row) == 4
        ids = [i for i, _ in row]
        assert all(type(i) is int and 0 <= i < 64 for i in ids)
        assert len(set(ids)) == 4
~~~

本轮从原 v3 字节中仅移除报告所列这六行，所得 7265 字节 SHA256 精确为 v2 报告绑定的 bb7d555b…；保留文件及 version_comparison.json 记录此可复核重建。此过程没有推测其它旧逻辑，也未执行重建的 v2。重建代码现在是平面版本存件，原来以 parents[3] 查输入的逻辑仍保留；若需运行，须另在独立 fixture 中恢复 tests/audits/unrelated_machines/actual_kronecker_product.py 及同根三个输入路径，不能在当前平面位置直接调用。

| v3 原 case | 原报告的拒绝点 | 与旧模型的区别 |
|---|---|---|
| duplicate_same_endpoint_appended | len(row)==4 | 关闭 v2 曾接受的第五条同端记录 |
| duplicate_same_endpoint_replaces_distinct | len(set(ids))==4 | 行长仍四，但有重复 ID；先检查原记录，不靠去重后矩阵缺边才发现 |
| row_boolean_id | type(i) is int 且范围 | 原稀疏输入 ID0 写为 false，不能借字典键等同性混入 |
| fifth_entry_in_row | len(row)==4 | 第五条不同端同样在原记录层拒绝 |
| extra_101st_finite_row | len(finite_edges)==100 | 输入任务行总数必须精确匹配 |

五项 returncode 均为 1，rejected 与 no_success_output_created 均为 true，stderr_tail 分别指向上述六行内的断言。报告声明 only_new_sparse_guard_retested=true；这个限制不能省去。它没有逐个重跑 v2 的九类证书错误，亦不是初版 v1 的拒绝证明。原资格/时间字典完全比较继续存在，因此新增语法规则没有改变合法数学实例或调度/LP 检查定义。

## 原驱动缺口与本轮必要定向运行

全仓按驱动文件名检索，仅在两份历史说明中找到 review_checker_mutations_v2.py 与 review_sparse_guard_v3.py 的名字；本批报告不包含驱动源码或完整变异后的 JSON 文件，也未检索到对应独立来源 ID。历史 stderr 中的 scratch 路径是当时运行位置，不是现在可依赖的可重放资源。两报告仍可完整理解和保存，但不能声称现在已经按原驱动、原变异字节重放历史实验。

本轮为直接检查唯一新增的六行写了新驱动 replay_v3_guards.py。它依赖上一计算对象已保存的最终原 checker、完整平方输入和两证书，只使用标准库。每个 case 在新工作目录建立独立副本，保持原根目录结构、原代码字节和证书字节，仅修改输入 JSON；调用未经改动的最终 checker CLI。

五个新 fixture 的具体操作全部固定，未假装与缺失的旧 fixture 字节相同：

| 本轮 case | 具体新变异 |
|---|---|
| duplicate_same_endpoint_appended | 向 finite_edges 第 0 行追加该行第 0 项的副本 |
| duplicate_same_endpoint_replaces_distinct | 用第 0 行第 0 项覆盖同一行第 1 项 |
| row_boolean_id | 把第 0 行第 0 项的机器 ID0 改为 JSON false |
| fifth_entry_in_row | 向第 0 行追加 [2,"1"]；ID2 不在原四个 ID0、1、8、9 中 |
| extra_101st_finite_row | 追加第 0 行的副本作为第 101 行 |

本轮普通 Python 3.12.14 下每项只运行一次。驱动不仅要求非零退出，还要求 returncode=1、stdout 为空、尾部为 AssertionError、stderr 中出现预期断言且没有创建成功输出。五项全部满足；所触发六行在 seed_options 构造和种子穷举之前，因此没有重复种子 1024 次枚举、两证书检查或四次幂构造。运行前后最终原代码与三个原输入的 hash 全部一致。

需要再次调用时，必须指定新的工作目录和新的输出文件：

~~~bash
python3 tools/evidence/private-tree/kronecker-checker-mutations/replay_v3_guards.py \
  --work-dir cleanup/workspaces/Boss3/private-tree/v3-guard-new-fixtures \
  --output cleanup/workspaces/Boss3/private-tree/v3-guard-new-results.json
~~~

保存的新结果给出驱动及原代码 hash、原依赖 hash、每个变异后输入 hash、实际首行及行数、具体拒绝位置。没有旧驱动也能复现这些明确的新案例，但不能据此回填旧报告的任何执行事实。没有重跑 v2 的接受项、旧负编号实验或已有输出拒覆盖测试；这几项当前仍以精确历史报告及代码关系为证据。

## 用途、关系及未覆盖范围

这两份来源给[完整矩阵反例](../反例/完整矩阵Kronecker偶次幂坍缩--反例.md)补充“数学见证正确”和“输入记录会被怎样检查”的区别：同一数学矩阵可以有不同原始记录表达，v3 在不改数学实例的前提下把这种表达固定为 100 行、每行四个不同严格整数端，再比较原资格及时间。完整正例的规范重放见上一计算对象；本对象只承担版本及指定错误输入的证据。

本轮还为版本关系全文比较了三份历史说明：cb2d91934f58059179de（初版异议）、30e302f02f337c8c4b75（v2 读后）、bcce655bc830b0b0f58c（v3 补充）。这些是比较读取，不把三份来源自动记为已完成清洗。原说明的独立性和运行顺序保持原状。

此处不主张所有畸形 JSON 均被拒绝，也不把 hash 匹配当作算法正确性证明。可复用的是确定版本、完整原报告、可核重建的 v2 字节、最终原 checker 及五项新明确 fixture。若后续必须复现历史驱动的每个精确变异，需要补取得旧驱动或旧完整输入；若扩展为一般验证服务，需要另立接受语法和拒绝行为合同。当前材料没有一般 LP 求解、普遍调度算法、源困难性或所有乘积均失败的结论。
