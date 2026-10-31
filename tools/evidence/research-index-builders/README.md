# 旧研究索引程序的实际依赖与有限证据

三主源全部代码及模板全文读；JSON只按真实字段/记录/引用结构核，不自动审读所链数学。原件不改写。新检查只在本证据副本运行一次，原程序和旧suite均未运行。

## 主源

| ID | 路径 | 字节 | SHA-256 |
| --- | --- | ---: | --- |
| `3c77f5d856d06d7dcff2` | [research/build_crosswalk.py](original/research/build_crosswalk.py) | 6355 | `6cd25f45abd9faa0c5d3fd06e819643b71e19fea6a756915a261cce37c32d355` |
| `a8447f8474582ae3d971` | [research/build_map.py](original/research/build_map.py) | 14336 | `160da0e86b53aba6e8f731f37c149a4850c51c921a2398ab7ce4a3a7c4339fbc` |
| `2f6fe35ae6ddbac5dbca` | [research/check_assets.py](original/research/check_assets.py) | 10213 | `b91499b187578b43d5f1c832ed7179974140f485ff70fa50720350f17d16d4cf` |

两源版本定位均在[source-manifest.json](source-manifest.json)；原commit/path/SHA绑定不变。

## 真实旁读输入

[related-manifest.json](related-manifest.json)给所有54份旁读实际来源、字节和SHA；其中33学习MD用于真实链接输入和与前批已读语义比较，不额外done。三个依赖程序完整源码已读，只用于明确主检查器合同。冻结清单10885项不冒作全旧树已物化。

| 真实输入 | 字节 | SHA-256 |
| --- | ---: | --- |
| [learning/manifest.json](related/learning/manifest.json) | 12962 | `0d775a3d0d22823d2962d95adfebdaf2589e6b20d8601759ef65899080e41e72` |
| [research/catalog.json](related/research/catalog.json) | 1236965 | `b22bc7bfe560e3be434682dc262b5b7e29de7b2c4ce33d0cbc1a9320f444a24c` |
| [research/source_crosswalk.json](related/research/source_crosswalk.json) | 395476 | `f6017cabf428a34e8e79ebe5e15fd5c04f5d81ad9b64ff29ffd7bba7c680ca02` |
| [research/active_research.json](related/research/active_research.json) | 4601 | `cb52c2d1d43699ff4ad1c79ca17c9e0b6de7146b810005df83a9d7b8ba571af6` |
| [research/check_wc_assets.py](related/research/check_wc_assets.py) | 3453 | `fb7746a368f6063997a91c29f9f98b09371a847c305a07f06723ebd2ee330fb0` |
| [research/path_migration.json](related/research/path_migration.json) | 7217 | `2dbcc3539d2e1e1f007babe7fad281a4ed2c444fa19f86c48de7cc6cb5cf53c8` |
| [research/check_active_research.py](related/research/check_active_research.py) | 5961 | `2b38761ce4a292d024c6357644e9f15d4c9def7cb723c8aa87507bca885e057b` |
| [research/source_crosswalk.md](related/research/source_crosswalk.md) | 457647 | `fc234ebf594f13473662266557a31835c00f916d7adfedf8a314050c0dce6f68` |
| [research/index.html](related/research/index.html) | 1530181 | `012dbe9594c8c83f0f96948d0088496dbd9957e2fe46f03d2219b439ab09be11` |
| [research/README.md](related/research/README.md) | 2924 | `568b37c53e0915f88ad4b8e951fcd7a848f169898219b2a351a1b1b96283ae44` |
| [research/review_status.json](related/research/review_status.json) | 320527 | `3d98af571ab7b2115a22320187651c768eccbe8e75a52735b6d7f3968351b4b8` |
| [research/assets.json](related/research/assets.json) | 773683 | `7fe6d17b1fc477e76b1d63ac36251de728aca55e73402c73af14372a1f29233a` |
| [research/build_catalog.py](related/research/build_catalog.py) | 13050 | `e8bd7c89abaf263aec5898a63a13f2aff76175e13cf784a3e6cbb37e5a270040` |
| [research/graph.json](related/research/graph.json) | 1794179 | `8d42c15f2c01dcd35ed5d0725b3e42d2e85bcdc194e6454f285da1c9bb0450f4` |
| [research/current/claims.md](related/research/current/claims.md) | 385407 | `dd25571aac7cd4fc71a8a2e3ffaa7f5638ba90619c4e4ccacf7774a28bef0b81` |
| [research/weighted_congestion_frontier/INTEGRATION.json](related/research/weighted_congestion_frontier/INTEGRATION.json) | 194010 | `e9f9ce109aa070f105199bf62764c7688eb7d69dbe148d2c349ccc3386dda7d1` |
| [history/research_operations/customer_attraction_transition/manifest.json](related/history/research_operations/customer_attraction_transition/manifest.json) | 11220 | `8a284aae93cd14c277b9d7c94e14164c95209a65756bd435dc947effba90addf` |
| [evidence/runs/2026-10-01/on_path_chord.json](related/evidence/runs/2026-10-01/on_path_chord.json) | 1757 | `851dfff804dbeeb50b4649414446a8ccbddf805d976c5f9f8126fd2d21c1068f` |
| [evidence/runs/2026-10-01/sharp_lower_rational.json](related/evidence/runs/2026-10-01/sharp_lower_rational.json) | 1407 | `1d34cc1e17375233ae5e2c466268e7b5c00d7eb58950e3613532b0dac321d50d` |
| [evidence/runs/2026-10-01/sparse_bad_long_cycles.json](related/evidence/runs/2026-10-01/sparse_bad_long_cycles.json) | 2674 | `4b34dd94c35bbbc714f73dbfa0f6c3602da1e4a81f3c99cb664048a96fa5bcac` |
| [evidence/runs/2026-10-01/sparse_high_reach.json](related/evidence/runs/2026-10-01/sparse_high_reach.json) | 2245 | `8b7580e72f207bd5eb9735604ff258c63028a1fcf4107397135fdb31954fe48a` |

## 新增有限检查

- [inspect_inputs.py](inspect_inputs.py)：新代码，不导入或调用冻结程序。
- [execution-record.json](execution-record.json)：实际一次成功run的范围、结果与未执行项目；早先一次草稿分析语法错误亦准确注明。
- [json-field-census.json](json-field-census.json)：14实际JSON的每字段类型/计数、顺序叶值digest与输入SHA。
- [reference-census.json](reference-census.json)：15535次引用、2754唯一路径的逐条冻结元数据比对；不等于这些文件的全文已读或全部物化。
- [input-structural-audit.json](input-structural-audit.json)：1153/1353旧图、640行前缀登记、标题后遗漏候选、680行解释表、351资产/2099目录/273链接/四运行元数据、静态HTML精确字节绑定。
- [frozen-path-index.json](frozen-path-index.json)：冻结68fa提交10885文件的inventory定位与SHA，不是旧动态Git工作树。

## 当前版本比较

[comparison-manifest.json](comparison-manifest.json)绑定实际当前AGENTS/cleanup/OBJECTS/map/PROGRAM_CHECK及已done导航资源的读取时副本。当前允许孤立、明确共同条件和实际关系审读；旧强制连通和claim入边不继承。原JSON中的旧主攻/角色/授权文字均只是历史输入。

没有当前原suite PASS、浏览器交互/视觉PASS、外审或数学证明认证。五项输入/证书hash只与冻结清单元数据相等，代码source_sha256原检查只非空。所有领域数学仍按对应源实际读审。
