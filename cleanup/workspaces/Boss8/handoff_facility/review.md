# Boss8 本地清洗记录：`prop-certificate` 附录

## 来源身份

- 源 ID：`a26587a0ca45f80f9875`
- 路径：`research/reviews/facility/multiple_facilities_appendix/prop-certificate.md`
- 冻结来源：`68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）
- SHA-256：`57db9bb34a442996c7d8ea4131494121eb5cf012e7c9ac34905bf4689fefc7c8`；两冻结提交逐字相同。
- 本地读取：使用 `tools/cleanup.py show` 完整读取 112 行附录；随后用固定提交读取 228 行 `research/manuscripts/multiple_facilities/main.tex`，并比较当前 `archives/facility-games` 中的主定理、审查、有限重构和逆向证据对象。

## 数学内容

该源是多设施共同目录因子二主稿的 `prop:certificate` 审查附录，不是新的独立定理。它确认以下命题在其明确假设下按稿件文字成立：客户权重为正二进制有理数，客户—地点覆盖和全部 `k` 个带标签设施显式给出；枚举有限布局与站点分配，保留 Construction 的升序负载字典序首个最大者；按 `lem:packing`、`lem:capped` 为每个实际单设施偏离构造纯客户 NE；其余布局用固定客户枚举和“首个严格改善最佳反应”的确定默认程序补全。保存的在轨/实际偏离策略、负载不等式和默认程序描述具有输入长度的多项式位长。

它没有声称全局枚举或严格改善过程在输入位长上多项式时间。证明使用的是真实有限性和势函数终止：`lem:capped` 中每次严格客户移动使 `1/2 Σ_f L_f^2` 严格下降；这保证终止和精确纯 NE，但不限制步骤数。该附录也明确保留原子客户的自重项、零覆盖/零到达、重单例、源地点消失和任意平局边界。

## 关联阅读与比较

1. 逐段核对 `research/manuscripts/multiple_facilities/main.tex` 的模型、Construction、`lem:onpath`、`lem:transfer`、`lem:packing`、`lem:capped`、`lem:deviation`、`thm:main` 与 `prop:certificate`。主稿的因子二存在性量词是共同有限非空目录、任意正实原子权重、`k≥2`，在轨站内独立均匀混合，所有离轨布局可取纯 NE。
2. 阅读并比较已入库对象 `archives/facility-games/state/审查/设施因子二主稿与位多项式选择器--审查.md`。该对象已经逐字吸收本附录的独有结论：多项式**证书长度**与搜索时间分离、`lem:capped` 只给有限终止、等权流实现只是受限 on-path 选择器而非异权 off-path 算法；其 frontmatter 已把本源 ID 列为 `clean:a26587a0ca45f80f9875`。
3. 阅读 `archives/facility-games/subarchives/common-many/state/定理/共同目录任意设施数因子二存在--定理.md`、`.../state/计算/因子二连续稿的八页核读与有限重构--计算.md` 及 `.../state/审查/因子二逆向审查与证据边界--审查.md`。这些对象把附录放回完整证明链，并明确有限 419 游戏/2518 布局重构是证据，不外推任意输入的时间复杂度；逆向审计也不把内部第二路径写成外部独立评审。
4. 查到 Boss3 已保存的 `cleanup/workspaces/Boss3/agent-gamma/multiple_facilities_appendix_review_tracker.md`，其 `prop:certificate` 行与本源 hash、`thm:main`/`lem:packing`/`lem:capped` 依赖及 “closed: verified as written” 一致；这只是历史审查记录，不能替代本次来源处置。

## 处置判断

本源版本的全部实质数学内容已有明确、可定位的现存正文目标，且目标 frontmatter 已引用该源。重复新写一份对象会制造同一稳定 ID 的平行解释；因此本地拟登记为 `duplicate`，目标为：

- `archives/facility-games/state/审查/设施因子二主稿与位多项式选择器--审查.md`

冻结原文件保留在历史来源中，不删除、不改写。当前记录只说明语义处置草稿，未执行 `clean done`，也未声称目标已推送。若以后获得写权限，应先确认该目标版本已在 `rebuild/research-v2` 远端，再提交该源的 `duplicate` receipt。

## 仍需保留的边界

- “closed: verified as written” 是来源内部审查判断，不是外部同行评审、优先权或正确性独立认证。
- 证书位长多项式不等于寻找字典序最大者或运行严格改善默认程序的多项式时间算法；一般位多项式在轨选择仍应按开放边界记录。
- 本源不扩大共同目录条件到设施依赖目录，也不把双设施黄金比转成任意设施数黄金比。
- 程序/有限重构只能作为辅助证据；主定理的普遍性仍由完整证明链承重。
