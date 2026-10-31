# TeX preservation checker implementation evidence

`original/check_preservation.py` 是 clean source `96419c9b43c635697b7e` 的 3500 行、125543 字节实现。已用 AST 统计 70 个函数和 9 个数据类，实际 `--help` exit 0 与 `py_compile` exit 0；运行输出在 `runs/`。没有声称任意稿件 preservation、编译或渲染成功。

`source-manifest.json` 记录冻结源身份；`comparison-notes.md` 将实现和已有 TeX-safe guide、测试合同逐项分工。
