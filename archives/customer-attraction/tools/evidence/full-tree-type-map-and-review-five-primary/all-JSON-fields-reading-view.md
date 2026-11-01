# 全字段原记录阅读视图

只作JSON无损重排；未运行policy完成、收益、Gaussian秩、SCC或任何原审计。

779B实际输入

{
  "weights": [
    3,
    4,
    3,
    4,
    3,
    4,
    3
  ],
  "players": 4,
  "topics": 3,
  "policy": [
    1,
    1,
    0,
    0,
    1,
    2,
    1,
    2,
    2,
    0,
    1,
    0,
    1,
    2,
    2,
    1,
    2,
    2,
    1,
    1,
    2,
    1,
    2,
    2,
    2,
    2,
    2,
    0,
    2,
    0,
    0,
    1,
    2,
    1,
    1,
    0,
    0,
    1,
    0,
    1
  ],
  "scc_rank": 1,
  "lineality_rank": 2,
  "reverse_target": {
    "history": [
      0,
      0
    ],
    "action": 2
  },
  "reverse_certificate": [
    {
      "history": [
        1,
        0
      ],
      "action": 1,
      "multiplier": "2/5"
    },
    {
      "history": [
        0,
        0,
        0
      ],
      "action": 1,
      "multiplier": "4/5"
    }
  ]
}

2397B作者原报告

{
  "status": "exact_audit_passed",
  "example": {
    "histories": 40,
    "comparisons": 120,
    "minimum_slack": "0",
    "path": [
      1,
      0,
      2,
      2
    ],
    "payoffs": [
      "91/12",
      "25/4",
      "61/12",
      "61/12"
    ],
    "welfare": 24,
    "optimum": 24,
    "scc_image_rank": 1,
    "mapped_lineality_rank": 2,
    "zero_slack_row_rank": 2,
    "nontrivial_sccs": [
      [
        [
          [
            1,
            1,
            2
          ],
          2
        ],
        [
          [
            1,
            2,
            1
          ],
          1
        ]
      ]
    ],
    "reverse_relation": {
      "r": [
        "0",
        "1",
        "1/3",
        "-1",
        "-1/3",
        "0",
        "0"
      ],
      "s": [
        "0",
        "-1/2",
        "-1/3",
        "1/2",
        "1/3",
        "0",
        "0"
      ],
      "t": [
        "0",
        "-1",
        "-1/4",
        "1",
        "1/4",
        "0",
        "0"
      ],
      "identity": "r+(2/5)s+(4/5)t=0"
    }
  },
  "rank_boundaries": [
    {
      "players": 1,
      "topics": 1,
      "vertices": 1,
      "rank": 1,
      "difference_rank": 0
    },
    {
      "players": 1,
      "topics": 5,
      "vertices": 5,
      "rank": 5,
      "difference_rank": 4
    },
    {
      "players": 2,
      "topics": 1,
      "vertices": 1,
      "rank": 1,
      "difference_rank": 0
    },
    {
      "players": 7,
      "topics": 1,
      "vertices": 1,
      "rank": 1,
      "difference_rank": 0
    },
    {
      "players": 2,
      "topics": 2,
      "vertices": 4,
      "rank": 3,
      "difference_rank": 2
    },
    {
      "players": 3,
      "topics": 2,
      "vertices": 6,
      "rank": 3,
      "difference_rank": 2
    },
    {
      "players": 2,
      "topics": 4,
      "vertices": 16,
      "rank": 10,
      "difference_rank": 9
    },
    {
      "players": 3,
      "topics": 4,
      "vertices": 40,
      "rank": 14,
      "difference_rank": 13
    },
    {
      "players": 5,
      "topics": 3,
      "vertices": 45,
      "rank": 7,
      "difference_rank": 6
    },
    {
      "players": 3,
      "topics": 5,
      "vertices": 75,
      "rank": 25,
      "difference_rank": 24
    },
    {
      "players": 5,
      "topics": 5,
      "vertices": 350,
      "rank": 31,
      "difference_rank": 30
    }
  ]
}

935B独审原报告

{
  "status": "PASS",
  "histories": 40,
  "all_action_rows": 120,
  "nonself_rows": 80,
  "positive_mass": true,
  "zero_slack_rows": 50,
  "zero_slack_row_span_rank": 2,
  "r": [
    "0",
    "1",
    "1/3",
    "-1",
    "-1/3",
    "0",
    "0"
  ],
  "s": [
    "0",
    "-1/2",
    "-1/3",
    "1/2",
    "1/3",
    "0",
    "0"
  ],
  "t": [
    "0",
    "-1",
    "-1/4",
    "1",
    "1/4",
    "0",
    "0"
  ],
  "positive_relation": "r+(2/5)s+(4/5)t=0",
  "relation_span_rank": 2,
  "mapped_row_cone_lineality_rank": 2,
  "payoff_graph_vertices": 30,
  "payoff_graph_sccs": 29,
  "nontrivial_sccs": [
    [
      {
        "action": 1,
        "counts": [
          1,
          2,
          1
        ]
      },
      {
        "action": 2,
        "counts": [
          1,
          1,
          2
        ]
      }
    ]
  ],
  "scc_image_rank": 1,
  "actual_counts": [
    1,
    1,
    2
  ],
  "actual_welfare": 24
}
