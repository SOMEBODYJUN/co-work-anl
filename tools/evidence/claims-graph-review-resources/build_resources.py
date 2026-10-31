"""New lossless resource writer. Does not execute or import a frozen builder."""
from pathlib import Path
import collections, hashlib, json, re

E = Path(__file__).resolve().parent
S = E.parents[2]
F = S / 'archives/customer-attraction/state/资源'
F.mkdir(parents=True, exist_ok=True)
W = S / 'cleanup/workspaces/Boss4/r3-claims-graph-review-resources-next'
W.mkdir(parents=True, exist_ok=True)
g = json.loads((E / 'original/research/graph.json').read_text())
claims = (E / 'original/research/current/claims.md').read_text()
sources = json.loads((E / 'source-manifest.json').read_text())
commits = ['68fad804ec5946cb296f77dc5b336308a66abf12', 'aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']
formal = []
dispositions = {'nodes': [], 'hyperedges': [], 'claim_segments': []}

def j(x):
    return json.dumps(x, ensure_ascii=False, indent=2)

def save_json(path, obj):
    path.write_text(j(obj) + '\n')

def write(name, ident, summary, paths, body):
    refs = ['source:' + c + ':' + p for p in paths for c in commits]
    meta = {'id': ident, 'kind': 'resource', 'type_tag': '资源', 'title': name,
            'status': 'historical-resource-fully-read-with-explicit-scope-and-version-boundaries',
            'summary': summary}
    text = '---\n' + ''.join(k + ': ' + json.dumps(v, ensure_ascii=False) + '\n' for k, v in meta.items())
    text += 'source_refs:\n' + ''.join('  - ' + json.dumps(x, ensure_ascii=False) + '\n' for x in refs) + '---\n\n'
    text += '# ' + name + '\n\n' + body.rstrip() + '\n'
    # Derived prose only: preserve frozen source text in explicit blocks; reject C0.
    if any(ord(c) < 32 and c not in '\n\t\r' for c in text):
        raise ValueError('C0 in formal ' + name)
    path = F / (name + '--资源.md')
    path.write_text(text)
    rel = str(path.relative_to(S))
    formal.append(rel)
    return rel

contract_name = '旧命题登记与研究超图的范围和版本合同'
common = r'''本页保存冻结旧图的完整对象记录，供查找原条件、证明接口、方法障碍及实现证据。下列 JSON 是可读的逐对象资源正文，原索引和所有字段完整保留；并非把旧图导入当前 map。`refs` 是旧仓根相对的来源字符串，其字节存在性、内容正确性和证明充分性是不同命题。本批没有逐个重新读取所有被引文件，也未额外完成这些来源。

节点 `kind/title/detail/status` 分别承担对象类型、可读名称、精确范围与历史状态，不能只取一个 status 判断真值。超边 `premises` 的各项保持合取，`statement` 给具体作用，`conclusion` 是旧端点，`refs/status` 给来源及当时审查界；缺席字段仍缺席。原 `checks` 指有限计算支持，`implements` 指实现，均不能作为全称数学证明。原 `limits` 还混合审查和文档边界；原 `attacks` 有时只否定应用接口，并未推翻一个仍正确的条件定理。详细实际例子及时间纠错见[总合同](旧命题登记与研究超图的范围和版本合同--资源.md)。

图内 source/paper 节点的已读章节、已发表定理及历史无法取得的叙述是原作者记录；它们不表示本批重新取得或全文读过外部论文。当前任务焦点仍按 AGENTS 为六名单位提供者的任意完整历史纯 SPE 半覆盖问题，旧 Q-CAG-HALF/UM/WC 的任务优先级只作历史信息。保留候选、条件、撤回接口和 OPEN，不能因教材、图连通或审查标签自动升级。
'''

