# boss3-B-review-publication-v1

**verdict: changes-required；evidence_level: internal-independent。** 准确 freeze_id=boss3-B-publication-v1，revision_pin=a3b9567feaa1db69ce19e39e47d13dc444742dca41dff06821a72ca3d2dea56c。

本轮为非作者 /root/review_q5 对正式发布字节的定向复核，RUN=n6-boss3-20261118。本人未参与 B 论证生成，independent=true 表示作者独立性，不冒称原 obstacle 输入隔离。完整数学已在 records/review-B-math-v1.md 核通（SHA256 a200a481db73cc9e393c2f3d5f491ce87d55ed20ff43692d0b5f4141e4ecfe75），包括原标签全历史、锚后手排除、223型/165必要行、TQ未知真实末位消元、20736→1365→69、69份独立Fraction重建矩阵/对偶。这里复用相同字节与用法，不重复数学计算。

实际适用范围只为六不交等大最大锚、q≤5的 B 类三步前缀第四位 K/2。325/632 只属四强制枝全 double-extra 必要模型；A/C、一般 q5 和原六人目标仍开放。批准只可 local-result，不可 whole-target。

## confirmed：六份附件处置错误

research/IMPLEMENTATION.md 第155行明确要求“正文用objects，必要附件用attachment并归相应对象”。冻结 B-registration-batch.json 的 materials[1]…materials[6]（verify脚本、证书、映射、重放、发现脚本、发现摘要）全为 disposition=objects，应为 attachment；正文 materials[0] 应保持 objects。六附件的数学 owner 正确，程序实现兼容接受 objects 所属 evidence；因此这是发布元数据合同不符，不是数学、程序执行或哈希错误。最小修复仅六处 disposition，再另存新 batch/artifact/freeze，不改本旧冻结。

已将准确位置、影响和最小修复真实送达 Main 与作者，双方确认，Main 另建 v2。旧 v1 的 changes-required 继续绑定旧字节，B 数学 approve 不撤销。

## 其它范围核通

全部24条 frozen content_refs 的原始字节 SHA256 逐项吻合，共21个不同文件。新 batch、edge、artifact、六人问题容器全文实读；同字节正文、所有证据和前提复用实际已完成审读，并重核准确哈希。

正式正文与受审完整证明逐字节一致；六个 canonical 附件也逐字节等于受审数学实物。正式 verifier 的 BASE 实际为 tools/evidence/six-five-extra-B-prefix，直接只读调用 verify() 从新路径读取全部69证书与1365映射，输出与冻结 replay 完全相等。未运行会写作者 JSON 的 __main__，没有重做发现器或独立矩阵。

batch 只登记一个局部 theorem，proved 状态及 statement/quantifiers/assumptions/scope/objections 与已核 B 命题一致。sources 为合法来源追溯字符串，准确指实际作者/RUN/正式旧来源；其字节依据另由 body/evidence 付款，没有用 sources 文本代替证据。

edge 的唯一 source 是 B 对象，target 为原六人问题；premises_mode=all，relation_mode=conditional，完整保六锚/q≤5/原历史/真实后继结构条件。contribution.result 只为 B 的第四位 K/2，remaining 明确保 A/C 及无六锚、更多额外等其它原题目录。无 whole_result，无互斥枝福利相加，无325/632越界。原 target 仍 open。

独立重算 source/target endpoint_pins、evidence_pins、review_digest 均吻合；batch、edge、artifact、原target对象全部显式path/SHA引用均在本freeze内闭合。正式模型、四额外定理、末两位定理及计数引理全部在freeze中；两个 idea 稿未迁入，但正式正文已自足重述所采用的解析/TQ接口，历史有限案例不承重，未形成遗漏依赖。A/B/C reduction-v2 的精确文件与section亦在freeze，仍为条件接口。局部artifact的空欠账不删除edge中的目标remaining。

作者 reviewed_by/review_note 清楚标为作者实读声明，不冒称提前完成非作者审核。除六附件字段外，引用缺失/元数据范围越界/迁移破坏等疑点为 not-real，无其它 unresolved。

## 实物

records/review-B-publication-v1/publication_audit.py 保存全部24哈希、七项字节迁移、引用闭合、指纹复算、六处confirmed及canonical只读重放；结果 publication-audit-results.json，完整重放另存canonical-readonly-replay.json。复现：

```sh
python research/workspaces/n6-boss3-20261118/records/review-B-publication-v1/publication_audit.py
```

未改作者冻结文件，未Git或studio mutation。本报告仅供Main串行登记，不声称已发布。

## 精确文件哈希

