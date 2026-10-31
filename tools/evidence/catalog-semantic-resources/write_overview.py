from pathlib import Path
import json,collections,hashlib
E=Path(__file__).resolve().parent;B=E.parents[2];x=json.loads((E/'original/research/catalog.json').read_text());binding=json.loads((E/'full-md-binding.json').read_text());dest=json.loads((E/'topic-destinations.json').read_text());R=B/'archives/customer-attraction/state/资源';name='旧研究总目录的字段语义与版本边界--资源.md'
head='''---
id: historical-research-catalog-semantic-contract
kind: resource
type_tag: 资源
title: "旧研究总目录的字段语义与版本边界"
status: historical-resource-semantically-integrated
summary: "完整实读2099条人类名称用途与全部字段，保12专题资源、35改名与导出合同，校正五人旧界、弱iid桥及滞后路由；不将目录角色升级为数学证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/catalog.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/catalog.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/CATALOG.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/CATALOG.md"
---
# 旧研究总目录的字段语义与版本边界

这是旧研究目录本身的资源清洗。目录提供人类名称、用途、文件角色、历史状态与来源路由；它不包含2099份目标数学的完整证明。已实际逐项读完全部2099记录的名称/用途/主题/角色/可选包/关联字段、JSON外壳和35改名，原Markdown的全部非表格正文及其表内语义。精确重复用途只在首次完整阅读后复用。本批不凭记录数、role或旧作者“逐文件整理”声明代替阅读，也不额外勾选这2099个被引用源。

两原件保持精确字节：JSON 1,236,965字节，SHA256 `b22bc7bfe560e3be434682dc262b5b7e29de7b2c4ce33d0cbc1a9320f444a24c`；Markdown 1,596,733字节，SHA256 `530bb95cee99af8d6946eed49b439551686ab651bb9f9bd910bca17cba038436`。均在两个冻结提交字节相同。原件、inventory记录与旁读材料见[证据目录](../../../../tools/evidence/catalog-semantic-resources/source-manifest.json)。

## 完整内容和去向

原schema_version=1。原scope完整含义是：逐文件中文名称与用途，数学范围和五轴状态仍以精确账本为准；覆盖current/questions/reviews、研究入口与已整合拥塞证据，历史原稿及规范程序由专门入口按需查询。它是旧目录的覆盖合同，既不是全仓源分母，也不是今天已完成的知识图。

每条记录的四个必要语义字段是title/purpose/topic/role，path承担原定位。1192条有package，1148条有related_paths，另14条有related；缺席与空数组分别保留。全表18种role、111种package取值（含字段缺席这一种情况），共有1484个逐字不同purpose。各记录完整字段保在[逐项原文与去向](../../../../tools/evidence/catalog-semantic-resources/catalog-semantic-records.json)，不是只保存摘要。分主题资源如下：

| 原topic | 完整记录数 | 自足用途资源 |
| --- | --- | --- |
'''
lines=[head]
for d in dest:lines.append('| `'+d['topic']+'` | '+str(d['count'])+' | ['+Path(d['target']).stem+']('+Path(d['target']).name+') |')
lines.append('''
各专题完整用途字典保留全部原数学断言与限制，每条原路径各有去向。共同存放不意味同模型；同时设施分配的均衡、顺序客户吸引完整SPE、加权拥塞、非相关机调度和正核表示分别按真实定义复用。本批没有按目录先后、人数大小或role自动创建数学推导。

## Markdown表示：已绑定什么

已用本次独立写的[静态重建程序](../../../../tools/evidence/catalog-semantic-resources/bind_catalog.py)，读取真实JSON、真实assets.json以及旧build_catalog.py中TOPICS/ROLES/PACKAGE_TITLES的AST字面常量，重建整份Markdown。结果为全部1,596,733字节相等，双方SHA相同；不是只核2099条数据行或DOM摘要。旧生成程序没有导入/执行，旧`--check`和任何数学suite没有复跑。此结果只认证该冻结输入的表示绑定，不认证文件存在、一般算法、历史审查独立性或所有目标数学。

原Markdown先说明名称/目录不能代替数学身份，再给12专题首读表、历史/来源/全仓资产入口、五轴账本与精确命题账本。它明确“下表只说明文件角色”，关联Claim由资产包汇总，不能解释成该文件逐一证明全部所列命题。这些限制现全部保留。原维护段要求先改catalog.json再运行`python3 research/build_catalog.py`，`--check`拒绝漏项/缺文件/缺中文/过时导出；这是旧维护说明，非本批执行或现行清洗入口。

旧显示顺序是TOPICS固定次序；同主题按package首次出现分组，WC用23已知包标签顺序，其余包保持稳定；WC组内按18角色顺序排列，其他主题保原记录次序。名称/用途对竖线、换行及方括号的转义和相对路径只影响表示。本次专题资源以原JSON索引保存，原Markdown精确字节与全排序仍可复原。

Claim显示读取assets每个包的proof/tests/records/examples/reviews/candidates/sources/implementation八种路径角色，对每条目录路径聚合Claim集合，按字典序只展示前三个，超过三个另显示总数与命题合同链接。全表实际可见479个不同ID，已读作身份标识；它们的完整显示值与每行总数保在分主题资源及逐项数据中。这里未把479个ID重新证明，亦未额外done assets.json。18种role的旧人类含义如下：

| role | 原显示语义 |
| --- | --- |
''')
for k,v in binding['role_labels'].items():lines.append('| `'+k+'` | '+v.replace('|',r'\|')+' |')
lines.append('''
### `related`与`related_paths`的真实差异

原JSON的779..785、794..797、799..801共14条含`related`；779..785的值是779/780/783所指的完整三路径，799..801的值是779/780/801三路径，794..797为空数组。10条非空，4条空。旧validate在125行、render_rows在163行只读取`related_paths`，所以这些`related`既不参与“关联文件已命名”检查，也不会加到用途的“配套”链接；字节相等的Markdown仍遗漏这个JSON字段的可见表示。

最小实际例是779：对称条件矩资源原记录有指向正文/审查/运行证据的`related`，而该行不会因此出现三个配套链接。新资源明确保两个键以及空/缺席差异，[14项实据](../../../../tools/evidence/catalog-semantic-resources/hidden-related-fields.json)逐条列值。把读取处统一接受两个键并做顺序去重是可接续修正建议；本批没有作用于冻结JSON/生成器，没有声称该修正已运行验证，也不从资源链接推断数学依赖。

### 旧包的显示名字

这23个映射只解释旧排表名字；原111种取值不强行归并成23个数学对象。

| 原package | 旧显示名 |
| --- | --- |
''')
for k,v in binding['package_label_dictionary'].items():lines.append('| `'+k+'` | '+v+' |')
lines.append(r'''
## 当前比较与两处数学状态校正

原名称/用途一字不覆盖；以下是本批与真实已交付正文全文比较得到的当前注记。历史记录中的“仍开放”“当前较强”“独立”必须保持其对象和版本，不能由更新的目录多数票决定真值。

### 五人2.061695是保留旧界，不是当前最强比较

原entries[60]说恰五人零根背景的“当前较强上界”β≈2.061695、有理证书尚未达到半覆盖。同目录entries[2089]已列五人half完整证书。实读当前[五人半覆盖](../定理/五人半覆盖--定理.md)全文确认：有限单位客户集、有限非空共同目录、恰五名单位权提供者、全部有序历史完整纯SPE、零根背景；允许空主题、重复、零客户和任意离轨平局。对任意合法五主题比较元组覆盖O，证明2W−O≥0，取最优元组即2W≥OPT5。因此2.061695旧数值界及其索引机制仍可保存，“当前较强”和五人half未证的时态不再适用。

该正式证明不是用浮点最优值作结论：53行非负整数乘子（共同分母10^22）乘真正SPE不等式，经完整6144类系数域、零常数及32重数型等精确剩余验证，得到2W−O为合法非负组合。实际正文含局部定价投影、末两人强重叠比较与全部系数证据。此处用其完整已交付证明纠正目录比较状态，不复制成另一份发现，也不将旧模板可行点当half反例。

证据层级保持：用户交付的精确计算机辅助证明，内部数学复核与同实现复跑；历史“两份实现”没有第二份可运行主域primary程序随包交付，不能因此补签两实现认证。未据此声称外审、新颖性、锐性。更不把恰五人结论改成一般背景五人、恰六人或任意人数结论。

### 弱iid全局桥已有原模型反例

原entries[100]保存动态独立查询债务接口与弱逐步漂移反例，但末句“较弱全局桥仍开放”不再准确。已全文比较当前[福利支付反例](../反例/独立同分布福利支付--反例.md)及[实际前缀局部漂移](../反例/实际前缀的独立同分布局部漂移--反例.md)。Z_m是同一静态均分游戏对称混合Nash的iid抽样期望覆盖，不是最大任意iid覆盖，也不是真安全值v_m。反驳的是动态W≥(1−1/(2m))Z_m，既不否定静态基准也不反驳half。

可接续的精确见证：m≥2,J≥2，A含2客户，B含2(m−1)客户，J个独有c_j，全部不交；共同目录为A,B,Q_j=A∪{c_j}。根选A，其余非末位选B。末位令s为历史中小主题A/Q的次数：s=0选Q1；s=1且唯一小主题A则选B；s=1且唯一Q_j则选另一预定Q_l；s≥2选B。每个有序历史都定义，包括重复。s≥2时选B收益>2而偏离小主题≤5/3；s=1且旧A时B与新Q并列2；旧Q时非末位B收益>2、末位另一Q与B并列2，其他偏离≤2；s=0非末位各根偏离真实后继得2，末位Q得3最佳。故是完整纯SPE，终局AB^(m−1)，W=2m，OPT_m=2m+min(J,m−1)。

令g_m(t)=m^−1∑_(i=0)^(m−1)(1−t)^i，对静态q_B=r、q_A=0、q_Q=(1−r)/J，有U_B=2(m−1)g_m(r)、U_Q=2g_m(1−r)+g_m((1−r)/J)、U_A<U_Q。U_B−U_Q严格递减且两端异号，唯一内根r*给对称混合Nash，Z_m=mU_B(r*)。m=20,J=100，取rbar=25/27：135·25^20<29·27^20与逐项Bernoulli给U_Q(rbar)>5543/2700>513/250>U_B(rbar)，所以r*<rbar。且

$$\frac{39}{2}U_B(\bar r)-40=\frac{7-20007(2/27)^{20}}{500}>0.$$

因此(39/40)Z20>40=W，而OPT20=59。该实例有140客户、102主题；140不是最优20主题覆盖。完整正式正文另证所有m≥41的族，本批不靠新近似根或重跑软件补证。60客户五人实际路径的局部漂移反例却仍满足弱全局桥；它只否定局部归纳式，不能借它单独反驳全局桥。两个对象和真实安全值聚合桥保持不同。

## 滞后路由与当前任务范围

entries[794]把实际active_research.json称为固定UM-TARGET-v1、unrelated-machines的合同，entries[795]也以“新题默认”指该旧身份。但同冻结来源实际JSON是schema2，target_id=Q-CAG-HALF、default_save=customer-attraction，并列Boss/cleaner/editor三角色及旧入口兼容重定向。这是可核的同来源目录滞后，不只是今天另换了焦点。实际配置/检查器已在前批完整清洗；此处旁读原字节分别SHA `cb52c2d1d43699ff4ad1c79ca17c9e0b6de7146b810005df83a9d7b8ba571af6` 与 `2b38761ce4a292d024c6357644e9f15d4c9def7cb723c8aa87507bca885e057b`，不额外done。

那份schema2 goal自身仍是任意人数的历史目标；现AGENTS是Q-CAG-HALF-6、恰六人全部完整历史纯SPE。旧检查器的Q-CAG-HALF子串通过不能认证恰六人与一般人数相同。历史policy_version、source授权文字、角色操作和提交说明只作为资源，不在本批执行或覆盖现行清洗任务。

## 全部35改名的身份保全

原renamed_paths只是旧目录维护的35个路径对应；不保证两份正文数学等价，不指示现在删文件。以下保所有原键和值：

| 原路径 | 原映射目标 |
| --- | --- |
''')
for k,v in x['renamed_paths'].items():lines.append('| `'+k+'` | `'+v+'` |')
lines.append('''
## 自查、关系判断与接续

完整阅读范围在[阅读进度](../../../../tools/evidence/catalog-semantic-resources/reading-progress.json)保原索引0..2098；UM后段使用精确用途字典加逐记录名称/路径/role/package/关系编号的无损视图，创建视图不自动记阅读，实际完整读取后才确认上一块。先前十小主题及WC分块在会话中实际读原字段，本次不伪造当时不存在的逐块转录。479个可见Claim身份列表、三份当前正式数学正文的完整旁读字节也归档。原proof/原成功same-SHA suite没有重复跑；本批新有限检查仅目录表示、字段保全、资源完整性和字节绑定。

数学对象、来源资源、内部审查、外审、软件实现和有限计算六层保持分开。主源两个目录都语义integrated；被引用数学、assets/review_status/FILES以及原审计程序不因成为依赖而额外done。本批没有再尝试取消的141旧blob核验，没有Git命令、网络补对象、共享树旧程序写入或认证动作。

关系判断：12专题资源与本总资源是“完整字段的分拆表示”，JSON和Markdown是有遗漏字段差异的生成表示关系；相关旧生成器资源解释其合同。两处当前数学注记由真实正式正文支持，可作为版本纠错来源关系；目录的“配套”与Claim聚合未逐命题证明，故不导入为2099条因果边。阶段三再按精确对象和实际证据逐边判断，允许此资源暂时孤立。先前完成来源与他人所有页保持原件，不覆写旧历史或补签当时取不到的证明。

后续修正旧目录的最小范围是：entries[60]移除“当前较强”的比较时态并指向五人half；entries[100]把弱全局桥开放改为已有一般反例并保局部例的不同范围；entries[794]/[795]对齐同冻结schema2的真实CAG路由；另给两个关联键明确schema。以上仅建议，冻结原件未修改。当前六人任务、一般调度突破与外审状态都没有由目录清洗升级。
''')
(R/name).write_text('\n'.join(lines))
print(len((R/name).read_bytes()))
