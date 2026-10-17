# 列表度数预算：陈述先行重构与全文读后攻击

对象：[现行正文](../../current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)，精确身份 `UM-LIST-AGREEMENT-DEGREE-BUDGET-v1`。本记录不把组合预算引理升级成源困难性或 UM 反面。

## 实际顺序

root 先在交流中给一位源研究者贪心计数构想，后冻结只含四条结论的 Exact，SHA256 `2c36eff940c9918105631b40908df15a3d5dfe334761a7bb3d7bfe26cca2f454`。另一位内部研究者未读这些交流、root 证明或其他研究者新稿，仅据该 Exact 独立重构全部四条。其原始完整稿 SHA256 `155e4fdbebac53b94e74da05ad35cd875445a1bc351d7ee63929f10fc65c9432`，原字节保存在 [source](../../../history/source/notes/unrelated_machines/list_degree_budget_independent_source.md)。这份稿自足重构 ticket 贪心、整数流、每图 private-symbol 锐性和 soundness 代数；不是只做投票。

随后该审查者才全文读 root 自写 canonical，实际 SHA256 `05be90578af3f5762f040a482d96e6aff3dc5cadb07a9c792134428bc02fff07`。读后稿 SHA256 `1b5df7e5d8912fa7aac7872695bcc0d1041de3d42537ad85ef514a11e1f64d1f`。四条无 standing fatal。其建议把末段单独引用的“满足(1)”澄清成“满足本页对象域（包括两个不同邻居和局部公共像）”，root 已采纳；审查者精确回换单句并核恢复原 hash，确认没有悄改证明。澄清稿 SHA256 `3507cbf9fbfaee0e660805742ac83b5db9a3319029b3fa2fe984f214e844896c`。

另一位先前已看 root 证明消息的研究者，仅将自己的初审记为读后审查，稿 SHA256 `22ae4eb141d99bc357218b96b8bf33259f3da1e1f94f17756836d09802af9f52`；该阶段未见锐性构造，明确不冒审。之后其真实全文读 `05be9057…`，又全文重读 `3507cbf9…`，新增核验了此前未见的 sharp 地图及全部源连接，冻结完整稿 SHA256 `a3a3e22c537dc2142848813ab7a1b0e63e548c807fe13545cdb9ecd9e5a33dc0`。其亲读官方最终版 Moshkovitz PDF 的定义、Cor4.8 和 Claim4.10；另建议把来源措辞明确为“固定素数幂右度数”，root 已采纳。这第二处仅改善文献定位，不改变本页任意整数 D≥2 的自足组合结论。

最终 canonical SHA256 `0bd6853705a06a9adf0ec550d627776ed6b6518dbc61224c33cbb5b0d66ba473`。第二名研究者随后实际核对最终稿，精确回换“素数幂”一处得到此前全文实读的3507cbf9…，确认只有这处来源措辞变动；补记SHA256 `5551517e5bdfe0c74247ac05b21126edd37d36f24028c5ad8d66ec55d1dd7fb1`，没有重写旧冻结稿。以上 scratch hash 用于固定实际审查次序；承重证明全部在现行正文和保存的独立原始稿中。

## 实际攻击项目

- 每个右点至少两个**不同**左邻居；simple 与关联容量1不能删。局部公共像不保证一个共同左赋值，证明只逐关联取原像。
- ticket 数和真实列表大小分开。一次添加可能使多个右点 agreement，不能反向把实际 agreement 数当成已支付步骤；规范证明固定已服务集 S，恰有 2|S| 张 ticket，其他 agreement 只提高结论。
- 重复原像在输出列表中去重，只减少预算；使用 ticket 保守计数不会假设原像互异。
- 二进制巨大 L 不驱动循环。贪心至多 |B| 步，流容量先截成 d；没有伪多项式展开。
- 第2项分数流 2/D 合法的两个条件是 D≥2 和 L≥ceil(2d/D)；整数流保证不同邻居，并返回实际原像列表。
- 锐性地图的私有符号按左点不同。跨邻居仅能通过0相等；每个符号 ℓ_b 只能付一个右点的关联。因此总列表预算至少2|B|，不是仅凭某个图的实验猜阈值。
- cutoff=1 的低 L 范围为空；|B|=1、L>|Σ_A| 及 d=1 没有被误当成非空反例。分数下界未宣称锐，也未宣称 sharp 地图是 hard source。
- alpha=0 在对象域内确不可能；式(4)只在 alpha>0 正数相除。两项必要条件不自动给足够 soundness 或一个源归约。
- 总 O(|B|) 标签量不能替代逐左列表；2|B| 的平凡全 agreement 构造沿用不同邻居及局部公共像前提。
- 第一名审查者未亲读外部 PDF，明确只核自足数学和条件使用。第二名研究者及 root 真实查看官方最终 PDF 相关页，不依据旧会议版猜 PGC 条件。Cor4.8 的图结构没有被默认成本文全部前提。

## 实现、核验与认证

本 Claim 没有新的生产实现或冻结有限实验。所述确定性构造和位复杂度是一般证明，非软件完成声明；root 用 Fraction 核了显示的参数代数，不把这几项数值核验当一般证明。限定证明和实际内审已闭合；外审、新颖性及独立成文价值未认证，UM-TARGET-v1 仍 OPEN。