track_specs = [
('model', '旧图模型节点的输入和量词', r'''模型节点共四个，分别给原设施主模型、可达集合与目标等起点。设施模型使用正原子权、实现负载和完整客户续局；与顺序客户吸引的单位客户均分、完整有序历史纯 SPE 不是同一模型。此 track 没有自身标记的超边，相关关系在其他 track 中；这不表示它们无关系，也不产生补造入边的要求。'''),
('local', '旧图局部几何节点和关系的条件', r'''局部两设施客户均衡用共有客户的固定混合概率、实际完整自身负载和支持内无差别式；弦条件及精确分支需要端点、零退化和并列点的条件。局部可行多面体与全局选择、构造达到与实例最优是不同输出；完整原记录保留 LOCAL-CHORD-IFF/POLY 等，不能从一个短证书推断全实例最优。'''),
('shared', '旧图共同目录节点和关系的范围', r'''共同目录的两设施 φ 结果与任意设施数的因子二、固定占位的客户 NE 和设备层偏离均不同。正权、强制服务、目录共享及完整续局规则是共同域；普遍上界存在一份规则，并不量化任意客户 NE 选择。下界要在同一域逐较小因子给实际实例，位复杂度亦不得从有限程序运行推得。'''),
('heterogeneous', '旧图异构目录节点和关系的时态', r'''HC-RHO 的短目录条件必须保留。旧节点 HC-RHO 仍写双方长目录 OPEN，但同一冻结图已有 SPARSE-RHO-ALL：每个合法跨目录对至多一个共同客户、任意有限目录、任意预固定 reach/priority 纯规则的 ρ 上界。它以新身份扩展范围，不是删除旧定理前提。HC-2 的候选状态也不因 ρ 子类完整而被升级；共同目录和单交叠域不可比。'''),
('computation', '旧图计算实现节点和关系的合同', r'''程序节点保存确切输入、输出、精确性和规模边界。实例最优枚举、普遍保证构造、固定布局补全与客户反例 oracle 不混用。任意 k 的一部分数学 Nash 化/限制分配调度时界不等于 canonical 软件已实现；程序输出达到证书不自动是实例最优证书。有限或指数算法的终止不提供总位多项式时界。'''),
('extensions', '旧图顺序客户吸引及费用扩展的完整范围', r'''本 track 混合顺序客户吸引和原设施费用扩展，不能仅由 track 名推断模型。CAG 断言逐条保留人数、共同有限目录、单位客户、任意完整有序历史纯 SPE、背景/根覆盖、平局和空/重复主题。两剩余收益 R_b 不等于非零背景总覆盖；完整策略反例与松弛可行点不同。五人根半覆盖已在新身份闭合，任意背景五人利润、六人及任意 m 不随之闭合。真实续局的互斥孩子损失仍需共同付款，末端局部恒等式不能代付整树。'''),
('evidence', '旧图证据节点和关系的有限作用', r'''全部证据记录保留实际输入范围、分母/参数、哈希与冻结报告定位。Fraction 恒等式在所检全域的系数分解和有限游戏抽查是不同证据；对偶分离松弛不等于实际策略反例。checks 指向数学节点只是旧端点组织方式，不能把有限测试当该全称命题的推导前提。未记录外审或未交付软件的对象仍保原状态。'''),
('weighted_congestion', '旧图加权拥塞节点和关系的实际边界', r'''完整加权拥塞 MODEL 是有限正权、非负非降多项式资源费用及真实全负载普通成本；规定的权类、密度、森林、奇环、clock 或势函数模板是额外子类。改善环/前沿稳定不等于所有状态无近似均衡。旧 Cd/ln d 开放话语与后续全状态线性下界并存：后者要同时支付非法态修复、全 front 出口和同次数预算，不能由小 fixture 代证。新 near-degree 身份不覆写旧 d/10 证明。资源存在性、实际可计算核心和社会质量也分开。'''),
('unrelated_machines', '旧图不相关机节点和关系的量词与实现', r'''UM 的一般目标是存在一个统一常数 ε>0 的确定性总位多项式实际调度器、对全部合法非负有理矩阵输出 (2−ε)OPT 调度。固定结构的 promise 算法、给定 T/证书的舍入、相对 CONFIG 阈值的 gap、固定槽/修复模板障碍及条件困难性不等于此目标或其否定。原任务身份、所有机器负载、零值/∞、未知 OPT、固定参数与输入参数的位复杂度均逐条保留。共同一阶与二阶、raw K2/SH3/SA、真实分布与形式矩、局部 law 与共同 global context 不合并。source 硬度仍需实际 P 和全部低负载完整 σ decoder，不能由源定理直接推出 UM 反面。'''),
]

