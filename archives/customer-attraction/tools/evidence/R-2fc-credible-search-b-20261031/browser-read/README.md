这些十个文件的原始 GitHub blob 页面在冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 逐一打开，页面的只读文本区从首字节读到末字节并由浏览器 JSON.parse。`summaries.json` 保留每一条的 inventory SHA/size、页面文本长度、完整参数、MILP 记录和 exact_candidate 全字段读数。

`clean show` 本地调用因 partial-clone promisor 的网络端点不可用而无法把 blob 物化到 shell 工作树；因此本目录不伪造 raw 副本。冻结原始字节身份仍以 `source-manifest.json` 的 inventory SHA-256/blob/size 为准，`clean-show/` 保存每次调用的原始 stdout/stderr。
