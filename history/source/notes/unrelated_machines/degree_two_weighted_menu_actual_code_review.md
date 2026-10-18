# Degree-two weighted-menu backend：独立实际代码审查

审查者：general_query_response_review。2026-10-18。

**实质结论：当前 core 与 audit 通过，未发现算法或原任务恢复的 fatal。** 本文件只记录实际读代码及独立运行范围，不修改或替代此前冻结的数学审查。

## 冻结输入

- core `tests/audits/unrelated_machines/degree_two_weighted_menu_backend.py`：`3ac389c7ab6bf1037c51d744d18e6191b5be8df1ba559e731fbbcaf4ebcc3c99`
- audit `tests/audits/unrelated_machines/audit_degree_two_weighted_menu_backend.py`：`2a6b5b009ecedc417343fe42b44113aaf513b7e661756005fdd6738e71979a3d`
- fixtures `examples/unrelated_machines/weighted_menu_joint_fixtures.json`：`59501d74f2c092af8cbf56921987436b160274db325f4f30b69b058c10edf72f`

审查者实际读完 core 416行、audit 220行、全部fixtures及原 frozen audit report，并遵循本次只读repo/只写scratch的指令。导入和执行使用 `-B`/禁写bytecode，没有向repo写入pycache。所有新运行落在本独占scratch目录，原数学记录、源代码、原freeze及Work/Git均未改。

## 静态代码审查

1. **强制最大项与两端移除。** `vw_threshold`中active只表示仍可二选的items。force-largest的必要性条件恰是`available+private-largest<T`；强制时先置inactive，在两个端点都扣available，仅owner端增加private。既有固定项计入private，不会再参与pairing。每item只强制一次，available不重复扣。
2. **队列关闭。** 两个受影响端点均重新入队，queued只防止同时重复排队，不跳过后续处理。已弹出owner也重新入队，使下一最大项继续受检；已处理过的另一端能被后向级联重新激活。ptr只越过inactive条目，静态降序列表过滤后仍是live降序。出队结束后逐agent断言`tail+private≥T`验证强制闭包。
3. **Pairing及迭代BFS。** 每active item两occurrences连接job边，各agent连续live项连接相邻pair边。每vertex一条job边、至多一条pair边，循环交替而为偶环。源码用deque迭代BFS、无递归DFS，选一种颜色使每item恰一owner，并回算全部utility与T/2保证。
4. **单向二分。** `high=min(initial_totals)+1`有有效初始拒绝证书；成功仅更新low及保存allocation，失败才更新high及其forced证书。未把成功当T精确可行，也未假设accept单调。终止`high=low+1`、真实整数aux OPT<high，故low≥OPT；保存allocation≥low/2。fallback适用无positive items或aux OPT0，仍每retained item选一合法端。
5. **精确权值和determinism。** private p解析为Fraction，明确拒绝float/bool/decimal/exponent shorthand；averaging按group做，清分母用lcm不复制item。排序按`(-weight,item_index)`、固定group/item顺序及选态`(mass,-index)`打破tie；无随机后端。顶端取消CPython decimal-digit上限，允许显式大有理编码。完整search trace可能随编码长度二次增长，仍是bitpoly，不是数值份数展开。
6. **Normalization及group层。** 每欠量indexed state只添一个tagged bonus resource/job，W=0/empty state也适用；原resource与bonus键命名空间隔离。所有states贡献同一个group auxiliary agent的平均，positive agents数保留≤2；zero edges仅从辅助allocation省略，原zero jobs仍保留。
7. **原jobs一一恢复。** `original_jobs`用selector/group及incidence/group/state/resource四元标识，私有machine与resource machine有不同tag。一个selector只放所选state；仅该state且获分配resource的jobs export，其余全部原incidences各回私有机。重复indexed states有不同机器和原jobs，不会合并丢失。
8. **Bonus投影与完整负载。** 内部从原完整loads重建normalized bonus jobs；被选且获allocated bonus者去独有resource，否则停其state机。断言normalized peak恰`2−min(chosen_mass)`，投影后原C不增，且chosen mass≥group平均utility。不存在仅输出所选state jobs的遗漏。
9. **实际时间和验证器。** 输出start/finish按各machine累计负载构造；verify核全部原jobs恰一次、原资格、真实p、非负start、finish关系、正长区间不重叠及实际peak。它验证此后端的紧凑实际输出；不是任意带idle调度的通用容许性判定器，也不单独认证approximation ratio。
10. **非法语义输入。** 代码检查空groups/菜单、重复resource/group/state/incidence、未知resource、负p、row sum>1、非精确p、非字符串ID及resource跨三groups；degree统计包括零权membership，符合Exact。此审查不声称完成任意JSON schema fuzz或提供所有缺键/容器错误的统一异常API；backend仅解释声明的groups/resources结构，不是任意raw UM适配器。
11. **无OPT/brute生产路径。** core imports仅stdlib。`solve→parse/normalized_auxiliary/vw_two_approx/original_jobs/verify`，后端只调threshold与utility；core没有brute函数、product、LP、外部solver或audit导入。枚举OPT只存在独立audit/harness，未混入production solve。
12. **Frozen IO。** audit必须显式`--fixtures`与`--output-dir`；先`mkdir(exist_ok=False)`，两个输出再`open('x')`。已有目录即拒绝，文件也不覆盖。失败可能保留新建目录，不能把非零退出当成功freeze；本次成功包的两个文件均完整。

