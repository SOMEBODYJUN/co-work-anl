# 十八主题真实最优覆盖范围：单源闭合

主来源1934B完整原字节与两个冻结版本在[source-manifest.json](source-manifest.json)。此前仅作related的身份保持，本次正式claim后完成源处置。

[数学正文](../../../subarchives/six-providers/state/引理/十八主题势停界的真实覆盖最优性--引理.md)给出一般势最优且无多重覆盖时的静态最优引理，并对普通点从d全为1直接证明六比较题覆盖全部客户。所有覆盖最优交换均成立，而严格倒二盈利偏离仍排除SPE。

[复用依赖](reused-dependencies.json)绑定此前已发表的原正类型输入、完整原审计程序和普通报告；原100947多重集合枚举不再执行。一次标准库[derive_scope.py](derive_scope.py)只检查输入域、精确总和、整数展开和旧报告绑定，结果为[scope-arithmetic.json](scope-arithmetic.json)。原LP、原势枚举及全SPE核验在本批均为0。重现本批算术（输出须新路径）：

```sh
python3 archives/customer-attraction/tools/evidence/full18-optimal-scope/derive_scope.py --repo . --output /tmp/full18-scope-new.json
```

这里的OPT数值证明不依赖浮点对偶，亦不把旧必要点写成六人半覆盖反例。private点和88类型重权实例没有合并。
