# 四份冻结完整证书的无损结构阅读视图

本视图来自父方正式导出的实际冻结JSON：读取全部字段和每一条history/action，再将完全相同的有序子树合并。没有执行原程序、BI、收益回放、LP或新参数测试。

每类保当前行动及全部p个有序孩子；孩子按动作标签0至p−1排列，`[重复次数,子类ID]`逐段展开，−1为长度m终局。类的“出现次数”是完整有序树中的前缀数。根类递归展开可还原每个历史动作，再按history字典序排回源actions；其余字段全部原值和源键序也列出。恢复后以原indent=2序列化，要求与实际源JSON逐字相等，而不只相同摘要或节点数。

## m=2：aaec1d5779f9c9eda520

冻结路径：`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_m2_certificate.json`。原件816B，SHA256 `160781210be362dc9fd936160b956453942a5a8a3232adee9f54b64500955ffd`；Git blob也吻合。现有唯一gzip解压与源逐字相同。

源顶层键顺序：`scope,m,p,unit_customer_interests,actions,path,W,OPT,root_payoff,root_deviations`。除actions以外全部字段如下：

```json
{
  "scope": "Complete pure SPE from a root-defective old policy; all ordered histories and legal tuple deviations audited.",
  "m": 2,
  "p": 4,
  "unit_customer_interests": [
    [
      2,
      3
    ],
    [
      2,
      3
    ],
    [
      0,
      2
    ],
    [
      0,
      2
    ],
    [
      1,
      3
    ]
  ],
  "path": [
    0,
    3
  ],
  "W": 5,
  "OPT": 5,
  "root_payoff": "2",
  "root_deviations": [
    "2",
    "1",
    "2",
    "2"
  ]
}
```

actions共5条，根类2；完整无损子树表：

| 类ID | 当前联合行动 | 有序孩子的[次数,类ID]段 | 出现次数 |
|---:|---:|---|---:|
| 0 | 3 | `[[4,-1]]` | 1 |
| 1 | 2 | `[[4,-1]]` | 3 |
| 2 | 0 | `[[1,0],[3,1]]` | 1 |

已从上表展开全部5条actions并恢复源全部字段、键序和缩进，JSON重建逐字同原件：true。

## m=3：9e820a8fb167b7b484fb

冻结路径：`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_m3_certificate.json`。原件3976B，SHA256 `c938107103c62fc8014462d5e8c1595df162f07e3a951e50504ffb57ffd14606`；Git blob也吻合。现有唯一gzip解压与源逐字相同。

源顶层键顺序：`scope,m,p,unit_customer_interests,actions,path,W,OPT,root_payoff,root_deviations`。除actions以外全部字段如下：

```json
{
  "scope": "Complete pure SPE from a root-defective old policy; all ordered histories and legal tuple deviations audited.",
  "m": 3,
  "p": 6,
  "unit_customer_interests": [
    [
      3,
      4,
      5
    ],
    [
      3,
      4,
      5
    ],
    [
      3,
      4,
      5
    ],
    [
      0,
      3
    ],
    [
      0,
      3
    ],
    [
      1,
      4
    ],
    [
      1,
      4
    ],
    [
      2,
      5
    ]
  ],
  "path": [
    0,
    4,
    4
  ],
  "W": 7,
  "OPT": 8,
  "root_payoff": "2",
  "root_deviations": [
    "2",
    "1",
    "1",
    "2",
    "2",
    "2"
  ]
}
```

actions共43条，根类5；完整无损子树表：

| 类ID | 当前联合行动 | 有序孩子的[次数,类ID]段 | 出现次数 |
|---:|---:|---|---:|
| 0 | 4 | `[[6,-1]]` | 20 |
| 1 | 4 | `[[6,0]]` | 1 |
| 2 | 3 | `[[6,-1]]` | 16 |
| 3 | 3 | `[[1,0],[2,2],[1,0],[2,2]]` | 4 |
| 4 | 3 | `[[6,0]]` | 1 |
| 5 | 0 | `[[1,1],[2,3],[1,4],[2,3]]` | 1 |

已从上表展开全部43条actions并恢复源全部字段、键序和缩进，JSON重建逐字同原件：true。

## m=4：93f2d4e154c8ea2fe94c

冻结路径：`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_m4_certificate.json`。原件53107B，SHA256 `702e51f323213866c1f4d74f4bd37633ca05fbbcebff05db84e49ec6a93e3cec`；Git blob也吻合。现有唯一gzip解压与源逐字相同。

源顶层键顺序：`scope,m,p,unit_customer_interests,actions,path,W,OPT,root_payoff,root_deviations`。除actions以外全部字段如下：

