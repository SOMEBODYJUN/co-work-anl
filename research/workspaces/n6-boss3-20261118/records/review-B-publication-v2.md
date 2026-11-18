# boss3-B-review-publication-v2

**verdict: approve；evidence_level: internal-independent；仅可 local-result。** 准确 freeze_id=boss3-B-publication-v2，revision_pin=c6cd6c74ad193338d935f372da3686a6faaefff80b513b5d833988cfef16b695。

本轮为非作者 /root/review_q5 对正式发布字节的定向复核，RUN=n6-boss3-20261118。本人未参与 B 论证生成，independent=true 表示作者独立性，不冒称原 obstacle 输入隔离。完整数学已在 records/review-B-math-v1.md 核通（SHA256 a200a481db73cc9e393c2f3d5f491ce87d55ed20ff43692d0b5f4141e4ecfe75），包括原标签全历史、锚后手排除、223型/165必要行、TQ未知真实末位消元、20736→1365→69、69份独立Fraction重建矩阵/对偶。这里复用相同字节与用法，不重复数学计算。

实际适用范围只为六不交等大最大锚、q≤5的 B 类三步前缀第四位 K/2。325/632 只属四强制枝全 double-extra 必要模型；A/C、一般 q5 和原六人目标仍开放。批准只可 local-result，不可 whole-target。

## 六处准确修复

逐项核全部24条新content_refs SHA256，全吻合，共21个不同文件。新batch及artifact全文解析并结构差分，其余相同字节按实际既有审查复用。全部旧publication-v1引用也仍为原SHA。

新 B-registration-batch-v2.json SHA256=539d9f634a545714af6ad26ee5f22f2d1db2050e0c3a2a553076e3aef7cf21d5。独立深拷贝旧batch，仅将 /materials/1/disposition … /materials/6/disposition 从 objects 改 attachment，所得结构与新batch完全相等。正文 materials[0] 仍 objects；所有 owner/path/SHA/reason 均不变。六处修复分别对应verify、证书、映射、replay、发现脚本和摘要，符合IMPLEMENTATION第155行合同。旧confirmed在新revision实质解决，旧review仍绑定旧freeze。

其余batch完全不变，包括唯一 B 对象、version、proved 局部状态、statement/quantifiers/assumptions/scope/objections、body/evidence/sources。源对象pin不变。artifact仅变第一条publication_ref的新batch路径/SHA及实际line_event_id；statement、note_ref、authors、applications、局部欠账及edge引用均不变。spec_pin、packet_pins、application_refs、authors/state与旧freeze一致。

正文、六个canonical证据、edge及其条件/result/remaining均原字节。相同路径SHA逐项一致。前轮已实核的七项字节迁移、canonical BASE只读重放、sources来源字段、显式引用闭合和全部端点/证据/边指纹继续成立。新材料处置不改变源对象或数学证据。本轮无必要重跑同一69证书计算。

## 复用与适用限度

完整数学复用上述review-B-math-v1.md；publication-v1.md中对新正式路径、来源字段、B-only conditional contribution、全部显式引用和原target仍open的实际窄核也复用（准确SHA见末表）。不是凭作者/Main自信通过，而以字节不变和逐字段精确差分为依据。

remaining仍保A/C及原题其它目录；没有whole-target、target discharge或隐含一般q5闭合。允许发布的是 B 局部定理和保remaining的条件贡献边。325/632不升级为一般B下界。所有旧问题已在新revision解决，没有新增confirmed或unresolved；数学改动、证据漏移、端点失效或目标remaining丢失疑点均not-real。

## 实物与反馈

records/review-B-publication-v2/repair_audit.py及repair-audit-results.json保存六个准确JSON差分、24条哈希、旧freeze不变、artifact仅有路由/真实事件改变及源pin复算。复现：

```sh
python research/workspaces/n6-boss3-20261118/records/review-B-publication-v2/repair_audit.py
```

没有求解器或数学重跑，没有修改作者文件、Git或studio mutation。完整结论与准确文件交回Main和作者，供Main串行登记，不声称已经注册或远端发布。

## 精确文件哈希

| 文件 | SHA256 |
|---|---|
| `research/runs/n6-boss3-20261118/studio/artifact-notes/1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b.md` | `1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b` |
| `research/workspaces/n6-boss3-20261118/records/B-registration-batch-v2.json` | `539d9f634a545714af6ad26ee5f22f2d1db2050e0c3a2a553076e3aef7cf21d5` |
| `map/edges/n6-boss3-20261118/B-prefix-half-contribution.json` | `53f6da8f1ad6c27f3753613e94dd03266c0644b420ba469caec5924fbdac8242` |
| `research/runs/n6-boss3-20261118/studio/artifacts/SIX-FIVE-EXTRAS-B-PREFIX/a05d2f11c77bc03d155711fa162deea5ee2a6a03828f25bda7615a9edaf0b228.json` | `ae9c535b977b58e912cec81256c8cbd9e35c13f0c4fe827afadf6f017368ed89` |
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
| `research/workspaces/n6-boss3-20261118/records/review-B-publication-v1.md` | `8639d0dff9e38fce62421dabe3fcc2858e07a8c68b4d8c868861db49ac304bca` |
| `research/workspaces/n6-boss3-20261118/records/review-B-publication-v2/repair-audit-results.json` | `6d1e4247e9193362834030a563786d1b293bba96065dec288d8261c3f89f4726` |
| `research/workspaces/n6-boss3-20261118/records/review-B-publication-v2/repair_audit.py` | `30048e10c21a7b8067c68f1856f751350001f77aece22ed627dd3348e886a40f` |
