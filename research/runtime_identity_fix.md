# 固定身份 `boss 1` 的绑定与恢复

运行环境为 Linux、Python 3.12.14、Git 2.56.1。复现时的分支为 `work/cn-crisis`，基线提交为 `e5f3898`。

## 改动

`cncrisis/runtime.py` 的身份校验接受内部 ASCII 普通空格（U+0020），直接返回输入字符串。首位仍须为 ASCII 字母或数字，总长仍为 1 至 64 个字符。首尾空格、路径分隔符、控制字符和非 ASCII 空白均无法通过校验。`boss 1` 和 `boss1` 保持两个独立的身份号。

`tests/test_runtime.py` 新增两项测试。一项检查字符集、连续内部空格及长度边界；另一项在临时 Git 仓库绑定 `boss 1`，读取账本确认作者和相对路径，再将整个工作区复制到同分支的新临时目录。真实 CLI 在新目录以 `session next --actor 'boss 1'` 恢复默认的 `work/boss 1`，返回相同的 run_id 与周期。测试还确认用 `boss1` 打开这份账本会被拒绝。

## 执行记录

增加测试后，在尚未修复的基线上运行：

```sh
python -m unittest discover -s tests -p test_runtime.py -k spaced_actor
```

退出码 1。新测试在 `checked_actor` 抛出 `argparse.ArgumentTypeError`，结尾为 `FAILED (errors=1)`。

修复后运行：

```sh
python -m unittest discover -s tests -p test_runtime.py -v
git diff --check -- cncrisis/runtime.py tests/test_runtime.py
```

第一条命令的结果为 `Ran 9 tests in 1.458s`、`OK`，退出码 0。原有合成材料、分支变更、复核后篡改、验收路径以及未完成时的 CLI 退出码测试均通过。第二条命令无输出，退出码 0。

## 验证范围

检查了 CLI 的默认路径拼接、账本读取及 Git 仓库定位。这些步骤使用 `Path` 或独立的进程参数，测试覆盖了名称含空格的仓库目录与工作区目录。本次验证使用临时目录和测试账本，涵盖本地身份恢复。正式研究的新克隆重放、经济结论和独立复核仍需随各自的正式产物验收。
