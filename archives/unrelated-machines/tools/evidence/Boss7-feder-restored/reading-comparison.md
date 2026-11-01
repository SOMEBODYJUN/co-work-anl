# Boss7：Feder 全文阅读、数学核对及语义处置证据

## 材料与权限范围

只处理已有认领源 `d0fcf01aa8bd6952ea25`。读取 AGENTS.md、cleanup/README.md、cleanup/OBJECTS.md、tools/README.md；使用 edit-chinese-math-paper 的先审数学、保留缺口、再给正式中文顺序，并读取 PDF 技能。未调用 work.py 的 start/register/doctor/claim/done/send/handoff，未访问仓库外凭据，未重试失败写端点，未执行 git add/commit/push。本批为本地实质清洗、待父级统一推送。

## 重新取源与转换

通过 `python tools/cleanup.py --repo . show d0fcf01aa8bd6952ea25 --out .../feder-original.ps` 直接导出冻结原件。SHA-256 与 inventory 一致，159618 B。工具检查确认 gs、pdftotext、pdftoppm 可用。Ghostscript 首次因系统 /tmp 不可写失败，随后将 TMPDIR 设为本工作区下临时目录重跑成功；这不是认证或写端点重试。系统 `/usr/bin/pdfinfo` 确认 12 页。提取 `pdftotext -layout` 全文为 552 行、42030 B，与上次留存 clean.txt 字节相同，但本次原件另行导出并核哈希。

`/usr/bin/pdftoppm` 转出的 3、8、9、10、11 页已实际用 view_image 查看。旧 Type 3 字体触发 Bad bounding box 警告；页面可读，否定文字上横线在图像中存在而文本提取会丢失。因此 `¬x∨u`、`¬x∨v`、负二文字子句、归结公式均按图像核准。没有把抽取文本无上横线的词当作原始正文字面含义。

## 逐页实际阅读

|印刷页|实际读域及保留内容|
|---|---|
|1|摘要、三分研究背景、Schaefer 三类与 CSP 结构动机；不把摘要当全文|
|2|一般 CSP 同态背景、bounded-width/subgroup 线索、扇出复制动机、网络稳定性起源|
|3|网络 adjacency-preserving、图 CSP、graph matching/matroid parity 背景、广义拟阵与共独立定义；目视核 bases/independent 所指|
|4|二部交动机及有限关系结构/固定模板/同态定义|
|5|retract/core、常量背景、定理1、bounded/strict width 的推断闭包说明|
|6|支撑 f、三元多数 g、群陪集 ab^{-1}c、Boolean 异或、实凸闭包；函数门/常量/吸收/COPY 定义|
|7|定理2及历史归属、非Boolean monotone/nonexpansive、图/二部恰两次约束定义|
|8|关系实现、二部保留端口同侧、定理3、Fact1/Fact2 起始；目视核负号|
|9|Fact2 最小反例/奇偶分组、Fact3 二文字子句、Fact4 多数失败与三支持组、二部单调子句；目视核公式|
|10|定理4、笛卡尔直和/相等配对消去、交换失败最小K、三坐标 A/B/C 全分支；目视核下标/关系|
|11|三次使用到循环复制、共独立路径法、定理5二部交、不可实现相等/蕴含下交换及补位；目视核正负子句|
|12|一般复杂度开放的来源当时状态、固定模板/常数块、完整参考文献；未将列出的引用原件当作已另行全文读过|

## 数学审查与已落实修正

1. 非空固定Hamming权关系对应普通拟阵基族；不是全部独立集族。原文 uniform generalized matroid 的表达不能写成独立集公理。
2. coindependent 是禁止点在超立方体图中不相邻，非 matroid-independent，也非对每个集合取补的对偶拟阵。
3. binary EQ 与 ternary COPY 区分；定理5可实现binary EQ只消去二部性，不能单凭它判NP-hard。
4. 关系直和在向量表示是Cartesian product；不是不同向量集直接集合并。
5. 变量恰两次约束、二部外端同侧、常量、固定有限模板均显化；全子句可实现不自动等于SAT-hard。
6. 定理4的5种A/B/C分支、min到fork、三次使用的正负文字、循环复用保留；闭包只提供fanout obstruction证据，不升级成所有generalized matroids易解。
7. 共独立算法和定理5补位在来源中很压缩。正文记录来源定理并紧贴复用断点标待补：搜索状态/失败证书/复杂度，以及padding、两个oracles、回投见证；不声称本次实现。
8. 原文开放结论加“当时”；仓库KKR资料已给even子类后续多项式进展，不能继续笼统写该子类开放。

## 全仓比较的实际范围

先 `rg` 全仓档案中的 Feder/generalized matroid/fanout/扇出/拟阵与相关术语，再读以下正式对象。comparison 子代理作为 Boss7 内部只读 Solver 同时完整读了相关审查；父Solver也读了下列承重正文或其明确段落。仅以下Feder PS是本批重新读的原始文献；其他比较基于已清洗对象，未冒称重读其原PDF。

- 本篇旧Feder正式对象：发现基族、coindependent、binary-EQ困难性、开放时态的表达需修正。
- `archives/matroid-structures/state/资料/两份拟阵文献精读与适用边界--资料.md`：全文比较。独立集/基/一般graph-matching非matroid；evenΔ子类、输入表示与非matching-realizable边界。后续进展非来源当时结论。
- `archives/unrelated-machines/state/文献/稀疏CSP与平坦矩阵两篇文献整理--文献.md`：全文比较。小目标同态与girth的Kun稀疏化不同于恰两次出现；Laurent矩扩展不是本篇广义拟阵。
- `archives/unrelated-machines/state/文献/Davies-Rothvoss-Zhang--Santa拟阵超图--文献.md`：全文比较。独立元素/基/资源超匹配分离，非Feder端口关系。
- `archives/unrelated-machines/state/障碍/私有需求组合与共享三维匹配复制--障碍.md`：全文比较。3DM完全池为分母分数解整数化，parity张量的边匹配非端口parity。
- `archives/unrelated-machines/state/审查/近单位PCSP蕴含与物理复制义务最终范围审查--审查.md`：全文比较。r≤k−3时weak投影full cube，ordinary non-delta不承担weak soundness；physical compiler未闭。
- `archives/unrelated-machines/state/审查/近单位PCSP与单位presence胶合双源审查--审查.md`：全文比较。两实际见证presence胶合不等于源Boolean复制；其PCSP限制同前。
- `archives/customer-attraction/state/资源/旧图不相关机节点和关系的量词与实现--资源.md`：只读UM-SOURCE-FEDER-ORDINARY-FANOUT等约4680–4760行与相关open-transfer约16320–16390行；旧targeted阅读不充本次全文证据。

comparison 子代理另读加权扇出二度、零缺陷/加权扇出、三维匹配高维配额等审查及非负列拟阵基舍入对象，用于排除同名“扇出/匹配”的自动推导；未把其全部原始来源纳入本批完成声明。

## 证据强度、关系与未做事项

来源定理和证明机制依原件记录，非新定理、非形式验证、非独立软件实现或新颖性/外审认证。配对闭包、三坐标困难性分支和普通/二部模型可复用；共独立solver及padding编译仍需补实现细节。后续even-Δ算法是特定子类推进；PCSP物理迁移与六人SPE没有自动边。第二阶段本页保留有解释的比较链接，未自行改第三阶段map。

完成前自查：源hash/长度匹配，12页有逐页内容记录；公式含否定文字经图像复核；formal所有本地链接存在；Markdown无diff whitespace错误；receipt为pending-push，未声称done。
