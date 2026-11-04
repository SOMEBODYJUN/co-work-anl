---
id: facility-games/manuscript-build-scripts-continuation-review-20261031
kind: review
type_tag: 审查
title: 异构与共享黄金比稿构建脚本接续审查
status: complete-source-read-build-contract-preserved
truth_status: build-script-provenance-only; frozen PDFs remain mathematical evidence; local TeX replay environment-limited
review_level: full-clean-show-read-and-local-replay-attempt
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/manuscripts/heterogeneous/build.sh
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/manuscripts/heterogeneous/build.sh
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/manuscripts/shared_phi/build_manuscript.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/manuscripts/shared_phi/build_manuscript.py
evidence_paths:
  - archives/facility-games/tools/evidence/manuscript-build-scripts-20261031/manifest.json
  - archives/facility-games/tools/evidence/manuscript-build-scripts-20261031/heterogeneous_build.sh
  - archives/facility-games/tools/evidence/manuscript-build-scripts-20261031/shared_phi_build_manuscript.py
  - archives/facility-games/tools/evidence/manuscript-build-scripts-20261031/heterogeneous_replay.stdout
  - archives/facility-games/tools/evidence/manuscript-build-scripts-20261031/shared_replay.stdout
related_objects:
  - ../审查/共享目录黄金比主稿源码与PDF接续审查--审查.md
  - ../审查/异构主手稿完整证明与现行对象接续--审查.md
  - ../资料/双设施黄金比连续稿与固定菜单证明合同--资料.md

# 异构与共享黄金比稿构建脚本接续审查

本批读取两份构建脚本。它们只负责从已经存在的 `main.tex` 编译 PDF，不生成或改写数学正文；因此本审查只登记构建合同、依赖和实际重放边界，不把脚本运行成功当作数学证明。

## 1. 来源身份

| source ID | 路径 | blob | 字节 | SHA-256 |
| --- | --- | --- | ---: | --- |
| `75d42852649cd59a5e7c` | `history/source/manuscripts/heterogeneous/build.sh` | `41d471329e83c2f7ace913ab5b85d73210522ae1` | 908 | `3260a39ed0f5a5d69596de7bc2d8ce20b5757b8b49e038c26abd2541ee22eeda` |
| `3e063894e44fb056b63d` | `history/source/manuscripts/shared_phi/build_manuscript.py` | `73b91d7d6e8152e8c4118fda1aa463df27306ba6` | 1037 | `3dd5e75a80acf9a7c6f77bcf4af61fdd017897c107cdb34ad76b5b1f377c4725` |

原件副本与 replay transcript 保存在 `archives/facility-games/tools/evidence/manuscript-build-scripts-20261031/`。

## 2. 异构稿 `build.sh`

脚本进入自身所在目录，创建 `build/`，检查 `kpsewhich article.cls` 和 `pdflatex.fmt`。若 filename database 缺少，它设置 `TEXMF`、`TEXINPUTS`、`TEXFORMATS`，用 `pdftex -ini -etex` 生成本地 `pdflatex.fmt`，再对 `main.tex` 连续执行两遍 `pdflatex -interaction=nonstopmode -halt-on-error`，日志分别写入 `build/pass1.log` 和 `build/pass2.log`。它不调用 Markdown、Python 研究脚本，也不变更 source 文字。

本地 replay 将现有冻结异构 `main.tex` 复制到隔离工作区后运行脚本。该环境能够生成 format 并开始读取 `article.cls`、`geometry`、`mathtools` 等包，但在本次执行窗口内没有形成最终 PDF；冻结 `main.pdf` 已另行保全并由主稿审查逐页读取。构建脚本因此只能登记为“正确的两遍编译合同，当前运行受 TeX 环境/时间边界限制”。

## 3. 共享黄金比稿 `build_manuscript.py`

Python 脚本以自身目录为 `out`，创建 `build/`，复制环境变量并在 `/usr/share/texlive/texmf-dist` 存在时设置 `TEXMF`。若本地 `build/pdflatex.fmt` 存在，它把 `-fmt=` 路径传给 `pdflatex`；否则直接执行 `pdflatex -interaction=nonstopmode -halt-on-error main.tex`。两遍编译分别写入 `compile_polynomial_pass1.log` 和 `compile_polynomial_pass2.log`，任一非零返回码立即退出。脚本最后只打印 `main.pdf` 路径，明确“never regenerate its mathematical text”。

本地 replay 使用冻结 `shared_phi/main.tex` 副本运行。当前 runtime 缺少可用 `pdflatex.fmt`，`mktexfmt` 配置没有 `byfmt=pdflatex` 条目，脚本在第一遍退出；日志和状态已保存在 evidence 目录。README 中“pdfTeX 1.40.25、两遍编译、25页 PDF”是来源自报，与本批读取到的现存 PDF metadata/pypdf 25页相符；本次环境错误不应改写成源码数学错误。

## 4. 与主稿数学对象的关系

两脚本只影响 PDF 生成和复现，不影响：

* 共享目录黄金比稿的 P/E/T/C 菜单、闭响应环、强弦和两锚证明合同；
* 异构主稿或通用因子二对象的数学量词；
* 外部同行评审、候选状态或有限测试证据。

数学正文仍以 clean-show 的 `main.tex`、冻结 `main.pdf` 和对应审查对象为准。构建脚本中的 `set -euo pipefail`、两遍编译和日志路径可作为复现说明；它们不提供证明、LP 证书或模型扩展。

本批两源已实读、保全并记录本地 replay 边界；未执行 Git commit、push 或 `clean done`，Boss 串行 checkpoint 后再按 receipt 逐来源确认。