track_paths = {}
for track, name, intro in track_specs:
    nodes = [{'source_index': i, 'record': n} for i, n in enumerate(g['nodes']) if n['track'] == track]
    edges = [{'source_index': i, 'record': n} for i, n in enumerate(g['hyperedges']) if n['track'] == track]
    body = intro + '\n\n' + common
    body += '\n## 完整节点\n\n每项 source_index 是 graph.nodes 的零基原位置；原 record 不删字段。\n\n```json\n' + j(nodes) + '\n```\n'
    body += '\n## 完整关系记录\n\n每项 source_index 是 graph.hyperedges 的零基原位置；保留共同前提的顺序和全部实际字段。\n\n```json\n' + j(edges) + '\n```\n'
    rel = write(name, 'historical-research-graph/' + track, '冻结旧图本分支的全部节点/关系、精确范围及证据角色；资源性保全而非当前图导入。', ['research/graph.json'], body)
    track_paths[track] = rel
    for group, records in [('nodes', nodes), ('hyperedges', edges)]:
        dispositions[group].extend({'source_index': z['source_index'], 'id': z['record']['id'], 'target': rel} for z in records)

claim_specs = [
('cag', '旧命题登记的顺序客户吸引全部陈述', [(1,120),(1431,1444),(1457,1463),(1485,1535)], r'''顺序 CAG 使用任意有限单位客户、有限非空共同主题目录和依次行动的单位提供者。客户在所有最终覆盖者之间均分，策略指定每个有序历史的动作，任意平局、空主题、重复标签和不可覆盖客户不删除。每个历史选极大花瓣的结论仅在删除全目录共同核心后不同极大花瓣两两不交的结构域成立；并非一般 SPE→PNE。根 W 是覆盖，非零前缀的剩余利润另记，不能换成覆盖量。

登记中的三人 5/3、四人 1499/750 上界和五人 2W 上界是不同人数的结果；四人尖锐性未证。许多失败桥远强于半覆盖：完整 SPE 福利可以小于同实例最差 PNE/CCE 或静态 iid 值，这仍不构成半覆盖反例；仅有局部负漂移更不足否定全局补偿。静态真实 maxmin 值、弱 iid 债、固定策略锥或少数图模板各有独立状态。末两人重查询/报价的非负行组合保留原支出和关联信息，不能据此声称六人付款证书。

末行 CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1 在“逻辑使用规则”之后：其全范围动态 LP 包络 W≥c+(U−c)Σ_t1/E_t 以及 τ_inc≤2 的充分桥是完整解析候选、内部清洗待做。它未进入旧 build_map 的 declared 集合，不得因完整登记校验 PASS 被默认为已审或已证。'''),
('facility', '旧命题登记的设施模型全部陈述', [(121,286)], r'''两设施客户费用按包含自身完整重量的实现负载期望，服务强制；完整客户 NE 规则在每个布局指定。共同/异构目录、单交叠/任意交叠、两设施/任意 k、固定占位/设施层偏离分别保域。弦精确性和根式最优值、因子二/φ 的普遍构造、固定地点弱 NP 完全及无 FPTAS 的结论各有自己的量词和编码。

任意 k 的 greedy、盒、帽和补全接口要保真实初态及所有替代。SC-K-GREEDY-UNOPENED-2 只保证从指定贪心分配的任意有限严格客户改善前缀，最小设施收益≥末插入 γ、从未开启点的新覆盖 N≤γ；不保证所有 NE、不保证旧全部强预算、不给改善次数多项式。给定可行纯种子、冻结超帽客户及自身替代检查是冻结补全的共同前提，不能当免费生成器。一般 full-box 存在与特定盒最小者/字典序选态失败并不冲突。数学调度定理时界也不等于 canonical 软件已实施。'''),
('wc', '旧命题登记的加权拥塞全部陈述', [(287,597),(1445,1456),(1464,1484)], r'''WC 使用有限正权、非负非降多项式普通资源费用。单源/多源、实际占用高度、潜在用户共占图、森林、类内 clock、full signature cone、可分势和全状态无均衡是不同范围。有限严格改善环只能反驳 FIP，不能单独反驳均衡存在；要否定全类 Cd/ln d 目标，既有线性族的每个纯状态都必须有真实严格改善。

后续全状态 d/10 与 near-degree 是分版本证明；固定 n 的 d₀(n) 不能直接带入随 d 增长的 n。前沿成本平移、社会 OPT 压缩及核心稳定转移需要共同的 RD/SD/正则化条件，有限势最小点不免费给位多项式求解。权类高度下界和条件尺度势只给其图/资源合同，不能反推一般目标。完整表保留旧 OPEN，但当前纠错以同冻结版后的实际证明为准。'''),
('um', '旧命题登记的不相关机全部陈述', [(598,1430)], r'''本登记中的 UM 主目标量化全部普通非负有理处理时间矩阵，包括零端、∞和无有限端任务的分支处理，并要求统一 ε 与确定性总位多项式实际调度。已知有序槽 ST 是一般二倍地基；CONFIG、弱 coalition、固定行/槽、C2/K2/SH3 层级的阈值趋二障碍不等于相对真实 OPT 的算法不可能。

受限结构如共同资格私有组、固定大宏占位、有限 sink、共同尺寸/倍率、树/仙人掌/反馈秩、小支撑或 XOS 显式菜单各有精确附加域。给定矩、给定真实两份 σ、给定 T、原身份保持、逐机共同容量和未知 OPT 搜索不能省略。有限 backend 检查不认证完整 all-input 软件。NP-hard 的见证选择或源 SC/PCSP 事实需要实际物理 compiler、全部低负载 σ decoder 及固定参数规模，不能直接否定主目标；SCHA/P≠NP 等假设仍作为条件。完整源文也保留撤回的 sharpness/能垒/高低 γ 解释及其修复身份，不把旧摘要升级。'''),
]
lines = claims.splitlines(keepends=True)
claim_paths = {}
for tag, name, ranges, intro in claim_specs:
    body = intro + '\n\n这些是冻结登记的完整原陈述与来源定位，属于资源对象而非本批新证明。原 source 相对链接只在原 current/claims.md 目录解释；下面用原文块保留，避免把历史链接改绑到新资源目录。公式、所有非表格正文、候选和逻辑规则不因计数去重而删除。现行纠错和实际比较见[总合同](旧命题登记与研究超图的范围和版本合同--资源.md)。\n'
    for lo, hi in ranges:
        block = ''.join(lines[lo-1:hi])
        body += f'\n## 原登记第 {lo}–{hi} 行\n\n```markdown\n' + block + '```\n'
    rel = write(name, 'historical-claims/' + tag, '完整冻结登记按模型保全所有条件、结论、状态及非表格论证；不升级未重审的数学。', ['research/current/claims.md'], body)
    claim_paths[tag] = rel
    for lo, hi in ranges:
        dispositions['claim_segments'].append({'first_line':lo, 'last_line':hi, 'target':rel, 'sha256':hashlib.sha256(''.join(lines[lo-1:hi]).encode()).hexdigest()})

