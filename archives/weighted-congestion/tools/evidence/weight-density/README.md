# 权密度来源与重放

`source-manifest.json`列3份本批来源及2份已由Boss2完成的程序/报告比较依赖，完整冻结commit/path和SHA-256；`original/`字节不改。

`replay.py`加载原始density程序，只包装`audit_game`记录全部49个实际输入，再执行原main的所有断言；新JSON、stdout、完整策略/多项式输入及与原冻结JSON的精确比较均在`replay/`。原数学/生成字段全部相同，仅base_commit运行元数据不同。程序/报告不随本批重复done。

一般实参数证明与三带历史、独立审查、有限运行的边界见[审查对象](../../../state/审查/权密度三带推导与独立审查范围--审查.md)，不是从有限样本推断真值。`related-search/`保存三个固定文本关键词的全冻结Markdown命中及实际比较行/节。
