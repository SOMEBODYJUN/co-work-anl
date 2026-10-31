# take/continue 实际反例：审查层级纠正

审查者：general_query_response_review。2026-10-18。

## 必须纠正的实际读取事实

此前实际全文读取的source为：
/workspace/scratch/038d9dcc4cac/partial_sum_take_continue_flat_menu_actual_escape_exact_v1.md

SHA-256：27d2926563eeb34591ca44a75cf09ca623719827a67eedff485edf78e22053ac。

该文件虽然命名为Exact，但并非statement-only。其§4已经给出达界bundles、全部原jobs的实际调度、各机负载、root u_1 jobs被迫外送的完整解析lower，以及V的直接上界；§1也已给source SC=0的论证。这些内容在我的实际读取中均可见。

因此，原记录的“Exact-only独立审查/重构”标签不能作为“只见陈述、未见作者证明内容”的严格独立盲重构证据。原记“未读作者Proof”若仅指未打开另一份单独命名的Proof文件，属于文件访问事实；若解读为未见作者证明内容，则不准确，本补记明确撤回该解读。不能因为文件名是Exact而把其中已读的证明排除在污染范围之外。

## 本轮工作的准确身份与仍成立的证据

本轮实际工作是：读取含证明的完整source，逐对象重建其明确矩阵，核对所给bundles及全部jobs调度，检查原source中解析上/下界的正确性和量词范围，并独立执行精确Fraction原矩阵回算。它是实际构造/证明与原矩阵核验，不是严格statement-first盲审，也不是独立发现该反例或证明路线的认证。

具体仍有效的核验：
- Source SC max-min为0的鸽笼论证正确。
- 9 selectors、21 incidences、30 jobs、15 private及11 resource machines、57 finite entries的完整矩阵计数正确。
- 给定assignment确实执行全部30 jobs，包含未选off-state jobs；峰8/5、partial质量2/5。
- 任意partial的u_1资源上界、任意actual C<8/5的强迫外送矛盾，及局部take/continue合同的准确范围均已实际核查。
- Fraction证书是本审查者按已读source表与指定witness生成和运行的数值核对。源文件已告知witness和预期峰，因此它不应被描述为未见构造或目标值的盲检，更不是求最优的有限穷举。

以上数学结论不因审查层级纠正而改变；严格独立证明环节必须由此前未读该source的人，仅据真正statement-only陈述另做，不能由本补记追认。

## 原字节冻结与记录边界

保留原审查，不回改历史：
/workspace/scratch/038d9dcc4cac/partial_sum_take_continue_flat_menu_actual_escape_exact_only_review_v1.md

SHA-256：690700b71ff3e86756dd3b9b2c29e926d831442f47d548ff77dcf178196ecd14。

保留原Fraction证书：
/workspace/scratch/038d9dcc4cac/partial_sum_take_continue_flat_menu_actual_escape_independent_fraction_check_v1.json

SHA-256：9cf13ec0f81346889d177095e1c04b0dac13230ff8fd13f3fc8d23e537edd2f7。

本纠正另立冻结，仅scratch新增；未改repo/Work/Git、原source、旧审查或证书。未读取新造statement-only文件或接触新reviewer输出，不冒称参与新盲审环节。

**最终身份：含作者证明的source实际读后与完整原矩阵核验通过；原690700...记录不得作为严格Exact-first独立盲证明证据。**