review_body = r'''这两份短源是作者审查协议和命题写作模板，没有独立数学定理。以下完整保留，并按现行模型解释其可复用部分。旧审查 README 的 active Q-CAG-HALF 是历史任意人数任务；当前 AGENTS 的 Q-CAG-HALF-6 精确六人优先。清洗者/Boss/editor 是旧协作角色，不是数学证明前提，也不自动要求候选先经表决才可保存。

审查的承重问题是：实际对象/量词/全部假设是否一致，证明有无未覆盖反例和退化，算法复杂度按什么编码，软件核查究竟覆盖什么输入，是否真实读取了相同版本。赞同票不能代替证明；旧稿不同既不自动错误，也不能无条件迁移到新模型。source proof/current proof/internal review/external review/implementation 的五轴应保持独立。

claim 模板要求精确输入和上下界量词，特别是下界“每个更小因子有实例”。假设须先合取再给结论；不能把程序、历史文档或审查状态作为数学前提。构造一个因子、证明普遍最优及验证实例达到三个任务分开。复杂度要给有理/整数位长，唯一性、并列点、零端和 gap 不能略去。测试应绑定代码、真实输入、证书与冻结输出；新原材料注明日期及来源。

模板把设施个数/目录等列作示例，不适合作为 CAG 的唯一字段清单。当前正式资源用 cleanup/OBJECTS.md 的平坦 MATEK 元数据；本页保留旧模板语义，不覆盖模板原件，也不把旧 reviewer 判断算作外部同行评审。
'''
for p in ['research/reviews/README.md','research/templates/claim.md']:
    review_body += '\n## 完整原文：' + p + '\n\n```markdown\n' + (E/'original'/p).read_text() + '```\n'
