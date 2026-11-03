# 菜单AP与同最大根重复元组：原件、固定点资格与版本

此证据包由四个正式对象拥有：

- [七十六原子2621行精确点](../../../state/计算/真实源双菜单AP必要系统的七十六原子精确可行点--计算.md)。
- [六十一原子4007行精确点](../../../state/计算/最大根重复元组必要系统的六十一原子精确可行点--计算.md)。
- [完整发现与恢复合同](../../../state/程序/双菜单AP与最大根元组的发现及恢复合同--程序.md)。
- [原四例回放、版本及补全边界](../../../state/审查/菜单AP与最大主题元组原始点的版本及补全边界--审查.md)。

## 冻结来源与逐项身份

下列十主源全部来自source:68fad804ec5946cb296f77dc5b336308a66abf12下R-cd789330fc7141299ac491bbb3ffa420/round13/certificate，相同内容亦列main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c；[逐源manifest](source-manifest.json)保完整路径、blob、SHA、字节、多来源与本地copy位置。原字节保留，文件中的旧SHA/seconds不改。

|源ID|原文件|字节|SHA-256|
|---|---|---:|---|
|b9b61b6ac8d7b4b44642|[README.md](original/b9b61b6ac8d7b4b44642/README.md)|5210|9febc96b08a786a5a233ed7d86c4074af6eeaffe349f6f64f959b8217553697b|
|4619bee4f9d8619db6cf|[audit_menu_ap.json](original/4619bee4f9d8619db6cf/audit_menu_ap.json)|2080|2bf229207a6067f96a68219e0a3d1615464ee47f204abba30a76d44e2a7d6a37|
|59383357b44abbbdcfa7|[audit_menu_ap.py](original/59383357b44abbbdcfa7/audit_menu_ap.py)|4695|e6ead141ae1c9363c19074768963c7bfcf86fac7c4be3a49a818813d3ff13193|
|5db6a037342bdee0f107|[exact_max_menu_tuple_primal.json](original/5db6a037342bdee0f107/exact_max_menu_tuple_primal.json)|651061|c0415208b932451f54646b4d49209876e8678e9da0d4a5297ee0207898af1feb|
|435e9d4bab69861905d1|[exact_menu_ap_primal.json](original/435e9d4bab69861905d1/exact_menu_ap_primal.json)|555420|59e4393c8781a864ac5b898a5faec2fe1e25ceaef2c128746edcf1f92b9bed2b|
|9a09412ce5b93d6e2536|[freeze_menu_ap_primal.py](original/9a09412ce5b93d6e2536/freeze_menu_ap_primal.py)|3069|929de1f7e45acaa9792687e41d5c212c2c1d83d05ae6e259a43a76a7cda0f056|
|cd89b461ba6f34668855|[max_menu_tuple_discovery.json](original/cd89b461ba6f34668855/max_menu_tuple_discovery.json)|163966|13952017a634254b5eab2a7848bd09b7f0ffd5563aa5f06377cee2041fe10849|
|1f4560c9319c2a285e47|[max_menu_tuple_pricing.py](original/1f4560c9319c2a285e47/max_menu_tuple_pricing.py)|2478|400ab4b0839b0acf9f72a8855c733db975fa3f2f9f8bcd8c035226acd6e9d27e|
|64d42044677286960ce2|[menu_ap_discovery.json](original/64d42044677286960ce2/menu_ap_discovery.json)|796382|02ab432555bd8d1a16b70d12dbf2f55ff15228c1426fe152cd15fa40089d6a4e|
|95ae42780dac898a9c0d|[menu_ap_pricing.py](original/95ae42780dac898a9c0d/menu_ap_pricing.py)|9062|1bf8fac75ae4a5f65c13ad66c8c3ae4463b642572623baf3a3f1321b054e2f19|

四个小主程序/README/audit报告全部全文实读。四个大JSON的每个顶层字段、全部有序行名、全部原子字段、每个质量/保存余量、全部history和非零dual均通过原文件及完整可逆视图消费；没有只取最终正支持或旧摘要。[完整消费记录](complete-data-reading-report.json)描述每份schema和投影域，不把字段消费当数学正确性证书。

## 原函数固定点资格：仅有的一次数学运行

