---
id: "unrelated-machines/check-preservation-test-contract"
kind: resource
type_tag: "资源"
title: "TeX 保真检查器测试合同、边界族与递归项目审计"
status: "integrated-verification-resource"
truth_status: "test-contract-not-mathematical-evidence"
review_level: "full-source-read-cross-archive-comparison"
scope: "expected tests for math preservation, protected content, approved symbol maps, and recursive TeX project traversal"
source_refs:
  - "clean:e9f2d7002f97c09165ae:research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/tests/test_check_preservation.py"
  - "local:archives/unrelated-machines/tools/evidence/check-preservation-tests-20261031/original/test_check_preservation.py"
  - "local:archives/unrelated-machines/tools/evidence/check-preservation-tests-20261031/comparisons/comparison-notes.md"
  - "local:archives/unrelated-machines/state/资料/TeX安全润色、符号保全与源到输出审计--资料.md"
  - "local:archives/unrelated-machines/state/资料/TeX安全润色与受保护内容验证边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
  - "local:archives/unrelated-machines/state/资料/论文论证重构与主张证据对齐--资料.md"
  - "local:archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
source_identity:
  inventory_blob: "46c4bb7906da00f70fe8c8824dc5be2feddddc5f"
  source_sha256: "76d46348717e3a597a5d88ca5fd6fa0f1a57dba7436ec83903e29dc80e173305"
  source_size_bytes: 60524
  source_line_count: 1479
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/check-preservation-tests-20261031/original/test_check_preservation.py"
  - "archives/unrelated-machines/tools/evidence/check-preservation-tests-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/unrelated-machines/state/资料/TeX安全润色、符号保全与源到输出审计--资料.md"
  - "archives/unrelated-machines/state/资料/TeX安全润色与受保护内容验证边界--资料.md"
  - "archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
  - "archives/unrelated-machines/state/资料/论文论证重构与主张证据对齐--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
---

# TeX 保真检查器测试合同、边界族与递归项目审计

## 来源身份与处置

本对象完整实读 clean source `e9f2d7002f97c09165ae` 对应的上游 `paper-polisher/tests/test_check_preservation.py`：1479 行、60,524 字节，inventory blob 为 `46c4bb7906da00f70fe8c8824dc5be2feddddc5f`，SHA-256 为 `76d46348717e3a597a5d88ca5fd6fa0f1a57dba7436ec83903e29dc80e173305`。原字节保存在 [test_check_preservation.py 原文证据](../../tools/evidence/check-preservation-tests-20261031/original/test_check_preservation.py)，和相邻资料的比较在 [comparison-notes.md](../../tools/evidence/check-preservation-tests-20261031/comparisons/comparison-notes.md)。冻结索引记录的两个来源提交为 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

处置为 `integrated` 资源。这个文件是对 `check_preservation.py` 实现应满足的可执行测试合同和边界族，不是 TeX 语言全覆盖证明，也不是数学定理。测试中动态加载 sibling script；该实现是另一 clean source，本 receipt 不把实现细节或测试通过状态冒充已审计的数学正确性。未在本次 receipt 中声称运行整套测试、编译任意稿件或完成 PDF/HTML 渲染。

## 测试组织与总合同

源文件包含两个 `unittest.TestCase`：`MathPreservationTests` 直接调用 `check_math_preservation`，`EndToEndPreservationContractTests` 通过临时目录调用命令行脚本，检查静态内容、结构键和项目递归。测试的共通合同是：语言润色可以改变允许的 prose/layout，但必须保留数学对象、结构、引用/标签、数字和 literal 内容；模式参数（尤其 `--allow-additions` 与 `--approved-symbol-map`）只能扩大明确授权的空间，不能绕过硬保护。

测试辅助函数把一对原始/润色字符串写入临时目录，执行脚本并根据返回码判断通过/失败。它们使用 `assert_pair_passes`、`assert_pair_fails` 和 `assert_rejected_in_all_modes` 把“默认模式和 allow-additions 都拒绝”写成重复检查。该结构适合发现回归，但返回码通过只说明测试输入满足当前实现的合同，不说明任意 TeX 文档或所有宏包均被识别。

