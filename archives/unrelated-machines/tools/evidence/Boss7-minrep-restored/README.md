# MinRep 原文、公式核图与审查复现

本目录服务于 [MinRep 度数与字母表逼近困难](../../../state/文献/MinRep度数与字母表逼近困难--文献.md)。整理者内部身份 Boss7；日期 2026-10-31。这里是已有认领 `533900faa02356c5f2df` 的本地工作，不包含 Git 提交、推送或 done 成功声明。

## 原件和读取

- `original/manurangsi_minrep_degree_1807_00936v1.pdf` 是 `python3 tools/cleanup.py --repo . show 533900faa02356c5f2df --out ...` 直接导出的完整原字节，134,108 字节、9 页，SHA-256 `259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8`。
- `original/manurangsi-v1-layout.txt` 为完整 `pdftotext -layout` 抽取，非人工改写；其数学排版不能替代原图。
- `rendered/page-1.png` 至 `page-9.png` 为逐页渲染，全部实际查看；印 1、3–7 页的参数、概率和证明式逐图核对。页 2 初次图像不完整，重新渲染后查看；最终校验逐张解码。
- `rendered/minzer-zheng-060.png`、`minzer-zheng-061.png` 为已归档后续论文的相关两页原图；它们揭示 δ、正则性接口及连通性 log 幂的实际问题。完整 PDF 已存在于 `../retired-literature-four-to-one-20261031/minzer_zheng.pdf`，没有重复复制。

已完整阅读全文的定义、定理 1/2/4/6、推论 3/5、引理 7/9/10、命题 8/11/12、全部证明、讨论和参考文献。没有把词条命中当全文阅读，也没有把先前 primary 比较报告当本次独立复核。

## 复现

在仓库根目录运行：

```bash
python3 archives/unrelated-machines/tools/evidence/Boss7-minrep-restored/validate_evidence.py
```

脚本核原件字节、9 页数、每张最终图像的完整解码、原抽取文本中的承重标识，并以高精度 Decimal 重算尖锐下尾系数和后续 Γ 参数常数。它只检查证据完整性与数值恒等式；完整定理依赖正文给出的符号证明，PASS 不代表软件形式化证明或生产算法运行。

如需重新生成文本与图像：

```bash
pdftotext -layout archives/unrelated-machines/tools/evidence/Boss7-minrep-restored/original/manurangsi_minrep_degree_1807_00936v1.pdf /tmp/manurangsi-layout.txt
/usr/bin/pdftoppm -r 110 -png archives/unrelated-machines/tools/evidence/Boss7-minrep-restored/original/manurangsi_minrep_degree_1807_00936v1.pdf /tmp/manurangsi-page
```

本环境默认 `pdftoppm` 包装器缺少 `libpoppler.so.160`，实际改用 `/usr/bin/pdftoppm` 成功；不把失败命令记成已渲染。不同分辨率/Poppler 版本的 PNG 字节可能不同，原 PDF 的 SHA 才是冻结身份。

## 实际比较与检索边界

实读比较对象及其哈希见 `source-manifest.json`；临时读取记录、全仓当前 Markdown 的 357 行检索命中、冻结来源路径清单和回执在 `cleanup/workspaces/Boss7/resume-20261031-current/minrep/`。其中 `782a...` 和 `7e630...` 是完整导出的冻结 canonical/审查，另外对已归档 v2、v3、v4/v5、坐标切片反例和两篇 PCP 文献页作实质比较。没有给这些未由本子任务认领的比较来源另记 done。

当前结果树已做全仓文本检索，并按 inventory 对冻结相关路径定位。一次直接对冻结整棵树的广泛 `git grep` 未完成、已中止；不把它计为完整的冻结全文搜索。数学比较由已实际读取的精确来源承担，不声称所有 10,921 份冻结来源全文都已搜索或阅读。

另于本日打开以下 primary 页面：

- [arXiv 元数据/版本历史](https://arxiv.org/abs/1807.00936)：页面仍只列 v1，摘要仍出现旧度数平方根。
- [期刊公开条目](https://www.sciencedirect.com/science/article/abs/pii/S0020019019300043)：公开摘要把此前度数写为平方，文献为 Information Processing Letters 145 (2019), 24–29，DOI `10.1016/j.ipl.2018.08.007`。未取得/未审期刊付费全文，不声称它已修复本文指出的所有证明问题。
- [Minzer–Zheng ECCC Revision 1](https://eccc.weizmann.ac.il/report/2024/027/revision/1/download/)：只复核相关定义、主定理、§7.4 的 60–61 页；没有重读 106 页全证明。原件本地哈希已核。

第 4.3 节的尾界是本次独立推导：`c=0.3−0.2ln(2.5)>0.1`，而不是照抄原文缺少因子的二次 Chernoff 中间式。Prop8 的删边尺度必须用 `pDn`。这些修复保留主 theorem 的全部渐近参数和 0.9 合同；不保留原文无上界 γ 的错误字面域。
