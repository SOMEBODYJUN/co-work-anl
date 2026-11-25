# 代表性排版预览的实际状态

作者：/root/ra09_rebuild。

已用 Pandoc 将当前学习稿转换为包含本地 MathML 的 `study-preview.html`，转换输出没有数学转换警告。蓝色 info callout 的每一行仍由源 Markdown 的 `>` 表达；预览仅对普通 HTML blockquote 施加蓝色样式，不改变交付正文。

实际截图尝试未成功，不能记为已看渲染：

1. 首次 Chromium 启动返回 `ENOENT: no such file or directory, mkdtemp '/tmp/playwright-artifacts-…'`。
2. 将临时目录设为本任务 `qa/tmp` 后重试，启动返回 `socket() failed: Operation not permitted (1)`，随后浏览器关闭。没有截图产物。

因此本作者只报告转换成功、公式静态语法检查及正文人工核对，不报告代表性渲染已视觉通过。需要在可用的独立预览环境实际查看 M001 长证明、四组合表格和示性函数 cases 公式。该限制不改变原件全页与六区已经实际查看的事实。
