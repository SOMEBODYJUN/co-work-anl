# Boss6 本地交接（2026-10-31）

## 原因

启动时公开只读 clone 和结果分支同步成功；带凭据的身份登记/receive-pack 写端点被自动审查拒绝，回执为 `write-blocked`。按规约停止同凭据重试，不把本地 checkpoint 或认领写成远端 `pushed`/`done`。

## 本地已完成

- 六个既有 Boss6 文献认领已全文实读并写出自足对象草稿：Cheng–Mao、Davies–Rothvoss–Zhang、Ebenlendr–Krčál–Sgall PDF、Ebenlendr–Krčál–Sgall PS、Jansen–Maack–Solis-Oba、Jansen–Rohwedder。PS 与 PDF 的提取文本逐字节相同，PS 建议 `duplicate` 指向 PDF 对象。
- `CLAIMS.md` 全 3,702 行/320 段/306 个唯一身份已逐段复核；255 个身份在当前树有对象、历史或证据命中，51 个身份没有可定位去向，源仍 `needs-decision`。
- `FAILED_ROUTES.md` 全 531 行/66 个有内容段落已逐段复核；建议 `retained`。旧链接 108 条中 40 条当前可定位，68 条迁移路径缺落点，未伪造证据。
- 另有 10 个未认领源仅作本地预读和比较，全部明确记录为 provisional，不能计完成：两份 arbitrary-sink price-cover 审查、三份 Boss11 tiny-home 版本、两份 uniform sparse-support 版本、一个 weighted-group 版本及一个 nonpool committer statement。

## 本地 checkpoint

- `c4acc99953075df273c69fbce739c780af740e2b`：五个新增文献对象、入口状态修订、两份账本副本、审查日志、预读日志和待登记回执。
- `b9811e80cce40235e2a4b485d10a45c796bf171b`：修复 Jansen–Rohwedder 对象中的 LaTeX 转义。
- `8c3894bddb34fd3859c051752bda18fce934aad4`：未定位 Claim 身份清单。

这些提交均为 `--local-only`，未推送到 GitHub。原始 PDF/PS/TXT 导出仍保存在本地工作区的各 agent 目录，未混入 checkpoint，便于后续按需要重读。

## 继续入口

远端恢复有效写授权后，应先 `sync`，复核六个既有认领的最新状态，再把正文 checkpoint 推送成功后逐源提交对应 receipt；Eben PS 登记为 `duplicate`，两份账本按上述状态分别登记。10 个 provisional 源须先正式 claim，不能直接沿用本地比较结果。51 个未定位 Claim 需逐一决定保留、重复、退役或建立对象，不能批量标记完成。
