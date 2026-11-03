---
id: unrelated-machines/tex-checker-implementation
kind: resource
category: 资源
title: TeX 保真检查器实现脚本的结构与执行边界
status: integrated-implementation-resource
truth_status: source-read-code-boundary; help-and-compile-verified; no-mathematical-claim
source_refs:
  - clean:96419c9b43c635697b7e
related_objects:
  - archives/unrelated-machines/state/资料/TeX安全润色与受保护内容验证边界--资料.md
  - archives/unrelated-machines/state/资源/TeX保真检查器测试合同、边界族与递归项目审计--资源.md
---

源文件 `check_preservation.py` 共 3500 行、125543 字节，是 paper-polisher 的实现脚本。全文读取后，静态结构为 70 个顶层函数与 9 个数据类/记录类，依赖仅为 Python 标准库（`argparse`、`re`、`sys`、`collections`、`dataclasses`、`difflib`、`pathlib`）。它不包含研究数学模型、优化器或外部网络调用。

## 实现覆盖

代码先处理注释、转义、平衡组和命名环境，再对数学区域、literal/opaque command 参数和 TeX 非 prose 区域做 masking。主要检查器包括：

- structural command/key 的解析与序列比较，覆盖 label/ref/cite/bibliography/image 等键；
- math region tokenization、数学区域顺序与 parse issue；
- 数字、单位、货币、百分比、符号和显著性标记的 occurrence 与顺序保护；
- placeholder reference、硬编码 Figure/Table/Equation/Section 编号、reference-name style 和 prose dash 检查；
- `--allow-additions` 的普通 prose 增量模式，以及 `--approved-symbol-map OLD=NEW` 的授权符号归一化模式；
- `--project` 下对静态 `input/include/subfile/import` 的递归加载、缺失/动态/循环 include 报告和相对路径解析。

`load_tex_project` 维护 include stack 并报告 missing/cyclic targets，`check_math_preservation`、`check_numeric_preservation` 与 `check_structural_preservation` 分别给出 protected sequence 的差异；主函数只返回检查状态，不声称 TeX 编译、PDF 渲染或数学正确。

## 实际验证和限制

本批实际运行 `python3 .../check_preservation.py --help`，exit 0，确认命令行参数为 `original polished`、`--limit`、`--allow-additions`、`--approved-symbol-map` 与 `--project`；`python3 -m py_compile` 也 exit 0。没有虚构任意稿件的 preservation pass、编译、渲染或语义单位解析。

实现边界与相邻资料一致：checker 是 source-to-output/static preservation 工具，不理解所有自定义宏、figure 内嵌文字、任意自然语言量词或完整数学语义。`--allow-additions` 仍不授权新增结构键、数学、数字、单位或 sign；approved mapping 只在精确授权范围内改 symbol。要称 FULL MANUSCRIPT 或 Render-bound，仍需 authoritative root、静态/动态 include 清单、编译结果和高风险页面视觉检查。

原始脚本、help/compile 输出、SHA manifest 和比较记录见 [evidence](../../tools/evidence/tex-checker-implementation-20261031/README.md)。该源处置为 `integrated` 实现资源，不产生新的 UM theorem、approximation ratio 或 hardness 结论。
