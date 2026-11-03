---
id: "unrelated-machines/artifact-verification-reference"
kind: resource
type_tag: "资料"
title: "Artifact 验证层级、执行/渲染与证据新鲜度"
status: "verification-policy-read-and-workflow-compared"
summary: "上游数学写作参考把文本、来源、执行、渲染四种验证层级分开，并给出 notebook、TeX/PDF、MathJax 及 source/output/preview 新鲜度规则；本对象将其绑定到当前 cleaner 的证据合同。"
truth_status: "workflow-reference-not-mathematical-evidence"
review_level: "full-source-read-related-manifest-comparison"
scope: "text-bound/source-bound/execution-bound/render-bound verification and freshness binding"
source_refs:
  - "clean:1beaeed5bcb64a69fa73:research/weighted_congestion_frontier/upstream/mathematical-academic-writing/references/artifact_verification.md"
  - "local:tools/README.md"
  - "local:cleanup/workspaces/Boss3/root/round2_manifest.json"
  - "local:cleanup/workspaces/Boss3/receipt-round2-manifest.json"
related_materials:
  - "local:tools/evidence/multiple-facilities-paper/current-verification.json"
  - "local:tools/evidence/multiple-facilities-paper/verify_current.py"
  - "local:tools/evidence/structural-paper/current-verification.json"
  - "local:tools/evidence/shared-catalog-side-results/execution-boundary.json"
  - "local:archives/unrelated-machines/tools/evidence/unit-readout-runtime/README.md"
  - "local:archives/unrelated-machines/tools/evidence/query-witness-originals/README.md"
source_sha256: "5242c290487211fe8d9f37fa112db5b9131d531c598cdbe7ba4676291f34b644"
source_size_bytes: 2750
---

# Artifact 验证层级、执行/渲染与证据新鲜度

## 对象身份与处置

这是一个上游 mathematical-academic-writing 参考资料对象，不是 unrelated-machines 的模型、反例、定理或算法。冻结源为 `research/weighted_congestion_frontier/upstream/mathematical-academic-writing/references/artifact_verification.md`，本批 clean source ID 为 `1beaeed5bcb64a69fa73`，原文大小 2750 字节，SHA-256 为 `5242c290487211fe8d9f37fa112db5b9131d531c598cdbe7ba4676291f34b644`。完整原字节保存在 [artifact_verification.md 原文证据](../../tools/evidence/artifact-verification-reference-20261031/original/artifact_verification.md)。

处置为 `retained`。它的独有内容是“看到了什么，最多能声称什么”的验证分级、可执行输出与可视渲染的检查清单，以及 source/output/preview 的新鲜度合同。该参考不产生数学结论，也不能替代每个数学对象的定义、证明、有限审计或反例。保留它作为清洗和发布时的 provenance 资料，避免把哈希、文件存在或一次静态检查误报成执行或渲染成功。

## 原文规定的四层验证边界

源文件先把验证深度分为四层，要求最终报告写明实际达到的最深层级。

| 层级 | 必须检查的对象 | 允许的最强表述 |
| --- | --- | --- |
| **Text-bound** | 源正文、公式、记号、内部链接 | 只能说文本内部一致，或指出已发现的文字问题 |
| **Source-bound** | 指定参考文献、定理位置、引用目标 | 只能说与支配来源一致或冲突 |
| **Execution-bound** | 新鲜执行、输出、随机种子、容差、依赖 | 才能说该程序运行成功并复现被检查的输出 |
| **Render-bound** | 导出的 HTML、PDF 或 notebook 预览 | 才能说可见 artifact 按描述渲染 |

源文特别禁止三个常见越界：仅证明文件存在，不等于程序执行成功；读取旧输出，不等于输出由当前源码生成；只读源码或公式，不等于 HTML/PDF/notebook 可见页面正确。若只达到 Text-bound 或 Source-bound，应把结论限定在对应边界，而不能用“验证完成”笼统覆盖后两层。

## Notebook 检查合同

对 notebook 或代码输出，源文要求先固定精确 notebook 路径，并在 fixture 工作中记录 cell ID 与 cell hash。随后应核对代码、参数、随机种子和数学叙述是否描述同一个实验；若声称执行验证，必须 restart 并运行全部 cells，而不是依赖内核残留状态。运行时要检查 traceback、会影响结论的 warning、缺失输出以及非确定状态。执行后还要导出目标 preview，并在 preview 中检查公式、表格、caption、坐标轴、图例、单位和代码可见性。reader preview 隐藏代码不代表源 notebook 可以删除代码；源有改动而 output 尚未重生成时，旧 output 一律视为 stale。

这组规则对当前 finite audit 的含义是：脚本文件、输入 JSON、冻结输出、命令和依赖版本应分层保存。若只对 JSON 做字节/SHA 检查，得到的是 source/frozen-evidence provenance；只有在新目录中重新运行并保存 stdout、stderr、argv、seed、tolerance 和结果哈希后，才可登记 execution-bound。任何运行后覆盖原冻结输出的做法都会破坏新鲜度链。

## TeX、PDF 与数学渲染检查