[audit_saved_primals.py](audit_saved_primals.py)与[qualified_scalar_loader.py](qualified_scalar_loader.py)原样保留；[进程事件](qualification-process-event.json)、[stdout](qualification.stdout.txt)、[stderr](qualification.stderr.txt)和[固定点完整报告](saved-primal-qualification.json)为同一次已完成事件。exit0、stderr0B、外墙6.097549676895142秒、内部6.058989875999941秒。接续整理没有重跑。

检查只在两个固定输入上执行Python标准库白名单抽取的原scalar函数，共137正原子、443623个系数，6628条保存余量逐项重算等值并非负；W1、O/正差、88/72零行、支持按序结构、全部类型域与输入SHA相符。它不是原CLI回放，不是第二独立系数实现，也未import原模块或运行原main/Universe初始化/QR/LP/BI/CG/全域price。完整结果：

|点|全部逐行结果|全部原子指标|家族摘要|
|---|---|---|---|
|76/2621|[2621相等式](menu-all-row-equalities.json)|[76指标](menu-all-atom-metrics.json)|[家族零行/最小值](menu-row-family-reading-summary.json)|
|61/4007|[4007相等式](tuple-all-row-equalities.json)|[61指标](tuple-all-atom-metrics.json)|[家族零行/最小值](tuple-row-family-reading-summary.json)|

家族摘要只从已有完整行值聚合，没有执行新系数计算。菜单点2621行零数62+2+10+14=88；最大点4007零数48+1+1+0+22+0+0=72。所有点的精确原子/质量与有理余量在上表原JSON中；指标里的系数散列不替代原始质量或公式。

[所选原AST](selected-original-scalar-AST.json)记录10个实际抽取文件的全文件SHA及选取节点：八个related scalar依赖加两主程序。related/保全部十个比较依赖，另两件exact_cross_primal/frozen_pair_reoptimization只为恢复合同阅读，不被本核执行；[related manifest](related-manifest.json)将其原仓位置与字节分别记录，不追加done来源。loader/driver读取的original/<id>/和related/布局须保，其他消费此包的同批driver依赖这一结构。当前源码和旧报告code_sha的差异详见正式审查，不因为当前逐值相符便认证旧生成同版。

若以后明确需要重复同一受限核，可复制完整包到隔离目录再执行driver；driver会覆写本地selected AST、报告和逐行JSON，应保新事件为另一个身份，不在保存原证据的目录原位覆盖。它仍只重复同一原函数，不增加独立实现等级。

## 完整发现池与精确点阅读视图

[read_complete_data.py](read_complete_data.py)只生成可逆完整字段视图，无优化、无行公式评价。reading/menu_ap-complete-lossless-view.json保1080列所有字段、全部零质量、71个非零dual、12轮history及完整2621行名；reading/max_menu_tuple-complete-lossless-view.json保68列全部字段/7个零质量、一条跳价history和4007行名。原子字段用字典+每列索引无损表达，解码已断言与整个原JSON对象相等；缺字段用null而不伪造旧exact_mass。相邻full-reading-view.txt展示所有字典、1080/68条索引记录、全部非零质量和其余标量/轨迹；两all-row-segments.json保有序行域的分层边界。两份exact-all-atoms.jsonl及all-nonvector-fields.json展开全部精确原子质量与顶层标量；余量在两个完整逐行核中消费。

菜单发现末轮仍有负浮点全域余项并加61列；元组报告β>2时未定价，minimum/context均null。二者都不提供全域有理dual或模板精确最优。原四例audit_menu_ap.json保存9179完整历史IC/41300合法AP对通过，但其menu代码SHA dae5573f…与当前9062B的1bf8fac7…不同，本次未执行它。精确点source_sha精确绑定对应发现数据；其code_sha不绑定历史全部依赖闭包。

## 与后续数学的边界

同SHA61点被后继末菜单精确分离（包括610允许拆分）及新增1414行中的79个负行排除。新关系排旧点与旧4007行可行不冲突；后继旧页当时没有核旧4007资格，本包补的是独立范围。原README的五人half OPEN不是当前状态，当前五人定理由另一完整证书完成。任何必要点都没有因有理质量或O>2自动成为真实共同目录/σ/OPT反例。