```json
{
  "scope": "Complete pure SPE from a root-defective old policy; all ordered histories and legal tuple deviations audited.",
  "m": 4,
  "p": 8,
  "unit_customer_interests": [
    [
      4,
      5,
      6,
      7
    ],
    [
      4,
      5,
      6,
      7
    ],
    [
      4,
      5,
      6,
      7
    ],
    [
      4,
      5,
      6,
      7
    ],
    [
      0,
      4
    ],
    [
      0,
      4
    ],
    [
      1,
      5
    ],
    [
      1,
      5
    ],
    [
      1,
      5
    ],
    [
      2,
      6
    ],
    [
      3,
      7
    ]
  ],
  "path": [
    0,
    5,
    5,
    5
  ],
  "W": 9,
  "OPT": 11,
  "root_payoff": "2",
  "root_deviations": [
    "2",
    "1",
    "1",
    "1",
    "2",
    "2",
    "2",
    "2"
  ]
}
```

actions共585条，根类9；完整无损子树表：

| 类ID | 当前联合行动 | 有序孩子的[次数,类ID]段 | 出现次数 |
|---:|---:|---|---:|
| 0 | 5 | `[[8,-1]]` | 360 |
| 1 | 5 | `[[8,0]]` | 28 |
| 2 | 5 | `[[8,1]]` | 1 |
| 3 | 4 | `[[8,-1]]` | 152 |
| 4 | 4 | `[[1,0],[3,3],[1,0],[3,3]]` | 20 |
| 5 | 4 | `[[1,1],[3,4],[1,1],[3,4]]` | 2 |
| 6 | 5 | `[[1,0],[1,3],[3,0],[1,3],[2,0]]` | 16 |
| 7 | 4 | `[[1,1],[1,4],[2,6],[1,1],[1,4],[2,6]]` | 4 |
| 8 | 4 | `[[8,1]]` | 1 |
| 9 | 0 | `[[1,2],[1,5],[2,7],[1,8],[1,5],[2,7]]` | 1 |

已从上表展开全部585条actions并恢复源全部字段、键序和缩进，JSON重建逐字同原件：true。

## m=5：24f121d985425a6daf3c

冻结路径：`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_m5_certificate.json`。原件1120713B，SHA256 `308cc9062dd3cd644eab5edf1f4a8d0fc8369d9a617512b91edb035f51669e6a`；Git blob也吻合。现有唯一gzip解压与源逐字相同。

源顶层键顺序：`scope,m,p,unit_customer_interests,actions,path,W,OPT,root_payoff,root_deviations`。除actions以外全部字段如下：

```json
{
  "scope": "Complete pure SPE from a root-defective old policy; all ordered histories and legal tuple deviations audited.",
  "m": 5,
  "p": 10,
  "unit_customer_interests": [
    [
      5,
      6,
      7,
      8,
      9
    ],
    [
      5,
      6,
      7,
      8,
      9
    ],
    [
      5,
      6,
      7,
      8,
      9
    ],
    [
      5,
      6,
      7,
      8,
      9
    ],
    [
      5,
      6,
      7,
      8,
      9
    ],
    [
      0,
      5
    ],
    [
      0,
      5
    ],
    [
      1,
      6
    ],
    [
      1,
      6
    ],
    [
      1,
      6
    ],
    [
      1,
      6
    ],
    [
      2,
      7
    ],
    [
      3,
      8
    ],
    [
      4,
      9
    ]
  ],
  "path": [
    0,
    6,
    6,
    6,
    6
  ],
  "W": 11,
  "OPT": 14,
  "root_payoff": "2",
  "root_deviations": [
    "2",
    "1",
    "1",
    "1",
    "1",
    "2",
    "2",
    "2",
    "2",
    "2"
  ]
}
```

actions共11111条，根类12；完整无损子树表：

| 类ID | 当前联合行动 | 有序孩子的[次数,类ID]段 | 出现次数 |
|---:|---:|---|---:|
| 0 | 6 | `[[10,-1]]` | 7200 |
| 1 | 6 | `[[10,0]]` | 488 |
| 2 | 6 | `[[10,1]]` | 36 |
| 3 | 6 | `[[10,2]]` | 1 |
| 4 | 5 | `[[10,-1]]` | 2800 |
| 5 | 5 | `[[1,0],[4,4],[1,0],[4,4]]` | 296 |
| 6 | 5 | `[[1,1],[4,5],[1,1],[4,5]]` | 28 |
| 7 | 5 | `[[1,2],[4,6],[1,2],[4,6]]` | 2 |
| 8 | 6 | `[[1,0],[1,4],[4,0],[1,4],[3,0]]` | 216 |
| 9 | 5 | `[[1,1],[1,5],[3,8],[1,1],[1,5],[3,8]]` | 36 |
| 10 | 5 | `[[1,2],[1,6],[3,9],[1,2],[1,6],[3,9]]` | 6 |
| 11 | 5 | `[[10,2]]` | 1 |
| 12 | 0 | `[[1,3],[1,7],[3,10],[1,11],[1,7],[3,10]]` | 1 |

已从上表展开全部11111条actions并恢复源全部字段、键序和缩进，JSON重建逐字同原件：true。