review_path = write('审查阅读与命题模板的精确合同', 'historical-research/review-template-contract', '完整旧审查协议与命题模板、当前六人焦点和MATEK格式的边界；审查元数据不作数学证明。', ['research/reviews/README.md','research/templates/claim.md'], review_body)

html_body = r'''冻结 index.html 是 standalone 静态 HTML：graph-data 内嵌整份 graph.json，客户端 JS 渲染关系卡与节点检查栏。本批已读完实际 HTML 的全部非数据区 8,972 字节，内嵌 1,521,223 字节数据区通过结构相等绑定到已逐字段读完的 1,153 节点和 1,353 超边；静态模板替换重建整个 1,530,181 字节原件全等。shell 的 __GRAPH_DATA__ 标记占14字节，所以两分区字节数不能直接相加等于原件。没有运行旧 builder，且这不构成浏览器显示或交互 PASS。

## 页面实际行为与遗漏

头部可见标题“数学研究超图”，介绍前提合取、红色反驳、黄色有限测试/边界，链接总览、旧现行命题、JSON；“完整主稿内部审读”是原页面历史说明，不能推广成全页所有节点均获同级审查。红色亦不能保证每条旧 attacks 真以假命题为端点，实际反例见总合同。

工具栏是 search、九分支 track、五种 relation、清除选中节点和计数。kind 下拉只使用 legend 的键，完整五条定义没有展示；version/title/updated 的 graph metadata 也没有展示。两条额外 hyperedge.detail 均未使用：E-UM-COMMON-SIZE-UNKNOWN-B-EXACT-v1 与 E-UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1，其 detail 为阶段接口不升级主目标。此信息仍在完整图资源中。

render 遍历全部超边，以 e.track/e.kind 筛选；搜索词只拼 e.id/e.statement/e.refs、结论及前提 ID/title，不包含节点 detail/refs/status、超边 status、legend 定义和额外 detail。选节点后只保直接关联入/出边，非传递闭包。节点按钮展示 ID/title、aria-label；检查栏展示 kind/status/track/detail/refs，并列出相关边。清除只取消 selected 和隐藏按钮，保留搜索/track/kind 与检查栏原内容；点相关边的锚点不清其它筛选，所以不能保证该边当时可见。当前源图无游离节点，静态上所有节点至少出现在一张关系卡；这不是当前新图必须连通的要求。

卡片展示 id/kind/status/track、所有前提、结论、statement 和 refs；attacks 用⊣，其余用⇒，共同前提在左框。derives 青绿、attacks 红、checks/limits 黄褐、implements 蓝。textContent 插入所有文本，未装 KaTeX/MathJax，因此数学是原文字/TeX样式字符串，不承诺排版数学公式。来源链接一律 ../ + 旧仓根相对路径，新标签页且 noopener；本批未逐个访问全部1,420种路径。颜色、字形和布局来自此 CSS，没有外部图片、嵌入字体或外部脚本的独有语义资产。

布局主宽1480px，关系卡加270–340px sticky 检查栏；850px以下改普通流，570px以下前提/结论纵排且旋转箭头。focus-visible 给节点描边，inspector aria-live=polite。这里只从实际 CSS/DOM/JS 得出设计行为，未验证浏览器实际像素、滚动性能、读屏或事件运行；不复用另一 learning HTML 的字体缺陷认定本页也有此缺陷。

## 完整外壳

下面移除且仅移除已完整另存/阅读的 JSON payload，以 __GRAPH_DATA__ 标记替代；全部 CSS、外壳文字、JS 原样保留。完整原件和绑定报告在 tools/evidence/claims-graph-review-resources。
'''
html_body += '\n```html\n' + (E/'html-shell.html').read_text() + '```\n'
html_path = write('旧研究超图HTML的完整表示和交互边界', 'historical-research/graph-html-contract', '全部shell/CSS/JS、完整graph payload绑定与未显示字段保全；静态表示检查不认证实际渲染或数学。', ['research/index.html','research/graph.json'], html_body)

