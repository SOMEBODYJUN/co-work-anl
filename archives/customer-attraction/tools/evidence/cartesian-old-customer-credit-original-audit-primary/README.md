# 笛卡尔旧客户信用原始审计证据

对应[程序正文](../../../state/程序/笛卡尔完整策略与旧客户信用分离的原始有理审计--程序.md)。两件冻结主源4463B/1738B均完整实读，原字节保存在`original/`，双冻结完整提交、路径、size/SHA256/blob见`source-manifest.json`。

- `original/audit_product_credit.py`：自足标准库程序，无外部输入，无CLI或main guard；import或执行都会写同目录报告。
- `original/product_credit_independent_audit.json`：全1738B冻结报告，包含两小产品的全部回归、64人代数/同H及不同b0分布字段。
- `replay/`：本次未修改原入口唯一一次运行的execution、完整stdout/stderr和新报告。原脚本副本及运行目录在clone外；此处不再复制运行脚本，因为`original/`已有同SHA代码。
- `repository-related-search.txt`：实际全仓Markdown检索的9个命中路径，不声明这些命中都已额外逐源清洗。

本次Python3.12.14以`-I -B`、无`-O`运行，exit0、stderr空；stdout和新报告均1738B，与冻结报告逐字节一致，SHA256为`0ce2275f45c23bc86fe7a77bea4d85c356b50ba2c79de9f5b25f932343f5c1e5`。新运行与原历史输出保各自身份。

程序只枚举m2/3的完整A/B与A×B策略、全前缀剩余利润F；64人部分只核给定解析公式、同H及272差额，没有构造C策略或巨大产品目录。一般结论由正文链接的完整产品证明、C的全历史可信性和F消元承担，不把有限PASS扩成普遍half证明。
