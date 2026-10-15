# 分支收口记录与后续规则

当前远端仅保留 main 与 wcg/board。所有观察到的旧工作分支和教学/旧研究分支已经完成分类或核对其被现行稿取代，原提交保留为 main 可达祖先。主整合先推送并重新核对，再使用原 tip 的原子 compare-and-delete 删除；没有对 main 或公屏强推。

| 原分支 | 整理时冻结 tip | 实际处置 |
| --- | --- | --- |
| `main` | `bd7798d5bbcc8086217ff54d7f91b445d0374b4f` | 保留：共同研究状态 |
| `research/assault-c` | `3e1982dc694b038a2342ab5dad285b643ddac765` | 已删除：内容已分类，原提交可从 main 恢复 |
| `teaching/final-20261010` | `946149cec13a7ee63ec20216704f08492c4e9743` | 已删除：内容已分类，原提交可从 main 恢复 |
| `teaching/readability-20261007` | `31d1f1a4f40def3fe60ae96a6aa29ba0a31793cf` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/board` | `23aec896b8af834d554478f98d4393e70f70cb78` | 保留：旧消息已清空，成果已入 main |
| `wcg/work/R1/06d07d4f2a` | `ba6fb27b6b5e1d5b00fe6fbb40178f1b5e334194` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R1/2c7ed05d02` | `6a4ea46b6d57c252ac5c6b8e1660fb04ae9fccfd` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R1/4bd11822f7` | `9f02c1acb95cc1d1242d145a34551c6f31da2a59` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R1/8075536cdd` | `809b032207ea7a4c03e87a70fa470572cdcce7d9` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R1/9555b45dd3` | `de6055a977d48da760dd49177d9b4aa4fb33b4d1` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R1/e18ff3b3e4` | `a3f0c7aa977a6e2036df08afb7b66225cf372d42` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R1/e9ca869c94` | `6e13c941dde9b6f00e1cae2dabca712e17f2b2a4` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R2/286b1a78fb` | `90ec22d9d61a80b51a0d63a52a4e18e6916b752a` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R2/a9515ff55c` | `d0724ef2d5626d22a5dddb255afb537399d9343d` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R3/6679ad71f7` | `6cb5255e4b088f90368dbf04cb04a048131917c9` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R3/810ea60147` | `3ae52dbdc1ecebc19580e4d2e01e9f541ee9bea8` | 已删除：内容已分类，原提交可从 main 恢复 |
| `wcg/work/R3/d940dc9710` | `d6ec59dceae9b9b71a033c3ba8d9f038d90516db` | 已删除：内容已分类，原提交可从 main 恢复 |

原始逐文件/hash 和保留/退役决定见 [INTEGRATION](weighted_congestion_frontier/INTEGRATION.json)。删除分支名不等于删除数学来源；新对话只需读现行地图和按问题选择正文。临时分支仅在明确需要时创建，默认启动与 checkpoint 都使用 main。