contract = r'''本资源吸收五份冻结主源的全部人类与数学语义：命题登记全1,535行、旧图全部1,153节点及1,353超边、嵌入该图的HTML、审查README和claim模板。它们是待核的范围/关系/审查/表示来源，不是将旧图当数学事实继承。所有完整记录按模型/旧track分置下列资源，必要条件、证明接口、失败路线、软件和外审边界均保留；没有进入阶段三 mapper，也没有修改旧正式数学页。

## 精确版本和去向

两冻结提交 legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12 与 main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c 的这五件内容相同。原件路径、SHA、字节和对应blob以 source-manifest.json 为准；本批只取已核SHA的缓存或Root实际clean show导出的template，不做Git或网络访问。
'''
contract += '\n| 原路径 | 字节 | SHA-256 |\n| --- | ---: | --- |\n'
for x in sources:
    contract += f'| `{x["path"]}` | {x["size"]} | `{x["sha256"]}` |\n'
contract += '\n完整去向如下；相关条件解读不替代逐对象原记录。\n\n'
for path in [*claim_paths.values(),*track_paths.values(),review_path,html_path]:
    title=Path(path).name[:-3]
    contract += f'- [{title}]({Path(path).name})。\n'
contract += '\n## 旧图完整顶层元数据\n\n以下是除节点/关系数组外的全部顶层字段，图例五种原定义完整保留。\n\n```json\n' + j({k:v for k,v in g.items() if k not in ['nodes','hyperedges']}) + '\n```\n'
contract += r'''

命题表在逻辑规则前有632个数据行，因一行可含多个ID，共640个不同登记身份；其中620个旧graph kind=claim、20个lemma。规则后另有一行 incidence-LP 候选，不在这640集合中。旧 build_map.validate 明确 split("## 逻辑使用规则")[0]，所以字段集合相等并未检查尾行。此发现来自全文读尾部和实际源码比较，不是新数学反例。资源保存全部633数据行、所有非表格段落、候选与逻辑规则，不能用640计数替代阅读。

## 真值、条件与时态的实际纠正

| 原定位与说法 | 实际比较和准确处置 |
| --- | --- |
| claims第35行、旧graph CA-FOUR-UPPER-1499-750/相关limits称“五人以上仍开放”；旧ALL-N等也有类似下一步叙述 | 同冻结登记第10行/graph末端CA-FIVE-HALF-EXACT-v1已给恰五人根 OPT5≤2W。本批复用前批全文读完、当前同SHA的五人/四人正式证明比较：四人只有1499/750上界，锐性仍未证；五人不推广非零背景五剩余利润、六人或任意m。原旧下一步叙述是过时时态，不删除原定理身份。 |
| graph.nodes[31] HC-RHO.detail称双方长目录OPEN | 同图SPARSE-RHO-ALL及本批全文读正式ρ证明已给任意长单交叠上界。固定reach/priority规则、高区严格全序下降、首高→低边和同一客户身份共同给 q(r)=r³−r²−2r+1<0 的矛盾。短目录条件仍留在HC-RHO；不能移去单交叠或全局固定规则。 |
| graph.nodes[115] greedy-unopened说所有loads“exceed γ” | 实际源 SC-K-GREEDY-UNOPENED-2 节和登记均为 ≥γ。最后插入所在站的初负载可正好γ；严格客户移动使排序负载严格词典序改善，却只保最小坐标非降。准确表述是所有到达态a≥γ、从未开启N≤γ，单占来源另N+w(J∩Cr)≤2a；不外推所有NE、全部旧强预算或多项式步数。这里只全文读该独立节，不宣称本批重读整polytime_frontier。 |
| graph.nodes[293]动态iid债detail仍称weak global OPEN | 同图CA-WEAK-IID-GAP已rejected且末端CA-IID-WEAK-WELFARE-NO-v1给完整策略族。复用前批全文读、当前同SHA的全局/局部iid页：m≥41既有解析族否定旧弱iid全局桥；局部负漂移本身不够，静态/债恒等式保留。不是一般half反例。 |
| 旧WC gap/model节点仍写Cd/ln d OPEN，后续RESOLVE边与线性全状态族并存 | 复用前批全文读、当前同SHA的全状态证明：每p≥2²⁰有有限合法正权纯p次费用游戏，每个纯状态有严格p/10改善。因此任意固定C在lnp>10C时的Cd/ln d全类存在保证为假。有限构造规模非多项式承诺；新near-degree身份另留，不覆写旧证明时态。 |
| claims一般boxed NE算法“OPEN”与后续full-box存在并存 | 一般可行/有限穷尽存在已被后续身份证明；高效构造、指定盒极小/字典序选择的可靠性及旧强预算依然是不同问题。此处按精确文字解释，不把每个“open search”判为可行性被否定。 |
| CA-DISJOINT-MAXIMA 与sunflower推广 | 本批全文读正式不交极大花瓣证明：K是全目录交集，删除后不同极大花瓣两两不交；后继极大资源的singleton SPE→PNE和降低单资源占用不增共同支付真实扩张。不能把结论混为所有sunflower内部主题自动极大，或把“极大花瓣”偷换为任意资源。这是范围核对，未发现足以撤回原登记的冲突。 |

这些纠正均留旧字节，另给当前用途；不修改归其他Owner的旧页。未逐篇重核的其余数学陈述仍按作者范围和状态保全，source/paper节点的历史阅读记录也不算本批外文阅读。

## 关系类型不能机械变成当前证明图

原图包含641 derives、18 attacks、318 checks、16 implements、360 limits。以下是实际实读到的语义差别，而非格式警报：

1. e-mf-static-pack-no 指向SC-K-LOCAL-PLS，但它否定固定冻结修复足以提供其前提，不反驳该条件PLS引理。e-mf-global-cap-limit指向MF-PURE-CAP-POLY，原statement明说定理仍真、初始帽假设可能失败。若以后建新图，应指向被否定的无条件应用接口，保明确量词；本批不替它们造新边。
2. e-mf-box-potential-hard 的kind=limits而statement叙述3-PARTITION归约；只有读实际归约域才决定是推导还是方法边界。实现边方向也混有数学→程序和程序→数学，不能以箭头推断因果证明。
3. 大量checks指向全称定理，原statement已限定有限整数/Fraction/具体矩阵/有限参数或边界。不能因结论端点是claim，就让有限运行承担实参数、渐近、全状态或总时界量词。
4. review与publication/source地位不是数学前提。WC结构末端边特别披露作者/positive reviewer与Root另做S7重构；内部review不认证外部review和世界优先权。UM PaperFact与条件硬度也保未完成物理编译/解码义务，不把源结论自动接到UM反面。

原生成器强制每个claim有入边且所有节点被使用；现行AGENTS明确不强制连通/入边。当前源无游离节点是历史数据事实，不构成现阶段要求。1,420种refs、5,505次引用出现只是定位语义，未作这些路径的全仓字节PASS或被引证明完成断言。

## 数学、软件与显示的三种合同

原登记的数学证明或给定证书算法、已交付实现、有限审计分别记录。例如限制分配MAX/RANGE的位多项式数学Nash化不能扩到未交付canonical后端；真最优边际或共同矩的存在不能当免费oracle；给定T的可靠FAIL也不自动生成未知最优调度。五轴review对640身份的覆盖不含尾部候选，且外审全部not_recorded的事实不会因图status字符串而改变。

HTML静态全字节绑定只说明原表示由该整图与该外壳组成，既不证明所有图字段可见，也不证明实际浏览器交互或数学。完整legend定义与两额外edge.detail未显示，节点detail/refs不参与search；textContent只显示文字，无公式渲染器。完整shell和准确行为见HTML资源。没有新渲染、截图、PDF、外部论文下载或交互PASS。

## 全文阅读、去重及本批实际新检查

claims全1,535行实际逐段读完；graph全部节点/超边逐字段实读。图重复字符串只有在全文已读过相同SHA的catalog路径/标题、assets/review精确字段或claims完全相同子串时，才用字典代码复用；U字符串在首次出现完整输出，后出现按原值引用，未以DOM摘要或对象计数替代正文。两次输出截断未计为实读，随后分小块补全，读范围与字典原值保留在evidence。

实际新操作只有读取/精确拷贝、无损资源表示、静态HTML绑定及本批self-check；未执行旧build_map/check_assets/数学suite，没有覆盖共享导出。完整原HTML、JSON、MD和生成器依赖不修改。当前自查覆盖全部原字节SHA、2,506对象全字段回读、1,535行无损去向、5receipt以及正式页C0/行尾空白；这些是结构/格式检查，不是数学正确性认证。旧批2,198项自查曾漏C0，已另批修复；本批不借旧总数声称覆盖新问题。

全部新文件位于tools/evidence/claims-graph-review-resources与独立workspace，formal中只新增资源页。对账本、旧图或模板的integrated处置不意味着其全部引用来源一并done。后续阶段三仍须逐边按数学对象重建关系，不能复用旧kind/连通要求替代实读。
'''
contract_path = write(contract_name, 'historical-research/claims-graph-review-contract', '五源全语义去向、尾部候选漏登记、历史时态/关系类型纠正、表示和审查界准确保全。', [x['path'] for x in sources], contract)

save_json(E/'formal-manifest.json', [{'path':p,'bytes':(S/p).stat().st_size,'sha256':hashlib.sha256((S/p).read_bytes()).hexdigest()} for p in formal])
save_json(E/'dispositions.json', dispositions)
save_json(E/'resource-targets.json', {'contract':contract_path,'claims':claim_paths,'tracks':track_paths,'review_template':review_path,'html':html_path})
print(j({'formal_count':len(formal),'formal_bytes':sum((S/p).stat().st_size for p in formal),'nodes':len(dispositions['nodes']),'edges':len(dispositions['hyperedges']),'claim_lines':sum(z['last_line']-z['first_line']+1 for z in dispositions['claim_segments'])}))
