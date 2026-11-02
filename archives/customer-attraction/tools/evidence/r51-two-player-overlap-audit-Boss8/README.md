# 两人重叠税恒等式与策略端点的精确核验

本包保存四个冻结源：`33a7ad7c1c761c51c319`、`a688a554b33bce8def2f`（背景程序/报告），`514a5475422ce77ab849`、`8790d2f2ec1c1e3501f0`（零背景根程序/报告）。

背景原程序对九个整数背景各核64个局部会员型，共576个；生成290B JSON与冻结报告逐字节一致。根程序核全部64型及三份完整策略的98项含自行动比较，生成9590B JSON亦逐字节一致。两程序均只用Python标准库。局部型不是完整博弈样本，任意背景数学由已有解析六格证明承担。

独立核验器不导入作者程序，从直接客户份额和集合收益重算，实际输出保在 independent/：

```sh
python3 independent/background/verify_json_direct.py
python3 independent/root/verify_json_from_definitions.py
```

原源码位于 background/source/、root/original/；实际原字节执行位于相应 replay/，运行会覆盖该路径的同名报告，故复用时先复制到自己的临时目录。所有原件和既存报告按原字节保全。有限回归不外推六人半覆盖。