## 数学区域和分隔符边界

`MathPreservationTests` 覆盖 `$...$`、`$$...$$`、`\(...\)`、`\[...\]`、equation 以及嵌套 aligned/xalignat 等环境；也覆盖 standalone `\ensuremath`、tikzpicture 中的数学和数学环境中嵌套 `\text{...}`。布局空白与数学注释可变化，但可见 `\text` 内容、变量、运算符和环境种类必须稳定。测试要求区域一一匹配：删除、插入、重排、重复区域不通过；allow-additions 不能在已有数学区内插入，也不能引入新的数学区。

边界测试包含 TeX `%` 注释的行拼接语义：注释可能连接 token，但不能凭“视觉上有空格”擅自改变 `\text` 内容。注释和 `\verb`、URL/path 等 opaque command 参数中的 `$` 不应误识别成数学起点；但 `\href` 的可见文本仍需检查。未闭合数学分隔符和未闭合数学环境必须 fail closed。label 绑定与公式变量同时改变时也必须失败，防止只比较数学字符串而漏掉结构联系。

## 数值、单位、符号和数量词

端到端测试把数字语义列为所有模式的硬保护。测试字典覆盖：整数/小数、正负号、Unicode minus、`±/∓`、百分号、SI 与自定义单位、复合单位、货币、时间词、样本/折数/epoch 等计数词、上标/下标数字、分数、圈号、全角数字、显著性星号/匕首、数字宏、数学中的数值、`\verb`/`\texttt` literal 数字、独立单位/货币/符号 cue，以及注释拼接、TeX 空格和 `\hspace`/`\mspace`/`\kern` 等间隔命令。

测试同时保留允许的 prose 变化，避免数量扫描器把普通代词或序数当成不可编辑数字。例如“Experiment 2 presents”可改为“shows”，“One can observe”可改为“We can observe”，“We second the recommendation”可改为“support”，但“One model”改成“Two models”必须失败。区间 `1--2` 可改写为 `from 1 to 2`，说明 dash-free prose 规则可以和数值保全共存；终止小数点也可以移动，只要数值 token 未改变。这个负向/正向配对使测试同时约束过宽和过窄的 scanner。

`--allow-additions` 不允许通过“先改数字再把旧数字加回另一处”来掩盖变化；插入新的数字、数学区、结构或保护内容都会失败。测试因而把 additions 解释为对普通 prose 的受限授权，而不是对 claim、数据、单位或公式的授权。

## TeX 结构、环境和资产键

端到端测试保护环境种类、选项、表格列导言、`multicolumn` 对齐、`multirow` 布局参数、组平衡、嵌套环境和 theorem/section 结构。可见 theorem 标题可以润色，正文不变；但 section/itemize 删除、环境类型改变、未平衡组或错误 begin/end 必须失败。`label` 的键和值绑定必须保持，即使键的计数相同也不允许交换。

引用和资产层覆盖 `includegraphics*` 路径、`pageref`、`textcite`、嵌套 citation note 中的 `ref`、BibLaTeX 的 volcite/pvolcite/ftvolcite、多引用和 hyperref key。测试也覆盖 bibliography display number 的特殊情况：文献表的显示数字变化仍是数值变化，不能因看似排版数字而放过；BibTeX key 改变同样失败。这个范围说明“保留引用”不仅是保留 `\cite` 命令名，还包括内部 key、定位参数和嵌套引用。

## comment、literal 与 opaque 区域

测试把 comment、verbatim、`\verb`、`\Verb`、`\SaveVerb`、fancyvrb restore、minted/lstinline 等当作硬保护。注释内容、注释与正文的边界、literal 的字节和空白、命令星号、listing language、保存 literal 名称都不能改变；即使可见数学相同，也不允许把一行 comment 移动到数学后、把 comment 转成 verbatim、把 inline literal 换位置或改变 literal 空白。这个合同保护的是 source-level semantics，不能用“渲染后看起来一样”替代。

