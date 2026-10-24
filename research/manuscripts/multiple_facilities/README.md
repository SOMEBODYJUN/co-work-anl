# 任意设施数共同目录的因子二存在性论文

[英文主稿](main.tex)将已有 SC-K-2-E 证明整理为两节：Introduction（含完整模型及主要结果），以及以字典序转移预算、原子装箱和保上界修复为主链的证明。定理的最后证明直接调用已证引理并补全所有带标签布局的续局。

本稿不是新数学身份，现行精确范围仍见 [model.md](../../current/multi_facility/model.md)、[uniform_two.md](../../current/multi_facility/uniform_two.md) 和 [claims.md](../../current/multi_facility/claims.md)。它仅覆盖共同目录，存在量词允许指定一整套精确客户均衡；一般位多项式构造与全设施数黄金比猜想仍未解决。

- `main.tex`：完整英文正文，不依赖内部 Markdown 承担证明。
- `references.bib`：本稿实际引用文献及公开版本。
- `main.pdf`：由当前正文生成的阅读稿。
- `WRITING_STATE.md`：用户的结构要求、来源与未决期刊格式，不属于论文正文。
- `REVISION-NOTES.md`：本轮已读英文范文、叙述改动范围及两项审查精度修正。

编译命令（在本目录运行）：`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`。

当前使用 `amsart` 成文稿格式；尚未指定最终投稿期刊，不能视为某刊的最终投稿模板。作者身份留空。未将现有内部审查升级为外审或优先权认证。
