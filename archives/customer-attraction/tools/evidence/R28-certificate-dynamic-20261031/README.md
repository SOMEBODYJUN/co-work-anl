# R-28 certificate/dynamic audit evidence

本目录对应正文 `archives/customer-attraction/state/审查/R28空稀释、加入冲突与UTP有限审计--审查.md`，覆盖 clean IDs `6428425c5f2d179bda44`、`e7b636c58363075d0597`、`25623d0276ff9bcce131`、`39d94cf8fbd2c99e909f`、`dcca41f3ea1230dad37a`、`5209aad2ad96dc0ebe89`、`3bd18bf79f9166429ee3`、`da14edc75259534416f5`、`6db6fa7471aaa2e1a0ed`、`67bcd1e5d345605fc7e0`、`517b02cd2eea8b5358c3`、`a62b7a378ecbc3ea24f7`、`a541fe42e26e2f0969cb`、`be13357485a38d6a56f5`、`78639434fb10c28feb7f`、`c28a144021f51fbc1dba`、`2ee6853fcb25f83330d5`、`d79cafeaf057f5b0fd67`、`922e5ec827e40811b409`、`d3619a01f7340af36965`。

## 实读与可复现边界

- 旧三十四客户空稀释脚本和 JSON：57 个历史、342 个非自身偏离、21 个端点（19 distinct），`all_checks_passed=true`；是指定旧证书的定义级复核，不是一般结论。
- 端点混合：9 个有限诊断，代表 gap `-0.7`、`-0.6704545` 等，未得到正分离。
- directed private-parking：48 行，全部 gap<0，范围约 `[-3.60194,-1.05022]`；仅浮点参数诊断。
- UTP：`p=5,m=5,seed=2026102321,checked=600,positive=false`。
- join verifier：singleton 14/6（full/Markov），generic anonymous 7/3；join payoff vectors `(1/2,1)`、`(1,1/2)`。
- graph conflict：`p=5,target=[0,2,4],checked=10,root=4,second=2,last=0,root_floor=0`。
- blind tail：7 客户、13 个历史，实际 `CCA`，福利 7，严格有理偏离表见 run output。
- reply cycle：7 客户 39 个比较，最小 slack 0，cycle difference `-1/6`；旧 34 客户对照 cycle difference `-2`。
- theta：三份预选证书全部 violation count 0；没有随机或扩展样本。

`runs/` 保存实际执行的四个自包含探针 stdout/stderr：`blind_tail_cycle_audit`、`verify_join_conflict`、`graph_conflict_probe`、`audit_reply_cycles`。其余 JSON 是通过 `clean show` 全文读取并与同一 R-28 工作台及相关旧页比较后的冻结输出。含旧路径、`customer_attraction` 或示例模块依赖的脚本未在当前 clone 伪造重跑。

`source-manifest.json` 是 inventory 中 20 个源的稳定 ID、路径和 sha256 快照；`comparison-notes.md` 记录唯一内容去向、重复/障碍处置和第三阶段接续关系。