## approved symbol map 的窄授权

`--approved-symbol-map` 允许显式的一对一数学符号替换，例如 `M=N`、`x=u`、`y=z`；选项可重复，但只允许真正的 math symbol token。测试拒绝数字、正负号、分数、圈号、文字数字、Roman numeral、货币、百分号、TeX 命令和粗体文字映射，并拒绝额外数学变化、prose 变化、text-mode acronym 变化、label key 变化、comment/literal 变化和 literal 空白变化。

批准映射不能改写 `\operatorname`/`\mathrm` 中的数学名字；它只允许声明的数学 token 替换，其余 protected ledgers 仍逐字或按各自规范比较。测试覆盖多种 literal 命令，证明 literal 里的 `$M$` 不因外层 map 而获得授权，外层 math `$M$` 才能按 map 变化。这一组测试把 author-approved notation normalization 与数字/结构/文本编辑严格隔开。

## 项目模式与递归路径语义

测试在临时项目中构造 `main.tex` 与嵌套 `\input`、`\include`、`\subfile`，验证 `--project` 会递归至深层文件并发现隐藏的数学变更；没有 `--project` 时，单文件模式可以不递归，这是显式模式差异而非遗漏。缺失 include target 必须失败。

另一组测试覆盖 import family：`import`、`import*`、`subimport`、`inputfrom`、`includefrom`、`subinputfrom`、`subincludefrom`，并检查空静态目录、项目根重置、前一 import 目录回退、subfile/subfileinclude 的目录上下文和 nested input。测试说明路径解析不是简单“相对当前文件”规则，而是取决于 TeX 命令族及其 import stack。动态或空目录表达式不能安全静态解析时，project mode 应 fail closed 并报告 dynamic/empty。

这些测试尤其适用于多文件论文的 source-bound 审计：主文件未变化不能推出被 include 文件未变化；必须确认递归覆盖、路径解析、缺失目标和动态导入状态。它们仍不执行 TeX 编译，因此不能说明宏展开后 PDF 语义、字体、浮动体或渲染布局正确。

## 与相邻资料的关系、唯一增量与使用边界

与 TeX 安全润色两份资料相比，本源把抽象的保护规则落为可复现的正/负输入对和路径递归夹具；它新增具体 edge cases，但不重新定义 mode precedence。与 Artifact 验证资料相比，它只说明 preservation checker 的 source-level expected behavior，不提供 execution、render 或 freshness 证据。与论文论证重构和反防御审计相比，它保护公式、数字、引用、否定和结构键的技术载体，但不判断一段 prose 的 claim 是否被证明；与数学写作文类资料相比，它不能决定对象是定理、障碍、反例还是有限实验。

该资源可用于第三阶段审计：运行测试时记录实现版本、Python 版本、依赖、测试命令、通过/失败数量和 stderr；若实现缺失 sibling、可选宏包或环境导致测试不能运行，应记录 blocked/needs-source。单元测试通过后仍需对真实稿件运行 checker，并按 text/source/execution/render 分层保存 receipt。不要把测试 fixture 中的 `M`、`N`、数字或路径当作当前 UM 数学对象，也不要把源代码测试合同迁移成调度定理、算法保证或文献优先权。

## 未覆盖项和停止条件

本源没有证明 checker 对所有 TeX 宏、catcode、展开时命令、外部资源或任意编译器均完备；没有覆盖所有 biblatex 宏、LuaTeX/XeTeX 特殊语法、动态 Python/TeX 生成内容或渲染可见性。测试失败可能反映实现 bug、测试环境或未支持语法，必须回到实现和源文定位。清洗本来源只完成测试合同的准确归档；数学正确性、论文完整性和 PDF/HTML 可见渲染仍需各自证据。
