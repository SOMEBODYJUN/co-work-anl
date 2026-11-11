# signed 标签措辞的最小更正方案

这是对 registry v2 已有标签域的实施澄清，不是扩大模型或改变 donor 成本。当前 v2 明确保重复覆盖标签；正文的“并集投影唯一读回标签”在已有 alias 时不成立。正确证明直接使用 Cartesian 标签元组和观察到的元组历史，不依赖覆盖商。

精确四项旧/新文本、旧源 SHA 和应用四项替换后的预测 SHA，见同包 `source-clarification.json`；所有替换已静态核对唯一命中，但没有写共享源。四项分别修正开头域、Cartesian 身份、首次退出的完整前缀/own-action/永久性及末尾模型链接文案。正文数学证明见 `review.md` 第五节。

受影响的当前 registry owner 包括 signed v2、M-04595ddc5e2849e08c5fe21138dc8208 v1、M-28e6e7f3210943bc961637e22c5322a8 v1；其精确 statement/model/引用 section 和旧 SHA 均在 JSON 中保留。当前 material 的源引用也须同步。全部 literal 引用文件的实际 SHA、JSON pointer、边 endpoint/evidence pins、任务当前静态状态，见 `source-reference-inventory.json`。另按 signed endpoint input pins 补查完整任务依赖：4个 done 任务 b3aa35、6b319、26d5d0、7b5d2，加本 active e15ef；后两 done 只绑定 endpoint 而没有正文 literal 路径，仍需定向修复，不能只按 literal 搜索的3个任务处理。精确路径、状态、owner、文件SHA和输入pin另保在 `source-clarification.json` 的 affected_endpoint_pinned_tasks。旧 baseline/input/batch/receipt 作为冻结历史身份保留，不能把它们一律重写成新字节。

Root 应按现行勘误/登记规范原子发布正文与受影响当前记录，再根据当前队列关系定向刷新/替代关联任务和边。本 worker 未改变 registry 或 task、未绑定新边。若源哈希或 registration pin 变化，本包独立数学保持可用，Root 在最终绑定前刷新本包 evidence SHA、input pin、ledger 和 receipt assets 即可。