TeX/PDF 工作流要求从当前 source 编译并查看 compiler result，检查 undefined references、citation failures、隐藏数学的 overfull 内容和 equation numbering。应渲染代表性及高风险页面，包括密集 display、theorem block、表格、图和 bibliography；还应检查抽取文本和可见 glyph 是否保留符号、负号、下标和分隔符。

数学渲染层还需逐项检查 inline/display delimiter 是否成对、HTML/JSON escaping 是否吞掉反斜杠、带 MathJax 的表格单元格是否造成列移位、目标 renderer 是否支持使用的 macro，以及导出后 equation label/link 是否仍然指向正确位置。源公式本身正确而 preview 断裂，属于 rendering failure；不能借渲染问题改写数学命题，也不能把静态公式阅读升级为 PDF 已成功编译或可视检查通过。

## 证据新鲜度与哈希绑定

源文把发布或 regression 工作的 reproducibility 归结为：用当前 artifact 的路径、时间戳或哈希绑定每一个声称；artifact 重生成后重新计算哈希；当 source、output、preview 的新鲜度不一致时，以最老的依赖层为准，并把后续层视为 stale。换言之，`source -> execution output -> exported preview` 是一条有方向的依赖链，任何上游改动都会使下游旧快照失效，除非重新执行或重新导出并留下新 provenance。

这和本仓库 evidence 的实际组织一致。`tools/evidence/multiple-facilities-paper/current-verification.json` 同时记录 current source hash、TeX 的 formal/label/reference 计数、逐页 PDF text hash、抽取匹配和可视检查说明；`tools/evidence/structural-paper/current-verification.json` 明确区分源哈希、TeX 语法/标签检查、PDF 页文本哈希、有限例子和 `not_claimed`，并把“有限检查不证明无限量词”写在 scope 中。`tools/evidence/shared-catalog-side-results/execution-boundary.json` 则保存实际命令、cwd、exit code、成功与失败的运行以及缺失依赖，说明“部分入口成功”不能改写为“完整套件成功”。

## 与当前 cleaner 规范的逐项比较

本批对照了 `tools/README.md`、`cleanup/workspaces/Boss3/root/round2_manifest.json` 及其 receipt，并搜索了 source-manifest、execution-boundary、replay、current-verification 和 verify_current 文件。比较结果如下：

1. **`clean show` 与原文复制属于 source-bound provenance。** 通过 clean source 的冻结 blob、路径、大小、SHA 读取原文并复制到 evidence，可以证明本批确实读到哪个版本；它不能证明该来源中的代码曾运行，也不能证明其 PDF/HTML 预览曾成功渲染。
2. **本地 SHA、控制字符扫描、JSON parse 和 manifest 结构检查是静态证据。** 这些检查确认字节完整性、格式可读性和目录关系，但不改变程序、模型或证明的真值。receipt 必须写明阅读范围和实际最深验证层级，不能只写“integrated”。
3. **`audit_code` 与 `frozen_evidence` 应保持分离。** `round2_manifest.json` 明确把脚本列为 `audit_code`、结果列为 `frozen_evidence`，并写出 Fraction/integer 与 floating-point scope 分离、复制到 scratch 目录重跑以避免原脚本在旁写文件。这是 execution-bound 之前的再现性前提；清单本身不构成 theorem。
4. **fresh execution 需要可复核边界。** 若要宣称执行层，必须额外保存新目录、完整 argv/cwd、exit code、依赖/版本、seed/tolerance、stdout/stderr、输出 SHA 及失败入口；`execution-boundary.json` 中实际的 `ModuleNotFoundError` 就是应保留的障碍，而不是用成功的旁路 probe 掩盖它。
5. **PDF/HTML/notebook 的 visible correctness 是独立层。** 即便 TeX 语法、引用和源码公式都通过，仍需编译和渲染高风险页面；若当前来源没有导出 preview，只能报告至 Source-bound，并标注 Render-bound 未达到。
6. **清洗正文和 receipt 应把失败、候选和未检查项写出来。** “文件存在”“历史输出可读”“静态计数为零”分别是不同证据，不可合并为证明、一般算法或完整执行成功。每次 source/output/preview 的版本变化都需要新的 hash 绑定。

## 处置决定与适用范围

本资料保留为当前阶段的验证政策和写作边界。它支持以下实践：

- 对数学正文先登记 Text-bound/Source-bound 的实际阅读；只有确有新鲜运行记录时才标 Execution-bound；只有确有导出及可视检查时才标 Render-bound。
- 对程序、冻结 JSON、编译产物、页面预览分别保存路径、SHA、版本、命令和 scope；不要把复现清单与结果正文合并。
- 对旧 output、旧 PDF、旧 preview 记录其来源版本；上游 source 改动后，先判断下游 stale，再决定是否重新执行。
- 在 receipt 的 `read_note`、`comparison_note`、`decision_note` 中明确哪些内容是有限审计、哪些是候选、哪些是未检查或被依赖缺失阻断的证据。

它不授权把任何 unrelated-machines 目标、weighted-congestion 参考、有限程序输出或渲染状态升级为一般定理。后续若要声称新的执行或渲染结果，应新建对应的 evidence/manifest 和 source ID，而不是修改本资料的历史处置。