## 实际独立运行

所有结果详见本目录`independent_results.json`与`provided_audit_replay_checks.json`；运行脚本分别为`independent_code_checks.py`、`run_provided_audit.py`。它们是独立有限审计，不由core调用。

- **4681个穷尽小backend输入**：两agents，0–4items，degree1或2、每端权1或2。独立枚举真实additive OPT，并作20522次整数threshold调用，逐次核成功≥T/2、失败⇒OPT<T、最终low≥OPT且high>OPT。实际看到225次T>OPT仍success，验证二分确实没有当成精确feasibility。
- **反向force闭包**：1800agents路径，起点private item，末端开始反向强制1799items，所有先前已处理agents被重新入队，最终min utility1。删private项则最终sound failure。专门覆盖两端扣除和回队。
- **长pair环**：1800agents、3600incidence vertices，T1无强制，迭代BFS得每agent utility1，超出典型Python递归栈规模。
- **140个结构实例**：固定seed20261018，含不等menus、私有权、zeros、empty states与bonuses。独立直接从JSON构造所有原job资格，不用core原job表，枚举26265份完整原assignments取得实际OPT，再逐一核relative-OPT界、ratio及完整真实输出。
- **大显式菜单**：一组2600个empty states，恰一原selector输出、2600bonuses内部处理后删除、K2600、原makespan1；不依赖固定K循环上限。
- **原5002位分母回归**：精确输入`p='1/'+'1'+'0'*5000+'1'`现solve成功，C1，16613次binary调用；大integer-scale转字符串与末次大整数threshold JSON编码成功。未写出其约二次长度的完整trace。另以同样超长N/N通过真实CLI输入解析、完整JSON输出及独立schedule回算。
- **标识和零jobs**：resource/group/state相同文本、重复empty/zero indexed states保持不同标签；每原zero job输出，主动删去一原zero job时verify拒绝。
- **16类语义拒绝**：negative、bool、float、decimal string、exponent、zero denominator、duplicate resource/group/state/incidence、unknown resource、row sum>1、empty menu/groups、degree3即使全零、nonstring ID全部抛ValueError。
- **提供audit重跑**：新建`provided_audit/`完整运行成功，其audit report及fixture outputs与repo既有freeze解析JSON完全相同。再次同目录运行因FileExistsError拒绝，所有已产生文件hash不变；三组缺必选参数测试均exit2，且未创建输出目录。

提供audit重跑的两个输出SHA-256：

- `audit_results.json`：`75ee844b64ecc2ef672d4d03a6c3276377f10bebbabb590a30ad2c6dd0ba4bca`
- `fixture_outputs.json`：`90491b0227782c056b0992e94054d8dfbfbb66a95810ad945dfd34b6d39560d1`

## 准确批准范围

批准上述两个源hash的结构化backend及其所列有限audit实现，与已审数学算法一致。没有运行一般UM求解、没有把finite oracle检查当全量词证明、没有认证未列JSON malformed变体或一般软件安全性，也没有升级外审/新颖性。原数学记录保持原字节。

**冻结判断：实际代码审查通过，无standing fatal；所有新证据仅本exclusive scratch目录。**