| 文件 | SHA256 |
|---|---|
| `research/runs/n6-boss3-20261118/studio/artifact-notes/1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b.md` | `1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b` |
| `research/workspaces/n6-boss3-20261118/records/B-registration-batch.json` | `b824adf45bc574988c0e252d7385fc637c7081aa02c3bb34733c4f2d56a49a35` |
| `map/edges/n6-boss3-20261118/B-prefix-half-contribution.json` | `53f6da8f1ad6c27f3753613e94dd03266c0644b420ba469caec5924fbdac8242` |
| `research/runs/n6-boss3-20261118/studio/artifacts/SIX-FIVE-EXTRAS-B-PREFIX/9989c35fc8f3b4b20a4d98c1cb23f50efd787fcb61c7979fc1166fa39ed4406b.json` | `55e0a3e135e2083a20adea89d6d000b0ba46c47505043fdbddd1fbc6fba40f6c` |
| `research/workspaces/n6-boss3-20261118/spec.json` | `5d45871b81dff68042f35c8faef132e224c4bea6bab14b9db5a00b4e6a6f8dc3` |
| `research/runs/n6-boss3-20261118/packet-full.json` | `62bcd3ed08e4d455673e98f5834789121a915adaf0d5881f14f86f1fdfff149b` |
| `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md` | `0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `research/runs/n6-boss3-20261118/packet-obstacle.json` | `109c9f8ef683db0814d99e72a6bddd6df7def51438ffc8521f4b3f76ef10278b` |
| `archives/customer-attraction/subarchives/six-providers/state/定理/六不交最大锚与五额外目录的B类前缀--定理.md` | `1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b` |
| `tools/evidence/six-five-extra-B-prefix/verify_B_all_orbits.py` | `8cfd37578233a67ff55db43b2700f0c092a2ddf7927be5d00ae53cd666a8ca27` |
| `tools/evidence/six-five-extra-B-prefix/B-all-orbit-rational-certificates.json` | `47a1e8b2a792b31fc2ddca384a8b75ef10dec54d6695aafe320c8203f80db1b9` |
| `tools/evidence/six-five-extra-B-prefix/B-1365-to-69-orbit-map.json` | `f326dbcebf8b18688dfd4a71b76d294568d7cb5936d99f91935ac9bd0ecf976c` |
| `tools/evidence/six-five-extra-B-prefix/B-all-orbit-exact-replay.json` | `3ed6a868cb9ef45d99ade8d0143b2bbeb18ffb3f2ea3953c6655062247ee28f6` |
| `tools/evidence/six-five-extra-B-prefix/certify_B_all_orbits.py` | `9cf85d342a683438db132b31dd485f5e4f114f02f73188c067484ba15f0829ac` |
| `tools/evidence/six-five-extra-B-prefix/B-all-orbit-discovery-summary.json` | `14b2b3e5501c56766c18a2cb68938fcfc04f45ee06d8785cf19948c3ac08ad7a` |
| `archives/customer-attraction/state/定理/六不交最大锚与四种额外覆盖--定理.md` | `e38f88c49cd7475cc8fdb84bd6885b349e4913d0d970bd25273ef91ff7a0b969` |
| `archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md` | `204030503c37b18f8d26ce664b9cb99afc688fed77c8221a00cf0d8d7b21b34b` |
| `archives/customer-attraction/state/引理/末位最坏背景值与目录计数界--引理.md` | `6263b3d935b1c2d3d7ae6aee4016ae78cb369de1f28ddb284e8202fd21b69c3d` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-prefix-reduction-v2.md` | `bf78bb43f183698f3d5db02582f1a576c8b78fb3da8058ad4cc2d3eed606127c` |
| `archives/customer-attraction/subarchives/six-providers/问题--问题.md` | `21391fbaaa2893fef7b228a345fcf1d7f5c5d1dc8a42cc642d6bfbbeccc7c065` |
| `research/workspaces/n6-boss3-20261118/records/review-B-math-v1.md` | `a200a481db73cc9e393c2f3d5f491ce87d55ed20ff43692d0b5f4141e4ecfe75` |
| `research/workspaces/n6-boss3-20261118/records/review-B-publication-v1/canonical-readonly-replay.json` | `3ed6a868cb9ef45d99ade8d0143b2bbeb18ffb3f2ea3953c6655062247ee28f6` |
| `research/workspaces/n6-boss3-20261118/records/review-B-publication-v1/publication-audit-results.json` | `8057acdcb9f4c624b4ff48cfff667df390bf40417c90e98e0a9de1677b5d1d29` |
| `research/workspaces/n6-boss3-20261118/records/review-B-publication-v1/publication_audit.py` | `fee958bec79aa11d51001c96df6d42479b8e79551f13f52b36b70e5713307e7d` |
